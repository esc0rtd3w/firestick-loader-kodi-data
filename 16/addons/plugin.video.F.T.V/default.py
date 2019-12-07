'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
import calendar
from datetime import date
from threading import Timer
from hashlib import md5
from helpers import clean_file_name
import json
import glob
import shutil
from threading import Thread
import cookielib
import plugintools
from t0mm0.common.net import Net
net = Net()


ADDON = settings.addon()
FILMON_KEEP = settings.keep_session_flag()
FILMON_ACCOUNT = settings.filmon_account()
FILMON_USER = settings.filmon_user()
FILMON_QUALITY = settings.filmon_quality()
AUTO_SWITCH = settings.auto_switch()
STRM_TYPE = settings.stream_type()
FILMON_PASS = md5(settings.filmon_pass()).hexdigest()
FILMON_PASSWORD = settings.filmon_pass()
MY_VIDEOS = settings.my_videos()
MY_AUDIO = settings.my_audio()
OTHER_MENU = settings.other_menu()
HIDDEN_FILE = settings.hidden_file()
FAV_CHAN = settings.favourite_channels()
FAV_MOV = settings.favourite_movies()
SORT_ALPHA = settings.sort_alpha()
DOWNLOAD_PATH = settings.download_path()
MOVIE_DIR = settings.movie_directory()
SHOW_ID = settings.show_ch_id()
ROOT_CH = settings.root_channel()
cookie_jar = settings.cookie_jar()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'icon.png'))
channel_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'channel.list'))
group_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'groups.list'))
xml_list = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V/helpers', 'FilmOn.xml'))
base_url = 'http://www.filmon.com/'
disneyjrurl = 'http://www.disney.co.uk/disney-junior/content/video.jsp?b='
session_url = 'http://www.filmon.com/api/init/'
trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )



def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def GET_URL(url):
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['User-Agent'] = 'User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = net.http_GET(url, headers=header_dict).content
    return req
	
def keep_session():
    currentWindow = xbmcgui.getCurrentWindowId()
    #if currentWindow == 10000:
        #session_id = xbmcgui.Window(10000).getProperty("session_id")
        #lourl = "http://www.filmon.com/api/logout?session_key=%s" % (session_id)
        #open_url(lourl)
        #xbmcgui.Window(10000).clearProperty("session_id")
        #print 'FilmOn.TV..........logged out of Filmon'
        #return
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "http://www.filmon.com/api/keep-alive?session_key=%s" % (session_id)
    open_url(url)
    print 'FilmOn.TV..........Filmon session kept alive'
    tloop = Timer(60.0, keep_session)
    tloop.start()

try:
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s" % (base_url,'/tv/api/groups?session_key=',(session_id))
    link = open_url(url)
except:
    xbmcgui.Window(10000).setProperty("session_id", '')
if not xbmcgui.Window(10000).getProperty("session_id"):
    link = open_url(session_url)
    match= re.compile('"session_key":"(.+?)"').findall(link)
    session_id=match[0]
    if FILMON_ACCOUNT:
        login_url = "%s%s%s%s%s%s" % ("http://www.filmon.com/api/login?session_key=", session_id, "&login=", urllib2.quote(FILMON_USER), "&password=", FILMON_PASS)
        login = open_url(login_url)
        print "FilmOn.TV......Logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
        keep_session()
    else:
        print "FilmOn.TV......Not logged in"
        xbmcgui.Window(10000).setProperty("session_id", session_id)
        keep_session()
            
FILMON_SESSION = xbmcgui.Window(10000).getProperty("session_id")

def CATEGORIES():
    hidden_links = read_from_file(HIDDEN_FILE)
    addDir('Non Geo','url',110,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'xml.png')), '', '')
    addDir('FilmOn Demand ','url',199,'http://www.filmon.com/tv/themes/filmontv/img/mobile/filmon-logo-stb.png', '', '')
    addDir('My Channels','url',122,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    addDir('My Recordings','url',131,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'f_record.jpg')), '', '')
    addDir('Favourite Channels','url',415,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'my_channels.jpg')), '', '')
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s" % (base_url,'/tv/api/groups?session_key=', (session_id))
    link = open_url(url)
    all_groups = regex_get_all(link, '{', '_count')
    for groups in all_groups:
        alias = regex_from_to(groups, 'alias":"', '",')
        group_id = regex_from_to(groups, 'group_id":"', '",')
        channels=regex_from_to(groups,'channels":',',"channels').replace('[','').replace(']','').replace('"','')
        title = regex_from_to(groups, 'title":"', '",')
        thumb = regex_from_to(groups, 'logo_148x148_uri":"', '",').replace('\\', '')
        url = regex_from_to(groups, 'group_id":"', '",')
        if not title in hidden_links:
            addDir(title,group_id,123,thumb, alias,channels)
            setView('episodes', 'episodes-view')

		
