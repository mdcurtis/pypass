from pypass.commands import EntryCommand

from pypass import Container, PasswordEntry

class ListCommand( EntryCommand ):
	name = 'list'
	aliases = [ 'ls' ]
	help = 'List contents of a directory or subdirectory'
	requires = [ Container, PasswordEntry ]
	isOptional = True

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( '-t', '--tree', action='store_true' )

	def executeEntry( self, args, entry ):
		if not entry.exists():
			print( '%s: does not exist' % ( entry.name ) )
			return False

		def itemSuffix( item ):
			if isinstance( item, Container ):
				return '/'
			return ''

		def treeCallback( item, indent = 0 ):
			print( '  ' + ' ' * indent + '|- ' + item.name + itemSuffix( item ) )

		def displayItem( item, alias = None ):
			flags = ''
			if isinstance( item, Container ):
				flags = 'd'
				if item.hasOverride():
					flags += 'O'
			else:
				flags = 'P'

			print( '[%2s] %s' % ( flags, alias if alias else item.name ) )

		if isinstance( entry, Container ):
			if args.tree:
				entry.walk( treeCallback )
			else:
				children = entry.children()
				displayItem( entry, '.' )

				for child in children:
					displayItem( child )
		else:
			displayItem( entry )