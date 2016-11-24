from AdventureEngine.CoreEngine.gameobject import GameObject
from AdventureEngine.CoreEngine.game import Game
from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.CoreEngine.input import Input

from src.states import *
from src.player import Player
from src.audioplayer import AudioPlayer

import load
import os


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
		newmap.LoadMapsInDirectory(os.path.join('data', 'maps'), 
				os.path.join('data', 'logs', 'log.log'))

		for world in newmap.Worlds:
			self.AddObject(world)
