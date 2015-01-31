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
			

