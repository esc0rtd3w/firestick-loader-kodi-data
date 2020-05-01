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

import re
import urllib
import urlparse
import json

from resources.lib.modules import cleantitle
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['1kino.in', 'streamkiste.tv']
        self.base_link = 'http://1kino.in'
        self.search_link = '/include/live.php?keyword=%s&nonce=%s'
        self.search_js = '/js/live-search.js'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            pid = re.findall('[e|t]\s*=\s*"(\w+)"\s*,', r)[0]

            r = dom_parser.parse_dom(r, 'div', attrs={'id': 'stream-container'})[0].content
            r = re.compile('<div id="stream-h">.*?</li>.*?</div>\s*</div>', re.IGNORECASE | re.DOTALL).findall(r)
            r = [(dom_parser.parse_dom(i, 'div', attrs={'id': 'mirror-head'}), dom_parser.parse_dom(i, 'div', attrs={'id': 'stream-links'})) for i in r]
            r = [(i[0][0].content, i[1]) for i in r if i[0]]
            r = [(re.findall('.+\s[\||-]\s(.*)', i[0]), i[1]) for i in r]
            r = [(i[0][0].strip(), i[1]) for i in r if len(i[0]) > 0]

            for name, links in r:
                quality, info = source_utils.get_release_quality(name)

                links = [dom_parser.parse_dom(i.content, 'a', req=['href', 'title', 'data-mirror', 'data-host']) for i in links]
                links = [([i[0].attrs.get('data-mirror'), i[0].attrs.get('data-host'), pid, url], i[0].content) for i in links]

                info = ' | '.join(info)

                for link, hoster in links:
                    valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                    if not valid: continue

                    link = urllib.urlencode({'mirror': link[0], 'host': link[1], 'pid': link[2], 'ceck': 'sk'})

                    sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'url': link, 'info': info, 'direct': False, 'debridonly': False, 'checkquality': True})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            r = client.request(urlparse.urljoin(self.base_link, '/include/load.php'), post=url, XHR=True)
            r = r.replace('\r', '').replace('\n', '')

            links = [i.attrs['href'] for i in dom_parser.parse_dom(r, 'a', req='href') if i]
            ifrms = [i.attrs['src'].strip() for i in dom_parser.parse_dom(r, 'iframe', req='src') if i]
            links += ifrms

            for link in links:
                if not link.startswith('http'): link = urlparse.urljoin(self.base_link, link)

                if self.base_link in link:
                    link = client.request(link, output='geturl')

                if self.base_link not in link:
                    return link
        except:
            return

    def __search(self, titles, year):
        try:
            n = cache.get(self.__get_nonce, 24)

            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])), n)
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)
            r = json.loads(r)
            r = [(r[i].get('url'), r[i].get('title'), r[i].get('extra').get('date')) for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return

    def __get_nonce(self):
        n = client.request(urlparse.urljoin(self.base_link, self.search_js))
        try: n = re.findall('nonce=([0-9a-zA-Z]+)', n)[0]
        except: n = '273e0f8ea3'
        return n