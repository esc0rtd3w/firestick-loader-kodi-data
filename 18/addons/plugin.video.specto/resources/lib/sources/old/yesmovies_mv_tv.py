# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2016 mrknow

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

# TODO: Check gvideo resolving

import re,urllib,urlparse, json, hashlib
import base64
import random, string
import time


from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import directstream
from resources.lib.libraries import control
from resources.lib.libraries import jsunfuck
import requests



class source:
    def __init__(self):
        self.base_link = 'https://yesmovies.to'
        self.search_link = '/movie/search/%s.html'
        self.info_link = '/ajax/movie_info/%s.html?is_login=false'
        self.server_link = '/ajax/v4_movie_episodes/%s'
        self.embed_link = '/ajax/movie_embed/%s'
        self.token_link = '/ajax/movie_token?eid=%s&mid=%s'
        self.source_link = '/ajax/movie_sources/%s?x=%s&y=%s'


    def getImdbTitle(self, imdb):
        try:
            t = 'http://www.omdbapi.com/?i=%s' % imdb
            t = client.request(t)
            t = json.loads(t)
            t = cleantitle.normalize(t['Title'])
            return t
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.getsearch(title)))
            r = client.request(url, headers=headers, timeout='15')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            years = [str(year), str(int(year)+1), str(int(year)-1)]


            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                #url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
                for i in r:
                    print("I:",i, i[2])
                    print(cleantitle.get(i[1]))

                r = [i for i in r if any(x in i[2] for x in years)]
                url = [i[0] for i in r if cleantitle.get(i[1]) in cleantitle.get(title)][0]
                print r


            except:
                url = None
                pass

            if (url == None):
                url = [i[0] for i in r if cleantitle.get(i[1]) in cleantitle.get(title)][0]
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

    def searchShow(self, title, season):
        try:
            title = cleantitle.normalize(title)
            search = '%s Season %s' % (title, int(season))
            url = urlparse.urljoin(self.base_link, self.search_link_2 % urllib.quote_plus(cleantitle.getsearch(search)))
            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            print len(r)
            if len(r) == 0:
                url = url.replace('+','-')
                r = client.request(url, timeout='10')
                r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            url = [i[0] for i in r if cleantitle.get(search) == cleantitle.get(i[1])][0]
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            if 'tvshowtitle' in data:
                r = self.searchShow(data['tvshowtitle'], season)

            if r == None:
                t = cache.get(self.getImdbTitle, 900, imdb)
                if t != data['tvshowtitle']:
                    r = self.searchShow(t, season)

            return urllib.urlencode({'url': r, 'episode': episode})
        except:
            return

    def movie_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = client.request(u % url)

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return y, q
        except:
            return

    def ymovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)

            for i in range(3):
                r = client.request(u % url)
                if not r == None: break

            q = client.parseDOM(r, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(r, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #sources.append({'source': 'gvideo', 'quality': s['quality'],'url': s['url'],'provider': 'Yesmovies'})
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            headers = {}

            if 'tvshowtitle' in data:
                episode = int(data['episode'])
                url = self.searchShow(data['tvshowtitle'], data['season'], '', headers)
            else:
                episode = 0
                url = self.searchMovie(data['title'], data['year'], '', headers)

            mid = re.findall('-(\d+)', url)[-1]

            try:
                headers = {'Referer': url}
                u = urlparse.urljoin(self.base_link, self.server_link % mid)
                r = client.request(u, headers=headers, XHR=True)
                r = json.loads(r)['html']
                r = client.parseDOM(r, 'div', attrs = {'class': 'pas-list'})
                ids = client.parseDOM(r, 'li', ret='data-id')
                servers = client.parseDOM(r, 'li', ret='data-server')
                labels = client.parseDOM(r, 'a', ret='title')
                r = zip(ids, servers, labels)
                for eid in r:
                    try:
                        ep = re.findall('episode.*?(\d+).*?',eid[2].lower())[0]
                    except:
                        ep = 0
                    if (episode == 0) or (int(ep) == episode):
                        url = urlparse.urljoin(self.base_link, self.token_link % (eid[0], mid))
                        script = client.request(url)
                        if '$_$' in script:
                            params = self.uncensored1(script)
                        elif script.startswith('[]') and script.endswith('()'):
                            params = self.uncensored2(script)
                        elif '_x=' in script:
                            x = re.search('''_x=['"]([^"']+)''', script).group(1)
                            y = re.search('''_y=['"]([^"']+)''', script).group(1)
                            params = {'x': x, 'y': y}
                        else:
                            raise Exception()

                        u = urlparse.urljoin(self.base_link, self.source_link % (eid[0], params['x'], params['y']))
                        r = client.request(u, XHR=True)
                        url = json.loads(r)['playlist'][0]['sources']
                        url = [i['file'] for i in url if 'file' in i]
                        #url = [i[0] for i in url if i]
                        for i in url:
                            print "i",i


                        links = []
                        links += [{'source': 'gvideo', 'url': i, 'quality': client.googletag(i)[0]['quality']} for i in
                                  url if 'google' in i]

                        for i in links:
                            sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Yesmovies',
                                            'url': i['url']})

            except:
                pass

            return sources
        except Exception as e:
            control.log('Yes sources error:%s' % e)
            return sources

    def resolve(self, url):
        try:
            if self.embed_link in url:
                result = client.request(url, XHR=True)
                url = json.loads(result)['embed_url']
                return url

            try:
                if not url.startswith('http'):
                    url = 'http:' + url

                for i in range(3):
                    u = directstream.googlepass(url)
                    if not u == None: break

                return u
            except:
                return
        except:
            return

    def uncensored(a, b):
        x = '' ; i = 0
        for i, y in enumerate(a):
            z = b[i % len(b) - 1]
            y = int(ord(str(y)[0])) + int(ord(str(z)[0]))
            x += chr(y)
        x = base64.b64encode(x)
        return x

    def uncensored1(self, script):
        try:
            script = '(' + script.split("(_$$)) ('_');")[0].split("/* `$$` */")[-1].strip()
            script = script.replace('(__$)[$$$]', '\'"\'')
            script = script.replace('(__$)[_$]', '"\\\\"')
            script = script.replace('(o^_^o)', '3')
            script = script.replace('(c^_^o)', '0')
            script = script.replace('(_$$)', '1')
            script = script.replace('($$_)', '4')

            vGlobals = {"__builtins__": None, '__name__': __name__, 'str': str, 'Exception': Exception}
            vLocals = {'param': None}
            exec (CODE % script.replace('+', '|x|'), vGlobals, vLocals)
            data = vLocals['param'].decode('string_escape')
            x = re.search('''_x=['"]([^"']+)''', data).group(1)
            y = re.search('''_y=['"]([^"']+)''', data).group(1)
            return {'x': x, 'y': y}
        except:
            pass

    def uncensored2(self, script):
        try:
            js = jsunfuck.JSUnfuck(script).decode()
            x = re.search('''_x=['"]([^"']+)''', js).group(1)
            y = re.search('''_y=['"]([^"']+)''', js).group(1)
            return {'x': x, 'y': y}
        except:
            pass