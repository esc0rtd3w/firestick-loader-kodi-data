# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import urllib2,urllib,xbmcgui,os,xbmc
from parsers import links

addonName		= links.link().addonName
addonPath   	= links.link().addonPath
getSetting		= links.link().getSetting
language		= links.link().language
movieLibrary	= os.path.join(xbmc.translatePath(getSetting("movie_library")),'')


def open_url(url,post=None,headers=None):
	try:
		if not post:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
			req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		else:
			req = urllib2.Request(url,post,headers)
		response = urllib2.urlopen(req,timeout=15)
		link=response.read()
		response.close()
		return link
	except BaseException as e: print '##ERROR-addonsresolver:open_url: '+str(url)+' '+str(e)
	
def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()
	
def readoneline(file):
	f = open(file,"r")
	line = f.read()
	f.close()
	return line
	
def infoDialog(str, header=addonName):
	try: xbmcgui.Dialog().notification(header, str, addonPath+'icon.png', 3000, sound=False)
	except: xbmc.executebuiltin("Notification(%s,%s, 6000, %s)" % (header, str, addonPath+'icon.png'))
	
def removestrm(strmPath):
	try:
		for root,dir,files in os.walk(strmPath):
			for f in files: os.unlink(os.path.join(root, f))
	except BaseException as e: print "removecache ERROR: %s" % (str(e))
	
def getstrm(strmPath):
	paths = []
	try:
		for root,dir,files in os.walk(strmPath):
			for f in files: paths.append(os.path.join(root, f))
		return paths
	except BaseException as e: print "getstrm ERROR: %s" % (str(e))
	
def library_movie_add(name,url,imdbid,year):
	try:
		if getSetting("check_library") == 'true': filter = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["imdbnumber"]}, "id": 1}' % (year, str(int(year)+1), str(int(year)-1)))
		filter = unicode(filter, 'utf-8', errors='ignore')
		filter = json.loads(filter)['result']['movies']
		filter = [i for i in filter if imdbid in i['imdbnumber']][0]
	except: filter = []
	try:
		if not filter == []: return
		if not os.path.exists(movieLibrary): os.makedirs(movieLibrary)
		sysname, sysyear, sysimdb, sysurl = urllib.quote_plus(name), urllib.quote_plus(year), urllib.quote_plus(imdbid), 'external'
		content = '%s?action=play&name=%s&year=%s&imdbid=%s&url=%s' % (links.link().addon_plugin, sysname, sysyear, sysimdb, sysurl)
		enc_name = name.translate(None, '\/:*?"<>|').strip('.')+' (%s)' % sysyear
		folder = os.path.join(movieLibrary,enc_name)
		if not os.path.exists(folder): os.makedirs(folder)
		stream = os.path.join(folder, enc_name + '.strm')
		writefile(stream,'w',content)
		infoDialog(language(30309).encode("utf-8"))
		if getSetting("update_library") == 'true' and not xbmc.getCondVisibility('Library.IsScanningVideo'): xbmc.executebuiltin('UpdateLibrary(video)')		
	except BaseException as e: 
		print "basic.library_movie_add ERROR: %s - %s" % (str(name),str(e).decode('ascii','ignore'))
		return