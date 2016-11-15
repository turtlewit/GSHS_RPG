from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.components.world import Tile, World
from AdventureEngine.CoreEngine.input import Input
from src.createmap import CreateMap
import os
import pygame.mixer
import curses

class Player(GameComponent):

	def __init__(self):
		GameComponent.__init__(self)

		self.m_name = "player"
		self.currentTile = None
		self.oldTile = Tile()

		self.world = None
		self.oldWorld = World()

		self.printDescription = True

		self.mapText = None

		self.thingToPrint = []
		self.m_spaceTransform = (0,0)
		self.playMusic = True
		try:
			pygame.mixer.init()
		except:
			self.playMusic = False
		self.worldDifference=None

	def Move(self, direction):
		x = 0
		y = 0
		if direction in ['n', 'north']:
			if self.currentTile.move_north_message:
				self.thingToPrint.append(self.currentTile.move_north_message)
			else:
				y = 1
		elif direction in ['s', 'south']:
			if self.currentTile.move_south_message:
				self.thingToPrint.append(self.currentTile.move_south_message)
			else:
				y = -1
		elif direction in ['e', 'east']:
			if self.currentTile.move_east_message:
				self.thingToPrint.append(self.currentTile.move_east_message)
			else:
				x = 1
		elif direction in ['w', 'west']:
			if self.currentTile.move_west_message:
				self.thingToPrint.append(self.currentTile.move_west_message)
			else:
				x = -1

		self.m_parent.m_transform = (self.m_parent.m_transform[0] + x, self.m_parent.m_transform[1] + y)
		self.mapText = CreateMap.Create(self.currentTile.m_parent.m_parent, self)

	def Update(self):

		if Input().command:
			self.thingToPrint = []
			self.printDescription = True
			self.m_parent.m_renderer.useLineConvert = True

			if type(Input().command) is not str:
				if Input().command in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
					directiondict = {curses.KEY_UP: 'n', curses.KEY_DOWN: 's', curses.KEY_LEFT: 'w', curses.KEY_RIGHT: 'e'}
					self.Move(directiondict[Input().command])
			else:
				if len(Input().command.lower().split()) > 0:

					if Input().command.lower().split()[0] in ['move', 'go', 'walk', 'n', 's', 'e', 'w']:
						try:
							direction = Input().command.lower().split()[1]
						except:
							try:
								direction = Input().command.lower().split()[0]
							except:
								direction = None

						if direction:
							self.Move(direction)
				


				if Input().command.lower() in ['map']:
					self.printDescription = False
					self.thingToPrint.append(self.mapText)
					self.m_parent.m_renderer.useLineConvert = False

				elif Input().command.lower() in ['down']:
					self.m_spaceTransform = (self.m_spaceTransform[0], self.m_spaceTransform[1] + 1)
					self.m_parent.m_transform = (0,0)

				elif Input().command.lower() in ['up']:
					self.m_spaceTransform = (self.m_spaceTransform[0], self.m_spaceTransform[1] - 1)
					self.m_parent.m_transform = (0,0)

				elif Input().command.lower() in ['quit', 'exit']:
					self.m_parent.m_engine.m_isRunning = False

		


		for child1 in self.m_parent.m_engine.m_game.m_root.m_children:
			if child1.m_transform == self.m_spaceTransform and child1.m_components[0].m_type == "world":
				for child2 in child1.m_children:
					if child2.m_transform == self.m_parent.m_transform and child2.m_components[0].m_type == "tile":
						self.currentTile = child2.m_components[0]
					else:
						#self.thingToPrint.append(child2.m_components[0].m_name)
						pass

		if self.world != self.currentTile.m_parent.m_parent.m_components[0]:
			self.world = self.currentTile.m_parent.m_parent.m_components[0]

		self.worldDifference = None
		try:
			if self.oldWorld != self.world:
				self.worldDifference = True
			else:
				self.worldDifference = False
		except:
			self.worldDifference = True
		if self.worldDifference == True:
			self.oldTile = self.currentTile
			self.oldWorld = self.world
			self.mapText = CreateMap.Create(self.world.m_parent, self)

			
		# else:
		# 	self.oldTile = self.currentTile
		# 	if self.currentTile.m_parent.m_parent.m_components[0].m_name == "Example":
		# 		pygame.mixer.music.load(os.path.join('data', 'audio', 'rush-la-villa-strangiato.mp3'))
		# 		pygame.mixer.music.play()
		# 	elif self.currentTile.m_parent.m_parent.m_components[0].m_name == "Ship":
		# 		pygame.mixer.music.load(os.path.join('data', 'audio', '41_Starship_Bridge.mp3'))
		# 		pygame.mixer.music.play()

		if self.currentTile:
			if self.currentTile.m_description not in self.thingToPrint and self.printDescription == True:
				self.thingToPrint.append(self.currentTile.m_name)
				self.thingToPrint.append(self.currentTile.m_description)


		for i in self.thingToPrint:
			self.m_parent.m_renderer.m_mainTextBox += ("%s\n" % i)