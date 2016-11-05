import os
import AdventureEngine.components.world as world
from AdventureEngine.CoreEngine.gameobject import GameObject


class Map:

	def __init__(self):
		self.Worlds = []
		self.mapFiles = []

	def Walking(self,directory):

		for root, dirs, files in os.walk(directory):
			for file in files:
				for file in files:
					if file.endswith('.map'):
						path = os.path.join(root)
						if file == "world.map":
							if os.path.join(path,file) not in self.mapFiles:
								self.mapFiles.insert(0, os.path.join(path,file))
						else:
							if os.path.join(path,file) not in self.mapFiles:
								self.mapFiles.append(os.path.join(path,file))
			for adir in dirs:
				self.Walking(adir)

	def LoadMapsInDirectory(self, directory, log_file):
		log_file = open(os.path.join(log_file), 'w')
		self.Walking(directory)
		#mapFiles = []
		# for root, dirs, files in os.walk(directory):
		# 	for file in files:
		# 		if file.endswith('.map'):
		# 			path = os.path.join(root)
		# 			for adir in dirs:
						
		# 				path = os.path.join(path, adir)
		# 				try:
		# 					log_file.write(file)
		# 					open(os.path.join(path,file))
		# 					close(os.path.join(path,file))

		# 					if file == "world.map":
		# 						if os.path.join(path,file) not in mapFiles:
		# 							mapFiles.insert(0, os.path.join(path,file))
		# 					else:
		# 						if os.path.join(path,file) not in mapFiles:
		# 							mapFiles.append(os.path.join(path,file))
		# 				except:
		# 					log_file.write("\n%s probably doesn't exist." % str(os.path.join(path,file)))

		#log_file.write(str(self.mapFiles))
		for loopNumber in range(0, 2):

			for map_file_name in self.mapFiles:

				map_file = open(os.path.join(map_file_name))
				log_file.write("%s\n" % map_file_name)
				possible_attributes = [	'space_description', 'landing_description', 'music', 'location', 'parent', 'description',
									'move_east_message','move_west_message','move_north_message','move_south_message']

				possible_types = ['WORLD', 'TILE']

				object_attributes = {}
				inside_definition=0

				returnstuff = []

				#self.World = None


				for line in map_file:

					if inside_definition==1:

						if '}' in list(line):
							returnstuff.append(object_attributes)
							object_attributes = {}
							inside_definition = 0
						else:
							line = line.split('\t')
							line = ''.join(line)
							line = line.split('\n')
							line = ''.join(line)
							line = line.split('=')
							try:
								line2 = list(line[1])
								for i in range(0, line2.count('\"')):
									line2.remove('\"')
								line2 = ''.join(line2)
								line = [line[0], line2]
							except:
								pass

							if line[0] in possible_attributes and len(line) == 2:
								object_attributes[line[0]] = line[1]
							else:
								log_file.write("\nLINEDETAILS %s\n" % str(line))


					else:
						line = line.split()
						line = ' '.join(line)
						line = line.split(':')
						try:
							line2 = list(line[1])
							for i in range(0, line2.count('\"')):
								line2.remove('\"')
							line2 = ''.join(line2)
							line = [line[0], line2]
						except:
							pass
						if line[0] in possible_types and len(line) == 2:
							object_name = line[1].split()
							object_name = ' '.join(object_name)
							object_name = list(object_name)
							object_attributes['type'] = (line[0])
							object_attributes['name'] = (''.join(object_name))

						if '{' in line:
							inside_definition=1

				for i in returnstuff:
					# try:
						log_file.write("%s\n\n" % str(i))
						world_or_tile = i['type']

						if world_or_tile == 'WORLD' and loopNumber == 0:
							name = i['name']
							s_desc = i['space_description']
							l_desc = i['landing_description']
							try:
								musicname = i['music']
							except:
								musicname = None
							location = (int(i['location'].split(',')[0]), int(i['location'].split(',')[1]))
							#world.World(name,location,s_desc,l_desc)
							World = GameObject()
							World.m_transform = location
							worldComponent = world.World()
							worldComponent.m_spaceDescription = s_desc
							worldComponent.m_landingDescription = l_desc
							worldComponent.m_name = name
							worldComponent.m_music = musicname
							World.AddComponent(worldComponent)
							self.Worlds.append(World)
						if world_or_tile == 'TILE' and loopNumber == 1:
							#try:
								name2 = ' '.join(i['name'].split())
								parent = ' '.join(i['parent'].split())
								desc = ' '.join(i['description'].split())
								location = (int(i['location'].split(',')[0]), int(i['location'].split(',')[1]))

								try:
									move_north_message = i['move_north_message']
								except:
									move_north_message = None
								try:
									move_south_message = i['move_south_message']
								except:
									move_south_message = None
								try:
									move_east_message = i['move_east_message']
								except:
									move_east_message = None
								try:
									move_west_message = i['move_west_message']
								except:
									move_west_message = None

								direction_messages = [move_north_message, move_south_message, move_east_message, move_west_message]
								tileComponent = world.Tile(move_north_message, move_south_message, move_east_message, move_west_message, name2, desc)
								Tile = GameObject()
								Tile.m_transform = location
								Tile.AddComponent(tileComponent)
								for aworld in self.Worlds:
									for component in aworld.m_components:
										if component.m_name == parent:
											aworld.AddChild(Tile)

							# except:
							# 	log_file.write("Could not load tile %s.\n" % (i['name']))
					# except:
					# 	log_file.write("Could not load entity.\n\n%s\n\n" % str(returnstuff))
				map_file.close()
				log_file.write('\n')
				#log_file.write(str(self.Worlds))
		for aworld in self.Worlds:
			log_file.write("%s\n" % aworld.m_components[0].m_name)
			for atile in aworld.m_children:
				log_file.write("%s %s \n" % (atile.m_components[0].m_name, str(atile.m_transform)))
		log_file.write("\ndone")