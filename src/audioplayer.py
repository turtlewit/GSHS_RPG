from AdventureEngine.components.gamecomponent import GameComponent
import os

class AudioPlayer(GameComponent):
	def __init__(self):
		self.m_name = "AudioPlayer"
		GameComponent.__init__(self)
		self.play = True
		self.player = None
		self.audio = None


	def Update(self):
		if self.audio == None:
			self.audio = self.m_parent.m_engine.m_audio
		if self.player == None:
			for component in self.m_parent.m_components:
				if component.m_name == "player":
					self.player = component
		if self.play == True and self.player != None:
			worldDifference = self.player.worldDifference
			
			if self.player.m_parent.m_engine.m_game.m_root.stctrl.GetState().m_name == ("explore" or "map"):
				if self.player.world.m_music:
					if self.audio.m_currentSong != self.player.world.m_name:
						self.audio.LoadSong(self.player.world.m_name, os.path.join('data', 'audio', self.player.world.m_music))
						self.audio.PlaySong(self.player.world.m_name)
				else:
					self.audio.StopMusic()

			if self.player.m_parent.m_engine.m_game.m_root.stctrl.GetState().m_name == "default" and self.audio.m_currentSong != "menu":
				self.audio.LoadSong("menu", os.path.join('data', 'audio', 'menu.mp3'))
				self.audio.PlaySong("menu")


