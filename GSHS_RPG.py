from AdventureEngine.CoreEngine.gameobject import GameObject
from AdventureEngine.CoreEngine.game import Game
from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.CoreEngine.input import Input
from src.player import Player
import load
import os

class DumbThing(GameComponent):

	def __init__(self):
		GameComponent.__init__(self)
		self.m_print = False
		self.m_print2 = False

	def Update(self):
		if Input().command == "get rekt":
			self.m_print = True

		if Input().command == "rise":
			self.m_print2 = True

		if self.m_print2 == True:
			self.m_parent.m_renderer.m_mainTextBox = ""
			for child in self.m_parent.m_parent.m_children:
				for component in child.m_components:
					try:
						self.m_parent.m_renderer.m_mainTextBox += component.m_name
					except:
						pass
				for child2 in child.m_children:
					for childcomponent in child2.m_components:
						try:
							self.m_parent.m_renderer.m_mainTextBox += " \"%s\"" % childcomponent.m_name
						except:
						 	pass



		if self.m_print:
			self.m_parent.m_renderer.m_mainTextBox = "Skrub Lord"

class GSHS_RPG(Game):

	def Initialize(self):
		testObject = GameObject()
		testObject.AddComponent(DumbThing())
		self.AddObject(testObject)
		newmap = load.Map()

		pc = GameObject()
		pc.AddComponent(Player())
		self.AddObject(pc)
		newmap.LoadMapsInDirectory(os.path.join('data', 'maps'), os.path.join('data', 'logs', 'log.log'))

		for world in newmap.Worlds:
			self.AddObject(world)
