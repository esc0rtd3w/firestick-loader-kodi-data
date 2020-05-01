# -*- coding: utf-8 -*-
# moviedb TV SHOW Module by: Blazetamer


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

basetv_url ='http://www.merdb.cn/'
basetvshow_url ='http://www.merdb.cn/tvshow'
base_url ='http://www.merdb.cn'
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def MERDBTVCATS():
     
          main.addDir('All TV Shows','http://www.merdb.cn/tvshow/index.php','tvindex',artwork + 'all.jpg','','dir')
          main.addDir('Featured TV Shows','http://www.merdb.cn/tvshow/?sort=featured','tvindex',artwork + 'featured.jpg','','dir')
          main.addDir('TV Shows by Popularity','http://www.merdb.cn/tvshow/?featured=1&sort=views','tvindex',artwork + 'popular.jpg','','dir')
          main.addDir('TV Shows by Rating','http://www.merdb.cn/tvshow/?featured=1&sort=ratingp','tvindex',artwork + 'rating.jpg','','dir')
          main.addDir('TV Shows by Release Date','http://www.merdb.cn/tvshow/?sort=year','tvindex',artwork + 'releasedate.jpg','','dir')
          main.addDir('TV Shows by Date Added','http://www.merdb.cn/tvshow/?sort=stamp','tvindex',artwork + 'dateadded.jpg','','dir')
          main.addDir('[COLOR gold]Search TV Shows[/COLOR]','http://www.merdb.cn/tvshow/?search=','searchtv',artwork + 'search.jpg','','dir')
          
          main.AUTO_VIEW('')    
  
        
def TVINDEX (url):
   
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" class=".+?" alt=".+?"/></a><div class=".+?"><a href="(.+?)" title="(.+?)">(.+?)</a>').findall(link)
        if len(match) > 0:
         for sitethumb,url,movie_name,fullyear in match:
                
                inc = 0
                #movie_name = fullyear[:-6]
                year = fullyear[-6:]
                #movie_name = movie_name.decode('UTF-8','ignore')
              
                data = main.GRABTVMETA(movie_name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               

                favtype = 'tvshow'
                addMERDBDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,data,favtype)
                
                #main.addSDir(movie_name +'('+ year +')',basetv_url + url,'episodes',thumb,year,favtype)
                
         nmatch=re.compile('<span class="currentpage">.+?</span></li><li><a href="(.+?)">(.+?)</a></li><li>').findall(link)
         if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                     
                main.addDir('Page'+ pageno,basetvshow_url + pageurl,'tvindex',artwork +'nextpage.jpg','','dir')
             
        main.AUTO_VIEW('tvshow')
   
        
def TVPLAYGENRE (url):
   
        link = net.http_GET(url).content
        match=re.compile('<a href="(.+?)" title=".+?">\r\n                        <img src="(.+?)" class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
        if len(match) > 0:
         for url,sitethumb,name in match:
          matchyear=re.compile('<a class="filmyar" href="http://moviedb.name/browse_tv_shows/all/byViews/(.+?)/">\r\n').findall(link)
          if len(matchyear) > 0:
             for year in matchyear:        
                 data = main.GRABTVMETA(name,year)
                 thumb = data['cover_url']
                
                   
             types = 'tvshow'
             main.addSDir(name,url,'episodes',thumb,'',types)
             nmatch=re.compile('<a id="next" class=".+?" href="(.+?)">Next &raquo</a>').findall(link)
        if len(nmatch) > 0:
        
                    main.addDir('Next Page',(nmatch[0]),'tvplaygenre',artwork + 'nextpage.jpg','','dir')
             
                    main.AUTO_VIEW('')
   

def SEARCHSHOW(url):
              
             link = net.http_GET(url).content
             match=re.compile('<a href="(.+?)">\r\n        <img src=".+?" data-original="(.+?)"  class=".+?" style=".+?"  border=".+?" height=".+?" width=".+?" alt="Watch (.+?) Online for Free">\r\n').findall(link)
             if len(match) > 0:
              for url,sitethumb,name in match:
               matchyear=re.compile('<div class="filmyar"><a class="filmyar" href="http://moviedb.name/browse_tv_shows/all/byViews/.+?/">(.+?)</a>').findall(link)
               if len(match) > 0:
                    for year in matchyear:        
                         data = main.GRABTVMETA(name,year)
                         thumb = data['cover_url']
                    types = 'tvshow'
                    if 'watch_tv_show' in url:
                              main.addTVDir(name,url,'episodes',thumb,data,types,'')
                              main.AUTO_VIEW('tvshows')
   

                                
def EPISODES(url,name,thumb):
          
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,} 
    dlfoldername = name
    mainimg = thumb
    show = name
    link = net.http_GET(url).content
    matchurl=re.compile('<div class="tv_episode_item"> <a href="(.+?)">.+?<span class="tv_episode_name"> - (.+?)</span><span class="tv_episode_airdate"> - .+?</span>').findall(link)             
    for url,epname in matchurl:
         matchse=re.compile('/tvshow_watch.+?/season-(.+?)-episode-(.+?)').findall(url)
         for season,epnum in matchse:
              s = 'S' + season
              e = 'E' + epnum
              se = s+e
              name = se + ' ' + epname
              favtype = 'episodes'
              addMERDBEPDir(name,base_url + url,thumb,'tvlinkpage',show,dlfoldername,mainimg,season,epnum)
             
              main.AUTO_VIEW('episode')
  

