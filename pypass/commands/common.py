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

class CommandInterface( object ):
	name = None
	help = None
	aliases = []

	def buildParser( self, parser ):
		# Closure
		def callback( args, root ):
			self.execute( args, root )

		parser.set_defaults( func = callback )

	def execute( self, args, root ):
		print( 'NYI' )

class EntryCommand( CommandInterface ):
	requires = []

	def buildParser( self, parser ):
		super().buildParser( parser )

		parser.add_argument( 'entry', metavar='ENTRY-NAME' )

	def execute( self, args, root ):
		entry = root.findEntry( args.entry )

		if len( self.requires ):
			acceptable = False
			for entryType in self.requires:
				if isinstance( entry, entryType ):
					acceptable = True

			if not acceptable:
				print( '%s: is a directory' %( entry.name ) )
				return False

		self.executeEntry( args, entry )
