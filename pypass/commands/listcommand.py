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

from pypass.commands import EntryCommand

from pypass import Container

class ListCommand( EntryCommand ):
	name = 'list'
	help = 'List contents of a directory or subdirectory'
	requires = [ Container ]

	def executeEntry( self, args, entry ):
		print( 'Listing for %s' % ( entry.name ) )
		def callback( item, indent ):
			suffix = ''
			if isinstance( item, Container ):
				suffix = '/'

			print( '  ' + ' ' * indent + '|- ' + item.name + suffix )

		entry.walk( callback )