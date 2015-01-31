
class CommandInterface( object ):
	name = None
	help = None
	aliases = []

	def buildParser( self, parser ):
		# Closure
		def callback( args, gpg ):
			self.execute( args, gpg )

		parser.set_defaults( func = callback )

	def execute( self, args ):
		print( 'NYI' )
