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
				entry.data = newData
				
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
