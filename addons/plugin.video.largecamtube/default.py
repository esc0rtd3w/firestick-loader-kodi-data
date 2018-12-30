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
addonId = "plugin.video.largecamtube"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
if not path.exists(dataPath):
       cmd = "mkdir -p " + dataPath
       system(cmd)
       
Host = "http://www.largecamtube.com/"

def getUrl(url):
        pass#print "Here in getUrl url =", url
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link
	
def showContent():
        pic = " "
        addDirectoryItem("Search", {"name":"Search", "url":Host, "mode":4}, pic)           
        i = 0           
        content = getUrl(Host)
	pass#print "content A =", content
	n1 = content.find('<div class="list bullet clear">', 0)
        n2 = content.find('</div>', n1)
        content = content[n1:n2]

	regexvideo = '<a href="(.*?)">(.*?)<'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 pic = " "
                 pass#print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
#http://www.tubesex.com/search/?q=Anal&kwid=5462&c=1&p=2&lid=1
def getPage(name, urlmain):
                pass#print "name =", name
	        pass#print "urlmain =", urlmain
                pages = [1, 2, 3, 4, 5, 6]
                n1 = urlmain.find("&lid=1",0)
                if (n1 < 0):
                        return
#                pn = "2"
                url1 = urlmain[:(n1)]
                url2 = urlmain[n1:]
                for page in pages:
                        text = "?q=&p=" + str(page-1)
                        url = url1 + text + url2
                        name = "Page " + str(page)
                        pic = " "
                        addDirectoryItem(name, {"name":name, "url":url, "mode":2}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)

def getVideos(name1, urlmain):
	content = getUrl(urlmain)
	pass#print "content B =", content
#        pos0 = content.find("Promoted Videos", 0)
        
	regexvideo = '<div class="thumb">.*?href="(.*?)".*?img src="(.*?)" alt="(.*?)"'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        for url, pic, name in match:
                 name = name.replace('"', '')
                 pass#print "Here in getVideos url =", url
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	         
#http://www.tubesex.com/search/?lid=1&q=german+nikita&submit=Search        
def getVideos3(name, url):
                f = open("/tmp/xbmc_search.txt", "r")
                icount = 0
                for line in f.readlines(): 
                    sline = line
                    icount = icount+1
                    if icount > 0:
                           break

                name = sline.replace(" ", "+")
                url1 = "http://www.tubesex.com/search/?lid=1&q=" + name + "&submit=Search" 
                getVideos(name, url1)


        		
def getVideos2(name, url):
        pass#print "Here in getVideos2 url =", url
        content = getUrl(url)
	pass#print "content B2 =", content
	regexvideo = '<iframe src="(.*?)"'
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        url = match[0]
        pass#print "Here in getVideos2 url B=", url
        
	"""
        try:
               regexvideo = "clip.*?'(.*?)'"
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = match[0]
        except:
               pass
        try:
               regexvideo = "video_url: '(.*?)'"
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = match[0]
        except:
               pass
        try:
               regexvideo = 'var videoFile="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = match[0]
        except:
               pass
        try:
               regexvideo = '<source src="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = match[0]
        except:
               pass
        try:
               regexvideo = 'file="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = match[0]
        except:
               pass       
        try:
               regexvideo = 'file:"(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = match[0]
        except:
               pass   
        try:
               regexvideo = 'Quality FLV.*?a href="(.*?)"'
               match = re.compile(regexvideo,re.DOTALL).findall(content)
               pass#print "match =", match
               vurl = "http:" + match[0]
        except:
               pass   
        """
        if "xvideos" in url:
            url = url.replace("http://flashservice.xvideos.com/embedframe/", "http://www.xvideos.com/video") + "/"
            pass#print "Here in getVideos2 url C=", url
            content = getUrl(url)
            pass#print "content B3 =", content


            regexvideo = 'flv_url=(.*?)&amp;'
	    match = re.compile(regexvideo,re.DOTALL).findall(content)
            pass#print  "match =", match
            for url in match:
               url = url.replace("%3A", ":")
               url = url.replace("%2F", "/")
               url = url.replace("%3F", "?")
               url = url.replace("%3D", "=")
               url = url.replace("%26", "&")
               pass#print  "Here in getvideos2 url =", url
               player = xbmc.Player()
               player.play(url)
               break    
               
        elif "pornhub" in url.lower():
          pass#print "In pornhub "
          regexvideo = 'iframe src=&quot;(.*?)&quot;'
	  match = re.compile(regexvideo,re.DOTALL).findall(content)
	  pass#print "match =", match
          url1 = match[0]
          content = getUrl(url1)
          pass#print "content B3 =", content
          n1 = content.find(".mp4", 0)
          n2 = content.rfind("http", 0, n1)
          n3 = content.find("'", n1)
          url11 = content[n2:n3]
          player = xbmc.Player()
          pass#print "url11 C=", url11
          player.play(url11)          
        """
        if "tubeq" in url:
                regexvideo = "clip.*?'(.*?)'"
        elif "theclassicporn" in url:
                regexvideo = "video_url: '(.*?)'"
        elif "fantasy8" in url:
                regexvideo = 'var videoFile="(.*?)"'
        elif "kinkytube" in url:
                regexvideo = 'var videoFile="(.*?)"'
        elif "alphaporno" in url:
                regexvideo = "video_url: '(.*?)'"
        elif "vid2c" in url:
                regexvideo = 'var videoFile="(.*?)"'
        elif "hd21" in url:
                regexvideo = '<source src="(.*?)"'
        elif "winporn" in url:
                regexvideo = '<source src="(.*?)"'
        elif "wankoz" in url:
                regexvideo = "video_url: '(.*?)'"
        elif "drtuber" in url:
                regexvideo = '<source src="(.*?)"'
        elif "hd21" in url:
                regexvideo = '<source src="(.*?)"'
        elif "winporn" in url:
                regexvideo = '<source src="(.*?)"'        
 	else:
	        regexvideo = '<source src="(.*?)"'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        pass#print "match =", match
        vurl = match[0] 
        pass#print "vurl =", vurl       
        player = xbmc.Player()
        player.play(vurl) 
        """
        
