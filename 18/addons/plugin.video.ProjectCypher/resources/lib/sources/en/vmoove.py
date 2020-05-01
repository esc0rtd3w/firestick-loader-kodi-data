# -*- coding: utf-8 -*-

'''
    Jor-EL Add-on
    Copyright (C) 2016 Jor-EL

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

# Addon Name: Project Cypher
# Addon id: plugin.video.ProjectCypher
# Addon Provider: Cypher

from bs4 import BeautifulSoup
from resources.lib.modules import directstream
import requests
import sys

class source:

    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = 'vmovee.me'
        self.base_link = 'https://vmovee.me'
        self.search_link = '/gold-app/gold-includes/GOLD.php?seasons_post_name='
        self.search_episode_link = '/gold-app/gold-includes/GOLD.php?season_id='
        self.movie_link = ''
        self.episode_link = '/gold-app/gold-includes/GOLD.php?episode_id='

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        tvshowtitle = tvshowtitle.replace(" ", "-")
        url = tvshowtitle
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if not url:
            return url
        try:
            with requests.session() as s:
                p = s.get(self.base_link + self.search_link + url)
                if p.text == '':
                    p= s.get(self.base_link + self.search_link + url + "-all-seasons")
                    if p.text == '':
                        return url
                soup = BeautifulSoup(p.text, 'html.parser')
                season_link_list = soup.findAll('a')
                url = []
                season_list = {}
                c = 0
                for i in season_link_list:
                    c += 1
                    season_list[str(c)] = (''.join(filter(lambda x: x.isdigit(), str(i.prettify()))))

                p = s.get(self.base_link + self.search_episode_link + season_list[season])
                # NOW SCRAPPING EPISODES
                soup = BeautifulSoup(p.text, 'html.parser')
                episode_link_list = soup.findAll('a')
                episode_list = {}
                c = 0
                for i in episode_link_list:
                    c += 1
                    episode_list[str(c)] = (''.join(filter(lambda x: x.isdigit(), str(i.prettify()))))

            url = episode_list[episode]
        except:
            print("Unexpected error in VMOOVE Script:", sys.exc_info()[0])
        return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        if not url:
            return sources

        try:
            with requests.Session() as s:
                p = s.get(self.base_link + self.episode_link + url)
                soup = BeautifulSoup(p.text, 'html.parser')
                src = soup.findAll('iframe')[0]
                url = src['src']
                if '//apu,litaurl.com/' in url:
                    p = s.get(url)
                    url = p.url

                if 'thevideo' in url:
                    sources.append(
                        {'source': "thevideo.me",
                         'quality': '720p',
                         'language': "en",
                         'url': url,
                         'info': '',
                         'direct': False,
                         'debridonly': False})
        except:
            print("Unexpected error in VMOOVE Sources Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            pass

        return sources

    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url
