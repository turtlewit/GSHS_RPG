from AdventureEngine.components.gamecomponent import GameComponent

class World(GameComponent):
	def __init__(self):
		GameComponent.__init__(self)
		self.m_type = "world"
		self.m_spaceDescription = None
		self.m_landingDescription = None
		self.m_name = None
		self.m_music = None
		self.m_tileList = []

class Tile(GameComponent):
	def __init__(self, move_north_message=None, move_south_message=None, move_east_message=None, move_west_message=None, m_name=None, m_description=None):
		GameComponent.__init__(self)
		self.m_type = "tile"
		self.move_north_message = move_north_message
		self.move_south_message = move_south_message
		self.move_east_message = move_east_message
		self.move_west_message = move_west_message
		self.m_name = m_name
		self.m_description = m_description