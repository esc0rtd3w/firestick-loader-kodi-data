# -*- coding: utf-8 -*-

'''
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
'''


import re,json,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['fmovie.co', 'afdah.org', 'xmovies8.org', 'putlockerhd.co']
        self.base_link = 'https://afdah.org'
        self.search_link = '/results?q=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            c, h = self.__get_cookies(query)

            t = cleantitle.get(title)

            r = client.request(query, headers=h, cookie=c)

            r = client.parseDOM(r, 'div', attrs={'class': 'cell_container'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            referer = urlparse.urljoin(self.base_link, url)

            c, h = self.__get_cookies(referer)

            try: post = urlparse.parse_qs(urlparse.urlparse(referer).query).values()[0][0]
            except: post = referer.strip('/').split('/')[-1].split('watch_', 1)[-1].rsplit('#')[0].rsplit('.')[0]

            post = urllib.urlencode({'v': post})

            url = urlparse.urljoin(self.base_link, '/video_info/iframe')

            r = client.request(url, post=post, headers=h, cookie=c, XHR=True, referer=referer)
            r = json.loads(r).values()
            r = [urllib.unquote(i.split('url=')[-1]) for i in r]

            for i in r:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources

    def __get_cookies(self, url):
        h = {'User-Agent': client.randomagent()}

        c = client.request(url, headers=h, output='cookie')
        c = client.request(urlparse.urljoin(self.base_link, '/av'), cookie=c, output='cookie', headers=h, referer=url)
        c = client.request(url, cookie=c, headers=h, referer=url, output='cookie')

        return c, h

    def resolve(self, url):
        return directstream.googlepass(url)


