# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    Copyright (C) 2016 Exodus

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
"""

import json
import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['meinkino.to']
        self.base_link = 'http://meinkino.to'
        self.search_link = '/filter?type=%s&suche=%s'
        self.get_link = '/geturl/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search_movie(imdb, year)
            if not url: url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), 'filme', year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), 'filme', year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'aliases': aliases, 'year': year}
            return urllib.urlencode(url)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'year': re.findall('(\d{4})', premiered)[0]})
            tvshowtitle = data['tvshowtitle']
            localtvshowtitle = data['localtvshowtitle']
            aliases = source_utils.aliases_to_array(eval(data['aliases']))

            url = self.__search([localtvshowtitle] + aliases, 'tv', data['year'], season, episode)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + aliases, 'tv', data['year'], season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            hostDict.append('vodcloud.co')  # seems like the internal host

            query = urlparse.urljoin(self.base_link, self.get_link % (re.findall('-id(.*?)$', url)[0]))

            r = client.request(query, post='', XHR=True)
            r = json.loads(r)
            r = [i[1] for i in r.items()]

            for i in r:
                try:
                    if isinstance(i, dict): i = i.values()
                    if isinstance(i, unicode): i = [i]

                    if isinstance(i, list):
                        for urlData in i:
                            if isinstance(i, dict) and urlData.get('link_mp4'):
                                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(urlData['link_mp4'])[0]['quality'], 'language': 'de', 'url': urlData['link_mp4'], 'direct': True, 'debridonly': False})
                                except: pass
                            else:
                                valid, hoster = source_utils.is_host_valid(urlData, hostDict)
                                if not valid: continue

                                sources.append({'source': hoster, 'quality': 'SD', 'language': 'de', 'url': urlData, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search_movie(self, imdb, year, type='filme'):
        try:
            years = [str(year), str(int(year) + 1), str(int(year) - 1)]
            years = ['&veroeffentlichung[]=%s' % i for i in years]

            query = self.search_link % (type, imdb)
            query += ''.join(years)
            query = urlparse.urljoin(self.base_link, query)

            r = self.__proceed_search(query)

            if len(r) == 1:
                return source_utils.strip_domain(r[0][0])
        except:
            return

    def __search(self, titles, type, year, season=0, episode=False):
        try:
            years = [str(year), str(int(year) + 1), str(int(year) - 1)]
            years = ['&veroeffentlichung[]=%s' % i for i in years]

            query = self.search_link % (type, urllib.quote_plus(cleantitle.query(titles[0])))
            query += ''.join(years)
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]

            r = self.__proceed_search(query)
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and int(i[2]) == int(season)][0]

            url = source_utils.strip_domain(r)
            if episode:
                r = client.request(urlparse.urljoin(self.base_link, url))
                r = dom_parser.parse_dom(r, 'div', attrs={'class': 'season-list'})
                r = dom_parser.parse_dom(r, 'li')
                r = dom_parser.parse_dom(r, 'a', req='href')
                r = [i.attrs['href'] for i in r if i and int(i.content) == int(episode)][0]

                url = source_utils.strip_domain(r)
            return url
        except:
            return

    @staticmethod
    def __proceed_search(query):
        r = client.request(query)
        r = dom_parser.parse_dom(r, 'div', attrs={'class': 'ml-items'})
        r = dom_parser.parse_dom(r, 'div', attrs={'class': 'ml-item'})
        r = dom_parser.parse_dom(r, 'a', attrs={'class': 'ml-name'}, req='href')
        r = [(i.attrs['href'], re.sub('<.+?>|</.+?>', '', i.content).strip()) for i in r if i[0]]
        r = [(i[0], i[1], re.findall('(.+?)\s+(?:staf+el|s)\s+(\d+)', i[1].lower())) for i in r]
        r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
        return r
