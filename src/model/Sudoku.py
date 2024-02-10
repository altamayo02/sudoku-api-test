import requests

class Sudoku:
	def __init__(self) -> None:
		response = requests.get("https://sudoku-api.vercel.app/api/dosuku")
		if response.status_code // 100 == 2:
			self.board = response.json()["newboard"]["grids"][0]["value"]
			self.solution = response.json()["newboard"]["grids"][0]["solution"]
		else:
			raise Exception("Couldn't fetch sudoku from https://sudoku-api.vercel.app/api/dosuku")
	
	def __str__(self) -> str:
		string = "- " + "- - - - " * 3 + "\n"
		for row in range(len(self.board)):
			string += "| "
			for col in range(len(self.board[row])):
				string += f"{' ' if self.board[row][col] == 0 else self.board[row][col]} "
				if (col + 1) % 3 == 0:
					string += "| "
			string += "\n"
			if (row + 1) % 3 == 0:
				string += "- " + "- - - - " * 3 + "\n"
		return string
	
	def is_valid(self, row, col, val) -> bool:
		return not (
			self.in_row(row, val) or
			self.in_col(col, val) or
			self.in_cell(row, col, val)
		)
	
	def in_row(self, row, val) -> bool:
		return val in self.board[row]

	def in_col(self, col, val) -> bool:
		for row in range(len(self.board)):
			if self.board[row][col] == val:
				return True
		return False

	def in_cell(self, row, col, val) -> bool:
		pass