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
import os.path

from pypass import Repository, ExtendedGPG, Signature
import gnupg

import yaml

class Entry( object ):
	_haveParent = False
	_parentCache = None
	_fullPath = None

	def __init__( self, path, *args ):
		parent = None
		for arg in args:
			if isinstance( arg, Entry ):
				parent = arg
				self.repository = arg.repository
				self.gpg = arg.gpg
			elif isinstance( arg, Repository ):
				self.repository = arg
			elif isinstance( arg, ExtendedGPG ):
				self.gpg = arg
		
		if parent is not None:
			self.path = self.repository.canonicalise( parent.path, path )
		else:
			self.path = path

		self.repository.checkPath( path )
		self.name = path
		

	def exists( self ):
		return os.path.exists( self.fullPath )

	@property
	def fullPath( self ):
		if self._fullPath is None:
			self._fullPath = self.repository.buildPath( self.path )
		return self._fullPath

	def name( self ):
		return self.name

	@property
	def parent( self ):
		if not self._haveParent:
			(head, tail) = os.path.split( self.path )
			if head == '':
				if self.path == '/':
					self._parentCache = None
				else:
					self._parentCache = Container( '/', self )
			else:
				self._parentCache = Container( head, self )

		return self._parentCache

class Container( Entry ):
	def __init__( self, path = '/', *args ):
		super().__init__( path, *args )

		if not os.path.isdir( self.repository.buildPath( self.path ) ):
			raise RuntimeError( '%s: is not a valid container' % ( self.path ) )

		self.gpgIdPath = self.repository.buildPath( os.path.join( self.path, '.gpg-id' ) )
		self._recipients = None

	def hasOverride( self ):
		if self.gpgIdPath:
			return True
		return False

	def children( self ):
		items = os.listdir( self.fullPath )

		childList = []
		for item in items:
			if item.startswith( '.' ): continue
			realPath = os.path.join( self.fullPath, item )
			if os.path.isdir( realPath ):
				childList.append( Container( item, self ) )
			elif item.endswith( '.gpg' ):
				childList.append( PasswordEntry( item, self ) )

		return childList

	def findEntry( self, path ):
		childPath = self.repository.canonicalise( self.path, path )

		realPath = self.repository.checkPath( childPath )
		if os.path.isdir( realPath ):
			return Container( childPath, self )
		else:
			return PasswordEntry( childPath, self )

	def defaultRecipients( self ):
		if not os.path.exists( self.gpgIdPath ) and self.parent:
			return self.parent.defaultRecipients()
		elif self._recipients is None:
			self._recipients = []
			gpgIdFile = open( self.gpgIdPath, 'r' )
			lines = gpgIdFile.readlines()
			for line in lines:
				line = line.strip()
				if len( line ):
					self._recipients.append( line )
			gpgIdFile.close()

		return self._recipients

	def signingKey( self ):
		signer = None
		for key in self.defaultRecipients():
			potentialSigners = self.gpg.keyDB().findKey( key )
			if len( potentialSigners ):
				signer = potentialSigners[ 0 ].keyid
				break

		return signer

	def walk( self, callback, level=0 ):
		childList = self.children()

		for child in childList:
			if isinstance( child, Container ):
				callback( child, level )
				child.walk( callback, level + 1 )
			else:
				callback( child, level )


class PasswordEntry( Entry ):
	def __init__( self, path, *args ):
		(name, ext) = os.path.splitext( path )
		if ext.lower() != '.gpg':
			ext += '.gpg'
		
		super().__init__( name + ext, *args )
		self.name = name

		self.needsSerialise = False
		self.needsParse = False

		self._data = ''
		self._password = None
		self._kvStore = dict()
		self.signature = None

	def _parse( self ):
		if self.needsParse:
			(password, sep, yamlData ) = str( self._data ).partition( '\n' )
			self._password = password.strip()

			self._kvStore = yaml.safe_load( yamlData )

			self.needsParse = False

	@property
	def password(self):
		self._parse()
		return self._password
	@password.setter
	def password(self, value):
		self._parse()
		self._password = value
		self.needsSerialise = True

	@property
	def extraData( self ):
		self._parse()
		return self._kvStore.copy()
	@extraData.setter
	def extraData(self, value):
		self._kvStore = value.copy()
		self.needsSerialise = True

	@property
	def data(self):
		return self._data
	@data.setter
	def data(self, value):
		self.needsSerialise = False
		self.needsParse = True
		self._data = value
	

	def load( self, verify = True ):
		entryFile = open( self.fullPath, 'rb' )
		decrypted_data = self.gpg.decrypt_file( entryFile, verify )
		entryFile.close()

		if not decrypted_data.ok:
			raise RuntimeError( 'Decryption failed' )

		self._data = decrypted_data.data.decode()

		self.needsParse = True
		self.needsSerialise = False

		self.signature = None
		if decrypted_data.username is not None:
			self.signature = Signature( decrypted_data )

	def reencrypt( self, signingKey ):
		currentRecipients = self.recipients()
		defaultRecipients = self.parent.defaultRecipients()

		currentRecipients.sort()
		defaultRecipients.sort()

		if currentRecipients != defaultRecipients:
			# Rencryption is necessary
			self.load()

			return self.save( signingKey )
		else:
			return False


	def recipients( self ):
		entryFile = open( self.fullPath, 'rb' )
		keyIds = self.gpg.list_encryption_keys( entryFile )
		entryFile.close()

		return keyIds

	def save( self, signingKey ):
		if self.needsSerialise:
			# Take 'cooked' (password + YAML dict) and convert to a data stream
			self._data = self.password + '\n' + yaml.dump( self._kvStore )

			self.needsSerialise = False

		encrypted = self.gpg.encrypt( self._data, self.parent.defaultRecipients(), sign=signingKey )
		if encrypted.ok:
			entryFile = open( self.fullPath, 'wb' )
			entryFile.write( str( encrypted ).encode() )
			entryFile.close()

			return True
		else:
			raise RuntimeError( encrypted.status )

