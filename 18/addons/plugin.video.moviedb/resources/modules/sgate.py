# -*- coding: utf-8 -*-
# moviedb Series Gate TV SHOW Module by: Blazetamer


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
show = addon.queries.get('show', '')


# Global Stuff
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

grab=metahandlers.MetaData()
net = Net()

basetv_url ='http://seriesgate.me/'
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def SGCATS():
         
          addDir('All Series Gate TV Shows','http://seriesgate.me/tvshows/','sgindex',artwork + 'all.jpg','','dir')
          addDir('[COLOR gold]Search TV Shows[/COLOR]','http://seriesgate.me/search/indv_episodes/','searchsgtv',artwork + 'search.jpg','','dir')
          
          main.AUTO_VIEW('')    
   
def SGINDEX (url):
         
        link = net.http_GET(url).content
        match=re.compile('<a href = "(.+?)"><img src = "(.+?)" height=".+?/><div class = "_tvshow_title">(.+?)</div>').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
                
                inc = 0
                #movie_name = fullyear[:-6]
                #year = fullyear[-6:]
                #movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABTVMETA(name,'')
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               
                dlfoldername = name
                favtype = 'tvshow'
                #main.addDir(name,url,'sgepisodelist',thumb,data,favtype)
                addDir(name,basetv_url + url,'sgepisodelist',thumb,data,favtype)
                
                #main.addSDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,year,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                addDir('Page'+ pageno,basetv_url + pageurl,'sgindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')
   
                                
def SGEPISODES(url,name,thumb):
        
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb} 
    dlfoldername = name
    mainimg = thumb
    show = name
    link = net.http_GET(url).content
    matchurl=re.compile('<div class="season_page">\n\t\t\t\t\t\t<a href="(.+?)" >(.+?)</a>').findall(link)             
    for url,snumber in matchurl:
              favtype = 'episodes'
              #main.addDir(snumber,url,'sgepisodelist',thumb,'',favtype)
              main.addEPNOCLEANDir(snumber,url,thumb,'sgepisodelist',show,dlfoldername,mainimg,'','')
             
              main.AUTO_VIEW('movies')
   
        
def SGEPISODELIST(url,name,thumb):
          
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb}
    dlfoldername = name
    mainimg = thumb
    show = name
    url2=url
    link = net.http_GET(url).content
    #match=re.compile('<a href="(.+?)">&raquo S(.+?) - E(.+?)  (.+?)</a><span>(.+?)</span>').findall(link)
    match=re.compile('<a href="(.+?)">&raquo S(.+?) - E(.+?)  (.+?)</a>').findall(link)
    for url,season,epnum,epname in match:
              s = 'S'+season
              e = 'E'+epnum
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPNOCLEANDir(name,url2+'/season'+season+'/episode'+epnum+'/searchresult',thumb,'sgtvlinkpage',show,dlfoldername,mainimg,season,epnum)
             
              main.AUTO_VIEW('movies')              
   
        
'''def SGEPISODELIST(url,name,thumb):
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb} 
    #dlfoldername = name
    mainimg = thumb
    link = net.http_GET(url).content
    match=re.compile('<div class=".+?" style=".+?" >Season(.+?) Episode(.+?)- <span><a href = ".+?">.+?</a></span></div><div class=".+?" >(.+?)</div><div class = ".+?"></div><div style=".+?"><a href="(.+?)"><img src="(.+?)" width=".+?" height=".+?"  alt=".+?" title = "(.+?)" ></a>').findall(link)             
    for season,epnum, date, url, thumb, epname in match:
              s = 'S'+season
              e = 'E'+epnum
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              main.addEPNOCLEANDir(name,url,thumb,'sgtvlinkpage',show,dlfoldername,mainimg,season,epnum)
             
              main.AUTO_VIEW('movies') '''             


def SGTVLINKPAGE(url,name,thumb,mainimg):
          
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        linkbase = 'http://seriesgate.me'
        mainimg = mainimg
        #link = net.http_GET(url).content
        #match=re.compile('href="(.+?)">More Links').findall(link)
        #for surl in match:
           #url = linkbase + surl
        #url = url +'searchresult/'    
            
                
  
        
        print 'host url look is' + url    
            
                   
        if inc < 50:
                 link = net.http_GET(url).content
                 #hostmatch=re.compile('<a rel="nofollow" href="(.+?)" TARGET="_blank" >(.+?)</a>').findall(link)
                 hostmatch=re.compile('hre_watch_tt" href="(.+?)">').findall(link)
                 #for urls,sourcename in hostmatch:
                 for urls in hostmatch:        
                   print 'Pre HMF url is  ' +urls
                   hmf = urlresolver.HostedMediaFile(urls)
                  ##########################################
                   print 'URLS is ' +urls
                   if hmf:
                          #try:
                                  host = hmf.get_host()
                                  hthumb = main.GETHOSTTHUMB(host)
                                  #dlurl = urlresolver.resolve(vidUrl)
                                  data = main.GRABTVMETA(name,'')
                                  thumb = data['cover_url']
                                  favtype = 'movie'
                                  hostname = main.GETHOSTNAME(host)
                                  try:    
                                        main.addTVDLDir(name+hostname,urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
                                        inc +=1
                                  except:
                                        continue
                                


#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHSGTV(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=tag' 
	print "Searching URL: " + searchUrl 
	SGSEARCHINDEX(searchUrl)

	main.AUTO_VIEW('movies')



def SGSEARCHINDEX (url):
           
        link = net.http_GET(url).content
        match=re.compile('</a><div class = ".+?" style=".+?"><div class = ".+?"><a href = "(.+?)">(.+?)</a>').findall(link)
        #match=re.compile('<a href="(.+?)">&raquo (.+?) - (.+?)  (.+?)</a>').findall(link)
        if len(match) > 0:
         for url,name in match:
         #for url,season,episode,name in match:        
                
                inc = 0
                #movie_name = fullyear[:-6]
                #year = fullyear[-6:]
                #movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABTVMETA(name,'')
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               
                dlfoldername = name
                favtype = 'tvshow'
                addDir(name,basetv_url + url,'sgepisodelist',thumb,data,favtype)
                
                #main.addSDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,year,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                addDir('Page'+ pageno,basetv_url + pageurl,'movieindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('movies')
   
def addDir(name,url,mode,thumb,labels,favtype):
        #name = nameCleaner(name)
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'dlfoldername':dlfoldername, 'mainimg':mainimg}
        contextMenuItems = []
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        sitethumb = thumb
        sitename = name
        fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
       
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb       
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
