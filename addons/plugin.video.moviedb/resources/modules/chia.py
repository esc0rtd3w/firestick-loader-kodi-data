
#  Chia Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'


try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer




#addon = Addon(addon_id, sys.argv)
addon = main.addon
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


# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/showgunart/images/', ''))
else:
    artwork = xbmc.translatePath(os.path.join('http://addonrepo.com/xbmchub/moviedb/images/', ''))
grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def CHIACATS():
      
     main.addDir('Latest Anime Episodes','http://www.chia-anime.com/','chialatest',artwork+'anime/latestepisodes.jpg','','dir')
     main.addDir('Anime by Genres','none','chiagenres',artwork+'anime/genre.jpg','','dir')
     main.addDir('A-Z','none','chiaalph',artwork+'anime/a-z.jpg','','dir')
     main.addDir('Search Anime ','http://www.chia-anime.com/search/','searchanime',artwork +'anime/search.jpg','','dir')     
     main.AUTO_VIEW('')
        


def CHIALATEST(url):
         
     link = net.http_GET(url).content
     match=re.compile('<h3><a href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h3></div></center><div><span class="video-episode">.+?</span></div><div class="thumb" style="background: #000 url(.+?) no-repeat').findall(link)
     for url,name,thumb in match:
          thumb = thumb.replace('(','')
          thumb = thumb.replace(')','')
          main.addDir(name,url,'chiavidpage',thumb,'','')
          main.AUTO_VIEW('movies')
            

def CHIAVIDPAGE(url,name):
           
     link = net.http_GET(url).content
     matchvid=re.compile('Watch via Mobile</font></a><a id="download" target="_blank" href="(.+?)">.+?MP4 Video format').findall(link)
     for url in matchvid:
          addCHIADLDir(name,url,'chialinkpage',thumb,'','','','')
          main.AUTO_VIEW('movies')
         


def CHIAALPH():
          
     main.addDir('#','http://www.chia-anime.com/alpha/#','chiaalphmain',artwork+'anime/hash.jpg','','dir')
     main.addDir('A','http://www.chia-anime.com/alpha/A','chiaalphmain',artwork+'anime/a.jpg','','dir')
     main.addDir('B','http://www.chia-anime.com/alpha/B','chiaalphmain',artwork+'anime/b.jpg','','dir')
     main.addDir('C','http://www.chia-anime.com/alpha/C','chiaalphmain',artwork+'anime/c.jpg','','dir')
     main.addDir('D','http://www.chia-anime.com/alpha/D','chiaalphmain',artwork+'anime/d.jpg','','dir')
     main.addDir('E','http://www.chia-anime.com/alpha/E','chiaalphmain',artwork+'anime/e.jpg','','dir')
     main.addDir('F','http://www.chia-anime.com/alpha/F','chiaalphmain',artwork+'anime/f.jpg','','dir')
     main.addDir('G','http://www.chia-anime.com/alpha/G','chiaalphmain',artwork+'anime/g.jpg','','dir')
     main.addDir('H','http://www.chia-anime.com/alpha/H','chiaalphmain',artwork+'anime/h.jpg','','dir')
     main.addDir('I','http://www.chia-anime.com/alpha/I','chiaalphmain',artwork+'anime/i.jpg','','dir')
     main.addDir('J','http://www.chia-anime.com/alpha/J','chiaalphmain',artwork+'anime/j.jpg','','dir')
     main.addDir('K','http://www.chia-anime.com/alpha/K','chiaalphmain',artwork+'anime/k.jpg','','dir')
     main.addDir('L','http://www.chia-anime.com/alpha/L','chiaalphmain',artwork+'anime/l.jpg','','dir')
     main.addDir('M','http://www.chia-anime.com/alpha/M','chiaalphmain',artwork+'anime/m.jpg','','dir')
     main.addDir('N','http://www.chia-anime.com/alpha/N','chiaalphmain',artwork+'anime/n.jpg','','dir')
     main.addDir('O','http://www.chia-anime.com/alpha/O','chiaalphmain',artwork+'anime/o.jpg','','dir')
     main.addDir('P','http://www.chia-anime.com/alpha/P','chiaalphmain',artwork+'anime/p.jpg','','dir')
     main.addDir('Q','http://www.chia-anime.com/alpha/Q','chiaalphmain',artwork+'anime/q.jpg','','dir')
     main.addDir('R','http://www.chia-anime.com/alpha/R','chiaalphmain',artwork+'anime/r.jpg','','dir')
     main.addDir('S','http://www.chia-anime.com/alpha/S','chiaalphmain',artwork+'anime/s.jpg','','dir')
     main.addDir('T','http://www.chia-anime.com/alpha/T','chiaalphmain',artwork+'anime/t.jpg','','dir')
     main.addDir('U','http://www.chia-anime.com/alpha/U','chiaalphmain',artwork+'anime/u.jpg','','dir')
     main.addDir('V','http://www.chia-anime.com/alpha/V','chiaalphmain',artwork+'anime/v.jpg','','dir')
     main.addDir('W','http://www.chia-anime.com/alpha/W','chiaalphmain',artwork+'anime/w.jpg','','dir')
     main.addDir('X','http://www.chia-anime.com/alpha/X','chiaalphmain',artwork+'anime/x.jpg','','dir')
     main.addDir('Y','http://www.chia-anime.com/alpha/Y','chiaalphmain',artwork+'anime/y.jpg','','dir')
     main.addDir('Z','http://www.chia-anime.com/alpha/Z','chiaalphmain',artwork+'anime/z.jpg','','dir')
          
        
     main.AUTO_VIEW('')
    

