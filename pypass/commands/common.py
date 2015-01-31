
class CommandInterface( object ):
	name = None
	help = None
	aliases = []

	def buildParser( self, parser ):
		# Closure
		def callback( args, root ):
			self.execute( args, root )

		parser.set_defaults( func = callback )

	def execute( self, args, root ):
		print( 'NYI' )

class EntryCommand( CommandInterface ):
	requires = []

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( 'entry', metavar='ENTRY-NAME' )

	def execute( self, args, root ):
		entry = root.findEntry( args.entry )

		if len( self.requires ):
			acceptable = False
			for entryType in self.requires:
				if isinstance( entry, entryType ):
					acceptable = True

			if not acceptable:
				print( '%s: is a directory' %( entry.name ) )
				return False

		self.executeEntry( args, entry )
