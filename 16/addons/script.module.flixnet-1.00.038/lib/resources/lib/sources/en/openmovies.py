# -*- coding: utf-8 -*-

'''
    Flixnet Add-on

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

import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import jsunpack
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['openloadmovies.net', 'openloadmovies.tv', 'openloadmovies.org', 'openloadmovies.co']
        self.base_link = 'http://openloadmovies.tv'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(title))
            r = client.request(url)
            r = client.parseDOM(r, 'div', attrs={'class': 'title'})
            r = [zip(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in r]
            r = [i[0] for i in r]
            r = [i[0] for i in r if (cleantitle.get(title) in cleantitle.get(i[1]))][0]
            url = {'imdb': imdb, 'title': title, 'year': year, 'url': r, 'headers': headers}
            url = urllib.urlencode(url)
            return url
        except:
            try:
                url =  '%s/movies/%s-%s/' % (self.base_link, cleantitle.geturl(title),year)
                url = client.request(url, output='geturl')
                if url == None or not cleantitle.geturl(title) in url:
                    url =  '%s/movies/%s/' % (self.base_link, cleantitle.geturl(title))
                    url = client.request(url, output='geturl')
                    if url == None or not cleantitle.geturl(title) in url: raise Exception
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

            if 'tvshowtitle' in data:
                url = '%s/episodes/%s-%01dx%01d/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']), int(data['episode']))
                year = re.findall('(\d{4})', data['premiered'])[0]
                url = client.request(url, output='geturl')
                if url == None: raise Exception()

                r = client.request(url)

                y = client.parseDOM(r, 'span', attrs = {'class': 'date'})[0]

                y = re.findall('(\d{4})', y)[0]
                if not y == year: raise Exception()

            else:
                url = client.request(url, output='geturl')
                if url == None: raise Exception()

                r = client.request(url)


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
                            {'source': 'openload.co', 'quality': 'SD', 'language': 'en', 'url': link, 'direct': False,
                             'debridonly': False})
                        raise Exception()
                    elif 'putstream' in link:
                        r = client.request(link)
                        r = re.findall(r'({"file.*?})',r)
                        for i in r:
                             try:
                                i = json.loads(i)
                                url = i['file']
                                q = source_utils.label_to_quality(i['label'])                           
                                if 'google' in url:
                                    valid, hoster = source_utils.is_host_valid(url, hostDict)
                                    urls, host, direct = source_utils.check_directstreams(url, hoster)
                                    for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
             
                                else:
                                    valid, hoster = source_utils.is_host_valid(url, hostDict)
                                    if not valid:
                                        if 'blogspot' in hoster or 'vidushare' in hoster:
                                            sources.append({'source': 'CDN', 'quality': q, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                                            continue
                                        else: continue
                                    sources.append({'source': hoster, 'quality': q, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})                            
                                
                             except:
                                pass

                except:
                    pass

                try:
                    url = link.replace('\/', '/')
                    url = client.replaceHTMLCodes(url)
                    url = 'http:' + url if url.startswith('//') else url
                    url = url.encode('utf-8')

                    if not '/play/' in url: raise Exception()

                    r = client.request(url, timeout='10')

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
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url



