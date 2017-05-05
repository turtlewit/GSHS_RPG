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

class GameComponent:
	def __init__(self):
		self.m_parent = None
		self.m_type = None


	def SetParent(self, parent):
		self.m_parent = parent

	def Update(self):
		pass

	def GetPosition(self):
		return self.m_parent.m_transform

	def GetEngine(self):
		return self.m_parent.m_engine

	def GetRenderer(self):
		return self.m_parent.m_engine.m_renderingEngine

	def GetGame(self):
		return self.m_parent.m_engine.m_game

	def GetRoot(self):
		return self.m_parent.m_engine.m_game.m_root

	def GetPlayer(self):
		return self.m_parent.m_engine.m_game.m_root.m_player

	def Destroy(self):
		self.m_parent.m_parent.m_children.remove(self.m_parent)
		self.m_parent.m_parent = None
