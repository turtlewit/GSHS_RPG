
class Command:
	command_dict = {}
	name_dict = {}
	command_list = []

	def __init__(self, command, flag, previous_command = None):
		self.flag = flag
		self.command = command
		if previous_command:
			self.independant = False
			self.previous_command = self.name_dict[previous_command]
		else:
			self.independant = True
			self.previous_command = None

		self.command_dict[self.command] = self.flag
		self.name_dict[self.command] = self
		self.command_list.append(self.command)

def init():

	#Previous commands must be listed first

	command_list = [
	['move', 	'MOVE_EMPTY'			],
	['north', 	'MOVE_NORTH', 	'move'	],
	['south', 	'MOVE_SOUTH', 	'move'	],
	['east', 	'MOVE_EAST',	'move'	],
	['west',	'MOVE_WEST',	'move'	]
	]

	for command in command_list:
		if len(command) == 2:
			Command(command[0], command[1])
		else:
			Command(command[0], command[1], command[2])

	print (Command.command_dict)



def get_input(conditions):
	print_list = []
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
			print('yea')
			if Command.name_dict[word].independant:
				commands.append(Command.name_dict[word])
			else:
				try:
					if Command.name_dict[inp_split[i-1]] == Command.name_dict[word].previous_command:
						commands.append(Command.name_dict[word])
					else:
						extra.append(not_lower)
				except:
					extra.append(not_lower)

	extra = ' '.join(extra)
	print (commands, extra)

init()
get_input(None)