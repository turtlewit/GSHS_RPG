from AdventureEngine.CoreEngine.engine import Engine
from GSHS_RPG import GSHS_RPG
import os

class Main:

	def __init__(self):
		if not os.path.exists(os.path.join('data', 'logs')):
			os.makedirs(os.path.join('data', 'logs'))

		engine = Engine(GSHS_RPG())
		engine.InitRenderer("Test")
		engine.Start()


if __name__ == "__main__":
	Main()