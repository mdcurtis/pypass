
from datetime import datetime

import re
keyIdRegex = re.compile( '^[0-9A-Za-z]{8,16}$' )
emailRegex = re.compile( '<(.+@.+)>')

class KeyInfo( object ):
	def __init__( self, keyData ):
		self.keyData = keyData

	def __getattr__( self, name ):
		return self.keyData[ name ]

	def _getTimestamp( self, name ):
		if not name in self.keyData:
			return None
		if self.keyData[ name ] == '':
			return None

		return datetime.fromtimestamp( int( self.keyData[ name ] ) )

	@property
	def emails( self ):
		result = []
		for uid in self.keyData[ 'uids' ]:
			regexResult = emailRegex.search( uid )
			if regexResult is not None:
				result.append( regexResult.groups()[ 0 ] )

		return result

	@property
	def expires( self ):
		return self._getTimestamp( 'expires' )

	@property
	def created( self ):
		return self._getTimestamp( 'date' )

	def isExpired( self ):
		if self.expires:
			return datetime.now() > self.expires()
		else:
			return False



class KeyDatabase( object ):
	def __init__( self, gpg ):
		self._gpg = gpg
		self._private_cache = self._populate( self._gpg.list_keys( True ) )
		self._public_cache = self._populate( self._gpg.list_keys() )

	def _populate( self, keyList ):
		keyDB = dict()

		for key in keyList:
			keyInfo = KeyInfo( key )

			keyDB[ keyInfo.keyid ] = keyInfo

		return keyDB


	def findKeys( self, keyIdList ):
		keys = []
		for keyId in keyIdList:
			matches = self.findKey( keyId )
			if len( matches ) == 0:
				raise RuntimeError( "No match found for key id %s" % ( keyId ) )
			else:
				keys += matches

		return keys

	def _indexSearch( self, cache, keyId ):
		if len( keyId ) == 16:
			# Full length key, super-fast
			if keyId in cache:
				return [ cache[ keyId ] ]
			else:
				return []
		elif len( keyId ) == 8:
			results = []
			for ( test, info ) in cache.items():
				shortKey = test[ -8: ]
				if shortKey == keyId:
					results.append( info )

			return results

		return []

	def findKey( self, search ):
		if keyIdRegex.match( search ): 
			private = self._indexSearch( self._private_cache, search )
			if len( private ):
				return private
			else:
				return self_._indexSearch( self._public_cache, search )
		elif '@' in search:
			for cache in [ self._private_cache, self._public_cache ]:
				results = []
				for info in cache.values():
					if search in info.emails:
						results.append( info )
				if len( results ):
					return results
			return []
		else:
			raise RuntimeError( "Invalid search string '%s' for key - try key fingerprint or email address" % ( keyId ))

		