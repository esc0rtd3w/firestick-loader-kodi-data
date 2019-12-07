
#  Live Module by: Blazetamer


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
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))


grab=metahandlers.MetaData()
net = Net()
def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

def SUPERTOONSCATS():
        main.addDir('[COLOR blue][B]***SUPERTOONS***[/B] [/COLOR]','none','supertoonscats',artwork+'supertoons.jpg','','dir')
        main.addDir('Best Cartoons','http://www.supercartoons.net/','supertoonsdirect',artwork+'bestcartoons.jpg','','dir')
        #main.addDir('Cartoons List','http://www.supercartoons.net/cartoons/1','supertoonsdirect',artwork+'toonlist.jpg','','dir')
        main.addDir('Characters','http://www.supercartoons.net/characters/1','supertoonsindex',artwork+'tooncharacters.jpg','','dir')
        #main.addDir('Studios','http://www.supercartoons.net/studios/1','supertoonsindex',artwork +'studios.jpg','','dir')
        main.AUTO_VIEW('')    


def SUPERTOONSINDEX(url):
        link = net.http_GET(url).content
        match=re.compile('class="img" href="(.+?)" title=".+?">\n\t\t\t<img src="(.+?)" alt="(.+?)Thumbnail"').findall(link)
        for url,thumb,name in match:
                main.addDir(name,url,'supertoonsdeep',thumb,'','dir')

        nmatch=re.compile('</a>\n\t<a href="(.+?)">(.+?)</a>').findall(link)
        if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                  main.addDir('[COLOR blue][B]Page '+ pageno+'[/B] [/COLOR]',pageurl,'supertoonsindex',artwork +'nextpage.jpg','','dir')

def SUPERTOONSDEEP(url):
        link = net.http_GET(url).content
        deepurl = url
        #match=re.compile('class="cartoons">\n\t<div class="cartoon">\n\t\t<a class="img" href="(.+?)" title="(.+?) ">\n\t\t        \t<img src="(.+?)" alt="(.+?)Thumbnail"').findall(link)
        match=re.compile('img src="(.+?)" alt=".+?" width=".+?" height=".+?" />\n        \t\t</a>\n\t\t<a class="title" href="(.+?)" title="(.+?) ">(.+?)</a>').findall(link)
        for thumb,url,description,name in match:
                link = net.http_GET(url).content
                match3=re.compile("file: \'(.+?)',\n\t\t\t\timage").findall(link)
                for url in match3:
                        main.addDir(name,url,'supertoonsresolve',thumb,'','dir')
                        
        link = net.http_GET(deepurl).content
        nmatch=re.compile('</a>\n\t<a href="(.+?)">(.+?)</a>').findall(link)
        if len(nmatch) > 0: 
          for pageurl,pageno in nmatch:
                  main.addDir('[COLOR blue][B]Page '+ pageno+'[/B] [/COLOR]',pageurl,'supertoonsdeep',artwork +'nextpage.jpg','','dir')                

def SUPERTOONSDIRECT(url):
        link = net.http_GET(url).content
        match=re.compile('<img src="(.+?)" alt=".+?" width=".+?" height=".+?" />\n\t\t</a>\n\t\t<span class="title">\n        \t<a href="(.+?)" title="(.+?)">(.+?)</a>').findall(link)
        for thumb,url,description,name in match:
                link = net.http_GET(url).content
                match3=re.compile("file: \'(.+?)',\n\t\t\t\timage").findall(link)
                for url in match3:
                        main.addDir(name,url,'supertoonsresolve',thumb,'','dir')   

def SUPERTOONSRESOLVE(name,url,iconimage):
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         main.AUTO_VIEW('')


  




