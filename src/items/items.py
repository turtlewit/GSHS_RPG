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

from enum import Enum


class Slot(Enum):
	HEAD=0
	SHOULDER_L=1
	SHOULDER_R=2
	TORSO=3
	ARM_L=4
	ARM_R=5
	LEGS=6
	FEET=7
	WEAPON_A=8
	WEAPON_B=9


class Stat:
	def __init__(self, name, id):
		self.m_ID = id
		self.m_name = name
		self.m_xp = 0

	def GetRating(self):
		x = 0
		y = -1
		while self.m_xp >= x:
			y += 1
			x += x + (100.0*(1.05**y))
		alphabet = [
		'A','B','C','D','E','F','G','H','I','J','K','L','M',
		'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
		]
		if y < 26:
			return alphabet[25 - y]
		else:
			return alphabet[0]

	def SetRating(self, letter):
		x = 0
		y = -1
		alphabet = [
		'A','B','C','D','E','F','G','H','I','J','K','L','M',
		'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
		]
		letter2 = None
		while True:
			y += 1
			x += x + (100.0*(1.05**y))
			if y < 26:
				letter2 = alphabet[25 - y]
			else:
				break
			if letter2 == letter:
				break
		self.m_xp = x


class Stats(Enum):
	PHYSICAL_INTEGRITY=0
	OLD_WAY=1
	NEW_WAY=2
	ACCURACY=3
	PRECISION=4
	ENGINEERING=5
	ARTIFICING=6
	MENTAL_FORTITUDE=7
	REFLEX=8

	def Generate():
		l = [
			Stat("Physical Integrity", 0),
			Stat("Old Way", 1),
			Stat("New Way", 2),
			Stat("Accuracy", 3),
			Stat("Precision", 4),
			Stat("Engineering", 5),
			Stat("Artificing", 6),
			Stat("Mental Fortitude", 7),
			Stat("Reflex", 8),
		]
		return l
