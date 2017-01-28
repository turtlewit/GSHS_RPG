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

import load

from AdventureEngine.CoreEngine.gameobject import GameObject

from src.items.signpost import SignPost
from src.tilelock import TileLock

import os


class MapDefs():

	def __init__(self, engine):
		self.MapsList = [TutorialMap(engine), ShipMap(engine)]
		self.MapsList2 = []
		for m in self.MapsList:
			m.Load()
			self.MapsList2.append(m.Map)


	def GetMaps(self):
		return self.MapsList2

class MapDef():

	def __init__(self, engine):
		self.MapFile = []
		self.Map = None
		self.engine = engine

	def FindTileAtCoord(self, coords):
		for tileObject in self.Map.m_children:
			if tileObject.m_transform == coords:
				for tileComponent in tileObject.m_components:
					if tileComponent.m_type == "tile":
						return tileObject
		raise ValueError("Shit's Fucked!")

	def LoadEntities(self):
		pass

	def Load(self):
		for amap in self.MapFile:
			self.Map = load.Map().LoadMap(amap)
		self.LoadEntities()

class ShipMap(MapDef):
	def __init__(self, engine):
		MapDef.__init__(self, engine)
		self.MapFile = [os.path.join('data', 'maps', 'ship', 'world.map'), os.path.join('data', 'maps', 'ship', 'core.map'), os.path.join('data', 'maps', 'ship', 'flank.map'),
			os.path.join('data', 'maps', 'ship', 'port.map'), os.path.join('data', 'maps', 'ship', 'starboard.map')]

	class TileLockForward(TileLock):
		def __init__(self):
			TileLock.__init__(self)
			self.m_tileLockedText = "The door south is locked."

		def Conditions(self):
			return True

	def LoadEntities(self):
		tl1g = GameObject()
		tl1g.m_transform = (0,-1)
		self.FindTileAtCoord((0,-1)).SetEngine(self.engine)
		tl1g.AddComponent(self.TileLockForward())
		self.FindTileAtCoord((0,-1)).AddChild(tl1g)

class TutorialMap(MapDef):

	def __init__(self, engine):
		MapDef.__init__(self, engine)
		self.MapFile.append(os.path.join('data', 'maps', 'tutorial.map'))

	def LoadEntities(self):
		gO = GameObject()
		gO.m_transform = (0,0)
		gO.AddComponent(
			SignPost(
"There is a sign post sticking out of the floor here.\n\
The title reads: Welcome!\n\
(Type 'inspect signpost' to inspect the sign post)",
"The signpost reads:\n\
Welcome to Verloren!\n\
Verloren is a Sci-Fi Text-Based Adventure Game.\n\
Verloren uses cardinal direction (north, south, east, and west) to convey direction.\n\
To move, type 'go [direction]', or use the arrow keys.\n\
Type 'go south' to continue the tutorial."
				)
			)
		self.FindTileAtCoord((0,0)).SetEngine(self.engine)
		self.FindTileAtCoord((0,0)).AddChild(gO)

		gO = GameObject()
		gO.m_transform = (0,-1)
		gO.AddComponent(
			SignPost(
"There is a sign post sticking out of the floor here.\n\
The title reads: Maps\n\
(Type 'inspect signpost' to inspect the sign post)",
"Verloren's many worlds are set out on grids of 'Tiles'\n\
You are now 1 tile south of where you started.\n\
Typing 'map' will open the map. On the map, every 't' represents a tile. The 'P' represents where the player (you) are. You can press any key to get rid of the map.\n\
Continue south to progress."
				)
			)
		self.FindTileAtCoord((0,-1)).SetEngine(self.engine)
		self.FindTileAtCoord((0,-1)).AddChild(gO)

		gO = GameObject()
		gO.m_transform = (0,-2)
		gO.AddComponent(
			SignPost(
"There is a sign post sticking out of the floor here.\n\
The title reads: Commands\n\
(Type 'inspect signpost' to inspect the sign post)",
"What you have been typing in order to view these sign posts are called 'commands'.\n\
Commands allow the player to interact with the world around them.\n\
Commands are usually formatted like this: [Command], [Direct Object], [Indirect Object]\n\
For example, 'destroy mailbox sword' would mean to destroy the mailbox using the sword.\n\
Try destroying this signpost. (destroy signpost)\n\
Once you have, continue south."
				)
			)
		self.FindTileAtCoord((0,-2)).SetEngine(self.engine)
		self.FindTileAtCoord((0,-2)).AddChild(gO)
