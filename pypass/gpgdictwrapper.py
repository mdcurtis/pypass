from datetime import datetime

class GPGDictWrapper( object ):
	def __init__( self, data ):
		if isinstance( data, dict ):
			self._data = data
		else:
			self._data = dict()
			for field in dir( data ):
				if field == 'gpg': continue 
				if field == 'data': continue
				if field.startswith( '_' ): continue
				
				self._data[ field ] = data.__getattribute__( field )

	def __getattr__( self, name ):
		return self._data[ name ]

	def _getTimestamp( self, name ):
		if not name in self._data:
			return None
		if self._data[ name ] == '':
			return None

		return datetime.fromtimestamp( int( self._data[ name ] ) )
