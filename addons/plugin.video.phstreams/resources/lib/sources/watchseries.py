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


import re,urllib,urlparse,json,base64,hashlib,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['watchseries.ag']
        self.base_link = 'aHR0cDovL3dzLm1n'
        self.hash_link = 'MzI4aiUlR3VTKiVzZkEyNDMxNDJmbyMyMyUl'
        self.search_link = 'L2pzb24vc2VhcmNoLyVz'
        self.agent_link = 'V1MgTW9iaWxl'


    def request(self, url):
        try:
            r = self.request_call(url)
            if r == None: time.sleep(1) ; r = self.request_call(url)
            if r == None: time.sleep(1) ; r = self.request_call(url)
            return r
        except:
            return


    def request_call(self, url):
        try:
            if not url.startswith('/'): url = '/' + url
            if not url.startswith('/json'): url = '/json' + url

            hash = hashlib.md5()
            hash.update(base64.b64decode(self.hash_link) % url)

            url = urlparse.urljoin(base64.b64decode(self.base_link), hash.hexdigest() + url)

            result = client.request(url, headers={'User-Agent': base64.b64decode(self.agent_link)})
            result = json.loads(result)['results'].values()
            return result
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            query = base64.b64decode(self.search_link) % urllib.quote_plus(cleantitle.query(tvshowtitle))

            result = self.request(query)

            tvshowtitle = cleantitle.get(tvshowtitle)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]

            result = [i for i in result if any(x in str(i['year']) for x in years)]

            match = [i['href'] for i in result if tvshowtitle == cleantitle.get(i['name'])]
            match = [i['href'] for i in result if tvshowtitle == cleantitle.get(i['name']) and str(year) == str(i['year'])]

            match2 = [i['href'] for i in result]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    if imdb in str(self.request(i)[0]['imdb']): url = i ; break
                except:
                    pass

            url = '/' + url.split('/json/')[-1]
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            result = self.request(url)

            result = result[0]['episodes'].values()

            for i, v in enumerate(result):
                try: result[i] = v.values()
                except: pass

            result = [i for i in result if type(i) == list]
            result = sum(result, [])
            result = [i for i in result if i['hasLinks'] == True]

            title = cleantitle.get(title)
            premiered = re.compile('(\d{4})-(\d{2})-(\d{2})').findall(premiered)[0]
            premiered = '%s/%s/%s' % (premiered[2], premiered[1], premiered[0])

            url = [i for i in result if title == cleantitle.get(i['name']) and premiered == i['release']][:1]
            if len(url) == 0: url = [i for i in result if premiered == i['release']]
            if len(url) == 0 or len(url) > 1: url = [i for i in result if '_s%01d_e%01d' % (int(season), int(episode)) in i['url']]

            url = '/' + url[0]['url'].split('/json/')[-1]
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            result = self.request(url)

            links = result[0]['links']
            links = [i['url'] for i in links if i['lang'] == 'English']

            for i in links:
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    url = i.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


