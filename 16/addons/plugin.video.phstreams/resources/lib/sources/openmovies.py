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

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import jsunpack

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['openloadmovies.net', 'openloadmovies.tv', 'openloadmovies.org', 'openloadmovies.co']
        self.base_link = 'http://openloadmovies.org'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(title))
            headers = {'Referer': url, 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
            cookie = client.request(url, headers=headers, output='cookie')
            cookie += client.request(url, headers=headers, cookie=cookie, output='cookie')
            client.request(url, headers=headers, cookie=cookie)
            cookie += '; '+ headers['Cookie']
            headers = {'Referer': url, 'Cookie': cookie, 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
            r = client.request(url, headers=headers)
            r = client.parseDOM(r, 'div', attrs={'class': 'title'})
            r = [zip(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [i[0] for i in r]
            r = [i[0] for i in r if (cleantitle.get(title) in cleantitle.get(i[1]))][0]
            url = {'imdb': imdb, 'title': title, 'year': year, 'url': r, 'headers': headers}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
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


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            headers = eval(data['headers'])

            if 'tvshowtitle' in data:
                url = '%s/episodes/%s-%01dx%01d/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']), int(data['episode']))
                year = re.findall('(\d{4})', data['premiered'])[0]
                url = client.request(url, headers=headers, output='geturl')
                if url == None: raise Exception()

                r = client.request(url, headers=headers)

                y = client.parseDOM(r, 'span', attrs = {'class': 'date'})[0]

                y = re.findall('(\d{4})', y)[0]
                if not y == year: raise Exception()

            else:
                url = data['url']
                url = client.request(url, headers=headers, output='geturl')
                if url == None: raise Exception()

                r = client.request(url, headers=headers)


            try:
                result = re.findall('sources\s*:\s*\[(.+?)\]', r)[0]
                r = re.findall('"file"\s*:\s*"(.+?)"', result)

                for url in r:
                    try:
                        url = url.replace('\\', '')
                        url = directstream.googletag(url)[0]
                        sources.append({'source': 'gvideo', 'quality': url['quality'], 'language': 'en', 'url': url['url'], 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

            links = client.parseDOM(r, 'iframe', ret='src')

            for link in links:
                try:
                    if 'openload.io' in link or 'openload.co' in link or 'oload.tv' in link:
                        sources.append(
                            {'source': 'openload.co', 'quality': 'HD', 'language': 'en', 'url': link, 'direct': False,
                             'debridonly': False})
                        raise Exception()
                except:
                    pass

                try:
                    url = link.replace('\/', '/')
                    url = client.replaceHTMLCodes(url)
                    url = 'http:' + url if url.startswith('//') else url
                    url = url.encode('utf-8')

                    if not '/play/' in url: raise Exception()

                    r = client.request(url, headers=headers, timeout='10')

                    s = re.compile('<script type="text/javascript">(.+?)</script>', re.DOTALL).findall(r)

                    for i in s:
                        try:
                            r += jsunpack.unpack(i)
                        except:
                            pass

                    try:
                        result = re.findall('sources\s*:\s*\[(.+?)\]', r)[0]
                        r = re.findall('"file"\s*:\s*"(.+?)"', result)

                        for url in r:
                            try:
                                url = url.replace('\\', '')
                                url = directstream.googletag(url)[0]
                                sources.append({'source': 'gvideo', 'quality': url['quality'], 'language': 'en', 'url': url['url'], 'direct': True, 'debridonly': False})
                            except:
                                pass
                    except:
                        pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return directstream.googlepass(url)


