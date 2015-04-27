
def flatmap( func, iterable ):
	result = []
	for item in iterable:
		result.extend( func( item ) )
	return result


def canonicalise( *args ):
	"""
		canonicalise URIs
		Converts path to UNIX-style notation (\ is converted to /),
		then splits and normalises. A bit like a cross between
		os.path.split() and os.path.normpath(), except:
		 a) canonicalise works exclusively on UNIX-style paths, even on Windows, and
		 b) canonicalise will strip 'directory-up' (../) directives that try to
		 	proceed above the virtual root ('/').
	"""
	# UNIX-style path names
	components = [ component.replace( '\\', '/' ) for component in args ]

	startComponent = 0
	for idx in range( 0, len( components ) ):
		if components[ idx ].startswith( '/' ):
			startComponent = idx

	components = components[ startComponent: ]
	expanded = flatmap( lambda x: x.split( '/' ), components )

	idx = 0
	while idx < len( expanded ):
		if expanded[ idx ] == '.' or len( expanded[ idx ] ) == 0:
			expanded.pop( idx )
		elif expanded[ idx ] == '..':
			expanded.pop( idx )
			if idx > 0:
				expanded.pop( idx - 1 )
				idx -= 1
		else:
			idx += 1

	return expanded

def join( *args ):
	return '/'.join( canonicalise( *args ) )

def split( uri ):
	partition = uri.rpartition( '/' )
	return (partition[ 0 ], partition[ 2 ] )

def explode( *args ):
	return list( filter( lambda _: len(_) > 0, flatmap( lambda _: _.split( '/' ), args ) ) )
