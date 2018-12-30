
#  Live Streams Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers
from resources.utils import buggalo
import urlresolver
import ninestreams

from addon.common.addon import Addon
addon_id = 'plugin.video.moviedb'

from addon.common.net import Net
net = Net()
try:
     import StorageServer
except:
     import storageserverdummy as StorageServer




#addon = Addon(addon_id, sys.argv)
addon = main.addon
# Cache  
streamcache = StorageServer.StorageServer("MovieDBfavs", 0)
standardstreamcache = StorageServer.StorageServer("MovieDBSTfavs", 0)

mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
desc = addon.queries.get('desc', '')
gomode = addon.queries.get('gomode', '')


# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)
if settings.getSetting('theme') == '0':
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg', ''))
else:
    artwork = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/', ''))
    fanart = xbmc.translatePath(os.path.join('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart/fanart.jpg', ''))
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




def LIVECATS(url):
   try:        
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)
        #addDir('User Submitted Playlists' ,'http://goo.gl/JQzOhw','database',artwork +'submitted.jpg','User Submitted Playlists ',fanart)        
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()        
        
def COMMONSTREAMS(url):
   try:        
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                addDir(name,url,'livecatslist',thumb,'',thumb)                        
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()

def USERSTREAMS(url):
   try:
             link=OPEN_URL(url).replace('\n','').replace('\r','')
             match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
             for name,url,thumb in match:
                     addDir(name,url,'ninelists',thumb,'',thumb)
             match=re.compile('<name>(.+?)</name><thumbnail>(.+?)</thumbnail><link>(.+?)</link>').findall(link)
             for name,thumb,url in match:
                     addDir(name,url,'ninelists',thumb,'',thumb)
             match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
             for name,url,thumb in match:
                     addDir(name,url,'ninelists',thumb,'',thumb)         
             main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()

        
        
def USERSUB(url):
   try:        
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><submitted>(.+?)</submitted>').findall(link)
        for name,url,thumb,date in match:
                 addDir(name,url,'livecatslist',thumb,'',thumb)                        
        main.AUTO_VIEW('movies')        
   except Exception:
        buggalo.onExceptionRaised()


        
def LIVECATSLIST(url):
   try:        
        mainurl=url
        link=OPEN_URL(url).replace('\n','').replace('\r','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                #addDir(name,url,mode,thumb,desc,thumb)                        
                addSTFavDir(name,url,mode,thumb,'','',isFolder=False, isPlayable=True)
        link=OPEN_URL(mainurl).replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
        for name,url,thumb in match:
                #addDir(name,url,'liveresolve',thumb,'',thumb)       
                addSTFavDir(name,url,'liveresolve',thumb,'','',isFolder=False, isPlayable=True)

        main.AUTO_VIEW('movies')   
   except Exception:
        buggalo.onExceptionRaised()


def ILIVERESOLVE(name,url,iconimage):
         liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
 
         liz.setInfo( type="Video", infoLabels={ "Title": name} )
         liz.setPath(url)

         xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
         


def LIVERESOLVE(name,url,thumb):
         params = {'url':url, 'name':name, 'thumb':thumb}
         addon.add_video_item(params, {'title':name}, img=thumb)
         liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
         #xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)
         

  

def addDir(name,url,mode,thumb,desc,favtype):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/showgunart/images/fanart/fanart.jpg'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


        
#==============================Attempt to scrape Ilive.to==============================================================

def ILIVEMAIN():
   try:        
        addDir('All(English)','allenglish','ilivelists',artwork+'/ilive.png','All English Streams available from iLive','')
        addDir('All','all','ilivelists',artwork+'/ilive.png','All English Streams available from iLive','')
        addDir('Animation','animation','ilivelists',artwork+'/ilive.png','Animation Stream Listings','')
        addDir('Entertainment(English)','entertainmentenglish','ilivelists',artwork+'/ilive.png','English Entertainment Streams from iLive','')
        addDir('Entertainment','entertainment','ilivelists',artwork+'/ilive.png','All Entertainment Streams from iLive','')
        addDir('General','general','ilivelists',artwork+'/ilive.png','General Streams','')
        addDir('Movies','movies','ilivelists',artwork+'/ilive.png','Movie Streams from iLive','')
        addDir('Music','music','ilivelists',artwork+'/ilive.png','Current Listed Music Streams','')
        addDir('News','news','ilivelists',artwork+'/ilive.png','Current News Streams','')
        addDir('Sports(English)','sportsenglish','ilivelists',artwork+'/ilive.png','Live English Sports Streams from iLive','')
        addDir('Sports','sports','ilivelists',artwork+'/ilive.png','Live Sports Streams from iLive','')
        link=OPEN_URL('https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/streams/ilivemenu.xml').replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)
