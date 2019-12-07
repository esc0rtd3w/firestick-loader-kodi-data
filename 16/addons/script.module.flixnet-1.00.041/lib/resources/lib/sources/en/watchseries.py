# -*- coding: utf-8 -*-

'''
    Exodus Add-on

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


import re,urllib,urlparse,json,base64,xbmc

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
from resources.lib.modules import directstream

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['watch-series.co','watch-series.ru', 'watch-series.io']
        self.base_link = 'https://watch-series.io'
        self.search_link = '/search.html?keyword=%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            data = {'tvshowtitle': tvshowtitle, 'year': year}
            return urllib.urlencode(data)

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            data.update({'season': season, 'episode': episode, 'title': title, 'premiered': premiered})

            return urllib.urlencode(data)

        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)

            url = self.__get_episode_url(data)

            result = client.request(url)

            dom = re.findall('data-video="(.+?)"', result)
            urls = [i if i.startswith('https') else 'https:' + i for i in dom]

            for url in urls:
                if 'vidnode.net' in url:
                    link = url
                    files = []

                    while True:
                        try:
                            try:r = client.request(link)
                            except: continue

                            files.extend(re.findall("(?!file: '.+?',label: 'Auto')file: '(.+?)',label: '(.+?)'", r))

                            link = re.findall('window\.location = \"(.+?)\";', r)[0]

                            if not 'vidnode' in link:
                                break

                        except Exception:
                            break

                    for i in files:
                        try:
                            video = i[0]
                            quality = i[1]
                            host = 'CDN'

                            if 'google' in video or 'blogspot' in video:
                                pass

                            sources.append({
                                'source': host,
                                'quality': source_utils.label_to_quality(quality),
                                'language': 'en',
                                'url': video,
                                'direct': True,
                                'debridonly': False
                            })

                        except:
                            pass

                else:
                    try:
                        host = urlparse.urlparse(link.strip().lower()).netloc

                        if not host in hostDict: raise Exception()

                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')

                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                    except:
                        pass

            return sources

        except:
            return sources

    def resolve(self, url):
        return url


    def __get_episode_url(self, data):
        try:
            path = self.search_link % urllib.quote_plus(cleantitle.query(data['tvshowtitle']))
            url = urlparse.urljoin(self.base_link, path)

            xbmc.log('__get_episode_url start url: ' + str(url))

            response = client.request(url)

            exp = 'href="([^"]+?)".+?videoHname.+?title="%s - Season %s"' % (data['tvshowtitle'], data['season'])
            get_season = re.findall(exp, response, flags=re.I)[0]
            url = urlparse.urljoin(self.base_link, get_season + '/season')

            xbmc.log('__get_episode_url season url: ' + str(url))

            response = client.request(url)

            exp = 'href="([^"]+?)" title="(.+?Episode (?:%02d|%s):.+?)".+?videoHname' % (int(data['episode']), data['episode'])
            episode = re.findall(exp, response)[0][0]
            url = urlparse.urljoin(self.base_link, episode)

            xbmc.log('__get_episode_url episode url: ' + str(url))

            return url

        except Exception:
            return
