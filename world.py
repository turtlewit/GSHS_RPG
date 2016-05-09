
class Tile:
	# tile_list_dictionary = {}		#Stores the index location of the list of tiles for each parent world.
	# tile_list_list = []				#This is required, as each tile list needs to be attached to the parent. The class will look in the dictionary to see if the parent has a tile list. If it does not, add it to this list.
	def __init__(self, parent, name, location, desc):
		self.parent = parent
		self.name = name
		self.location = location
		self.description = desc

		parent.tile_list.append(self)
		parent.tile_dictionary[location] = self

		# try:
		# 	self.tile_list_list[self.tile_list_dictionary[parent]].append(self)
		# except:
		# 	self.tile_list_list.append([self])
		# 	self.tile_list_dictionary[parent] = len(self.tile_list_list) - 1

class World:
	world_name_dictionary = {}
	world_dictionary = {}
	world_list = []

	def __init__(self,name,location,s_desc,l_desc):
		self.name = name
		self.location = location
		self.space_description = s_desc
		self.landing_description = l_desc

		self.tile_list = []
		self.tile_dictionary = {}

		self.world_name_dictionary[self.name] = self
		self.world_dictionary[location] = self
		self.world_list.append(self)
