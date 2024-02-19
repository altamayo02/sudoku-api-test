import requests

class Sudoku:
	def __init__(self, board = None) -> None:
		self.board = [[" " for _ in range(9)] for _ in range(9)]
		self.draft = self.board.copy()
		if board:
			# Iterate quadrant rows
			for quad_row in range(0, 3):
				# Iterate quadrant columns
				for quad_col in range(0, 3):
					# Iterate rows
					for row in range(0, 3):
						# Iterate values
						for col in range(0, 3):
							self.board[3 * quad_row + row][3 * quad_col + col] = (
								board[quad_row]["columnas"][quad_col][row][col]
							)
			self.solution = None
		else:
			response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
			if response.status_code // 100 == 2:
				self.board = response.json()["newboard"]["grids"][0]["value"]
				self.solution = response.json()["newboard"]["grids"][0]["solution"]
			else:
				raise Exception("Couldn't fetch sudoku from https://sudoku-api.vercel.app/api/dosuku")
			
	# Retorna una representación del sudoku en ASCII
	def __str__(self) -> str:
		string = "- " + "- - - - " * 3 + "\n"
		for row in range(len(self.board)):
			string += "| "
			for col in range(len(self.board[row])):
				if self.board[row][col] != 0:
					string += f'\u001B[34m{self.board[row][col]}\u001B[0m '
				else:
					string += f'\u001B[33m{self.draft[row][col]}\u001B[0m '
				if (col + 1) % 3 == 0:
					string += "| "
			string += "\n"
			if (row + 1) % 3 == 0:
				string += "- " + "- - - - " * 3 + "\n"
		return string
	
	def is_valid(self, row, col, val) -> bool:
		return (
			self.is_writable(row, col) and
			not self.in_row(row, val) and
			not self.in_col(col, val) and
			not self.in_cell(row, col, val)
		)
	
	def is_writable(self, row, col) -> bool:
		return self.board[row][col] == 0
	
	def in_row(self, row, val) -> bool:
		return val in self.board[row]

	def in_col(self, col, val) -> bool:
		for row in range(len(self.board)):
			if self.board[row][col] == val:
				return True
		return False

	def in_cell(self, row, col, val) -> bool:
		i0 = 3 * (row // 3)
		j0 = 3 * (col // 3)
		for i in range(i0, i0 + 3):
			for j in range(j0, j0 + 3):
				if val == self.board[i][j]: return True
		return False
	
	def fill(self, row, col, val) -> None:
		self.draft[row][col] = val
		if not self.solution:
			return False

		# Verificar si faltan números para resolver el sudoku
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if (
					self.board[i][j] != self.solution[i][j] and
					self.draft[i][j] != self.solution[i][j]
				):
					return False
		return True

	def desestructurar(self, data):
		filas = []
		subcolumnas = []


		"""aquí todo queda guardado en 3 filas, cada una con tres filas de la matriz sin ordenarse"""

		# recorro las filas de cuadrantes
		for cuad_fila in range(0, 3):
			# recorro las columnas de cuadrantes
			for cuad_col in range(0, 3):
				# recorro las columnas
				for fila in range(0, 3):
					# recorro las subfilas
					for valor in range(0, 3):
						subcolumnas.append(data[cuad_fila]["columnas"][cuad_col][fila][valor])
			filas.append(subcolumnas)
			subcolumnas = []

		"""aquí todo el sudoku queda guardado en 9 filas"""

		matrix = []
		for temp in filas:

			# almacenamos las filas que hay dentro de las tres filas principales
			matrixTemp = [[], [], []]

			# b es un iterador entre 0,1,2
			b = 0
			for valor in temp:

				if b == 0:
					matrixTemp[0].append(valor)
					b += 1

				elif b == 1:
					matrixTemp[1].append(valor)
					b += 1

				else:
					matrixTemp[2].append(valor)
					b = 0

			for subfila in matrixTemp:
				matrix.append(subfila)

		self.board = matrix

	def in_cell2(self, argumentos):

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
