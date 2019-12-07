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
import json
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://watch5s.to'
        self.base_link = 'http://moviefree.to'
        self.search_link = '/watch/%s-%s-online.html'

    def get_movie(self, imdb, title, year):
        try:
            url = self.search_link % (cleantitle.geturl(title), year)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, limit='1')
            r = client.parseDOM(r, 'title')[0]
            if r == '': raise Exception()

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
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
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            s = re.findall('data-film\s*=\s*"(.+?)"\s+data-name\s*=\s*"(.+?)"\s+data-server\s*=\s*"(.+?)"', r)

            h = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}

            for u in s:
                try:
                    if not u[2] in ['1', '11', '4']: raise Exception()
                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/plugins/ipplugins.php')

                    post = {'ipplugins': '1', 'ip_film': u[0], 'ip_name': u[1], 'ip_server': u[2]}
                    post = urllib.urlencode(post)

                    r = client.request(url, post=post, headers=h)
                    r = json.loads(r)

                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/ipplayer/ipplayer.php')

                    post = {'u': r['s'], 'w': '100%', 'h': '500', 's': r['v'], 'n': '0'}
                    post = urllib.urlencode(post)

                    r = client.request(url, post=post, headers=h)
                    r = json.loads(r)

                    try:
                        url = [i['files'] for i in r['data']]
                    except:
                        url = [r['data']]

                    for i in url:
                        try:
                            sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'],
                                            'provider': 'MovieFree','url': i})
                        except:
                            pass

                    if 'openload' in url[0]:
                        sources.append(
                            {'source': 'openload.co', 'quality': 'SD', 'provider': 'MovieFree', 'url': i})
                except:
                    pass

            return sources
        except Exception as e:
            control.log('ERROR moviefree %s' % e)
            return sources



    def resolve(self, url):
        if 'openload' in url: return resolvers.request(url)
        return client.googlepass(url)


