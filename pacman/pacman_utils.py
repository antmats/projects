from enum import Enum
from operator import sub


class Direction(Enum):
	RIGHT = (1, 0)
	LEFT = (-1, 0)
	UP = (0, -1)
	DOWN = (0, 1)


def get_reverse_direction(direction):
	return tuple(-x for x in direction)


def add(t1, t2):
	return tuple(map(sum, zip(t1, t2)))	


def subtract(t1, t2):
	return tuple(map(sub, t1, t2))


if __name__ == '__main__':
	t1 = (1, 0)
	t2 = (1, 0)
	print(subtract(t1, t2))