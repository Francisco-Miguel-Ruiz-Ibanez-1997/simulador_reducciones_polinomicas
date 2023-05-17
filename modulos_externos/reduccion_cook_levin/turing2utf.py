#QUE HACE: CONVERTIR UNA MT DE J-FLAP A TEXTO.

#FORMATO del TXT:
# linea 1: alfabeto de entrada
# linea 2: alfabeto de la cinta
# linea 3: simbolo que representa un espacio en blanco en la cinta
# linea 4: conjunto de estados totales
# linea 5: estado inicial
# linea 6: conjunto de estados finales
# linea 7: cantidad de fitas
# lineas 8 en adelante: transiciones, una por linea, no formato estado atual, nuevo estado y, para cada cinta,  simbolo atual, nuevo simbolo, direccion para mover la cabeca

from string import ascii_uppercase
#from typing_extensions import Self
from xml.etree import ElementTree as ET
import csv
import sys

#clase transicion
class Transition(object):
	def __init__(self):
		self.currentState = None
		self.newState = None
		self.tapeMovements = []

	def __lt__(self, other):
		if self.currentState < other.currentState:
			return True
		elif self.currentState > other.currentState:
			return False
		elif self.newState < other.newState:
			return True
		elif self.newState > other.newState:
			return False
		else:
			return self.newState < other.newState

# Clase movimiento de la cinta; los necesita para la clase transición
class TapeMovement(object):
	def __init__(self):
		self.tape = 1
		self.currentTapeSymbol = None
		self.newTapeSymbol = None
		self.headDirection = None

	def __lt__(self, other):
		if self.currentTapeSymbol < other.currentTapeSymbol:
			return True
		elif self.currentTapeSymbol > other.currentTapeSymbol:
			return False
		elif self.newTapeSymbol < other.newTapeSymbol:
			return True
		elif self.newTapeSymbol > other.newTapeSymbol:
			return False
		else:
			return self.headDirection < other.headDirection

# esta clase coge un objeto JFLAP y lo pasa a texto (UTF)
class Jflap2Utfpr(object):

    #Crea al incio un objeto vacio de su clase
	def __init__(self):
		self.alphabet = set()
		self.states = set()
		self.tapeSymbols = set()
		self.tapes = 1
		self.initialState = None
		self.finalStates = set()
		self.transitions = set()    #aqui va a haber un conjunto de transiciones
		self.singleTape = False
		

    #Añadido: hastag, quiero que no se use a la hora de la creación de la tabla
	def convert(self, inputFile, outputFile, blankSymbol = 'B', alphabet = None, hastagSymbol = '#'):
		try: 
			xmldoc = ET.parse(inputFile)
		except FileNotFoundError:
			print("El archivo introducido no existe")
			exit()

		root = xmldoc.getroot()
		if root.find('tapes') == None:
			self.singleTape = True
			self.tapes = 1
		else:
			self.tapes = int(root.find('tapes').text)

		tm = root.find('automaton')
		stateElementName = 'block'
		if tm == None:  # Old JFLAP format
			tm = root
			stateElementName = 'state'

		# Discover states
		for s in tm.findall(stateElementName):
			state = s.attrib['id']
			self.states.add(state)
			if s.find('initial') is not None:
				self.initialState = state
			if s.find('final') is not None:
				self.finalStates.add(state)

		# Discover tape alphabet (and fix blank symbol if required)
		for t in tm.findall('transition'):
			tapeXPath = ''
			for i in range(1, self.tapes + 1):
				if not self.singleTape: # Workaround for handling single and multitape Turing machines
					tapeXPath = "[@tape='" + str(i) + "']"
				if t.find("read" + tapeXPath).text is not None:
					self.tapeSymbols.add(t.find("read" + tapeXPath).text)
				if t.find("write" + tapeXPath).text is not None:
					self.tapeSymbols.add(t.find("write" + tapeXPath).text)
		for s in self.tapeSymbols:
			#añadido
			if s == hastagSymbol:	#Si "#" está en el alfabeto, lo cambiamos
				newHastagSymbol=''
				for c in ascii_uppercase:
					if c not in self.tapeSymbols:
						newHastagSymbol = c
						break
				self.tapeSymbols.remove(hastagSymbol)
				self.tapeSymbols.add(newHastagSymbol)
				print("El símbolo # es un símbolo protegido, se va a realizar un cambio de simbolo, '#' se cambia por \'" + newHastagSymbol + "\'")
			if s == blankSymbol:
				oldBlankSymbol = blankSymbol
				for c in ascii_uppercase:	#se añade comprobación para que no se ponga el simbolo hastag
					if c not in self.tapeSymbols and c is not hastagSymbol:
						blankSymbol = c
						break
				print("Símbolo elegido para representar el blanco (" + oldBlankSymbol + ") se utilizó para otros fines en la máquina. El símbolo del blanco ha sido sustituido por " + blankSymbol + ".")
		self.blankSymbol = blankSymbol
		self.tapeSymbols.add(self.blankSymbol)

		for t in tm.findall('transition'):
			transition = Transition()
			self.transitions.add(transition)
			transition.currentState = t.find('from').text
			transition.newState = t.find('to').text
			tapeXPath = ''
			for i in range(1, self.tapes + 1):
				movement = TapeMovement()
				transition.tapeMovements.append(movement)
				movement.tape = i
				if not self.singleTape: # Workaround for handling single and multitape Turing machines
					tapeXPath = "[@tape='" + str(i) + "']"
				if t.find("read" + tapeXPath).text is not None:
					movement.currentTapeSymbol = t.find("read" + tapeXPath).text
					if movement.currentTapeSymbol is hastagSymbol:
						movement.currentTapeSymbol = newHastagSymbol
				else:
					movement.currentTapeSymbol = self.blankSymbol
				if t.find("write" + tapeXPath).text is not None:
					movement.newTapeSymbol = t.find("write" + tapeXPath).text
					if movement.newTapeSymbol is hastagSymbol:
						movement.newTapeSymbol = newHastagSymbol
				else:
					movement.newTapeSymbol = self.blankSymbol
				movement.headDirection = t.find("move" + tapeXPath).text

		if alphabet is None:
			self.alphabet = self.tapeSymbols.copy()
			self.alphabet.remove(self.blankSymbol)
		else:
			self.alphabet = alphabet

        # En esta parte del codigo mete la traducción en un archivo de salida de texto.
        # no se si quiero esto, voy a intentar obtener un objeto del tipo que es este.
		with open(outputFile, 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=' ', lineterminator='\n')
			writer.writerow(sorted(self.alphabet))
			writer.writerow(sorted(self.tapeSymbols))
			writer.writerow([self.blankSymbol])
			writer.writerow(sorted(self.states))
			writer.writerow(self.initialState)
			writer.writerow(sorted(self.finalStates))
			writer.writerow([self.tapes])
			for transition in sorted(self.transitions):
				transitionDescription = []
				transitionDescription.append(transition.currentState)
				transitionDescription.append(transition.newState)
				for i in range(1, self.tapes+1):
					for movement in sorted(transition.tapeMovements):
						if movement.tape == i:
							transitionDescription.append(movement.currentTapeSymbol)
							transitionDescription.append(movement.newTapeSymbol)
							transitionDescription.append(movement.headDirection)
				writer.writerow(transitionDescription)
        

        