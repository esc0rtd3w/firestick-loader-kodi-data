#IWatchOnline Module by : Bazetamer   Thanks to O9 for the basic code setup
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys,htmlcleaner
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

base_url = 'http://www.iwatchonline.to'

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



#PATHS
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

def AFnameCleaner(name):
        name = name.replace('&#8211;','')
        name = name.replace("&#8217;","")
        name = name.replace("&#039;s","'s")
        name = htmlcleaner.clean(name,strip=True)
        return(name)    


#Main Links 

def CATZEEMOVIES (url):
        addDir('Random Movies ','http://www.zmovie.tw/','zeemovies','','','dir')
        addDir('Genres','http://www.zmovie.tw/search/genre','zeegenres','','','dir')
        addDir('Featured Movies','http://www.zmovie.tw/movies/featured','zeemovies','','','dir')
        addDir('New Movies','http://www.zmovie.tw/movies/new','zeemovies','','','dir')
        addDir('Top Movies All-Time','http://www.zmovie.tw/movies/top','zeemovies','','','dir')

        
        main.AUTO_VIEW('')

def CATIWO (url):
        live.addDir('Featured Movies','http://www.iwatchonline.to/movies?sort=featured','iwomovies','','','')
        live.addDir('Popular','http://www.iwatchonline.to/movies?sort=popular','iwomovies','','','')
        live.addDir('Genre','none','iwogenres','','','')
        live.addDir('A-Z','none','iwoalph','','','')
        live.addDir('HD Movies','none','iwohd','','','')
        
        
        main.AUTO_VIEW('')

def CATTVSHOWS (url):
        addDir('Genre','http://www.iwatchonline.to/movies','iwogenres','','','dir')
        
        main.AUTO_VIEW('')

