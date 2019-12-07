# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Eggman
# Addon id: Eggmans
# Addon Provider: Eggman

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animetoon.org']
        self.base_link = 'http://animetoon.org'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = '%s %s' % (title,year)
            return url
        except:
            return
			
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            if season == '1': 
                url = self.base_link + '/' + url + '-episode-' + episode
            else:
                url = self.base_link + '/' + url + '-season-' + season + '-episode-' + episode
            return url
        except:
            return

# videozoome
# playbbme
# easyvideo
# playpanda # playpandanet.gogoanime.to/
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('Playlist .+?</span></div><div><iframe src="(.+?)"').findall(r)
                for url in match: 
                    r = client.request(url)
                    if 'gogoanime' in url:
                        match = re.compile("url: '(.+?)',").findall(r)
                    else:
                        match = re.compile('file: "(.+?)",').findall(r)
                    for url in match: 
                        sources.append({'source': 'Direct','quality': 'SD','language': 'en','url': url,'direct': False,'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url