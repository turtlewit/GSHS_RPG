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

class Game:
	def __init__(self):
		self.m_root = None
		self.m_engine = None

	def Initialize(self):
		pass

	def Update(self):
		self.GetRootObject().UpdateAll()

	def SetEngine(self, engine):
		self.m_engine = engine
		self.GetRootObject().SetEngine(engine)

	def SetRenderer(self, renderer):
		self.GetRootObject().SetRenderer(renderer)

	def GetRootObject(self):
		if self.m_root == None:
			self.m_root = GameObject()

		return self.m_root

	def AddObject(self, obj):
		if self.m_root == None:
			self.m_root = obj
			self.m_root.SetEngine(self.m)
		else:
			self.GetRootObject().AddChild(obj)