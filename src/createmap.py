import os
class CreateMap:
	def Create(world, player):
		log_file = open(os.path.join('data', 'logs', 'maplog.log'), 'w')
		for child in world.m_children:
			log_file.write("%s\n" % str(child))
		xBounds = (0,0)
		yBounds = (0,0)

		mapText = ""

		for child1 in world.m_children:
			if child1.m_components[0].m_type == 'tile':
				if child1.m_transform[0] < xBounds[0]:
					xBounds = (child1.m_transform[0], xBounds[1])
					log_file.write("%s %s min x\n" % (child1.m_components[0].m_name, str(child1.m_transform)))
				elif child1.m_transform[0] > xBounds[1]:
					xBounds = (xBounds[0], child1.m_transform[0])
					log_file.write("%s %s max x\n" % (child1.m_components[0].m_name, str(child1.m_transform)))
				if child1.m_transform[1] < yBounds[0]:
					yBounds = (child1.m_transform[1], yBounds[1])
					log_file.write("%s %s min y\n" % (child1.m_components[0].m_name, str(child1.m_transform)))
				elif child1.m_transform[1] > yBounds[1]:
					yBounds = (yBounds[0], child1.m_transform[1])
					log_file.write("%s %s max y\n" % (child1.m_components[0].m_name, str(child1.m_transform)))

		log_file.write("%s%s\n" % (str(xBounds), str(yBounds)))
		tileFound = False
		for y in range(yBounds[1], yBounds[0] - 1, -1):
			for x in range(xBounds[0], xBounds[1] + 1):
				tileFound = False
				for child1 in world.m_children:
					if child1.m_components[0].m_type == "tile":
						if child1.m_transform == player.m_parent.m_transform and child1.m_transform == (x,y):
							mapText += 'P'
							tileFound = True
						elif child1.m_transform == (x,y):
							mapText += 't'
							tileFound = True
				if tileFound == False:
					mapText += ' '
					log_file.write("%s\n" % str((x,y)))
			mapText += '\n'
		log_file.write(mapText)
		log_file.close()
		return mapText