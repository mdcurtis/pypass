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

from pypass.commands  import EntryCommand

from pypass import PasswordEntry

import os
import os.path
import sys
from datetime import datetime
import time

class EditCommand( EntryCommand ):
	name = 'edit'
	help = 'Edit ENTRY using a simple Tk dialog'
	requires = [ PasswordEntry ]

	def executeEntry( self, args, entry ):
		if not entry.exists:
			print( 'Entry not found' )
			return False

		entry.load()

		# Dodgy hack to ensure python passes by reference
		shouldSave = [ False ]

		import tkinter
		root = tkinter.Tk()

		textBox = tkinter.Text( root )
		textBox.insert( '1.0', entry.data )
		textBox.pack()

		def saveCB():
			newData = textBox.get( '1.0', tkinter.END )

			if newData != entry.data:
				shouldSave[ 0 ] = True

			root.destroy()

		saveButton = tkinter.Button( root, text='Save', command=saveCB )
		saveButton.pack()

		root.mainloop()

		if shouldSave[ 0 ]:
			entry.save( entry.parent.signingKey() )
			print( 'Entry updated' )
		else:
			print( 'Cancelled (not saved)' )

		return True
