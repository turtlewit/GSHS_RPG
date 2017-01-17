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

from src.textitem import TextItem
from AdventureEngine.CoreEngine.input import Input

class SignPost(TextItem):

	def __init__(self, groundDescription, inspectDescription, name="signpost", canBeDestroyed=True):

		TextItem.__init__(self, name)

		self.destroyed = False
		self.canBeDestroyed = canBeDestroyed

		self.m_groundDescription = groundDescription
		self.m_inspectDescription = inspectDescription

		self.printed = False

	def Update2(self):
		if self.canBeDestroyed:
			if Input.command:
				if type(Input().command) is str:
					if Input.command.lower() == "destroy %s" % self.m_name:
						self.destroyed = True
						self.m_groundDescription = "There is a destroyed signpost here.\nYou can get rid of this signpost by typing 'clear signpost'"
						self.m_inspectDescription = "The signpost lies in pieces scattered across the ground."

					if Input.command.lower() == "clear %s" % self.m_name and self.destroyed:
						self.m_enabled = False

		self.m_parent.m_engine.m_game.GetRootObject().stctrl.GetState().AddText("\n%s" % self.m_groundDescription, 4)

			