def group_channels(url, title,alias,channels):#1416096000
    gt = str(title)
    if gt=="KIDS":
        addDir('Disney Junior Videos','http://www.disney.co.uk/disney-junior/content/video.jsp',301,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'disney_junior.jpg')), '', '')
        addDir('Disney Classic','http://gdata.youtube.com/feeds/api/users/UCa0h983kQj5OYa06gYhxgiw/uploads?start-index=1&max-results=50',395,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'mickey.gif')),'','')
    name_lst = []
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s%s%s" % (base_url, 'api/group/', url, '?session_key=', session_id)
    link = GET_URL(url).translate(trans_table)#.encode("utf-8", 'ignore')#.replace('\u00a0','').replace('\u00ae','').replace('\u00e9','').replace('\u00e0','')
    link=cleanlink(link)
    data=json.loads(link)
    channels=data['channels']
    for c in channels:
        channel_id=c['id']
        title=c['title']
        description=c['description']
        name_lst.append(title)
        if SHOW_ID:
            title="%s (%s)" % (title,channel_id)
        thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % channel_id
        #if 'BBC Music Magazine' not in title:
        addDirPlayable(title,str(channel_id),125,thumb,"na",'description', "na", "grp")
        setView('episodes', 'episodes-view')

    # read from channel list
    s = read_from_file(channel_list)
    search_list = s.split('\n')
    for list in search_list:
        if list != '':
            list1 = list.split('<>')
            st_grp = list1[0]
            st_name = list1[1]
            st_id = list1[2]
            st_url = list1[3]
            par = "%s<>%s" % (st_id, st_url)
            thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(st_id).rstrip()
            if st_grp == gt  and st_name not in name_lst:#
                addDirPlayable(st_name,gt,125,thumb,par,"", "", "lst")

    setView('episodes', 'episodes-view')
    if SORT_ALPHA:    
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	
def favourites():
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url='http://www.filmon.com/api/favorites?session_key=%s&run=get'% (session_id)
    link = open_url(url)
    all_channels = regex_from_to(link, 'result":', ',"reason')
    channel_ids = regex_get_all(all_channels, '"channel"', '}')
    for id in channel_ids:
        channel_id = regex_from_to(id, '"id":', ',')
        title = regex_from_to(id, 'title":"', '",').encode("utf-8")
        if SHOW_ID:
            title="%s (%s)" % (title,channel_id)
        description = clean_file_name(regex_from_to(id, 'description":"', '",'), use_blanks=False)
        thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % channel_id
        addDirPlayable(title,channel_id,125,thumb,"",description, "", "fav")
        setView('episodes', 'episodes-view')
 
		
def add_fav(name, ch_id, iconimage):
    dialog = xbmcgui.Dialog()
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = 'http://www.filmon.com/api/favorites?session_key=%s&channel_id=%s&run=add'%(session_id,ch_id)
    link = open_url(url)
    text = regex_from_to(link, 'reason":"', '",').replace('"',' ')
    dialog.ok("Add Favourite",name.upper(),text.upper())  

def delete_fav(name, ch_id, iconimage):
    dialog = xbmcgui.Dialog()
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = 'http://www.filmon.com/api/favorites?session_key=%s&channel_id=%s&run=remove'%(session_id,ch_id)
    link = open_url(url)
    text = regex_from_to(link, 'reason":"', '",').replace('"',' ')
    dialog.ok("Remove Favourite",name.upper(),text.upper())
    xbmc.executebuiltin("Container.Refresh")
		
def tv_guide(name, url, iconimage):
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url='http://www.filmon.com/tv/api/tvguide/%s?session_key=%s' % (url, session_id)
    link = open_url(url)
    programmes = regex_get_all(link, '{', 'vendor_id')
    utc_now = datetime.datetime.now()
    for p in programmes:
        p_id = regex_from_to(p, 'programme":"', '"')
        try:
            try:
                start = regex_from_to(p, 'startdatetime":"', '"')
            except:
                start = regex_from_to(p, 'startdatetime":', ',"')
            start_time = datetime.datetime.fromtimestamp(int(start))
            print start_time
            end_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'enddatetime":"', '"')))
        except:
            start_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'startdatetime":', ',')))
            end_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'enddatetime":', ',')))
        description = regex_from_to(p, 'programme_description":"', '"')
        p_name = regex_from_to(p, 'programme_name":"', '"')
        allow_dvr = regex_from_to(p, 'allow_dvr":', ',')
        channel_id = regex_from_to(p, 'channel_id":', ',"')
        title = "%s - %s" % (start_time.strftime('%d %b %H:%M'),p_name)
        try:
            matchthumb = regex_from_to(p, 'type":"2"', 'cop')
            thumb = regex_from_to(matchthumb, 'url":"', '"').replace("\/", "/")
        except:
            thumb = iconimage
        if end_time > utc_now:
            if start_time < utc_now and end_time > utc_now:
                addDirPlayable('[COLOR cyan]' + title + '[/COLOR]',channel_id,125,thumb,"",description, start, "gd")
            else:
                if allow_dvr == "true":
                    addDirPlayable(title,channel_id,129,thumb,p_id,description, start, "gd")
                else:
                    addDirPlayable(title + "  [COLOR red](not recordable)[/COLOR]",channel_id,"",thumb,p_id,description, start, "gd")
            setView('episodes', 'episodes-view')

		
