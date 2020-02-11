import tkinter as tk
from pacman import PacManGame
from keyboard_controller import KeyboardController


def run_game():
	root = tk.Tk()
	root.title('Pac-Man')
	game = PacManGame(KeyboardController(root), root)
	game.update()
	game.start()
	if game.status == 1:
		print('Pac-Man wins with score ' + str(game.agents[0].score) + '.')
	elif game.status == -1:
		print('Game over.')


if __name__ == '__main__':
	run_game()


# TODO:
#	- change 'cell' to 'node'