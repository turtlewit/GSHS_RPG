import pygame.mixer

class Audio:

	def __init__(self):
		try:
			pygame.mixer.init()
			self.mixerInit = True
		except:
			self.mixerInit = False

		self.m_sounds = {}
		self.m_songs = {}
		self.m_currentSong = None

		self.m_queue = []

		self.m_volume = 1.0

	def LoadSound(self, name, file):
		if self.mixerInit:
			self.m_sounds[name] = pygame.mixer.Sound(file)

	def LoadSong(self, name, file):
		if self.mixerInit:
			self.m_songs[name] = file

	def PlaySound(self, name, loops=0):
		if self.mixerInit:
			try:
				self.m_sounds[name].set_volume(self.m_volume)
				self.m_sounds[name].play()
			except:
				pass

	def StopPlayingSound(self, name, fadeout=False, fadeoutTime=1000):
		if self.mixerInit:
			try:
				self.m_sounds[name].stop()
			except:
				pass

	def Panic(self):
		if self.mixerInit:
			try:
				pygame.mixer.music.stop()
			except:
				pass

			for sound in self.m_sounds:
				try:
					sound.stop()
				except:
					pass

	def PlaySong(self, name, loops=-1, startTime=0.0):
		if self.mixerInit:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.stop()

			pygame.mixer.music.load(self.m_songs[name])
			self.m_currentSong = name
			pygame.mixer.music.play(loops, startTime)
	def StopMusic(self):
		if self.mixerInit:
			self.m_currentSong = None
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.stop()


