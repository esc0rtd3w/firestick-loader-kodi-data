#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2016 PodGod
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#


from xbmcswift2 import Plugin
from tools2 import *
import feedparser
import plugintools
import xbmc,xbmcaddon

storage = Storage(settings.storageName, type="dict", eval=True)
plugin = Plugin()

textViewer(plugin.get_string(32000), once=True)

torAudio = 'https://extratorrent.cc/rss.xml?type=search&cid=9&search=howard+stern'
name = '[COLOR blue]AUDIO[/COLOR] - Archived Shows'
storage.database[name] = (torAudio, False)
storage.save()
# torVideo = 'https://extratorrent.cc/rss.xml?type=search&cid=9&search=howard+stern'
# name = '[COLOR red]VIDEO[/COLOR] - HTV On Demand'
# storage.database[name] = (torVideo, False)
# storage.save()

@plugin.route('/')
def index():
    items = [
         {'label': '[COLOR blue]AUDIO[/COLOR] - Archived Shows',
         'path': ('rss://cast.xtothezracing.com/?feed=podcast&podcast_series=hss'),
         'thumbnail': dirImages('audio.png'),
         'properties': {'fanart_image': dirImages('fanart.jpg')}
         },
		 {'label': '[COLOR blue]AUDIO[/COLOR] - Alternate Archive',
         'path': ('rss://julien.familyds.com:8080/howardsternshow'),
         'thumbnail': dirImages('audio.png'),
         'properties': {'fanart_image': dirImages('fanart.jpg')}
         },
		 {'label': '[COLOR red]VIDEO [/COLOR]- Howard Vids',
         'path': 'plugin://plugin.video.youtube/search/?sp=CAI%253D&q=howard+stern',
         'thumbnail': dirImages('video.png'),
         'properties': {'fanart_image': dirImages('fanart.jpg')}
         },
		 {'label': '[COLOR red]VIDEO [/COLOR]- HTV On Demand',
         'path': 'plugin://plugin.video.youtube/search/?q=htvod&sp=CAISAhAB',
         'thumbnail': dirImages('video.png'),
         'properties': {'fanart_image': dirImages('fanart.jpg')}
         },
		 {'label': '[B]DISCLAIMER / SETTINGS[/B]',
         'path': plugin.url_for('set'),
         'thumbnail': dirImages('icon.png'),
         'properties': {'fanart_image': dirImages('fanart.jpg')}
         }
    ]
    items.extend(read())
    return items

@plugin.route('/readRss/<url>/')
def readRss(url):
    items = []
    titlesTorrent, magnetsTorrent = _readRss(url)
    torrents = plugin.get_storage('torrents')
    torrents.clear()

    if len(titlesTorrent) > 0:
        torrents.update({
            'titles': titlesTorrent,
            'magnets': magnetsTorrent
        })
        items.append(
            {'label': plugin.get_string(32022),
             'path': plugin.url_for('readList', type="Torrent"),
             'thumbnail': dirImages("torrents.png"),
             'properties': {'fanart_image': settings.fanart}
             }

        )
    return items
	
@plugin.route('/set')
def set():
    textViewer(plugin.get_string(32000))
    settings.settings.openSettings()

@plugin.route('/readList/<type>')
def readList(type):
    torrents = plugin.get_storage('torrents')
    info = {}
    info['titles'] = ""
    info['magnets'] = ""
    if type == "Torrent":
        plugin.set_content("torrents")
        info = torrents
    items = []
    for (title, magnet) in zip(info['titles'], info['magnets']):
        info = UnTaggle(title)
        try:
            items.append({'label': info.label,
                          'path': plugin.url_for('play', magnet=normalize(magnet)),
                          'thumbnail': dirImages('torrents.png'),
                          'properties': {'fanart_image': dirImages('fanart.jpg')},
                          'info': info.info,
                          'stream_info': info.infoStream,
                          })
        except:
            pass
    return plugin.finish(items=items, view_mode=0)


@plugin.route('/play/<magnet>')
def play(magnet):
    uri_string = quote_plus(getPlayableLink(uncodeName(magnet)))
    if settings.value["plugin"] == 'Quasar':
        link = 'plugin://plugin.video.quasar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'Pulsar':
        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
    elif settings.value["plugin"] == 'KmediaTorrent':
        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
    elif settings.value["plugin"] == "Torrenter":
        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
               '&not_download_only=True'
    elif settings.value["plugin"] == "YATP":
        link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
    elif settings.value["plugin"] == "XBMCtorrent":
        link = 'plugin://plugin.video.xbmctorrent/play/%s' + uri_string
    settings.debug("PlayMedia(%s)" % link)
    xbmc.executebuiltin("PlayMedia(%s)" % link)
    xbmc.executebuiltin('Dialog.Close(all, true)')


def read():
    items = []
    for name in sorted(storage.database):
        (RSS, isIntegrated) = storage.database[name]
        items.append({'label': "*" + '[B][COLOR green]TORRENTS[/COLOR] ' + name + '[/B]',
                      'path': plugin.url_for('readRss', url=RSS),
                      'thumbnail': dirImages('torrents.png'),
                      'properties': {'fanart_image': dirImages('fanart.jpg')},
                      })
    return items


def _readRss(url):
    from socket import setdefaulttimeout
    magnetsTorrent = []
    titlesTorrent = []
    if url is not '':
        settings.log(url)
        setdefaulttimeout(10)
        feeds = feedparser.parse(url)
        for entry in feeds.entries:
            settings.debug(entry)
            isMagnet = False
            for key in entry.keys():
                if "magnet" in key:
                    isMagnet = True
                    tag = key
                    break
            if isMagnet:
                value = entry[tag]
            else:
                for link in entry.links:
                    value = link.href
            entry.title = entry.title.replace('/', '')
            info = formatTitle(entry.title.replace('/', ''))
            if 'MOVIE' in info['type']:
                titlesTorrent.append(entry.title)
                magnetsTorrent.append(value)
    return titlesTorrent, magnetsTorrent
	
import urllib,urllib2,re,cookielib,string,os,xbmc, xbmcgui, xbmcaddon, xbmcplugin, random
from t0mm0.common.net import Net as net
	
if __name__ == '__main__':
    plugin.run()
	

