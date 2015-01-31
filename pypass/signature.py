
from pypass import GPGDictWrapper

class Signature( GPGDictWrapper ):
	def __init__( self, data ):
		super().__init__( data )

	@property
	def timestamp( self ):
		return self._getTimestamp( 'timestamp' )

	@property
	def sig_timestamp( self ):
		return self._getTimestamp( 'sig_timestamp' )

	@property
	def expire_timestamp( self ):
		return self._getTimestamp( 'expire_timestamp' )

	@property
	def creation_date( self ):
		return self._getTimestamp( 'creation_date' )
