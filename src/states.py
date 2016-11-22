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
			self.timeticks = 0
			self.textobject2IsIn = not self.textobject2IsIn

		try:
			self.stuffToGive.remove(self.object2)
		except:
			pass
		if self.textobject2IsIn:
			self.stuffToGive.append(self.object2)

		for thing in self.stuffToGive:
			self.renderer.m_renderObjects.append(thing)

		self.timeticks +=1

		if Input.char:
			self.m_controller.ChangeState("explore")

class ExplorationState(State):
	def __init__(self, controller):
		State.__init__(self, controller, "explore")

	def Init2(self):
		Input.takeTextInput = True
		self.m_parent.m_renderer.m_vorCmd = ">"

