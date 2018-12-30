# -*- coding: utf-8 -*-

import re
import urllib2
import HTMLParser
import urllib,urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from BeautifulSoup import BeautifulSoup as bs
from utils.webutils import *
from scrapers import *



try:
    from addon.common.addon import Addon

    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("Import Failure", "Failed to import addon.common", "A component needed by P2P Sport is missing on your system", "Please visit www.tvaddons.ag.com for support")




base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
params=urlparse.parse_qs(sys.argv[2][1:])

addon = Addon('plugin.video.p2psport', sys.argv)
AddonPath = addon.get_path()


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

my_addon = xbmcaddon.Addon()



if mode is None:


    url = build_url({'mode': 'av'})
    li = xbmcgui.ListItem('Arenavision.in',iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'roja'})
    li = xbmcgui.ListItem('Rojadirecta.me',iconImage='http://www.rojadirecta.me/static/roja.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'ws'})
    li = xbmcgui.ListItem('Livefootball.ws',iconImage='http://www.userlogos.org/files/logos/clubber/football_ws___.PNG')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'livefootballvideo.com'})
    li = xbmcgui.ListItem('Livefootballvideo.com',iconImage='https://pbs.twimg.com/profile_images/3162217818/2ee4b2f728ef9867d4e1d86e17bb2ef5.jpeg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'livefooty'})
    li = xbmcgui.ListItem('Livefootballol.com',iconImage='http://www.livefootballol.com/images/logo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)



    # url = build_url({'mode': 'livefootF1'})
    # li = xbmcgui.ListItem('Livefootballol.com (F1)',iconImage='http://www.livefootballol.com/images/logo.png')
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    #                             listitem=li, isFolder=True)

    url = build_url({'mode': 'phace'})
    li = xbmcgui.ListItem('Sport Channels 1',iconImage='http://cdn.streamcentral.netdna-cdn.com/images/software/acestreamlogo.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'serbplus'})
    li = xbmcgui.ListItem('Sport Channels 2',iconImage='http://cdn.streamcentral.netdna-cdn.com/images/software/acestreamlogo.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'ttv', 'url':'http://livehdstreams.com/trash/ttv-list/ttv.sport.player.m3u'})
    li = xbmcgui.ListItem('Sport Channels 3',iconImage='http://cdn.streamcentral.netdna-cdn.com/images/software/acestreamlogo.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': '1ttv'})
    li = xbmcgui.ListItem('1torrent.tv',iconImage='http://s3.hostingkartinok.com/uploads/images/2013/06/6e4452212490ac0a66e358c97707ef77.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'ttv_sport', 'url':'http://livehdstreams.com/trash/ttv-list/ttv.sport.player.m3u'})
    li = xbmcgui.ListItem('Torrent-tv.ru (Sport)',iconImage='http://addons.tvaddons.ag/cache/images/bc591d6d5ec442d4ddb43a347a8be6_icon.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'ttv_all', 'url':'http://livehdstreams.com/trash/ttv-list/ttv.sport.player.m3u'})
    li = xbmcgui.ListItem('Torrent-tv.ru',iconImage='http://addons.tvaddons.ag/cache/images/bc591d6d5ec442d4ddb43a347a8be6_icon.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    # url = build_url({'mode': 'soccer188'})
    # li = xbmcgui.ListItem('Soccer188',iconImage='')
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    #                             listitem=li, isFolder=True)

    # url = build_url({'mode': '247'})
    # li = xbmcgui.ListItem('Livesports 24/7',iconImage='http://i.imgur.com/Mv5ySt4.jpg')
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    #                             listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='streamhub':
    streamhub_cats()
elif mode[0]=='open_streamhub_cat':
    url=params['url'][0]
    open_streamhub_cat(url)
elif mode[0]=='open_streamhub_event':
    url=params['url'][0]
    open_streamhub_event(url)


elif mode[0]=='soccer188':
    soccer188()
elif mode[0]=='play_sopc':
    url=params['url'][0]
    name=params['name'][0]
    play_sop(url,name)

elif mode[0]=='ttv_sport':
    ttv_sport()
elif mode[0]=='serbplus':
    serbplus()
elif mode[0]=='play_serb':
    url=params['url'][0]
    name=params['name'][0]
    resolve_roja(url,name)

elif mode[0]=='phace':
    phace()
elif mode[0]=='247':
    url = build_url({'mode': 'schedule_247'})
    li = xbmcgui.ListItem('Event schedule',iconImage='http://i.imgur.com/Mv5ySt4.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'all_247'})
    li = xbmcgui.ListItem('All channels',iconImage='http://i.imgur.com/Mv5ySt4.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_247_event':
    url=params['url'][0]
    open_247_event(url)
elif mode[0]=='all_247':
    all_live247()

elif mode[0]=='schedule_247':
    schedule247()

elif mode[0]=='open_247_stream':
    url='http://pilkalive.weebly.com'+params['url'][0]
    name=params['name'][0]
    play247(url,name)

elif mode[0]=='livefootballvideo.com':
    livefoot_com()

elif mode[0]=='ttv_all':
    ttv_cats()
elif mode[0]=='open_ttv_cat':
    cat=params['cat'][0]
    tag=params['channels'][0]
    get_ttv_cat(cat,tag)

elif mode[0]=='1ttv':
    one_ttv_cats()

elif mode[0]=='open_1ttv_cat':
    tag=params['tag'][0]
    name=params['name'][0]
    open_1ttv_cat(tag,name)

elif  mode[0]=='open_1ttv_channel':
    url=params['url'][0]
    open_1ttv_channel(url)

elif mode[0]=='ws':
    livefootballws_events()

elif mode[0]=='roja':
    rojadirecta_events()

elif mode[0]=='ttv':
    get_ttv()


elif mode[0]=='open_ttv_stream':
    url=params['url'][0]
    name=params['name'][0]
    open_ttv_stream(url,name)
elif mode[0]=='av':
    url = build_url({'mode': 'av_schedule'})
    li = xbmcgui.ListItem('[COLOR orange]Schedule / Agenda[/COLOR]',iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    for i in range(10):
        url = build_url({'mode': 'av_ace','url':'av%s'%(str(i+1)), 'name':'Arenavision %s'%(i+1)})
        li = xbmcgui.ListItem('Arenavision %s'%(i+1),iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    for i in range(11,13):
        url = build_url({'mode': 'av_rand','url':'av%s'%(str(i+1)), 'name':'Arenavision %s'%(i)})
        li = xbmcgui.ListItem('Arenavision %s'%(i),iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    for i in range(13,23):
        url = build_url({'mode': 'av_sop','url':'av%s'%(str(i+1)), 'name':'Arenavision %s'%(i)})
        li = xbmcgui.ListItem('Arenavision %s'%(i),iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    for i in range(23,25):
        url = build_url({'mode': 'av_rand','url':'av%s'%(str(i+1)), 'name':'Arenavision %s'%(i)})
        li = xbmcgui.ListItem('Arenavision %s'%(i),iconImage='http://kodi.altervista.org/wp-content/uploads/2015/07/arenavision.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='av_ace':
    url='http://arenavision.in/'+params['url'][0]
    name=params['name'][0]
    try:
        play_arena(url,name)
    except:
        play_arena_sop(url,name)

elif mode[0]=='av_sop':
    url='http://arenavision.in/'+params['url'][0]
    name=params['name'][0]
    try:
        play_arena_sop(url,name)
    except:
        play_arena(url,name)
elif mode[0]=='av_rand':
    url='http://arenavision.in/'+params['url'][0]
    name=params['name'][0]
    try:
        play_arena(url,name)
    except:
        play_arena_sop(url,name)
elif mode[0]=='open_roja_stream':
    url='http://www.rojadirecta.me/'+params['url'][0]
    name=params['name'][0]
    resolve_roja(url,name)

elif mode[0]=='av_schedule':
    arenavision_schedule()

elif mode[0]=='av_open':
    channels=((params['channels'][0]).replace('[','').replace(']','').replace("'",'').replace('u','').replace(' ','')).split(',')
    name=params['name'][0]
    sources=[]
    for i in range(len(channels)):
        title='AV%s'%channels[i]
        sources+=[title]
    dialog = xbmcgui.Dialog()
    index = dialog.select('Select a channel:', sources)

    if index>-1:
        url=sources[index]
        url='http://arenavision.in/'+url.lower()
        try: play_arena(url,name)
        except: play_arena_sop(url,name)


elif mode[0]=='livefooty':
    livefootballol()

elif mode[0]=='open_livefoot':
    url='http://www.livefootballol.com'+params['url'][0]
    name=params['name'][0]
    get_livefoot(url,name)

elif mode[0]=='open_livefoot_stream':
    url=params['url'][0]
    name=params['name'][0]
    play_livefoot(url,name)

elif mode[0]=='livefootF1':
    livefootF1()

elif mode[0]=='open_livefoot.com_stream':
    url=params['url'][0]
    name=params['name'][0]
    play_livefoot(url,name)
    open_com_event(name,url)

elif mode[0]=='open_ws_stream':
    url=params['url'][0]
    livefootballws_streams(url)