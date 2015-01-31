from pypass.commands  import EntryCommand

from pypass import PasswordEntry

import os
import os.path
import sys
from datetime import datetime
import time

class ShowCommand( EntryCommand ):
	name = 'show'
	help = 'Show (or send to clipboard) the password stored in ENTRY'
	requires = [ PasswordEntry ]

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( '--clip', '-c', action='store_true' )
		parser.add_argument( '--no-verify', action='store_true' )
		parser.add_argument( '-q', '--quiet', action='store_true' )

		parser.add_argument( '-y', '--yaml' )
	
	def clip( self, password ):
		try:
			import pyperclip
		except ImportError:
			print( 'Clipboard support requires the pyperclip module' )
			return False

		passwordTimer = 5
		print( 'Password will be available on the clipboard for %i seconds.' % ( passwordTimer ))
		pyperclip.copy( password )
		for seconds in range( passwordTimer, 0, -1 ):
			print( '%i... ' % ( seconds ), end='', flush=True )
			time.sleep( 1 )
		print( 'clipboard cleared.' )

		pyperclip.copy( '' )

		return True


	def executeEntry( self, args, entry ):

		if not entry.exists():
			print( 'No such entry: %s' % ( entry.name ) )
			return False

		entry.load()
		
		if entry.signature is None:
			if not args.no_verify:
				print( 'Error: password is not signed. Authenticity cannot be validated!', file=sys.stderr )
				print( ' Skip this check with --no-verify', file=sys.stderr )
				return False
		
		if not args.quiet and entry.signature.username is not None:
			print( '---- Signed Password ----', file=sys.stderr )
			print( 'Signed by:  %s' % ( entry.signature.username ), file=sys.stderr )
			print( 'Sign key:   %s' % ( entry.signature.pubkey_fingerprint ), file=sys.stderr )
			print( 'Signed on:  %s' % ( entry.signature.sig_timestamp ), file=sys.stderr )
			print( 'Trusted:    %s' % ( entry.signature.trust_level ), file=sys.stderr )
			print( '-------------------------', file=sys.stderr )

		if args.clip:
			password = entry.password
			return self.clip( password )
		elif args.yaml:
			def recursiveDict( source, path ):
				(head, sep, tail) = path.partition( '.' )
				lNames = [ s.lower() for s in source.keys() ]
				names = [ s for s in source.keys() ]
				if head.lower() in lNames:
					properName = names[ lNames.index( head.lower() ) ]
					entry = source[ properName ]
					if len( tail ) and isinstance( entry, dict ):
						return recursiveDict( entry, tail )
					elif len( tail ) and isinstance( entry, list ):
						for subentry in entry:
							result = recursiveDict( subentry, tail )
							if result is not None: return result
					elif len( tail ) == 0:
						return entry
				return None

			print( recursiveDict( entry.extraData, args.yaml ) )
		else:
			print( entry.data )
			return True