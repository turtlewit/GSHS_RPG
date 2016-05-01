"""The main file of the GSHS_RPG game."""

import os, sys

map_dir = os.path.join('data', 'maps')

def load_map(map_file_name):
	map_file = open(os.path.join(map_dir, map_file_name))
	value_type = 0
	location = None;
	ldesc = None;
	sdesc = None;
	for line in map_file:
		split_line = line.split()
		if value_type == 1:

			if split_line[0] == 'location':
				loc_value = list(split_line[1])
				comma_pos = loc_value.index(',')
				new_value1 = ""
				new_value2 = ""
				for i in range(0, len(loc_value)):
					if i == comma_pos:
						new_value1 = int(new_value)
						new_value = ""
						i += 1
					new_value = "%s%s" % (new_value, loc_value[i])
				new_value2 = int(new_value)
				location = (new_value1, new_value2)

