import json

from flask import Flask, request, jsonify
app = Flask(__name__)


def desestructurar(data):

    filas=[]
    subcolumnas=[]

    """aquí todo queda guardado en 3 filas, cada una con tres filas de la matriz sin ordenarse"""

    #recorro las filas
    for i in range(0,3):
        #recorro las subcolumnas
        for j in range(0,3):
            #recorro las columnas
            for k in range(0,3):
                #recorro las subfilas
                for a in range(0,3):
                    subcolumnas.append(data[i]["columnas"][j][k][a])
        filas.append(subcolumnas)
        subcolumnas=[]

    """aquí todo el sudoku queda guardado en 9 filas"""

    matrix = []
    for temp in filas:

        # almacenamos las filas que hay dentro de las tres filas principales
        matrixTemp = [[], [], []]

        # b es un iterador entre 0,1,2
        b = 0
        for a in temp:

            if b == 0:
                matrixTemp[0].append(a)
                b += 1

            elif b == 1:
                matrixTemp[1].append(a)
                b += 1

            else:
                matrixTemp[2].append(a)
                b = 0

        for subfila in matrixTemp:
            matrix.append(subfila)

    return "matrix"


    def estructurar(matrix):
        for i in matrix:
            if

@app.route('/sudoku', methods=['POST'])
def recibir():x
    sudoku = request.get_json()
    return desestructurar(sudoku)


if __name__=='__main__':
    app.run(debug=True)