import random
import copy
from graph import Graph
from pacman_utils import *
from pacman_graphics import Ghost


class RandomGhost(Ghost):
	color = 'orange'
	
	def __init__(self, position):	
		Ghost.__init__(self, position, self.color)
	
	def get_direction(self, legal_directions):
		i = random.randint(0, len(legal_directions) - 1)
		return legal_directions[i]
	
	def get_color(self):
		return self.color


class ChaseGhost(Ghost):
	color = 'red'

	def __init__(self, position, maze):
		Ghost.__init__(self, position, self.color)
		self.graph = None
		self.maze = maze

	def get_direction(self, legal_directions):  # The ghosts are updated after Pac-Man in the class PacManGame
		if self.graph is None: self.graph = Graph(self.maze.cells)
		graph_copy = copy.deepcopy(self.graph)
		if self.direction is not None:
			# Since the ghost cannot turn around, the node "behind" the ghost is deleted
			graph_copy.delete_node(add(self.position, get_reverse_direction(self.direction)))
		if self.maze.pacman.direction is None or self.maze.pacman.direction == (0, 0) or True:
			# Pac-Man does not move at the moment. Let the ghost aim at the cell where Pac-Man is.
			next_cell = graph_copy.shortest_path(self.position, self.maze.pacman.position)[1]
			return subtract(next_cell, self.position)
		else:
			# Pac-Man is moving. Aim at one cell behind Pac-Man
			pass
		return None

	def get_color(self):
		return self.color


class AheadGhost:
	color = 'blue'
	pass


class FickleGhost:
	color = 'pink'
	pass
