import gnupg
import sys
import os.path

from pypass import KeyDatabase

def findInPath( paths, name ):
	for path in paths:
		fullPath = os.path.join( path, name )
		if os.path.exists( fullPath ):
			return fullPath

	return None

def openRegKey3264( rootKey, key ):
	import winreg

	try:
		return winreg.OpenKeyEx(
				rootKey, key, 
				access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY )
	except FileNotFoundError:
		try:
			return winreg.OpenKeyEx( 
				rootKey, key, 
				access=winreg.KEY_READ | winreg.KEY_WOW64_32KEY )
		except FileNotFoundError:
			pass

	return None

def findGPGWindows():
	import winreg

	tryPaths = []

	gnupgRegRoot = openRegKey3264( winreg.HKEY_LOCAL_MACHINE, 'Software\\GNU\\GnuPG' )
	if gnupgRegRoot is not None:
		try:
			root, typeNum = winreg.QueryValueEx( gnupgRegRoot, 'Install Directory' )
			if root is not None:
				tryPaths.append( root )
		except FileNotFoundError:
			pass

	tryPaths.extend( os.environ[ 'PATH' ].split( ';' ) )

	return findGPG( tryPaths, '.exe' )

def findGPGPosix():
	tryPaths = os.environ[ 'PATH' ].split( ':' )
	return findGPG( tryPaths )

def findGPG( tryPaths, exeSuffix = '' ):
	gpg2 = findInPath( tryPaths, 'gpg2' + exeSuffix )

	if gpg2:
		return gpg2
	else:
		return findInPath( tryPaths, 'gpg' + exeSuffix )

class GPGNotFoundError( RuntimeError ):
	pass

class EncryptionKeys( object ):
	"Handle status messages for --decrypt --list-only"
	def __init__( self, gpg ):
		self.gpg = gpg
		self.key_ids = []

	def handle_status( self, key, value ):
		if key == 'ENC_TO':
			( key_id, flagA, flagB ) = value.split( ' ' )
			self.key_ids.append( key_id )



class ExtendedGPG( gnupg.GPG ):
	_keyDB = None

	def __init__( self, *args, **kwargs ):
		discoveredBinary = None
		if sys.platform.startswith( 'win32' ):
			discoveredBinary = findGPGWindows()
		else:
			# All other platforms are unix-like (or so we assume...)
			discoveredBinary = findGPGPosix()

		if discoveredBinary is None:
			raise GPGNotFoundError( 'No GPG binary found in PATH' )

		kwargs[ 'gpgbinary' ] = discoveredBinary
		super().__init__( *args, **kwargs )

	def keyDB( self ):
		if not self._keyDB:
			self._keyDB = KeyDatabase( self )
		return self._keyDB

	def list_encryption_keys( self, file, passphrase=None ):
		gpgargs = [ '--decrypt',  '--list-only', '--keyid-format', 'long' ]
		
		result = EncryptionKeys( self )
		self._handle_io( gpgargs, file, result, passphrase=passphrase, binary=True )
		
		return result.key_ids

	def versionStr( self ):
		return ".".join( str( i ) for i in self.version )