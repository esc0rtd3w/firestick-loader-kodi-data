# -*- coding: utf-8 -*-

'''
    Covenant Add-on

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
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['http://onlinemovies.is/']
        self.base_link = 'http://onlinemovies.is/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])


             
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
                    valid, hoster = source_utils.is_host_valid(link, hostDict)
                    if not valid: continue
                    urls, host, direct = source_utils.check_directstreams(link, hoster)
                    for x in urls:
                         if x['quality'] == 'SD':
                             try:                                 
                                 if 'HDTV' in x['url'] or '720' in  x['url']: x['quality'] = 'HD'
                                 if '1080' in  x['url']: x['quality'] = '1080p'
                             except:
                                 pass
                    sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