#Start Tester Phase===========================================
        '''link=OPEN_URL('http://addonrepo.com/tester.xml').replace('\n','').replace('\r','')
        match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode><desc>(.+?)</desc>').findall(link)
        for name,url,thumb,mode,desc in match:
                print 'Description is  ' + desc
                addDir(name,url,mode,thumb,desc,thumb)'''
#END Tester Phase===============================================                
        main.AUTO_VIEW('movies')
   except Exception:
        buggalo.onExceptionRaised()
        
def ILIVELISTS(menuurl):
   try:
        if menuurl=='movies':
                try: urllist=['http://www.ilive.to/channels/Movies?sort=1','http://www.ilive.to/channels/Movies?p=2','http://www.ilive.to/channels/Movies?p=3','http://www.ilive.to/channels/Movies?p=4','http://www.ilive.to/channels/Movies?p=5','http://www.ilive.to/channels/Movies?p=6','http://www.ilive.to/channels/Movies?p=7']
                except: urllist=['http://www.ilive.to/channels/Movies']  
                  
        if menuurl=='general':
                try: urllist=['http://www.ilive.to/channels/General','http://www.ilive.to/channels/General?p=2']
                except: urllist=['http://www.ilive.to/channels/General']
        if menuurl=='entertainment':
                try: urllist=['http://www.ilive.to/channels/Entertainment','http://www.ilive.to/channels/Entertainment?p=2','http://www.ilive.to/channels/Entertainment?p=3','http://www.ilive.to/channels/Entertainment?p=4','http://www.ilive.to/channels/Entertainment?p=5','http://www.ilive.to/channels/Entertainment?p=6']
                except: urllist=['http://www.ilive.to/channels/Entertainment','http://www.ilive.to/channels/Entertainment?p=2','http://www.ilive.to/channels/Entertainment?p=3','http://www.ilive.to/channels/Entertainment?p=4','http://www.ilive.to/channels/Entertainment?p=5']
        if menuurl=='sports':
                try: urllist=['http://www.ilive.to/channels/Sport','http://www.ilive.to/channels/Sport?p=2','http://www.ilive.to/channels/Sport?p=3','http://www.ilive.to/channels/Sport?p=4']
                except: urllist=['http://www.ilive.to/channels/Sport','http://www.ilive.to/channels/Sport?p=2','http://www.ilive.to/channels/Sport?p=3']
        if menuurl=='news':
                try: urllist=['http://www.ilive.to/channels/News']
                except: urllist=['http://www.ilive.to/channels/News']
        if menuurl=='music':
                try: urllist=['http://www.ilive.to/channels/Music']
                except: urllist=['http://www.ilive.to/channels/Music']
        if menuurl=='animation':
                try: urllist=['http://www.ilive.to/channels/Animation','http://www.ilive.to/channels/Animation?p=2']
                except: urllist=['http://www.ilive.to/channels/Animation']
        if menuurl=='family':
                try: urllist=['http://www.ilive.to/channels/Family']
                except: urllist=['http://www.ilive.to/channels/Family']
        if menuurl=='lifecaster':
                try: urllist=['http://www.ilive.to/channels/Lifecaster']
                except: urllist=['http://www.ilive.to/channels/Lifecaster']
        if menuurl=='gaming':
                try: urllist=['http://www.ilive.to/channels/Gaming']
                except: urllist=['http://www.ilive.to/channels/Gaming']
        if menuurl=='mobile':
                try: urllist=['http://www.ilive.to/channels/Mobile']
                except: urllist=['http://www.ilive.to/channels/Mobile']
        if menuurl=='religion':
                try: urllist=['http://www.ilive.to/channels/Religion']
                except: urllist=['http://www.ilive.to/channels/Religion']
        if menuurl=='radio':
                try: urllist=['http://www.ilive.to/channels/Radio']
                except: urllist=['http://www.ilive.to/channels/Radio']
        if menuurl=='all':
                try: urllist=['http://www.ilive.to/channels','http://www.ilive.to/channels?p=2','http://www.ilive.to/channels?p=3','http://www.ilive.to/channels?p=4','http://www.ilive.to/channels?p=5','http://www.ilive.to/channels?p=6','http://www.ilive.to/channels?p=7','http://www.ilive.to/channels?p=8','http://www.ilive.to/channels?p=9','http://www.ilive.to/channels?p=10','http://www.ilive.to/channels?p=11','http://www.ilive.to/channels?p=12','http://www.ilive.to/channels?p=13','http://www.ilive.to/channels?p=14','http://www.ilive.to/channels?p=15','http://www.ilive.to/channels?p=16']
                except: urllist=['http://www.ilive.to/channels','http://www.ilive.to/channels?p=2','http://www.ilive.to/channels?p=3','http://www.ilive.to/channels?p=4','http://www.ilive.to/channels?p=5','http://www.ilive.to/channels?p=6','http://www.ilive.to/channels?p=7','http://www.ilive.to/channels?p=8','http://www.ilive.to/channels?p=9','http://www.ilive.to/channels?p=10']
        if menuurl=='allenglish':
                try: urllist=['http://www.ilive.to/channels?lang=1','http://www.ilive.to/channels?lang=1&p=2','http://www.ilive.to/channels?lang=1&p=3','http://www.ilive.to/channels?lang=1&p=4','http://www.ilive.to/channels?lang=1&p=5','http://www.ilive.to/channels?lang=1&p=6','http://www.ilive.to/channels?lang=1&p=7','http://www.ilive.to/channels?lang=1&p=8','http://www.ilive.to/channels?lang=1&p=9','http://www.ilive.to/channels?lang=1&p=10']
                except: urllist=['http://www.ilive.to/channels?lang=1','http://www.ilive.to/channels?lang=1&p=2','http://www.ilive.to/channels?lang=1&p=3','http://www.ilive.to/channels?lang=1&p=4','http://www.ilive.to/channels?lang=1&p=5','http://www.ilive.to/channels?lang=1&p=6','http://www.ilive.to/channels?lang=1&p=7','http://www.ilive.to/channels?lang=1&p=8','http://www.ilive.to/channels?lang=1&p=9']
        if menuurl=='entertainmentenglish':
                try: urllist=['http://www.ilive.to/channels/Entertainment?lang=1','http://www.ilive.to/channels/Entertainment?lang=1&p=2','http://www.ilive.to/channels/Entertainment?lang=1&p=3','http://www.ilive.to/channels/Entertainment?lang=1&p=4','http://www.ilive.to/channels/Entertainment?lang=1&p=5','http://www.ilive.to/channels/Entertainment?lang=1&p=6']
                except: urllist=['http://www.ilive.to/channels/Entertainment?lang=1','http://www.ilive.to/channels/Entertainment?lang=1&p=2','http://www.ilive.to/channels/Entertainment?lang=1&p=3','http://www.ilive.to/channels/Entertainment?lang=1&p=4','http://www.ilive.to/channels/Entertainment?lang=1&p=5']
        if menuurl=='sportsenglish':
                try: urllist=['http://www.ilive.to/channels/Sport?lang=1','http://www.ilive.to/channels/Sport?lang=1&p=2']
                except: urllist=['http://www.ilive.to/channels/Sport?lang=1']        
        if 'http' in menuurl:
                print 'MENUURL IS '+ menuurl
                urllist = [menuurl]

        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Loading Menu..Standby...')
        pages = len(urllist)
        gotpages = 0
        remaining_display = 'Pages  :: [B]'+str(gotpages)+' / '+str(pages)+'[/B].'
        dialogWait.update(0,'[COLOR gold][B]Loading.....[/B][/COLOR]',remaining_display)
        for durl in urllist:
                link=OPEN_URL(durl)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
                #Changed regex for main menu load 
                #match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?</noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                #match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?</noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                for thumb,url,name in match:
                        if settings.getSetting('adult') == 'true':
                                addSTFavDir(name,url,'iliveplaylink',thumb,'','',isFolder=False, isPlayable=True)
                                
                        else:        
                                if 'venus' not in name.lower() and '+16' not in name.lower() and '+18' not in name.lower() and 'hongkong' not in name.lower() and   'playboy' not in name.lower() and   'sex' not in name.lower() and   'girls' not in name.lower() and   'fuck' not in name.lower() and   'hardcore' not in name.lower() and   'softcore' not in name.lower() and   'pussy' not in name.lower() and   'dick' not in name.lower() and   'anal' not in name.lower() and   'cum' not in name.lower() and   'blowjob' not in name.lower() and   'adult' not in name.lower() and   '18+' not in name.lower() and  '16+' not in name.lower():
                                        addSTFavDir(name,url,'iliveplaylink',thumb,'','',isFolder=False, isPlayable=True)
                                        
                                      
                gotpages = gotpages + 1
                percent = (gotpages * 100)/gotpages
                remaining_display = 'Pages loaded :: [B]'+str(gotpages)+' / '+str(pages)+'[/B].'
                dialogWait.update(percent,'[COLOR gold][B]Loading.....[/B][/COLOR]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
   except Exception:
        buggalo.onExceptionRaised()        
         


def ILIVEPLAYLINKOLD(name,menuurl,thumb):
   try:        
                       
                link=OPEN_URL(menuurl)
                ok=True
                if link:
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.clear()
                                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
                                matchserv=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)
                                for server in matchserv:
                                        print 'Server IS ' +server
                                        headers = {'Referer': 'http://www.ilive.to/'}
                                        url = server
                                        html = net.http_GET(url, headers=headers).content
                                        match=re.compile('{"token":"(.+?)"}').findall(html)
                                        for token in match:
                                                print 'SERVERTOKEN IS  '+ token
                                                token = token

                                match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
                                for vid in match:
                                        pageUrl='http://www.ilive.to/m/channel.php?n='+vid
                                        playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
                                        playpath = playpath[0]
                                        newplaypath =str(playpath)        
                                        rtmp=re.compile('''streamer: "([^"]+?)"''').findall(link)
                                        app=rtmp[0].split('?xs=')
                                        #newrtmp = str(rtmp)
                                        #newrtmp = newrtmp.replace('\/','/').replace('\\','')        
                                        #newapp = str(app)
                                        link=OPEN_URL(pageUrl)
                                        swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
                                        for swf in swff:
                                                swf= swf
                                                #swf= swf[0]
                                                #Manual SWF Added
                                                #swf = 'http://www.ilive.to/player/player.swf'
                                                print 'SWF IS ' + swf
                                        playable =rtmp[0]+' app=edge/?xs='+app[1]+' playpath=' + newplaypath + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
                                        
                                        print 'RTMP IS ' +  playable
                                        ILIVERESOLVE(name,playable,thumb)
                                        
   except Exception:
        buggalo.onExceptionRaised()                                

