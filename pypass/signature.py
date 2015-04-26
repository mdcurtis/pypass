#
# This file is part of pypass.  pypass is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Michael Curtis, 2015

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
