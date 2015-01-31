from pypass.commands  import EntryCommand
from pypass.util import confirm, isInteractive

from pypass import Container, PasswordEntry
from pypass import PasswordGenerator

import os.path
import sys
import getpass

class GenerateCommand( EntryCommand ):
	name = 'generate'
	help = 'Generate a password and insert it into the store'
	requires = [ PasswordEntry ]

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( '-l', '--length', type=int, help='Length of password to generate (default: 16).', default=16 )
		parser.add_argument( '-c', '--classes', help="List of character classes: [U]pper, [l]ower, [d]igit or [@]ymbols (default: Uld)", default='Uld' )

		parser.add_argument( '-i', '--in-place', dest='inPlace', action='store_true',
			help='Edit an existing password in-place, replacing the first line with the new password (preserves YAML metadata)' )
		parser.add_argument( '-f', '--force', action='store_true',
			help='Don\'t ask to confirm overwrites' )
		

	def executeEntry( self, args, entry ):
		if entry.exists() and not args.force and not args.inPlace:
			if not confirm( 'An entry already exists for %s. Overwrite it' % (args.entry) ):
				return False

		pwgen = PasswordGenerator()
		pwgen.classes = args.classes

		password = pwgen.generate( args.length )

		if args.inPlace:
			entry.load()

			entry.password = password

			entry.save( entry.parent.signingKey() )
		else:
			entry.data = password

			entry.save( entry.parent.signingKey() )