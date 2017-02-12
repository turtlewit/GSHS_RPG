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

import sys
import curses

class Input:

	#renderer = None

	commandHistory = []
	command = None
	unf_command = ""
	cheese = "cheese"
	takeTextInput = False
	char = None

	def Update(self, renderer):
		Input.command = None
		Input.char = None
		if renderer:
			currentCharacter = renderer.m_screen.getch()



			if currentCharacter != -1:
				if currentCharacter != curses.KEY_RESIZE:
					Input.char = currentCharacter
				if Input.takeTextInput:
					if currentCharacter == ord('\n'):
						if len(Input.unf_command.split()) > 0:
							Input.commandHistory.insert(0,Input.command)
							Input.command = Input.unf_command
						renderer.m_cmd = ""
						Input.unf_command = ""

					if sys.platform == 'linux' \
						or sys.platform == 'linux2' \
						or sys.platform == 'linux-armv7l':
						if currentCharacter == 127 \
							or currentCharacter == curses.KEY_BACKSPACE:
							renderer.m_cmd = renderer.m_cmd[:-1]
							Input.unf_command = Input.unf_command[:-1]
					else:
						if currentCharacter == 8:
							renderer.m_cmd = renderer.m_cmd[:-1]
							Input.unf_command = Input.unf_command[:-1]

					if currentCharacter >=32 and currentCharacter <= 126:

						if renderer.m_vorCmd:
							if len(Input.unf_command) \
								< renderer.BUFFER_X \
								- len(renderer.m_vorCmd) \
								- 1:
								renderer.m_cmd += chr(currentCharacter)
								Input.unf_command += chr(currentCharacter)

					if currentCharacter in [
						curses.KEY_UP,
						curses.KEY_DOWN,
						curses.KEY_LEFT,
						curses.KEY_RIGHT,
						27
						]:
						Input.command = currentCharacter
