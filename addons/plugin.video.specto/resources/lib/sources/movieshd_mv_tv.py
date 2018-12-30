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


import re,urllib,urlparse
import json, time, random, string
import base64, hashlib

from resources.lib.libraries import cleantitle
from resources.lib.libraries import cache
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'https://cartoonhd.cc'
        #http://api.cartoonh0A6ru35yevokjaqbb8
        self.social_lock = '0A6ru35yevokjaqbb8'
        #http://api.cartoonhd.online/api/v1/0A6ru35yevokjaqbb8
        self.search_link = '%s/api/v1/%s' % (self.base_link, self.social_lock)


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
        #            for i in links: sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'MoviesHD', 'url': i['url']})
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                try:imdb = data['imdb']
                except: imdb = ''
                year = data['year']

                if 'tvshowtitle' in data:
                    url = '%s/tv-show/%s/season/%01d/episode/%01d' % (
                    self.base_link, cleantitle.geturl(title).replace('+','-'), int(data['season']), int(data['episode']))
                else:
                    url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(title).replace('+','-'))

                r = client.request(url, limit='10', output='extended')
                result = r[0]

                if result == None and not 'tvshowtitle' in data:
                    url += '-%s' % year
                    r = client.request(url, limit='10', output='extended')
                    result = r[0]

                cookie = r[4]
                headers = r[3]

                result2 = client.parseDOM(result, 'title')[0]

                if '%TITLE%' in result2: raise Exception()


                if not imdb in r[0]: raise Exception()


            else:
                url = urlparse.urljoin(self.base_link, url)

                r = client.request(url, output='extended')
                cookie = r[4]
                headers = r[3]
                result = r[0]



            try:
                auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except:
                auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)

            headers['Authorization'] = auth
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Cookie'] = cookie
            headers['Referer'] = url

            u = '/ajax/tnembeds.php'
            self.base_link = client.request(self.base_link, output='geturl')
            u = urlparse.urljoin(self.base_link, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            r = client.request(u, post=post, XHR=True)
            r = str(json.loads(r))
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)

            links = []

            links += [{'source': 'gvideo', 'url': i, 'quality': client.googletag(i)[0]['quality']} for i in r if 'google' in i]
            links += [{'source': 'streamango', 'url': i, 'quality': 'HD'} for i in r if 'streamango' in i]
            links += [{'source': 'openload.co', 'url': i, 'quality': 'HD'} for i in r if 'openload.co' in i]

            for i in links:
                sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'MoviesHD', 'url': i['url']})

            return sources

        except Exception as e:
            control.log('ERROR moviesHD %s' % e)
            return sources


    def resolve(self, url):
        try:
            if 'openload.co' in url or 'thevideo.me' in url or 'streamango' in url:
                mylink =  resolvers.request(url)
                control.log('> Resolve moviesHD %s | %s' % (url,mylink))
                return mylink
            else:
                return client.googlepass(url)
        except:
            return

    def movieshd_token(self):
        try:
            token = client.request(self.base_link)
            token = re.findall("var\s+tok\s*=\s*'([^']+)", token)[0]
            return token
        except:
            return


    def movieshd_set(self):
        return ''.join([random.choice(string.ascii_letters) for _ in xrange(25)])

    def movieshd_sl(self):
        return hashlib.md5(base64.encodestring('0A6ru35yyi5yn4THYpJqy0X82tE95btV')+self.social_lock).hexdigest()


    def movieshd_rt(self, s, shift=13):
        s2 = ''
        for c in s:
            limit = 122 if c in string.ascii_lowercase else 90
            new_code = ord(c) + shift
            if new_code > limit:
                new_code -= 26
            s2 += chr(new_code)
        return s2

