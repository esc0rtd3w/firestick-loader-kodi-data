
#  Live Streams Module by: Blazetamer


import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main

from metahandler import metahandlers

import urlresolver
import live

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
regex = addon.queries.get('regex', '')
page = addon.queries.get('page', '')
stream = addon.queries.get('stream', '')
key = addon.queries.get('key', '')


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


def NINETOOLS():
     live.addDir('URL Tester' ,'none','addfile','','Test your playable url','')
     #live.addDir('Developer Testing Tester' ,'none ','ninelists','','Dev Testing Mode','')
     #live.addDir('User Playlists From WEB' ,'none','userdatabase','','','')
     live.addDir('Playlist Tester' ,'none','addplaylist','','Test your Playlist','')
     live.addDir('[COLOR gold]Whats My IP[/COLOR]','none','myip',artwork +'myip.png','','dir')
     main.AUTO_VIEW('movies')

     
def NINEINDEX():       
     live.addDir('External Stream File' ,'none','ninemain','','Your Own Custom Playlist','')
     live.addDir('Local Stream File' ,'none','ninemainlocal','','Your Own Local Playlist','')               
     main.AUTO_VIEW('movies')
          

def DATABASE(url):

     link=OPEN_URL(url).replace('\n','').replace('\r','')        
     match=re.compile('<name>(.+?)</name><link>(.+?)</link>').findall(link)
     for name,url in match:
          live.addDir(name,url,'ninelists','','','')
          
def USERDATABASE():
     #-------------Start Type Fetch------------------------------------
     link=OPEN_URL('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/streams/usersubmitted/subtypemenu.xml').replace('\n','').replace('\r','')        
     match=re.compile('<title>(.+?)</title><thumbnail>(.+?)</thumbnail><typekey>(.+?)</typekey>').findall(link)
     for name,thumb,url in match:
          addDBDir(name,url,'playlistdata',thumb,'','')
     #--------------End Fetch-------------------------------------------      
     #live.addDir('Standard Playlists','none','standarddbtypes','','','')
     #live.addDir('Box Sets','none','boxdbtypes','','','')
     #live.addDir('Author Sets','none','authordbtypes','','','')

     
def PLAYLISTDATA(url):
     print 'KEYTYPE IS '+ url
     key = url
     regex = '<name>(.+?)</name><link>(.+?)</link><type>(.+?)</type>'
     if 'new' in key:
          link=OPEN_URL('http://cliqaddon.com/cliqpldbnewest.php').replace('\n','').replace('\r','')
          match=re.compile(regex).findall(link)
          for name,url,keytype in match:
               live.addDir(name,url,'ninelists','','','')

     if 'other' in key:
          link=OPEN_URL('http://cliqaddon.com/cliqpldbother.php').replace('\n','').replace('\r','')
          match=re.compile(regex).findall(link)
          for name,url,keytype in match:
               live.addDir(name,url,'ninelists','','','')          
     else:     
          print 'REGEX IS '+ regex
          link=OPEN_URL('http://cliqaddon.com/cliqpldb.php').replace('\n','').replace('\r','')
          #link=OPEN_URL('cliqaddon.com/cliqpldbtest.php').replace('\n','').replace('\r','')
          
          match=re.compile(regex).findall(link)
          for name,url,keytype in match:
               if key in keytype:
                    live.addDir(name,url,'ninelists','','','')

               


          
'''def STANDARDDBTYPES():

     link=OPEN_URL('http://goo.gl/dR7emd').replace('\n','').replace('\r','')        
     match=re.compile('<name>(.+?)</name><link>(.+?)</link><type>(.+?)</type>').findall(link)
     for name,url,kind in match:
          if 'standard' in kind:
               live.addDir(name,url,'ninelists','','','')

def BOXDBTYPES():

     link=OPEN_URL('http://goo.gl/dR7emd').replace('\n','').replace('\r','')        
     match=re.compile('<name>(.+?)</name><link>(.+?)</link><type>(.+?)</type>').findall(link)
     for name,url,kind in match:
          if 'boxset' in kind:
               live.addDir(name,url,'ninelists','','','')

def AUTHORDBTYPES():

     link=OPEN_URL('http://goo.gl/dR7emd').replace('\n','').replace('\r','')        
     match=re.compile('<name>(.+?)</name><link>(.+?)</link><type>(.+?)</type>').findall(link)
     for name,url,kind in match:
          if 'author' in kind:
               live.addDir(name,url,'ninelists','','','')  '''            

         

