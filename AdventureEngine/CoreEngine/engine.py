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

from AdventureEngine.CoreEngine.game import Game
from AdventureEngine.render.renderer import Renderer
from AdventureEngine.CoreEngine.input import Input
from AdventureEngine.CoreEngine.audio import Audio
class Engine:
	def __init__(self,game):
		self.m_isRunning = False
		self.m_restartGame = False
		self.m_game = game
		self.m_renderingEngine = None
		self.m_audio = Audio()
		game.SetEngine(self);

	def InitRenderer(self,name):
		self.m_renderingEngine = Renderer(name)
		self.m_game.SetRenderer(self.m_renderingEngine)
		Input().renderer = self.m_renderingEngine

	def Start(self):
		if self.m_isRunning:
			return

		return self.Run()

	def Stop(self):
		if self.m_isRunning == False:
			return

		self.m_isRunning = False

	def Run(self):
		self.m_isRunning = True

		self.m_game.Initialize()

		while(self.m_isRunning):
			Input().Update(self.m_renderingEngine)

			self.m_game.Update()

			#self.m_game.Render(self.m_renderingEngine)
			self.m_renderingEngine.Render()

		self.m_renderingEngine.Cleanup()

		if self.m_restartGame:
			self.m_restartGame = False
			return True
		else:
			return False
