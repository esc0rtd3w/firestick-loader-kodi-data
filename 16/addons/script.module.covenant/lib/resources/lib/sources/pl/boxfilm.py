# -*- coding: utf-8 -*-

'''
    Covenant Add-on
    Copyright (C) 2017 homik

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
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['boxfilm.pl']
        
        self.base_link = 'http://www.boxfilm.pl'
        self.search_link = '/szukaj'
        
    def movie(self, imdb, title, localtitle, aliases, year):
        try:

            url = urlparse.urljoin(self.base_link, self.search_link)
            r = client.request(url, redirect=False, post={'szukaj' :cleantitle.query(localtitle)})
            r = client.parseDOM(r, 'div', attrs={'class':'video_info'})
            
            local_simple = cleantitle.get(localtitle)            
            for row in r:                
                name_found = client.parseDOM(row, 'h1')[0]
                year_found = name_found[name_found.find("(") + 1:name_found.find(")")]                        
                if cleantitle.get(name_found) == local_simple and year_found == year:
                    url = client.parseDOM(row, 'a', ret='href')[0]               
                    return url
        except:
            return       
  
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return None


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return None

    def get_lang_by_type(self, lang_type):
        if 'LEKTOR' in lang_type:
            return 'pl', 'Lektor'
        if  'DUBBING' in lang_type: 
            return 'pl', 'Dubbing'
        if 'NAPIS' in lang_type :
            return 'pl', 'Napisy'
        return 'en', None
    
    def sources(self, url, hostDict, hostprDict):
        
        sources = []
        try:

            if url == None: return sources            
            result = client.request(urlparse.urljoin(self.base_link, url), redirect=False)
            
            section = client.parseDOM(result, 'section', attrs={'id':'video_player'})[0]
            link = client.parseDOM(section, 'iframe', ret='src')[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            if not valid: return sources
            spans = client.parseDOM(section, 'span')
            info = None
            for span in spans:
                if span == 'Z lektorem':
                    info = 'Lektor'

            q = source_utils.check_sd_url(link)
            sources.append({'source': host, 'quality':q, 'language': 'pl', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            
            return sources
        except:
            return sources
    
    def resolve(self, url):
        return url
        
