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

import re,urllib,urlparse,base64,json,random,hashlib

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import cache


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movieshd.sk']
        self.base_link = 'https://123movieshd.sk'
        self.search_link = '/search/%s'
        self.grabber_api = 'https://player.123movieshd.sk/grabber-api/episode/%s?token=%s'

    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            search = '%s Season %01d' % (title, int(season))
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(search))
            r = client.request(url, headers=headers, timeout='15')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            url = [i[0] for i in r if self.matchAlias(i[2][0], aliases) and i[2][1] == season][0]
            url = url.replace('/film/','/watch/')
            return url
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
            r = client.request(url, headers=headers, timeout='15')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
            except:
                url = None
                pass

            if (url == None):
                url = [i[0] for i in results if self.matchAlias(i[1], aliases)][0]

            url = url.replace('/film/','/watch/')
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            headers = {}

            if 'tvshowtitle' in data:
                url = '%s/watch/%s-season-%01d' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']))
                url = client.request(url, headers=headers, timeout='10', output='geturl')

                if url == None:
                    url = self.searchShow(data['tvshowtitle'], data['season'], aliases, headers)

            else:
                url = self.searchMovie(data['title'], data['year'], aliases, headers)

            if url == None: raise Exception()

            r = client.request(url, headers=headers, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            links = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
            if 'episode' in data:
                links = [i[0] for i in links if i[1].lower().startswith('episode %02d:' % int(data['episode']))]
            else:
                links = [i[0] for i in links]

            for link in links:
                try:
                    r = client.request(link, headers=headers, timeout='10')
                    episodeId = re.compile('.?episode:\s+"(\d+)"').findall(r)[0]
                    decoded = self._token(link, episodeId)
                    url = self.grabber_api % (episodeId, decoded['token'])
                    cookie = '%s=%s' % (decoded['k'], decoded['n'])
                    headers['Referer'] = link
                    headers['Cookie'] = cookie
                    r = client.request(url, headers=headers, XHR=True, timeout='10')
                    js = json.loads(r)

                    try:
                        u = js['playlist'][0]['sources']
                        u = [i['file'] for i in u if 'file' in i]

                        for i in u:
                            try:
                                sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'],
                                                'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                            except:
                                pass
                    except:
                        pass
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url


    def _token(self, url, episodeId):
        try:
            token = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz') for i in range(8))
            k = hashlib.md5('!@#$%^&*(' + str(episodeId) + token).hexdigest()
            n = hashlib.md5(token + url + str(episodeId)).hexdigest()
            return {'token': token, 'k': k, 'n': n}
        except:
            return