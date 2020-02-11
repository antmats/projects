from pacman_graphics import PacMan, Ghost, Food, PowerPellet, Wall
from ghost_behavior import *


class Maze:
	def __init__(self, layout='layout.txt'):
		self.n_rows = None
		self.n_columns = None
		self.walls = []
		self.cells = {}
		self.pacman = None
		self.ghosts = []
		self.n_dots_left = 0
		self.load_maze(layout)

	def load_maze(self, layout):
		with open(layout) as f:
			maze = [line.split() for line in f if line.strip()]
		self.n_rows, self.n_columns = len(maze), len(maze[0])
		for row, y in zip(maze, range(self.n_rows)):
			for cell, x in zip(row, range(self.n_columns)):
				position = x, y
				if cell[0] == '0':
					if cell[1] == '0':
						# The cell is empty (but Pac-Man or a ghost can be here)
						self.cells[position] = None
						if cell[2] == '1':
							# Pac-Man is here
							self.pacman = PacMan(position)
						elif cell[2] == '2':
							# A ghost with a random behavior is here
							self.ghosts.append(RandomGhost(position))
						elif cell[2] == '3':
							# A ghost that chases Pac-Man is here
							self.ghosts.append(ChaseGhost(position, self))
					elif cell[1] == '1':
						# The cell contains food
						self.cells[position] = Food(position)
						self.n_dots_left += 1
					elif cell[1] == '2':
						# The cell contains a power pellet
						self.cells[position] = PowerPellet(position)
				elif cell[0] == '1':
					# The cell contains a wall segment
					if cell[1] == '1' and cell[2] == '1':
						# The wall extends to the cell to the right and to the cell below
						extensions = [(x + 1, y), (x, y + 1)]
					elif cell[1] == '1' and cell[2] == '0':
						# The wall extends to the cell to the right
						extensions = [(x + 1, y)]
					elif cell[1] == '0' and cell[2] == '1':
						# The wall extends to the cell below
						extensions = [(x, y + 1)]
					elif cell[1] == '0' and cell[2] == '0':
						# There is no extension of the wall
						extensions = []
					self.walls.append(Wall(position, extensions))

	def get_items(self):
		return [self.pacman, *self.ghosts, *list(self.cells.values()), *self.walls]

if __name__ == '__main__':
	from graph import *
	from matplotlib import pyplot as plt
	maze = Maze()
	fig, ax = plt.subplots()
	for i in maze.cells:
		ax.plot(i[0], i[1], 'k*')
	ax.plot(11, 6, 'ro')
	ax.plot(10, 10, 'ro')
	ax.invert_yaxis()
	# graph = Graph(maze.cells)
	# for i in graph.shortest_path((11, 16), (10, 10)):
	# 	ax.plot(i[0], i[1], 'ro')
	plt.show()
