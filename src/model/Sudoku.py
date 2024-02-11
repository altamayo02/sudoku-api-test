import requests

class Sudoku:
	def __init__(self) -> None:
		response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
		if response.status_code // 100 == 2:
			self.board = response.json()["newboard"]["grids"][0]["value"]
			self.draft = [[" " for _ in range(9)] for _ in range(9)]
			self.solution = response.json()["newboard"]["grids"][0]["solution"]
		else:
			raise Exception("Couldn't fetch sudoku from https://sudoku-api.vercel.app/api/dosuku")
	
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
		self.fill[row][col] = val

		# Verificar si faltan números para resolver el sudoku
		for i in range(self.board):
			for j in range(self.board[i]):
				if self.board[i][j] == 0 and self.fill[i][j] == " ":
					return False
		return True