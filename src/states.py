from AdventureEngine.components.gamecomponent import GameComponent 
from AdventureEngine.components.state import State
from AdventureEngine.CoreEngine.input import Input
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

	def GetState(self):
		if self.m_currentState:
			return self.m_currentState
		else:
			self.ChangeState("default")
			return self.m_currentState

class DefaultState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "default")
		self.renderer = None
		#self.m_init2HasRun = False
		self.textobject1 = open(os.path.join('data', 'assets', 'art', 'Verloren.txt')).read()
		self.textobject2 = "Press Any Key To Continue"

		self.stuffToGive = []

		self.timeticks = 0
		self.textobject2IsIn = False



	def Init2(self):
		self.m_parent.m_renderer.m_vorCmd = None
		Input.takeTextInput = False
		if self.renderer == None:
			self.renderer = self.m_parent.m_renderer
		'''
		textpos1 = int(self.renderer.BUFFER_X / 2) - int(len(self.textobject1) / 2) 
		textpos2 = int(self.renderer.BUFFER_Y / 3)
		'''
		self.stuffToGive.append([0, 0, self.textobject1])

		self.object2 = [int(self.renderer.BUFFER_Y / 3) * 2, int(self.renderer.BUFFER_X / 2) - int(len(self.textobject2) / 2), self.textobject2]

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

	def Init2(self):
		self.m_parent.m_renderer.m_renderObjects = []
		self.m_parent.m_renderer.m_mainTextBoxList = []
		self.m_mainTextBox = ""
		Input.takeTextInput = True
		self.m_parent.m_renderer.m_vorCmd = ">"
		self.thingsToPrint = []
		self.extraToPrint = []


		self.checkForItems = True

	def Update2(self):

		
		if self.m_parent.m_player.thingToPrint not in self.m_parent.m_renderer.m_mainTextBoxList and len(self.m_parent.m_player.thingToPrint) > 0:
			for i in self.m_parent.m_player.thingToPrint:
				if i not in self.m_parent.m_renderer.m_mainTextBoxList and i != "":
					self.m_parent.m_renderer.m_mainTextBoxList.append(i)

		if self.checkForItems:
			'''
			if self.m_parent.m_transform == self.m_parent.m_player.m_parent.m_transform:
				for comp in self.m_parent.m_components:
					if comp.m_type == "item":
						if comp.m_enabled:
							self.m_parent.m_renderer.m_mainTextBoxList.append(comp.m_groundDescription)
			'''
			for child in self.m_parent.m_player.world.m_parent.m_children:
				if child.m_transform == self.m_parent.m_player.m_parent.m_transform:
					for comp in child.m_components:
						if comp.m_type == "item":
							if comp.m_enabled:
								self.m_parent.m_renderer.m_mainTextBoxList.append(comp.m_groundDescription)


			self.m_parent.m_player.changeTile = False

		'''
		for i in self.thingsToPrint:
			if i not in self.m_parent.m_renderer.m_mainTextBoxList:
				self.m_parent.m_renderer.m_mainTextBoxList.append("%s\n" % i)
		'''
		for i in self.extraToPrint:
			if i not in self.m_parent.m_renderer.m_mainTextBoxList:
				self.m_parent.m_renderer.m_mainTextBoxList.append("%s\n" % i)


		self.checkForItems = False

		if Input.command:
			self.m_parent.m_renderer.m_mainTextBoxList = []
			self.extraToPrint = []
			self.checkForItems = True
			if type(Input().command) is str:
				if Input.command.lower().split()[0] == "inspect":
					'''
					if self.m_parent.m_transform == self.m_parent.m_player.m_parent.m_transform:
						for comp in self.m_parent.m_components:
							if comp.m_type == "item":
								if comp.m_enabled and comp.m_name == Input.command.lower().split()[1]:
									self.extraToPrint.append(comp.m_inspectDescription)
					'''
					for child in self.m_parent.m_player.world.m_parent.m_children:
						if child.m_transform == self.m_parent.m_player.m_parent.m_transform:
							for comp in child.m_components:
								if comp.m_type == "item":
									if comp.m_enabled and comp.m_name == Input.command.lower().split()[1]:
										self.extraToPrint.append(comp.m_inspectDescription)


class MapState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "map")

	def Init2(self):
		Input.takeTextInput = False
		self.m_parent.m_renderer.m_vorCmd = None
		Input.char = None

	def Update2(self):
		if [0, 0, self.m_parent.m_player.mapText] not in self.m_parent.m_renderer.m_renderObjects:
			self.m_parent.m_renderer.m_renderObjects.append([0, 0, self.m_parent.m_player.mapText])

		if Input.char:
			self.m_controller.ChangeState("explore")