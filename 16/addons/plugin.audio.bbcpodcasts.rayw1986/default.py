"""
 Author: RayW1986

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
 
 """

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
import plugintools
import settings

DATA_PATH = settings.data_path()
ADDON = settings.addon()
WATCHED_FILE = settings.watched_videos_file()
FAVOURITES_FILE = settings.favourite_podcasts()

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.bbcpodcasts.rayw1986/resources/art', ''))
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.bbcpodcasts.rayw1986', 'fanart.jpg'))

def CATEGORIES():
		addDirMain('Categories','url',3,art+'cats.png')
		addDirMain('Stations','url',4,art+'stations.png')
		addDirMain('My Podcasts','url',5,art+'favs.png')
		
def cats():
		addDirMain('Childrens','http://www.bbc.co.uk/podcasts/genre/childrens',1,art+'childrens.png')
		addDirMain('Comedy','http://www.bbc.co.uk/podcasts/genre/comedy',1,art+'comedy.png')
		addDirMain('Drama','http://www.bbc.co.uk/podcasts/genre/drama',1,art+'drama.png')
		addDirMain('Entertainment','http://www.bbc.co.uk/podcasts/genre/entertainment',1,art+'ent.png')
		addDirMain('Factual','http://www.bbc.co.uk/podcasts/genre/factual',1,art+'factual.png')
		addDirMain('Learning','http://www.bbc.co.uk/podcasts/genre/learning',1,art+'learning.png')
		addDirMain('Music','http://www.bbc.co.uk/podcasts/genre/music',1,art+'music.png')
		addDirMain('News','http://www.bbc.co.uk/podcasts/genre/news',1,art+'news.png')
		addDirMain('Religion & Ethics','http://www.bbc.co.uk/podcasts/genre/religionandethics',1,art+'religion.png')
		addDirMain('Sport','http://www.bbc.co.uk/podcasts/genre/sport',1,art+'sport.png')
		
def stations():
		addDirMain('Radio 1','http://www.bbc.co.uk/podcasts/radio1',1,art+'radio1.png')
		addDirMain('Radio 1Xtra','http://www.bbc.co.uk/podcasts/1xtra',1,art+'radio1xtra.png')
		addDirMain('Radio 2','http://www.bbc.co.uk/podcasts/radio2',1,art+'radio2.png')
		addDirMain('Radio 3','http://www.bbc.co.uk/podcasts/radio3',1,art+'radio3.png')
		addDirMain('Radio 4','http://www.bbc.co.uk/podcasts/radio4',1,art+'radio4.png')
		addDirMain('Radio 4 Extra','http://www.bbc.co.uk/podcasts/radio4extra',1,art+'radio4extra.png')
		addDirMain('Radio 5 Live','http://www.bbc.co.uk/podcasts/5live',1,art+'5live.png')
		addDirMain('Radio 6 Music','http://www.bbc.co.uk/podcasts/6music',1,art+'6music.png')
		addDirMain('Asian Network','http://www.bbc.co.uk/podcasts/asiannetwork',1,art+'asiannetwork.png')
		addDirMain('World Service','http://www.bbc.co.uk/podcasts/worldserviceradio',1,art+'worldservice.png')
		addDirMain('Radio Scotland','http://www.bbc.co.uk/podcasts/radioscotland',1,art+'radioscotland.png')
		addDirMain('Radio Nan Gaidheal','http://www.bbc.co.uk/podcasts/radionangaidheal',1,art+'radionangaidheal.png')
		addDirMain('Radio Ulster','http://www.bbc.co.uk/podcasts/radioulster',1,art+'radioulster.png')
		addDirMain('Radio Foyle','http://www.bbc.co.uk/podcasts/radiofoyle',1,art+'radiofoyle.png')
		addDirMain('Radio Wales','http://www.bbc.co.uk/podcasts/radiowales',1,art+'radiowales.png')
		addDirMain('Radio Cymru','http://www.bbc.co.uk/podcasts/radiocymru',1,art+'radiocymru.png')
		addDirMain('BBC Radio','http://www.bbc.co.uk/podcasts/radio',1,art+'bbcradio.png')
		addDirMain('CBeebies','http://www.bbc.co.uk/podcasts/cbeebies',1,art+'cbeebies.png')
		addDirMain('School Radio','http://www.bbc.co.uk/podcasts/schoolradio',1,art+'schoolradio.png')
		
