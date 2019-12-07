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


import re,urllib,urlparse,json


from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import control
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['allrls.me']
        self.base_link = 'http://allrls.me'
        self.search_link = '?s=%s+%s&go=Search'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            if debrid.status() == False: raise Exception()
            url = urlparse.urljoin(self.base_link, '%s-%s' % (cleantitle.geturl(title), year))
            url = client.request(url, output='geturl')
            if url == None: 
                url = urlparse.urljoin(self.base_link, '%s' % (cleantitle.geturl(title)))
                url = client.request(url, output='geturl')
            if url == None: raise Exception()
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() == False: raise Exception()
        return tvshowtitle

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.urljoin(self.base_link, '%s-s%02de%02d' % (cleantitle.geturl(url), int(season), int(episode)))
            url = client.request(url, output='geturl')
            print url
            if url == None: raise Exception()
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
      
            hostDict = hostprDict + hostDict

            r = client.request(url)           

            urls = client.parseDOM(r, 'a', ret = 'href')

            for url in urls:
                try:

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    
                    if any(x in url for x in ['.rar', '.zip', '.iso']): raise Exception()
                    
                    quality, infoo = source_utils.get_release_quality(url)
                    
                    info = []
                    
                    if any(x in url.upper() for x in ['HEVC', 'X265', 'H265']): info.append('HEVC')
                    
                    info.append('ALLRLS')
                    
                    info = ' | '.join(info)
                    
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                     
                except:
                    pass

            return sources
        except:
            return

    def resolve(self, url):
        return url
