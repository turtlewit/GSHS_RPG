
class Command:
	command_dict = {}
	name_dict = {}
	command_list = []

	def __init__(self, command, flag, previous_command = None):
		self.flag = flag
		self.command = command
		if previous_command:
			self.independant = False
			self.previous_command = previous_command
		else:
			self.independant = True
			self.previous_command = None

		self.command_dict[self.command] = self.flag
		self.name_dict[self.command] = self
		self.command_list.append(self.command)

def init():

	#Previous commands must be listed first

	command_list = [
	['move', 	'MOVE_EMPTY'					],
	['go',		'MOVE_EMPTY'					],
	['north', 	'MOVE_NORTH', 	'MOVE_EMPTY'	],
	['n',	 	'MOVE_NORTH', 	'MOVE_EMPTY'	],
	['south', 	'MOVE_SOUTH', 	'MOVE_EMPTY'	],
	['s',	 	'MOVE_SOUTH', 	'MOVE_EMPTY'	],
	['east', 	'MOVE_EAST',	'MOVE_EMPTY'	],
	['e',	 	'MOVE_EAST',	'MOVE_EMPTY'	],
	['west',	'MOVE_WEST',	'MOVE_EMPTY'	],
	['w',		'MOVE_WEST',	'MOVE_EMPTY'	]
	]

	for command in command_list:
		if len(command) == 2:
			Command(command[0], command[1])
		else:
			Command(command[0], command[1], command[2])




def get_input():
	flag_list = []
	commands = []

	global flags

	inp = input(str('>'))
	inp_split = inp.split()
	extra = []

	for i, word in enumerate(inp_split):
		not_lower = word
		word = word.lower()
		if word in Command.command_list:
			if Command.name_dict[word].independant:
				commands.append(Command.name_dict[word])
			else:
				try:
					if Command.name_dict[inp_split[i-1]].flag == Command.name_dict[word].previous_command:
						commands.append(Command.name_dict[word])
					else:
						extra.append(not_lower)
				except:
					extra.append(not_lower)

	extra = ' '.join(extra)
	return commands

