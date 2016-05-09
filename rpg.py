"""The main file of the GSHS_RPG game."""

import os, sys

from player import Player
import world

map_dir = os.path.join('data', 'maps')

#Dude, I couldn't even fully explain how this parses text, but it does, so whatever.
def load_map(map_file_name):
	map_file = open(os.path.join(map_dir, map_file_name))

	possible_attributes = ['space_description', 'landing_description', 'location', 'parent', 'description']

	possible_types = ['WORLD', 'TILE']

	object_attributes = {}
	inside_definition=0

	returnstuff = []

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
			line = line.split()
			line = ''.join(line)
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

				object_name = list(line[1])
				object_attributes['type'] = (line[0])
				object_attributes['name'] = (''.join(object_name))

			if '{' in line:
				inside_definition=1

	for i in returnstuff:
		world_or_tile = i['type']

		if world_or_tile == 'WORLD':
			name = i['name']
			s_desc = i['space_description']
			l_desc = i['landing_description']
			location = i['location']

			world.World(name,location,s_desc,l_desc)
		if world_or_tile == 'TILE':
			parent = i['parent']
			desc = i['description']
			location = i['location']

			world.Tile(world.World.world_name_dictionary[parent], name, location, desc)






def lineConvert(line):
	line = line.split()
	linelen = 0
	word = line.pop(0)
	wordsplit = list(word)
	linelen += len(wordsplit) + 1
	newLine = word
	for x in range(0, len(line)):
		word = line.pop(0)
		wordsplit = list(word)
		linelen += len(wordsplit) + 1
		if linelen > 79:
			newLine = "%s\n" % (newLine)
			linelen = 0
			newLine = "%s%s" % (newLine, word)
			linelen += len(wordsplit) + 1
		else:
			newLine = "%s %s" % (newLine, word)
	return newLine

# Startup init

player = Player()

load_map('example.map')

print(world.World.world_list, world.World.world_list[0].tile_list)