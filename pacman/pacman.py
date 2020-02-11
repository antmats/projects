from math import ceil
from maze import Maze
from pacman_graphics import PacManGraphics, Food, PowerPellet
from pacman_utils import *


UPDATE_AFTER = 200
PACMAN_SPEED = 1.0  # cell per time interval
TIME_PENALTY = 1
FOOD_POINTS = 10
EAT_GHOST_POINTS = 200
GHOST_SPEED = 1.0  # cell per time interval
SCARED_GHOST_SPEED = 0.125  # cell per time interval
SCARED_GHOST_TIME = 40


class PacManGame:
	global EAT_GHOST_POINTS

	def __init__(self, pacman_controller, root=None):
		self.maze = Maze()
		if root is not None:
			self.display_graphics = True
			self.graphics = PacManGraphics(root, self.maze)
		else:
			self.display_graphics = False
		self.agents = [PacManAgent(pacman_controller, self.maze), *[GhostAgent(ghost, self.maze) for ghost in self.maze.ghosts]]
		self.timer = -1
		self.status = 0  # -1: Pac-Man loses, 0: game is running, 1: Pac-Man wins

	def update_agents(self):
		# Check for a collision between Pac-Man and any of the ghosts
		self.agent_collision()
		
		# Check the status of the game
		if self.status == 1 or self.status == -1:
			# The game is over
			return

		# Update Pac-Man
		if self.agents[0].update():
			if self.timer < 0:
				self.timer = SCARED_GHOST_TIME
			else:
				self.timer += SCARED_GHOST_TIME
			for ghost in self.agents[1:]: 
				ghost.is_scared = True
				if self.display_graphics: ghost.agent.change_color('blue')
		self.timer -= 1
		if self.timer == 0:
			for ghost in self.agents[1:]:
				ghost.is_scared = False
				if self.display_graphics: ghost.agent.change_color(ghost.agent.color)
		if self.maze.n_dots_left == 0: self.status = 1

		# Update the ghosts
		for ghost in self.agents[1:]:
			if self.timer == 0 and ghost.agent.position not in self.maze.cells:
				# The ghost just became dangerous again. If it is between two cells, it should be moved to the next cell
				ghost.move_to_next_cell()
			else:
				ghost.update()

	def agent_collision(self):
		for ghost in self.agents[1:]:
			if self.interaction(ghost):
				if ghost.is_scared:
					ghost.agent.move_to_cave()
					ghost.agent.change_color(ghost.agent.color)
					ghost.is_scared = False
					self.agents[0].score += EAT_GHOST_POINTS
				else:
					self.status = -1

	def interaction(self, ghost):
		pacman_position = self.agents[0].agent.position
		ghost_position = ghost.agent.position
		manhattan_distance = get_manhattan_distance(pacman_position, ghost_position)
		if manhattan_distance < 1:
			return True
		pacman_direction = self.agents[0].direction
		ghost_direction = ghost.direction 
		if manhattan_distance == 1 and pacman_direction == get_reverse_direction(ghost_direction):
			# We must check if the ghost and the Pac-Man just passed each other
			if pacman_position == add(ghost_position, get_reverse_direction(ghost_direction)):
				return True
		return False

	def start(self):
		if self.display_graphics: self.graphics.start()
		self.update()

	def update(self):
		if self.display_graphics:
			self.update_agents()
			if self.status == 1 or self.status == -1:
				self.graphics.quit()
				return
			self.graphics.update_scoreboard(self.agents[0].score)
			self.graphics.canvas.canvas.after(UPDATE_AFTER, self.update)
		else:
			pass


class PacManAgent:
	global PACMAN_SPEED, TIME_PENALTY, FOOD_POINTS

	speed = PACMAN_SPEED

	def __init__(self, controller, maze):
		self.controller = controller
		self.maze = maze
		self.agent = maze.pacman
		self.cells = maze.cells
		self.direction = None
		self.score = 0

	# def set_direction(self, direction):
	# 	if direction.value in self.get_legal_directions():
	# 		self.direction = direction.value

	def update(self):
		self.update_position()
		self.score -= TIME_PENALTY
		# Check if Pac-Man has reached a cell that contains food or a power pellet
		cell = self.cells[self.agent.position]
		if isinstance(cell, Food) and cell.item is not None:
			cell.delete_item()
			self.maze.n_dots_left -= 1
			self.score += FOOD_POINTS
		if isinstance(cell, PowerPellet) and cell.item is not None:
			cell.delete_item()
			return True
		return False

	def update_position(self):
		self.direction = self.controller.get_direction(self.direction, self.get_legal_directions())
		displacement = tuple(x * self.speed for x in self.direction)
		self.agent.move_item(displacement)

	def get_legal_directions(self):
		return [d.value for d in Direction if add(d.value, self.agent.position) in self.cells]


class GhostAgent:
	global GHOST_SPEED, SCARED_GHOST_SPEED

	def __init__(self, ghost, maze):
		self.agent = ghost
		self.cells = maze.cells
		self.direction = None
		self.speed = GHOST_SPEED
		self.is_scared = False

	def update(self):
		self.speed = SCARED_GHOST_SPEED if self.is_scared else GHOST_SPEED
		self.update_position()

	def update_position(self):
		if self.is_scared and self.agent.position not in self.cells:
			# Let the direction be unchanged when the ghost is between cells
			pass
		else:
			self.direction = self.agent.get_direction(self.get_legal_directions())
		displacement = tuple(x * self.speed for x in self.direction)
		self.agent.move_item(displacement)

	def move_to_next_cell(self):
		current_position = self.agent.position
		if self.direction == Direction.RIGHT.value or self.direction == Direction.DOWN.value:
			new_poisition = tuple(ceil(x) for x in current_position)
		else:
			new_poisition = tuple(int(x) for x in current_position)
		displacement = subtract(new_poisition, current_position)
		self.agent.move_item(displacement)

	def get_legal_directions(self):
		legal_directions = [d.value for d in Direction if add(d.value, self.agent.position) in self.cells]
		if self.direction is None: return legal_directions
		reverse_direction = get_reverse_direction(self.direction)
		# Ghosts cannot turn around
		if reverse_direction in legal_directions: legal_directions.remove(reverse_direction)
		if legal_directions:
				return legal_directions
		else:
			# ... unless they get stuck in a dead end
			return [reverse_direction]


def get_manhattan_distance(xy1, xy2):
	return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
