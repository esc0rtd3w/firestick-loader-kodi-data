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


import re,urllib,urlparse,json,random,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['directdownload.tv']
        self.base_link = 'http://directdownload.tv'
        self.search_link = 'L2FwaT9rZXk9NEIwQkI4NjJGMjRDOEEyOSZxdWFsaXR5W109SERUViZxdWFsaXR5W109RFZEUklQJnF1YWxpdHlbXT03MjBQJnF1YWxpdHlbXT1XRUJETCZxdWFsaXR5W109V0VCREwxMDgwUCZxdWFsaXR5W109MTA4MFAtWDI2NSZsaW1pdD0yMCZrZXl3b3JkPQ=='
        self.b_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mbw=='
        self.u_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9tZW1iZXJzb25seS9jb21wb25lbnRzL2NvbV9pY2VwbGF5ZXIvdmlkZW8ucGhwP2g9Mzc0Jnc9NjMxJnZpZD0lcyZpbWc9'
        self.r_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9pcC5waHA/dj0lcyY='
        self.j_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9tZW1iZXJzb25seS9jb21wb25lbnRzL2NvbV9pY2VwbGF5ZXIvdmlkZW8ucGhwQWpheFJlc3AucGhwP3M9JXMmdD0lcw=='
        self.p_link = 'aWQ9JXMmcz0lcyZpcXM9JnVybD0mbT0lcyZjYXA9KyZzZWM9JXMmdD0lcw=='


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
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def request(self, url, post=None, cookie=None, referer=None, output='', close=True):
        try:
            headers = {'Accept': '*/*'}
            if not cookie == None: headers['Cookie'] = cookie
            if not referer == None: headers['Referer'] = referer
            result = client.request(url, post=post, headers=headers, output=output, close=close)
            result = result.decode('iso-8859-1').encode('utf-8')
            result = urllib.unquote_plus(result)
            return result
        except:
            return


    def directdl_cache(self, url):
        try:
            url = urlparse.urljoin(base64.b64decode(self.b_link), url)
            result = self.request(url)
            result = re.compile('id=(\d+)>.+?href=(.+?)>').findall(result)
            result = [(re.sub('http.+?//.+?/','/', i[1]), 'tt' + i[0]) for i in result]
            return result
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if debrid.status() == False: raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])



            try:
                if not 'tvshowtitle' in data: raise Exception()

                links = []

                f = ['S%02dE%02d' % (int(data['season']), int(data['episode']))]
                t = data['tvshowtitle']

                q = base64.b64decode(self.search_link) + urllib.quote_plus('%s %s' % (t, f[0]))
                q = urlparse.urljoin(self.base_link, q)

                result = client.request(q)
                result = json.loads(result)
            except:
                links = result = []

            for i in result:
                try:
                    if not cleantitle.get(t) == cleantitle.get(i['showName']): raise Exception()

                    y = i['release']
                    y = re.compile('[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s]').findall(y)[-1]
                    y = y.upper()
                    if not any(x == y for x in f): raise Exception()

                    quality = i['quality']

                    size = i['size']
                    size = float(size)/1024
                    size = '%.2f GB' % size

                    if 'X265' in quality: info = '%s | HEVC' % size
                    else: info = size

                    if '1080P' in quality: quality = '1080p'
                    elif quality in ['720P', 'WEBDL']: quality = 'HD'
                    else: quality = 'SD'

                    url = i['links']
                    for x in url.keys(): links.append({'url': url[x], 'quality': quality, 'info': info})
                except:
                    pass

            for i in links:
                try:
                    url = i['url']
                    if len(url) > 1: raise Exception()
                    url = url[0].encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostprDict: raise Exception()
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': i['quality'], 'language': 'en', 'url': url, 'info': i['info'], 'direct': False, 'debridonly': True})
                except:
                    pass



            try:
                hostDict2 = [(i.rsplit('.', 1)[0], i) for i in hostDict]

                q = ('/tv/a-z/%s', data['tvshowtitle']) if 'tvshowtitle' in data else ('/movies/a-z/%s', data['title'])
                q = q[0] % re.sub('^THE\s+|^A\s+', '', q[1].strip().upper())[0]

                url = cache.get(self.directdl_cache, 120, q)
                url = [i[0] for i in url if data['imdb'] == i[1]][0]
                url = urlparse.urljoin(base64.b64decode(self.b_link), url)

                try: v = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
                except: v = None

                if v == None:
                    result = self.request(url)
                    url = re.compile('(/ip[.]php.+?>)%01dx%02d' % (int(data['season']), int(data['episode']))).findall(result)[0]
                    url = re.compile('(/ip[.]php.+?)>').findall(url)[-1]
                    url = urlparse.urljoin(base64.b64decode(self.b_link), url)

                url = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]

                u = base64.b64decode(self.u_link) % url ; r = base64.b64decode(self.r_link) % url
                j = base64.b64decode(self.j_link) ; p = base64.b64decode(self.p_link)

                result = self.request(u, referer=r)

                secret = re.compile('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?').findall(result)[0]
                secret = ''.join(secret)

                t = re.compile('"&t=([^"]+)').findall(result)[0]

                s_start = re.compile('(?:\s+|,)s\s*=(\d+)').findall(result)[0]
                m_start = re.compile('(?:\s+|,)m\s*=(\d+)').findall(result)[0]

                img = re.compile('<iframe[^>]*src="([^"]+)').findall(result)
                img = img[0] if len(img) > 0 else '0'
                img = urllib.unquote(img)

                result = client.parseDOM(result, 'div', attrs = {'class': 'ripdiv'})
                result = [(re.compile('<b>(.*?)</b>').findall(i), i) for i in result]
                result = [(i[0][0], i[1].split('<p>')) for i in result if len(i[0]) > 0]
                result = [[(i[0], x) for x in i[1]] for i in result]
                result = sum(result, [])
            except:
                result = []

            for i in result:
                try:
                    quality = i[0]
                    if any(x in quality for x in ['1080p', '720p', 'HD']): quality = 'HD'
                    else: quality = 'SD'

                    host = client.parseDOM(i[1], 'a')[-1]
                    host = re.sub('\s|<.+?>|</.+?>|.+?#\d*:', '', host)
                    host = host.strip().rsplit('.', 1)[0].lower()
                    host = [x[1] for x in hostDict2 if host == x[0]][0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    s = int(s_start) + random.randint(3, 1000)
                    m = int(m_start) + random.randint(21, 1000)
                    id = client.parseDOM(i[1], 'a', ret='onclick')[-1]
                    id = re.compile('[(](.+?)[)]').findall(id)[0]
                    url = j % (id, t) + '|' + p % (id, s, m, secret, t)
                    url += '|%s' % urllib.urlencode({'Referer': u, 'Img': img})
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': True})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            b = urlparse.urlparse(url).netloc
            b = re.compile('([\w]+[.][\w]+)$').findall(b)[0]

            if not b in base64.b64decode(self.b_link): return url
 
            u, p, h = url.split('|')
            r = urlparse.parse_qs(h)['Referer'][0]
            #u += '&app_id=Exodus'

            c = self.request(r, output='cookie', close=False)
            result = self.request(u, post=p, referer=r, cookie=c)

            url = result.split('url=')
            url = [urllib.unquote_plus(i.strip()) for i in url]
            url = [i for i in url if i.startswith('http')]
            url = url[-1]

            return url
        except:
            return