def play_filmon(name,url,iconimage,ch_id):
    plsource='FTV'
    GID = ch_id
    grpurl = url
    origname=name
    if url == "PAY TV" or url == "UK LIVE TV":
        parsplit = ch_id.split('<>')
        swap_ch = parsplit[0]
        swap_url = parsplit[1]
    else:
        swap_ch = ch_id

    if url == "PAY TV":
        url = ROOT_CH
    if url == "UK LIVE TV":
        url = ROOT_CH
    if len(url)>6:
        url=ch_id	
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s%s%s" % (base_url, 'api/channel/', url, '?session_key=', session_id)
    utc_now = datetime.datetime.now()
    channel_name=name.upper()
    try:
        link = open_url(url)
    except:
        url = "%s%s%s%s%s" % (base_url, 'api/channel/', ROOT_CH, '?session_key=', session_id)
        plsource='GUIDE'
        link = open_url(url)
    nowplaying = regex_from_to(link, 'tvguide":', 'upnp_enabled')
    pr_list = regex_get_all(nowplaying, '{"programme', '}')
    for p in pr_list:
        programme_name = regex_from_to(p, 'programme_name":"', '",')
        try:
            start_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'startdatetime":"', '",')))
            end_time = datetime.datetime.fromtimestamp(int(regex_from_to(p, 'enddatetime":"', '",')))
            if start_time < utc_now and end_time > utc_now:
                npet = regex_from_to(p, 'enddatetime":"', '",')
                programme_name = regex_from_to(p, 'programme_name":"', '",')
                description = regex_from_to(nowplaying, 'programme_description":"', '",').replace('\u2019', "'").replace('\u2013', "-")
                start_t = start_time.strftime('%H:%M')
                end_t = end_time.strftime('%H:%M')
                p_name = "%s (%s-%s)" % (programme_name, start_t, end_t)
                if grpurl != "UK LIVE TV" and grpurl != "PAY TV" and plsource!='GUIDE':
                    dp.update(50, p_name)
                try:
                    next = regex_from_to(nowplaying, 'startdatetime":"' +npet, '}')
                    n_start_time = datetime.datetime.fromtimestamp(int(npet))
                    n_end_time = datetime.datetime.fromtimestamp(int(regex_from_to(next, 'enddatetime":"', '",')))
                    n_programme_name = regex_from_to(next, 'programme_name":"', '",')
                    n_start_t = n_start_time.strftime('%H:%M')
                    n_end_t = n_end_time.strftime('%H:%M')
                    n_p_name = "[COLOR cyan]Next: %s (%s-%s)[/COLOR]" % (n_programme_name, n_start_t, n_end_t)
                except:
                    n_p_name = ""
        except:
            p_name = programme_name
            n_p_name = ""
    streamlink=regex_from_to(link, '"streams":', ']}')
    if not '"quality":"low"' in streamlink:
        streams = re.compile('"id":(.+?),"quality":"high","url":"(.+?)","name":"(.+?)","is_adaptive":(.+?),"watch-timeout":(.+?)}').findall(streamlink)
    else:
        streams = re.compile('"id":(.+?),"quality":"low","url":"(.+?)","name":"(.+?)","is_adaptive":(.+?),"watch-timeout":(.+?)}').findall(streamlink)
    for id,url,name,adaptive,wt in streams:
        url = url.replace("\/", "/")
        name = name
        id=id
        if not '=' in url:
            url=url+name		
        if name.endswith('m4v'):
            app = 'vodlast'
        else:#rtmp://204.107.26.234/live/?
            if  not '=' in url:
                app='NA'
            else:
                app='live/?id=' + url.split('=')[1]
    swapout_url = regex_from_to(url,'rtmp://','/')
    if grpurl == "UK LIVE TV":
        name = name.replace(ROOT_CH, swap_ch)
        url=url.replace(swapout_url,swap_url)
    if grpurl == "PAY TV":
        name = name.replace(ROOT_CH, swap_ch)
        url=url.replace(swapout_url,swap_url)
    if plsource=='GUIDE':
        # read from channel list
        s = read_from_file(channel_list)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                st_grp = list1[0]
                st_name = list1[1]
                st_id = list1[2]
                st_url = list1[3]
                par = "%s<>%s" % (st_id, st_url)
                thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(st_id).rstrip()
                if st_id == GID:
                    name = name.replace(ROOT_CH, st_id)
                    url=url.replace(swapout_url,st_url)

    if FILMON_QUALITY == '480p':
        name = name.replace('low','high')

    if app=='NA':
        STurl = str(url) + ' playpath=' + name + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf' + ' tcUrl=' + url + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'
    else:
        STurl = str(url) + ' playpath=' + name + ' app=' + app + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf' + ' tcUrl=' + url + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    if grpurl=='UK LIVE TV' or grpurl=='PAY TV' or plsource=='GUIDE' or len(pr_list)==0:
        listitem = xbmcgui.ListItem(origname, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
    else:
        listitem = xbmcgui.ListItem(p_name + ' ' + n_p_name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
    if handle != "-1":	
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(STurl,listitem)	
    dp.close()
	
def non_geo():
    list = read_from_file(xml_list)
    all_streams = regex_get_all(list, '<stream>', '</stream>')
    for s in all_streams:
        title = regex_from_to(s, '<title>', '</title>').replace(' [Borg TV Update]', '')
        name = regex_from_to(s, '<playpath>', '</playpath>')
        link = regex_from_to(s, '<link>"', '"</link>')
        ch_id=name.split('.')[0]
        thumb = 'http://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(ch_id)#+ '.mp4' + advpp
        addDirPlayable(title,ch_id,111,thumb,link,"", "", "ng")
		
def add_ng(title,ch_id,link):
    grp_texts = []
    dialog = xbmcgui.Dialog()
    s = read_from_file(group_list)
    grp_list = s.split('\n')
    for grp in grp_list:
        grp_texts.append(grp)
		
    menu_id = dialog.select('Select Group', grp_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    else:	
        grpname = grp_texts[menu_id]
        list_data = "%s<>%s<>%s<>%s" % (grpname, title, ch_id, link)
        add_to_list(list_data, channel_list)
        notification(title + ' added to:', grpname, '5000', iconart)

def play_ng(name,url,iconimage,link):
    chname=name
    ng_link=link
    ng_id=url
    url=ROOT_CH
    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    url = "%s%s%s%s%s" % (base_url, 'api/channel/', url, '?session_key=', session_id)
    utc_now = datetime.datetime.now()
    channel_name=name.upper()
    link = open_url(url)
    streams = re.compile('"id":(.+?),"quality":"high","url":"(.+?)","name":"(.+?)","is_adaptive":(.+?),"watch-timeout":(.+?)}').findall(link)
    for id,url,name,adaptive,wt in streams:
        url = url.replace("\/", "/")
        name = name
        id=id
        if name.endswith('m4v'):
            app = 'vodlast'
        elif '=' in url:
            app='live/?id=' + url.split('=')[1]
        elif '?' in name:
            app='live/?id=' + name.split('?')[1]
            name=name.split('?')[0].replace('mp4:','')
        else:app="no_app"
    name = name.replace(ROOT_CH, ng_id)
    print app,ng_link
    url = "%s/%s" % (ng_link.replace(':1935',''),app.replace('live/live/','live/'))
    if FILMON_QUALITY == '480p':
        name = name.replace('low','high')
    if app=="no_app":
        STurl = str(url) + ' playpath=' + name + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf' + ' tcUrl=' + url + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'
    else:		
        STurl = str(url) + ' playpath=' + name + ' app=' + app + ' swfUrl=http://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf' + ' tcUrl=' + url + ' pageUrl=http://www.filmon.com/' + ' live=1 timeout=45 swfVfy=1'
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    listitem = xbmcgui.ListItem(chname, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
    if handle != "-1":	
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(STurl,listitem)	
    dp.close()	

def record_programme(name,ch_id,p_id,start):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Record Programme?", '', name.upper()):
        session_id = xbmcgui.Window(10000).getProperty("session_id")
        rec_url ='http://filmon.com/api/dvr-add?session_key=%s&channel_id=%s&programme_id=%s&start_time=%s' % (session_id,ch_id,p_id,start)
        link = open_url(rec_url)
        text = regex_from_to(link, 'reason":"', '"}').replace('"',' ')
        dialog = xbmcgui.Dialog()
        dialog.ok("Record Programme",name.upper(),text.upper())
		
def delete_recording(name,start,iconimage):
    dialog = xbmcgui.Dialog()
    if dialog.yesno("Delete Recording?", '', name.upper()):
        session_id = xbmcgui.Window(10000).getProperty("session_id")
        rec_url ='http://filmon.com/api/dvr-remove?session_key=%s&recording_id=%s' % (session_id, start)
        link = open_url(rec_url)
        text = regex_from_to(link, 'reason":"', '"}').replace('"',' ')
        dialog = xbmcgui.Dialog()
        dialog.ok("Delete Recording",name.upper(),text.upper())
        xbmc.executebuiltin("Container.Refresh")

	
def recordings(url):
    session_id = xbmcgui.Window(10000).getProperty("session_id")
    recs_url='http://www.filmon.com/api/dvr-list?session_key=%s'%(session_id)
    link = open_url(recs_url)
    match = re.compile('"permanent":"(.+?)","subscribed":(.+?),"recorded":(.+?),"total":(.+?),"available":(.+?)}').findall(link)
    for p,s,r,t,a in match:
        acc_status = "Allowed: %shrs - Recorded: %shrs - Available %shrs" % (t, r, a)
    addLink('[COLOR cyan]'+acc_status+'[/COLOR]',"","","","","", "", "", "")
    recordings = regex_get_all(link, '"id":"', 'is_deleted"')
    for r in recordings:
        STurl = regex_from_to(r, 'stream_url":"', '",').replace("\/", "/")
        STname = regex_from_to(r, 'stream_name":"', '",').replace("\/", "/")
        p_id = regex_from_to(r, 'id":"', '",')
        p_name = regex_from_to(r, 'title":"', '",')
        description = regex_from_to(r, 'description":"', '",')
        channel_id = regex_from_to(r, 'channel_id":"', '",')
        logo = 'https://static.filmon.com/couch/channels/%s/extra_big_logo.png' % str(channel_id)
        start = regex_from_to(r, 'time_start":"', '",')
        start_time = datetime.datetime.fromtimestamp(int(regex_from_to(r, 'time_start":"', '",')))
        duration = regex_from_to(r, 'duration":"', '",')
        status = regex_from_to(r, 'status":"', '",')
        try:
            download_link = regex_from_to(r,'download_url":"','"').replace('\/','/')
        except:
            download_link = "error"
        print download_link
        text = "[COLOR gold]%s[/COLOR] %s (%s) [COLOR cyan]Dur[%s][/COLOR]" % (p_name, start_time.strftime('%d %b %H:%M'), status,duration)
        addLink(text,STurl,logo,description,status,download_link, p_id, start,p_name)
        setView('episodes', 'episodes-view')

def download_rec(name, url, iconimage):
    WAITING_TIME = 5
    directory=DOWNLOAD_PATH
    filename = "%s.%s" % (name, url[len(url)-3:])
    data_path = os.path.join(directory, filename)
    dlThread = DownloadThread(name, url, data_path)
    if directory == "notset" or directory == "":
        xbmcgui.Dialog().ok('Download directory not set', 'Set your download path in settings first')
        ADDON.openSettings()
    else:
        dlThread.start()
        wait_dl_only(WAITING_TIME, "Starting Download")
        if os.path.exists(data_path):
            notification('FilmOn.TV - Download started', name.upper(), '5000', iconart)
        else:
            notification('FilmOn.TV - Download failed', name.upper(), '5000', iconart)
       

class DownloadThread(Thread):
    def __init__(self, name, url, data_path):
        self.data = url
        self.path = data_path
        Thread.__init__(self)

    def run(self):
        path = str(self.path)
        data = self.data
        urllib.urlretrieve(data, path)
        notification('FilmOn.TV - Download finished', name.upper(), '5000', iconart)
        xbmc.executebuiltin(notify)	
		
def on_demand()	:
    url = "http://www.filmon.com/vod/documentary"
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)#id,vid,title,slug,pos,ccount
    match=re.compile('{"id":"(.+?)","vendorka_id":"(.+?)","name":"(.+?)","slug":"(.+?)","position":"(.+?)","content_count":"(.+?)","updated_at":"').findall(link)
    for id,vid,title,slug,pos,ccount in match:
        url = slug + '<>0'
        thumb = "http://static.filmon.com/couch/genres/%s/image.png" % slug
        addDir(title,url,201,thumb, '','')
        setView('episodes', 'episodes-view')

def on_demand_list(url):
    urlsplit=url.split('<>')
    genre = urlsplit[0]
    startindex=urlsplit[1]
    nextindex=int(startindex) + 16
    if startindex == '0':
        featuredurl = 'http://www.filmon.com/api/vod/search?genre=%s&is_featured=1&max_results=8&start_index=0' % genre
        link = net.http_GET(featuredurl).content.encode("utf-8").rstrip()
        all_videos = regex_get_all(link, '"id":', 'is_synchronized')
        for a in all_videos:
            title = regex_from_to(a, 'title":"', '"')
            id = regex_from_to(a, 'id":', ',"')
            thumb = 'http://static.filmon.com/couch/vod_content/%s/thumb_220px.png' % id
            plot = regex_from_to(a, 'description":"', '"')
            slug = regex_from_to(a, 'slug":"', '"')
            url = "%s<>%s" % (id,slug)
            if ' Series' in title:
                addDir(title,url,202,thumb, '',plot)
            else:
                addDirPlayable(title,url,203,thumb,"",plot, "", "od")
	
    url = 'http://www.filmon.com/api/vod/search?genre=%s&max_results=16&noepisode=1&start_index=%s' % (genre,startindex)
    np_url = "%s<>%s" % (genre, nextindex)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_videos = regex_get_all(link, '"id":', 'is_synchronized')
    for a in all_videos:
        title = regex_from_to(a, 'title":"', '"')
        id = regex_from_to(a, 'id":', ',"')
        thumb = 'http://static.filmon.com/couch/vod_content/%s/thumb_220px.png' % id
        plot = regex_from_to(a, 'description":"', '"')
        slug = regex_from_to(a, 'slug":"', '"')
        url = "%s<>%s" % (id,slug)
        if ' Series' in title:
            addDir(title,url,202,thumb, '',plot)
        else:
            addDirPlayable(title,url,203,thumb,"",plot, "", "od")
    addDir("[COLOR gold]>> Next Page[/COLOR]",np_url,201,xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'next.png')), '','')
    setView('episodes', 'episodes-view')
	
def on_demand_series_list(name,url,iconimage):
    playlist = []
    id = url.split('<>')[0]
    slug = url.split('<>')[1]
    url = 'http://www.filmon.com/api/vod/movie?id=%s' % slug
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    eplink = regex_from_to(link, 'episodes":', ',"type').replace('"','').replace('[','').replace(']','')
    url = "http://www.filmon.com/api/vod/movies?ids=%s" % eplink
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    all_s = regex_get_all(link, '"id', '}')
    for s in all_s:
        plot = regex_from_to(s, '"description":"', '",')
        title = regex_from_to(s, '"title":"', '",')
        id = regex_from_to(s, 'id":', ',"')
        slug = regex_from_to(s, '"slug":"', '",')
        url = "%s<>%s" % (id,slug)
        thumb = thumb = 'http://static.filmon.com/couch/vod_content/%s/thumb_220px.png' % id
        addDirPlayable(title,url,203,thumb,"",plot, "", "od")
    setView('episodes', 'episodes-view')
	
def play_od(name, url, iconimage):

    playlist = []
    id = url.split('<>')[0]
    slug = url.split('<>')[1]
    url = 'http://www.filmon.com/api/vod/movie?id=%s' % id

    dp = xbmcgui.DialogProgress()
    dp.create('Opening ' + name.upper())
    net.set_cookies(cookie_jar)
    link = net.http_GET(url).content.encode("utf-8").rstrip()
    low = regex_from_to(link, '"low"', '}')
    lowurl = regex_from_to(low, '"url":"', '"').replace('\/', '/')
    high = regex_from_to(link, '"high"', 'watch-timeout')
    highurl = regex_from_to(high, '"url":"', '"').replace('\/', '/')
    try:
        timeout = regex_from_to(link, '"HD","watch-timeout":', "}")
    except:
        timeout = '86500'
    timeout = int(timeout)
	
    if FILMON_QUALITY == '480p' and (AUTO_SWITCH == False or timeout > 1800):
        STurl = highurl
    else:
        STurl = lowurl
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    handle = str(sys.argv[1])
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=STurl)
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(STurl,listitem)
    dp.close()

 