def ILIVEPLAYLINK(name,menuurl,thumb):
   try:        
                mobileurl=menuurl.replace('http://www.ilive.to/view/','http://www.mobileonline.tv/channel.php?n=')        
                link=OPEN_URL(mobileurl)
                ok=True
                if link:
                     
                     match=re.compile('<a href=(.+?) target=".+?">Link 1').findall(link)
                     for playable in match:

     
                          ILIVERESOLVE(name,playable,thumb)
                                        
   except Exception:
        buggalo.onExceptionRaised()


def ILIVEPLAYLINKTEST(name,menuurl,thumb):
   try:               
                link=OPEN_URL(menuurl)
                ok=True
                if link:
                                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                                playlist.clear()
                                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
                                matchserv=re.compile('''.*getJSON\("([^'"]+)".*''').findall(link)
                                for server in matchserv:
                                        print 'Server IS ' +server
                                        headers = {'Referer': 'http://www.ilive.to/'}
                                        url = server
                                        html = net.http_GET(url, headers=headers).content
                                        match=re.compile('{"token":"(.+?)"}').findall(html)
                                        for token in match:
                                                print 'SERVERTOKEN IS  '+ token
                                                token = token

                                match=re.compile('http://www.ilive.to/embed/(.+?)&width=.+?&height=.+?&autoplay=true').findall(link)
                                for vid in match:
                                        pageUrl='http://www.ilive.to/m/channel.php?n='+vid
                                        playpath=re.compile('''.*file[:,]\s*['"]([^'"]+).flv['"]''').findall(link)
                                        playpath = playpath[0]
                                        newplaypath =str(playpath)        
                                        rtmp=re.compile('''streamer: "([^"]+?)"''').findall(link)
                                        app=rtmp[0].split('?xs=')
                                        #newrtmp = str(rtmp)
                                        #newrtmp = newrtmp.replace('\/','/').replace('\\','')        
                                        #newapp = str(app)
                                        link=OPEN_URL(pageUrl)
                                        swff=re.compile("type: \'flash\', src: \'(.+?)'").findall(link)
                                        for swf in swff:
                                                swf= swf
                                                #swf= swf[0]
                                                #Manual SWF Added
                                                #swf = 'http://www.ilive.to/player/player.swf'
                                                print 'SWF IS ' + swf
                                        playable =rtmp[0]+' app=edge/?xs='+app[1]+' playpath=' + newplaypath + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=http://www.ilive.to'
                                        
                                        print 'RTMP IS ' +  playable
                                        ILIVERESOLVE(name,playable,thumb)
                                        
   except Exception:
        buggalo.onExceptionRaised()                                
        
