import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
import plugintools
import settings
import glob
import shutil
from t0mm0.common.net import Net
from threading import Thread
net = Net()

DATA_PATH = settings.data_path()
ADDON = settings.addon()
BROKEN_FILE = settings.broken_file()
FAVOURITES_FILE = settings.favourites_file()
FAVOURITES_AUDIO_FILE = settings.favourites_audio_file()
DOWNLOAD_PATH = settings.download_directory()
AUDIO_FANART = settings.blind_me()

base_url = 'http://www.concertsvideos.com'
bv_url = 'http://www.bandsvideos.com/'
audio_url = 'http://tela.sugarmegs.org/'
youtube_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.concertarchive', 'fanart.jpg'))
audio_fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.concertarchive', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.concertarchive/art', ''))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.concertarchive', 'icon.png'))

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def POST_URL(url, form_data):
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Host'] = 'tela.sugarmegs.org'
    header_dict['Referer'] = 'http://tela.sugarmegs.org/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    req = net.http_POST(url, form_data=form_data, headers=header_dict).content.encode("utf-8").rstrip()
    return req

def CATEGORIES():
        addDir('Top Concerts','http://www.concertsvideos.com/top-concerts',1,art + 'icon_menu_topconcerts.jpg','')
        addDir('New Concerts','http://www.concertsvideos.com/new-concerts',1,art + 'icon_menu_newconcerts.jpg','')
        addDir('Artists','http://www.concertsvideos.com/artists',2,art + 'icon_menu_byartist.jpg','')
        addDir('Search','url',9,art + 'icon_menu_searcharchives.jpg','')
        addDir('Favourites','url',8,art + 'icon_menu_favourites.jpg','')
        addDir('Top Concerts (audio)','http://tela.sugarmegs.org/MostListened.aspx',51,art + 'icon_menu_audio_topconcerts.png','a')
        addDir('New Concerts (audio)','http://tela.sugarmegs.org/latestadditions.aspx',51,art + 'icon_menu_audio_newconcerts.png','a')
        addDir('Artists (audio)','url',53,art + 'icon_menu_audio_byartist.png','a')
        addDir('Search (audio)','url',52,art + 'icon_menu_audio_searcharchives.png','a')
        addDir('Favourites (audio)','url',57,art + 'icon_menu_audio_favourites.png','a')


def concert_list(url):
    link = open_url(url)
    all_concerts = regex_get_all(link, '<tr class', '</tr>')
    for concert in all_concerts:
        cd = regex_get_all(concert, '<td', '</td>')
        artist = regex_from_to(cd[3], '">', '</a>')
        artist_url = regex_from_to(cd[3], 'href="', '">')
        artist_url = base_url + artist_url
        title = regex_from_to(cd[2], '">', '</a>')
        title_url = regex_from_to(cd[2], 'href="', '">')
        url = base_url + title_url
        thumb = regex_from_to(cd[1], '<img src="', '"')
        try:
            views = regex_from_to(cd[4], 'totalcount" >', '</td').strip() + ' views'
            text = "%s - %s - %s views" % (artist, title, views)
        except:
            text = "%s - %s" % (artist, title)
        addDirVideo(artist,text,url,5,thumb,artist_url)
		
def artists(url):
    addDir('[COLOR cyan] << Return to Main Menu [/COLOR]', '','','', '')
    link = open_url(url)
    matchpg = re.compile('"pager-item"><a title="(.+?)" href="(.+?)">(.+?)</a>').findall(link)
    all_artists = regex_get_all(link, '<div class="views-field views-field-field-image">', '<div class="views-row')
    for artists in all_artists:
        a = regex_get_all(artists, '<div class="views-field', '</div>')
        thumb = regex_from_to(a[0], 'img src="', '"')
        artist_str = re.compile('<span class="field-content"><a href="(.+?)">(.+?)</a>').findall(a[1])
        for u,t in artist_str:
            url = base_url + u  
            artist = t.replace('&#8211;', '-').replace('&amp;', '&')
        try:
            description = regex_from_to(a[2], '<p>', '</p>').replace('<strong>','').replace('</strong>','')
        except:
            description = ''
        addDir(artist,url,3,thumb,description)
    for text, purl, pg in matchpg:
        purl = base_url + purl
        title = '[COLOR lime]' + text + '[/COLOR]'
        addDir(title, purl,2,'', '')
    setView('episodes', 'episodes-view')
	
