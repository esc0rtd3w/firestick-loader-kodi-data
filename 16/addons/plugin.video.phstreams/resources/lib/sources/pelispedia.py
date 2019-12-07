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


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import jsunpack

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['pelispedia.tv']
        self.base_link = 'http://www.pelispedia.tv'
        self.moviesearch_link = '/pelicula/%s/'
        self.tvsearch_link = '/serie/%s/'
        self.player_link = 'http://player.pelispedia.tv/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.moviesearch_link % cleantitle.geturl(title)

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1', timeout='10')
            r = client.parseDOM(r, 'title')

            if not r:
                url = 'http://www.imdb.com/title/%s' % imdb
                url = client.request(url, headers={'Accept-Language':'es-ES'}, timeout='10')
                url = client.parseDOM(url, 'title')[0]
                url = re.sub('(?:\(|\s)\d{4}.+', '', url).strip()
                url = cleantitle.normalize(url.encode("utf-8"))
                url = self.moviesearch_link % cleantitle.geturl(url)

                r = urlparse.urljoin(self.base_link, url)
                r = client.request(r, limit='1', timeout='10')
                r = client.parseDOM(r, 'title')

            if not year in r[0]: raise Exception()

            return url
        except:
            pass


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.tvsearch_link % cleantitle.geturl(tvshowtitle)

            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r, limit='1', timeout='10')
            r = client.parseDOM(r, 'title')

            if not r:
                url = self.tvsearch_link % cleantitle.geturl(tvshowtitle + '-')
                r = urlparse.urljoin(self.base_link, url)
                r = client.request(r, limit='1', timeout='10')
                r = client.parseDOM(r, 'title')
                url = self.tvsearch_link % cleantitle.geturl(tvshowtitle)

            if not r:
                url = 'http://www.imdb.com/title/%s' % imdb
                url = client.request(url, headers={'Accept-Language':'es-ES'}, timeout='10')
                url = client.parseDOM(url, 'title')[0]
                url = re.sub('\((?:.+?|)\d{4}.+', '', url).strip()
                url = cleantitle.normalize(url.encode("utf-8"))
                url = self.tvsearch_link % cleantitle.geturl(url)

                r = urlparse.urljoin(self.base_link, url)
                r = client.request(r, limit='1', timeout='10')
                r = client.parseDOM(r, 'title')

            if not year in r[0]: raise Exception()

            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return


            ep_url = '/pelicula/%s-season-%01d-episode-%01d/' % (url.strip('/').split('/')[-1], int(season), int(episode))
            ep_url = urlparse.urljoin(self.base_link, ep_url)
            r = client.request(ep_url, limit=1, timeout='10')

            if not r:
                ep_url = '/pelicula/%s-season-%01d-episode-%01d-/' % (url.strip('/').split('/')[-1], int(season), int(episode))
                ep_url = urlparse.urljoin(self.base_link, ep_url)
                r = client.request(ep_url, limit=1, timeout='10')

            if not r:
                url = 'http://www.imdb.com/title/%s' % imdb
                url = client.request(url, headers={'Accept-Language':'es-ES'}, timeout='10')
                url = client.parseDOM(url, 'title')[0]
                url = re.sub('\((?:.+?|)\d{4}.+', '', url).strip()
                url = cleantitle.geturl(url.encode("utf-8"))
                url = '/pelicula/%s-season-%01d-episode-%01d/' % (url.strip('/').split('/')[-1], int(season), int(episode))
                ep_url = urlparse.urljoin(self.base_link, url)
                r = client.request(ep_url, limit=1, timeout='10')

            if not r:
                raise Exception()
            return ep_url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            r = urlparse.urljoin(self.base_link, url)

            result = client.request(r, timeout='10')

            f = client.parseDOM(result, 'iframe', ret='src')
            f = [i for i in f if 'iframe' in i][0]

            result = client.request(f, headers={'Referer': r}, timeout='10')

            r = client.parseDOM(result, 'div', attrs = {'id': 'botones'})[0]
            r = client.parseDOM(r, 'a', ret='href')
            r = [(i, urlparse.urlparse(i).netloc) for i in r]

            links = []

            for u, h in r:
                if not 'pelispedia' in h: continue

                result = client.request(u, headers={'Referer': f}, timeout='10')

                try:
                    if 'pelispedia' in h: raise Exception()

                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')\s*,\s*label\s*:\s*(?:\"|\')(.+?)(?:\"|\')', url)
                    url = [i[0] for i in url if '720' in i[1]][0]

                    links.append({'source': 'cdn', 'quality': 'HD', 'url': url, 'direct': False})
                except:
                    pass

                try:
                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')', url)

                    for i in url:
                        try:
                            links.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'url': i, 'direct': True})
                        except:
                            pass
                except:
                    pass

                try:
                    post = re.findall('gkpluginsphp.*?link\s*:\s*"([^"]+)', result)[0]
                    post = urllib.urlencode({'link': post})

                    url = urlparse.urljoin(self.base_link, '/Pe_flsh/plugins/gkpluginsphp.php')
                    url = client.request(url, post=post, XHR=True, referer=u, timeout='10')
                    url = json.loads(url)['link']

                    links.append({'source': 'gvideo', 'quality': 'HD', 'url': url, 'direct': True})
                except:
                    pass

                try:
                    post = re.findall('var\s+parametros\s*=\s*"([^"]+)', result)[0]

                    post = urlparse.parse_qs(urlparse.urlparse(post).query)['pic'][0]
                    post = urllib.urlencode({'sou': 'pic', 'fv': '23', 'url': post})

                    url = urlparse.urljoin(self.base_link, '/Pe_Player_Html5/pk/pk_2/plugins/protected.php')
                    url = client.request(url, post=post, XHR=True, timeout='10')
                    url = json.loads(url)[0]['url']

                    links.append({'source': 'cdn', 'quality': 'HD', 'url': url, 'direct': True})
                except:
                    pass

                try:
                    if not jsunpack.detect(result): raise Exception()

                    result = jsunpack.unpack(result)
                    url = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    url = re.findall('file\s*:\s*.*?\'(.+?)\'', url)
                    for i in url:
                        try:
                            i = client.request(i, headers={'Referer': f}, output='geturl', timeout='10')
                            links.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'url': i,
                                          'direct': True})
                        except:
                            pass
                except:
                    pass

                try:
                    post = re.findall('var\s+parametros\s*=\s*"([^"]+)', result)[0]

                    post = urlparse.parse_qs(urlparse.urlparse(post).query)['pic'][0]
                    token = 'eyJjdCI6InZGS3QySm9KRWRwU0k4SzZoZHZKL2c9PSIsIml2IjoiNDRkNmMwMWE0ZjVkODk4YThlYmE2MzU0NDliYzQ5YWEiLCJzIjoiNWU4MGUwN2UwMjMxNDYxOCJ9'
                    post = urllib.urlencode({'sou': 'pic', 'fv': '0', 'url': post, 'token': token})

                    url = urlparse.urljoin(self.player_link, '/template/protected.php')
                    url = client.request(url, post=post, XHR=True, timeout='10')
                    js = json.loads(url)
                    url = [i['url'] for i in js]
                    for i in url:
                        try:
                            i = client.request(i, headers={'Referer': f}, output='geturl', timeout='10')
                            links.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'url': i,
                                          'direct': True})
                        except:
                            pass
                except:
                    pass

            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'language': 'en', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


