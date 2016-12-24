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

from AdventureEngine.components.gamecomponent import GameComponent 

class State(GameComponent):

	def __init__(self, controller, name):
		GameComponent.__init__(self)

		self.m_name = name
		self.m_init2HasRun = False

		self.m_controller = controller
		self.m_controller.m_stateList.append(self)

	def Update(self):
		if self.m_init2HasRun == False and self.m_controller.m_currentState == self:
			self.Init2()
			self.m_init2HasRun = True
		if self.m_controller.GetState() == self:
			self.Update2()

	def Init2(self):
		pass

	def Update2(self):
		pass