def play(name, url, iconimage):  
    link = open_url(url)
    match = re.compile('src="(.+?)" FlashVars="controlbar=over&skin=(.+?)&bufferlength=(.+?)&autostart=(.+?)&fullscreen=(.+?)&file=(.+?)&height').findall(link)
    for swf, nonswf, buffer, autostart, fullscreen, rtmp in match:
        stream_url = rtmp + ' swfUrl=' + swf + ' live=true timeout=45'
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)

		
def disney_jr(url):
    link = open_url(url)#.replace('\n','')
    categories = regex_get_all(link, '<li class="video_brand_promo">', '</li>')
    for c in categories:
        url = 'http://www.disney.co.uk' + regex_from_to(c, 'href="', '"')
        name = regex_from_to(c, 'data-originpromo="', '"').replace('-',' ').upper()
        thumb = 'http://www.disney.co.uk' + regex_from_to(c, 'data-hover="', '"')
        if name == 'A POEM IS HOME IN THE FASHION':
            thumb = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', 'art', 'disney_junior.jpg'))
        addDir(name,url,302,thumb, '','')
		
def disney_jr_links(name, url):
    link = open_url(url).replace('\t', '').replace('\n', '')
    videos = regex_get_all(link, 'div class="promo" style', 'img src="/cms_res/disney-junior/images/promo')
    for v in videos:
        url = 'http://www.disney.co.uk' + regex_from_to(v, 'href="', '"')
        name = regex_from_to(v, 'data-itemName="', '"').replace('-',' ').upper()
        thumb = 'http://www.disney.co.uk' + regex_from_to(v, 'img src="', '"')
        addDirPlayable(name,url,310,thumb,'', '', '', 'djr')
	
