"""This class describes the Player.

The player object, of which there is one, is controlled by the user. 
The player's starting attributes are described in rpg.py and are given in a list format.
"""

class Player:

	def __init__(self):

		self.local_position = (0,0)
		self.global_position = (0,0)

		self.health = 25

	def move(self, direction, tiles):
		#Direction 0-3
		y_dir = 0
		x_dir = 0
		if direction == 0:
			y_dir = tiles
		elif direction == 1:
			y_dir = -tiles
		elif direction == 2:
			x_dir = tiles
		elif direction == 3:
			x_dir = -tiles

		x,y = self.local_position
		x += x_dir
		y += y_dir
		self.local_position = (x,y)