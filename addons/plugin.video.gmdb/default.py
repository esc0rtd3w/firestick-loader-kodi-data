'''
    Game Movie Database Add-on
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

ADDON = xbmcaddon.Addon(id='plugin.video.gmdb')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.gmdb'), '')

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.gmdb', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.gmdb/resources/art', ''))
baseurl = 'http://www.gmdb.tv/'
genreurl = 'http://www.gmdb.tv/search/label/'

def CATEGORIES():
        addDirMain('Featured',baseurl,1,art+'featured.png')
        addDirMain('Film Genre','url',5,art+'film.png')
        addDirMain('Game Genre','url',6,art+'game.png')
        addDirMain('A-Z','url',7,art+'az.png')
        addDirMain('Search','url',4,art+'search.png')
		
def getFilm():
        addDirMain('Action',genreurl+'Action%20%28Film%29',1,art+'action.png')
        addDirMain('Adventure',genreurl+'Adventure%20%28Film%29',1,art+'adventure.png')
        addDirMain('Animation',genreurl+'Animation',1,art+'animation.png')
        addDirMain('Comedy',genreurl+'Comedy',1,art+'comedy.png')
        addDirMain('Crime',genreurl+'Crime',1,art+'crime.png')
        addDirMain('Drama',genreurl+'Drama',1,art+'drama.png')
        addDirMain('Family & Kids',genreurl+'Family%20%2F%20Kids',1,art+'family.png')
        addDirMain('Fantasy',genreurl+'Fantasy',1,art+'fantasy.png')
        addDirMain('Horror',genreurl+'Horror',1,art+'horror.png')
        addDirMain('Mystery',genreurl+'Mystery',1,art+'mystery.png')
        addDirMain('Romance',genreurl+'Romance',1,art+'romance.png')
        addDirMain('Sci-Fi',genreurl+'Sci-Fi',1,art+'scifi.png')
        addDirMain('Sports',genreurl+'Sports%20%28Film%29',1,art+'sports.png')
        addDirMain('Thriller',genreurl+'Thriller',1,art+'thriller.png')
        addDirMain('War',genreurl+'War',1,art+'war.png')
        addDirMain('Western',genreurl+'Western',1,art+'western.png')
		
def getGame():
        addDirMain('Action',genreurl+'Action%20%28Game%29',1,art+'action.png')
        addDirMain('Action Adventure',genreurl+'Action%20Adventure',1,art+'actionadventure.png')
        addDirMain('Action RPG',genreurl+'Action%20RPG',1,art+'actionrpg.png')
        addDirMain('Adventure',genreurl+'Adventure%20%28Game%29',1,art+'adventure.png')
        addDirMain('Fighting',genreurl+'Fighting',1,art+'fighting.png')
        addDirMain('Platformer',genreurl+'Platformer',1,art+'platformer.png')
        addDirMain('Puzzle',genreurl+'Puzzle',1,art+'puzzle.png')
        addDirMain('Racing',genreurl+'Racing',1,art+'racing.png')
        addDirMain('RPG',genreurl+'RPG',1,art+'rpg.png')
        addDirMain('Shooter',genreurl+'Shooter',1,art+'shooter.png')
        addDirMain('Sports',genreurl+'Sports%20%28Game%29',1,art+'sports.png')
        addDirMain('Strategy',genreurl+'Strategy',1,art+'stratgey.png')
        addDirMain('Survival Horror',genreurl+'Survival%20Horror',1,art+'survivalhorror.png')
        addDirMain('Visual Novel',genreurl+'Visual%20Novel',1,art+'visualnovel.png')
		
def getAZ():
        addDirMain('A',genreurl+'A',1,art+'a.png')
        addDirMain('B',genreurl+'B',1,art+'b.png')
        addDirMain('C',genreurl+'C',1,art+'c.png')
        addDirMain('D',genreurl+'D',1,art+'d.png')
        addDirMain('E',genreurl+'E',1,art+'e.png')
        addDirMain('F',genreurl+'F',1,art+'f.png')
        addDirMain('G',genreurl+'G',1,art+'g.png')
        addDirMain('H',genreurl+'H',1,art+'h.png')
        addDirMain('I',genreurl+'I',1,art+'i.png')
        addDirMain('J',genreurl+'J',1,art+'j.png')
        addDirMain('K',genreurl+'K',1,art+'k.png')
        addDirMain('L',genreurl+'L',1,art+'l.png')
        addDirMain('M',genreurl+'M',1,art+'m.png')
        addDirMain('N',genreurl+'N',1,art+'n.png')
        addDirMain('O',genreurl+'O',1,art+'o.png')
        addDirMain('P',genreurl+'P',1,art+'p.png')
        addDirMain('Q',genreurl+'Q',1,art+'q.png')
        addDirMain('R',genreurl+'R',1,art+'r.png')
        addDirMain('S',genreurl+'S',1,art+'s.png')
        addDirMain('T',genreurl+'T',1,art+'t.png')
        addDirMain('U',genreurl+'U',1,art+'u.png')
        addDirMain('V',genreurl+'V',1,art+'v.png')
        addDirMain('W',genreurl+'W',1,art+'w.png')
        addDirMain('X',genreurl+'X',1,art+'x.png')
        addDirMain('Y',genreurl+'Y',1,art+'y.png')
        addDirMain('Z',genreurl+'Z',1,art+'z.png')
		
def	getMovies(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,"<h3 class='post-title entry-title'>(.*?)--</div>")
    nextpage = plugintools.find_multiple_matches(link,"<a class='blog-pager-older-link'(.*?)title='Older Posts'>")
    
    for entry in matches:
       
        name = plugintools.find_single_match(entry,".html'>(.+?)</a")
        iconimage = plugintools.find_single_match(entry,'src="(.+?)" style=')
        url = plugintools.find_single_match(entry,"<a href='(.+?)'>")

        addDirMain(name,url,3,iconimage)
		
    for entry in nextpage:
       
        name = 'Next Page'
        iconimage = art+'nextpage.png'
        url = plugintools.find_single_match(entry,"href='(.+?)'")

        addDirMain(name,url,1,iconimage)
		
def	getStreams(url):
    find_url=url.find('?')
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    h2 = plugintools.find_multiple_matches(link,"<h2>\n(.+?)</iframe>")
    h3 = plugintools.find_multiple_matches(link,"<h3>\n(.*?)</iframe>")
    
    for entry in h2:
       
        name = plugintools.find_single_match(entry,".html'>(.+?)</a")
        title = plugintools.find_single_match(entry,"(.+?)</h2>").replace('\n','')
        ytID = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed(.+?)rel=').replace('/','video_id=').replace('?','')
        ytID2 = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/(.+?)rel=').replace('?','')
        ytID3 = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/(.+?)list=').replace('?','')
        plID = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/.+?is(.+?)width').replace('t=','playlist_id=').replace('" ','&order=default')
        url = 'plugin://plugin.video.youtube/play/?'+ytID+plID
        thumbnail = 'http://i.ytimg.com/vi/'+ytID2+ytID3+'/hqdefault.jpg'

        plugintools.add_item( action="play" , title=title , url=url , fanart=fanart , thumbnail=thumbnail , folder=True )
		
    for entry in h3:
       
        title = plugintools.find_single_match(entry,"(.+?)</h3>").replace('\n','').replace('</h3><h3>','')
        ytID = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed(.+?)rel=').replace('/','video_id=').replace('?','')
        ytID2 = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/(.+?)rel=').replace('?','')
        ytID3 = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/(.+?)list=').replace('?','')
        plID = plugintools.find_single_match(entry,'src="https://www.youtube.com/embed/.+?is(.+?)width').replace('t=','playlist_id=').replace('" ','&order=default')
        url = 'plugin://plugin.video.youtube/play/?'+ytID+plID
        thumbnail = 'http://i.ytimg.com/vi/'+ytID2+ytID3+'/hqdefault.jpg'

        plugintools.add_item( action="play" , title=title , url=url , fanart=fanart , thumbnail=thumbnail , folder=True )
		
def search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'search/?q='+search
                getMovies(url)
		
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
        getMovies(url)
        
elif mode==2:
        play(name,url)
		
elif mode==3:
        print ""+url
        getStreams(url)
		
elif mode==4:
        search()
		
elif mode==5:
        getFilm()
		
elif mode==6:
        getGame()
		
elif mode==7:
        getAZ()
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
