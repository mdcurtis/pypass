#
# This file is part of pypass.  pypass is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Michael Curtis, 2015

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
