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

import os.path
import os
import io

class AtomicFileStream( io.FileIO ):
	"""
	A file-like object which attempts to behave atomically - either the new file
	is created and is complete, or it is not created at all (in reality, it is 
	created under a temporary name, then deleted).
	This is a bit like the way rsync does things.

	It adds a new method to the file object called commit, which is intended to be
	called when all data has been successfully written to the file.
	"""
	def __init__( self, path ):
		self.path = path
		# TODO: need a better algorithm for choosing a temporary filename?
		self.tmpPath = path + '.tmp'

		super().__init__( self.tmpPath, 'w' )

	def commit( self ):
		super().close()

		if self.tmpPath:
			os.replace( self.tmpPath, self.path )
			self.tmpPath = None

	def close( self ):
		super().close()

		if self.tmpPath:
			os.unlink( self.tmpPath )
			self.tmpPath = None


class Repository( object ):
	baseDir = None

	def __init__( self, baseDir ):
		self.baseDir = baseDir

	def _path( self, uri ):
		# Treat absolute URIs as relative to baseDir, not the system
		if uri.startswith( '/' ) or uri.startswith( '\\' ):
			uri = uri[ 1: ]

		return os.path.join( self.baseDir, uri )

	def exists( self, uri ):
		return os.path.exists( self._path( uri ) )

	def isDir( self, uri ):
		return os.path.isdir( self._path( uri ) )

	def read( self, uri ):
		return open( self._path( uri ), 'rb' )

	def write( self, uri, msg = None ):
		fullPath = self._path( uri )
		if os.path.exists( fullPath ):
			return AtomicFileStream( fullPath )
		else:
			raise OSError( "File %s not found" % ( fullPath ) )

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

	def notifyAdd( self, path, msg = None ):
		self.buildPath( path )

		return True

	def notifyDelete( self, path, msg = None ):
		self.buildPath( path )

		return True

	def commit( self, message ):
		return True
