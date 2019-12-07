# -*- coding: utf-8 -*-

'''
    Covenant Add-on

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
        self.domains = ['movie2z.to']
        self.base_link = 'https://www.movie2z.to/de/'
        self.search_link = 'search-%s.html'
        self.get_link = 'redirect.php?a=m&id=%s'

    def movie(self, imdb, title, localtitle, aliases, year):        
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases))
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases))
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = url[:-1] if url.endswith('/') else url
            url += '/%d/%d/' % (int(season), int(episode))
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            query = urlparse.urljoin(self.base_link, url)

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'ul', attrs={'id': 'mainmenu'})
            r = dom_parser.parse_dom(r, 'li')

            for i in r:
                i = dom_parser.parse_dom(i, 'a')
                i = i[0][0]['href']
                i = client.request(i)
                i = dom_parser.parse_dom(i, 'select', attrs={'id': 'selecthost'})
                i = dom_parser.parse_dom(i, 'option')

                for x in i:
                    hoster = re.search('^\S*', x[1]).group().lower()
                    url = x[0]['value']

                    valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                    if not valid: continue

                    sources.append({'source': hoster, 'quality': 'SD', 'language': 'de', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        url = url.replace('amp;', '')
        url = client.request(url, output='geturl')

        return url

    def __search(self, titles):
        try:
            query = self.search_link % (urllib.quote_plus(urllib.quote_plus(cleantitle.query(titles[0]))))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            post = urllib.urlencode({'movlang_de': '1', 'movlang': ''})

            r = client.request(query, post=post)

            r = dom_parser.parse_dom(r, 'table', attrs={'class': 'table'})
            r = dom_parser.parse_dom(r, 'a', attrs={'class': 'PreviewImage'})

            for x in r:
                title = cleantitle.get(x[1])
                if title in t:
                    return source_utils.strip_domain(x[0]['href'])
            return
        except:
            return
