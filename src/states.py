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
		'''Run when activated by player'''
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
		self.state.Attack(
			self.state.subject, self.attack
		)
		self.state.GoToHomeMenu()


class DefendOption(Option):
	def __init__(self, text, position, state):
		Option.__init__(self, text, position)
		self.state = state

	def ClickAction(self):
		self.state.Defend()


class CombatState(State):

	# Constant DEFENCE_COOLDOWN dictates how long
	# the Defence command will be active
	DEFENCE_COOLDOWN = .5

	def __init__(self, controller):
		State.__init__(self, controller, "combat")
		self.renderer = None

		self.subject = None
		self.s_queue = [None, None]
		self.sMaxCooldown = 0

		self.target = None
		self.t_queue = [None, None]
		self.tMaxCooldown = 0

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
		curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_GREEN)
		curses.init_pair(11, curses.COLOR_RED, curses.COLOR_RED)
		curses.init_pair(20, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(21, curses.COLOR_RED, curses.COLOR_BLACK)
		self.m_parent.m_renderer.m_vorCmd = None

		self.s_queue = [None, None]
		self.t_queue = [None, None]

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
			DefendOption("Defend", (20, 1), self),
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
		self.TakeInput()

		if self.subject.a_health <= 0:
			self.m_controller.ChangeState("gameover")

		if self.target.a_health <= 0:
			self.target.Destroy()
			self.target.m_enabled = False
			self.m_controller.ChangeState("explore")

		self.AttackCheck()
		if self.subject.defending:
			self.DefenceCheck()
		self.Render()

	def TakeInput(self):
		if type(Input().command) is not str:
			if Input().command == curses.KEY_UP:
				if self.activeOption.direction[0]:
					self.activeOption = self.activeOption.direction[0]
			if Input().command == curses.KEY_DOWN:
				if self.activeOption.direction[1]:
					self.activeOption = self.activeOption.direction[1]
			if Input().command == 27:
				self.GoToHomeMenu()
			if Input().command == 10:
				self.activeOption.ClickAction()
	
	def GoToHomeMenu(self):
		'''Returns to the default menu'''
		if self.activeOption in self.submenus[0].options:
			self.m_controller.ChangeState("explore")
		else:
			for submenu in self.submenus:
				if submenu != self.submenus[0]:
					submenu.enabled = False
			self.activeOption = self.submenus[0].options[0]

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

		if self.sMaxCooldown > 0:
			percent = self.subject.currentCooldown / self.sMaxCooldown
			tiles = 80 - int(80 * percent)
			toRender = ""
			for i in range(0, tiles):
				toRender += " "
			self.renderer.m_renderObjects.append(
				[2, 0, toRender, curses.color_pair(10)]
			)

		if self.tMaxCooldown > 0:
			percent = self.target.currentCooldown / self.tMaxCooldown
			tiles = 80 - int(80 * percent)
			toRender = ""
			for i in range(0, tiles):
				toRender += " "
			self.renderer.m_renderObjects.append(
				[17, 0, toRender, curses.color_pair(11)]
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

	def Attack(self, subject, attack):
		# If the subject is the player, add the attack
		# to the subject queue, if the queue is not full
		if subject == self.subject:
			if self.s_queue[0]:
				if self.s_queue[1]:
					pass
				else:
					self.s_queue[1] = attack
					self.textBuffer += "%s prepares another attack...\n" \
						% self.subject.m_name.capitalize()

			else:
				self.s_queue[0] = attack
				subject.currentCooldown = attack.cooldown
				self.sMaxCooldown = attack.cooldown
				self.textBuffer += "%s prepares an attack...\n" \
					% self.subject.m_name.capitalize()

		# If the subject is the target, add the attack
		# to the target queue, if the queue is not full
		else:
			if self.t_queue[0]:
				pass
			else:
				self.t_queue[0] = attack
				subject.currentCooldown = attack.cooldown
				self.tMaxCooldown = attack.cooldown
				self.textBuffer += "%s prepares an attack...\n" \
					% self.target.m_name.capitalize()

	def Defend(self):
		if not self.subject.defending:
			self.subject.defending = True
			self.subject.currentCooldown = self.DEFENCE_COOLDOWN
			self.sMaxCooldown = self.DEFENCE_COOLDOWN
			self.textBuffer += "%s is defending...\n" \
				% self.subject.m_name.capitalize()

	def AttackCheck(self):
		# Subject
		if self.subject.currentCooldown <= 0 and self.s_queue[0]:
			self.DoAttack(self.pair[1], self.subject, self.s_queue[0])
			if self.s_queue[1]:
				attack = self.s_queue[1]
				self.s_queue = [None, None]
				self.sMaxCooldown = 0
				self.Attack(self.subject, attack)
			else:
				self.sMaxCooldown = 0
				self.s_queue = [None, None]

		# Target
		if self.target.currentCooldown <= 0 and self.t_queue[0]:
			self.DoAttack(self.pair[0], self.target, self.t_queue[0])
			if self.t_queue[1]:
				attack = self.t_queue[1]
				self.t_queue = [None, None]
				self.tMaxCooldown = 0
				self.Attack(self.target, attack)
			else:
				self.tMaxCooldown = 0
				self.t_queue = [None, None]

	def DefenceCheck(self):
		if self.subject.currentCooldown <= 0:
			if self.s_queue[0]:
				self.sMaxCooldown = self.s_queue[0].cooldown
				self.subject.currentCooldown = self.s_queue[0].cooldown
			else:
				self.sMaxCooldown = 0
			self.subject.defending = False

	def DoAttack(self, target, subject, attack):
		blocking = False
		if target == self.subject:
			if self.subject.defending:
				blocking = True
			else:
				target.TakeDamage(attack.baseAttack, attack.type)
				self.textBuffer += "\n%s\nYour Health is now: %d\n" \
					% (attack.text, self.subject.a_health)
			if blocking:
				self.textBuffer += "\n%s\nHowever, %s blocked the attack!\n" \
					% (attack.text, self.subject.m_name.capitalize())
		else:
			self.target.TakeDamage(attack.baseAttack, attack.type)
			self.textBuffer += "\n%s\n\n" \
				% (attack.text)



	def Initiate(self, subject, target):
		self.target = target
		self.subject = subject
		self.pair = [subject, target]
		self.m_controller.ChangeState("combat")


class GameOverState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "gameover")
		self.gameovertext = "You have died."

	def Init2(self):
		self.m_parent.m_renderer.m_vorCmd = None
		Input.takeTextInput = False
		self.GetRenderer().m_renderObjects = []

	def Update2(self):
		self.GetRenderer().m_renderObjects.append(
			[
				int(self.GetRenderer().BUFFER_Y / 2),
				int((self.GetRenderer().BUFFER_X / 2)
					- (len(self.gameovertext) / 2)),
				self.gameovertext
			]
		)

		if Input.char:
			self.GetEngine().m_restartGame = True
			self.GetEngine().m_isRunning = False
