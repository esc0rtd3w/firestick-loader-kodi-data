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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['movie25.ph', 'movie25.hk', 'tinklepad.is', 'tinklepad.ag', 'movie25.ag']
        self.base_link = 'https://movie25.ag'
        self.search_link_2 = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwODQ5Mjc2ODA5NjE4MzM5MDAwMzowdWd1c2phYm5scSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            q = self.search_link_2.decode('base64') % urllib.quote_plus(title)

            r = client.request(q)
            if r == None: r = client.request(q)
            if r == None: r = client.request(q)
            if r == None: r = client.request(q)

            r = json.loads(r)['results']
            r = [(i['url'], i['titleNoFormatting']) for i in r]
            r = [(i[0], re.findall('(?:^Watch |)(.+? \(\d{4}\))', i[1])) for i in r]
            r = [(urlparse.urljoin(self.base_link, i[0]), i[1][0]) for i in r if i[1]]

            t = cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            r = [i for i in r if any(x in i[1] for x in years)]

            match = [i[0] for i in r if t in cleantitle.get(i[1]) and '(%s)' % str(year) in i[1] and self.base_link in i[0]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0 : url = match[0] ; break
                except:
                    pass

            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            result = client.request(url);

            quality = re.compile('Quality(.+?)<').findall(result.replace('\n',''))
            quality = quality[0].strip() if quality else 'SD'
            if quality == 'CAM' or quality == 'TS': quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            result = client.parseDOM(result, 'a', ret='href')
            links = [i for i in result if 'movie25.ag/link' in i]

            dupes = []

            for i in links:
                try:
                    url = i
                    url = url.split('/')[4]
                    url = url.decode('base64')
                    url = re.findall('((?:http|https)://.+?/.+?)(?:&|$)', url)[0]
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    if url in dupes: raise Exception()
                    dupes.append(url)

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