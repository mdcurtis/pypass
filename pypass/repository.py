import os.path

class Repository( object ):
	baseDir = None

	def __init__( self, baseDir ):
		self.baseDir = baseDir

	def buildPath( self, path ):
		# Treat absolute paths as relative to baseDir, not the system
		if path.startswith( '/' ) or path.startswith( '\\' ):
			path = path[ 1: ]
		realPath = os.path.normpath( os.path.join( self.baseDir, path ) )
		
		if os.path.commonprefix( [ self.baseDir, realPath ] ) == self.baseDir:
			return realPath
		else:
			return None

	def checkPath( self, path ):
		if self.buildPath( path ) is None:
			raise RuntimeError( "Bad path '%s'!" % (path ) )

	def findFile( self, path, fileName ):
		self.checkPath( path )

		def find( path, fileName ):
			test = os.path.join( self.baseDir, path, fileName )
			if os.path.exists( test ):
				return test
			else:
				( head, tail ) = os.path.split( path )
				if len( head ):
					return find( head, fileName )

			return None

		return find( path, fileName ) 

	def entryPath( self, entry ):
		(name, ext) = os.path.splitext( entry )
		if ext == '':
			ext = '.gpg'
		if ext.lower() != '.gpg':
			raise RuntimeError( 'Entry extension must be .gpg or blank' )
		return self.buildPath( name + ext )

	def notifyAdd( self, path, msg = None ):
		self.buildPath( path )

		return True

	def notifyDelete( self, path, msg = None ):
		self.buildPath( path )

		return True

	def commit( self, message ):
		return True
