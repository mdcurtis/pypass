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

from pypass.commands import CommandInterface

from pypass import PasswordEntry, Container
import pypass.uri as uri

import sys
import os
import os.path

from pypass import KeyDatabase

class InitCommand( CommandInterface ):
	name = 'init'
	help = 'Initialises a new folder with the given GPG-IDs as the default encryption keys'
	repository = None

	def buildParser( self, parser ):
		parser.add_argument( '-r', '--recipients', metavar='GPG-ID', nargs='+' )
		parser.add_argument( 'path', metavar='PATH' )

		super().buildParser( parser )

	def execute( self, args ):
		keys = self.root.gpg.keyDB().findKeys( args.recipients )

		havePrivate = False
		for key in keys:
			if key.type == 'sec':
				havePrivate = True

		if not havePrivate:
			print( "At least one key provided should have a private key available, otherwise you will not be able to decrypt the passwords. Aborting.")
			sys.exit()

		pathUri = uri.join( args.path )

		print( self.repository._path( pathUri ))

		if self.repository.exists(pathUri ):
			if not self.repository.isDir(  pathUri ):
				print( "'%s' is not a directory!" % (pathUri ) )
				sys.exit( 1 )
			#else: #if os.path.islink( realPath ):
			#	print( "'%s' is a symlink!" % ( pathUri ) )
			#	sys.exit( 1 )
		else:
			os.makedirs( realPath )

		keyIds = []
		for key in keys:
			keyIds += [ key.keyid ]

		# Double-check that this isn't a no-op
		gpgIdPath = uri.join( pathUri, '.gpg-id' )
		gpgIdFile = self.repository.write( gpgIdPath )
		#gpgIdPath = os.path.join( args.path, '.gpg-id' )

		for keyId in keyIds:
			gpgIdFile.write( (keyId + '\n').encode() )
		gpgIdFile.commit()

		self.repository.notifyAdd( gpgIdPath, 'Set GPG id to %s' % ( ', '.join( keyIds ) ) )
		print( "Password store initialized for %s" % ( ', '.join( keyIds ) ) )

		print( 'Re-encrypting entries as necessary...' )
		container = self.root.findEntry( args.path )
		signature = container.signingKey()
		print( 'signingKey is %s' % ( signature ) )
		def reencryptCallback( entry, level ):
			try:
				if isinstance( entry, PasswordEntry ):
					print( 'Re-encrypting ' + entry.name, end='', flush=True )
					if entry.reencrypt( signature ):
						print( ' done' )
					else:
						print( ' not needed' )
			except RuntimeError as e:
				print( ' failure' )
				print( 'Failed to encrypt file %s' % ( e ) )

		container.walk( reencryptCallback )

