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
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib.libraries import jsunpack



class source:
    def __init__(self):
        self.base_link = 'http://watchonline.pro'

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
        #                        try: sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'provider': 'Onlinemovies','url': i})
        try:
            sources = []

            if url == None: return sources
            url = url.replace('+','-')

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                if 'tvshowtitle' in data:
                    url = '%s/episode/%s-s%02de%02d/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']), int(data['episode']))
                    year = re.findall('(\d{4})', data['premiered'])[0]

                    url = client.request(url, output='geturl')
                    if url == None: raise Exception()

                    r = client.request(url)

                    y = client.parseDOM(r, 'span', attrs = {'class': 'date'})
                    y += [i for i in client.parseDOM(r, 'div', attrs = {'class': 'metadatac'}) if 'date' in i]
                    y = re.findall('(\d{4})', y[0])[0]
                    if not y == year: raise Exception()

                else:
                    #url = '%s/watch/%s-%s/' % (self.base_link, cleantitle.geturl(data['title']), data['year'])
                    url = '%s/%s-%s/' % (self.base_link, cleantitle.geturl(data['title']), data['year'])

                    url = client.request(url, output='geturl')
                    if url == None: raise Exception()

                    r = client.request(url)

            else:
                url = urlparse.urljoin(self.base_link, url)

                r = client.request(url)


            links = client.parseDOM(r, 'iframe', ret='src')

            for link in links:
                try:
                    url = link.replace('\/', '/')
                    url = client.replaceHTMLCodes(url)
                    url = 'http:' + url if url.startswith('//') else url
                    url = url.encode('utf-8')

                    if not '.php' in url: raise Exception()

                    r = client.request(url, timeout='10')

                    s = re.compile('<script>(.+?)</script>', re.DOTALL).findall(r)

                    for i in s:
                        try: r += jsunpack.unpack(i)
                        except: pass

                    r = re.findall('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')', r)

                    for i in r:
                        try: sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'provider': 'Onlinemovies', 'url': i})
                        except: pass
                except:
                    pass

            return sources
        except Exception as e:
            control.log('ERROR onlinemovies %s' % e)
            return sources



    def resolve(self, url):
        return client.googlepass(url)


