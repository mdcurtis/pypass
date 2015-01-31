from pypass.commands import EntryCommand

from pypass import Container

class ListCommand( EntryCommand ):
	name = 'list'
	help = 'List contents of a directory or subdirectory'
	requires = [ Container ]

	def executeEntry( self, args, entry ):
		print( 'Listing for %s' % ( entry.name ) )
		def callback( item, indent ):
			suffix = ''
			if isinstance( item, Container ):
				suffix = '/'

			print( '  ' + ' ' * indent + '|- ' + item.name + suffix )

		entry.walk( callback )