import string
import random
import os

class PasswordGenerator( object ):
	classDefinitions = {
		'U': string.ascii_uppercase,
		'l': string.ascii_lowercase,
		'd': string.digits,
		'@': string.punctuation
	}

	defaultClasses = "Uld"

	def __init__( self ):
		self._classes = self.defaultClasses

	@property
	def classes(self):
		return self._classes
	@classes.setter
	def classes(self, value):
		for item in value:
			if not item in self.classDefinitions:
				raise RuntimeError( '%s is not a character class (try U, l, d or @)' )
		self._classes = value

	def generate( self, length = 16 ):
		pool = []
		for item in self._classes:
			pool += list( self.classDefinitions[ item ] )

		rng = random.SystemRandom()

		rng.shuffle( pool )

		result = ""
		for idx in range( 0, length ):
			result += pool[ rng.randrange( 0, len( pool ) ) ]

		return result
