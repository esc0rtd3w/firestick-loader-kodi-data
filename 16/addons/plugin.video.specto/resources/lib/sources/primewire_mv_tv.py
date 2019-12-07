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


import re,urllib,urlparse,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://www.primewire.ag'
        self.key_link = '/index.php?search'
        self.link_1 = 'http://www.primewire.ag'
        self.link_2 = 'http://www.primewire.org'
        self.link_3 = 'http://www.primewire.is'
        self.moviesearch_link = '/index.php?search_keywords=%s&key=%s&search_section=1'
        self.tvsearch_link = '/index.php?search_keywords=%s&key=%s&search_section=2'
        self.headers = {'Connection' : 'keep-alive'}


    def get_movie(self, imdb, title, year):
        try:
            key = urlparse.urljoin(self.base_link, self.key_link)
            key = client.request(key, 'searchform')
            key = client.parseDOM(key, 'input', ret='value', attrs = {'name': 'key'})[0]

            query = self.moviesearch_link % (urllib.quote_plus(cleantitle.query(title)), key)
            query = urlparse.urljoin(self.base_link, query)

            result = str(client.request(query, 'index_item'))
            if 'page=2' in result or 'page%3D2' in result: result += str(client.request(query + '&page=2', 'index_item'))

            result = client.parseDOM(result, 'div', attrs = {'class': 'index_item.+?'})

            title = 'watch' + cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            r = []
            for i in result:
                u = i[0]
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['u'][0]
                except: pass
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['q'][0]
                except: pass
                r += [(u, i[1])]

            match = [i[0] for i in r if title == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    r = client.request(urlparse.urljoin(self.base_link, i), 'choose_tabs')
                    if imdb in str(r): url = i ; break
                except:
                    pass

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            key = urlparse.urljoin(self.base_link, self.key_link)
            key = client.request(key, 'searchform')
            key = client.parseDOM(key, 'input', ret='value', attrs = {'name': 'key'})[0]

            query = self.tvsearch_link % (urllib.quote_plus(cleantitle.query(tvshowtitle)), key)
            query = urlparse.urljoin(self.base_link, query)

            result = str(client.request(query, 'index_item'))
            if 'page=2' in result or 'page%3D2' in result: result += str(client.request(query + '&page=2', 'index_item'))

            result = client.parseDOM(result, 'div', attrs = {'class': 'index_item.+?'})

            tvshowtitle = 'watch' + cleantitle.get(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            r = []
            for i in result:
                u = i[0]
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['u'][0]
                except: pass
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['q'][0]
                except: pass
                r += [(u, i[1])]

            match = [i[0] for i in r if tvshowtitle == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    r = client.request(urlparse.urljoin(self.base_link, i), 'tv_episode_item')
                    if imdb in str(r): url = i ; break
                except:
                    pass

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url, 'tv_episode_item')
            result = client.parseDOM(result, 'div', attrs = {'class': 'tv_episode_item'})

            title = cleantitle.get(title)

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'tv_episode_name'}), re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in result]
            result = [(i[0], i[1][0], i[2]) for i in result if len(i[1]) > 0] + [(i[0], None, i[2]) for i in result if len(i[1]) == 0]
            result = [(i[0], i[1], i[2][0]) for i in result if len(i[2]) > 0] + [(i[0], i[1], None) for i in result if len(i[2]) == 0]
            result = [(i[0][0], i[1], i[2]) for i in result if len(i[0]) > 0]

            url = [i for i in result if title == cleantitle.get(i[1]) and date == i[2]][:1]
            if len(url) == 0: url = [i for i in result if date == i[2]]
            if len(url) == 0 or len(url) > 1: url = [i for i in result if 'season-%01d-episode-%01d' % (int(season), int(episode)) in i[0]]

            url = client.replaceHTMLCodes(url[0][0])
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
            except: pass
            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url, 'choose_tabs')

            links = client.parseDOM(result, 'tbody')

            for i in links:
                try:
                    url = client.parseDOM(i, 'a', ret='href')[0]
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
                    except: pass
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['url'][0]

                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = client.parseDOM(i, 'span', ret='class')[0]
                    if quality == 'quality_cam' or quality == 'quality_ts': quality = 'CAM'
                    elif quality == 'quality_dvd': quality = 'SD'
                    else:  raise Exception()

                    sources.append({'source': host, 'quality': quality, 'provider': 'Primewire', 'url': url})
                except:
                    pass

            return sources
        except Exception as e:
            control.log('ERROR PRIME %s' % e)
            return sources


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return

