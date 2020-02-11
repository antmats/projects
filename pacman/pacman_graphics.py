import tkinter as tk
import numpy as np
from pacman_utils import add


class PacManGraphics:
	def __init__(self, root, maze, width=640, height=480):
		self.root = root
		self.maze = maze
		self.canvas = None
		self.width = width
		self.height = height
		self.scoreboard = None
		self.draw_graphics()
		
	def draw_graphics(self):
		canvas = tk.Canvas(self.root, width=self.width, height=self.height)
		dx = self.width / (self.maze.n_columns - 1)
		dy = self.height / (self.maze.n_rows - 1)
		self.canvas = Canvas(canvas, dx, dy)
		canvas.pack()
		self.add_background()
		self.draw_maze()
		self.create_scoreboard()

	def add_background(self, color='black'):
		self.canvas.canvas.create_rectangle(0, 0, self.width, self.height, outline=color, fill=color)

	def draw_maze(self):
		for item in self.maze.get_items():
			if item is not None: item.draw_item(self.canvas)

	def create_scoreboard(self):
		x = self.canvas.dx
		y = self.height - self.canvas.dy
		self.scoreboard = self.canvas.canvas.create_text(x, y, fill='white', anchor='w', text='Score: 0')

	def update_scoreboard(self, score):
		self.canvas.canvas.itemconfigure(self.scoreboard, text='Score: ' + str(score))

	def start(self):
		self.root.mainloop()

	def quit(self):
		self.canvas.canvas.destroy()
		self.root.quit()


class Canvas:
	def __init__(self, canvas, dx, dy):
		self.canvas = canvas
		self.dx = dx
		self.dy = dy


class PacMan:
	color = 'yellow'
	r = 0.5

	def __init__(self, position):
		self.position = position
		self.canvas = None
		self.item = None
		self.direction = None

	def draw_item(self, canvas):
		self.canvas = canvas
		canvas_coordinates = get_canvas_coordinates(canvas, self.position)
		radius = self.r * min(canvas.dx, canvas.dy)
		self.item = create_circle(canvas.canvas, canvas_coordinates, radius, self.color)

	def move_item(self, displacement):
		self.direction = tuple(np.sign(x) for x in displacement)  # This attribute is needed for class ChaseGhost
		self.position = add(self.position, displacement)
		self.canvas.canvas.move(self.item, *get_canvas_displacement(self.canvas, displacement))


class Ghost:
	def __init__(self, position, color):
		self.position = self.intial_position = position
		self.color = color
		self.item = None
		self.direction = None

	def draw_item(self, canvas):
		self.item = GhostItem(self.position, canvas, self.color)

	def move_item(self, displacement):
		self.direction = tuple(np.sign(x) for x in displacement)  # This attribute is needed for class ChaseGhost
		self.position = add(self.position, displacement)
		self.item.move_item(displacement)

	def move_to_cave(self):
		self.position = self.intial_position
		self.item.move_to_initial_position(self.position)

	def change_color(self, color):
		self.item.set_color(color)


