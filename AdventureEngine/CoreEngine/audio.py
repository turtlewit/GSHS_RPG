import simpleaudio as sa


class Audio:

	def __init__(self):


		self.m_sounds = {}
		self.m_songs = {}
		self.m_currentSong = None
		self.m_currentSongPlayObject = None
		self.m_currentSoundPlayObjects = {}

		self.m_queue = []

		self.m_volume = 1.0

	def LoadSound(self, name, file):


		self.m_sounds[name] = sa.WaveObject.from_wave_file(file)

	def LoadSong(self, name, file):


		self.m_songs[name] = sa.WaveObject.from_wave_file(file)

	def PlaySound(self, name, loops=0):


		# Cleanup before playing sound
		for obj in self.m_currentSoundPlayObjects.copy():
			if not obj.is_playing():
				self.m_currentSoundPlayObjects.pop(obj)


		self.m_currentSoundPlayObjects[name] = (self.m_sounds[name].play())

	def StopPlayingSound(self, name, fadeout=False, fadeoutTime=1000):


		self.m_currentSoundPlayObjects[name].stop()
		self.m_currentSoundPlayObjects.pop(name)

	def Panic(self):

		for obj in self.m_currentSoundPlayObjects:
			obj.stop()

		self.m_currentSoundPlayObjects = {}

	def PlaySong(self, name, loops=-1, startTime=0.0):

		if not self.m_currentSongPlayObject:
			self.m_currentSongPlayObject = self.m_songs[name].play()
		else:
			self.m_currentSongPlayObject.stop()
			self.m_currentSongPlayObject = self.m_songs[name].play()

		self.m_currentSong = name

	def StopMusic(self):

		if self.m_currentSongPlayObject:
			self.m_currentSongPlayObject.stop()
			self.m_currentSongPlayObject = None

		self.m_currentsong = None


