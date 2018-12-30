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


import re,urllib,urlparse,random
import hashlib, string, json
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control


class source:
    def __init__(self):
        self.base_link = 'http://watch5s.to'
        self.random_link = ['watch5s.to', 'cmovieshd.com']
        self.info_link = '/ajax/movie_qtip/%s'

    def request(self, url, check):
        try:
            result = client.request(url)
            if check in str(result): return result.decode('iso-8859-1').encode('utf-8')
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
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

    def get_episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            choice = random.choice(self.random_link)
            base_link = 'http://%s' % choice
            strm_link = 'http://play.%s' % choice + '/grabber-api/episode/%s?token=%s'

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                if 'tvshowtitle' in data:
                    url = '/tv-series/%s-season-%01d/watch/' % (cleantitle.geturl(title), int(data['season']))
                    year = str((int(data['year']) + int(data['season'])) - 1)
                    episode = '%01d' % int(data['episode'])

                else:
                    url = '/movie/%s/watch/' % cleantitle.geturl(title)
                    year = data['year']
                    episode = None

                url = urlparse.urljoin(base_link, url)
                referer = url
                url = url.replace('+','-')
                r = client.request(url)

                y = re.findall('Release\s*:\s*.+?\s*(\d{4})', r)[0]

                if not year == y: raise Exception()
            else:
                try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
                except: episode = None

                url = urlparse.urljoin(base_link, url)
                url = re.sub('/watch$', '', url.strip('/')) + '/watch/'
                referer = url

                r = client.request(url)

            r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
            r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

            if not episode == None:
                r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
            else:
                r = [i[0] for i in r]

            r = [i for i in r if '/server-' in i]

            for u in r:
                try:
                    p = client.request(u, referer=referer, timeout='10')

                    t = re.findall('player_type\s*:\s*"(.+?)"', p)[0]
                    if t == 'embed': raise Exception()

                    s = client.parseDOM(p, 'input', ret='value', attrs = {'name': 'episodeID'})[0]
                    t = ''.join(random.sample(string.digits + string.ascii_uppercase + string.ascii_lowercase, 8))
                    k = hashlib.md5('!@#$%^&*(' + s + t).hexdigest()
                    v = hashlib.md5(t + referer + s).hexdigest()

                    stream = strm_link % (s, t)
                    cookie = '%s=%s' % (k, v)

                    u = client.request(stream, referer=referer, cookie=cookie, timeout='10')

                    u = json.loads(u)['playlist'][0]['sources']
                    u = [i['file'] for i in u if 'file' in i]

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'provider':'Watch5s', 'url': i})
                        except: pass
                except:
                    pass

            return sources

        except Exception as e:
            control.log('ERROR mowie5s %s' % e)
            return sources



    def resolve(self, url):
        return client.googlepass(url)


