

from src.textitem import TextItem
from AdventureEngine.CoreEngine.input import Input

class SignPost(TextItem):

	def __init__(self, groundDescription, inspectDescription, name="signpost", canBeDestroyed=True):

		TextItem.__init__(self, name)

		self.destroyed = False
		self.canBeDestroyed = canBeDestroyed

		self.m_groundDescription = groundDescription
		self.m_inspectDescription = inspectDescription

	def Update2(self):
		if self.canBeDestroyed:
			if Input.command:
				if type(Input().command) is str:
					if Input.command.lower() == "destroy %s" % self.m_name:
						self.destroyed = True
						self.m_groundDescription = "There is a destroyed signpost here.\nYou can get rid of this signpost by typing 'clear signpost'"
						self.m_inspectDescription = "The signpost lies in pieces scattered across the ground."

					if Input.command.lower() == "clear %s" % self.m_name and self.destroyed:
						self.m_enabled = False

			