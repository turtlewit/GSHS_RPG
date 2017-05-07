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

"""Item class

This class describes the basic definition of an item.
"""
from AdventureEngine.components.gamecomponent import GameComponent
from AdventureEngine.CoreEngine.input import Input

class Item(GameComponent):

	def __init__(self, name = None):

		GameComponent.__init__(self)
		self.m_name = name
		self.m_type = "item"
		self.m_equipable = False

		self.m_groundDescription = None
		self.m_inspectDescription = None

		self.m_canBePickedUp = False
		self.m_isPickedUp = False
		self.m_enabled = True
		self.m_active = False

	def Update(self):
		if self.m_isPickedUp:
			self.m_active = False
		else:
			if self.GetPlayer().GetPosition() == self.GetPosition() \
				and self.GetPlayer().GetSpacePosition() \
				== self.m_parent.m_parent.m_parent.m_transform:
				self.m_active = True
			else:
				self.m_active = False
		if self.m_enabled and self.m_active and self.GetRoot().stctrl.GetState().m_name == "explore":
			if type(Input().command) is str:
				if Input.command.lower() in ['inspect %s' % self.m_name]:
					self.GetRoot().stctrl.GetState().ClearText()
					self.GetRoot().stctrl.GetState().AddText(self.m_inspectDescription, 5)
			self.Update2()

	def Update2(self):
		pass
