from AdventureEngine.components.gamecomponent import GameComponent

class State(GameComponent):
	def __init__(self):
		GameComponent.__init__(self)
		self.m_name = "DefaultState"

		