class GhostItem:
	width = 0.9
	height = 0.9
	eye_radius = 4
	pupil_radius = 2
	scared_color = 'blue'

	def __init__(self, position, canvas, color):
		self.canvas = canvas
		self.color = color
		self.body = self.draw_body(position)
		self.eyes = self.draw_eyes(position)

	def draw_body(self, position):
		width = self.width * min(self.canvas.dx, self.canvas.dy)
		height = self.height * min(self.canvas.dx, self.canvas.dy)
		return create_rectange(self.canvas.canvas, get_canvas_coordinates(self.canvas, position), width, height, self.color)

	def draw_eyes(self, position):
		canvas_coordinates = get_canvas_coordinates(self.canvas, position)
		left_eye_position = canvas_coordinates[0] - 0.2 * self.canvas.dx, canvas_coordinates[1] - 0.15 * self.canvas.dy
		right_eye_position = canvas_coordinates[0] + 0.2 * self.canvas.dx, canvas_coordinates[1] - 0.15 * self.canvas.dy
		# eye_radius = self.eye_radius * min(self.canvas.dx, self.canvas.dy)
		# pupil_radius = self.pupil_radius * min(self.canvas.dx, self.canvas.dy)
		left_eye = create_circle(self.canvas.canvas, left_eye_position, self.eye_radius, 'white')
		left_pupil = create_circle(self.canvas.canvas, left_eye_position, self.pupil_radius, 'black')
		right_eye = create_circle(self.canvas.canvas, right_eye_position, self.eye_radius, 'white')
		right_pupil = create_circle(self.canvas.canvas, right_eye_position, self.pupil_radius, 'black')
		return left_eye, right_eye, left_pupil, right_pupil

	def set_color(self, color):
		self.color = color
		self.canvas.canvas.itemconfigure(self.body, outline=color, fill=color)

	def move_item(self, displacement):
		canvas_displacement = get_canvas_displacement(self.canvas, displacement)
		for i in [self.body, *self.eyes]:
			self.canvas.canvas.move(i, *canvas_displacement)
			self.canvas.canvas.lift(i)

	def move_to_initial_position(self, position):
		for i in [self.body, *self.eyes]:
			self.canvas.canvas.delete(i)
		self.body = self.draw_body(position)
		self.eyes = self.draw_eyes(position)


class Wall:
	color = 'blue'
	width = 10

	def __init__(self, position, extensions):
		self.position = position
		self.extensions = extensions

	def draw_item(self, canvas):
		# width = self.width * min(canvas.dx, canvas.dy)
		x0, y0 = get_canvas_coordinates(canvas, self.position)
		for position in self.extensions:
			x1, y1 = get_canvas_coordinates(canvas, position)
			if y0 == y1:
				# The wall segment is horizontal
				start = x0 - self.width / 2, y0
				stop = x1 + self.width / 2, y1
			else:
				# The wall segment is vertical
				start = x0, y0 - self.width / 2
				stop = x1, y1 + self.width / 2
			canvas.canvas.create_line(start, stop, fill=self.color, width=self.width)


class Food:
	color = 'white'
	r = 0.1

	def __init__(self, position):
		self.position = position
		self.canvas = None
		self.item = None

	def draw_item(self, canvas):
		self.canvas = canvas
		canvas_coordinates = get_canvas_coordinates(canvas, self.position)
		radius = self.r * min(canvas.dx, canvas.dy)
		self.item = create_circle(canvas.canvas, canvas_coordinates, radius, self.color)

	def delete_item(self):
		self.canvas.canvas.delete(self.item)
		self.item = None


class PowerPellet:
	color = 'white'
	r = 0.2

	def __init__(self, position):
		self.position = position
		self.canvas = None
		self.item = None

	def draw_item(self, canvas):
		self.canvas = canvas
		canvas_coordinates = get_canvas_coordinates(canvas, self.position)
		radius = self.r * min(canvas.dx, canvas.dy)
		self.item = create_circle(canvas.canvas, canvas_coordinates, radius, self.color)

	def delete_item(self):
		self.canvas.canvas.delete(self.item)
		self.item = None


def get_canvas_displacement(canvas, displacement):
	return displacement[0] * canvas.dx, displacement[1] * canvas.dy


def get_canvas_coordinates(canvas, position):
	x, y = position
	return x * canvas.dx, y * canvas.dy


def create_circle(canvas, center_coordinates, r, outline_color, fill_color=None):
	x, y = center_coordinates
	x0, x1 = x - r - 1, x + r
	y0, y1 = y - r - 1, y + r
	if fill_color == None: 
		fill_color = outline_color
	return canvas.create_oval(x0, y0, x1, y1, outline=outline_color, fill=fill_color)


def create_rectange(canvas, center_coordinates, width, height, outline_color, fill_color=None):
	if fill_color == None: 
		fill_color = outline_color
	return canvas.create_rectangle(get_coorner_coordinates(center_coordinates, width, height), outline=outline_color, fill=fill_color)


def get_coorner_coordinates(center_coordinates, width, height):
	x, y = center_coordinates
	x0, y0 = x - width / 2, y + height / 2
	x1, y1 = x + width / 2, y - height / 2
	return x0, y0, x1, y1
