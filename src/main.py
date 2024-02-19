import json

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/sudoku', methods=['POST'])
def recibir():

    sudoku = Sudoku()
    respuesta = request.get_json()

    sudoku.desestructurar(respuesta["sudoku"])
    return sudoku.in_cell(respuesta)


if __name__=='__main__':
    app.run(debug=True)