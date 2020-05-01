# -*- coding: utf-8 -*-

'''
    Exodus Add-on

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

import re, urllib, urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['freemoviedownloads6.com']
        self.base_link = 'http://freemoviedownloads6.com/'
        self.search_link = '/?s=%s+&x=0&y=0'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            posts = client.parseDOM(r, 'div', attrs={'class': 'post-\d+.+?'})

            items = []

            for post in posts:
                try:
                    r = dom_parser2.parse_dom(post, 'a', req='href')
                    t = r[0].content
                    u = r[0].attrs['href']
                    items += [(t, u)]

                except:
                    pass

            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D|Free Movie Downloads)(\.|\)|\]|\s|)(.+|)', '', name)

                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                    if not y == hdlr: raise Exception()

                    data = client.request(item[1])
                    data = client.parseDOM(data, 'div', attrs={'class': 'postcont'})
                    data = client.parseDOM(data, 'p')[-1]
                    data = dom_parser2.parse_dom(data, 'a')
                    data = [(i.attrs['href'], i.content) for i in data]
                    data = [(i[0], i[1]) for i in data]
                    for i in data:
                        quality, info = source_utils.get_release_quality(i[1], i[0])
                        url = i[0]
                        if any(x in url for x in ['.rar', '.zip', '.iso']): raise Exception()
                        url = client.replaceHTMLCodes(url)
                        url = url.encode('utf-8')

                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                        'direct': True, 'debridonly': False})
                except:
                    pass

            check = [i for i in sources if not i['quality'] == 'CAM']
            if check: sources = check

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


