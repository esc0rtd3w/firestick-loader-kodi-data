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
from resources.lib.libraries import pyaes as pyaes
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://playboxhd.com'
        self.search_link = '/api/box?type=search&os=Android&v=291.0&k=0&keyword=%s'
        self.sources_link = '/api/box?type=detail&id=%s&os=Android&v=291.0&k=0&al=key'
        self.stream_link = '/api/box?type=stream&id=%s&os=Android&v=291.0'

    def get_movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return None

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
            url['title'],  url['season'], url['episode'], url['premiered'] = title, season, episode, premiered
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #sources.append({'source': host.split('.')[0], 'quality': 'SD', 'provider': 'Movie25', 'url': url})
        sources = []

        try:
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            result = client.request(query, mobile=True, timeout=20, output='extended')
            r = json.loads(result[0])
            r = r['data']['films']

            years = [str(data['year']), str(int(data['year']) + 1), str(int(data['year']) - 1)]

            print r
            if 'episode' in data:
                r = [i for i in r if cleantitle.get(title) == cleantitle.get(i['title'])]
                r = [(i,re.sub('[^0-9]', '', str(i['publishDate']))) for i in r ]
                for i in r:
                    print i[0]['id'], i[0]['publishDate'], i[0]['title'], i[1]
                r = [i[0] for i in r if any(x in i[1] for x in years)][0]
                result = client.request(urlparse.urljoin(self.base_link, self.sources_link % r['id']), mobile=True, headers=result[4], output='extended')
                r = json.loads(result[0])
                r = [i for i in r['data']['chapters'] if i['title'].replace('0','').lower() == 's%se%s' %(data['season'],data['episode'])][0]


            else:
                r = [i for i in r if cleantitle.get(title) == cleantitle.get(i['title'])]
                r = [i for i in r if any(x in i['publishDate'] for x in years)][0]
                print r
                result = client.request(urlparse.urljoin(self.base_link, self.sources_link % r['id']), mobile=True, headers=result[4], output='extended')
                r = json.loads(result[0])
                r = r['data']['chapters'][0]
                #self.stream_link % r['data']['chapters'][0]

            result = client.request(urlparse.urljoin(self.base_link, self.stream_link % r['id']), mobile=True,
                                    headers=result[4], output='extended')
            r = json.loads(result[0])

            r = [(i['quality'], i['server'], self._decrypt(i['stream'])) for i in r['data']]

            for i in r:
                if 'google' in i[2]:
                    sources.append({'source': 'gvideo', 'quality': client.googletag(i[2])[0]['quality'],
                                            'url': i[2], 'provider': 'Cinemabox'})
                elif 'freemovietube' in i[2]:
                    pass
                else:
                    try:
                        try:
                            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(i[2].strip().lower()).netloc)[0]
                        except:
                            host='cdn'
                        if not host in hostDict: raise Exception()
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')

                        sources.append({'source': host, 'quality': 'SD', 'url': i[2], 'provider': 'Cinemabox'})
                    except:
                        pass

            return sources
        except Exception as e:
            control.log('ERROR Boby %s' % e)
            return sources

    def resolve(self, url):
        control.log('Cinema resolve %s' % url)
        if 'google' in url:
            return client.googlepass(url)
        else:
            return  resolvers.request(url)

    def _decrypt(self,url):
        import base64
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(base64.urlsafe_b64decode('cXdlcnR5dWlvcGFzZGZnaGprbHp4YzEyMzQ1Njc4OTA='), '\0' * 16))
        url = base64.decodestring(url)
        url = decrypter.feed(url) + decrypter.feed()
        return url