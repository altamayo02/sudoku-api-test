from flask import Flask, request, jsonify
from model.Sudoku import Sudoku

app = Flask(__name__)
sudoku = Sudoku()

@app.route("/sudokugame/cell", methods=["POST"])
def validar_cuadrante():
	jugada: dict = request.get_json()
	
	# Si cada atributo de jugada está entre 1 y 9
	if all([attr in range(1, 10) for attr in jugada.values()]):
		fila = jugada["fila"] - 1
		col = jugada["columna"] - 1
		num = jugada["numero"]
		if sudoku.in_cell(fila, col, num):
			resuelto = sudoku.fill(fila, col, num)
			print(f"\n{sudoku}")
			if resuelto:
				return jsonify({
					"message": "¡Ha rellenado el sudoku!",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
			else:
				return jsonify({
					"message": "¡La jugada es válida!",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
		else:
			return jsonify({
				"message": (
					"La jugada no es válida. " +
					"Asegúrese también de no escribir sobre los números ya dados."
				)
			}), 400
	else:
		return jsonify({
			"message": "La fila, la columna y el número deben estar entre 1 y 9."
		}), 400

@app.route("/sudokugame/lines", methods=["POST"])
def validar_lineas():
	jugada: dict = request.get_json()
	
	# Si cada atributo de jugada está entre 1 y 9
	if all([attr in range(1, 10) for attr in jugada.values()]):
		fila = jugada["fila"] - 1
		col = jugada["columna"] - 1
		num = jugada["numero"]
		if sudoku.in_col(fila, col, num) and sudoku.in_row(fila, col, num):
			resuelto = sudoku.fill(fila, col, num)
			print(f"\n{sudoku}")
			if resuelto:
				return jsonify({
					"message": "¡Ha rellenado el sudoku!",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
			else:
				return jsonify({
					"message": "¡La jugada es válida!",
					"board": sudoku.board,
					"draft": sudoku.draft
				}), 200
		else:
			return jsonify({
				"message": (
					"La jugada no es válida. " +
					"Asegúrese también de no escribir sobre los números ya dados."
				)
			}), 400
	else:
		return jsonify({
			"message": "La fila, la columna y el número deben estar entre 1 y 9."
		}), 400

if __name__ == "__main__":
	app.run(debug = True)