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

from AdventureEngine.components.item import Item, Stats, Slot
from enum import Enum


class DamageType(Enum):
	BALLISTIC = 0
	ENERGY = 1
	EXPLOSIVE = 2


class Weapon(Item):
	def __init__(self):
		Item.__init__(self)
		self.m_type = "weapon"
		self.m_equipable = True
		self.m_slot = Slot.WEAPON

		self.a_speed = 0
		self.a_damage = 0
		self.a_damageType = None
		
		self.m_equipRequirements = {}
		