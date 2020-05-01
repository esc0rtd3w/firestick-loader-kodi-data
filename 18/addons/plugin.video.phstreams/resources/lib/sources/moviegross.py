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

import re, urllib, urlparse, string

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['afdah.tv']
        self.base_link = 'http://afdah.tv'
        self.search_link = '/wp-content/themes/afdah/ajax-search.php'
        self.post_link = 'yreuq=%s&meti=title'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            t = cleantitle.get(title)

            p = self.post_link % urllib.quote_plus(cleantitle.query(title))
            q = urlparse.urljoin(self.base_link, self.search_link)

            r = proxy.request(q, 'playing top', post=p, XHR=True)

            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            r = [(i[0], re.findall('(.+?)\((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i for i in r if t == cleantitle.get(i[1]) and str(year) == i[2]]

            url = proxy.parse(r[0][0])

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = proxy.request(url, 'movie')

            d = re.findall('(/embed\d*/\d+)', r)
            d = [x for y, x in enumerate(d) if x not in d[:y]]

            s = client.parseDOM(r, 'a', ret='href')
            s = [proxy.parse(i) for i in s]
            s = [i for i in s if i.startswith('http')]
            s = [x for y, x in enumerate(s) if x not in s[:y]]

            q = re.findall('This movie is of poor quality', r)
            quality = 'SD' if not q else 'CAM'

            for i in d:
                try:
                    raise Exception()
                    if quality == 'CAM': raise Exception()

                    url = urlparse.urljoin(self.base_link, i)
                    url = proxy.request(url, 'movie')
                    url = re.findall('salt\("([^"]+)', url)[0]
                    url = self.__caesar(self.__get_f(self.__caesar(url, 13)), 13)
                    url = re.findall('file\s*:\s*(?:\"|\')(http.+?)(?:\"|\')', url)
                    url = [directstream.googletag(u) for u in url]
                    url = sum(url, [])
                    url = [u for u in url if u['quality'] in ['1080p', 'HD']]
                    url = url[:2]
                    for u in url: u.update({'url': directstream.googlepass(u)})
                    url = [u for u in url if not u['url'] == None]

                    for u in url:
                        sources.append({'source': 'gvideo', 'quality': u['quality'], 'language': 'en', 'url': u['url'], 'direct': True, 'debridonly': False})
                except:
                    pass

            for i in s:
                try:
                    url = i
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    u = len(re.findall('((?:http|https)://)', url))
                    if u > 1: raise Exception()

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __caesar(self, plaintext, shift):
        lower = string.ascii_lowercase
        lower_trans = lower[shift:] + lower[:shift]
        alphabet = lower + lower.upper()
        shifted = lower_trans + lower_trans.upper()
        return plaintext.translate(string.maketrans(alphabet, shifted))

    def __get_f(self, s):
        i = 0
        t = ''
        l = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
        while i < len(s):
            try:
                c1 = l.index(s[i])
                c2 = l.index(s[i + 1])
                t += chr(c1 << 2 & 255 | c2 >> 4)
                c3 = l.index(s[i + 2])
                t += chr(c2 << 4 & 255 | c3 >> 2)
                c4 = l.index(s[i + 3])
                t += chr(c3 << 6 & 255 | c4)
                i += 4
            except:
                break

        return t


