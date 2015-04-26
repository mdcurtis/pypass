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

from pypass.commands  import EntryCommand
from pypass.util import confirm, isInteractive

from pypass import Container, PasswordEntry
from pypass import KeyDatabase

import os.path
import sys
import getpass

class InsertCommand( EntryCommand ):
	name = 'insert'
	help = 'Insert a password into the store'

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( '-m', '--multiline', action='store_true' )
		parser.add_argument( '-e', '--echo', action='store_true' )
		parser.add_argument( '-f', '--force', action='store_true' )
		parser.add_argument( '--unsigned', action='store_true' )
		

	def executeEntry( self, args, entry ):
		if isinstance( entry, Container ):
			print( '%s: is a directory' %( entry.name ) )
			return False

		if entry.exists() and not args.force:
			if not confirm( 'An entry already exists for %s. Overwrite it' % (args.entry) ):
				return False
		
		if entry.parent is None or not entry.parent.exists():
			print( 'It looks like we can\'t find the parent folder for %s, perhaps initialise the folder first with pypass init?' % (entry.name) )
			return False

		if entry.parent.defaultRecipients() is None:
			print( 'Please initialise the repository with pypass init first' )
			return False

		password = self.passwordFromStdin( args )

		if password is not None:
			entry.data = password

			signer = None
			if not args.unsigned:
				signer = entry.parent.signingKey()
				if signer is None:
					print( "Warning: cannot find a key that can be used for signing in the recipients list" )
					print( " Password will be unsigned" )

			entry.save( signer )

			return True 

		return False

	def passwordFromStdin( self, args ):
		if args.multiline:
			osSpecificKey = 'Ctrl-D'
			if sys.platform.startswith( 'win32' ):
				osSpecificKey = 'Ctrl-Z, then Enter'
			print( 'Enter password, then type %s to finish.' % ( osSpecificKey ) )
			password = sys.stdin.read()

			return password
		elif args.echo:
			try:
				password = input( 'Password (will be echo\'d on screen): ' )
				if len( password ):
					return password
			except EOFError:
				return None
			return None
		else:
			if not isInteractive():
				print( 'stdin is not a console: abort' )
				return None

			password1 = getpass.getpass( 'Enter password for %s: ' % (args.entry ) )
			password2 = getpass.getpass( 'Retype password for %s: ' % (args.entry ) )

			if password1 != password2:
				print( "Error: the entered passwords do not match." )
				return None

			return password1