def disney_play(name, url, iconimage):
    urlid = url.replace('http://www.disney.co.uk/disney-junior/content/video.jsp?v=','')
    link = open_url(url)
    stream = regex_from_to(link, urlid, 'progressive')
    server = regex_from_to(stream,'server":"', '"')
    strm = regex_from_to(stream, 'program":"', '"')
    url = server + strm + ' swfVfy=1'
    title = regex_from_to(stream, 'pageTitle":"', '"').replace('Disney Junior | Videos - ', '')
    liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player().play(pl)
	
def disney_playlist(name, url, iconimage):
    dp = xbmcgui.DialogProgress()
    dp.create("FilmOn.TV",'Creating Playlist')
    playlist = []
    link = open_url(url)
    stream = regex_get_all(link, 'analyticsAssetName', 'progressive')
    nItem = len(stream)
    for s in stream:
        server = regex_from_to(s,'server":"', '"')
        strm = regex_from_to(s, 'program":"', '"')
        url = server + strm + ' swfVfy=1'
        title = regex_from_to(s, 'pageTitle":"', '"').replace('Disney Junior | Videos - ', '')
        liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": title} )
        liz.setProperty("IsPlayable","true")
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        playlist.append((url, liz))
        progress = len(playlist) / float(nItem) * 100  
        dp.update(int(progress), 'Adding to Your Playlist',title)

        if dp.iscanceled():
            return
    dp.close()
    for blob ,liz in playlist:
        try:
            if blob:
                pl.add(blob,liz)
        except:
            pass
    if not xbmc.Player().isPlayingVideo():
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(pl)
		
