class Sudoku:
    def __init__(self):
        self.board = None

    def desestructurar(self, data):

        filas = []
        subcolumnas = []

        """aquí todo queda guardado en 3 filas, cada una con tres filas de la matriz sin ordenarse"""

        # recorro las filas
        for i in range(0, 3):
            # recorro las subcolumnas
            for j in range(0, 3):
                # recorro las columnas
                for k in range(0, 3):
                    # recorro las subfilas
                    for a in range(0, 3):
                        subcolumnas.append(data[i]["columnas"][j][k][a])
            filas.append(subcolumnas)
            subcolumnas = []

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

        self.board = matrix

    def in_cell(self, argumentos):

        valores = list(argumentos.values())

        """encontramos las filas y columnas de su celda"""
        for a in range(0, 2):
            if (valores[2] + a) % 3 == 0:
                if a != 0:
                    filaInicio = (valores[2] + a) - 3
                else:
                    filaInicio = valores[2]

        for a in range(0, 2):
            if (valores[3] + a) % 3 == 0:
                if a != 0:
                    columnaInicio = (valores[3] + a) - 3
                else:
                    columnaInicio = valores[3]

        """revisamos si no está ya el numero, de estarlo enviamos un True"""
        for a in range(filaInicio, filaInicio + 3):
            for i in range(columnaInicio, columnaInicio + 3):
                if valores[1] == self.board[a][i]:
                    return True
        return False