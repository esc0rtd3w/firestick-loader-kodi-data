# -*- coding: utf-8 -*-

import os,re,sys,urllib,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin

addon_id = 'plugin.video.spoxtv'
addon = xbmcaddon.Addon(id=addon_id)
home = addon.getAddonInfo('path').decode('utf-8')
iconimage = xbmc.translatePath(os.path.join(home, 'icon.png'))
pluginhandle = int(sys.argv[1])
quality_list = ['Niedrig','Hoch']
q = addon.getSetting('video_quality')
quality = quality_list[int(q)]

from resources.lib.client import Client
from resources.lib import helper

def categories():
    data = Client().get_categories()
    if data:
        items = helper.get_category_items(data)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def channels():
    id = args['id'][0]
    data = Client().get_categories()
    if data:
        items = helper.get_channel_items(data,id)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def videos():
    id = args['id'][0]
    total = args['total'][0]
    offset = args['offset'][0]
    data = Client().get_videos(id,offset,total)
    if data:
        items = helper.get_video_items(data)
        total = helper.get_video_items(data,get_total=True)
        items = helper.get_next_item(items,id,offset,total)
        list_items(items)
    xbmcplugin.endOfDirectory(pluginhandle)

def live_videos():
    all_items = []
    live_items = []
    result = Client().get_all_live_videos()
    if result:
        for data in result:
            items = helper.get_live_items(data)
            for i in items:
                if i['name'].startswith('[COLOR red]LIVE[/COLOR]'):
                    live_items.append(i)
                else:
                    all_items.append(i)
        all_items =  sorted(all_items, key=lambda k:k['name'])
        for x in live_items:
            all_items.insert(0,x)
        list_items(all_items)
    xbmcplugin.endOfDirectory(pluginhandle)

def play_video():
    id = args['id'][0]
    path = None
    if id.startswith('http') and 'm3u8' in id:
        path = select_quality(id,hls=True)
    elif id.startswith('rtmp'):
        path = id
    if path:
        listitem = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def play_live_video():
    id = args['id'][0]
    data = Client().get_live_stream(id)
    if data:
        path = helper.get_live_url(data,quality)
        if path:
            listitem = xbmcgui.ListItem(path=path)
            xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def get_hls_list(url):
    list = []
    data = Client().get_data(url)
    if data:
        pattern = 'bandwidth=(\d+)\s*,\s*resolution.*?\n(http://.*?)$'
        match = re.findall(pattern, data, re.I|re.M)
        if match:
            for b,u in match:
                list.append({'bandwidth':int(b), 'url':u})
            return list
    return [{'bandwidth':int('1'), 'url':url}]
        
def get_rtmp_list(content):
    list = []
    for i in content:
        list.append({'bandwidth':int(i['bitrate']), 'url':i['url']})
    return list

def select_quality(id,rtmp=False,hls=False):  
    if rtmp:
        list = get_rtmp_list(id)
    elif hls:
        list = get_hls_list(id)
    list = sorted(list, key=lambda k:k['bandwidth'])
    if quality == 'Niedrig':
        return list[len(list)//2]['url']
    if quality == 'Hoch':
        return list[-1]['url']

def list_items(items):
    for i in items:
        if i['type'] == 'dir':
            add_dir(i)
        elif i['type'] == 'video':
            add_video(i)

def add_dir(item):
    u = build_url({'mode':item['mode'], 'name':item['name'], 'id':item['id'], 'offset':item.get('offset', '1'), 'total':item.get('total', '6')})
    item=xbmcgui.ListItem(item['name'], iconImage="DefaultFolder.png", thumbnailImage=item.get('image', iconimage))
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=True)
    
def add_video(item):
    name = item['name']
    duration = item['duration']
    id = item['id']
    if 'rtmp://' in str(id) and item['mode'] == 'play_video':
        id = select_quality(id,rtmp=True)
    u = build_url({'mode': item['mode'], 'name':name, 'id':id})
    item=xbmcgui.ListItem(item['name'], iconImage="DefaultVideo.png", thumbnailImage=item.get('image', iconimage))
    item.setInfo(type='Video', infoLabels={'Title':name})
    item.addStreamInfo('video', {'duration':duration})
    item.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item)

def build_url(query):
    return sys.argv[0] + '?' + urllib.urlencode(query)

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
xbmc.log(msg='Arguments: %s' % str(args), level=-1)

if mode==None:
    categories()
else:
    exec '%s()' % mode[0]