#Start Ketboard Function                
def _get_keyboard( default="", heading="", hidden=False ):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard( default, heading, hidden )
        keyboard.doModal()
        if ( keyboard.isConfirmed() ):
                return unicode( keyboard.getText(), "utf-8" )
        return default


#Start Search Function
def SEARCHILIVE(url):
        searchUrl = url 
        vq = _get_keyboard( heading="Searching for Streams" )
        if ( not vq ): return False, 0
        title = urllib.quote_plus(vq)
        searchUrl += title  
        print "Searching Streams: " + searchUrl 
        SEARCHLINKS(searchUrl)
             
               
def SEARCHLINKS(urllist):                 
   try:        
                link=OPEN_URL(urllist)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.*?)</strong></a><br/>').findall(link)
                if len(match) > 0:
                        for thumb,url,name in match:
                                addSTFavDir(name,url,'iliveplaylink',thumb,'','', isFolder=False, isPlayable=True)
                                  
                else:
                        addDir('[COLOR red]None Found Try again[/COLOR]','http://www.ilive.to/channels/?q=','searchilive','','','')
   except Exception:
        buggalo.onExceptionRaised()        


def PLAYFAVS(name,url,thumb):        
        queue = streamcache.get('queue')
        if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               name = item[0]
               url = item[1]
               thumb = item[2]
               print 'PLAY URL IS ' + url
               main.RESOLVE(name,url,thumb)
               
  



