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
import plugintools,xbmcaddon
import settings

DATA_PATH = settings.data_path()
ADDON = settings.addon()
WATCHED_FILE = settings.watched_videos_file()
FAVOURITES_FILE = settings.favourite_podcasts()

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.podcastone.rayw1986/resources/art', ''))
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.podcastone.rayw1986', 'fanart.jpg'))

addon_id = xbmcaddon.Addon().getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)
enable_auto_view = selfAddon.getSetting('enable_auto_view')
view_mode_id = selfAddon.getSetting('view_mode_id')

def CATEGORIES():
		addDirMain('My Podcasts','url',5,art+'favs.png')
		addDirMain('Featured','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Featured',1,art+'featured.png')
		addDirMain('New','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=New',1,art+'new.png')
		addDirMain('Categories','url',3,art+'cats.png')
		
def cats():
		addDirMain('Arts','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Arts',1,art+'arts.png')
		addDirMain('Comedy','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Comedy',1,art+'comedy.png')
		addDirMain('Games & Hobbies','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Games%20%26%20Hobbies',1,art+'games.png')
		addDirMain('Government & Organizations','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Government%20%26%20Organizations',1,art+'gov.png')
		addDirMain('Health','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Health',1,art+'health.png')
		addDirMain('Kids & Family','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Kids%20%26%20Family',1,art+'kids.png')
		addDirMain('Music','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Music',1,art+'music.png')
		addDirMain('News & Politics','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=News%20%26%20Politics',1,art+'news.png')
		addDirMain('Religion & Spirituality','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Religion%20%26%20Spirituality',1,art+'religion.png')
		addDirMain('Science & Medicine','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Science%20%26%20Medicine',1,art+'science.png')
		addDirMain('Society & Culture','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Society%20%26%20Culture',1,art+'society.png')
		addDirMain('Sports & Recreation','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Sports%20%26%20Recreation',1,art+'sports.png')
		addDirMain('Technology & Business','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=Technology;Business',1,art+'tech.png')
		addDirMain('TV & Film','http://www.podcastone.com/pg/jsp/general/showcategory.jsp?podcastCategory=TV%20%26%20Film',1,art+'tv.png')
		
		
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
            if enable_auto_view=='true':
                xbmc.executebuiltin('Container.SetViewMode(%d)' % int(view_mode_id))
            else:
                pass
		
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
    matches = plugintools.find_multiple_matches(link,'<td style="padding-bottom:22px;(.*?)</td>')
    
    for entry in matches:
        
        name = plugintools.find_single_match(entry,'alt="(.+?)"').replace("&amp;","&").replace('&quot;','"')
        get_iconimage = plugintools.find_single_match(entry,'src="(.+?)"')
        iconimage = 'http://www.podcastone.com' + get_iconimage
        get_url = plugintools.find_single_match(entry,'<a href="(.+?)">')
        url = 'http://www.podcastone.com'+get_url+'?showAllEpisodes=true'

        addDir(name,url,2,iconimage)
	
    if enable_auto_view=='true':
        xbmc.executebuiltin('Container.SetViewMode(%d)' % int(view_mode_id))
    else:
        pass
	
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
    matches = plugintools.find_multiple_matches(link,'<div class="programText"(.*?)/images/buttons/fb_icon_off.png')
    
    for entry in matches:
        
        title = plugintools.find_single_match(entry,'<div style="line-height: 20px;">(.+?)</div>').replace("&amp;","&")
        thumbnail = plugintools.find_single_match(entry,'<meta property="thumbnailUrl" content="(.+?)" />')
        plot = plugintools.find_single_match(entry,'<div id="description0" style="display:none;margin-top:5px;margin-left:55px;">(.+?)</div>')
        get_url = plugintools.find_single_match(entry,'href="http://www.podcastone.com/downloadsecurity(.+?)"').replace("\n","")
        url = 'http://www.podcastone.com/downloadsecurity'+get_url+''

        plugintools.add_item( action="play" , title=title , url=url , thumbnail=thumbnail , folder=False )

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
            contextMenuItems.append(('Remove from My Podcasts', 'XBMC.RunPlugin(%s?mode=104&url=%s)'% (sys.argv[0], urllib.quote_plus(nameurl))))
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