def addDBDir(name,url,mode,thumb,desc,key):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc, 'key':key}        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
  

def addDir(name,url,mode,thumb,key):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'page':page, 'key':key}        
        desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": desc } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


        
#==============================Attempt to scrape ==============================================================
#testurl ='http://cliqaddon.com/support/commoncore/tvaddons/moviedb/streams/ninestream.xml'
def NINEMAIN():
     customstream =settings.getSetting('custom_streams')
     customname =settings.getSetting('custom_name')
     if customname =='':
          customname= 'Custom Streams'
     if customstream =='':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Source Not Set', '               Please Choose Custom Tab and Add Source')
                if ok:
                        LogNotify('Choose Custom Tab ', 'Add Source & Name', '5000', 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png')        
                        print 'Source Not Set!'
                        addon.show_settings()
     else:     
          
        live.addDir(customname,customstream,'ninelists','','Your Own Custom Playlist','')
        
        main.AUTO_VIEW('movies')

def NINEMAINLOCAL():
     customstream =settings.getSetting('local_file')
     customname =settings.getSetting('local_custom_name')
     if customname =='':
          customname= 'Custom Local Stream'
     if customstream =='':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Source Not Set', '               Please Choose Custom Tab and Add Source')
                if ok:
                        LogNotify('Choose Custom Tab ', 'Add Local Source & Name', '5000', 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png')        
                        print 'Source Not Set!'
                        addon.show_settings()
     else:     
          
        live.addDir(customname,customstream,'ninelocallists','','Your Own Custom Playlist','')
        
        main.AUTO_VIEW('movies')                 
   
        
def NINELISTSOLD(url):

     link=OPEN_URL(url).replace('\n','').replace('\r','')
     #===============Info/Messages========================
     match=re.compile('<info>(.+?)</info>').findall(link)
     for name in match:
          live.addDir(name,'','ninelists','','','')
     match=re.compile('<name>(.+?)</name><thumbnail>(.+?)</thumbnail><link>(.+?)</link>').findall(link)
     for name,thumb,url in match:
          live.addDir(name,url,'ninelists',thumb,'',thumb)
     match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
     for name,url,thumb in match:
          live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)     
     match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(link)
     for name,url,thumb in match:
          live.addDir(name,url,'ninelists',thumb,'',thumb)
     if '<poster>schedule' in link:
          match=re.compile('<name>(.+?)</name>').findall(link)
          for name in match:
               live.addDir(name,'','ninelists','','','')

#=========================================================================               
def NINELISTS(url):

     #link=OPEN_URL(url).replace('\n','').replace('\r','')
     link=OPEN_URL(url)
               
     #===============Info/Messages========================
                    
     match=re.compile('<info>(.+?)</info>',re.DOTALL).findall(link)
     for name in match:
          live.addDir(name,'','ninelists','','','')
     #     
     match=re.compile('<name>(.+?)</name>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
     for name,url,thumb in match:
          live.addDir(name,url,'ninelists',thumb,'',thumb)
     #REMOVED BELOW FOR DOUBLE LISTING ERRORS #########################    
     #match=re.compile('<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<link>(.+?)</link>',re.DOTALL).findall(link)
     #for name,thumb,url in match:
          #live.addDir(name,url,'ninelists',thumb,'',thumb)
     ###END REMOVAL FOR DOUBLES########################################     
     match=re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
     for name,url,thumb in match:
          if 'sublink' in url:
               live.addDir(name,url,'sublinks',thumb,'',thumb)
          if 'sublink' not in url:     
               live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)

     if '<poster>schedule' in link:
          match=re.compile('<message>(.+?)</message>').findall(link)
          for name in match:
               live.addDir(name,'','ninelists','','','')          
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#NAVI EXTREME SCraper+++++++++++++++++++++++++++++++++++++++               
     match=re.compile('\nname=(.+?)\nthumb=(.+?)\nURL=(.+?)\n').findall(link)
     for name, thumb,url in match:
       if 'www.navixtreme.com' in url:
            live.addDir(name,url,'ninelists',thumb,'',thumb)
       if 'www.navixtreme.com' not in url:
            live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)

     
         


     match3=re.compile('\nname=(.+?)\n.+?URL=(.+?)\n').findall(link)
     for name,url in match3:
       if 'www.navixtreme.com' in url:
            thumb = ''
            live.addDir(name,url,'ninelists',thumb,'',thumb)
       if 'www.navixtreme.com' not in url:
            thumb = ''
            live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)  


     match4=re.compile('\nname=(.+?)\nthumb=(.+?)\n.+?\nURL=(.+?)\n').findall(link)
     for name, thumb,url in match4:
       if 'www.navixtreme.com' in url:
            live.addDir(name,url,'ninelists',thumb,'',thumb)
       if 'www.navixtreme.com' not in url:
            live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)
