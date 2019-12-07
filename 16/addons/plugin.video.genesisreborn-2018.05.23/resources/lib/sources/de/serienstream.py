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
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['serienstream.to']
        self.base_link = 'https://serienstream.to'
        self.search_link = '/ajax/search'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = url[:-1] if url.endswith('/') else url
            url += '/staffel-%d/episode-%d/' % (int(season), int(episode))
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = client.request(urlparse.urljoin(self.base_link, url))

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'hosterSiteVideo'})
            r = dom_parser.parse_dom(r, 'li', attrs={'data-lang-key': re.compile('[1|3]')})
            r = [(dom_parser.parse_dom(i, 'a', req='href'), dom_parser.parse_dom(i, 'h4')) for i in r]
            r = [(i[0][0].attrs['href'], i[1][0].content.lower()) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], i[1], re.findall('(.+?)\s*<br\s*/?>(.+?)$', i[1], re.DOTALL)) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '') for i in r]
            r = [(i[0], i[1], 'HD' if 'hosterhdvideo' in i[2] else 'SD') for i in r]

            for link, host, quality in r:
                valid, host = source_utils.is_host_valid(host, hostDict)
                if not valid: continue

                sources.append({'source': host, 'quality': quality, 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            url = client.request(urlparse.urljoin(self.base_link, url), output='geturl')
            if self.base_link not in url:
                return url

            r = client.request(url)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'container'})
            return dom_parser.parse_dom(r, 'iframe', req='src')[0].attrs['src']
        except:
            return

    def __search(self, titles, year):
        try:
            r = urllib.urlencode({'keyword': titles[0]})
            r = client.request(urlparse.urljoin(self.base_link, self.search_link), XHR=True, post=r)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = json.loads(r)
            r = [(i['link'], re.sub('<.+?>|</.+?>', '', i['title'])) for i in r if 'title' in i and 'link' in i]
            r = [(i[0], i[1], re.findall('(.+?)\s*Movie \d+:.+?$', i[1], re.DOTALL)) for i in r]
            r = [(i[0], i[2][0] if len(i[2]) > 0 else i[1]) for i in r]
            r = [(i[0], i[1], re.findall('(.+?) \((\d{4})\)?', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return