def youtube_videos(name,url,iconimage):
    find_url=url.find('?')+1
    keep_url=url[:find_url]
    
    iconimage=""
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(link,"<entry>(.*?)</entry>")
    
    for entry in matches:
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>").replace("&amp;","&")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([^\&]+)\&").replace("&amp;","&")
        play_url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        plugintools.add_item( action="play" , title=title , plot=plot , url=play_url ,thumbnail=thumbnail , folder=True )
    
    # Calculates next page URL from actual URL
    start_index = int( plugintools.find_single_match( link ,"start-index=(\d+)") )
    max_results = int( plugintools.find_single_match( link ,"max-results=(\d+)") )
    next_page_url = keep_url+"start-index=%d&max-results=%d" % ( start_index+max_results , max_results)

    addDir(">> Next page",next_page_url,395,"",'','')
		
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
		
def list_favourites(name, url, iconimage):
    if  'Movies' in name:
        dir = FAV_MOV
    else:
        dir = FAV_CHAN
    if os.path.isfile(dir):
        s = read_from_file(dir)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url1 = list1[2]
                thumb = urllib.unquote(list1[1])
                url = urllib.unquote(regex_from_to(url1, 'url=', 'mode').replace('&', ''))
                mode = regex_from_to(url1, 'mode=', 'iconimage').replace('&', '')
                try:
                    start = regex_from_to(url1, 'channel/', 'mode').replace('&', '')
                except:
                    start = ''
                if dir == FAV_CHAN:
                    ch_id = url1[url1.find('ch_fanart='):]
                    ch_id = ch_id.replace('ch_fanart=','')#channel/
                else:
                    ch_id = ''
                addDirPlayable(title,url,mode,thumb,ch_id,'', start, 'favlist')
                #addLink(title,url,thumb,list,'','', '', '', '')

