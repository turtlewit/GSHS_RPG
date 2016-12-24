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

class GameObject:

	def __init__(self):
		self.m_children = []
		self.m_components = []
		self.m_transform = (0,0)
		self.m_parent = None
		self.m_engine = None
		self.m_renderer = None

	def AddComponent(self, component):
		self.m_components.append(component)
		component.SetParent(self)

		return self.m_components[len(self.m_components) - 1]

	def AddChild(self, child):
		self.m_children.append(child)
		child.m_engine = self.m_engine
		child.m_renderer = self.m_renderer
		child.m_parent = self

	def Update(self):
		for component in self.m_components:
			component.Update()

	def UpdateAll(self):
		self.Update()

		for child in self.m_children:
			child.UpdateAll()

	def SetEngine(self,engine):
		self.m_engine = engine

	def SetRenderer(self,renderer):
		self.m_renderer = renderer

	def GetAllChildren(self):
		returnStuff = self.m_children
		for child in self.m_children:
			returnStuff += child.GetAllChildren()
		return returnStuff
