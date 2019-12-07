import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
import downloader
import extract
import time,re
import datetime
import shutil
from metahandler import metahandlers
from resources.modules import main
from resources.modules import live



from addon.common.addon import Addon
from addon.common.net import Net
net = Net(http_debug=True)
        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')

#PATHS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

URL= 'http://www.frightpix.com'

popartpath = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/popcornflix/images/', ''))



#HOOKS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')


def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link



def FRIGHTCATS():
    main.addDir('New Arrivals','http://www.frightpix.com/New%20Arrivals-movies','frightindexdeep','','','movies')
    main.addDir('Most Popular','http://www.frightpix.com/most-popular-movies','frightindexdeep','','','movies')
    link=OPEN_URL('http://www.frightpix.com/').replace('\n','').replace('\r','').replace('\t','')
    match=re.compile('Genres(.+?)<div class="copyright">').findall(link)
    genres = match[0]
    gmatch=re.compile('<a href="(.+?)">(.+?)</a>').findall(genres)
    for genre, name in gmatch:
        print 'Genres is ' +genre
      
        main.addDir(name,'http://www.frightpix.com'+genre,'frightindexdeep','','','movies')
    
    main.AUTO_VIEW('')
        
def FRIGHTINDEX(url,favtype):
          params = {'url':url, 'favtype':favtype}
          link = net.http_GET(url).content
          #match=re.compile('<a href="(.+?)">\n\t\t  <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
          match=re.compile('<a href="(.+?)">\n                    <img width="184" height="256" src="(.+?)" alt="(.+?)"/>').findall(link)
          for url,thumb,name in match:
                    url = URL + url
                    data = main.GRABMETA(name,'')
                    thumb = data['cover_url']
                    favtype = 'movies'
                    main.addMDCDir(name,url,'frightvideolinks',thumb,data,favtype)
                    main.AUTO_VIEW('movies')
                    

                
def FRIGHTVIDEOLINKS(name,url,thumb,favtype):
        params = {'url':url, 'name':name, 'thumb':thumb, 'favtype':favtype}
        link=OPEN_URL(url).replace('\n','').replace('\r','').replace(' ','')
        #link = net.http_GET(url).content.replace('\n','').replace('\r','').replace(' ','')
        match=re.compile('id="flashContent"data-videosrc="(.+?)"data-videodata="(.+?)"></div>').findall(link)
        matchyear=re.compile('<spanclass="year">(.+?)</span>').findall(link)
        for url,url2 in match:
             #if 'undefined' in url:
                  url = url2
                  for year in matchyear:
                       link = net.http_GET(url).content
                       url = URL + url
                       match4=re.compile('"poster":"(.+?)","slider":".+?","duration":.+?,"rating":"(.+?)","language":".+?","cuepoints":".+?","urls":{".+?":"(.+?)"}').findall(link)
                       for thumb,rating,url in match4:
                              #replace odd strings
                              thumb = thumb.replace("\/","/")
                              url = url.replace("\/","/")
                              mainimg = thumb
                              favtype = 'movies'
                              link = net.http_GET(url).content
                              match3=re.compile('RESOLUTION=864x480\r\n(.+?)\r\n#').findall(link)
                              for url in match3:
                                   live.addDir(name + year + ' Rated- ' +rating,url,'frightaddlink',thumb,'',fanart)
                                   main.AUTO_VIEW('movies')



def FRIGHTINDEX_DEEP(url,favtype):
        mainurl = url
        params = {'url':url,'favtype':favtype}  
        link=OPEN_URL(url)
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)"\n.+?alt="(.+?)"></a>\n\n').findall(link)
        #for url,thumb,name in match:
        for url,thumb,name in match[0:100]:
            
            
                    url = URL + url
                    data = main.GRABMETA(name,'')
                    thumb = data['cover_url'] 
                    main.addMDCDir(name,url,'frightvideolinks',thumb,data,favtype)
        if len(match) >=100:
                        
            main.addMDCDir('Next Page',mainurl,'frightindexdeeplarge','','',favtype)
                         
        main.AUTO_VIEW('movies')

def FRIGHTINDEX_DEEPLARGE(url,favtype):
        mainurl = url
        params = {'url':url,'favtype':favtype}  
        link=OPEN_URL(url)
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)"\n.+?alt="(.+?)"></a>\n\n').findall(link)
        #for url,thumb,name in match:
        for url,thumb,name in match[100:200]:
            
            
                    url = URL + url
                    data = main.GRABMETA(name,'')
                    thumb = data['cover_url'] 
                    main.addMDCDir(name,url,'frightvideolinks',thumb,data,favtype)
        if len(match) >=200:
                        
            main.addMDCDir('Next Page',mainurl,'frightindexdeeplarger','','',favtype)                 
        main.AUTO_VIEW('movies')

def FRIGHTINDEX_DEEPLARGER(url,favtype):
        mainurl = url
        params = {'url':url,'favtype':favtype}  
        link=OPEN_URL(url)
        match=re.compile('<a href="(.+?)"><img width="184" height="256" src="(.+?)"\n.+?alt="(.+?)"></a>\n\n').findall(link)
        #for url,thumb,name in match:
        for url,thumb,name in match[200:300]:
            
            
                    url = URL + url
                    data = main.GRABMETA(name,'')
                    thumb = data['cover_url'] 
                    main.addMDCDir(name,url,'frightvideolinks',thumb,data,favtype)
        if len(match) >=300:
                        
            main.addMDCDir('Next Page',mainurl,'frightindexdeeplarger','','',favtype)                 
        main.AUTO_VIEW('movies')                
               
	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def FRIGHTSEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching  FrightPix" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	frightindex,frightindex_DEEP(searchUrl,'')
        

                


def FRIGHTADDLINK(name,url,thumb):
         #params = {'url':url, 'name':name, 'thumb':thumb}      
         url= url
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         xbmc.executebuiltin("XBMC.Notification(Building Video File!,Please Wait,3000)")
         xbmc.sleep(1000)
         xbmc.Player ().play(url, liz, False)

         
             

def addDir(name,url,mode,thumb):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addlinkDir(name,url,mode,thumb):
     u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(thumb)
     liz = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
     liz.setProperty("IsPlayable","true")
     xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)

     
              








