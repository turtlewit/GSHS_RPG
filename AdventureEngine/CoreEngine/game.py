from AdventureEngine.CoreEngine.gameobject import GameObject

class Game:
	def __init__(self):
		self.m_root = None

	def Initialize(self):
		pass

	def Update(self):
		self.GetRootObject().UpdateAll()

	def SetEngine(self, engine):
		self.GetRootObject().SetEngine(engine)

	def SetRenderer(self, renderer):
		self.GetRootObject().SetRenderer(renderer)

	def GetRootObject(self):
		if self.m_root == None:
			self.m_root = GameObject()

		return self.m_root

	def AddObject(self, obj):
		if self.m_root == None:
			self.m_root = obj
			self.m_root.SetEngine(self.m)
		else:
			self.GetRootObject().AddChild(obj)