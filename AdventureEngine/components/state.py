from AdventureEngine.components.gamecomponent import GameComponent 

class State(GameComponent):

	def __init__(self, controller, name):
		GameComponent.__init__(self)

		self.m_name = name
		self.m_init2HasRun = False

		self.m_controller = controller
		self.m_controller.m_stateList.append(self)

	def Update(self):
		if self.m_init2HasRun == False and self.m_controller.m_currentState == self:
			self.Init2()
			self.m_init2HasRun = True
		if self.m_controller.GetState() == self:
			self.Update2()

	def Init2(self):
		pass

	def Update2(self):
		pass