def add_favourite(name, url, iconimage, ch_id, dir,text):
    ch_name = name
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    ch_id = urllib.quote(str(ch_id))
    if 'rtmp' in url:
        url = sys.argv[0] + '?name=%s&url=%s&mode=111&iconimage=%s' % (name, url, iconimage)
    else:
        url = sys.argv[0] + '?name=%s&url=%s&mode=125&iconimage=%s&ch_fanart=%s' % (name, url, iconimage,ch_id)
    data = "%s<>%s<>%s" % (ch_name, iconimage, url)
    add_to_list(data, dir)
    notification(ch_name, "[COLOR lime]" + text + "[/COLOR]", '5000', iconimage)
	
def add_favourite_movie(name, url, iconimage, ch_id, dir,text):#play_ng(name,url,iconimage)
    ch_name = name
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    url = sys.argv[0] + '?name=%s&url=%s&mode=111&iconimage=%s' % (name, url, iconimage)
    data = "%s<>%s<>%s" % (ch_name, iconimage, url)
    add_to_list(data, dir)
    notification(ch_name, "[COLOR lime]" + text + "[/COLOR]", '5000', iconimage)
	
def remove_favourite(name, url, iconimage, ch_fanart,text):
    ch_name = name
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    ch_id = urllib.quote(str(ch_fanart))
    if ch_fanart == '':
        dir = FAV_MOV
        url = sys.argv[0] + '?name=%s&url=%s&mode=111&iconimage=%s' % (name, url, iconimage)
    else:
        dir = FAV_CHAN
        url = sys.argv[0] + '?name=%s&url=%s&mode=125&iconimage=%s&ch_fanart=%s' % (name, url, iconimage,ch_id)
    data = "%s<>%s<>%s" % (ch_name, iconimage, url)
    remove_from_list(data, dir)
    notification(ch_name, "[COLOR lime]" + text + "[/COLOR]", '5000', urllib.unquote(iconimage))
	
def add_to_file(path, content, append=True, silent=False):
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

def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
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
	
def remove_from_list(list, file):
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

		
def create_strm_file(name, url, mode, dir_path, iconimage):
    strm_string = create_url(name, mode, url=url, iconimage=iconimage)
    #name1 = re.sub(r'\[[^]]*\]', '', name1)
    filename = clean_file_name("%s.strm" % name)
    path = os.path.join(dir_path, filename)
    if not os.path.exists(path):
        stream_file = open(path, 'w')
        stream_file.write(strm_string)
        stream_file.close()
        scan_library()

		
def create_url(name, mode, url, iconimage):
    name = urllib.quote(str(name))
    url = urllib.quote(str(url))
    iconimage = urllib.quote(str(iconimage))
    mode = str(mode)
    url = sys.argv[0] + '?name=%s&url=%s&mode=%s&iconimage=%s' % (name, url, mode, iconimage)
    return url
	
def download_only(name,url,iconimage,dir_path):
    filename = name + '.mp4'
    WAITING_TIME = 5
    directory=dir_path
    data_path = os.path.join(directory, filename)
    dlThread = DownloadFileThread(name, url, data_path, WAITING_TIME)
    dlThread.start()
    wait_dl_only(WAITING_TIME, "Starting Download")
    if os.path.exists(data_path):
        notification('Download started', name, '5000', iconimage)
        scan_library()
		
class DownloadFileThread(Thread):
    def __init__(self, name, url, data_path, WAITING_TIME):
        self.data = url
        self.path = data_path
        self.waiting = WAITING_TIME
        self.name = name
        Thread.__init__(self)

    def run(self):
        start_time = time.time() + 20 + self.waiting
        waiting = self.waiting
        path = self.path
        data = self.data
        name = self.name
        urllib.urlretrieve(data, path)

        notification('Download finished', name, '5000', iconart)
		
    def _dlhook(self, numblocks, blocksize, filesize, dt, start_time, path, waiting):
        raise StopDownloading('Stopped Downloading')
        callEndOfDirectory = False
		
class StopDownloading(Exception): 
    def __init__(self, value): 
        self.value = value 
    def __str__(self): 
        return repr(self.value)
		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
		
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
		
def scan_library():
    if xbmc.getCondVisibility('Library.IsScanningVideo') == False:           
        xbmc.executebuiltin('UpdateLibrary(video)')
		
link = open_url(session_url)
session_key = regex_from_to(link, 'session_key":"', '"')


