import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import cookielib
from helpers import clean_file_name
import settings, time
import glob
import shutil
from t0mm0.common.net import Net
from threading import Thread
import json
import requests
import cookielib
cookie_jar = settings.cookie_jar()

net = Net()
ADDON = settings.addon()
ACTIVEPL = settings.current_playlist()
JACCOUNT = settings.jango_account()
USER=settings.username()
PW=settings.password()
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.jango',  'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.jango',  'art')) + '/'
audio_fanart = ""
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.jango/art',  'icon_generic.jpg'))
dialog = xbmcgui.Dialog()


def login(url):
    if not JACCOUNT:
        f = open(cookie_jar, 'w')
        f.close()
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://www.jango.com/').content.encode("utf-8").replace('\n','')
    net.save_cookies(cookie_jar)
    try:contenttime=regex_from_to(link,'updated_time" content="','"')
    except:contenttime=str(int(round(time.time() * 1000)))
    try:sid=regex_from_to(link,'jm.session_id                  = "','"')
    except:sid='na'
    token=regex_from_to(link,'<meta name="csrf-param" content="authenticity_token" /><meta name="csrf-token" content="','"')
    try:userid=regex_from_to(link,'<a href="/profiles/','"')
    except:userid='na'
    xbmcgui.Window(10000).setProperty("user_id", userid)
    xbmcgui.Window(10000).setProperty("contenttime", contenttime)
    xbmcgui.Window(10000).setProperty("sid", sid)
    xbmcgui.Window(10000).setProperty("token", token)
    if len(userid)<4 and JACCOUNT: 
        try:	
            headers = {'Host': 'www.jango.com', 'Referer': 'http://www.jango.com/'}
            payload = {'authenticity_token': token, 'round_this_login_btn': '', 'user[email]': USER, 'user[password]': PW}
            net.set_cookies(cookie_jar)
            link = net.http_POST(url,headers=headers,form_data=payload).content.encode("utf-8").replace('\n','')
            net.save_cookies(cookie_jar)
            try: userid=regex_from_to(link,'a href="/profiles/','"')
            except:userid='na'
            xbmcgui.Window(10000).clearProperty("user_id")
            xbmcgui.Window(10000).setProperty("user_id", userid)
        except:
            pass

def login2():
    ADDON.setSetting('jango_account', 'true')
    login('https://www.jango.com/splogin')
    xbmc.executebuiltin("Container.Refresh")

def CATEGORIES():
    userid=xbmcgui.Window(10000).getProperty("user_id")
    if len(userid)<4:
        if len(USER)>4 and len(PW)>3:
            addDirAudio('Login','https://www.jango.com/splogin',9998,iconart,'','','','','')
    addDir('Browse Music','http://www.jango.com/browse_music',2,art + 'icon_browse_music.jpg','','')
    if len(userid)>4:
        addDir('Station History','url',9951,art + 'icon_station_history.jpg','1','')
        addDir('Song History','http://www.jango.com/my_song_history',9952,art + 'icon_song_history.jpg','1','')
        addDir('Favourite Songs','http://www.jango.com/song_ratings/favorites',9950,art + 'icon_favourite_songs.jpg','1','')
        addDir('Banned Songs','http://www.jango.com/song_ratings/bans',9950,art + 'icon_banned_songs.jpg','1','')
    addDir('Search Artists','url',24,art + 'icon_search_artists.jpg','','')
    addDir('Search Songs','url',24,art + 'icon_search_songs.jpg','','')

def music_sections(name, url):
    headers = {'Host': 'www.jango.com', 'Referer': 'http://www.jango.com/browse_music', 'X-XHR-Referer': 'http://www.jango.com/browse_music'}    
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.replace('\n','')
    net.save_cookies(cookie_jar)
    token=xbmcgui.Window(10000).getProperty("token")
    match=re.compile('<li id="(.+?)" class="(.+?)"><a data-no-turbolink href="(.+?)" data-genre-category="(.+?)" title="(.+?)">(.+?)</a></li>').findall(link)
    #addDir("Suggestions",'http://www.jango.com/stations/genre_category?gcid=suggestions&_=1445381979609',3,iconart,token,'')
    #addDir("Recent Stations",'http://www.jango.com/stations/genre_category?gcid=recent&_=1445381979609',3,iconart,token,'')
    for d1,cl,url,cat,title,title2 in match:
        id = url.replace('/browse_music?gcid=','')
        url='http://www.jango.com/stations/genre_category?gcid=%s' % id
        addDir(clean_file_name(title, use_blanks=False),url,3,iconart,token,'')
		
