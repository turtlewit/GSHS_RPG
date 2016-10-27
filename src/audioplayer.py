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
			
			if worldDifference:
				if self.player.world.m_music:
					self.audio.LoadSong(self.player.world.m_name, os.path.join('data', 'audio', self.player.world.m_music))
					self.audio.PlaySong(self.player.world.m_name)
				else:
					self.audio.StopMusic()

