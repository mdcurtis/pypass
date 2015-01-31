from pypass.commands  import CommandInterface

from pypass import PasswordEntry

import os
import os.path
import sys
from datetime import datetime
import time

class ShowCommand( CommandInterface ):
	name = 'show'
	help = 'Show (or send to clipboard) the password stored in ENTRY'

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( 'entry', metavar='ENTRY' )
		parser.add_argument( '--clip', '-c', action='store_true' )
		parser.add_argument( '--no-verify', action='store_true' )
		parser.add_argument( '-q', '--quiet', action='store_true' )
	
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


	def execute( self, args, gpg ):
		entry = PasswordEntry( self.repository, args.entry )

		if not entry.exists:
			print( 'No such entry: %s' % ( entry.name ) )
			return False

		entryFile = open( entry.fullPath, 'rb' )
		decrypted_data = gpg.decrypt_file( entryFile, not args.no_verify )
		entryFile.close()

		if decrypted_data.username is None:
			if not args.no_verify:
				print( 'Error: password is not signed. Authenticity cannot be validated!', file=sys.stderr )
				print( ' Skip this check with --no-verify', file=sys.stderr )
				return False
		
		if not args.quiet and decrypted_data.username is not None:
			print( '---- Signed Password ----', file=sys.stderr )
			print( 'Signed by:  %s' % ( decrypted_data.username ), file=sys.stderr )
			print( 'Sign key:   %s' % ( decrypted_data.pubkey_fingerprint ), file=sys.stderr )
			print( 'Signed on:  %s' % ( datetime.fromtimestamp( int(decrypted_data.sig_timestamp ) ) ), file=sys.stderr )
			print( 'Trusted:    %s' % ( decrypted_data.trust_level ), file=sys.stderr )
			print( '-------------------------', file=sys.stderr )

		if args.clip:
			password = str( decrypted_data ).split( '\n' )[ 0 ]
			return self.clip( password )
		else:
			print( decrypted_data )
			return True