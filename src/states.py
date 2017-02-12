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
from AdventureEngine.components.state import State
from AdventureEngine.CoreEngine.input import Input
import curses
import os
class StateController(GameComponent):

	def __init__(self):
		GameComponent.__init__(self)
		self.m_stateList = []
		self.m_currentState = None
		self.m_type = "stctrl"

	def ChangeState(self, nameOfState):
		for state in self.m_stateList:
			if state.m_name == nameOfState:
				self.m_currentState = state
				self.m_currentState.m_init2HasRun = False

	def GetState(self, name = None):
		if name:
			for state in self.m_stateList:
				if state.m_name == name:
					return state
		else:
			if self.m_currentState:
				return self.m_currentState
			else:
				self.ChangeState("default")
				return self.m_currentState

class DefaultState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "default")
		self.renderer = None
		self.textobject1 = open(
			os.path.join(
				'data', 'assets', 'art', 'Verloren.txt'
			)
		).read()
		self.textobject2 = "Press Any Key To Continue"
		self.stuffToGive = []
		self.timeticks = 0
		self.textobject2IsIn = False

	def Init2(self):
		self.m_parent.m_renderer.m_vorCmd = None
		Input.takeTextInput = False
		if self.renderer == None:
			self.renderer = self.m_parent.m_renderer

		self.stuffToGive.append([0, 0, self.textobject1])

		self.object2 = [
			int(self.renderer.BUFFER_Y / 3)\
				* 2,
			int(self.renderer.BUFFER_X / 2)\
				- int(len(self.textobject2) / 2),
			self.textobject2
		]

	def Update2(self):
		if self.timeticks >= 60:
			self.renderer.m_renderObjects = []
			self.timeticks = 0
			self.textobject2IsIn = not self.textobject2IsIn

		try:
			self.stuffToGive.remove(self.object2)
		except:
			pass

		if self.textobject2IsIn:
			self.stuffToGive.append(self.object2)

		for thing in self.stuffToGive:
			if thing not in self.renderer.m_renderObjects:
				self.renderer.m_renderObjects.append(thing)

		self.timeticks +=1

		if Input.char:
			self.m_controller.ChangeState("explore")

class ExplorationState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "explore")
		self.printDict = {}
		self.tempDict = {}
		self.clear = False

	def Init2(self):
		self.m_parent.m_renderer.m_renderObjects = []
		#self.m_parent.m_renderer.m_mainTextBoxList = []
		#self.m_mainTextBox = ""
		Input.takeTextInput = True
		self.m_parent.m_renderer.m_vorCmd = ">"


	def Update2(self):
		alist = list(self.printDict.keys())
		alist.sort()
		for order in alist:
			for textItem in self.printDict[order]:
				self.m_parent\
					.m_renderer\
					.m_mainTextBoxList\
					.append("%s\n" % textItem)

		if self.clear:
			self.printDict = {}
			self.clear = False
			self.printDict = self.tempDict

	def AddText(self, text, order = 3):
		# Default Text (Area descriptions, etc. go on layer 3.)
		if self.clear == False:
			try:
				if text not in self.printDict[order]:
					self.printDict[order].append(text)
			except:
				self.printDict[order] = [text]
		else:
			try:
				if text not in self.tempDict[order]:
					self.tempDict[order].append(text)
			except:
				self.tempDict[order] = [text]

	def ClearText(self):
		self.clear = True
		self.tempDict = {}


class MapState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "map")

	def Init2(self):
		Input.takeTextInput = False
		self.m_parent.m_renderer.m_vorCmd = None
		Input.char = None

	def Update2(self):
		if [0, 0, self.m_parent.m_player.mapText] \
			not in self.m_parent.m_renderer.m_renderObjects:
			self.m_parent\
				.m_renderer\
				.m_renderObjects\
				.append([0, 0, self.m_parent.m_player.mapText])

		if Input.char:
			self.m_controller.ChangeState("explore")


class CombatState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "combat")
		self.renderer = None
		self.target = None

		self.options = [
			self.Option("Attack"),
			self.Option("Defend"),
			self.Option("Item")
		]
		self.options[0].direction[1] = self.options[1]
		self.options[1].direction[0] = self.options[0]
		self.options[1].direction[1] = self.options[2]
		self.options[2].direction[0] = self.options[1]

		self.activeOption = self.options[0]

		self.menu_art = open(
			os.path.join(
					'data', 'assets', 'art', 'CombatMenu.txt'
				)
			).read()

	class Option:
		def __init__(self, text):
			self.text = text
			# Direction is [Up, Down, Left, Right]
			self.direction = [None, None, None, None]

	def Init2(self):
		curses.start_color()
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
		self.m_parent.m_renderer.m_vorCmd = None
		# Input.takeTextInput = False
		if self.renderer == None:
			self.renderer = self.m_parent.m_renderer

	def Update2(self):
		self.renderer.m_renderObjects.append(
			[0, 0, self.menu_art, curses.color_pair(1)]
		)

		position = 19
		for option in self.options:
			if self.activeOption == option:
				self.renderer.m_renderObjects.append(
					[position, 1, option.text, curses.color_pair(2)]
				)
			else:
				self.renderer.m_renderObjects.append(
					[position, 1, option.text, curses.color_pair(3)]
				)
			position += 1

		if type(Input().command) is not str:
			if Input().command == curses.KEY_UP:
				if self.activeOption.direction[0]:
					self.activeOption = self.activeOption.direction[0]
			if Input().command == curses.KEY_DOWN:
				if self.activeOption.direction[1]:
					self.activeOption = self.activeOption.direction[1]
			if Input().command == 27:
				self.m_controller.ChangeState("explore")
		mname = "Coolest Monster"
		minfo = "Health: 30"
		self.renderer.m_renderObjects.append(
			[
				0,
				int(self.renderer.BUFFER_X / 2)
					- int(len(mname) / 2),
				mname,
				curses.color_pair(3)
			]
		)
		self.renderer.m_renderObjects.append(
			[
				1,
				int(self.renderer.BUFFER_X / 2)
					- int(len(minfo) / 2),
				minfo,
				curses.color_pair(3)
			]
		)
		ftext = """The Coolest Monster decides that you are a worthy target.\n\
Coolest Monster uses Slash.\n\
You are minorly bruised."""
		self.renderer.m_renderObjects.append(
			[3, 0, ftext, curses.color_pair(3)]
		)


	def Initiate(self, target):
		self.target = target
		self.m_controller.ChangeState("combat")
