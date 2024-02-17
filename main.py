import json

from flask import Flask, request, jsonify
app = Flask(__name__)


def revisarsudoku(data):

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




@app.route('/sudoku', methods=['POST'])
def recibir():
    sudoku= request.get_json()
    return revisarsudoku(sudoku)


"""
def crear():
    temp=request.get_json()x
    usuarios.append(temp)
    respuesta={
        "Hola": f"van {len(usuarios)} usuarios"
    }
    return jsonify(respuesta)


@app.route('/users', methods=['GET'])
def mostrar():
    return jsonify(usuarios),200


@app.route('/users/<int:cc>', methods=['GET'])
def buscar(cc):
    print("dsf")
    for a in usuarios:
        if a["cc"] == cc:
            return jsonify(a)
    return jsonify({"Mensaje": "No se encontró el usuario"})

"""
if __name__=='__main__':
    app.run(debug=True)