def my_podcasts():
    if os.path.isfile(FAVOURITES_FILE):
        s = read_from_file(FAVOURITES_FILE)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('|')
                name = list[0]
                url = list[1]
                iconimage = list[2]
                prefix = ''
                addDir(name,url,2,iconimage)	
		
def get_podcasts(url):
    find_url=url.find('?')+1
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,'<div class="pc-results-box">(.*?)</li>')
    
    for entry in matches:
        
        name = plugintools.find_single_match(entry,'alt="(.+?)"').replace("&amp;","&").replace('&quot;','"')
        iconimage = plugintools.find_single_match(entry,'<img src="(.+?)"')
        get_url = plugintools.find_single_match(entry,'<a href="http://www.bbc.co.uk/programmes/(.+?)/episodes/downloads">')
        url = 'http://www.bbc.co.uk/programmes/'+get_url+'/episodes/downloads'

        addDir(name,url,2,iconimage)
		
    pattern = ""
    next_page = plugintools.find_multiple_matches(link,'<div class="pc-results-pages" id="pc-pages-bottom">(.*?)</div>')
    
    for entry in next_page:
		
        url = plugintools.find_single_match(entry,'<li class="nav-pages-next"><a href="(.+?)" data-page=".+?" aria-label="Next page">Next</a>')
        name = plugintools.find_single_match(entry,'<li class="nav-pages-next"><a href=".+?" data-page=".+?" aria-label="(.+?)">Next</a>')

        addDir(name,url,1,art+'')
	
def get_episodes(url):
    find_url=url.find('?')+1
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    pattern = ""
    matches = plugintools.find_multiple_matches(link,'<div class="programme__overlay programme__overlay--available">(.*?)</li>')
    
    for entry in matches:
        
        title = plugintools.find_single_match(entry,'<span property="name">(.+?)</span>').replace("&amp;","&")
        thumbnail = plugintools.find_single_match(entry,'<meta property="thumbnailUrl" content="(.+?)" />')
        plot = plugintools.find_single_match(entry,'<span property="description">(.+?)</span>')
        url = plugintools.find_single_match(entry,'<a class="link-complex br-linkinvert buttons__download__link" href="(.+?)" download=')

        plugintools.add_item( action="play" , title=title , plot=plot , url=url , fanart=fanart , thumbnail=thumbnail , folder=False )

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
            contextMenuItems.append(('Add to My Podcasts', 'XBMC.RunPlugin(%s?mode=103&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        else:
            name = name
            contextMenuItems.append(('Remove from My Promotions', 'XBMC.RunPlugin(%s?mode=104&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, True)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok        
              
params=get_params()
url=None
name=None
mode=None



def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path

def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None
		
def watched_index(url):
    try:
        content = read_from_file(WATCHED_FILE)
        line = str(url)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1 #Not subscribed
		
def favourites_index(url):
    try:
        content = read_from_file(FAVOURITES_FILE)
        line = str(url)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1

def watched(url,filename):
    if filename==WATCHED_FILE:
        index = watched_index(url)
    else:
        index = favourites_index(url)
    if index >= 0:
        return
    content = str(url) + '\n'
    write_to_file(filename, content, append=True)
    xbmc.executebuiltin("Container.Refresh")
    
def unwatched(url,filename):
    if filename==WATCHED_FILE:
        index = watched_index(url)
    else:
        index = favourites_index(url)
    if index >= 0:
        content = read_from_file(filename)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        
        if len(s) == 0:
            os.remove(filename)
        else:
            write_to_file(filename, s)
        xbmc.executebuiltin("Container.Refresh")

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
        get_podcasts(url)
		
elif mode==2:
        print ""+url
        get_episodes(url)
		
elif mode==3:
        print ""+url
        cats()
		
elif mode==4:
        print ""+url
        stations()

elif mode==5:
        my_podcasts()
		
elif mode==101:
        watched(url,filename=WATCHED_FILE)
		
elif mode==102:
        unwatched(url,filename=WATCHED_FILE)
		
elif mode==103:
        watched(url,filename=FAVOURITES_FILE)
		
elif mode==104:
        unwatched(url,filename=FAVOURITES_FILE)
		

xbmcplugin.endOfDirectory(int(sys.argv[1]))
