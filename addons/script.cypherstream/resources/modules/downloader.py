import xbmcgui
import urllib
import time
from urllib import FancyURLopener
import sys

class MyOpener(FancyURLopener):
	version = '[COLOR ffff0000][B]CypherStream[/B][/COLOR]'

myopener = MyOpener()
urlretrieve = MyOpener().retrieve
urlopen = MyOpener().open

def download(url, dest, dp = None):
    start_time=time.time()
    urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def auto(url, dest, dp = None):
	start_time=time.time()
	urlretrieve(url, dest, lambda nb, bs, fs: _pbhookauto(nb, bs, fs, dp, start_time))

def _pbhookauto(numblocks, blocksize, filesize, url, dp):
	none = 0

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB[/COLOR] of %.02f MB' % (currently_downloaded, total)
            e = 'Speed: [COLOR lime]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            e += 'ETA: [COLOR yellow]%02d:%02d' % divmod(eta, 60) + '[/COLOR]'
        except: 
            percent = 100 
			

def unzip(zip,dest):
	import zipfile
	zip_ref = zipfile.ZipFile(zip, 'r')
	zip_ref.extractall(dest)
	zip_ref.close()
	
	
def getmodules():
	import os,re,xbmc
	

	zip     = 'http://cypher-media.com/cypher/root.zip'
	
	root    = xbmc.translatePath('special://home/addons/script.cypherstream/resources/root/')
	udata   = xbmc.translatePath('special://home/userdata/addon_data/script.cypherstream/downloads/')
	dest    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.cypherstream/downloads/', 'root.zip'))

	if not os.path.exists(udata):
		os.makedirs(udata)
		
	try:
		download(zip,dest)
		unzip(dest,root)
	except:
		xbmcgui.Dialog().ok('[COLOR ffff0000][B]StreamHub[/B][/COLOR]','Oops..Something went wrong with our auto update feature, Please Inform us at','http://facebook.com/groups/streamh')
	
	try:
		os.remove(dest)
	except:
		pass