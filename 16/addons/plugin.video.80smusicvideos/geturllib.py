#/bin/python

import os
import time

gCacheDir = ""
gCacheSize = 20

#==============================================================================

def SetCacheDir( cacheDir ):
	global gCacheDir
	
	gCacheDir = cacheDir
	if not os.path.isdir(gCacheDir):
		os.makedirs(gCacheDir)

#==============================================================================

def _CheckCacheDir():
	if ( gCacheDir == '' ):
		raise Exception('CacheDir not defined')


#==============================================================================

def _GetURL_NoCache( url ):
	import urllib
	x = urllib.urlopen(url)
	return x.read()

#==============================================================================

def GetURL( url, maxAgeSeconds=0 ):
	_CheckCacheDir()
	if ( maxAgeSeconds > 0 ):
		# Is this URL in the cache?
		cachedURLTimestamp = _Cache_GetURLTimestamp( url )
		if ( cachedURLTimestamp > 0 ):
			# We have file in cache, but is it too old?
			if ( (time.time() - cachedURLTimestamp) > maxAgeSeconds ):
				# Too old, so need to get it again
				data = _GetURL_NoCache( url )
				# Cache it
				_Cache_Add( url, data )
				# Return data
				return data
			else:
				# Get it from cache
				return _Cache_GetData( url )
	
	# maxAge = 0 or URL not in cache, so get it
	data = _GetURL_NoCache( url )
	# Cache it
	_Cache_Add( url, data )
	# Cache size maintenance
	_Cache_Trim
	# Return data
	return data

#==============================================================================

def _Cache_GetURLTimestamp( url ):
	cacheKey = _Cache_CreateKey( url )
	cacheFileFullPath = os.path.join( gCacheDir, cacheKey )
	if ( os.path.isfile( cacheFileFullPath ) ):
		return os.path.getmtime(cacheFileFullPath)
	else:
		return 0

#==============================================================================

def _Cache_GetData( url ):
	cacheKey = _Cache_CreateKey( url )
	cacheFileFullPath = os.path.join( gCacheDir, cacheKey )
	f = file(cacheFileFullPath, "r")
	data = f.read()
	f.close()
	return data

#==============================================================================

def _Cache_Add( url, data ):
	cacheKey = _Cache_CreateKey( url )
	cacheFileFullPath = os.path.join( gCacheDir, cacheKey )
	f = file(cacheFileFullPath, "w")
	f.write(data)
	f.close()

#==============================================================================

def _Cache_CreateKey( url ):
	try:
		from hashlib import md5
		return md5(url).hexdigest()
	except:
		import md5
		return  md5.new(url).hexdigest()

#==============================================================================

def _Cache_Trim():
	files = glob.glob( gCacheDir )
	if ( len(files) > gCacheSize ):
		oldestFile = get_oldest_file( files )
		cacheFileFullPath = os.path.join( gCacheDir, oldestFile )
        if os.path.exists(cacheFileFullPath):
            os.remove(cacheFileFullPath)

#==============================================================================

def get_oldest_file(files, _invert=False):
    """ Find and return the oldest file of input file names.
    Only one wins tie. Values based on time distance from present.
    Use of `_invert` inverts logic to make this a youngest routine,
    to be used more clearly via `get_youngest_file`.
    """
    if _invert:
    	gt = operator.lt
    else:
    	gt = operator.gt
    # Check for empty list.
    if not files:
        return None
    # Raw epoch distance.
    now = time.time()
    # Select first as arbitrary sentinel file, storing name and age.
    oldest = files[0], now - os.path.getctime(files[0])
    # Iterate over all remaining files.
    for f in files[1:]:
        age = now - os.path.getctime(f)
        if gt(age, oldest[1]):
            # Set new oldest.
            oldest = f, age
    # Return just the name of oldest file.
    return oldest[0]