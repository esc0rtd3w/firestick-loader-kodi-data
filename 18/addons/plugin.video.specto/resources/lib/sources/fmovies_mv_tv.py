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


import re,urllib,urlparse,json, random, time
from resources.lib.libraries import control
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
import base64


class source:
    def __init__(self):
        self.base_link = 'http://fmovies.se/'
        self.search_link = '/sitemap'
        self.search_link2 = 'http://fmovies.to/ajax/film/search?sort=year%3Adesc&funny=1&keyword=%s'
        self.hash_link = '/ajax/episode/info'

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            #X - Requested - With:"XMLHttpRequest"
            return url
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):

        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return None


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):

        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'],  url['season'], url['episode'], url['premiered'] = title, season, episode, date
            url = urllib.urlencode(url)
            return url
        except:
            return

    def fmovies_cache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)
            control.log('>>>>>>>>>>>>---------- CACHE %s' % url)

            #result = client.source(url)
            result = client.request(url)
            result = result.split('>Movies and Series<')[-1]
            control.log('>>>>>>>>>>>>---------- CACHE-2 %s' % result)
            result = client.parseDOM(result, 'ul')[0]
            control.log('>>>>>>>>>>>>---------- CACHE-3 %s' % result)

            result = re.compile('href="(.+?)">(.+?)<').findall(result)

            result = [(re.sub('http.+?//.+?/','/', i[0]), re.sub('&#\d*;','', i[1])) for i in result]
            control.log('>>>>>>>>>>>>---------- CACHE-4 ')

            return result
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):

        try:
            sources = []
            myts = str(((int(time.time())/3600)*3600))

            if url == None: return sources

            if not str(url).startswith('http'):
                try:
                    data = urlparse.parse_qs(url)
                    data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                    title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                    year = re.findall('(\d{4})', data['premiered'])[0] if 'tvshowtitle' in data else data['year']
                    try: episode = data['episode']
                    except: pass

                    query = {'keyword': title, 's':''}
                    search_url = urlparse.urljoin(self.base_link, '/search')
                    search_url = search_url + '?' + urllib.urlencode(query)
                    result = client.request(search_url)


                    r = client.parseDOM(result, 'div', attrs = {'class': '[^"]*movie-list[^"]*'})[0]
                    r = client.parseDOM(r, 'div', attrs = {'class': 'item'})
                    r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', attrs = {'class': 'name'})) for i in r]
                    r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and  len(i[1]) > 0]
                    r = [(re.sub('http.+?//.+?/','/', i[0]), re.sub('&#\d*;','', i[1])) for i in r]

                    if 'season' in data:
                        r = [(i[0], re.sub(' \(\w*\)', '', i[1])) for i in r]
                        #title += '%01d' % int(data['season'])
                        url = [(i[0], re.findall('(.+?) (\d+)$', i[1])) for i in r]
                        url = [(i[0], i[1][0][0], i[1][0][1]) for i in url if len(i[1]) > 0]
                        url = [i for i in url if cleantitle.get(title) in cleantitle.get(i[1])]
                        for i in url:
                            print i[2],i[0],i[1]
                            print '%01d' % int(data['season']) == '%01d' % int(i[2])

                        url = [i for i in url if '%01d' % int(data['season']) == '%01d' % int(i[2])]
                    else:
                        url = [i for i in r if cleantitle.get(title) in cleantitle.get(i[1])]
                    #print("r1", cleantitle.get(title),url,r)


                    url = url[0][0]

                    url = urlparse.urljoin(self.base_link, url)
                    r2 = url.split('.')[-1]


                except:
                    url == self.base_link


            try: url, episode = re.compile('(.+?)\?episode=(\d*)$').findall(url)[0]
            except: pass

            referer = url
            result = client.request(url, limit='0')
            r = client.request(url, limit='0', output='extended')
            cookie1 = r[4] ; headers = r[3] ; r1 = r[0]

            hash_url = urlparse.urljoin(self.base_link, '/user/ajax/menu-bar')
            # int(time.time())
            query = {'ts': myts}
            query.update(self.__get_token(query))
            hash_url = hash_url + '?' + urllib.urlencode(query)
            r = client.request(hash_url, limit='0', output='extended', cookie=cookie1)
            cookie2 = r[4] ; headers = r[3] ; r1 = r[0]

            alina = client.parseDOM(result, 'title')[0]

            atr = [i for i in client.parseDOM(result, 'title') if len(re.findall('(\d{4})', i)) > 0][-1]
            if 'season' in data:
                years = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1)]
                mychk = False
                for y in years:
                    if y in atr: mychk = True
                result = result if mychk ==True else None
            else:
                result = result if year in atr else None

            #print("r3",result)

            try: quality = client.parseDOM(result, 'span', attrs = {'class': 'quality'})[0].lower()
            except: quality = 'hd'
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd' or 'hd ' in quality: quality = 'HD'
            else: quality = 'SD'

            result = client.parseDOM(result, 'ul', attrs = {'data-range-id':"0"})

            servers = []
            #servers = client.parseDOM(result, 'li', attrs = {'data-type': 'direct'})
            servers = zip(client.parseDOM(result, 'a', ret='data-id'), client.parseDOM(result, 'a'))
            servers = [(i[0], re.findall('(\d+)', i[1])) for i in servers]
            servers = [(i[0], ''.join(i[1][:1])) for i in servers]
            #print("r3",servers)

            try: servers = [i for i in servers if '%01d' % int(i[1]) == '%01d' % int(episode)]
            except: pass

            for s in servers[:4]:
                try:

                    headers = {'X-Requested-With': 'XMLHttpRequest'}
                    time.sleep(0.2)
                    hash_url = urlparse.urljoin(self.base_link, self.hash_link)
                    query = {'ts': myts, 'id': s[0], 'update': '0'}

                    query.update(self.__get_token(query))
                    hash_url = hash_url + '?' + urllib.urlencode(query)
                    headers['Referer'] = urlparse.urljoin(url, s[0])
                    headers['Cookie'] = cookie1 + ';' + cookie2 + ';user-info=null; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A3%2C%22TejndEEDj%22%3A%22MTQ4MTM2ODE0NzM0NzQ4NTMyOTAx%22%7D%2C%22C48532%22%3A%7B%22page%22%3A1%2C%22time%22%3A1481368147359%7D%2C%22C77945%22%3A%7B%22page%22%3A1%2C%22time%22%3A1481368147998%7D%2C%22C77947%22%3A%7B%22page%22%3A1%2C%22time%22%3A1481368148109%7D%7D'
                    result = client.request(hash_url, headers=headers, limit='0')
                    print("r101 result",result,headers)

                    time.sleep(0.3)
                    query = {'id': s[0], 'update': '0'}
                    query.update(self.__get_token(query))
                    url = url + '?' + urllib.urlencode(query)
                    #result = client2.http_get(url, headers=headers)
                    result = json.loads(result)
                    quality = 'SD'
                    if s[1] == '1080': quality = '1080p'
                    if s[1] == '720': quality = 'HD'
                    if s[1] == 'CAM': quality == 'CAM'

                    query = result['params']
                    query['mobile'] = '0'
                    query.update(self.__get_token(query))
                    grabber = result['grabber'] + '?' + urllib.urlencode(query)
                    if not grabber.startswith('http'):
                        grabber = 'http:'+grabber

                    result = client.request(grabber, headers=headers, referer=url, limit='0')

                    result = json.loads(result)

                    result = result['data']
                    result = [i['file'] for i in result if 'file' in i]

                    for i in result:
                        if 'google' in i:
                            try:sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'provider': 'Fmovies', 'url': i})
                            except:pass
                        else:
                            try: sources.append({'source': 'gvideo', 'quality': quality, 'provider': 'Fmovies', 'url': i})
                            except: pass
                    control.sleep(410)

                except:
                    pass

            if quality == 'CAM':
                for i in sources: i['quality'] = 'CAM'

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return

    def __get_token_item(self, index2, mykey):
        T = ''
        # for index2 in data:
        if not index2.startswith('_'):
            o = list(range(0, 256))
            i = 0
            for r in range(0, 256):
                i = (i + o[r] + ord(mykey[r % len(mykey)])) % 256
                n = o[r]
                o[r] = o[i]
                o[i] = n
            r = 0
            i = 0
            a = T
            b = 0
            for s in range(0, len(index2)):
                r = (r + 1) % 256
                i = (i + o[r]) % 256
                n = o[r]
                o[r] = o[i]
                o[i] = n
                a = a + unichr(ord(index2[s]) ^ (o[(o[r] + o[i]) % 256]))
                b = b + ord(unichr(ord(index2[s]) ^ (o[(o[r] + o[i]) % 256])))

        print b
        return b
        # return T + a
        # return {'_': str(index1)}


    def __get_token(self,data):
        basickey = base64.decodestring('QlE0QXdCZ1RSenBCYlNLTEI=')
        c = 0
        for i in basickey:
            c = c + ord(i)
        for i in data:
            c = c + self.__get_token_item(data[i], basickey + i)
        # return c
        return {'_': str(c)}

    def __get_xtoken(self):
        url = urlparse.urljoin(self.base_link, 'fghost?%s' % (random.random()))
        html = client.request(url, safe=True)
        k = self.__get_dict('k', html)
        v = self.__get_dict('v', html)
        if k and v:
            data = {}
            l = 0
            while l < len(k):
                for i in k:
                    if k[i] == l:
                        data[k[i]] = v[i]
                        l = len(data)

            token = ''.join([str(data[key]) for key in data])
            rt = str(len(token))
            s = urlparse.urlparse(self.base_link).hostname
            for i, c in enumerate(token):
                rt += '.' + c
                try: nc = str(ord(s[i]))
                except: nc = str(random.randint(0, 5))
                rt += '.' + nc
            return rt

    def __get_dict(self, var, html):
        match = re.search('\s+%s\s*=\s*({[^}]+})' % (var), html)
        if match:
            return eval(match.group(1))
