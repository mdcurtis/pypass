#!/usr/bin/env python

import sys
import os.path
import os

import gnupg
import argparse

import pypass.commands
from pypass import Repository, Container
from pypass import ExtendedGPG

def detectRepository( startDir ):
	(drive, testDir) = os.path.splitdrive( startDir )
	repoDir = None

	while testDir != '' and testDir != '/' and testDir != '\\':
		currentPath = os.path.join( drive, testDir )
		if os.path.isfile( os.path.join( currentPath, '.gpg-id' ) ):
			repoDir =currentPath

		if os.path.isdir( os.path.join( currentPath, '.pypass' ) ):
			repoDir = currentPath
			break

		(testDir, leaf) = os.path.split( testDir )

	if not repoDir:
		return None

	if os.path.isdir( os.path.join( repoDir, '.git' ) ):
		# TODO: return a GitRepository object
		return Repository( repoDir )
	else:
		return Repository( repoDir )

def main_entry():
	gpg = ExtendedGPG( use_agent=True )

	parser = argparse.ArgumentParser( prog='pypass', description='GPG-based password management.')

	parser.add_argument( '--version', action='store_true' )

	subparsers = parser.add_subparsers( title='subcommands', metavar='' )
	for commandClass in pypass.commands.classes:
		command = commandClass()
		commandParser = subparsers.add_parser( command.name, help=command.help, aliases=command.aliases )
		command.buildParser( commandParser )

	args = parser.parse_args()

	if args.version:
		print( 'pypass version %s' % ( pypass.version ) )
		print( ' gpg found at %s' % ( gpg.gpgbinary ))
		print( ' gpg version %s' % ( gpg.versionStr() ) )
		sys.exit()

	if not 'commandObject' in args:
		parser.print_usage()
		parser.exit()

	command = args.commandObject

	# Initialise the repository
	repository = detectRepository( os.getcwd() )

	# for file based repositories, make the root entry based on the cwd...
	if repository:
		command.root = Container( os.path.relpath( os.getcwd(), repository.baseDir ) , repository, gpg )
	command.repository = repository

	command.execute( args )