def cleanlink(link):
    data=link.replace('\u00a0',' ').replace('\u00ae','').replace('\u00e9','').replace('\u00e0','').replace('\u2013','').replace('\u00e7','').replace('\u00f1','')
    return data
   

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

def addLink(name,url,iconimage,description,status,download_link, p_id, start, p_name):
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        contextMenuItems.append(("Delete Recording",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=133&iconimage=%s)'%(sys.argv[0],p_name,str(p_id),iconimage)))
        if status == "Recorded" and download_link != "error":
            contextMenuItems.append(("Download Recording",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=139&iconimage=%s)'%(sys.argv[0],p_name,str(download_link),iconimage)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage,ch_fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&ch_fanart="+urllib.quote_plus(ch_fanart)+"&description="+str(description)
        ok=True
        contextMenuItems = []
        contextMenuItems.append(('Hide Channel Group', 'XBMC.RunPlugin(%s?mode=10&url=%s)'% (sys.argv[0],str(name))))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.addContextMenuItems(contextMenuItems, False)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
	
def addDirPlayable(name,url,mode,iconimage,ch_fanart, description, start, function):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&start="+str(start)+"&ch_fanart="+str(ch_fanart)
        ok=True
        contextMenuItems = []
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        if function=="grp":
            contextMenuItems.append(("Add to Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=135&iconimage=%s)'%(sys.argv[0],name,url,iconimage)))
        if function=="fav":
            contextMenuItems.append(("Remove from Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=137&iconimage=%s)'%(sys.argv[0],name,url,iconimage)))
        if function != 'od' and function != 'gb'and function != 'djr' and function != 'ng' and function != '' and function != 'favlist':
            contextMenuItems.append(("TV Guide",'XBMC.Container.Update(%s?name=%s&url=%s&mode=127&iconimage=%s)'%(sys.argv[0],urllib.quote(name), url,iconimage)))
            contextMenuItems.append(("Add to FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=410&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))
        if function == 'favlist':
            contextMenuItems.append(("Remove from FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=416&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))
        if function == 'ng':
            contextMenuItems.append(("Add Channel to Group",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=112&iconimage=%s)'%(sys.argv[0],urllib.quote(start), str(ch_fanart),str(description))))
            contextMenuItems.append(("Add to FTV Favourites",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=410&iconimage=%s&ch_fanart=%s)'%(sys.argv[0],urllib.quote(name),urllib.quote(url),urllib.quote(iconimage),ch_fanart)))
	
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
              
params=get_params()

url=None
name=None
mode=None
iconimage=None



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
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        ch_fanart=urllib.unquote_plus(params["ch_fanart"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass


if mode==None or url==None or len(url)<1:
        CATEGORIES()
        
       
elif mode==121:
        other_menu()
		
elif mode==122:
        favourites()
		
elif mode==110:
        non_geo()
		
elif mode==151:
        featured()
		
elif mode==15:
        play(name, url, iconimage)
		
elif mode==2:
        other()
		
elif mode == 10:
        print "MODE " + url
        add_to_list(url, HIDDEN_FILE)
		
elif mode==123:
        group_channels(url, name,ch_fanart,description)
		
elif mode==125:
        play_filmon(name, url, iconimage, ch_fanart)
		
elif mode == 111:
        play_ng(name,url,iconimage,ch_fanart)
		
elif mode == 112:
        add_ng(name, url, iconimage)
		
elif mode==126:
        play_filmon_gb(name, url, iconimage)
		
elif mode==127:
        tv_guide(name, url, iconimage)
		
elif mode == 129:
        record_programme(name,url,ch_fanart,start)

elif mode == 131:
        recordings(url)
		
elif mode == 133:
        delete_recording(name,url,iconimage)
        recordings(url)
		
elif mode == 135:
        add_fav(name, url, iconimage)
		
elif mode == 137:
        delete_fav(name, url, iconimage)
		
elif mode == 139:
        download_rec(name, url, iconimage)

elif mode == 199:
        on_demand()

elif mode == 201:
        on_demand_list(url)
		
elif mode == 202:
        on_demand_series_list(name,url,iconimage)

elif mode == 203:
        play_od(name, url, iconimage)
		
elif mode == 395:
        youtube_videos(name,url,iconimage)
		
elif mode == 301:
        disney_jr(url)	

elif mode == 302:
        disney_jr_links(name, url)
		
elif mode == 303:
        disney_playlist(name, url, iconimage)

elif mode == 310:
        disney_play(name, url, iconimage)
		
elif mode==401:
        create_strm_file(name, url, '396', MOVIE_DIR, iconimage)

elif mode==402:
        create_all_strm_file(name, url, '396', MOVIE_DIR, iconimage)

elif mode==403:
        download_only(name, url, iconimage,MOVIE_DIR)

elif mode == 410:
    add_favourite(name, url, iconimage, ch_fanart, FAV_CHAN,"Added to Favourites")

elif mode == 411:
    add_favourite_movie(name, url, iconimage, "", FAV_MOV,"Added to Favourites")
	
elif mode == 416:
    remove_favourite(name, url, iconimage, ch_fanart,"Removed from Favourites")

elif mode == 415:
    list_favourites(name, url, iconimage)

elif mode == 417:
    play_favourites(name, url, iconimage)	

xbmcplugin.endOfDirectory(int(sys.argv[1]))
