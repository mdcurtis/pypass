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

from pypass.commands import EntryCommand

from pypass import Container, PasswordEntry

class RecipientsCommand( EntryCommand ):
	name = 'recipients'
	help = 'Lists default recipients for a folder, or recipients on an encrypted file'

	def executeEntry( self, args, entry ):
		if not entry.exists():
			print( '%s: does not exist!' % ( entry.name ) )

		title = ''
		recipients = []
		if isinstance( entry, Container ):
			title = 'Default recipients (encryption keys) for entries created in folder %s' % ( entry.name )
			
			recipients = entry.defaultRecipients()
		else:
			title = 'Recipients (encryption keys) for entry %s' % ( entry.name )
			
			recipients = entry.recipients()

		print( title )
		print( '=' * len( title ) )
		print()

		for recipient in recipients:
			keyInfo = entry.gpg.keyDB().findKey( recipient )
			if len( keyInfo ):
				print( '  %16s\t%s' % ( recipient, keyInfo[ 0 ].uids[ 0 ] ) )
			else:
				print( '  %16s' % ( recipient ) )
			

