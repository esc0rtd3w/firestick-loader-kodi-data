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


import urllib, urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['openkatalog.com']
        
        self.base_link = 'https://openkatalog.com'
        self.search_link = '/?s=%s'
        self.video_tab = '?tab=video'
        
    def movie(self, imdb, title, localtitle, aliases, year):
        return self.search(localtitle, year)

    
    def search(self, localtitle, year):
        try:
            simply_name = cleantitle.get(localtitle)

            query = self.search_link % urllib.quote_plus(cleantitle.query(localtitle))
            query = urlparse.urljoin(self.base_link, query)
            result = client.request(query)

            result = client.parseDOM(result, 'article')
          
            for row in result:
                a_href = client.parseDOM(row, 'h3')[0]  
                url = client.parseDOM(a_href, 'a', ret='href')[0] 
                name = client.parseDOM(a_href, 'a')[0]
                name = cleantitle.get(name)
                
                year_found = client.parseDOM(row, 'span', attrs={'class':'dtyear'})
                if year_found:
                    year_found = year_found[0]                
               
                if(name == simply_name and (not year_found or not year or year_found == year)):
                    return url
        except :
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return localtvshowtitle


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        query = url + ' s' + season.zfill(2) + 'e' + episode.zfill(2)
        return self.search(query, None)        

    def get_info_from_desc(self, desc):
        desc_list = desc.split(",")
        host = desc_list.pop(0)
        
        lang = None
        info = None
        q = 'SD'
        
        for el in desc_list:
            if 'napisy' in el:
                info = 'Napisy'
            elif 'lektor' in el:
                info = 'Lektor'
            elif 'dubbing' in el:
                info = 'Dubbing'

            if 'PL' in el:
                lang = 'pl'

            if '720p' in el:
                q = 'HD'
            elif '1080' in el:
                q = '1080p'             
       
        return host, lang, info, q
    
    def sources(self, url, hostDict, hostprDict):
        
        sources = []
        try:

            if url == None: return sources
            url = url + self.video_tab
            result = client.request(url)
                                    
            rows = client.parseDOM(result, 'ul', attrs={'class':'player_ul'})[0]
            rows = client.parseDOM(rows, 'li')        

            for row in rows:
                try:
                    desc = client.parseDOM(row, 'a')[0]
                    link = client.parseDOM(row, 'a', ret='href')[0]            
                    
                    host, lang, info, q = self.get_info_from_desc(desc)

                    sources.append({'source': host, 'quality': q, 'language': lang, 'url': link, 'info': info, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources
    
    def resolve(self, url):
        result = client.request(url)
        result = client.parseDOM(result, 'div', attrs={'class':'embed'})[0]
        result = client.parseDOM(result, 'iframe', ret='src')[0]
        
        return result      
