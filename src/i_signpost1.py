

from src.textitem import TextItem
from AdventureEngine.CoreEngine.input import Input

class ISignPost(TextItem):

	def __init__(self):

		TextItem.__init__(self, "signpost")

		self.destroyed = False

		self.m_groundDescription = "There is a sign post sticking out of the floor here.\n(Type 'inspect signpost' to inspect the sign post)"
		self.m_inspectDescription = "The signpost reads:\nI am but a little signpost! It would be a shame if someone came along and typed 'destroy signpost'!"

	def Update2(self):
		if Input.command:
			if type(Input().command) is str:
				if Input.command.lower() == "destroy %s" % self.m_name:
					self.destroyed = True
					self.m_groundDescription = "There is a destroyed signpost here.\nYou can get rid of this signpost by typing 'clear signpost'"
					self.m_inspectDescription = "The signpost lies in pieces scattered across the ground."

				if Input.command.lower() == "clear %s" % self.m_name and self.destroyed:
					self.m_enabled = False

			