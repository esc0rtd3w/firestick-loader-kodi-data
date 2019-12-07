#Porn Hub - Blazetamer.


import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import urlresolver
import cookielib
import downloader
from resources.modules import main


try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon

try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
net = Net(http_debug=True)
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

#========================DLStuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
repourl = addon.queries.get('repourl', '')


#PATHS

baseurl = 'http://www.pornhub.com'

def PHCATEGORIES():
         
    
    addDir('Amature Video','http://www.pornhub.com/video?c=3','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/3.jpg')
    addDir('Bi-Sexual','http://www.pornhub.com/video?c=76','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/76.jpg')
    addDir('Bondage','http://www.pornhub.com/video?c=10','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/10.jpg')
    addDir('Big Tits','http://www.pornhub.com/video?c=8','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/8.jpg')
    addDir('Threesome','http://www.pornhub.com/video?c=65','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/65.jpg')
    addDir('Celebrity','http://www.pornhub.com/video?c=12','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/12.jpg')
    addDir('Pornstar','http://www.pornhub.com/video?c=30','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/30.jpg')
    addDir('Female Friendly','http://www.pornhub.com/video?c=73','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/73.jpg')
    addDir('Masturbation ','http://www.pornhub.com/video?c=22','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/22.jpg')
    addDir('Cumshots','http://www.pornhub.com/video?c=16','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/16.jpg')
    addDir('Toys','http://www.pornhub.com/video?c=23','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/23.jpg')
    addDir('College','http://www.pornhub.com/categories/college','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/79.jpg')
    addDir('Big Dick','http://www.pornhub.com/video?c=7','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/7.jpg')
    addDir('Ebony','http://www.pornhub.com/video?c=17','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/17.jpg')
    addDir('Gay','http://www.pornhub.com/gayporn','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/63.jpg')
    addDir('Japanese','http://www.pornhub.com/video?c=111','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/111.jpg')
    addDir('Lesbian ','http://www.pornhub.com/video?c=27','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/27.jpg')
    addDir('Latina','http://www.pornhub.com/video?c=26','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/26.jpg')
    addDir('Massage','http://www.pornhub.com/video?c=78','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/78.jpg')
    addDir('Interracial','http://www.pornhub.com/video?c=25','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/25.jpg')
    addDir('MILF','http://www.pornhub.com/video?c=29','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/29.jpg')
    addDir('Uniforms','http://www.pornhub.com/video?c=81','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/81.jpg')
    addDir('Webcam','http://www.pornhub.com/video?c=61','phindex','http://cdn1a.static.pornhub.phncdn.com/images/categories/61.jpg')
    addDir('Search>>>','http://www.pornhub.com/video/search?search=','phsearch','')
    addDir('Top Rated','http://www.pornhub.com/video?o=tr','phindex','')
    addDir('All Videos','http://www.pornhub.com/video','phindex','')
    main.AUTO_VIEW('')
   
        
def OPEN_URL(url):
           
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link    
    
def PHINDEX(url):
   
    link=OPEN_URL(url)
    match=re.compile('href="(.+?)" title="(.+?)" class=".+?" data-related-url=".+?">\r\n\t\t\t\t\t\t\t\t\t<div class=".+?">\r\n\t\t\t\t<var class=".+?">.+?</var>\r\n\t\t\t\t\t\t\t</div>\r\n\t\t\t<img src=".+?" alt=".+?" data-smallthumb=".+?" data-mediumthumb="(.+?)"').findall(link)
    for url, name,thumb in match:
            addDir(name,baseurl + url,'phvideolinks',thumb)
    main.AUTO_VIEW('movies')
   
def PHVIDEOLINKS(url,name):
        
        link=OPEN_URL(url)
        match=re.compile('iframe src=&quot;(.+?)&quot;').findall(link)
        for url in match:
                 EMBED(url,name)
   
        
def EMBED(url,name):
           
        link=OPEN_URL(url).replace('\r','').replace('\n','').replace('\t','')
        #match=re.compile('data-src="(.+?)" poster="(.+?)"').findall(link)
        match=re.compile("video : {src: \'(.+?)',poster: \'(.+?)'").findall(link)
        for url,iconimage in match:
                 addLink(name,url,iconimage)
                 
               

#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default


#Start Search Function
def PHSEARCH(url):
	searchUrl = url 
	vq = _get_keyboard( heading="Searching  PornHub!!" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	searchUrl + title 
	print "Searching URL: " + searchUrl 
	PHINDEX(searchUrl)        

                
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name,iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo('video',{'Title':name,'Genre':'Live','Studio':name})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.sleep(1000)
        xbmc.Player ().play(url, liz, False)
        return ok


def addDir(name,url,mode,thumb):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb}
        desc = 'Like Porn? Dont forget to donate to Blazetamer'
        fanart = thumb
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              


