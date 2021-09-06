from enum import Enum
import random
from helper import Vec4

class CellState(Enum):
	Empty = 0
	Snake = 1
	Apple = 2

class Field:
	colors = {
		CellState.Empty: Vec4(0, 0, 0, 0),
		CellState.Snake: Vec4(1, 0, 0, 1),
		CellState.Apple: Vec4(1, 1, 0, 1),
	}

	def __init__(self, width, height):
		self.data = []
		self.width = width
		self.height = height

		for x in range(width):
			column = []
			for y in range(height):
				column.append(CellState.Empty)
			self.data.append(column)

	def get_random_x(self):
		return random.randint(0, self.get_width() - 1)

	def get_random_y(self):
		return random.randint(0, self.get_height() - 1)

	def get_color_of(self, x, y):
		state = self.data[x][y]
		return Field.colors[state]

	def clear(self):
		for x in range(len(self.data)):
			for y in range(len(self.data[x])):
				self.data[x][y] = CellState.Empty

	def get_width(self):
		return len(self.data)

	def get_height(self):
		return len(self.data[0])

	def get_width_range(self):
		return range(self.get_width())

	def get_height_range(self):
		return range(self.get_height())