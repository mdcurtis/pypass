#!/usr/bin/env python
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

import sys
import os.path
import os


import gnupg
import argparse

import pypass.commands
from pypass import Repository, Container
from pypass import ExtendedGPG

def verTupleToStr( verTuple ):
	numbers = []
	for num in verTuple:
		numbers.append( str( num ) )
	return '.'.join( numbers )

def main_entry():
	gpg = ExtendedGPG( use_agent=True )

	# Initialise the repository
	repository = Repository( os.getcwd() )
	root = Container( '/', repository, gpg )

	parser = argparse.ArgumentParser(description='GPG-based password management.')

	parser.add_argument( '--version', action='store_true' )

	subparsers = parser.add_subparsers( title='subcommands', metavar='' )
	for commandClass in pypass.commands.classes:
		command = commandClass()
		command.repository = repository
		commandParser = subparsers.add_parser( command.name, help=command.help, aliases=command.aliases )
		command.buildParser( commandParser )

	args = parser.parse_args()

	if args.version:
		print( 'pypass version %s' % ( pypass.version ) )
		print( 'gpg is %s version %s' % ( gpg.gpgbinary, gpg.versionStr() ) )
		sys.exit()

	if 'func' in args:
		args.func( args, root )
	else:
		parser.print_usage()
		parser.exit()
