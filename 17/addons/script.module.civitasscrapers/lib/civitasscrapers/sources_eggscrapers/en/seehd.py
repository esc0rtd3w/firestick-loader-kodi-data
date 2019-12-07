# -*- coding: utf-8 -*-

'''
    Eggman Add-on

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

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import cfscrape

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['seehd.pl']
        self.base_link = 'http://www.seehd.pl'
        self.search_link = '/%s-%s-watch-online/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_link % (title,year)
            return url
        except:
            return
			
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            title = url
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
            se = 's%se%s' % (season,episode)
            url = self.base_link + self.search_link % (title,se)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).content
            try:
                match = re.compile('<iframe.+?src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http,host,url in match: 
                    host = host.replace('www.','')
                    url = '%s://%s/%s' % (http,host,url)
                    if 'seehd' in host: pass
                    else: sources.append({'source': host,'quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url