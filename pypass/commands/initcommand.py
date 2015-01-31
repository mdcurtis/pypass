from pypass.commands import CommandInterface

import sys
import os
import os.path

from pypass import KeyDatabase

class InitCommand( CommandInterface ):
	name = 'init'
	help = 'Initialises a new folder with the given GPG-IDs as the default encryption keys'
	repository = None

	def buildParser( self, parser ):
		parser.add_argument( 'gpgIds', metavar='GPG-ID', nargs='+' )
		parser.add_argument( '-p', '--path', metavar='subfolder' )

		super().buildParser( parser )

	def execute( self, args, gpg ):
		keyDB = KeyDatabase( gpg )
		keys = keyDB.findKeys( args.gpgIds )

		havePrivate = False
		for key in keys:
			if key.type == 'sec':
				havePrivate = True

		if not havePrivate:
			print( "At least one key provided should have a private key available, otherwise you will not be able to decrypt the passwords. Aborting.")
			sys.exit()

		if args.path is None:
			args.path = '.'

		realPath = self.repository.buildPath( args.path )
		if realPath is None:
			print( "'%s' is not a valid path within this repository" % ( args.path ) )
			sys.exit( 1 )

		if os.path.exists( realPath ):
			if not os.path.isdir( realPath ):
				print( "'%s' is not a directory!" % ( args.path ) )
				sys.exit( 1 )
			elif os.path.islink( realPath ):
				print( "'%s' is a symlink!" % ( args.path ) )
				sys.exit( 1 )
		else:
			os.mkdir( realPath )

		keyIds = []
		for key in keys:
			keyIds += [ key.keyid ]

		# Double-check that this isn't a no-op
		gpgIdPath = os.path.join( args.path, '.gpg-id' )

		gpgIdFile = open( self.repository.buildPath( gpgIdPath ), 'w' )
		for keyId in keyIds:
			print( keyId, file=gpgIdFile )
		gpgIdFile.close()

		self.repository.notifyAdd( gpgIdPath, 'Set GPG id to %s' % ( ', '.join( keyIds ) ) )
		print( "Password store initialized for %s" % ( ', '.join( keyIds ) ) )

		# Re-encrypt stuff...