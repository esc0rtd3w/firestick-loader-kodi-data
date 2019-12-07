# -*- coding: utf-8 -*-

'''
    Covenant Add-on

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

import re,urllib,urlparse,json,base64,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movieshd.tv', 'movieshd.is', 'movieshd.watch', 'flixanity.is', 'flixanity.me','istream.is','flixanity.online']
        self.base_link = 'https://flixanity.online'
        self.streampost = 'ajax/zuxkvfdvfn.php'
        
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

    def searchShow(self, title, season, episode, aliases, headers):
        try:
            url = '%s/tv-show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(title), int(season), int(episode))
            url = client.request(url, headers=headers, output='geturl', timeout='10')
            if url == None:
                for alias in aliases:
                    url = '%s/tv-show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(alias['title']), int(season), int(episode))
                    url = client.request(url, headers=headers,output='geturl', timeout='10')
                    if not url == None: break
            return url
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(title))
            url = client.request(url, headers=headers, output='geturl', timeout='10')
            if url == None:
                for alias in aliases:
                    url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(alias['title']))
                    url = client.request(url, headers=headers, output='geturl', timeout='10')
                    if not url == None: break
                if url == None:
                    for alias in aliases:
                        url = '%s/movie/%s-%s' % (self.base_link, cleantitle.geturl(alias['title']), year)
                        url = client.request(url, headers=headers, output='geturl', timeout='10')
                        if not url == None: break
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            imdb = data['imdb']
            aliases = eval(data['aliases'])
            headers = {}
            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), aliases, headers)
            else:
                url = self.searchMovie(title, data['year'], aliases, headers)

            result = client.request(url, headers=headers, timeout='10')
            result = client.parseDOM(result, 'title')[0]

            if '%TITLE%' in result: raise Exception()

            r = client.request(url, headers=headers, output='extended', timeout='10')

            if not imdb in r[0]: raise Exception()

            cookie = r[4] ; headers = r[3] ; result = r[0]

            try:
                r = re.findall('(https:.*?redirector.*?)[\'\"]', result)
                for i in r:
                    try:
                        sources.append(
                            {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en',
                             'url': i, 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

            try: auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except: auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url

            u = urlparse.urljoin(self.base_link, self.streampost)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            c = client.request(u, post=post, headers=headers, XHR=True, output='cookie', error=True)

            headers['Cookie'] = cookie + '; ' + c

            r = client.request(u, post=post, headers=headers, XHR=True)
            r = str(json.loads(r))
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)

            for i in r:
                try:
                    if 'googleapis' in i:
                        sources.append({'source': 'GVIDEO', 'quality': 'SD', 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                    else:
                        valid, hoster = source_utils.is_host_valid(i, hostDict)
                        urls, host, direct = source_utils.check_directstreams(i, hoster)
                        if valid:
                            for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
                        else:
                            sources.append({'source': 'CDN', 'quality': 'SD', 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})

                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url
