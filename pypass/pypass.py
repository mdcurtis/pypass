#!/usr/bin/env python

import sys
import os.path
import os


import gnupg
import argparse

import pypass.commands
from pypass import Repository
from pypass import ExtendedGPG

def verTupleToStr( verTuple ):
	numbers = []
	for num in verTuple:
		numbers.append( str( num ) )
	return '.'.join( numbers )

def main_entry():
	repository = Repository( os.getcwd() )

	gpg = ExtendedGPG( use_agent=True )

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
		args.func( args, gpg )
	else:
		parser.print_usage()
		parser.exit()