def CHIAGENRES(url):
         
     genreurl = 'http://www.chia-anime.com/?genre='
     main.addDir('Adventure',genreurl + 'adventure','chiagenremain',artwork+'/anime/adventure.jpg','','dir')
     main.addDir('Comedy',genreurl + 'comedy','chiagenremain',artwork+'/anime/comedy.jpg','','dir')
     main.addDir('Drama',genreurl + 'drama','chiagenremain',artwork+'/anime/drama.jpg','','dir')
     main.addDir('Erotica',genreurl + 'erotica','chiagenremain',artwork+'/anime/erotica.jpg','','dir')
     main.addDir('Fantasy',genreurl + 'fantasy','chiagenremain',artwork+'/anime/fantasy.jpg','','dir')
     main.addDir('Horror',genreurl + 'horror','chiagenremain',artwork+'/anime/horror.jpg','','dir')
     main.addDir('Mystery',genreurl + 'mystery','chiagenremain',artwork+'/anime/mystery.jpg','','dir')
     main.addDir('Romance',genreurl + 'romance','chiagenremain',artwork+'/anime/romance.jpg','','dir')
     main.addDir('Thriller',genreurl + 'thriller','chiagenremain',artwork+'/anime/thriller.jpg','','dir')
     main.addDir('Ninja',genreurl + 'ninga','chiagenremain',artwork+'/anime/ninja.jpg','','dir')
     main.addDir('Military',genreurl + 'milatary','chiagenremain',artwork+'/anime/military.jpg','','dir')
     main.addDir('Space',genreurl + 'space','chiagenremain',artwork+'/anime/space.jpg','','dir')
     main.addDir('Aliens',genreurl + 'aliens','chiagenremain',artwork+'/anime/aliens.jpg','','dir')
     main.addDir('Music',genreurl + 'music','chiagenremain',artwork+'/anime/music.jpg','','dir')
     main.addDir('Sports',genreurl + 'sports','chiagenremain',artwork+'/anime/sports.jpg','','dir')
     main.addDir('Demons',genreurl + 'demons','chiagenremain',artwork+'/anime/demons.jpg','','dir')
     main.addDir('Girls with Guns',genreurl + 'girls+with+guns','chiagenremain',artwork+'/anime/girlswithguns.jpg','','dir')
     main.addDir('Supernatural',genreurl + 'supernatural','chiagenremain',artwork+'/anime/supernatural.jpg','','dir')
     main.addDir('Police',genreurl + 'police','chiagenremain',artwork+'/anime/police.jpg','','dir')
     main.addDir('Vampires',genreurl + 'vampires','chiagenremain',artwork+'/anime/vampires.jpg','','dir')
     main.addDir('Super Powers',genreurl + 'superpowers','chiagenremain',artwork+'/anime/superpowers.jpg','','dir')
     main.addDir('Assassins',genreurl + 'assassins','chiagenremain',artwork+'/anime/assasins.jpg','','dir')
     main.addDir('Historical',genreurl + 'historical','chiagenremain',artwork+'/anime/historical.jpg','','dir')
     main.addDir('School',genreurl + 'school','chiagenremain',artwork+'/anime/school.jpg','','dir')
     main.addDir('Psychological',genreurl + 'psychological','chiagenremain',artwork+'/anime/psych.jpg','','dir')
     main.addDir('Martial Arts',genreurl + 'martial+arts','chiagenremain',artwork+'/anime/martialarts.jpg','','dir')
         
     main.AUTO_VIEW('')
   
              
