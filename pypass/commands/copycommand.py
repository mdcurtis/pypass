from pypass.commands import CommandInterface

class CopyCommand( CommandInterface ):
	name = 'copy'
	help = 'Copies/moves a password file, optionally re-encrypting it'
	aliases = ['move']
	