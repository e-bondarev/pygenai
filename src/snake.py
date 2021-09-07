import glfw

from field 	import *
from enum 	import Enum
from window import Input

class Direction(Enum):
	Up = 	0
	Down = 	1
	Left = 	2
	Right = 3
	
	@staticmethod
	def get_random():
		return Direction(randint(0, Direction.__len__() - 1))

class Vec2:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		self.last_x = x
		self.last_y = y

Cell = Vec2

directions = {
	Direction.Up: 		Vec2(0, -1),
	Direction.Down: 	Vec2(0, 1),
	Direction.Left: 	Vec2(-1, 0),
	Direction.Right: 	Vec2(1, 0)
}

class Snake:
	def __init__(self, field: Field):
		self.body = [Cell(field.get_random_x(), field.get_random_y())]
		self.apple = Cell(field.get_random_x(), field.get_random_y())
		self.direction = Direction.get_random()
		self.alive = True

	def get_body(self):
		return self.body

	def draw_on(self, field: Field):
		field.data[self.apple.x][self.apple.y] = CellState.Apple
		for cell in self.body:
			field.data[cell.x][cell.y] = CellState.Snake

	def control(self):
		if Input.key_is(glfw.KEY_W, Input.State.Pressed):
			self.direction = Direction.Up
		if Input.key_is(glfw.KEY_S, Input.State.Pressed):
			self.direction = Direction.Down
		if Input.key_is(glfw.KEY_A, Input.State.Pressed):
			self.direction = Direction.Left
		if Input.key_is(glfw.KEY_D, Input.State.Pressed):
			self.direction = Direction.Right

	def update(self, field: Field):
		if not self.alive:
			return

		for cell in self.body:
			cell.last_x = cell.x
			cell.last_y = cell.y

		dir = directions[self.direction]
		
		if not field.in_bounds(self.body[0].x + dir.x, self.body[0].y + dir.y):
			self.alive = False
			return

		if self.eats_apple():
			self.body.append(Cell(self.body[0].x, self.body[0].y))
			self.apple.x = field.get_random_x()
			self.apple.y = field.get_random_y()

		i = 0
		for cell in self.body:
			if i > 0:
				self.body[i].x = self.body[i - 1].last_x
				self.body[i].y = self.body[i - 1].last_y
			i += 1
			
		self.body[0].x += dir.x
		self.body[0].y += dir.y

	def eats_apple(self):
		return self.apple.x == self.body[0].x and self.apple.y == self.body[0].y
