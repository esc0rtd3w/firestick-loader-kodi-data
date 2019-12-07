# -*- coding: utf-8 -*-

"""
    Flixnet Add-on
    Copyright (C) 2016 Flixnet

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
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviefree.to', 'http://topfreemovies.online']
        self.base_link = 'http://topfreemovies.online'
        self.search_link = '/search/%s'
        self.server_link = '/ajax/loadServer'
        self.episode_link = '/ajax/loadEpisode'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'item'})
            r = [(dom_parser.parse_dom(i, 'a', attrs={'class': 'cluetip'}, req='href'), dom_parser.parse_dom(i, 'div', attrs={'class': 'description'})) for i in r]
            r = [(i[0][0].attrs['href'], dom_parser.parse_dom(i[1], 'h3', attrs={'class': 'text-nowrap'}), dom_parser.parse_dom(i[1], 'div', attrs={'class': 'meta'})) for i in r if i[0] and i[1]]
            r = [(i[0], i[1][0].content, dom_parser.parse_dom(i[2], 'span', attrs={'class': 'pull-left'})) for i in r if i[0] and i[1] and i[2]]
            r = [(i[0], i[1], re.sub('[^\d]+', '', i[2][0].content)) for i in r if i[2]]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) == t and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            hostDict.append('fastload.co')  # seems like the internal host

            url = urlparse.urljoin(self.base_link, url)
            url = url.replace('-online.html', '.html')

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'img', attrs={'class': 'info-poster-img'}, req=['data-id', 'data-name'])[0]
            id = r.attrs['data-id']
            n = r.attrs['data-name']

            r = client.request(urlparse.urljoin(self.base_link, self.server_link), post={'film_id': id, 'n': n, 'epid': 0}, referer=url)
            r = json.loads(r).get('list', '')

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'server-film'})
            r = dom_parser.parse_dom(r, 'a', attrs={'class': 'btn'}, req='data-id')

            for i in r:
                try:
                    l = client.request(urlparse.urljoin(self.base_link, self.episode_link), post={'epid': i.attrs['data-id']}, referer=url)
                    l = json.loads(l).get('link', {})

                    l = zip(l.get('l', []), l.get('q', []))
                    l = [(link[0], re.sub('[^\d]+', '', link[1])) for link in l]

                    links = [(x[0], '4K') for x in l if int(x[1]) >= 2160]
                    links += [(x[0], '1440p') for x in l if int(x[1]) >= 1440]
                    links += [(x[0], '1080p') for x in l if int(x[1]) >= 1080]
                    links += [(x[0], 'HD') for x in l if 720 <= int(x[1]) < 1080]
                    links += [(x[0], 'SD') for x in l if int(x[1]) < 720]

                    for link, quality in links:
                        valid, host = source_utils.is_host_valid(link, hostDict)
                        if not valid: continue

                        if directstream.googletag(link): host = 'gvideo'; direct = True
                        elif 'fastload.co' in link: direct = True
                        else: direct = False

                        sources.append({'source': host, 'quality': quality, 'language': 'de', 'url': link, 'direct': direct, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


