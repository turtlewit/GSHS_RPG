#------------------------------------------------------------------------------#
# Copyright 2016-2017 Golden Sierra Game Development Class                     #
# This file is part of Verloren (GSHS_RPG).                                    #
#                                                                              #
# Verloren (GSHS_RPG) is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# Verloren (GSHS_RPG) is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with Verloren (GSHS_RPG).  If not, see <http://www.gnu.org/licenses/>. #
#------------------------------------------------------------------------------#

from AdventureEngine.CoreEngine.gameobject import GameObject
from AdventureEngine.CoreEngine.game import Game
from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.CoreEngine.input import Input

from src.states import *
from src.player import Player
from src.audioplayer import AudioPlayer
from src.i_signpost1 import ISignPost
from src.maps.maps import MapDefs

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
		root.AddComponent(CombatState(stctrl))
		root.AddComponent(GameOverState(stctrl))
		self.AddObject(root)
		self.m_root = root
		self.GetRootObject().m_game = self
		newmap = load.Map()

		pc = GameObject()
		pc.AddComponent(Player())
		pc.AddComponent(AudioPlayer())
		self.AddObject(pc)
		root.m_player = pc.m_components[0]
		newmap.LoadMapsInDirectory(os.path.join('data', 'maps'),
				os.path.join('data', 'logs', 'log.log'))
		'''
		i_sp_go = GameObject()
		i_sp_go.AddComponent(ISignPost())
		root.AddChild(i_sp_go)
		'''

		for m in MapDefs(self.m_engine).GetMaps():
			self.AddObject(m)

		for world in newmap.Worlds:
			isFound = False
			for child in self.GetRootObject().GetAllChildren():
				if world.m_components[0].m_name == child.m_components[0].m_name:
					isFound = True
					break
			if not isFound:
				self.AddObject(world)
