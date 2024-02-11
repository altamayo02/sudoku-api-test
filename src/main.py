from flask import Flask, request, jsonify
from model.Sudoku import Sudoku

app = Flask(__name__)
sudoku = Sudoku()


@app.route("/sudokugame", methods=["GET"])
def ver_sudoku():
	print(f"\n{sudoku}")
	return jsonify({
		"board": sudoku.board,
		"draft": sudoku.draft
	}), 200

@app.route("/sudokugame", methods=["POST"])
def validar_jugada():
	jugada: dict = request.get_json()
	
	# Si cada atributo de jugada está entre 1 y 9
	if all([attr in range(1, 10) for attr in jugada.values()]):
		fila = jugada["fila"] - 1
		col = jugada["columna"] - 1
		num = jugada["numero"]
		if sudoku.is_valid(fila, col, num):
			resuelto = sudoku.draft(fila, col, num)
			print(f"\n{sudoku}")
			if resuelto:
				return jsonify({
					"message": "¡Ha resuelto el sudoku!",
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