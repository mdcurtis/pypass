import os.path
import re

class Repository( object ):
	baseDir = None
	slashes = re.compile( r'[\\/]+')

	def __init__( self, baseDir ):
		self.baseDir = baseDir

	def canonicalise( self, *args ):
		# UNIX-style path names
		components = [ self.slashes.sub( '/', component ) for component in args ]

		startComponent = 0
		for idx in range( 0, len( components ) ):
			if components[ idx ].startswith( '/' ):
				startComponent = idx

		components = components[ startComponent: ]
		canon = '/'.join( components )

		return self.slashes.sub( '/', canon )


	def buildPath( self, path, *args ):
		# Treat absolute paths as relative to baseDir, not the system
		if path.startswith( '/' ) or path.startswith( '\\' ):
			path = path[ 1: ]
		realPath = os.path.normpath( os.path.join( self.baseDir, path ) )

		if os.path.commonprefix( [ self.baseDir, realPath ] ) == self.baseDir:
			return realPath
		else:
			return None

	def checkPath( self, path ):
		fullPath = self.buildPath( path ) 
		if fullPath is None:
			raise RuntimeError( "Bad path '%s'!" % (path ) )
		return fullPath

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
