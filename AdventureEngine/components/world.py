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

class World(GameComponent):
	def __init__(self):
		GameComponent.__init__(self)
		self.m_type = "world"
		self.m_spaceDescription = None
		self.m_landingDescription = None
		self.m_name = None
		self.m_music = None
		self.m_tileList = []

class Tile(GameComponent):
	def __init__(self, move_north_message=None, move_south_message=None, move_east_message=None, move_west_message=None, m_name=None, m_description=None):
		GameComponent.__init__(self)
		self.m_type = "tile"
		self.move_north_message = move_north_message
		self.move_south_message = move_south_message
		self.move_east_message = move_east_message
		self.move_west_message = move_west_message
		self.m_name = m_name
		self.m_description = m_description