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

import curses
import sys
import os
import time

class Clock:
	def __init__(self):
		self.time1 = time.time()

	def Tick(self, fps):
		frametime = 1/fps
		currentTime = time.time()
		while (currentTime - self.time1) < frametime:
			currentTime = time.time()
		self.time1 = time.time()

	def DeltaTime(self):
		return time.time() - self.time1

class Renderer:

	BUFFER_Y = 25
	BUFFER_X = 80

	def __init__(self, name):
		if sys.platform == 'win32':
			os.system("title %s" % name)

		self.m_screen = curses.initscr()

		if sys.platform == 'linux' or sys.platform == 'linux2':
			curses.resizeterm(25, 80)

		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		self.m_screen.nodelay(1)
		self.m_screen.keypad(True)

		self.m_header = []
		self.m_vorCmd = ""
		self.m_cmd = ""

		# External Modification OK
		self.m_mainTextBoxList = []
		self.m_compareTextBoxList = []

		# Do not externally modify
		self.m_mainTextBox = ""
		self.m_mainTextBox2 = ""
		self.m_incompleteTextBox = ""
		self.m_placeInList = 0
		#

		self.useLineConvert = True

		self.m_clock = Clock()

		# Typical object: [y, x, text]
		# Or [y, x, text, color_pair]
		self.m_renderObjects = []

	def LineConvert(self, line):
		line = line.split()
		linelen = 0
		if len(line) > 0:
			word = line.pop(0)
		else:
			word = ""
		wordsplit = list(word)
		linelen += len(wordsplit) + 1
		newLine = word
		for x in range(0, len(line)):
			word = line.pop(0)
			wordsplit = list(word)
			linelen += len(wordsplit) + 1
			if linelen > self.BUFFER_X - 2:
				newLine = "%s\n" % (newLine)
				linelen = 0
				newLine = "%s%s" % (newLine, word)
				linelen += len(wordsplit) + 1
			else:
				newLine = "%s %s" % (newLine, word)
		return newLine


	def Render(self):
		self.m_clock.Tick(120)
		self.m_screen.clear()

		l = 0
		for line in self.m_header:
			self.m_screen.addstr(l,0,line)
			l+=1
		if self.m_vorCmd != None:
			if self.m_compareTextBoxList != self.m_mainTextBoxList:
				if len(''.join(self.m_compareTextBoxList)) \
					<= len(''.join(self.m_mainTextBoxList)):	#Adding
					good = True
					for i in range (0, len(''.join(self.m_compareTextBoxList))):
						if ''.join(self.m_compareTextBoxList)[i] \
							!= ''.join(self.m_mainTextBoxList)[i]:
							good = False
							break
					if good:
						if len(''.join(self.m_compareTextBoxList)) == 0:
							self.m_placeInList = 0
						self.m_compareTextBoxList = self.m_mainTextBoxList
						self.m_mainTextBox = ""
					else:
						self.m_placeInList = 0
						self.m_compareTextBoxList = self.m_mainTextBoxList
						self.m_mainTextBox = ""
						self.m_incompleteTextBox = ""

				elif len(''.join(self.m_compareTextBoxList)) \
					> len(''.join(self.m_mainTextBoxList)):	#Subtracting
					good = True

					for i in range (0, len(''.join(self.m_mainTextBoxList))):
						if ''.join(self.m_compareTextBoxList)[i] \
							!= ''.join(self.m_mainTextBoxList)[i]:
							good = False

					if not good:
						self.m_placeInList = 0
						self.m_compareTextBoxList = self.m_mainTextBoxList
						self.m_mainTextBox = ""
						self.m_incompleteTextBox = ""
					else:
						self.m_mainTextBox = ""
						self.m_compareTextBoxList = self.m_mainTextBoxList

				else:
					self.m_placeInList = 0
					self.m_compareTextBoxList = self.m_mainTextBoxList
					self.m_mainTextBox = ""
					self.m_incompleteTextBox = ""

		for item in self.m_mainTextBoxList:
			self.m_mainTextBox += ("%s\n") % item

		if self.useLineConvert == True:
			if len(self.m_mainTextBox.split()) > 0:
				newMainTextBox = ""
				for line in self.m_mainTextBox.split('\n'):
					if line != "" and line != "\n" and line != " ":
						newMainTextBox += "%s\n" % self.LineConvert(line)

				self.m_mainTextBox2 = newMainTextBox

		mainTextBoxList = list(self.m_mainTextBox2)

		if self.m_placeInList < len(mainTextBoxList):

			if len(self.m_mainTextBox2) < self.m_placeInList:
				self.m_incompleteTextBox = ""
				for i in range(0, self.m_placeInList):
					self.m_incompleteTextBox += mainTextBoxList[i]
			else:
				self.m_incompleteTextBox += mainTextBoxList[self.m_placeInList]
			self.m_placeInList += 1

		elif self.m_placeInList > len(mainTextBoxList):
			self.m_incompleteTextBox = self.m_incompleteTextBox[:-1]
			self.m_placeInList -= 1

		if self.m_vorCmd != None:
			self.m_screen.addstr(l, 0, self.m_incompleteTextBox)
			self.m_screen.addstr(self.BUFFER_Y -1, 0, self.m_vorCmd)

		self.m_screen.addstr(self.m_cmd)

		for obj in self.m_renderObjects:
			if len(obj)==4:
				self.m_screen.addstr(obj[0], obj[1], obj[2], obj[3])
			else:
				self.m_screen.addstr(obj[0], obj[1], obj[2])

		self.m_screen.refresh()

		self.m_mainTextBoxList = []
		self.m_mainTextBox = ""

	def Cleanup(self):
		curses.endwin()