def sub_sections(name, url, token):
    url=url.replace(' ','+')
    curr_time=int(round(time.time() * 1000))
    url="%s&_=%s" % (url,curr_time)
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/browse_music','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept': '*/*', 'X-CSRF-Token': token}
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=headers).content.encode("utf-8").replace('\n','').replace("'",'"')
    net.save_cookies(cookie_jar)
    all_sub=regex_get_all(link,'<div class="genre_station','<hr class="list_divider"/>')
    for a in all_sub:
        title=regex_from_to(a,'play"></span></span>','</a>')
        stid=regex_from_to(a,'href="/stations/','/')
        url='http://www.jango.com/stations/%s/tunein' % stid
        iconimage='http:' + regex_from_to(a,'data-original="','"').replace('_sm','_lg')
        addDir(clean_file_name(title, use_blanks=False),url,10,iconimage,token,stid)

def search(name, url):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            if name == 'Search Artists':
                search_artists(query)
            elif name == 'Search Songs':
                search_songs(query)
				
def search_artists(query):
    curr_time=int(round(time.time() * 1000))
    token=xbmcgui.Window(10000).getProperty("token")
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    url = 'http://www.jango.com/artists/jsearch?term=%s&cb=play&source=header&_=%s' % (urllib.quote_plus(query),str(curr_time))
    net.set_cookies(cookie_jar)
    link = net.http_GET(url,headers=headers).content.encode("utf-8").replace('\n','')
    net.save_cookies(cookie_jar)
    match=re.compile('{"label":"(.+?)","value":"(.+?)","id":(.+?),"url":"(.+?)","station_id":(.+?)}').findall(link)
    for label,value,id,url,stid in match:
        url='http://www.jango.com' + url
        addDir(clean_file_name(value, use_blanks=False),url,10,iconart,token,stid)
		
def search_songs(query):
    curr_time=int(round(time.time() * 1000))
    token=xbmcgui.Window(10000).getProperty("token")
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    url = 'http://www.jango.com/artists/search?search=%s&search_type=song' % (urllib.quote_plus(query))
    net.set_cookies(cookie_jar)
    link = net.http_GET(url,headers=headers).content.encode("utf-8").replace('\n','')
    net.save_cookies(cookie_jar)
    songs=regex_get_all(link,'<li class="song_li artist_song_li">','</li>')
    for s in songs:
        artist=regex_from_to(s,'class="block">','</a>')
        try:
            songname=regex_from_to(s,'title="Play ','"').replace(' Now!','')#video_id&quot;:&quot;
            vurl=regex_from_to(s,'video_id&quot;:&quot;','&quot')
            songid=regex_from_to(s,'trid&quot;:',',')
        except:
            songname=regex_from_to(s,'<div class="song_name" >','</div>').strip()
            vurl="NA"
            try:
                songid=regex_from_to(s,'song_id=','"')
            except:songid="na"
        iconimage='https://i.ytimg.com/vi/%s/mqdefault.jpg' % vurl
        url='plugin://plugin.video.youtube/play/?video_id=' + vurl
        title="%s - %s" % (artist,songname)
        if songid!="na":
            if vurl=="NA":
                addDirAudio(clean_file_name(title, use_blanks=False) + " (audio)",songid,13,iconimage,songname,artist,'na','na',vurl)
            else:
                addDirAudio(clean_file_name(title, use_blanks=False) + " (video)",url,12,iconimage,songname,artist,'na','na',vurl)
		
def favourite_tracks(name,url,page):
    if 'Banned' in name:
        tt='ban'
        url='http://www.jango.com/song_ratings/bans?page=%s' % page
    else:
        tt='fav'
        url='http://www.jango.com/song_ratings/favorites?page=%s' % page
    
    nextpage=int(page)+1
    refurl='http://www.jango.com/profiles/%s?ft=1' % xbmcgui.Window(10000).getProperty("user_id")   
    headers = {'Host': 'www.jango.com', 'Referer': refurl, 'X-XHR-Referer': refurl}
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=headers).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    if tt=='ban':
        songs=regex_get_all(link,'<li id="ban','</li>')
    else:
        songs=regex_get_all(link,'<li id="fav','</li>')
    for s in songs:
        artist=regex_from_to(s,'class="block">','</a>')
        try:
            songname=regex_from_to(s,'title="Play ','"').replace(' Now!','')#video_id&quot;:&quot;
            vurl=regex_from_to(s,'video_id&quot;:&quot;','&quot')
            songid=regex_from_to(s,'song_id=','"')
        except:
            songname=regex_from_to(s,'<div class="song_name" >','</div>').strip()
            vurl="NA"
            try:
                songid=regex_from_to(s,'song_id=','"')
            except:songid="na"
        iconimage='https://i.ytimg.com/vi/%s/mqdefault.jpg' % vurl
        url='plugin://plugin.video.youtube/play/?video_id=' + vurl
        title="%s - %s" % (artist,songname)
        if songid!="na":
            if vurl=="NA":
                addDirAudio(clean_file_name(title, use_blanks=False) + " (audio)",songid,13,iconimage,songname,artist,songid,tt,vurl)
            else:
                addDirAudio(clean_file_name(title, use_blanks=False) + " (video)",url,12,iconimage,songname,artist,songid,tt,vurl)
    addDir('Next page - '+name,'url',9950,art + 'topalbums.jpg',str(nextpage),'')
	
def station_history(page):
    nextpage=int(page)+1
    refurl='http://www.jango.com/users/%s/stations?page=%s' % (xbmcgui.Window(10000).getProperty("user_id"),page)
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','X-XHR-Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'text/html, application/xhtml+xml, application/xml', 'X-Requested-With': 'XMLHttpRequest'}
    net.set_cookies(cookie_jar)
    link = net.http_GET(refurl,headers=headers).content.encode("utf-8").replace('\n','').replace("'",'"')
    net.save_cookies(cookie_jar)
    token=xbmcgui.Window(10000).getProperty("token")
    all_sub=regex_get_all(link,'<div class="genre_station','<hr class="list_divider"/>')
    for a in all_sub:
        title=regex_from_to(a,'play"></span></span>','</a>')
        stid=regex_from_to(a,'href="/stations/','/')
        url='http://www.jango.com/stations/%s/tunein' % stid
        iconimage='http:' + regex_from_to(a,'data-original="','"').replace('_sm','_lg')
        addDir(clean_file_name(title, use_blanks=False),url,10,iconimage,token,stid)
    addDir('Next page','url',9951,art + 'icon_next_page.jpg',str(nextpage),'')
		
def song_history(url,page):
    nextpage=int(page)+1
    url='http://www.jango.com/users/%s/full_history?page=%s' % (xbmcgui.Window(10000).getProperty("user_id"),page) 
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','X-XHR-Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'text/html, application/xhtml+xml, application/xml', 'X-Requested-With': 'XMLHttpRequest'}
    net.set_cookies(cookie_jar)
    link = net.http_GET(url,headers=headers).content.encode("utf-8").replace('\n','').replace("'",'"')
    net.save_cookies(cookie_jar)
    songs=regex_get_all(link,'<li class="song_li artist_song_li">','</li>')
    for s in songs:
        artist=regex_from_to(s,'class="block">','</a>')
        try:
            songname=regex_from_to(s,'title="Play ','"').replace(' Now!','')#video_id&quot;:&quot;
            vurl=regex_from_to(s,'video_id&quot;:&quot;','&quot')
            songid=regex_from_to(s,'trid&quot;:',',')
        except:
            songname=regex_from_to(s,'<div class="song_name" >','</div>').strip()
            vurl="NA"
            try:
                songid=regex_from_to(s,'song_id=','"')
            except:songid="na"
        iconimage='https://i.ytimg.com/vi/%s/mqdefault.jpg' % vurl
        url='plugin://plugin.video.youtube/play/?video_id=' + vurl
        title="%s - %s" % (artist,songname)
        if songid!="na":
            if vurl=="NA":
                addDirAudio(clean_file_name(title, use_blanks=False) + " (audio)",songid,13,iconimage,songname,artist,'na','na',vurl)
            else:
                addDirAudio(clean_file_name(title, use_blanks=False) + " (video)",url,12,iconimage,songname,artist,'na','na',vurl)
    addDir('>> Next Page','http://www.jango.com/my_song_history',9952,art + 'icon_next_page.jpg',str(nextpage),'')

class play_timer(Thread):
    def __init__(self,url,name,token,iconimage,streamurl,stid):
        time.sleep(3)
        self.url=url
        self.name=name
        self.token=token
        self.iconimage=iconimage
        self.streamurl=streamurl
        self.stid=stid
        Thread.__init__(self)

    def run(self):
        start_time = time.time()
        url=self.url
        name=self.name
        token=self.token
        iconimage=self.iconimage
        streamurl=self.streamurl
        stid=self.stid
        #print "HAS NEXT " + str(xbmc.getCondVisibility('MusicPlayer.HasNext'))
        secs=0
        while xbmc.Player().isPlayingAudio() and xbmcgui.Window(10000).getProperty("station_id")==stid:#secs < (int(dur)-25) and xbmc.Player().isPlayingAudio() and streamurl==playerurl:
            while xbmc.getCondVisibility('MusicPlayer.HasNext'):
                if xbmcgui.Window(10000).getProperty("station_id")==stid:
                    secs += 1
                    time.sleep(1)
                else:
                    #print "STAION CHANGED " + stid
                    break
            time.sleep(3)
            if xbmcgui.Window(10000).getProperty("station_id")==stid:
                #print "NOW ADD TRACK TO PLAYLIST: Playlist has next item is " + str(xbmc.getCondVisibility('MusicPlayer.HasNext'))
                play_song(url, name, token, iconimage,stid,False,False)

          
def play_song(url, name, token, iconimage,stid, clear, skip):
    userid=xbmcgui.Window(10000).getProperty("user_id")
    if len(userid)>4:
        uid='&uid=%s' % userid
    else:
        uid=''
    curr_time=int(round(time.time() * 1000))
    origurl=url
    origtoken=token
    pl = get_XBMCPlaylist(clear)
    playlist=[]
    contenttime=xbmcgui.Window(10000).getProperty("contenttime")
    sid=xbmcgui.Window(10000).getProperty("sid")
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest'}
    if clear:
        f = open(ACTIVEPL, 'w')
        f.close
        url='http://www.jango.com/stations/%s/play?_=%s' % (stid,curr_time)
    elif skip:
        url='http://www.jango.com/streams/info?sid=%s%s&stid=%s&ver=11&skipped=1&cb=%s&_=%s' % (sid,uid,stid,curr_time,contenttime)
    else:
        url='http://www.jango.com/streams/info?sid=%s%s&stid=%s&ver=11&next=1&cb=%s&_=%s' % (sid,uid,stid,curr_time,contenttime)
    net.set_cookies(cookie_jar)
    link = net.http_GET(url,headers=headers).content.encode("utf-8").replace('\n','')
    net.save_cookies(cookie_jar)
    url='http:' + regex_from_to(link,'"url":"','"')
    artist=regex_from_to(link,'artist":"','"')
    artistid=regex_from_to(link,'artist_id":',',"')
    artistlink=""
    songname=regex_from_to(link,'song":"','"')
    songid=regex_from_to(link,'"song_id":',',"')
    genre=regex_from_to(link,'"genre":"','"')
    similarartists=regex_from_to(link,'similar_stations":',']')
    try:
        videoid=regex_from_to(link,'video_id":"','"')
    except:
        videoid="na"
    albumart='http:'+ regex_from_to(link,'album_art":"',',"').replace('_sm','_xl')
    stationname=regex_from_to(link,'station":"','"')
    title = "%s | %s" % (artist,songname)
    PL_TEXT="%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s" % (title,url,albumart,songname,artist,stationname,songid,videoid,genre,artistlink)
    add_to_list(PL_TEXT,ACTIVEPL,False)
    addDir("[COLOR lime]"+stationname+" (edit station...)[/COLOR]",'url',99000,iconimage,'na','na')
    addDirAudio("Previous Song",origurl,16,iconimage,origtoken,stid,'na','na','na')
    addDirAudio("Skip Song",origurl,11,iconimage,origtoken,stid,'na','na','na')
    addDir("View Playlist",origurl,17,iconimage,origtoken,stid)
    addDirAudio("[COLOR cyan]  Similar Stations[/COLOR]",'url',10000,iconimage,'na','na','na','na','na')
    match=re.compile('"station_id":(.+?),"station_name":"(.+?)"').findall(similarartists)
    for s_stationid,s_stationname in match:
        s_url='http://www.jango.com/stations/%s/tunein' % s_stationid
        addDir("  "+clean_file_name(s_stationname, use_blanks=False),s_url,10,iconimage,token,s_stationid)	
    liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':stationname })
    liz.setProperty('mimetype', 'audio/mpeg')
    liz.setProperty("IsPlayable","true")
    liz.setThumbnailImage(iconimage)
    if clear or ((xbmcgui.Window(10000).getProperty("station_id")=="" or xbmcgui.Window(10000).getProperty("station_id")==stid) and not clear):
        playlist.append((url, liz))
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
    if clear:
        xbmc.Player().play(pl)
        xbmcgui.Window(10000).clearProperty("station_id")
        xbmcgui.Window(10000).setProperty("station_id", stid)
        playThread = play_timer(origurl,name,origtoken,iconimage,url,stid)
        playThread.start()
    if skip:
        xbmc.executebuiltin('XBMC.Playlist.PlayOffset(1)')

def previous_track():
    xbmc.executebuiltin('XBMC.Playlist.PlayOffset(-1)')
	
def track_history():
    if os.path.isfile(ACTIVEPL):
        s = read_from_file(ACTIVEPL)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = "  " + list1[0]
                url = list1[1]
                albumart = list1[2]
                songname = list1[3] 
                artist = list1[4]
                stationname = list1[5] 
                songid = list1[6]
                videoid = list1[7]
                genre = list1[8]
                artistlink = list1[9]
                addDirAudio(title,url,18,albumart,genre,artist,stationname,songid,artistlink)
				
def track_options(name,url,iconimage,genre,artist,album,songid,artistlink):
    dialog = xbmcgui.Dialog()
    option_list = ["[COLOR lime]Thumbs Up[/COLOR]","[COLOR orange]Thumbs Down[/COLOR]","View stations with " + artist,"View biography for " + artist]
    option_id = dialog.select("Song/Artist Options", option_list)
    if(option_id < 0):
        return (None, None)
        dialog.close()
    if(option_id == 0):
        thumbs_up(name, url,iconimage,songid)
    elif(option_id == 1):
        thumbs_down(name, url,iconimage,songid)
    elif(option_id == 2):
        token=xbmcgui.Window(10000).getProperty("token")
        xbmc.executebuiltin('Container.Update(%s?name=%s&url=%s&mode=3&type=%s)'%(sys.argv[0], urllib.quote(artist), urllib.quote_plus(artistlink), urllib.quote(token)))
    elif(option_id == 3):
        artist_bio(artist,iconimage,artistlink + '/_full_bio')
		
def artist_bio(artist,iconimage,url):
    url=url.replace(' ','+')
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8")
    net.save_cookies(cookie_jar)
    biobody=regex_from_to(link,'<div class="artist-bio" style="margin:20px 0; clear:both">','<div class="wiki_link"')

    text=biobody.replace('</p><p>', '\n').replace('</p></p>', '').replace('<p><p>', '').replace('<br />', '\n')#.replace('<p>', '\n')
    #biobody = re.sub(r'<.+?>', '', newsbody).replace('<>', '')
    header = "[B][COLOR gold]" + artist + "[/B][/COLOR]"
    TextBoxes(header,text)
	
def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
		
def station_edit(name,url,iconimage):
    curr_time=int(round(time.time() * 1000))
    url='http://www.jango.com/quickmixes/suggestions?_=%s' % curr_time
    token=xbmcgui.Window(10000).getProperty("token")
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    net.set_cookies(cookie_jar)
    link = net.http_GET(url,headers=headers).content.encode("utf-8").replace('\n','').replace('\\','')
    net.save_cookies(cookie_jar)
    addDir("[COLOR lime]Search Any Artist[/COLOR]",'url',99002,iconimage,'na','na')
    all_artists=regex_get_all(link,'<li>','/li>')
    for a in all_artists:
        title=regex_from_to(a,'button>','<')
        url=urllib.unquote('http://www.jango.com/' +(regex_from_to(a,'<a href="/','"')))
        addDirAudio(title,url,99001,iconimage,'na','na','na','na','na')
		
def station_edit_search(name, url,iconimage):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            curr_time=int(round(time.time() * 1000))
            token=xbmcgui.Window(10000).getProperty("token")
            headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
            url = 'http://www.jango.com/artists/jsearch?term=%s&cb=add&source=quickmix&_=%s' % (urllib.quote_plus(query),str(curr_time))
            net.set_cookies(cookie_jar)
            link = net.http_GET(url,headers=headers).content.replace('\n','')
            net.save_cookies(cookie_jar)
            match=re.compile('{"label":"(.+?)","value":"(.+?)","id":(.+?),"url":"(.+?)","station_id":(.+?)}').findall(link)
            for title,value,id,url,stid in match:
                addDirAudio(title,url,99003,iconimage,id,stid,'na','na','na')
		
def station_edit_add(name,url,iconimage):
    cj = cookielib.LWPCookieJar(cookie_jar)
    cj.load()
    userid=xbmcgui.Window(10000).getProperty("user_id")
    token=xbmcgui.Window(10000).getProperty("token")
    referer='http://www.jango.com/profiles/%s' % userid
    payload=None
    #net.set_cookies(cookie_jar)
    headers = {'Host': 'www.jango.com','Content-Length':'0','Referer': referer,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    try:
        link=requests.post(url,headers=headers,data=payload,cookies=cj).content.replace('\\','').replace('\n','')
        cj.save()
        lsn=regex_from_to(link,'limited_station_name": "','"')
        if 'We have added' in link:
            notification(name, "Added to your station", '4000',iconimage)
    except:
        pass

	
def station_edit_add2(name,url,iconimage,id,stid):
    cj = cookielib.LWPCookieJar(cookie_jar)
    cj.load()
    userid=xbmcgui.Window(10000).getProperty("user_id")
    token=xbmcgui.Window(10000).getProperty("token")
    referer='http://www.jango.com/profiles/%s' % userid
    payload={'artist_id': id,'inline':'true'}
    headers = {'Host': 'www.jango.com','Content-Length':'0','Referer': referer,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    try:
        link=requests.post('http://www.jango.com/quickmixes',headers=headers,data=payload,cookies=cj).content.replace('\\','').replace('\n','')
        cj.save()
        lsn=regex_from_to(link,'limited_station_name": "','"')
        if 'We have added' in link:
            notification(name, "Added to your station", '4000',iconimage)
    except:
        pass
	
def play_track(name,url,iconimage,artist,song,clear,skip):
    token=xbmcgui.Window(10000).getProperty("token")
    userid=xbmcgui.Window(10000).getProperty("user_id")
    if len(userid)>4:
        uid='&uid=%s' % userid
    else:
        uid=''
    curr_time=int(round(time.time() * 1000))
    origurl=url
    origtoken=token
    pl = get_XBMCPlaylist(clear)
    playlist=[]
    contenttime=xbmcgui.Window(10000).getProperty("contenttime")
    sid=xbmcgui.Window(10000).getProperty("sid")
    headers = {'Host': 'www.jango.com','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'X-CSRF-Token': token}
    url='http://www.jango.com/stations/airplay_song_tunein/play?song_id=%s&_=%s' % (origurl,curr_time)
    net.set_cookies(cookie_jar)
    link = net.http_GET(url,headers=headers).content.encode("utf-8").replace('\n','')
    net.save_cookies(cookie_jar)
    url=regex_from_to(link,'"url":"','"')
    artist=regex_from_to(link,'artist":"','"')
    artistid=regex_from_to(link,'artist_id":',',"')
    songname=regex_from_to(link,'song":"','"')
    songid=regex_from_to(link,'"song_id":',',"')
    try:
        videoid=regex_from_to(link,'video_id":"','"')
    except:
        videoid="na"
    albumart=regex_from_to(link,'album_art":"',',"').replace('_sm','_xl')
    stationname=regex_from_to(link,'station":"','"')
    title = "%s | %s" % (artist,songname)
    addDirAudio(title,url,10,albumart,songname,artist,stationname,songid,videoid)
    liz=xbmcgui.ListItem(songname, iconImage=albumart, thumbnailImage=albumart)
    liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':stationname })
    liz.setProperty('mimetype', 'audio/mpeg')
    liz.setProperty("IsPlayable","true")
    liz.setThumbnailImage(albumart)
    if clear or ((xbmcgui.Window(10000).getProperty("station_id")=="" or xbmcgui.Window(10000).getProperty("station_id")==stid) and not clear):
        playlist.append((url, liz))
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
    if clear:
        xbmc.Player().play(pl)
	
def play_video(name,url,iconimage,artist,song,mix,clear):
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(url, listitem)
		
def thumbs_up(name, url,iconimage,songid):
    token=xbmcgui.Window(10000).getProperty("token")
    if dialog.yesno("Confirm", 'Click Confirm and this song, and others similar to it,', 'will play more often in this station.',"We'll also add the song to your favourites",'Cancel','Confirm'):
        url="http://www.jango.com/song_ratings/add_favorite?song_id=%s" % songid
        headers = {'Host': 'www.jango.com', 'Referer': 'http://www.jango.com/', 'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript'}
        payload = {'authenticity_token': token, 'commit': 'Confirm', 'utf8': '%E2%9C%93'}
        net.set_cookies(cookie_jar)
        link = net.http_POST(url,headers=headers,form_data=payload).content.encode("utf-8").replace('\n','')
        net.save_cookies(cookie_jar)


def thumbs_down(name, url,iconimage,songid):
    token=xbmcgui.Window(10000).getProperty("token")
    url='http://www.jango.com/song_ratings/add_ban?song_id=%s' % songid
    headers = {'Host': 'www.jango.com', 'Referer': 'http://www.jango.com/', 'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript'}
    payload = {'authenticity_token': token, 'commit': 'Confirm', 'utf8': '%E2%9C%93', 'song_id': songid}
    net.set_cookies(cookie_jar)
    link = net.http_POST(url,headers=headers,form_data=payload).content.encode("utf-8").replace('\n','')
    net.save_cookies(cookie_jar)
	
def remove_from_fav(name, url,iconimage,songid):
    cj = cookielib.LWPCookieJar(cookie_jar)
    cj.load()
    token=xbmcgui.Window(10000).getProperty("token")
    url='http://www.jango.com/song_ratings/delete_favorite?song_id=%s' % songid
    headers = {'Host': 'www.jango.com','Content-Length':'0','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    payload = {}
    link=requests.post(url,headers=headers,data=payload,cookies=cj).content
    cj.save()
    xbmc.executebuiltin("Container.Refresh")

def remove_from_ban(name, url,iconimage,songid):
    cj = cookielib.LWPCookieJar(cookie_jar)
    cj.load()
    token=xbmcgui.Window(10000).getProperty("token")
    url='http://www.jango.com/song_ratings/delete_ban?song_id=%s' % songid
    headers = {'Host': 'www.jango.com','Content-Length':'0','Referer': 'http://www.jango.com/song_ratings/favorites','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.5', 'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'}
    payload = {}
    link = requests.post(url,headers=headers,data=payload,cookies=cj).content
    cj.save()
    xbmc.executebuiltin("Container.Refresh")



def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file, refresh):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)
    if refresh == True:
        xbmc.executebuiltin("Container.Refresh")
    
def remove_from_list(list, file):
    list = list.replace('<>Ungrouped', '').replace('All Songs', '')
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        if not 'song' in file and not 'album' in file:
            xbmc.executebuiltin("Container.Refresh")
		
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
		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
		
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


def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if clear:
        pl.clear()
    return pl
	
def clear_playlist():
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    pl.clear()
    notification('Playlist', 'Cleared', '2000', iconart)

	
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
	
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', audio_fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,type,id):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&list="+str(list)+"&type="+urllib.quote_plus(type)+"&id="+urllib.quote_plus(id)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirAudio(name,url,mode,iconimage,songname,artist,album,dur,type):
        suffix = ""
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&songname="+urllib.quote_plus(songname)+"&artist="+urllib.quote_plus(artist)+"&album="+urllib.quote_plus(album)+"&dur="+str(dur)+"&type="+str(type)
        ok=True
        liz=xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        if dur=="fav":
            contextMenuItems.append(("[COLOR orange]Remove from Favourite Tracks[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=57&iconimage=%s&album=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url),urllib.quote(iconimage),urllib.quote(album))))
        if dur=="ban":
            contextMenuItems.append(("[COLOR orange]Remove from Banned Tracks[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=58&iconimage=%s&album=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url),urllib.quote(iconimage),urllib.quote(album))))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None
type=None
id=None

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
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        songname=urllib.unquote_plus(params["songname"])
except:
        pass
try:
        artist=urllib.unquote_plus(params["artist"])
except:
        pass
try:
        album=urllib.unquote_plus(params["album"])
except:
        pass
try:
        list=str(params["list"])
except:
        pass
try:
        dur=str(params["dur"])
except:
        pass
try:
        type=urllib.unquote_plus(params["type"])
except:
        pass
try:
        id=urllib.unquote_plus(params["id"])
except:
        pass

if mode==None or url==None or len(url)<1:
    login('https://www.jango.com/splogin')
    CATEGORIES()

elif mode == 2:
    music_sections(name, url)
	
elif mode == 3:
    sub_sections(name, url, type)
	
elif mode == 10:
        play_song(url,name,type,iconimage,id,True,False)
		
elif mode == 11:
        play_song(url,name,songname,iconimage,artist,False,True)
		
elif mode == 14:
        play_song(url,name,type,iconimage,id,False,False)

elif mode == 12:
    play_video(name,url,iconimage,artist,songname,False,True)  

elif mode == 13:
    play_track(name,url,iconimage,artist,songname,True,False)

elif mode == 16:
    previous_track()

elif mode == 17:
    track_history()
	
elif mode == 18:
    track_options(name,url,iconimage,songname,artist,album,dur,type)

elif mode == 24:
    search(name, url)

elif mode == 26:
    search_songs(name)
	
elif mode == 27:
    search_artists(name)

elif mode == 55:
    thumbs_up(name, url,iconimage,dur)
	
elif mode == 56:
    thumbs_down(name, url,iconimage,dur)
	
elif mode == 57:
    remove_from_fav(name, url,iconimage,album)
	
elif mode == 58:
    remove_from_ban(name, url,iconimage,album)
	
elif mode == 9999:
    login(url)
	
elif mode == 9998:
    login2()

elif mode == 9950:
    favourite_tracks(name,url,type)
	
elif mode == 9951:
    station_history(type)
	
elif mode == 9952:
    song_history(url,type)
	
elif mode == 99000:
    station_edit(name,url,iconimage)
	
elif mode == 99001:
    station_edit_add(name,url,iconimage)
	
elif mode == 99002:
    station_edit_search(name, url,iconimage)
	
elif mode == 99003:
    station_edit_add2(name,url,iconimage,songname,artist)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