def ZEEGENRES(url):
        link = net.http_GET(url).content
        match=re.compile('float:left"> <a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
            name = name.replace("&#039;s","'s")
            favtype = 'movie'
            addDir(name,url,'zeemovies','','',favtype)
            main.AUTO_VIEW('movies')

def IWOHD():
        addDir('Recently Added',base_url +'//movies?sort=latest&quality=hd','iwomovies','','','')
        addDir('Popular',base_url + '//movies?sort=popular&quality=hd','iwomovies','','','')
        addDir('A-Z','none','iwohdalph','','','')            

def IWOGENRES(url):
        addDir('Action','http://www.iwatchonline.to/movies?gener=action','iwomovies','','','dir')
        addDir('Adventure','http://www.iwatchonline.to/movies?gener=adventure','iwomovies','','','dir')
        addDir('Animation','http://www.iwatchonline.to/movies?gener=animation','iwomovies','','','dir')
        addDir('Biography','http://www.iwatchonline.to/movies?gener=biography','iwomovies','','','dir')
        addDir('Comedy','http://www.iwatchonline.to/movies?gener=comedy','iwomovies','','','dir')
        addDir('Crime','http://www.iwatchonline.to/movies?gener=crime','iwomovies','','','dir')
        addDir('Documentary','http://www.iwatchonline.to/movies?gener=documentery','iwomovies','','','dir')
        addDir('Drama','http://www.iwatchonline.to/movies?gener=drama','iwomovies','','','dir')
        addDir('Family','http://www.iwatchonline.to/movies?gener=family','iwomovies','','','dir')
        addDir('Fantasy','http://www.iwatchonline.to/movies?gener=fantasy','iwomovies','','','dir')
        addDir('Film-Noir','http://www.iwatchonline.to/movies?gener=film-noir','iwomovies','','','dir')
        addDir('History','http://www.iwatchonline.to/movies?gener=history','iwomovies','','','dir')
        addDir('Horror','http://www.iwatchonline.to/movies?gener=horror','iwomovies','','','dir')
        addDir('Music','http://www.iwatchonline.to/movies?gener=music','iwomovies','','','dir')
        addDir('Musical','http://www.iwatchonline.to/movies?gener=musical','iwomovies','','','dir')
        addDir('Mystery','http://www.iwatchonline.to/movies?gener=mystery','iwomovies','','','dir')
        addDir('News','http://www.iwatchonline.to/movies?gener=news','iwomovies','','','dir')
        addDir('Romance','http://www.iwatchonline.to/movies?gener=romance','iwomovies','','','dir')
        addDir('Sci-Fi','http://www.iwatchonline.to/movies?gener=sci-fi','iwomovies','','','dir')
        addDir('Short','http://www.iwatchonline.to/movies?gener=short','iwomovies','','','dir')
        addDir('Sport','http://www.iwatchonline.to/movies?gener=sport','iwomovies','','','dir')
        addDir('Thriller','http://www.iwatchonline.to/movies?gener=thriller','iwomovies','','','dir')
        addDir('War','http://www.iwatchonline.to/movies?gener=war','iwomovies','','','dir')
        addDir('Western','http://www.iwatchonline.to/movies?gener=western','iwomovies','','','dir')
        main.AUTO_VIEW('')

        
def IWOALPH():
        addDir('#',base_url + '/movies?startwith=09','iwomovies','','','dir')
        addDir('A',base_url + '/movies?startwith=a','iwomovies','','','dir')
        addDir('B',base_url + '/movies?startwith=b','iwomovies','','','dir')
        addDir('C',base_url + '/movies?startwith=c','iwomovies','','','dir')
        addDir('D',base_url + '/movies?startwith=d','iwomovies','','','dir')
        addDir('E',base_url + '/movies?startwith=e','iwomovies','','','dir')
        addDir('F',base_url + '/movies?startwith=f','iwomovies','','','dir')
        addDir('G',base_url + '/movies?startwith=g','iwomovies','','','dir')
        addDir('H',base_url + '/movies?startwith=h','iwomovies','','','dir')
        addDir('I',base_url + '/movies?startwith=i','iwomovies','','','dir')
        addDir('J',base_url + '/movies?startwith=j','iwomovies','','','dir')
        addDir('K',base_url + '/movies?startwith=k','iwomovies','','','dir')
        addDir('L',base_url + '/movies?startwith=l','iwomovies','','','dir')
        addDir('M',base_url + '/movies?startwith=m','iwomovies','','','dir')
        addDir('N',base_url + '/movies?startwith=n','iwomovies','','','dir')
        addDir('O',base_url + '/movies?startwith=o','iwomovies','','','dir')
        addDir('P',base_url + '/movies?startwith=p','iwomovies','','','dir')
        addDir('Q',base_url + '/movies?startwith=q','iwomovies','','','dir')
        addDir('R',base_url + '/movies?startwith=r','iwomovies','','','dir')
        addDir('S',base_url + '/movies?startwith=s','iwomovies','','','dir')
        addDir('T',base_url + '/movies?startwith=t','iwomovies','','','dir')
        addDir('U',base_url + '/movies?startwith=u','iwomovies','','','dir')
        addDir('V',base_url + '/movies?startwith=v','iwomovies','','','dir')
        addDir('W',base_url + '/movies?startwith=w','iwomovies','','','dir')
        addDir('X',base_url + '/movies?startwith=x','iwomovies','','','dir')
        addDir('Y',base_url + '/movies?startwith=y','iwomovies','','','dir')
        addDir('Z',base_url + '/movies?startwith=z','iwomovies','','','dir')    
def IWOHDALPH():
        addDir('#',base_url + '/movies?quality=hd&startwith=09','iwomovies','','','dir')
        addDir('A',base_url + '/movies?quality=hd&startwith=a','iwomovies','','','dir')
        addDir('B',base_url + '/movies?quality=hd&startwith=b','iwomovies','','','dir')
        addDir('C',base_url + '/movies?quality=hd&startwith=c','iwomovies','','','dir')
        addDir('D',base_url + '/movies?quality=hd&startwith=d','iwomovies','','','dir')
        addDir('E',base_url + '/movies?quality=hd&startwith=e','iwomovies','','','dir')
        addDir('F',base_url + '/movies?quality=hd&startwith=f','iwomovies','','','dir')
        addDir('G',base_url + '/movies?quality=hd&startwith=g','iwomovies','','','dir')
        addDir('H',base_url + '/movies?quality=hd&startwith=h','iwomovies','','','dir')
        addDir('I',base_url + '/movies?quality=hd&startwith=i','iwomovies','','','dir')
        addDir('J',base_url + '/movies?quality=hd&startwith=j','iwomovies','','','dir')
        addDir('K',base_url + '/movies?quality=hd&startwith=k','iwomovies','','','dir')
        addDir('L',base_url + '/movies?quality=hd&startwith=l','iwomovies','','','dir')
        addDir('M',base_url + '/movies?quality=hd&startwith=m','iwomovies','','','dir')
        addDir('N',base_url + '/movies?quality=hd&startwith=n','iwomovies','','','dir')
        addDir('O',base_url + '/movies?quality=hd&startwith=o','iwomovies','','','dir')
        addDir('P',base_url + '/movies?quality=hd&startwith=p','iwomovies','','','dir')
        addDir('Q',base_url + '/movies?quality=hd&startwith=q','iwomovies','','','dir')
        addDir('R',base_url + '/movies?quality=hd&startwith=r','iwomovies','','','dir')
        addDir('S',base_url + '/movies?quality=hd&startwith=s','iwomovies','','','dir')
        addDir('T',base_url + '/movies?quality=hd&startwith=t','iwomovies','','','dir')
        addDir('U',base_url + '/movies?quality=hd&startwith=u','iwomovies','','','dir')
        addDir('V',base_url + '/movies?quality=hd&startwith=v','iwomovies','','','dir')
        addDir('W',base_url + '/movies?quality=hd&startwith=w','iwomovies','','','dir')
        addDir('X',base_url + '/movies?quality=hd&startwith=x','iwomovies','','','dir')
        addDir('Y',base_url + '/movies?quality=hd&startwith=y','iwomovies','','','dir')
        addDir('Z',base_url + '/movies?quality=hd&startwith=z','iwomovies','','','dir')

def ZEEMOVIES(url):
        link = net.http_GET(url).content
        
        match=re.compile('relative;"><a href="(.+?)" title="(.+?)">').findall(link)
        
        inc = 0
        if len(match) > 0:
         for url,name in match:      


             inc += 1
             if inc > 8:
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore')
                                
                data = main.GRABMETA(movie_name,year)
                thumb = data['cover_url']
                

                favtype = 'movie'
                addDir(name,url,'zeevidpage',thumb,data,favtype)

                main.AUTO_VIEW('movies')

def IWOMOVIES(url):
        link = net.http_GET(url).content
        
        match=re.compile('<a href="(.+?)" class=".+?" rel=".+?">\r\n\t\t\t\t\t\t\t<img class=".+?" src="(.+?)" alt="">\r\n\t\t\t\t\t\t\t <div class=".+?">.+?</div>\t  \r\n\t\t\t\t\t\t</a>\r\n\t\t\t\t\t\t<div class=".+?">(.+?)\t\t\t\t\t\t<div').findall(link)
        inc = 0
        if len(match) > 0:
         for url,thumbnail,name in match:       

             inc += 1
             if inc > 6:
                movie_name = name[:-4]
                year = name[-4:]
                movie_name = movie_name.decode('UTF-8','ignore')               
                data = main.GRABMETA(movie_name,year)
                favtype = 'movie'
                addDir(name,url,'iwovidpage',thumbnail,data,favtype)
                match=re.compile('<li class="next pagea"><a href="(.+?)">Next &rarr;</a>').findall(link)
         for url in match:       
          if len(match) > 0:
                  url = url.replace('&amp;','&')
                  addDir('Next Page',url,'iwomovies','','','dir')

                  main.AUTO_VIEW('movies')



def LATESTO(url):
        link = net.http_GET(url).content
        match=re.compile('<a data-id="tooltip" href="(.+?)">\n<i class="icon-c-play fixed"></i>\n<img width="260" height="380" class="poster" src="(.+?)" alt="(.+?)"/>\n</a>\n<div class="caption">\n<a data-id="tooltip".+?">\n<h4>.+?</h4>\n</a>\n<table class="table table-custom">\n<tr>\n<th>Genre </th>\n<td>.+?</td>\n</tr>\n<tr>\n<th>Year </th>\n<td>(.+?)</td>').findall(link)
        inc = 0
        if len(match) > 0:
         for url,thumb,name,year in match:       
             name = name+'('+year+')'

             inc += 1
             if inc > 8:
                movie_name = name[:-6]
                year = name[-6:]
                movie_name = movie_name.decode('UTF-8','ignore') 
                data = main.GRABMETA(movie_name,year)
                favtype = 'movie'
                addDir(name,url,'linkpage',thumb,data,favtype)

                main.AUTO_VIEW('movies')

                   
def LINKPAGE(url,name):
        link = net.http_GET(url).content
        match=re.compile('target="_blank"   href="(.+?)"> <b> Watch Full </b></a> </td>').findall(link)
        for url in match:
                addDir(name,url,'vidpage',thumb,data,favtype)
                    
                favtype = 'movie'
                main.AUTO_VIEW('movies')
                
def ZEEVIDPAGE(url,name):
        dlfoldername = name
        titlename = name
        link = net.http_GET(url).content
        match=re.compile('target="_blank"   href="(.+?)"> <b> Watch Full </b></a> </td>').findall(link)
        for urls in match:
                
                hmf = urlresolver.HostedMediaFile(urls)
                   ##########################################
                print 'URLS is ' +urls
                
                print 'Pre HMF url is  ' +urls
                if hmf:
                          #try:
                                    host = hmf.get_host()
                                    hthumb = main.GETHOSTTHUMB(host)  
                                    favtype = 'movie'
                                    hostname = main.GETHOSTNAME(host)
                                    main.addDLDir(titlename+hostname,urls,'vidpage',hthumb,'',dlfoldername,favtype,'')
                                    favtype = 'movie'
                                    main.AUTO_VIEW('')





def IWOVIDPAGE(url,name):
        dlfoldername = name
        titlename = name
        link = net.http_GET(url).content
        match=re.compile('<a class="KAKA" href="(.+?)" target="_blank" rel="nofollow">').findall(link)
        for url in match:
            link = net.http_GET(url).content
            match=re.compile('<iframe name="frame" class="frame" src="(.+?)"').findall(link)
            for urls in match:
                hmf = urlresolver.HostedMediaFile(urls)
                   ##########################################
                print 'URLS is ' +urls
                
                print 'Pre HMF url is  ' +urls
                if hmf:
                          #try:
                                    host = hmf.get_host()
                                    hthumb = main.GETHOSTTHUMB(host)
                                    favtype = 'movie'
                                    hostname = main.GETHOSTNAME(host)
                                    #main.addDLDir(titlename,urls,'vidpage',hthumb,'',dlfoldername,favtype,thumb)
                                    addDir(titlename+hostname,urls,'vidpage',hthumb,'','')
                                    main.AUTO_VIEW('')                
                 


def ZEERESPASS(url,name):
        #if 'vidshark' in url:
             #vidshark.VIDINDEX(url)

        main.RESOLVE(name,url,'')

def IWOFORVID(url,name):
        link = net.http_GET(url).content
        match=re.compile('<iframe name="frame" class="frame" src="(.+?)"').findall(link)
        for url in match:

         main.RESOLVE(name,url,'')


	
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching......" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title 
	print "Searching URL: " + searchUrl 
	INDEX(searchUrl)

	main.AUTO_VIEW('movies') 
        

        


def addDir(name,url,mode,thumb,labels,favtype):
        name = AFnameCleaner(name)
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

              










