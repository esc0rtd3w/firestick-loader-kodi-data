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


import re,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser2

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviego.cc']
        self.base_link = 'http://moviego.cc'
        self.search_link = 'index.php?do=search'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            search_url = urlparse.urljoin(self.base_link, self.search_link)
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s+%s' % (clean_title.replace('-','+'), year))
            r = client.request(search_url, post=post)
            r = dom_parser2.parse_dom(r, 'article', {'class': ['shortstory','cf']})[0]
            r = dom_parser2.parse_dom(r.content, 'a', req='href')[0]
            url = r.attrs['href']
            return url
        except Exception:
            return
            
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []          
            r = client.request(url)
            r = dom_parser2.parse_dom(r, 'div', {'class': 'tab_box'})[0]
            r = dom_parser2.parse_dom(r.content, 'iframe', req='src')[0]
            url = r.attrs['src']
            if r:
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if host in hostDict:
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        sources.append({
                            'source': host,
                            'quality': 'SD',
                            'language': 'en',
                            'url': url.replace('\/','/'),
                            'direct': False,
                            'debridonly': False
                        })
                except: pass
            return sources
        except Exception:
            return

    def resolve(self, url):
        return url
