# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests

addon = xbmcaddon.Addon()
addon_icon = addon.getAddonInfo('icon')
addon_fanart = addon.getAddonInfo('fanart')
addon_handler = int(sys.argv[1])

# Fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), addon_fanart)

thumb_replacement = 'https://assets.democracynow.org/assets/default_content_image-354f4555cc64afadc730d64243c658dd0af1f330152adcda6c4900cb4a26f082.jpg'
current_show = 'http://www.democracynow.org/api/1/current_show'
r = requests.get(current_show).json()


def string_correction(_str):
    return _str.replace('&amp;', '&')\
               .replace('&quot;', '"')\
               .replace('&#8217;', "'")\
               .replace('<span class="caps">', '').replace('</span>', '')\
               .replace('<p>', '').replace('</p>', '')


def main():
    for show in r['media']:
        if 'High' in show['title']:
            url = show['src']
            title = 'Full Show'
            thumb = thumb_replacement
            summary = ''
            listitem = xbmcgui.ListItem(title, iconImage="DefaultVideoBig.png", thumbnailImage=thumb)
            listitem.setProperty('fanart_image', addon_fanart)
            listitem.setProperty('IsPlayable', 'true')
            listitem.setInfo(type="video",
                             infoLabels={"title": title,
                                         "plot": summary})
            xbmcplugin.addDirectoryItem(addon_handler, url, listitem, isFolder=False)

    for video in r['items']:
        if video['itemType'] == 'headline_section':
            title = 'Headlines'
        else:
            title = string_correction(video['title'])

        url = ''
        for _video in video['media']:
            if 'High' in _video['title']:
                url = _video['src']
            else:
                pass

        try:
            thumb = video['images'][0]['url']
        except KeyError:
            thumb = thumb_replacement

        try:
            duration = int(video['duration'])
        except KeyError:
            duration = ''

        try:
            summary = string_correction(video['summary'])
        except KeyError:
            summary = ''

        if url is not '':
            listitem = xbmcgui.ListItem(title, iconImage="DefaultVideoBig.png", thumbnailImage=thumb)
            listitem.setProperty('fanart_image', addon_fanart)
            listitem.setProperty('IsPlayable', 'true')
            listitem.setInfo(type="video",
                             infoLabels={"title": title,
                                         "plot": summary,
                                         "duration": duration})
            xbmcplugin.addDirectoryItem(addon_handler, url, listitem, isFolder=False)
        else:
            pass
    xbmcplugin.setContent(addon_handler, 'episodes')
    # End of list...
    xbmcplugin.endOfDirectory(addon_handler, True)

main()
