"""TextItem class

This file contains the TextItem class, which describes a basic text item. 
"""

from AdventureEngine.components.item import Item
from AdventureEngine.CoreEngine.input import Input


class TextItem(Item):

	def __init__(self, name):

		Item.__init__(self, name)

		self.m_groundDescription = None
		self.m_inspectDescription = None