from field import *
from enum import Enum

class Direction(Enum):
	Up = 	0
	Down = 	1
	Left = 	2
	Right = 3
	
	@staticmethod
	def get_random():
		return Direction(random.randint(0, Direction.__len__() - 1))

class Cell:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

class Snake:
	def __init__(self, field: Field):
		self.body = [Cell(field.get_random_x(), field.get_random_y())]
		self.apple = Cell(field.get_random_x(), field.get_random_y())
		self.direction = Direction.get_random()
		print(self.direction)

	def get_body(self):
		return self.body

	def draw_on(self, field: Field):
		for cell in self.body:
			field.data[cell.x][cell.y] = CellState.Snake

		field.data[self.apple.x][self.apple.y] = CellState.Apple