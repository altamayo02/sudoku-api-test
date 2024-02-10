from flask import Flask, request, jsonify
from model.Sudoku import Sudoku

app = Flask(__name__)
sudoku = Sudoku()
print(f"\n\nEl Sudoku a analizar es el siguiente: \n\n{sudoku}")

@app.route("/", methods=["GET"])
def get():
	return jsonify({"method": "get"}), 200

@app.route("/", methods=["POST"])
def post():
	return jsonify({"method": "post"}), 200

if __name__ == "__main__":
	app.run(debug = True)