from flask import Flask, request, jsonify
from model.Sudoku import Sudoku

app = Flask(__name__)
sudoku = Sudoku()

@app.route("/sudokugame", methods=["GET"])
def ver_sudoku():
	print(f"\n{sudoku}")
	return jsonify({
		"board": sudoku.board
	}), 200

@app.route("/sudokugame", methods=["POST"])
def validar_jugada():
	jugada: dict = request.get_json()
	
	# Si cada atributo de jugada está entre 1 y 9
	if all([attr in range(1, 10) for attr in jugada.values()]):
		if sudoku.is_valid(jugada["fila"]-1, jugada["columna"]-1, jugada["numero"]):
			# Update sudoku
			return jsonify({
				"message": "¡La jugada es válida!",
				"board": sudoku.board
			}), 200
	else:
		return jsonify({
			"message": "La fila, la columna y el número deben estar entre 1 y 9.",
		}), 400

if __name__ == "__main__":
	app.run(debug = True)