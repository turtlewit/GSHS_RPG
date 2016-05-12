"""The main file of the GSHS_RPG game."""

import os, sys, platform
import colorama
colorama.init()

from player import Player
import world
import command

current_os 	= platform.system()

if current_os == 'Windows':
	import msvcrt as m

map_dir = os.path.join('data', 'maps')

#Dude, I couldn't even fully explain how this parses text, but it does, so whatever.
#---------------------------------------------------------------------------------------------------------------#
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
				print(object_name)
				object_name = ' '.join(object_name)
				object_name = list(object_name)
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
			location = (int(i['location'][0]),int(i['location'][2]))
			print(name)
			world.World(name,location,s_desc,l_desc)
		if world_or_tile == 'TILE':
			name = i['name']
			parent = i['parent']
			desc = i['description']
			location = (int(i['location'][0]),int(i['location'][2]))

			world.Tile(world.World.world_name_dictionary[parent], name, location, desc)
#---------------------------------------------------------------------------------------------------------------#


def lineConvert(line):
	global buffer_x
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
		if linelen > buffer_x - 2:
			newLine = "%s\n" % (newLine)
			linelen = 0
			newLine = "%s%s" % (newLine, word)
			linelen += len(wordsplit) + 1
		else:
			newLine = "%s %s" % (newLine, word)
	return newLine


def setup_screen(textl, player, current_world, current_tile):
	if current_os == "Windows":
		os.system('cls')
	else:
		os.system('printf "\\033c"')

	global buffer_x
	global buffer_y

	print(colorama.Fore.BLACK + colorama.Back.WHITE + "[Health: %d, Position: (%d,%d): \"%s\" on \"%s\"]" % (player.health, player.local_position[0], player.local_position[1], current_tile.name, current_world.name) + colorama.Style.RESET_ALL)

	current_lines = 0
	for text in textl:
		text_list = list(text)
		text_split = text.split('\n')

		if text_list.count('\n') >= buffer_y - 1:
			for i in range(0, buffer_y - 3):
				print(text_split[i])

			print('Press any key to continue...')

			if current_os == 'Windows':
				m.getch()
			else:
				input()

			for i in range(buffer_y - 2, len(text_split)):
				print(text_split[i])
		else:
			print(text)
		current_lines += len(text_split) + 1
		print('')

	if current_lines < buffer_y - 2:
		for i in range(0, (buffer_y - 2) - current_lines):
			print('')




# Startup init

command.init()

buffer_x	= 80
buffer_y	= 25

print_list = []

player = Player()

load_map('example.map')

print('World position', world.World.world_list[0].location)
while True:
	current_world = world.find_world(player.global_position)
	current_tile = world.find_tile(player.local_position, current_world)
	print_list.append(lineConvert(current_tile.description))

	setup_screen(print_list, player, current_world, current_tile)
	print_list = []

	flags = command.get_input(None)
	for i, flag in enumerate(flags):
		if flag.flag == 'MOVE_EMPTY':
			try:
				if flags[i + 1].flag == 'MOVE_NORTH':
					player.move(0, 1)
					print_list.append('You move north.')
				elif flags[i + 1].flag == 'MOVE_SOUTH':
					player.move(1, 1)
					print_list.append('You move south.')
				elif flags[i + 1].flag == 'MOVE_EAST':
					player.move(2, 1)
					print_list.append('You move east.')
				elif flags[i + 1].flag == 'MOVE_WEST':
					player.move(3, 1)
					print_list.append('You move west.')
				else:
					print_list.append('Move where?')
			except:
				print_list.append('Move where?')