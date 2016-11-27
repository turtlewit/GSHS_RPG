"""Item class

This class describes the basic definition of an item.
"""
from AdventureEngine.components.gamecomponent import GameComponent

class Item(GameComponent):

	def __init__(self, name = None):

		GameComponent.__init__(self)
		self.m_name = name
		self.m_type = "item"

		self.m_groundDescription = None
		self.m_inspectDescription = None

		self.m_canBePickedUp = False
		self.m_enabled = True

	def Update(self):
		if self.m_enabled:
			self.Update2()

	def Update2(self):
		pass