#++++++++++++++END NAVI SCRAPE++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                       

def SUBLINKS(url,name):
     name = name
     submatch=re.compile('<sublink>(.+?)</sublink>',re.DOTALL).findall(url)
     for sublink in submatch:
          print 'SUBLINK URLIS ' + sublink
          hmf = urlresolver.HostedMediaFile(sublink)
          if hmf:
               
               host = hmf.get_host()
               hostname = main.GETHOSTNAME(host)
               live.addSTFavDir(name+'[COLOR lime]'+hostname+'[/COLOR]',sublink,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)

          else:
               live.addSTFavDir(name+' [COLOR lime]Unknown Host[/COLOR]',sublink,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)
               
     
               
def PREVIOUSMENU(url):
     xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Input.Back", "id": 1 }')

def NINELOCALLISTS(url):
     file = open(url, 'r')
     file = file.read()
     file = str(file).replace('\n','').replace('\r','')
     print 'FILE CONTENT IS ' +file
     match=re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(file)
     for name,url,thumb in match:
          live.addSTFavDir(name,url,'nineresolver',thumb,'','',isFolder=False, isPlayable=True)               


def NINEPLAYLINK(name,url,thumb,stream):
     playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
     playlist.clear()
       
     playable = url
     print 'RTMP IS ' +  playable
     live.LIVERESOLVE(name,playable,thumb)
                                                              


        
def NINERESOLVER(url,name):
             
        dlfoldername = name                            
        urls = url
        hmf = urlresolver.HostedMediaFile(urls)
        if hmf:
                host = hmf.get_host()
                dlurl = urlresolver.resolve(urls)
                live.ILIVERESOLVE(name,dlurl,'')
        else:
                live.ILIVERESOLVE(name,urls,'')        
                                  
     



#Start Search Function
def _get_keyboard( default="", heading="", hidden=False ):
     keyboard = xbmc.Keyboard( default, heading, hidden )
     keyboard.doModal()
     if keyboard.isConfirmed() :
          return keyboard.getText()
     return default

                
def ADDFILE():
     vq = _get_keyboard( heading="Add your url" )
     if ( not vq ): return False, 0
     url = vq  
     print "Searching URL: " + url 
     #NINERESOLVER(url,'URL TESTER')
     live.addSTFavDir('Click to Try URL',url,'nineresolver','','','',isFolder=False, isPlayable=True)
     
def ADDPLAYLIST():
     vq = _get_keyboard( heading="Add your Playlist URL" )
     if ( not vq ): return False, 0
     url = vq  
     print "Playlist URL: " + url 
     live.addDir('Click to Try Playlist',url,'ninelists','','','')   
        
def URLTEST(url):
            
        name= 'URL TESTER'                           
        urls = url
        hmf = urlresolver.HostedMediaFile(urls)
        if hmf:
                host = hmf.get_host()
                dlurl = urlresolver.resolve(urls)
                live.ILIVERESOLVE(name,dlurl,'')
        else:
                live.ILIVERESOLVE(name,urls,'')        
                                  
    
