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

from AdventureEngine.CoreEngine.engine import Engine
from GSHS_RPG import GSHS_RPG
import os

class Main:

	def __init__(self):
		if not os.path.exists(os.path.join('data', 'logs')):
			os.makedirs(os.path.join('data', 'logs'))


	def Run(self):
		engine = Engine(GSHS_RPG())
		engine.InitRenderer("Verloren")
		return engine.Start()


if __name__ == "__main__":
	while True:
		main = Main()
		if not main.Run():
			break
