"""The main file of the GSHS_RPG game."""

import os, sys

from player import Player

map_dir = os.path.join('data', 'maps')

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
			else:

				line.split('=')

				if line[0] in possible_attributes and len(line) == 2:
					object_attributes[line[0]] = line[1]


		else:
			line = raw(line.split(':'))
			print(line)
			if line[0] in possible_types and len(line) == 2:

				object_name = list(line[1])

				while '\"' != object_name[0]:
					try:
						object_name.pop(0)
					except:
						print("Syntax error! Could not load world!")
						break
				object_attributes['type'] = (line[0])
				object_attributes['name'] = (''.join(object_name))

			if '{' in line:
				inside_definition=1

	return(returnstuff)


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

