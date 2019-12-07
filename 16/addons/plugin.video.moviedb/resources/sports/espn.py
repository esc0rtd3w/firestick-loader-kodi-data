# ESPN Module --Blazetamer 2014===Thanks to  Annon for the partial regex code tips !!

import urllib,urllib2,re,cookielib,string, urlparse,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from resources.modules import main, live    
from addon.common.addon import Addon
from addon.common.net import Net
net = Net(http_debug=True)
        
addon_id = 'plugin.video.moviedb'
addon = main.addon
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
settings = xbmcaddon.Addon(id='plugin.video.moviedb')
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

    
def ESPNMAIN():
        live.addDir('NFL','2459789','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('NBA','2459788','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('WNBA','3414465','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('NCAA Basketball','2459792','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('NCAA Football','2564308','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('SOCCER','2731137','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('TENNIS','2491545','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('MLB','2521705','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('MMA','2881270','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('BOXING','2491554','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('NHL','2459791','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('GOLF','2630020','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('NASCAR','2492290','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('RACING','2755879','espnlist',artwork+'/espn.png','',fanart)
        live.addDir('OUTDOORS','2872804','espnlist',artwork+'/espn.png','',fanart)

def ESPNLIST(murl):
        
        if 'http://espn.go.com/video/' in murl:
                lurl=murl
                xurl=re.findall('(.+?)&pageNum=',murl)[0]
        else:
                lurl='http://espn.go.com/video/format/libraryPlaylist?categoryid='+murl
                xurl='http://espn.go.com/video/format/libraryPlaylist?categoryid='+murl
        link=main.OPEN_URL(lurl)
        match=re.compile('<a href="([^<]+)"><img src="(.+?)".+?></a><h5>(.+?)</h5>',re.DOTALL).findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Sports list is loaded.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Clips loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Loading Lists..[/B]',remaining_display)
        for url,thumb,name in match:
                live.addSTFavDir(name,url,'espnlink',thumb,'',fanart,isFolder=False, isPlayable=True)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Clips loaded :: '+str(loadedLinks)+' / '+str(totalLinks)+'.'
                dialogWait.update(percent,'Loading Lists..',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        match=re.compile('class="page-numbers">(\d+) of (\d+)</div>',re.DOTALL).findall(link)
        for p1,p2 in match:
                continue
        if p1 != p2:
                purl=xurl+ "&pageNum=" + str(int(p1)) + "&sortBy=&assetURL=http://assets.espn.go.com&module=LibraryPlaylist&pagename=vhub_index"
                live.addDir('Next Page '+p1+' of '+p2,purl,'espnlist',artwork+'/next.png','',fanart)
        

def ESPNLINK(name,url,thumb):
        ok=True
        link=main.OPEN_URL(url)
        match=re.compile('"thumbnailURL": "http://a.espncdn.com/combiner/i.?img=/media/motion(.+?).jpg',re.DOTALL).findall(link)[0]
        print match
        playpath = match + "_" + ADDON.getSetting("espn-quality") + ".mp4"
        playable = 'rtmp://svod.espn.go.com/motion'+playpath
        live.LIVERESOLVE(name,playable,thumb)
       
