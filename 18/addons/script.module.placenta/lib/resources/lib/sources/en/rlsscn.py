# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import requests, re
from bs4 import BeautifulSoup

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = 'rlsscn.in'
        self.base_link = 'http://rlsscn.in/'
        self.search_link = '?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'localtitle': localtitle, 'aliases': aliases, 'year': year}
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:

            url['episode'] = episode
            url['season'] = season
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):

        hostDict = hostDict + hostprDict

        sources = []
        season = url['season']
        episode = url['episode']
        if len(season) == 1:
            season = '0' + season
        if len(episode) == 1:
            episode = '0' + episode

        request =('%s+s%se%s' % (url['tvshowtitle'], season, episode)).replace(" ", "+")
        request = self.base_link + self.search_link % request
        request = requests.get(request)

        soup = BeautifulSoup(request.text, 'html.parser')
        soup = soup.find('h2', {'class':'title'})
        request = soup.find('a')['href']
        request = requests.get(request)
        soup = BeautifulSoup(request.text, 'html.parser')
        soup = soup.find('div', {'id':'content'})
        soup = soup.find_all('a', {'class':'autohyperlink'})
        source_list = []

        for i in soup:
            for h in hostDict:
                if h in i['href']:
                        source_list.append(i['href'])
        for i in source_list:
            host = i.replace('www.', '')
            host = re.findall(r'://(.*?)\..*?/', host)[0]

            if '1080p' in i:
                quality = '1080p'
            elif '720p' in i:
                quality = '720p'
            else:
                quality = 'SD'

            info = ''
            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': i, 'info': info,
                            'direct': False, 'debridonly': True})

        return sources



    def resolve(self, url):
        return url
