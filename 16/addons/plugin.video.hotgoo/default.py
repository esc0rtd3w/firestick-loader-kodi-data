#!/usr/bin/python
# -*- coding: latin-1 -*-


import xbmc,xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
from os import path, system
import socket
from urllib2 import Request, URLError, urlopen
from urlparse import parse_qs
from urllib import unquote_plus



thisPlugin = int(sys.argv[1])
addonId = "plugin.video.hotgoo"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
       
Host = "http://www.hotgoo.com/category/"

def getUrl(url):
        pass#print"Here in getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def showContent():
        content = getUrl(Host)
        pass#print"content A =", content
    
        i1 = 0           
        if i1 == 0:
                regexcat = 'br><a href="(.*?)" class="red">(.*?)<'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                ##pass#print"match =", match
                pic = " "
                addDirectoryItem("Search", {"name":"Search", "url":Host, "mode":4}, pic)       
                for url, name in match:
                        url1 = "http://www.hotgoo.com" + url
                        pic = " "
                        ##pass#print"Here in Showcontent url1 =", url1
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":1}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getPage(name, url):
                pages = [1, 2, 3, 4, 5, 6]
                for page in pages:
                        url1 = url +  str(page)
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name1, urlmain):
	content = getUrl(urlmain)
	pass#print"content B =", content

	regexvideo = 'align=center><a href="(.*?)" class="red">(.*?)<.*?<img src="(.*?)"'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        ##pass#print"match =", match
        for url, name, pic in match:
                 name = name.replace('"', '')
                 url = "http://www.hotgoo.com" + url
                 pic = pic 
                 ##pass#print"Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
        
def getVideos2(name, url):
                f = open("/tmp/xbmc_search.txt", "r")
                icount = 0
                for line in f.readlines(): 
                    sline = line
                    icount = icount+1
                    if icount > 0:
                           break

                sname = sline.replace(" ", "+")
                pages = [1, 2, 3, 4, 5, 6]
                for page in pages:
                        url = "http://www.hotgoo.com/search.php?page=" + str(page) + "&query=" + sname
                        pass#print "Here in getVideos2 url =", url
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url, "mode":5}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

                
def playVideo(name, url):
           ##pass#print"Here in playVideo url =", url
           fpage = getUrl(url)
	   pass#print"fpage C =", fpage
           regexvideo = 'video controls src="(.*?)"'
	   match = re.compile(regexvideo,re.DOTALL).findall(fpage)
           url = match[0]
           pic = "DefaultFolder.png"
           ##pass#print"Here in playVideo url B=", url
           li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
           player = xbmc.Player()
           player.play(url, li)

std_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
}  

def addDirectoryItem(name, parameters={},pic=""):
    li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))

if not sys.argv[2]:
	ok = showContent()
else:
        if mode == str(1):
		ok = getPage(name, url)
	elif mode == str(2):
		ok = getVideos(name, url)	
	elif mode == str(3):
		ok = playVideo(name, url)	
	elif mode == str(4):
		ok = getVideos2(name, url)	
	elif mode == str(5):
		ok = getVideos(name, url)	

		















