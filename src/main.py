from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from azure.communication.email import EmailClient

from model.Sudoku import Sudoku

load_dotenv()
app = Flask(__name__)

@app.route("/sudokugame/cell", methods=["POST"])
def validar_cuadrante():
	jugada: dict = request.get_json()
	sudoku = Sudoku(jugada["tablero"])
	del jugada["tablero"]
	email = jugada["correo"]
	del jugada["correo"]
	
	# Si cada atributo de jugada está entre 1 y 9
	if all([attr in range(1, 10) for attr in jugada.values()]):
		fila = jugada["fila"] - 1
		col = jugada["columna"] - 1
		num = jugada["numero"]
		if sudoku.in_cell(fila, col, num):
			resuelto = sudoku.fill(fila, col, num)
			print(f"\n{sudoku}")
			if resuelto:
				notify({
					"to": email,
					"subject": "¡Felicidades!",
					"content": "¡Usted ha resuelto el sudoku!",
				}, sudoku)
				return jsonify({
					"message": "Sudoku resuelto.",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
			else:
				notify({
					"to": email,
					"subject": "¡Enhorabuena!",
					"content": "¡Su jugada ha sido válida! Véalo por usted mismo:",
				}, sudoku)
				return jsonify({
					"message": "Jugada válida.",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
		else:
			notify({
				"to": email,
				"subject": "Oh no...",
				"content": "Su jugada no fue válida. Asegúrese también de no haber escrito sobre los números ya dados.",
			}, sudoku)
			return jsonify({
				"message": "Jugada inválida."
			}), 400
	else:
		notify({
			"to": email,
			"subject": "Oh no...",
			"content": "Su jugada no fue válida. La fila, la columna y el número deben estar entre 1 y 9.",
		}, sudoku)
		return jsonify({
			"message": "Jugada inválida."
		}), 400

@app.route("/sudokugame/lines", methods=["POST"])
def validar_lineas():
	jugada: dict = request.get_json()
	sudoku = Sudoku()
	del jugada["tablero"]
	email = jugada["correo"]
	del jugada["correo"]
	
	# Si cada atributo de jugada está entre 1 y 9
	if all([attr in range(1, 10) for attr in jugada.values()]):
		fila = jugada["fila"] - 1
		col = jugada["columna"] - 1
		num = jugada["numero"]
		if not sudoku.in_col(col, num) and not sudoku.in_row(fila, num):
			resuelto = sudoku.fill(fila, col, num)
			print(f"\n{sudoku}")
			if resuelto:
				notify({
					"to": email,
					"subject": "¡Felicidades!",
					"content": "¡Usted ha resuelto el sudoku!",
				}, sudoku)
				return jsonify({
					"message": "Sudoku resuelto.",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
			else:
				notify({
					"to": email,
					"subject": "¡Enhorabuena!",
					"content": "¡Su jugada ha sido válida! Véalo por usted mismo:",
				}, sudoku)
				return jsonify({
					"message": "Jugada válida.",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
		else:
			notify({
				"to": email,
				"subject": "Oh no...",
				"content": "Su jugada no fue válida. Asegúrese también de no haber escrito sobre los números ya dados.",
			}, sudoku)
			return jsonify({
				"message": 	"Jugada inválida."
			}), 400
	else:
		notify({
			"to": email,
			"subject": "Oh no...",
			"content": "Su jugada no fue válida. La fila, la columna y el número deben estar entre 1 y 9.",
		}, sudoku)
		return jsonify({
			"message": "Jugada inválida."
		}), 400
	
def notify(mail_data: dict, sudoku: Sudoku):
	try:
		connection_string = os.environ.get("CONN_STRING")
		client = EmailClient.from_connection_string(connection_string)

		sudokuHtml = mail_data["content"] + '\n\n\n' + '<table border="1">'
		for row in range(0, 9):
			sudokuHtml += '<tr>'
			for col in range(0, 9):
				style = ''
				data = ''
				if sudoku.draft[row][col] not in [0, " "]:
					style = "color: teal;"
					data = sudoku.draft[row][col]
				elif sudoku.board[row][col] != 0:
					style = "background: teal; color: white;"
					data = sudoku.board[row][col]
				else:
					style = "background: lightgrey; color: lightgrey;"
					data = "?"
				sudokuHtml += (
					f'<td style="width: 1.5em; text-align: center; {style}"><b>{data}</b></td>'
				)
			sudokuHtml += '</tr>'
		sudokuHtml += '</table>'

		message = {
			"senderAddress": os.environ.get("SENDER_ADDR"),
			"recipients":  {
				"to": [{
					"address": mail_data["to"]
				}],
			},
			"content": {
				"subject": mail_data["subject"],
				"plainText": mail_data["content"],
				"html": sudokuHtml
			}
		}

		poller = client.begin_send(message)
		result = poller.result()
		print(result)
	except Exception as ex:
		print(ex)
	return jsonify({
		'message': 'E-mail sent successfully',
	}), 200

if __name__ == "__main__":
	app.run(debug = True)
