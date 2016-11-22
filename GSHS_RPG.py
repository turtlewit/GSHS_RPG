from AdventureEngine.CoreEngine.gameobject import GameObject
from AdventureEngine.CoreEngine.game import Game
from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.CoreEngine.input import Input
from src.states import *
from src.player import Player
from src.audioplayer import AudioPlayer
import load
import os

'''
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
'''

class Root(GameObject):
	def __init__(self):
		GameObject.__init__(self)
		self.stctrl = None
		self.m_player = None

class GSHS_RPG(Game):

	def Initialize(self):
		root = Root()
		stctrl = root.AddComponent(StateController())
		root.stctrl = stctrl
		print(root.stctrl)
		root.AddComponent(DefaultState(stctrl))
		stctrl.ChangeState("default")
		root.AddComponent(MapState(stctrl))
		root.AddComponent(ExplorationState(stctrl))
		self.AddObject(root)
		self.m_root = root
		newmap = load.Map()

		pc = GameObject()
		pc.AddComponent(Player())
		pc.AddComponent(AudioPlayer())
		self.AddObject(pc)
		root.m_player = pc.m_components[0]
		newmap.LoadMapsInDirectory(os.path.join('data', 'maps'), os.path.join('data', 'logs', 'log.log'))

		for world in newmap.Worlds:
			self.AddObject(world)
