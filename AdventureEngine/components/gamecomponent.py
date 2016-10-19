

class GameComponent:
	def __init__(self):
		self.m_parent = None
		self.m_type = None

	def SetParent(self, parent):
		self.m_parent = parent

	def Update(self):
		pass