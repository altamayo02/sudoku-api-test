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
	jugada = request.get_json()
	
	if sudoku.is_valid(jugada["fila"], jugada["columna"], jugada["numero"]):
		# Update sudoku
		return jsonify({
			"message": "¡La jugada es válida!",
			"board": sudoku.board
		}), 200

if __name__ == "__main__":
	app.run(debug = True)