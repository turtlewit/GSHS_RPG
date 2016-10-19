from AdventureEngine.CoreEngine.engine import Engine
from GSHS_RPG import GSHS_RPG

class Main:

	def __init__(self):
		engine = Engine(GSHS_RPG())
		engine.InitRenderer("Test")
		engine.Start()


if __name__ == "__main__":
	Main()