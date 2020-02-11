from pacman_utils import Direction

class KeyboardController:
	def __init__(self, root, ):
		self.root = root
		self.direction = None
		self.bind_events()

	def bind_events(self):
		self.root.bind('<Right>', self.move_right)
		self.root.bind('<Left>', self.move_left)
		self.root.bind('<Up>', self.move_up)
		self.root.bind('<Down>', self.move_down)

	def move_right(self, event):
		self.direction = Direction.RIGHT.value

	def move_left(self, event):
		self.direction = Direction.LEFT.value

	def move_up(self, event):
		self.direction = Direction.UP.value

	def move_down(self, event):
		self.direction = Direction.DOWN.value

	def get_direction(self, current_direction, legal_directions):
		if self.direction in legal_directions:
			return self.direction
		elif current_direction in legal_directions:
			return current_direction
		else:
			return (0, 0)
