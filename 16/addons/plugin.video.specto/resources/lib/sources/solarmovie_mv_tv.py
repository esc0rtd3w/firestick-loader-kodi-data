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


import re,urllib,urlparse,time
import hashlib, string, json
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import cache
from resources.lib.libraries import directstream
from resources.lib.libraries import jsunfuck



class source:
    def __init__(self):
        self.base_link = 'https://solarmoviez.to'
        self.sourcelink = '/ajax/movie_sources/%s?x=%s&y=%s'
        self.search_link = '/search/%s.html'
        self.info_link = '/ajax/movie_get_info/%s.html'
        self.token_link = '/ajax/movie_token?eid=%s&mid=%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'


    def request(self, url, post=None, headers=None, XHR=False):
        try:
            r = client.request(url, post=post, headers=headers, XHR=XHR, output='extended')

            if r[0] == None: return r

            if 'internetmatters.org' in r[0]:
                url = re.findall('(?://.+?|)(/.+)', url)[0]
                url = urlparse.urljoin(self.base_link, url)
                r = client.request(url, post=post, headers=headers, XHR=XHR, output='extended')

            return r
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            q = q.replace('+','-')
            q = urlparse.urljoin(self.base_link, q)


            r = self.request(q)[0]
            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a', ret='data-url')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1]]
            #else:
            #    r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            r = [(i[0],i[2]) for i in r if cleantitle.get(t) == cleantitle.get(i[1])][:2]
            r = [(i[0], re.findall('(\d+)', i[1])[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.solar_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path
                except:
                    pass


        except Exception as e:
            control.log('ERROR Solar %s' % e )
            return

    def solar_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            headers = {'Referer' : self.base_link}
            #https://solarmoviez.to/ajax/movie_get_info/20324.html
            u = self.request(u % url, headers=headers,XHR=True)[0]

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
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

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.getsearch(title)
            cleanmovie = cleantitle.get(title)
            data['season'], data['episode'] = season, episode
            episodecheck = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            episodecheck = episodecheck.lower()
            query = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            ep = "%01d" % (int(data['episode']))
            full_check = 'season%01d' % (int(data['season']))
            full_check = cleanmovie + full_check
            query = self.search_link % (urllib.quote_plus(title), season)
            query = urlparse.urljoin(self.base_link, query)
            r = client.request(query, headers=self.headers)
            # print ("BOBBYAPP", r)
            match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(r)
            for id, name in match:
                name = cleantitle.get(name)
                # print ("BOBBYAPP id name", id, name)
                if full_check == name:
                    type = 'tv_episodes'
                    ep = "%01d" % (int(data['episode']))
                    print ("BOBBYAPP PASSED", id, name)
                    murl = id
            murl = client.replaceHTMLCodes(murl)
            murl = murl.encode('utf-8')

            url = {'imdb': imdb, 'title': title, 'episode': episode, 'url':murl}
            url = urllib.urlencode(url)
            return url
        except Exception as e:
            print "ERROR %s" % e
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #sources.append({'source': host.split('.')[0], 'quality': 'SD', 'provider': 'Movie25', 'url': url})
        sources = []
        results = []

        try:

            if url == None: return sources

            if url.startswith('http'): self.base_link = url

            url = urlparse.urljoin(self.base_link, url)
            url = referer = url.replace('/watching.html', '')
            url = url.replace('.html','')
            #if not url.endswith('/'): url = url + "/watching.html"
            #else : url = url + "watching.html"


            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            r = self.request(url+ '/watching.html')[0]
            try:mid = re.compile('name="movie_id" value="(.+?)"').findall(r)[0]
            except:mid = re.compile('id: "(.+?)"').findall(r)[0]

            try:
                headers = {'Referer': url}

                time_now = int(time.time() * 10000)
                EPISODES = '/ajax/v4_movie_episodes/%s' % (mid)
                EPISODES = urlparse.urljoin(self.base_link, EPISODES)
                r = self.request(EPISODES)[0]
                r = json.loads(r)['html']
                r = client.parseDOM(r, 'div', attrs={'class': 'pas-list'})
                ids = client.parseDOM(r, 'li', ret='data-id')
                servers = client.parseDOM(r, 'li', ret='data-server')
                labels = client.parseDOM(r, 'a', ret='title')
                r = zip(ids, servers, labels)
                for eid in r:
                    try:
                        try:
                            ep = re.findall('episode.*?(\d+).*?', eid[2].lower())[0]
                        except:
                            ep = 0
                        if (episode is None) or (int(ep) == int(episode)):
                            url = urlparse.urljoin(self.base_link, self.token_link % (eid[0], mid))
                            script = client.request(url)
                            if '$_$' in script:
                                params = self.uncensored1(script)
                            elif script.startswith('[]') and script.endswith('()'):
                                params = self.uncensored2(script)
                            else:
                                raise Exception()
                            u = urlparse.urljoin(self.base_link, self.sourcelink % (eid[0], params['x'], params['y']))
                            r = client.request(u, XHR=True)
                            url = json.loads(r)['playlist'][0]['sources']
                            url = [i['file'] for i in url if 'file' in i]
                            url = [directstream.googletag(i) for i in url]
                            url = [i[0] for i in url if i]
                            for s in url:
                                sources.append({'source': 'gvideo', 'quality': s['quality'], 'url': s['url'],
                                                'provider': 'Solarmovies'})
                    except:
                        pass
            except:
                pass

            return sources

        except Exception as e:
            control.log('ERROR SOLAR %s' % e)
            return sources

    def resolve(self, url):
        return url

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