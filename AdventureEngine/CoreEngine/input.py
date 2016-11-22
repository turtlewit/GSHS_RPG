import sys
import curses

class Input:

	#renderer = None

	commandHistory = []
	command = None
	unf_command = ""
	cheese = "cheese"
	takeTextInput = False
	char = None

	def Update(self, renderer):
		Input.command = None
		Input.char = None
		if renderer:
			currentCharacter = renderer.m_screen.getch()


			
			if currentCharacter != -1:
				Input.char = currentCharacter
				if Input.takeTextInput:
					if currentCharacter == ord('\n'):
						Input.commandHistory.insert(0,Input.command)
						Input.command = Input.unf_command
						renderer.m_cmd = ""
						Input.unf_command = ""

					if sys.platform == 'linux':
						if currentCharacter == 127:
							renderer.m_cmd = renderer.m_cmd[:-1]
							Input.unf_command = Input.unf_command[:-1]
					else:
						if currentCharacter == 8:
							renderer.m_cmd = renderer.m_cmd[:-1]
							Input.unf_command = Input.unf_command[:-1]

					if currentCharacter >=32 and currentCharacter <= 126:
						renderer.m_cmd += chr(currentCharacter)
						Input.unf_command += chr(currentCharacter)

					if currentCharacter in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
						Input.command = currentCharacter