def artist_videos(name, url):
    broken_links = read_from_file(BROKEN_FILE)
    addDir('[COLOR cyan] << Return to Main Menu [/COLOR]', '','','', '')
    try:
        link = open_url(url)
        body = regex_from_to(link, '<tbody>', '</tbody>')
        all_concerts = regex_get_all(body, 'views-field views-field-field-teaser-image', '</td>')
        for concert in all_concerts:
            cd = regex_get_all(concert, '<div class', '</div>')
            artist = name
            thumb = regex_from_to(cd[0], 'img src="', '"')
            title_str = re.compile('<span class="field-content"><a href="(.+?)">(.+?)</a>').findall(cd[1])
            for u,t in title_str:
                url = base_url + u
                title = t.replace('&#8211;', '-').replace('&amp;', '&')
                print url
            text = "[COLOR cyan]%s - %s[/COLOR] (concertsvideos.com)" % (artist, title)
            if not url in broken_links:
                addDirVideo(title,text,url,5,thumb,artist)
    except:
        pass
		
    #Search www.bandsvideos.com
    try:
        url = bv_url + '?s=' + urllib.quote_plus(name)
        link = open_url(url)
        matchpg = re.compile("<span class='pages'>(.+?)</span><span class='current'>(.+?)</span><a href='(.+?)' class='page larger'>(.+?)</a>").findall(link)
        all_concerts = regex_get_all(link, '<div class="entry-thumbnail">', '</div>')
        for c in all_concerts:
            url = regex_from_to(c, 'href="', '"')
            title = regex_from_to(c, 'title="', '"').replace('&#8211;', '-').replace('&amp;', '&')
            text = "[COLOR cyan]%s - %s[/COLOR] (bandsvideos.com)" % (name, title)
            thumb = regex_from_to(c, 'img src="', '"')
            if not url in broken_links:
                addDirVideo(title,text,url,5,thumb,name)
        if len(matchpg)>0:
            for a, b, purl, pg in matchpg:
                link = open_url(purl)
                all_concerts = regex_get_all(link, '<div class="entry-thumbnail">', '</div>')
                for c in all_concerts:
                    url = regex_from_to(c, 'href="', '"')
                    title = regex_from_to(c, 'title="', '"').replace('&#8211;', '-').replace('&amp;', '&')
                    text = "[COLOR cyan]%s - %s[/COLOR] (bandsvideos.com)" % (name, title)
                    thumb = regex_from_to(c, 'img src="', '"')
                    if not url in broken_links:
                        addDirVideo(title,text,url,5,thumb,name)
    except:
        pass

def search():
    keyboard = xbmc.Keyboard('', 'Search Artist', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_artist(query)
		
def search_artist(query):
    url = 'http://www.concertsvideos.com/search/node/' + query
    link = open_url(url) # Search concertsvideos.com
    results = regex_get_all(link, '<li class="search-result">', '</li>')
    for r in results:
        match = re.compile('<a href="(.+?)">(.+?)</a>').findall(r)
        for url, name in match:
            if '/artist/' in url:
                addDir(name,url,3,'','')
    if len(results)==0:
       addDir(query,'http://www.concertsvideos.com/artist/' + query,3,'','') 
        
def PLAY_VIDEO(name, url):
    link = open_url(url)
    try: #concertsvideos.com
        youtube_id = regex_from_to(link, 'data="http://www.youtube.com/v/', 'rel')
    except: #bandsvideos.com   
        youtube_id = regex_from_to(link, 'src="http://www.youtube.com/embed/', 'rel')
    vurl = youtube_id.replace('?', '')
    url='plugin://plugin.video.youtube/?action=play_video&videoid=%s' % vurl
    xbmc.Player().play(url)

			
def FAVOURITES():
    if os.path.isfile(FAVOURITES_FILE):
        s = read_from_file(FAVOURITES_FILE)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<>')
                name = list[0]
                url = list[1]
                thumb = list[2]
                addDirVideo('',name,url,5,thumb,'fav')
				
#################################################################################################################################################
###### AUDIO

def a_to_z():
    alphabet =  ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a, 'http://tela.sugarmegs.org/alpha/%s.html' % (a.lower().replace('#', 'Nu')),54,art + a.replace('#','hash') + '.png', 'a')
		
