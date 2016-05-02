"""The main file of the GSHS_RPG game."""

import os, sys

map_dir = os.path.join('data', 'maps')

def load_map(map_file_name):
	map_file_raw = open(os.path.join(map_dir, map_file_name))
	map_file = map_file_raw.read()
	map_file = map_file.split('\n')
	value_type = 0
	location = None
	ldesc = None
	sdesc = None
	returnList = []
	lineNumber = 0
	for line in map_file:

		split_line = line.split()

		if len(split_line) > 0:

			if value_type == 1:

				if split_line[0] == 'location':
					loc_value = list(split_line[1])
					comma_pos = loc_value.index(',')
					loc_value.remove(',')
					loc_value.insert(comma_pos, ' ')
					loc_value = ' '.join(loc_value)
					loc_value = loc_value.split()
					# new_value1 = ""
					# new_value2 = ""
					# for i in range(0, len(loc_value)):
					# 	if i == comma_pos:
					# 		new_value1 = int(new_value)
					# 		new_value = ""
					# 		i += 1
					# 	new_value = "%s%s" % (new_value, loc_value[i])
					# new_value2 = int(new_value)
					location = (loc_value[0], loc_value[1])

				if split_line[0] in ['ldesc', 'sdesc']:
					descType = split_line.pop(0)
					desc = split_line
					last_word = desc[len(desc) - 1]
					while list(last_word)[len(last_word) - 1] != "\"":
						nextLine = map_file[lineNumber + 1]
						desc.append('\n')
						newLineDesc = nextLine.split()
						for word in newLineDesc:
							desc.append(word)
						last_word = desc[len(desc) - 1]
					desc = ' '.join(desc)

					if descType == 'ldesc':
						ldesc = desc

					else:
						sdesc = desc


				if split_line[0] == 'end':
					returnList.append(location)
					returnList.append(ldesc)
					returnList.append(sdesc)
					location = None
					ldesc = None
					sdesc = None
					value_type = 0

			else:

				if split_line[0] == 'start':
					value_type = 1

				if split_line[0] == 'stop':
					return returnList
		lineNumber = lineNumber + 1




