import os.path

class Entry( object ):
	_haveParent = False
	_parentCache = None
	_fullPath = None

	def __init__( self, repository, path ):
		repository.checkPath( path )

		self.repository = repository
		self.path = path
		self.name = path

	def exists( self ):
		return os.path.exists( self.fullPath )

	@property
	def fullPath( self ):
		if self._fullPath is None:
			self._fullPath = self.repository.buildPath( self.path )
		return self._fullPath

	def name( self ):
		return self.name

	@property
	def parent( self ):
		if not self._haveParent:
			(head, tail) = os.path.split( self.path )
			if head == '':
				if self.path == '/':
					self._parentCache = None
				else:
					self._parentCache = Container( self.repository )
			else:
				self._parentCache = Container( self.repository, head )

		return self._parentCache

class Container( Entry ):
	def __init__( self, repository, path = '/' ):
		super().__init__( repository, path )

		if not os.path.isdir( repository.buildPath( path ) ):
			raise RuntimeError( '%s: is not a valid container' % ( path ) )

		self.gpgIdPath = self.repository.buildPath( os.path.join( self.path, '.gpg-id' ) )
		self._recipients = None

	def hasOverride( self ):
		if self.gpgIdPath:
			return True
		return False

	def recipients( self ):
		if not self.gpgIdPath and self.parent:
			return self.parent.recipients()
		elif self._recipients is None:
			self._recipients = []
			gpgIdFile = open( self.gpgIdPath, 'r' )
			lines = gpgIdFile.readlines()
			for line in lines:
				line = line.strip()
				if len( line ):
					self._recipients.append( line )
			gpgIdFile.close()

		return self._recipients

	def signingKey( self, keyDB ):
		signer = None
		for key in self.recipients():
			potentialSigners = keyDB.findKey( key )
			if len( potentialSigners ):
				signer = potentialSigners[ 0 ].keyid
				break

		return signer

class PasswordEntry( Entry ):
	def __init__( self, repository, path ):
		(name, ext) = os.path.splitext( path )
		if ext == '':
			ext = '.gpg'
		if ext.lower() != '.gpg':
			raise RuntimeError( 'Entry extension must be .gpg or blank' )
		
		super().__init__( repository, name + ext )
		self.name = name

		self.data = ''

	def load( self ):
		pass

	def save( self, gpg, signingKey ):
		encrypted = gpg.encrypt( self.data, self.parent.recipients(), sign=signingKey )

		entryFile = open( self.fullPath, 'wb' )
		entryFile.write( str( encrypted ).encode() )
		entryFile.close()

