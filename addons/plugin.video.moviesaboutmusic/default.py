'''
    MoviesAboutMusic.com Add-on
    Copyright (C) 2016 RayW1986

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime,string
import plugintools
import xbmcaddon
import urlresolver

ADDON = xbmcaddon.Addon(id='plugin.video.moviesaboutmusic')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.moviesaboutmusic'), '')

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviesaboutmusic', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviesaboutmusic/resources/art', ''))
main_url = 'http://moviesaboutmusic.com/?cat='

addon_id = xbmcaddon.Addon().getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)
enable_auto_view = selfAddon.getSetting('enable_auto_view')
view_mode_id = selfAddon.getSetting('view_mode_id')

def CATEGORIES():
        addDirMain('Documentaries',main_url+'69',1,art+'docs.png')
        addDirMain('Feature Films',main_url+'133',1,art+'films.png')
        addDirMain('Genres','http://moviesaboutmusic.com/',3,art+'genres.png')
        addDirMain('Decades','http://moviesaboutmusic.com/',4,art+'decades.png')
        addDirMain('Recently Added','http://moviesaboutmusic.com/blog/',1,art+'recent.png')
		
def	getVideos(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,'<div id="post(.*?)<i class=".+?">')
    nextpage = plugintools.find_multiple_matches(link,'"nextLink":"(.*?),')
    
    for entry in matches:
       
        title = plugintools.find_single_match(entry,'href=".+?" rel=".+?" title="(.+?)">').replace('&#8211;','-').replace("&#8217;","'").replace("&#8216;","'")
        ytID = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/(.+?)\?feature=')
        thumbnail = 'http://i.ytimg.com/vi/'+ytID+'/hqdefault.jpg'
        url = 'plugin://plugin.video.youtube/play/?video_id='+ytID
        fanart = 'http://i.ytimg.com/vi/'+ytID+'/hqdefault.jpg'
        plot = plugintools.find_single_match(entry,'<p>(.+?)</p>').replace('&#8211;','-').replace("&#8217;","'").replace("&#8216;","'").replace('&#8220;','"').replace('&#8221;','"')

        plugintools.add_item( action="play" , title=title , url=url , fanart=fanart , plot=plot , thumbnail=thumbnail , folder=True )
		
    for entry in nextpage:
       
        name = 'Next Page'
        iconimage = art+'nextpage.png'
        geturl = plugintools.find_single_match(entry,'http(.+?)"').replace('\/','/')
        url = 'http'+geturl

        addDirMain(name,url,1,iconimage)
		
    if enable_auto_view=='true':
        xbmc.executebuiltin('Container.SetViewMode(%d)' % int(view_mode_id))
    else:
        pass

def	getGenres(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,'<li id="nav-menu-item-17(.*?)</li>')
    
    for entry in matches:
       
        name = plugintools.find_single_match(entry,'sub-menu-link">(.+?)</a>')
        iconimage = art+'genres.png'
        url = plugintools.find_single_match(entry,'href="(.+?)"')

        addDirMain(name,url,1,iconimage)
        
def getDecades(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,'<li id="nav-menu-item-14(.*?)</li>')
    
    for entry in matches:
       
        name = plugintools.find_single_match(entry,'sub-menu-link">(.+?)</a>')
        iconimage = art+'genres.png'
        url = plugintools.find_single_match(entry,'href="(.+?)"')

        addDirMain(name,url,1,iconimage)
		
def play(name,url):
        if urlresolver.HostedMediaFile(url).valid_url():
            stream_url = urlresolver.HostedMediaFile(url).resolve()
            print stream_url
            if stream_url == False: return
        liz = xbmcgui.ListItem(name, path=stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    link=cleanHex(link)
    response.close()
    return link
	
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDirMain(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def addDir(name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        nameurl="%s|%s|%s" % (name,url,iconimage)
        if favourites_index(nameurl) < 0:
            contextMenuItems.append(('Add to My Promotions', 'XBMC.RunPlugin(%s?mode=103&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        else:
            name = name
            contextMenuItems.append(('Remove from My Promotions', 'XBMC.RunPlugin(%s?mode=104&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, True)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def addDirVideo(prefix,name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        nameurl="%s|%s" % (name,url)
        if watched_index(url) < 0:
            contextMenuItems.append(('Mark as Watched', 'XBMC.RunPlugin(%s?mode=101&url=%s)'% (sys.argv[0], url)))
        else:
            name = '[COLOR cyan]' + "<< " + '[/COLOR]' + name
            contextMenuItems.append(('Remove from Watched List', 'XBMC.RunPlugin(%s?mode=102&url=%s)'% (sys.argv[0], url)))
        if favourites_index(nameurl) < 0:
            contextMenuItems.append(('Save to Favourites', 'XBMC.RunPlugin(%s?mode=103&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        else:
            name = '[COLOR gold]' + "+  " + '[/COLOR]' + name
            contextMenuItems.append(('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=104&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, True)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
	
elif mode==1:
        print ""+url
        getVideos(url)
        
elif mode==2:
        play(name,url)
		
elif mode==3:
        getGenres(url)
		
elif mode==4:
        getDecades(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
