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
from src.items.items import Stats

import time

from random import randint


class Enemy(GameComponent):

	def __init__(self, name="Enemy", stats=Stats.Generate()):
		self.m_type = "npc"
		self.m_name = name
		self.a_stats = stats
		self.a_health = 200

		self.time1 = time.time()

		self.currentCooldown = 0.0

		self.canAttack = False

		self.attacks = [
			Attack(
				self,
				"Oh wow! %s slashed!" % self.m_name,
				1,
				None,
				1
			),
			Attack(
				self,
				"Oh wow! %s slashed in a different way!" % self.m_name,
				2,
				None,
				1
			)
		]

	def Update(self):
		if self.GetRoot().stctrl.GetState().m_name == "combat":
			if self.canAttack:
				self.GetRoot().stctrl.GetState('combat').Attack(
					self,
					0,
					self.attacks[randint(0, len(self.attacks) - 1)]
				)
				self.canAttack = False
			else:
				self.currentCooldown -= (time.time() - self.time1)
				if self.currentCooldown <= 0.0:
					self.canAttack = True
		self.time1 = time.time()


	def TakeDamage(self, damage, type):
		self.a_health -= damage


class Attack:
	def __init__(self, npc, text, baseAttack, type, cooldown, skills = []):
		self.m_npc = npc
		self.text = text
		self.type = type
		self.baseAttack = baseAttack
		self.cooldown = cooldown
		self.skills = skills
