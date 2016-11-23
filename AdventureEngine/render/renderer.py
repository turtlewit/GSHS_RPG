import curses
import sys
import os
import pygame.time


class Renderer:

	BUFFER_Y = 25
	BUFFER_X = 80

	def __init__(self, name):
		self.m_screen = curses.initscr()

		os.system("title %s" % name)

		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		self.m_screen.nodelay(1)
		self.m_screen.keypad(True)

		self.m_header = []
		self.m_vorCmd = ""
		self.m_cmd = ""
		self.m_mainTextBox = ""
		self.m_mainTextBox2 = ""
		self.m_compareTextBox = ""
		self.m_incompleteTextBox = ""
		self.m_placeInList = 0

		self.useLineConvert = True

		self.tickClock = pygame.time.Clock()

		self.m_renderObjects = []		#Typical object: [y, x, text]

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

		self.tickClock.tick(120)

		#self.Cleanup()
		self.m_screen.clear()

		l = 0
		for line in self.m_header:
			self.m_screen.addstr(l,0,line)
			l+=1

		if self.m_compareTextBox != self.m_mainTextBox:
			self.m_placeInList = 0
			self.m_compareTextBox = self.m_mainTextBox
			self.m_incompleteTextBox = ""

		if self.useLineConvert == True:
			if len(self.m_mainTextBox.split()) > 0:
				newMainTextBox = ""
				for line in self.m_mainTextBox.split('\n'):
					newMainTextBox += "%s\n" % self.LineConvert(line)

				self.m_mainTextBox2 = newMainTextBox

		mainTextBoxList = list(self.m_mainTextBox2)

		if self.m_placeInList < len(mainTextBoxList):
			self.m_incompleteTextBox += mainTextBoxList[self.m_placeInList]
			self.m_placeInList += 1

		self.m_screen.addstr(l, 0, self.m_incompleteTextBox)
		
		if(self.m_vorCmd != None):
			self.m_screen.addstr(self.BUFFER_Y -1, 0, self.m_vorCmd)
		
		self.m_screen.addstr(self.m_cmd)

		for obj in self.m_renderObjects:
			self.m_screen.addstr(obj[0], obj[1], obj[2])

		self.m_screen.refresh()

		"""
		self.m_mainTextBox = ""
		self.m_renderObjects = []
		"""

		

	def Cleanup(self):
		curses.endwin()

