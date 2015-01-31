import sys
import os

def isInteractive():
	return os.isatty( sys.stdin.fileno() )

def confirm( prompt ):
	if not isInteractive():
		print( prompt + '? NO [not interactive]' )
		return False
	
	answer = input( prompt + ' [y/N]? ' )
	if answer.lower() == 'y' or answer.lower() == 'yes':
		return True
	else:
		return False