def getVideos4(name1, urlmain):
        n1 = urlmain.find(".html",0)
        if (n1 < 0):
                return
        n2 = urlmain.rfind("-", 0, n1)
        if (n2 < 0):
                return
        pn = "4"
        url1 = urlmain[:(n2+1)]
        url2 = urlmain[n1:]
        #pass#print "Here in getVideos2 url1 =", url1
        #pass#print "Here in getVideos2 url2 =", url2
        url = url1 + pn + url2
        #pass#print "Here in getVideos2 url =", url
        content = getUrl(url)
	#pass#print "content B2 =", content
        pos0 = content.find("Promoted Videos", 0)
        if (pos0 < 0):
                return
	pos1 = content.find("<div class='video'", pos0)
        if (pos1 < 0):
                return
        content = content[pos1:]
	
	regexvideo = "><a href='(.*?)'.*?alt=(.*?)/>"
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        #pass#print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 pic = " " 
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
	name = "More videos"
	addDirectoryItem(name, {"name":name, "url":urlmain, "mode":7}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	

def getVideos5(name1, urlmain):
        n1 = urlmain.find(".html",0)
        if (n1 < 0):
                return
        n2 = urlmain.rfind("-", 0, n1)
        if (n2 < 0):
                return
        pn = "5"
        url1 = urlmain[:(n2+1)]
        url2 = urlmain[n1:]
        #pass#print "Here in getVideos2 url1 =", url1
        #pass#print "Here in getVideos2 url2 =", url2
        url = url1 + pn + url2
        #pass#print "Here in getVideos2 url =", url
        content = getUrl(url)
	#pass#print "content B2 =", content
        pos0 = content.find("Promoted Videos", 0)
        if (pos0 < 0):
                return
	pos1 = content.find("<div class='video'", pos0)
        if (pos1 < 0):
                return
        content = content[pos1:]
	
	regexvideo = "><a href='(.*?)'.*?alt=(.*?)/>"
	match = re.compile(regexvideo,re.DOTALL).findall(content)
        #pass#print "match =", match
        for url, name in match:
                 name = name.replace('"', '')
                 pic = " " 
	         addDirectoryItem(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)	

                
def playVideo(name, url):
           pass#print "Here in playVideo url =", url
           fpage = getUrl(url)
	   pass#print "fpage C =", fpage
           start = 0
           pos1 = fpage.find(".flv", start)
           if (pos1 < 0):
                           return
  	   pos2 = fpage.find("a href", pos1)
 	   if (pos2 < 0):
                           return
           pos3 = fpage.find('"', (pos2+10))
 	   if (pos3 < 0):
                           return                
           url = fpage[(pos2+8):pos3]
                    
           pic = "DefaultFolder.png"
           pass#print "Here in playVideo url B=", url
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
	        pass#print "name =", name
	        pass#print "url =", url
#		ok = getPage(name, url)
#        elif mode == str(2):
		ok = getVideos(name, url)        	
	elif mode == str(3):
		ok = getVideos2(name, url)		
	elif mode == str(4):
		ok = getVideos3(name, url)	
	elif mode == str(5):
		ok = getVideos3x(name, url)
	elif mode == str(6):
		ok = getVideos4(name, url)
	elif mode == str(7):
		ok = getVideos5(name, url)
		



