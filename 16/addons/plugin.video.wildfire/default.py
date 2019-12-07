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
addonId = "plugin.video.wildfire"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
       
Host = "http://www.wildfireporn.com/cat/1.html"

def getUrl(url):
        pass#print "Here in getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def showContent():
        content = getUrl(Host)
	pass#print "content A =", content
	regexvideo = 'class="subCategoryList".*?href="(.*?)">(.*?)<'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, name in match:
               pic = " "
               addDirectoryItem(name, {"name":name, "url":url, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)


def showContent1(name, url):
        names = []
        urls = []
        names.append("Page-1")
        names.append("Page-2")
        names.append("Page-3")
        names.append("Page-4")
        names.append("Page-5")
        n1 = url.find(".html", 0)
        url1 = url[:n1] + ".html"
        url2 = url[:n1] + "-p2.html"
        url3 = url[:n1] + "-p3.html"
        url4 = url[:n1] + "-p4.html"
        url5 = url[:n1] + "-p5.html"
        urls.append(url1)
        urls.append(url2)
        urls.append(url3)
        urls.append(url4)
        urls.append(url5)
        i = 0
        for name in names:
               url = urls[i]
               pic = " "
               i = i+1
               addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
        

def getPage(name, url):
                pages = [1, 2, 3, 4, 5, 6]
                for page in pages:
                        url1 = url + "/videos?p=" + str(page)
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url1, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name1, urlmain):
	content = getUrl(urlmain)
	pass#print "content A =", content
	n1 = content.find("<!-- main content -->", 0)
	content = content[n1:]
	regexvideo = 'align="left"><a href="(.*?)"><img src="(.*?)".*?class="movie">(.*?)<'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, pic, name in match:
               addDirectoryItem(name, {"name":name, "url":url, "mode":4}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)


def getVideos1(name1, urlmain):
	content = getUrl(urlmain)
	pass#print "content B =", content

	regexvideo = 'host=StreamCloud&video=(.*?)"'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        surl = match[0]
        surl = surl.replace("%3A", ":")
        surl = surl.replace("%2F", "/")
        pass#print "Here in default-py surl =", surl
        stream_url = urlresolver.HostedMediaFile(url=surl).resolve()
        pass#print "Here in default-py stream_url =", stream_url
        player = xbmc.Player()
        player.play(stream_url)	

                
def playVideo(name, url):
           ##pass#print "Here in playVideo url =", url
           fpage = getUrl(url)
	   ##pass#print "fpage C =", fpage
           start = 0
           pos1 = fpage.find("source src", start)
           if (pos1 < 0):
                           return
  	   pos2 = fpage.find("http", pos1)
 	   if (pos2 < 0):
                           return
           pos3 = fpage.find('"', (pos2+5))
 	   if (pos3 < 0):
                           return                

           url = fpage[(pos2):(pos3)]

           pic = "DefaultFolder.png"
           ##pass#print "Here in playVideo url B=", url
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
                ok = showContent1(name, url)
#		ok = getPage(name, url)
	elif mode == str(3):
		ok = getVideos(name, url)	
        elif mode == str(4):
                import urlresolver
		ok = getVideos1(name, url)
	elif mode == str(5):
		ok = playVideo(name, url)	

		




