#====================Standard Favorites===================================
def addSTFavDir(name,url,mode,thumb,desc,favtype, isFolder=True, isPlayable=False):
        gomode=mode
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlspecial', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(thumb)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        #addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems,context_replace=False, img= thumb)
        if isPlayable:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok

def addSTRemoveDir(name,url,mode,thumb,gomode):
        gomode=mode
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'gomode': gomode}
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems,context_replace=False, img= thumb)            
     
def ADDSTTOFAVS(name,url,thumb,gomode):
   try:        
     queue = standardstreamcache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,gomode) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Favorites[/COLOR]', msg=name + ' Is Already In Your Favorite List', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb,gomode))         
     standardstreamcache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Favorites [/COLOR]', msg=name + ' Was Added To Your Favorite List', delay=int(5000), image=thumb)
   except Exception:
        buggalo.onExceptionRaised()
        
def VIEWSTFAVS():
   try:        
     addDir('[COLOR blue]Favorites[/COLOR]','none','viewstfavs',artwork +'playfavs.jpg','','')
     queue = standardstreamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addSTRemoveDir(item[0],item[1],item[3],item[2],'')
   except Exception:
        buggalo.onExceptionRaised()

def REMOVESTFROMFAVS(name,url,thumb,gomode):
     queue = standardstreamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          queue_items.remove((name,url,thumb,gomode))
          standardstreamcache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")
          
#====================END Standard Favorites===============================          


def RESOLVER(url,name):
   try:        
        dlfoldername = name                            
        urls = url
        hmf = urlresolver.HostedMediaFile(urls)
        if hmf:
                host = hmf.get_host()
                dlurl = urlresolver.resolve(urls)
                ILIVERESOLVE(name,dlurl,'')
                                  
   except Exception:
        buggalo.onExceptionRaised()

#=============Below to be used for future updates==============================================================================================================        
               
'''
def addFavDir(name,url,mode,thumb,desc,favtype):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        contextMenuItems.append(('[COLOR red]Add to Live Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addtofavs', 'name': name,'url': url,'thumb': thumb})))
        contextMenuItems.append(('[COLOR red]Remove From Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removefromfavs', 'name': name,'url': url,'thumb': thumb})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)

def addRemoveDir(name,url,mode,thumb,desc,favtype):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}

        contextMenuItems.append(('[COLOR red]Remove From Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removefromfavs', 'name': name,'url': url,'thumb': thumb})))
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'https://raw.githubusercontent.com/Blazetamer/commoncore/master/xbmchub/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)            
     
def ADDTOFAVS(name,url,thumb):
   try:        
     queue = streamcache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,ext,console) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Favorites[/COLOR]', msg=name + ' Is Already In Your Favorite List', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb))         
     streamcache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Favorites [/COLOR]', msg=name + ' Was Added To Your Favorite List', delay=int(5000), image=thumb)
   except Exception:
        buggalo.onExceptionRaised()
        
def VIEWFAVS():
   try:        
     addDir('[COLOR blue]iLive Favorites[/COLOR]','none','viewfavs',artwork +'playfavs.jpg','','')
     queue = streamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addRemoveDir(item[0],item[1],'iliveplaylink',item[2],'','')
   except Exception:
        buggalo.onExceptionRaised()

def REMOVEFROMFAVS(name,url,thumb):
     queue = streamcache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          queue_items.remove((name,url,thumb,))
          streamcache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")
'''
