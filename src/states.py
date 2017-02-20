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


# Option Definitions
class Option:
	def __init__(self, text, position):
		self.text = text
		# Direction is [Up, Down, Left, Right]
		self.direction = [None, None, None, None]
		self.position = position

	def ClickAction(self):
		pass


class BasicOption(Option):
	def __init__(self, text, position, state, submenu_to_go_to):
		Option.__init__(self, text, position)
		self.state = state
		self.subNumber = submenu_to_go_to

	def ClickAction(self):
		self.state.submenus[self.subNumber].enabled = True
		self.state.activeOption \
			= self.state.submenus[self.subNumber].options[0]


class AttackOption(Option):
	def __init__(self, text, position, state, attack):
		Option.__init__(self, text, position)
		self.state = state
		self.attack = attack

	def ClickAction(self):
		if self.state.subject.currentCooldown <= 0:
			self.state.Attack(
				self.state.subject, 1, self.attack
			)


class CombatState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "combat")
		self.renderer = None
		self.target = None
		self.subject = None
		self.pair = []

		self.textBuffer = ""



		self.menu_art = open(
			os.path.join(
					'data', 'assets', 'art', 'CombatMenu.txt'
				)
			).read()

	class Submenu:
		def __init__(self):
			self.options = []
			self.uiAsset = None
			self.enabled = False

	def Init2(self):

		curses.start_color()
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
		self.m_parent.m_renderer.m_vorCmd = None
		# Input.takeTextInput = False
		if self.renderer == None:
			self.renderer = self.m_parent.m_renderer

		# Create Submenus
		self.submenus = [
			self.Submenu(), # First Submenu
			self.Submenu() # Attack Submenu
		]

		# First Submenu
		self.submenus[0].enabled = True
		self.submenus[0].options = [
			BasicOption("Attack", (19, 1), self, 1),
			BasicOption("Defend", (20, 1), self, 1),
			BasicOption("Item", (21, 1), self, 1)
		]
		self.submenus[0].options[0].direction[1] = self.submenus[0].options[1]
		self.submenus[0].options[1].direction[0] = self.submenus[0].options[0]
		self.submenus[0].options[1].direction[1] = self.submenus[0].options[2]
		self.submenus[0].options[2].direction[0] = self.submenus[0].options[1]

		# Attack Submenu
		self.submenus[1].options = [
			AttackOption("Weak", (19, 20), self, self.subject.attacks[0]),
			AttackOption("Strong", (20, 20), self, self.subject.attacks[1])
		]
		self.submenus[1].options[0].direction[1] = self.submenus[1].options[1]
		self.submenus[1].options[1].direction[0] = self.submenus[1].options[0]

		self.activeOption = self.submenus[0].options[0]

	def Update2(self):

		if type(Input().command) is not str:
			if Input().command == curses.KEY_UP:
				if self.activeOption.direction[0]:
					self.activeOption = self.activeOption.direction[0]
			if Input().command == curses.KEY_DOWN:
				if self.activeOption.direction[1]:
					self.activeOption = self.activeOption.direction[1]
			if Input().command == 27:
				self.m_controller.ChangeState("explore")
			if Input().command == 10:
				self.activeOption.ClickAction()

		self.Render()

	def Render(self):
		self.renderer.m_renderObjects.append(
			[0, 0, self.menu_art, curses.color_pair(1)]
		)

		for submenu in self.submenus:
			if submenu.enabled:
				for option in submenu.options:
					if option == self.activeOption:
						self.renderer.m_renderObjects.append(
							[
								option.position[0],
								option.position[1],
								option.text,
								curses.color_pair(2)
							]
						)
					else:
						self.renderer.m_renderObjects.append(
							[
								option.position[0],
								option.position[1],
								option.text,
								curses.color_pair(3)
							]
						)

		mname = self.target.m_name
		minfo = "Health: %d" % self.target.a_health
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

		if len(self.textBuffer.split('\n')) <= 14:
			self.renderer.m_renderObjects.append(
				[
					3,
					0,
					self.textBuffer,
					curses.color_pair(3)
				]
			)
		else:
			textlist = self.textBuffer.split('\n')
			for i in range(0, ((len(textlist) - 1) - 14)):
				textlist.pop(0)
			textlist = '\n'.join(textlist)
			self.renderer.m_renderObjects.append(
				[
					3,
					0,
					textlist,
					curses.color_pair(3)
				]
			)

	# Target: 0 = player, 1 = enemy
	def Attack(self, subject, target, attack):
		self.pair[target].TakeDamage(attack.baseAttack, attack.type)
		subject.currentCooldown = attack.cooldown
		self.textBuffer += "%s\n%d\n" \
			% (attack.text, self.pair[target].a_health)

	def Initiate(self, subject, target):
		self.target = target
		self.subject = subject
		self.pair = [subject, target]
		self.m_controller.ChangeState("combat")
