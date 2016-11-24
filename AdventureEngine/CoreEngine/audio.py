import simpleaudio as sa


class Audio:

	def __init__(self):

		# try:
		# 	pygame.mixer.init()
		# 	self.mixerInit = True
		# except:
		# 	self.mixerInit = False

		self.m_sounds = {}
		self.m_songs = {}
		self.m_currentSong = None
		self.m_currentSongPlayObject = None
		self.m_currentSoundPlayObjects = {}

		self.m_queue = []

		self.m_volume = 1.0

	def LoadSound(self, name, file):

		# if self.mixerInit:
		# 	self.m_sounds[name] = pygame.mixer.Sound(file)

		self.m_sounds[name] = sa.WaveObject.from_wave_file(file)

	def LoadSong(self, name, file):
		# if self.mixerInit:
		# 	self.m_songs[name] = file

		self.m_songs[name] = sa.WaveObject.from_wave_file(file)

	def PlaySound(self, name, loops=0):
		# if self.mixerInit:
		# 	try:
		# 		self.m_sounds[name].set_volume(self.m_volume)
		# 		self.m_sounds[name].play()
		# 	except:
		# 		pass

		# Cleanup before playing sound
		for obj in self.m_currentSoundPlayObjects.copy():
			if not obj.is_playing():
				self.m_currentSoundPlayObjects.pop(obj)


		self.m_currentSoundPlayObjects[name] = (self.m_sounds[name].play())

	def StopPlayingSound(self, name, fadeout=False, fadeoutTime=1000):
		# if self.mixerInit:
		# 	try:
		# 		self.m_sounds[name].stop()
		# 	except:
		# 		pass

		self.m_currentSoundPlayObjects[name].stop()
		self.m_currentSoundPlayObjects.pop(name)

	def Panic(self):
		# if self.mixerInit:
		# 	try:
		# 		pygame.mixer.music.stop()
		# 	except:
		# 		pass

		# 	for sound in self.m_sounds:
		# 		try:
		# 			sound.stop()
		# 		except:
		# 			pass

		for obj in self.m_currentSoundPlayObjects:
			obj.stop()

		self.m_currentSoundPlayObjects = {}

	def PlaySong(self, name, loops=-1, startTime=0.0):
		# if self.mixerInit:
		# 	if pygame.mixer.music.get_busy():
		# 		pygame.mixer.music.stop()

		# 	pygame.mixer.music.load(self.m_songs[name])
		# 	self.m_currentSong = name
		# 	pygame.mixer.music.play(loops, startTime)

		if not self.m_currentSongPlayObject:
			self.m_currentSongPlayObject = self.m_songs[name].play()
		else:
			self.m_currentSongPlayObject.stop()
			self.m_currentSongPlayObject = self.m_songs[name].play()

		self.m_currentSong = name

	def StopMusic(self):
		# if self.mixerInit:
		# 	self.m_currentSong = None
		# 	if pygame.mixer.music.get_busy():
		# 		pygame.mixer.music.stop()

		if self.m_currentSongPlayObject:
			self.self.m_currentSongPlayObject.stop()
			self.self.m_currentSongPlayObject = None

		self.m_currentsong = None


