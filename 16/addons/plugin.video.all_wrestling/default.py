'''
    All Wrestling Add-on
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
import liveresolver

ADDON = xbmcaddon.Addon(id='plugin.video.all_wrestling')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.all_wrestling'), '')

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.all_wrestling', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.all_wrestling/resources/art', ''))
main_url = 'http://www.allwrestling.net/category/'
art_url = 'http://www.allwrestling.net/wp-content/uploads/'

def CATEGORIES():
        addDirMain('WWE','url',4,art+'wwe.png')
        addDirMain('TNA','url',5,art+'tna.png')
        addDirMain('ROH',main_url+'ring-of-honor/',1,art_url+'2015/06/ROH-Wrestling-R-ing-of-Honor.jpg')
        addDirMain('Lucha Underground',main_url+'lucha-underground/',1,art_url+'2015/06/lucha-underground.png')
        addDirMain('NJPW',main_url+'njpw/',1,art_url+'2015/06/NJPW-New-Japan-Pro-Wrestling.jpg')
        addDirMain('UFC',main_url+'ufc/',1,art+'ufc.png')
        addDirMain('Search','url',6,art+'wwe.png')
		
def getWWE():
        addDirMain('Latest Shows',main_url+'wwe/',1,art+'wwe.png')
        addDirMain('WWE Pay-Per-Views',main_url+'wwe/wwe-ppv/',1,art+'wwe.png')
        addDirMain('WWE Raw',main_url+'wwe/raw/',1,art_url+'2015/06/Raw-640x360.png')
        addDirMain('WWE SmackDown!',main_url+'wwe/wwe-smackdown/',1,art_url+'2015/12/WWE-Thursday-Night-SmackDown-640x350.jpg')
        addDirMain('WWE Main Event',main_url+'wwe/main-event/',1,art_url+'2015/06/WWE-Main-Event-640x360.jpg')
        addDirMain('WWE Superstars',main_url+'wwe/superstars/',1,art_url+'2015/06/wwe-superstars-640x357.jpg')
        addDirMain('WWE NXT',main_url+'wwe/wwe-nxt/',1,art_url+'2015/06/WWE-NXT1-640x357.jpg')
        addDirMain('WWE Network','url',7,art+'wwe.png')
        addDirMain('Total Divas',main_url+'wwe/tota-divas/',1,art_url+'2016/01/total-divas-season-5-640x360.jpg')
		
def getTNA():
        addDirMain('Latest Shows',main_url+'tna/',1,art+'tna.png')
        addDirMain('TNA Pay-Per-Views',main_url+'tna/tna-ppv/',1,art+'tna.png')
        addDirMain('TNA Impact',main_url+'tna/tna-impact/',1,art_url+'2015/06/impactwrestling.png')
		
def getWWENetwork():
        addDirMain('Watch LIVE!','url',9,'iconimage')
        addDirMain('All WWE Network Shows',main_url+'wwe/wwe-network/',1,art+'wwe.png')
        addDirMain('WWE 24',main_url+'wwe/wwe-network/wwe-24/',1,art+'wwe.png')
        addDirMain('WWE Breaking Ground',main_url+'wwe/breaking-ground/',1,art+'wwe.png')
        addDirMain('WWE Ride Along',main_url+'wwe/wwe-network/ridealong/',1,art+'wwe.png')
        addDirMain('Unflitered With Renee Young',main_url+'wwe/wwe-network/wweunfiltered/',1,art+'wwe.png')
        addDirMain('WWE Swerved',main_url+'wwe/wwe-network/swerved/',1,art+'wwe.png')
        addDirMain('This Week in WWE',main_url+'wwe/wwe-network/this-week-in-wwe/',1,art+'wwe.png')
		
def getWWENetworkLive():
		addLink('Link 1 | HDFree.tv','http://hdfree.tv/wwe-network-live-stream.html',8,'iconimage')
		addLink('Link 2 | Shadow-Net.org','http://www.shadow-net.org/channels/WWE-Network.html',8,'iconimage')
		addLink('Link 3 | CricHD.co','http://www.crichd.co/wwe-network.php',8,'iconimage')
		
def search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = 'http://www.allwrestling.net/?s='+search
                getShows(url)
		
def	getShows(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,'<div id="post(.*?)</div>')
    nextpage = plugintools.find_multiple_matches(link,'<link rel="next" (.*?)/>')
    
    for entry in matches:
       
        name = plugintools.find_single_match(entry,'title="(.+?)"').replace('Watch ','').replace(' Online Free','').replace(' Full Show','').replace('&#8211;','-').replace(' Livestream','').replace('SmackDown ','SmackDown! ')
        iconimage = plugintools.find_single_match(entry,'<img src="(.+?)"')
        url = plugintools.find_single_match(entry,'href="(.+?)"')

        addDirMain(name,url,2,iconimage)
		
    for entry in nextpage:
       
        name = 'Next Page'
        iconimage = art+'nextpage.png'
        url = plugintools.find_single_match(entry,'href="(.+?)"')

        addDirMain(name,url,1,iconimage)
        
def getSource(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    wwetalks = plugintools.find_multiple_matches(link,'<a href=".+?talk.+?.php?(.*?)a>')
    vidgg = plugintools.find_multiple_matches(link,'<a href=".+?vid.gg(.*?)a>')
    letwatch = plugintools.find_multiple_matches(link,'<a href=".+?letwatch.us(.*?)a>')
    hugefiles = plugintools.find_multiple_matches(link,'<a href=".+?hugefiles.net(.*?)a>')
    dmembed = plugintools.find_multiple_matches(link,'<div class="screen fluid(.*?)v>')
    
    for entry in wwetalks:
       
        source = plugintools.find_single_match(entry,'wid(.+?)=').replace('=1&amp;id','DAILYMOTION').replace('=3&amp;id','NOWVIDEO').replace('=4&amp;id','NOVAMOV').replace('=5&amp;id','MOVSHARE').replace('=6&amp;id','CLOUDY').replace('=7&amp;id','VODLOCKER').replace('=8&amp;id','YOUWATCH').replace('=9&amp;id','VIDTO').replace('=11&amp;id','BESTREAMS').replace('=10&amp;id','OPENLOAD')
		
        part = plugintools.find_single_match(entry,'class="small cool-blue vision-button" target="_blank">(.+?)</').replace(' F','F').replace(' P','P')
		
        get_url = plugintools.find_single_match(entry,'wid(.+?)=').replace('=1&amp;id','http://www.dailymotion.com/video/').replace('=3&amp;id','http://www.nowvideo.sx/video/').replace('=4&amp;id','http://www.auroravid.to/video/').replace('=5&amp;id','http://www.wholecloud.net/video/').replace('=6&amp;id','http://www.cloudy.ec/v/').replace('=7&amp;id','http://vodlocker.com/').replace('=8&amp;id','http://youwatch.org/').replace('=9&amp;id','http://www.vidto.me/').replace('=11&amp;id','http://www.bestreams.net/')
		
        get_urlid = plugintools.find_single_match(entry,'wid=.+?id=(.+?)" class')
		
        name = '[B]'+source+'[/B] | '+part
		
        url = get_url+get_urlid
		
        iconimage = art+'play.png'
        
        addLink(name,url,3,iconimage)
		
    for entry in vidgg:
       
        source = 'VID.GG'
        part = plugintools.find_single_match(entry,'class="small cool-blue vision-button" target="_blank">(.+?)</').replace(' F','F').replace(' P','P')
        url = plugintools.find_single_match(entry,"'send', 'event', 'outbound-article', '(.+?)'")
        name = '[B]'+source+'[/B] | '+part
        iconimage = art+'play.png'
        
        addLink(name,url,3,iconimage)
		
    for entry in letwatch:
       
        source = 'LETWATCH'
        part = plugintools.find_single_match(entry,'class="small cool-blue vision-button" target="_blank">(.+?)</').replace(' F','F').replace(' P','P')
        url = plugintools.find_single_match(entry,"'send', 'event', 'outbound-article', '(.+?)'")
        name = '[B]'+source+'[/B] | '+part
        iconimage = art+'play.png'
        
        addLink(name,url,3,iconimage)
		
    for entry in hugefiles:
       
        source = 'HUGEFILES'
        part = plugintools.find_single_match(entry,'class="small cool-blue vision-button" target="_blank">(.+?)</').replace(' F','F').replace(' P','P')
        url = plugintools.find_single_match(entry,"'send', 'event', 'outbound-article', '(.+?)'").replace('download','en/mirrior')
        name = '[B]'+source+'[/B] | '+part
        iconimage = art+'play.png'
        
        addLink(name,url,3,iconimage)
		
    for entry in dmembed:
       
        source = 'DAILYMOTION'
        part = 'Full Show'
        url = plugintools.find_single_match(entry,"daily(.+?)</").replace(' ','').replace('motion','http://dailymotion')
        name = '[B]'+source+'[/B] | '+part
        iconimage = art+'play.png'
        
        addLink(name,url,3,iconimage)
		
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
	
def play_live(url):
	resolved = liveresolver.resolve(url)
	item = xbmcgui.ListItem(path=resolved)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        
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
        getShows(url)
        
elif mode==2:
        print ""+url
        getSource(url)
        
elif mode==3:
        play(name,url)
		
elif mode==4:
        getWWE()
		
elif mode==5:
        getTNA()
		
elif mode==6:
        search()
		
elif mode==7:
        getWWENetwork()
		
elif mode==8:
        play_live(url)
		
elif mode==9:
        getWWENetworkLive()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
