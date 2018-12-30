
# Series Gate Movie Module by: Blazetamer


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

base_url ='http://seriesgate.me/'
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def SGMOVIECATS():

          main.addMDCDir('All SeriesGate Movies','http://seriesgate.me/movies/browse/','sgmovieindex',artwork + 'all.jpg','','dir')  
          #main.addMDCDir('Featured Movies','http://seriesgate.me/movies/','sgmovieindex',artwork + 'featured.jpg','','dir')
          main.addMDCDir('Latest Movies','http://seriesgate.me/movies/latest/','sgmovieindex',artwork + 'latest.jpg','','dir')
          main.addMDCDir('Popular Movies','http://seriesgate.me/movies/popular/','sgmovieindex',artwork + 'popular.jpg','','dir')
          main.addMDCDir('By Genre','http://seriesgate.me/movies/browse/','sgmovieindexsec',artwork + 'genre.jpg','','dir')
          #main.addMDCDir('[COLOR gold]Search SeriesGate Movies[/COLOR]','http://www.moviesdatacenter.com/find/within-movies/','searchsgmovie',artwork + 'search.jpg','','dir')
          
          main.AUTO_VIEW('')    

        
def SGMOVIEINDEX (url):
        link = net.http_GET(url).content
        match=re.compile('"caption_title"><a  href = "(.+?)" >(.+?)</a></div><div class = "caption_imdb">(.+?)</div><div class = "caption_date_m">(.+?) </div>').findall(link)
        if len(match) > 0:
         for url,name,rate,year in match:     
                data = main.GRABMETA(name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               
                if thumb == '':
                  thumb = ''
                   
                favtype = 'movie'
                main.addMDCDir(name+ ' (' + year +')',base_url + url,'sgmovielinkpage',thumb,data,favtype)
             
        main.AUTO_VIEW('movies')

        
def SGMOVIEINDEXSEC (url):
        genre_url='http://seriesgate.me/movies/browse/#!All/All/'
        link = net.http_GET(url).content
        match=re.compile('"each_genre" id = "g_.+?" style = "">(.+?)</div>').findall(link)
        for genre in match:
                   
            favtype = 'movie'
            main.addMDCDir(genre,genre_url + url,'sgmovieindex','','',favtype)
                
                
        main.AUTO_VIEW('movies')
        



def SGMOVIESEARCH(url):
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" height=".+?" width=".+?" alt="Watch Movies: .+?" border=".+?" /></a></div><div class=".+?"><div class="title" style="display:inline-block;">.+? <a href="(.+?)" title=".+? >>> (.+?)">').findall(link)
        if len(match) > 0:
         for sitethumb,url,name in match:
            matchyear=re.compile('>Release:</td><td class="res"  style="padding:2px 0 6px 0;">.+?,(.+?)</td>').findall(link)     
            for year in matchyear:       
                data = main.GRABMETA(name,year)
                thumb = data['cover_url']               
                yeargrab = data['year']
                year = str(yeargrab)               
                if thumb == '':
                  thumb = sitethumb
                   
            favtype = 'movie'
            main.addMDCDir(name+ ' (' + year +')',base_url + url,'sgmovielinkpage',thumb,data,favtype)
             
        main.AUTO_VIEW('movies')             


                                



def SGMOVIELINKPAGE(url,name,thumb,mainimg):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,'mainimg':mainimg}
        inc = 0
        mainimg = mainimg
        link = net.http_GET(url).content
        match=re.compile('class="hre_watch" href="(.+?)"><img src=".+?"').findall(link)
  
        for url in match:
           print 'host url look is' + url    
            
                   
           if inc < 50:
                   urls = url
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
                                        main.addDLDir(name+hostname,urls,'vidpage',hthumb,data,dlfoldername,favtype,mainimg)
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

                
def SEARCHSGMOVIE(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for SeriesGate Movies" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '.html' 
	print "Searching URL: " + searchUrl 
	SGMOVIESEARCH (searchUrl)

	main.AUTO_VIEW('movies')