def TVLINKPAGE(url,name,thumb,mainimg):
          
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        mainimg = mainimg
        link = net.http_GET(url).content
        match=re.compile('<span class="movie_version_link">.+?<a href="(.+?)"').findall(link)
  
        for url in match:
           if 'http://' not in url:     
                 url = base_url + url
           print 'host url look is' + url    
            
                   
           if inc < 50:
                 link = net.http_GET(url).content
                 hostmatch=re.compile('name="bottom" src="(.+?)"/>\n</frameset>').findall(link)        
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
   
        
def DLTVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,}
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
         
                
        main.RESOLVETVDL(name,url,thumb)

def TVVIDPAGE(url,name):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':mainimg, 'dlfoldername':dlfoldername,} 
        #link = net.http_GET(url).content
        #match=re.compile('<iframe.*?src="(http://.+?)".*?>').findall(link)
        
        #for url in match:
        url = url
        name =name
                
        main.RESOLVE2(name,url,thumb)

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHTV(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	TVINDEX(searchUrl)

	main.AUTO_VIEW('movies')


def addMERDBDir(name,url,mode,thumb,labels,favtype):
        name = name.replace('&#8211;','')
        name = name.replace("&#8217;","")
        name = name.replace("&#039;s","'s")
        name = unicode(name, errors='ignore')
        #name.decode('utf-8', errors='replace')
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

def addMERDBEPDir(name,url,thumb,mode,show,dlfoldername,mainimg,season,episode):
        name = name.replace('&#8211;','')
        name = name.replace("&#8217;","")
        name = name.replace("&#039;s","'s")
        name = unicode(name, errors='ignore')
        #name.decode('utf-8', errors='replace')
        contextMenuItems = []
        fullname = name
        ep_meta = None
        show_id = None
        meta = None
        othumb = thumb
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        if settings.getSetting('metadata') == 'true':
          #meta = grab.get_meta('tvshow',dlfoldername,'',season,episode)
          inc = 0
          movie_name = show[:-6]
          year = show[-6:]
          print 'Meta Year is ' +year
          print 'Meta Name is ' +movie_name
          
              
          meta = main.GRABTVMETA(movie_name,year)
          thumb = meta['cover_url']               
          yeargrab = meta['year']
          year = str(yeargrab)       
          #meta = grab.get_meta('tvshow',name,'')
          show_id = meta['imdb_id']
          print 'IMDB ID is ' +show_id
        else:
          fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
          thumb = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png'
        s,e = main.GET_EPISODE_NUMBERS(name)
        if settings.getSetting('metadata') == 'true':
          try:
              
              ep_meta = main.GRABEPISODEMETA(show_id,season,episode,'')
              if ep_meta['cover_url'] == '':
                    thumb = mainimg
              else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = mainimg
             
        else:
          thumb = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png'
          if thumb == '':
               thumb = mainimg
     
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':season, 'episode':episode, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}        
        if settings.getSetting('metadata') == 'true':
         contextMenuItems.append(('[COLOR gold]Tv Show Information[/COLOR]', 'XBMC.Action(Info)'))
         if ep_meta==None:
               fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
               addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems, img=thumb) 
         else:
               if meta['backdrop_url'] == '':
                    fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
               else:
                    fanart = meta['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta,contextmenu_items=contextMenuItems, fanart=fanart, img=thumb)
        else:
            addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems,fanart=fanart, img=thumb)
     

#NAME METHOD*****************************

