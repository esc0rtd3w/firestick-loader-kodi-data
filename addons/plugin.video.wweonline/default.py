'''
    WWE Online (wweo.co) XBMC Plugin
    Copyright (C) 2013 XUNITYTALK.COM

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

import os
import string
import sys
import re
import urlresolver
import xbmc, xbmcaddon, xbmcplugin, xbmcgui,htmlcleaner

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

BASEURL = 'http://wweo.co/'
MEDIA_PAGE_REQ_URL = 'http://wweo.co/index.php'
MEDIA_REQ_URL = 'http://wweo.co/gkplugins/plugins/plugins_player.php'

showfilm = '1'
itemsperpage = '15'
itemsperrow = '3'
categoryid = ''

addon_id = 'plugin.video.wweonline'

net = Net()
addon = Addon(addon_id, sys.argv)

#PATHS
AddonPath = addon.get_path()

from universal import watchhistory

mode = addon.queries['mode']
url = addon.queries.get('url', '')
title = addon.queries.get('title', '')
img = addon.queries.get('img', '')
section = addon.queries.get('section', '')
page = addon.queries.get('page', '')
mediaid = addon.queries.get('mediaid', '')
typ = addon.queries.get('type', '')
historytitle = addon.queries.get('historytitle', '')
historylink = addon.queries.get('historylink', '')
iswatchhistory = addon.queries.get('watchhistory', '')
queued = addon.queries.get('queued', '')

def WatchedCallback():
    print 'Video completed successfully.'
    
def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",                   
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text
		

def MainMenu():  #home-page
    addon.add_directory({'mode' : 'Browse', 'section' : '9', 'page' : '1', 'type' : 'DVDs'}, {'title':  'DVDs'})
    addon.add_directory({'mode' : 'Browse', 'section' : '8', 'page' : '1', 'type' : 'Featured'}, {'title':  'Featured'})
    addon.add_directory({'mode' : 'Browse', 'section' : '1', 'page' : '1', 'type' : 'New'}, {'title':  'Newest'})
    addon.add_directory({'mode' : 'Browse', 'section' : '2', 'page' : '1', 'type' : 'TVT'}, {'title':  'Top Viewed - Today'})
    addon.add_directory({'mode' : 'Page', 'url' : '?movie=/list/view', 'page' : '1', 'type' : 'TVAT'}, {'title':  'Top Viewed - All Time'})
    addon.add_directory({'mode' : 'Browse', 'section' : '4', 'page' : '1', 'type' : 'TRT'}, {'title':  'Top Rated - Today'})
    addon.add_directory({'mode' : 'Page', 'url' : '?movie=/list/rate', 'page' : '1', 'type' : 'TRAT'}, {'title':  'Top Rated - All Time'})
    addon.add_directory({'mode' : 'Menu', 'section' : 'Categories', 'type' : 'Categories'}, {'title':  'Categories'})
    addon.add_directory({'mode' : 'Menu', 'section' : 'Type of Match', 'type' : 'ToM'}, {'title':  'Types of Match'})
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles(section, page):
    
    url_content = net.http_POST(MEDIA_PAGE_REQ_URL,
                                {'showfilm' : showfilm,
                                 'num' : section,
                                 'page' : page,
                                 'number' : itemsperpage,
                                 'apr' : itemsperrow,
                                 'cat_id' : categoryid}
                                ).content

    items = re.search(r"(?s)<table(.+?)pagecurrent", url_content)
    if items:
        items = addon.unescape(items.group(1))
        items = unescape(items)
        for item in re.finditer(r"<a.*?href=\"(.+?)\".*?title=\"(.+?)\".*?<img.*?src=\"(.+?)\"", items):
            item_url = BASEURL + item.group(1)
            item_img = item.group(3)
            item_title = htmlcleaner.cleanUnicode(item.group(2))
            try:addon.add_directory({'mode': 'GetLinks', 'url': item_url, 'title': item_title, 'img': item_img, 'type' : typ }, {'title': item_title}, img= item_img)
            except:pass

    if re.search(r"(?s)LAST", url_content):
        addon.add_directory({'mode': 'Browse', 'section' : section, 'page' : str(int(page) + 1), 'type' : typ }, {'title': 'Next Page >>'})
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetPage(url, page):
    
    url_content = net.http_GET(BASEURL + url + '/' + page).content

    items = re.search(r"(?s)<table(.+?)pagecurrent", url_content)
    
    if items:
        
        items = addon.unescape(items.group(1))
        items = unescape(items)
        
        for item in re.finditer(r"<a.*?href=(.+?) .*?title=\"(.+?)\".*?<img.*?src=\"(.+?)\"", items):
            item_url = BASEURL + item.group(1).replace('"','')

            item_img = item.group(3)
            item_title = item.group(2)
            if not 'wweo.co' in item.group(1):
            
                addon.add_directory({'mode': 'GetLinks', 'url': item_url, 'title': item_title, 'img': item_img, 'type' : typ }, {'title': item_title}, img= item_img)

    if re.search(r"(?s)LAST", url_content):
        addon.add_directory({'mode': 'Page', 'url' : url, 'page' : str(int(page) + 1), 'type' : typ }, {'title': 'Next Page >>'})
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Menu(section):

    url_content = net.http_GET(BASEURL).content

    items = re.search(r"(?s)" + section + "(.+?)</table>", url_content)
    
    if items:

        items = addon.unescape(items.group(1))
        items = unescape(items)

        for item in re.finditer(r"<a.*?href=(.+?)><b>(.+?)</b>", items):

            addon.add_directory({'mode' : 'Page', 'url' : item.group(1), 'page' : '1', 'type' : typ}, {'title':  item.group(2)})

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

def ReformatHostedMediaUrl(url):
    myurl = url
    
    myurl = myurl.replace("-nocookie", "")
    if 'youtube' in myurl:
        return myurl
        
    if re.search("\?", myurl):
        myurl = myurl[0:myurl.index('?')]
    
    return myurl

def GetLinks(url):
       
    url_content = net.http_GET(url).content

    episode_id = re.search(r"return player\((.+?)\)", url_content).group(1)
    url_content = net.http_POST(MEDIA_PAGE_REQ_URL,
                                {'watch' : '1',
                                 'episode_id' : episode_id }
                                ).content

    
    search_for_parts = re.search(r"return player\((.+?)\)", url_content)
    if search_for_parts:
        related_episodes = re.search(r"(?s)BEGIN RELATE EPISODE(.+?) END ", url_content)
        if related_episodes:
            related_episodes = addon.unescape(related_episodes.group(1))
            related_episodes = unescape(related_episodes)			
			
            for episode_meta in re.finditer(r"<tr><td>(.+?):.*?<td>(.+?)</td>", related_episodes):
                item_title = title + ' - ' + episode_meta.group(1)
                episodes = episode_meta.group(2)
                
                curr_item = re.search(r"\[(.+?)\]", episodes)
                if curr_item:
                    queries = {'mode': 'GetMedia', 'mediaid' : episode_id, 'title' : item_title + ' -' + curr_item.group(1), 'type' : typ, 'historytitle' : title, 'historylink' : sys.argv[0]+sys.argv[2] }
                    contextMenuItems = []
                    from universal import playbackengine    
                    contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, item_title + ' -' + curr_item.group(1), addon.build_plugin_url( queries ) ) ) )
                    
                    addon.add_directory(queries, {'title': item_title + ' -' + curr_item.group(1) }, contextMenuItems, context_replace=False, img= img)

                for episode in re.finditer(r"return player\((.+?)\).*?<b>(.+?)</b>", episodes):
                    queries = {'mode': 'GetMedia', 'mediaid' : episode.group(1), 'title' : item_title + ' - ' + episode.group(2), 'type' : typ, 'historytitle' : title, 'historylink' : sys.argv[0]+sys.argv[2]}
                    contextMenuItems = []
                    from universal import playbackengine    
                    contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, item_title + ' - ' + episode.group(2), addon.build_plugin_url( queries ) ) ) )
                    
                    addon.add_directory(queries, {'title': item_title + ' - ' + episode.group(2)}, contextMenuItems, context_replace=False, img= img)
                    
    else:
        #GetMedia(episode_id)
        queries = {'mode': 'GetMedia', 'mediaid' : episode_id, 'title' : title, 'type' : typ }
        
        contextMenuItems = []
        from universal import playbackengine    
        contextMenuItems.insert(0, ('Queue Item', playbackengine.QueueItem(addon_id, title, addon.build_plugin_url( queries ) ) ) )
        
        addon.add_directory(queries, {'title': title}, contextMenuItems, context_replace=False, img= img)
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetMedia(mediaid):

    from universal import playbackengine
    
    if queued == 'true':
    
        wh = watchhistory.WatchHistory(addon_id)    
                    
        url_content = net.http_POST(MEDIA_PAGE_REQ_URL,
                                    {'watch' : '1',
                                     'episode_id' : mediaid }
                                    ).content
                                    
        media_req_data = re.search(r"proxy\.link\=(.+?)\"", url_content)
        if media_req_data:
            media_req_data = media_req_data.group(1)
                    
            media_response_data = net.http_POST(MEDIA_REQ_URL, {'url':media_req_data}).content            

            media_url = ''
            media_size = 0
                    
            media_content = re.search(r"(?s)\"media\":(.+?),\"description\":", media_response_data)
            if media_content:
                media_links = addon.unescape(media_content.group(1))
                media_links = unescape(media_links)			
                for link in re.finditer("\"url\":\"(.+?)\",\"height\":(.+?),\"width\":(.+?),\"type\":\"(.+?)\"", media_links):

                    if (link.group(4).startswith("image")):
                        continue

                    size = int(link.group(2)) + int(link.group(3))
                    if (size <= media_size):
                        continue

                    media_url = link.group(1)
                    media_size = size

                if media_url:
                    
                    player = playbackengine.Play(resolved_url=media_url, addon_id=addon_id, video_type='wweonline', 
                                title=title,season='', episode='', year='', watchedCallback=WatchedCallback)
                    
                    # add watch history item                    
                    if historylink:
                        wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True, parent_title=historytitle)
                        wh.add_directory(historytitle, historylink, img=img, level='1')
                    else:
                        wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True)
                        
                    player.KeepAlive()
                        
                    
        else:
            check_for_hosted_media = re.search(r"(?s)<embed.*?flashvars.+?file=(.+?)[&\"]{1}", url_content)
            if check_for_hosted_media:        
                hosted_media_url = check_for_hosted_media.group(1)
                hosted_media_url = ReformatHostedMediaUrl(hosted_media_url)
                hosted_media = urlresolver.HostedMediaFile(url=hosted_media_url)
                if hosted_media:
                    resolved_media_url = urlresolver.resolve(hosted_media_url)
                    if resolved_media_url:
                        
                        player = playbackengine.Play(resolved_url=resolved_media_url, addon_id=addon_id, video_type='wweonline', 
                                title=title,season='', episode='', year='', watchedCallback=WatchedCallback)
                        
                        # add watch history item                        
                        if historylink:
                            wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True, parent_title=historytitle)
                            wh.add_directory(historytitle, historylink, img=img, level='1')
                        else:
                            wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True)
                            
                        player.KeepAlive()
            else:
                check_for_hosted_media = re.search(r"(?s)<embed.*?src=\"(.+?)\"", url_content)
               
                if check_for_hosted_media:        
                    hosted_media_url = check_for_hosted_media.group(1)
                    hosted_media_url = ReformatHostedMediaUrl(hosted_media_url)
                    hosted_media = urlresolver.HostedMediaFile(url=hosted_media_url)
                    if hosted_media:
                        print hosted_media_url
                        resolved_media_url = urlresolver.resolve(hosted_media_url)
                        if resolved_media_url:
                            
                            player = playbackengine.Play(resolved_url=resolved_media_url, addon_id=addon_id, video_type='wweonline', 
                                title=title,season='', episode='', year='', watchedCallback=WatchedCallback)
                            
                            # add watch history item
                            if historylink:
                                wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True, parent_title=historytitle)
                                wh.add_directory(historytitle, historylink, img=img, level='1')
                            else:
                                wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True)
                            
                            player.KeepAlive()
                else:
                    check_for_hosted_media = re.search(r"(?s)<iframe.*?src=\"(.+?)\"", url_content)
                    if check_for_hosted_media:        
                        hosted_media_url = check_for_hosted_media.group(1)                        
                        #hosted_media_url = ReformatHostedMediaUrl(hosted_media_url)
                        hosted_media = urlresolver.HostedMediaFile(url=hosted_media_url)
                        if hosted_media:
                            resolved_media_url = urlresolver.resolve(hosted_media_url)
                            if resolved_media_url:
                                
                                player = playbackengine.Play(resolved_url=resolved_media_url, addon_id=addon_id, video_type='wweonline', 
                                    title=title,season='', episode='', year='', watchedCallback=WatchedCallback)
                                
                                # add watch history item
                                if historylink:
                                    wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True, parent_title=historytitle)
                                    wh.add_directory(historytitle, historylink, img=img, level='1')
                                else:
                                    wh.add_video_item(title, sys.argv[0]+sys.argv[2], img=img, is_playable=True)
                                
                                player.KeepAlive()
    else:
        playbackengine.PlayInPL(title, img=img)
        
if mode == 'main': 
    MainMenu()
elif mode == 'Browse':
    GetTitles(section, page)
elif mode == 'Page':
    GetPage(url, page)
elif mode == 'Menu':
    Menu(section)
elif mode == 'GetLinks':
    GetLinks(url)
elif mode == 'GetMedia':
    try:GetMedia(mediaid)
    except:pass
elif mode == 'universalsettings':    
    from universal import _common
    _common.addon.show_settings()

