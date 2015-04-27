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
