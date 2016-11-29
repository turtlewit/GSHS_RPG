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
		self.m_active = False

	def Update(self):
		if self.m_parent.m_engine.m_game.m_root.m_player.m_parent.m_transform == self.m_parent.m_transform and self.m_parent.m_engine.m_game.m_root.m_player.m_spaceTransform == self.m_parent.m_parent.m_parent.m_transform:
			self.m_active = True
		if self.m_enabled and self.m_active:
			self.Update2()

	def Update2(self):
		pass