def audio_az(url):
    link = open_url(url).strip(' \t\n\r')
    link = regex_from_to(link, '<td>Setlist</td>', '</table>')
    all_concerts = regex_get_all(link, '<tr>', '</tr>')
    for concerts in all_concerts:
        match1=re.compile('href=(.+?)>mp3<').findall(concerts)
        match2=re.compile('href=(.+?).asx>(.+?)<').findall(concerts)
        for a in match1:
            mp3url = a
        for a,b in match2:
            title = b
        dp.close()
        addDirAudio('',title,mp3url,60,'')

def audio_new(url):
    link = open_url(url).strip(' \t\n\r')
    link = regex_from_to(link, '<td width="30px" class="colstyle">', '</table>')
    all_concerts = regex_get_all(link, '<tr>', '</tr>')
    for concerts in all_concerts:
        links = regex_get_all(concerts, '<td class="colstyle">', '</td>')
        for l in links:
            match1=re.compile('Repeater1_MP3Download_(.+?)" href="(.+?)">').findall(l)
            match2=re.compile('epeater1_ListenLink_(.+?)" title="(.+?)" href="(.+?)">(.+?)<').findall(l)
            for a,b in match1:
                mp3url = b
            for a,b,c,d in match2:
                title = d
        addDirAudio('',title,mp3url,60,'')
		
