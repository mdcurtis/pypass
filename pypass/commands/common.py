
class CommandInterface( object ):
	name = None
	help = None
	aliases = []

	def buildParser( self, parser ):
		# Closure
		def callback( args, root ):
			self.execute( args, root )

		parser.set_defaults( commandObject = self )

	def execute( self, args, root ):
		print( 'NYI' )

		return False

class EntryCommand( CommandInterface ):
	requires = []
	isOptional = False

	repository = None
	root = None

	def buildParser( self, parser ):
		super().buildParser( parser )

		nargs=1
		if self.isOptional:
			nargs = '?'

		parser.add_argument( 'entry', metavar='ENTRY-NAME', nargs=nargs )

	def execute( self, args ):
		if not self.repository or not self.root:
			print( 'No repository found! Please create one first with pypass init' )
			return False

		if not args.entry:
			self.executeEntry( args, self.root )
		else:
			entryPath = args.entry[ 0 ]
			if self.isOptional:
				entryPath = args.entry

			entry = self.root.findEntry( entryPath )

			if len( self.requires ):
				acceptable = False
				for entryType in self.requires:
					if isinstance( entry, entryType ):
						acceptable = True

				if not acceptable:
					print( '%s: is a %s' %( entry.name, entry.__class__.__name__ ) )
					return False

			return self.executeEntry( args, entry )
