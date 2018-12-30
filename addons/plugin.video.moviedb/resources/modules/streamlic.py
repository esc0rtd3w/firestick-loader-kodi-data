import urllib,urllib2,re,cookielib,string,sys,main
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from addon.common.addon import Addon
import datetime
import time
import os
from resources.modules import live
from addon.common.net import Net
net = Net()
addon_id = 'plugin.video.moviedb'
ADDON=xbmcaddon.Addon(id='plugin.video.moviedb')
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

def STREAMLICINDEX():
    main.addDir('All Stations','http://www.streamlicensing.com/directory/','streamlic','','','')
    #main.addDir('Genres','none','streamlicgenre','','','')
    main.addDir('[COLOR lime]Search Stations[/COLOR]','http://www.streamlicensing.com/directory/index.cgi?start=0&sid=&g=&e=0&s=','streamlicsearch','','','')
    

def STREAMLIC(url):
        link = net.http_GET(url).content
        link=link.replace('&quot;','').replace('&amp;','')
        match=re.compile('<a onClick="callToActionscript[(,]\'.+?\', \'(.+?)\', \'(.+?)\', \'\', \'.+?\', \'.+?\'[),]').findall(link)
        if len(match) > 0:
          for ipadd,port in match:
            murl ='http://'+ipadd+':'+port+'/;stream.mp3'
            matchname=re.compile('Station Name:</font></td><td width="550" style="padding-left: 10px;"><font size="3">(.+?)</font>').findall(link)
            if len(matchname) > 0:
                for name in matchname:
                    main.addDir(name,murl,'liveresolve','','','')
            nmatch=re.compile("href='(.+?)'><font color='black'>Next Page").findall(link)
            if len(nmatch) > 0: 
                addDir('[COLOR lime]Next Page[/COLOR]','http://www.streamlicensing.com/directory/'+(nmatch[0]),'streamlic','','','')
                return
            
def STREAMLICGENRES(url):
    link = net.http_GET(url).content
    link=link.replace('&quot;','').replace('&amp;','')
    match=re.compile('<a onClick="callToActionscript[(,]\'.+?\', \'(.+?)\', \'(.+?)\', \'\', \'.+?\', \'.+?\'[),]').findall(link)
    if len(match) > 0:
      for ipadd,port in match:
        murl ='http://'+ipadd+':'+port+'/;stream.mp3'
        matchname=re.compile('Station Name:</font></td><td width="550" style="padding-left: 10px;"><font size="3">(.+?)</font>').findall(link)
        if len(matchname) > 0:
            for name in matchname:
                main.addDir(name,murl,'liveresolve','','','')
        nmatch=re.compile("href='(.+?)'><font color='black'>Next Page").findall(link)
        if len(nmatch) > 0: 
            addDir('[COLOR lime]Next Page[/COLOR]','http://www.streamlicensing.com/directory/'+(nmatch[0]),'streamlic','','','')
            return



#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def STREAMLICSEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for Stations" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	STREAMLIC(searchUrl)

	main.AUTO_VIEW('movies')    
    

def addDir(name,url,mode,thumb,desc,favtype):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Audio", infoLabels={ "title": name,} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        