def search_audio():
    keyboard = xbmc.Keyboard('', 'Search Artist', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_audio_artist(query)
			
def search_audio_artist(query):
    playlist=[]
    fd_link = open_url(audio_url)
    viewstate = regex_from_to(fd_link, 'VIEWSTATE" value="', '"')
    eventvalidation = regex_from_to(fd_link, 'EVENTVALIDATION" value="', '"')
    form_data = ({'tbSearch': query, '__EVENTTARGET':	'btnSearch', '__VIEWSTATE': viewstate, '__EVENTVALIDATION': eventvalidation})
    link = net.http_POST(audio_url, form_data=form_data).content.encode("utf-8").strip(' \t\n\r')
    results = regex_from_to(link, 'font-size:large">Search Results<', '</table>')
    all_concerts = regex_get_all(results, '<tr>', '</tr>')
    for concerts in all_concerts:
        match1=re.compile('SearchResults_LinkDownloadMP3_(.+?)" href="(.+?)"').findall(concerts)
        match2=re.compile('SearchResults_AsxName_(.+?)">(.+?)<').findall(concerts)
        for a,b in match1:
            mp3url = b
        for a,b in match2:
            title = b
        addDirAudio('',title,mp3url,60,'')
		
def FAVOURITES_AUDIO():
    if os.path.isfile(FAVOURITES_AUDIO_FILE):
        s = read_from_file(FAVOURITES_AUDIO_FILE)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list = list.split('<>')
                name = list[0]
                url = list[1]
                addDirAudio('',name,url,60,'fav')

def play_audio(name,url):
    xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(url)
	
# DOWNLOAD
def download_show(name, url):
    WAITING_TIME = 5
    directory=DOWNLOAD_PATH
    filename = "%s.%s" % (name, '.mp3')
    data_path = os.path.join(directory, filename)
    dlThread = DownloadThread(name, url, data_path)
    if directory == "set" or directory == "":
        xbmcgui.Dialog().ok('Download directory not set', 'Set your download path in settings first')
        ADDON.openSettings()
    else:
        dlThread.start()
        wait_dl_only(WAITING_TIME, "Starting Download")
        if os.path.exists(data_path):
            notification('Concert Archive - Download started', name, '5000', iconart)
        else:
            notification('Concert Archive - Download failed', name, '5000', iconart)
       

class DownloadThread(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = str(self.path)
        data = self.data
        urllib.urlretrieve(data, path)
        notification('Concert Archive - Download finished', name, '5000', iconart)
        xbmc.executebuiltin(notify)	

# END DOWNLOAD


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

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        if description == 'a' and AUDIO_FANART:
            liz.setProperty('fanart_image', art + 'fanart_audio.jpg')
        else:
            liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirVideo(artist,name,url,mode,iconimage,artist_url):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        text = "%s<>%s<>%s" % (name, url, iconimage)
        if artist_url == 'fav':
            contextMenuItems.append(('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=15&url=%s)'% (sys.argv[0], text)))
        else:
            contextMenuItems.append(('Mark as Favourite', 'XBMC.RunPlugin(%s?mode=12&url=%s)'% (sys.argv[0], text)))
            contextMenuItems.append(('Mark as Broken', 'XBMC.RunPlugin(%s?mode=11&url=%s)'% (sys.argv[0], url)))
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, True)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addDirAudio(artist,name,url,mode,iconimage):
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        text = "%s<>%s" % (name, url)
        if iconimage == 'fav':
            contextMenuItems.append(('Remove from Favourites', 'XBMC.RunPlugin(%s?mode=55&url=%s)'% (sys.argv[0], text)))
        else:
            contextMenuItems.append(('Mark as Favourite', 'XBMC.RunPlugin(%s?mode=56&url=%s)'% (sys.argv[0], text)))
        contextMenuItems.append(("Download Show",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=70)'%(sys.argv[0],name,url)))
        liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, True)
        liz.setInfo('music', {'Artist':artist, 'Album':name})
        liz.setProperty('mimetype', 'audio/mpeg')
        if AUDIO_FANART:
            liz.setProperty('fanart_image', art + 'fanart_audio.jpg')
        else:
            liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None


########## HELPERS ############

def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r
	
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
		
def broken_index(url):
    try:
        content = read_from_file(BROKEN_FILE)
        line = str(url)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1 #Not subscribed
		
def favourites_index(name):
    try:
        content = read_from_file(FAVOURITES_FILE)
        line = str(url)
        lines = content.split('\n')
        index = lines.index(line)
        return index
    except:
        return -1
		
def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1

def write_to_list(url, filename):
    if filename==BROKEN_FILE:
        index = broken_index(url)
    else:
        index = favourites_index(url)
    if index >= 0:
        return
    content = str(url) + '\n'
    write_to_file(filename, content, append=True)
	
def remove_from_list(url, file):
    index = find_list(url, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        xbmc.executebuiltin("Container.Refresh")

def wait_dl_only(time_to_wait, title):
    print 'Waiting ' + str(time_to_wait) + ' secs'    

    progress = xbmcgui.DialogProgress()
    progress.create(title)
    
    secs = 0
    percent = 0
    
    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = int((100 * secs) / time_to_wait)
        secs_left = str((time_to_wait - secs))
        remaining_display = ' waiting ' + secs_left + ' seconds for download to start...'
        progress.update(percent, remaining_display)
        xbmc.sleep(1000)
        if (progress.iscanceled()):
            cancelled = True
            break
    if cancelled == True:     
        print 'wait cancelled'
        return False
    else:
        print 'Done waiting'
        return True 

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")		

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
try:
        description=str(params["description"])
except:
        pass

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        concert_list(url)
        
elif mode==2:
        artists(url)
		
elif mode==3:
        artist_videos(name,url)
		
elif mode==5:
        PLAY_VIDEO(name, url)

elif mode==8:
        FAVOURITES()
		
elif mode==9:
        search()
		
elif mode == 11:
        write_to_list(url, BROKEN_FILE)
		
elif mode == 12:
        write_to_list(url, FAVOURITES_FILE)
		
elif mode == 15:
        remove_from_list(url, FAVOURITES_FILE)
		
elif mode == 56:
        write_to_list(url, FAVOURITES_AUDIO_FILE)
		
elif mode == 55:
        remove_from_list(url, FAVOURITES_AUDIO_FILE)
		
elif mode==51:
        audio_new(url)
		
elif mode == 52:
        search_audio()
		
elif mode == 53:
        a_to_z()
		
elif mode == 54:
        audio_az(url)
		
elif mode ==60:
        play_audio(name,url)
		
elif mode==57:
        FAVOURITES_AUDIO()
		
elif mode == 70:
        download_show(name, url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
