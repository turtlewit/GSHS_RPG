from AdventureEngine.CoreEngine.game import Game
from AdventureEngine.render.renderer import Renderer
from AdventureEngine.CoreEngine.input import Input
class Engine:
	def __init__(self,game):
		self.m_isRunning = False
		self.m_game = game
		self.m_renderingEngine = None
		game.SetEngine(self);

	def InitRenderer(self,name):
		self.m_renderingEngine = Renderer(name)
		self.m_game.SetRenderer(self.m_renderingEngine)
		Input().renderer = self.m_renderingEngine

	def Start(self):
		if self.m_isRunning:
			return

		self.Run()

	def Stop(self):
		if self.m_isRunning == False:
			return

		self.m_isRunning = False

	def Run(self):
		self.m_isRunning = True

		self.m_game.Initialize()

		while(self.m_isRunning):
			Input().Update(self.m_renderingEngine)

			self.m_game.Update()

			#self.m_game.Render(self.m_renderingEngine)
			self.m_renderingEngine.Render()

		self.m_renderingEngine.Cleanup()