def CHIAGENREMAIN(url):
        
     link = net.http_GET(url).content
     match=re.compile('overflow:hidden;"> <a href="(.+?)" title="(.+?)"><img width=".+?" height=".+?" src="(.+?)"></a>').findall(link)
     for url,name,thumb in match:
          name = name.replace('View all episode in','')
          main.addDir(name,url,'chiaepisodes',thumb,'','')
          main.AUTO_VIEW('movies')
           

def CHIASEARCH(url):
         
     link = net.http_GET(url).content
     match=re.compile('<img style="padding-left:0px;" width="135" height="190" src="(.+?)"></a></div><div class="title"><a href="(.+?)">(.+?)</a></div>').findall(link)
     for thumb,url,name in match:
          #name = name.replace('View all episode in','')
          main.addDir(name,url,'chialinkpage',thumb,'','')
          main.AUTO_VIEW('movies')
            

def CHIAALPHMAIN(url):
         
     link = net.http_GET(url).content
     match=re.compile('<img width=".+?" height=".+?" src="(.+?)"></a></p></div></td><div style="width:.+?; float:.+?;"><td class=".+?" style=".+?; overflow:.+?;"><div style="height:.+?; width:.+?;"><div style=".+?;"><a href="(.+?)" title="(.+?)">').findall(link)
     for thumb,url,name in match:
          name = name.replace('View all episode in','')
          main.addDir(name,url,'chiaepisodes',thumb,'','')
          main.AUTO_VIEW('movies')
       
               
def CHIAEPISODES(url,name,year,thumb):
        
    dlfoldername = name 
    link = net.http_GET(url).content
    match=re.compile('background: #000 url(.+?) no-repeat.+?;" alt="(.+?)"><a href="(.+?)"').findall(link)             
    for thumb,name,url in match:
         thumb = thumb.replace('(','')
         thumb = thumb.replace(')','')
         mainimg = thumb
         name = name.replace('&#8211','-')
         link = net.http_GET(url).content
         matchvid=re.compile('Watch via Mobile</font></a><a id="download" target="_blank" href="(.+?)">.+?MP4 Video format').findall(link)
         for url in matchvid:
              addCHIADLDir(name,url,'chialinkpage',thumb,'',dlfoldername,'',mainimg)
              main.AUTO_VIEW('movies')
               
          
                      

def CHIALINKPAGE(url,name,thumb):
       
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb}
     link = net.http_GET(url).content
     matchsource = re.compile('class="bttn green" href="(.+?)">Save mp4 as Link</a>').findall(link)
     for url in matchsource:
          CHIARESOLVE(name,url,thumb)
        
     
        

                     

#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

                
def SEARCHCIA(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for TV Shows" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	SEARCHSHOW(searchUrl)

	main.AUTO_VIEW('movies')


def CHIARESOLVE(name,url,iconimage):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         main.AUTO_VIEW('')


def CHIADLVIDPAGE(url,name):
       
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername,}
     link = net.http_GET(url).content
     matchsource = re.compile('class="bttn green" href="(.+?)">Save mp4 as Link</a>').findall(link)
     for url in matchsource:
                
                CHIARESOLVEDL(name,url,thumb)
               

def CHIARESOLVEDL(name,url,thumb):
           
               if '.mp4' in url:
                    ext = '.mp4'
               elif '.flv' in url:
                    ext = '.flv'
               elif '.avi' in url:
                    ext = '.avi'
               if not ext == '':
          
          
                    console = 'Downloads/Anime/'+ dlfoldername
                    params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername}
               
               

                    xbmc.sleep(1000)
        
                    main.addToQueue(name,url,thumb,ext,console)#.play(url, liz, False)
                      

#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def SEARCHANIME(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching for Anime" )
	# if blank or the user cancelled the keyboard, return
	if ( not vq ): return False, 0
	# we need to set the title to our query
	title = urllib.quote_plus(vq)
	searchUrl += title + '&criteria=title' 
	print "Searching URL: " + searchUrl 
	CHIASEARCH(searchUrl)

	main.AUTO_VIEW('movies')

#*******************For Chia DownloadDir***********************
def addCHIADLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype,'mainimg':mainimg}
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'chiadlvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)	

