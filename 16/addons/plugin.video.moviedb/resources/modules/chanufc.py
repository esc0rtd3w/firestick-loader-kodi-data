# -*- coding: utf-8 -*-
# Cghannelcut UFC  Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'
#addon = Addon(addon_id, sys.argv)
addon = main.addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer






# Cache  
cache = StorageServer.StorageServer("MovieDB", 0)

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')

# Global Stuff
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

grab=metahandlers.MetaData()
net = Net()

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def CHANUFCCATS():
 
    
          main.addDir('UFC [COLOR red](ChannelCut)[/COLOR]','http://www.channelcut.me/?s=ufc&searchsubmit=Search','chanufcindex',artwork + 'ufc.jpg','','dir')
          
          
          main.AUTO_VIEW('')
   
        
def CHANUFCINDEX (url):
         
        link = net.http_GET(url).content
        match=re.compile('<h2><a href="(.+?)" rel="bookmark" title="(.+?)">').findall(link)
        if len(match) > 0:
         for url,name in match:
                
                
                dlfoldername = ''
                favtype = 'movies'
                main.addDir(name ,url,'ufclinkpage',artwork + 'ufc.jpg','',favtype)
                
                
                
         nmatch=re.compile('class="prev"><a href="(.+?)" >').findall(link)
         if len(nmatch) > 0: 
          for pageurl in nmatch:
                     
                main.addDir('[COLOR blue]Next Page>>[/COLOR]',pageurl,'chanufcindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')
         

        



                                


def UFCLINKPAGE(url,name):
          
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        link = net.http_GET(url).content
        match=re.compile('rel="nofollow">(.+?)</a>').findall(link)
        for urls in match:  
            
                   
           if inc < 50:
                   hmf = urlresolver.HostedMediaFile(urls)
                  ##########################################
                   print 'URLS is ' +urls
                   if hmf:
                          #try:
                                  host = hmf.get_host()
                                  hthumb = main.GETHOSTTHUMB(host)
                                  favtype = 'movie'
                                  try:    
                                        main.addUFCDLDir(name,urls,'vidpage',hthumb,'','UFC',favtype,artwork + 'ufc.jpg')
                                        inc +=1
                                  except:
                                        continue
                                  
                                   


def DLSPORTVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
         
                
        main.RESOLVESPORTDL(name,url,artwork + 'ufc.jpg')



#NAME METHOD*****************************

