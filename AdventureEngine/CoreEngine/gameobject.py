

class GameObject:

	def __init__(self):
		self.m_children = []
		self.m_components = []
		self.m_transform = (0,0)
		self.m_parent = None
		self.m_engine = None
		self.m_renderer = None

	def AddComponent(self, component):
		self.m_components.append(component)
		component.SetParent(self)

		return self

	def AddChild(self, child):
		self.m_children.append(child)
		child.m_engine = self.m_engine
		child.m_renderer = self.m_renderer
		child.m_parent = self

	def Update(self):
		for component in self.m_components:
			component.Update()

	def UpdateAll(self):
		self.Update()

		for child in self.m_children:
			child.UpdateAll()

	def SetEngine(self,engine):
		self.m_engine = engine

	def SetRenderer(self,renderer):
		self.m_renderer = renderer

	
