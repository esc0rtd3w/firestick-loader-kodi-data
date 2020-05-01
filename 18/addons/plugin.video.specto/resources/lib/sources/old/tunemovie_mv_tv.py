# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

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

from resources.lib.libraries import cleantitle
from resources.lib.libraries import pyaes
from resources.lib.libraries import control
from resources.lib.libraries import client
from resources.lib import resolvers
import json

class source:
    def __init__(self):
        self.base_link = 'https://tunemovies.to'
        self.search_link = '/search/%s.html'
        #http://tunemovie.is/search-movies/The+Hateful+Eight.html

    def get_movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(title)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs = {'class': 'thumb'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            url = [i[0] for i in r if t in cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(data['tvshowtitle'])

            t = cleantitle.get(data['tvshowtitle'])

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs = {'class': 'thumb'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            url = [i[0] for i in r if t in cleantitle.get(i[1]) and ('Season %s' % season) in i[1]][0]
            url += '?episode=%01d' % int(episode)

            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #try: sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'url': i})
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            try:
                url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except:
                episode = None

            ref = url

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            if not episode == None:
                result = client.parseDOM(result, 'div', attrs = {'id': 'ip_episode'})[0]
                ep_url = client.parseDOM(result, 'a', attrs = {'data-name': str(episode)}, ret='href')[0]
                for i in range(3):
                    result = client.request(ep_url)
                    if not result == None: break

            r = client.parseDOM(result, 'div', attrs = {'class': '[^"]*server_line[^"]*'})

            for u in r:
                try:
                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/plugins/ipplugins.php')
                    p1 = client.parseDOM(u, 'a', ret='data-film')[0]
                    p2 = client.parseDOM(u, 'a', ret='data-server')[0]
                    p3 = client.parseDOM(u, 'a', ret='data-name')[0]
                    post = {'ipplugins': 1, 'ip_film': p1, 'ip_server': p2, 'ip_name': p3}
                    post = urllib.urlencode(post)
                    for i in range(3):
                        result = client.request(url, post=post, XHR=True, referer=ref, timeout='10')
                        if not result == None: break

                    result = json.loads(result)
                    u = result['s']
                    s = result['v']

                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/ipplayer/ipplayer.php')

                    post = {'u': u, 'w': '100%', 'h': '420', 's': s, 'n': 0}
                    post = urllib.urlencode(post)

                    for i in range(3):
                        result = client.request(url, post=post, XHR=True, referer=ref)
                        if not result == None: break

                    url = json.loads(result)['data']

                    if type(url) is list:
                        url = [i['files'] for i in url]
                        for i in url:
                            try: sources.append({'source': 'gvideo', 'provider': 'Tunemovie', 'quality': client.googletag(i)[0]['quality'],'url': i})
                            except: pass

                    else:
                        url = client.request(url)
                        url = client.parseDOM(url, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
                        url += '|%s' % urllib.urlencode({'User-agent': client.randomagent()})
                        sources.append({'source': 'cdn', 'quality': 'HD','provider': 'Tunemovie', 'url': i})


                except:
                    pass

            return sources
        except:
            return sources


    def __resolve(self, result):
        try:
            result = client.parseDOM(result, 'div', attrs = {'id': 'player'})[0]

            try: url = client.parseDOM(result, 'iframe', ret='src')[0]
            except: pass
            try: url = base64.b64decode(re.compile('decode\("(.+?)"').findall(result)[0])
            except: pass

            if 'proxy.link=tunemovie' in url:
                url = re.compile('proxy[.]link=tunemovie[*]([^&]+)').findall(url)[-1]

                key = base64.b64decode('Q05WTmhPSjlXM1BmeFd0UEtiOGg=')
                decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key + (24 - len(key)) * '\0'))
                url = url.decode('hex')
                url = decrypter.feed(url) + decrypter.feed()

            url = resolvers.request(url)
            return url
        except:
            return


    def resolve(self, url):
        return client.googlepass(url)

