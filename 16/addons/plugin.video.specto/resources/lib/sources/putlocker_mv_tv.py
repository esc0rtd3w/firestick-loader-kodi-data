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


import re,urllib,urlparse,json,base64,time, random,string
import hashlib


from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import cache
from resources.lib import resolvers




class source:
    def __init__(self):
        #self.base_link = 'https://flixanity.watch'
        self.base_link = 'https://flixanity.online'
        self.sitemap = '/sitemap.xml'

        self.social_lock = '0A6ru35yevokjaqbb8'

        self.search_link = 'https://api.flixanity.online/api/v1/'+ self.social_lock
        #https://api.flixanity.watch/api/v1/0A6ru35yevokjaqbb8


    def get_movie(self, imdb, title, year):
        try:
            tk = cache.get(self.putlocker_token, 8)
            set = self.putlocker_set()
            rt = self.putlocker_rt(tk + set)
            sl = self.putlocker_sl()
            tm = int(time.time() * 1000)
            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = self.search_link

            post = {'q': title.lower(), 'limit': '20', 'timestamp': tm, 'verifiedCheck': tk, 'set': set, 'rt': rt, 'sl': sl}
            print("POST",post)
            post = urllib.urlencode(post)

            r = client.request(url, post=post, headers=headers, output='')
            print("R",r)
            r = json.loads(r)

            t = cleantitle.get(title)

            r = [i for i in r if 'year' in i and 'meta' in i]
            r = [(i['permalink'], i['title'], str(i['year']), i['meta'].lower()) for i in r]
            r = [i for i in r if 'movie' in i[3]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            print("U",url)
            return url

        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            """
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return None
            """
            tk = cache.get(self.putlocker_token, 8)
            set = self.putlocker_set()
            rt = self.putlocker_rt(tk + set)
            sl = self.putlocker_sl()

            tm = int(time.time() * 1000)

            headers = {'X-Requested-With': 'XMLHttpRequest'}

            url = self.search_link

            post = {'q': tvshowtitle.lower(), 'limit': '100', 'timestamp': tm, 'verifiedCheck': tk, 'set': set, 'rt': rt, 'sl': sl}
            post = urllib.urlencode(post)

            r = client.request(url, post=post, headers=headers)
            r = json.loads(r)

            t = cleantitle.get(tvshowtitle)

            r = [i for i in r if 'year' in i and 'meta' in i]
            r = [(i['permalink'], i['title'], str(i['year']), i['meta'].lower()) for i in r]
            r = [i for i in r if 'tv' in i[3]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            print(">>>",url)
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            #url = urlparse.parse_qs(url)
            #url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            #tvshowtitle =  cleantitle.query10(url['tvshowtitle'])
            tvshowtitle =  url.split('/')[-1]


            r = '/tv-show/%s/season/%01d/episode/%01d' % (tvshowtitle, int(season), int(episode))
            #y = '/tv-show/%s/season/%01d' % (tvshowtitle, int(season))

            control.log('AAAA y >>>>>>   %s' % r)
            #result = client.request(urlparse.urljoin(self.base_link, y))
            #print "ResUlt get_episode",result
            #result = client.parseDOM(result,'span', attrs={'class':'dat'})[0]
            #if url['year'] == str(result.strip()):
            #    url = r.encode('utf-8')
            #    control.log('>>>>>>  Putlocker URL  %s' % url)
            #    return url

            return r
        except:
            return

    def putlocker_token(self):
        try:
            token = client.request(self.base_link)
            token = re.findall("var\s+tok\s*=\s*'([^']+)", token)[0]
            return token
        except:
            return

    def putlocker_set(self):
        return ''.join([random.choice(string.ascii_letters) for _ in xrange(25)])

    def putlocker_sl(self):
        return hashlib.md5(base64.encodestring('0A6ru35yyi5yn4THYpJqy0X82tE95bt')+self.social_lock).hexdigest()

    def putlocker_rt(self, s, shift=13):
        s2 = ''
        for c in s:
            limit = 122 if c in string.ascii_lowercase else 90
            new_code = ord(c) + shift
            if new_code > limit:
                new_code -= 26
            s2 += chr(new_code)
        return s2

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        print("GetRes>>>>", url)

        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url, output='extended')
            cookie = r[4] ; headers = r[3] ; result = r[0]


            try:
                auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
                auth = 'Bearer %s' % urllib.unquote_plus(auth)
            except:
                auth = 'Bearer false'

            headers['Authorization'] = auth
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Referer'] = url
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            #u = '/ajax/embeds.php'
            u = '/ajax/jne.php'
            u = urlparse.urljoin(self.base_link, u)

            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'

            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]

            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]

            post = {'action': action, 'idEl': idEl, 'token': token, 'elid': elid}
            post = urllib.urlencode(post)

            r = client.request(u, post=post, headers=headers, output='')
            #print('PUTLOCKER RESP %s' % r)
            r = r.replace('\\', '')

            #r = str(json.loads(r))
            r = re.findall('"type":"([^"]+)","net":"([^"]+)","embed":"(.*?)","weight":"([^"]+)"', r)

            r = [client.parseDOM(i[2], 'iframe', ret='src')[0] for i in r]

            links = []

            for i in r:
                try: links += [{'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'url': i}]
                except: pass


            links += [{'source': 'openload.co', 'quality': 'SD', 'url': i} for i in r if 'openload.co' in i]
            #links += [{'source': 'vidto.me', 'quality': 'SD', 'url': i} for i in r if 'vidto.me' in i]
            links += [{'source': 'streamango', 'quality': 'HD', 'url': i} for i in r if 'streamango' in i]

            for i in links:
                sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Putlocker', 'url': i['url']})

            return sources
        except Exception as e:
            control.log('ERROR putlocker %s' % e)
            return sources

    def resolve(self, url):
        try:
            if 'openload.co' in url or 'streamango' in url or 'thevideo.me' in url :
                url = resolvers.request(url)
            return url
        except:
            return



