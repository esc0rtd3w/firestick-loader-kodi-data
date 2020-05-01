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

from resources.lib.modules import source_utils, dom_parser, client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['filmwebbooster.pl']
        
        self.base_link = 'http://178.19.110.218/filmweb/'
        self.search_more = 'wiecejzrodel.php'
        self.search_tvshow = 'search.php'
        self.search_movie = 'search_film.php'          

    def create_search_more(self, title, localtitle, year):
        return {'tytul':localtitle, 'engTitle':title, 'rok':year}

    def movie(self, imdb, title, localtitle, aliases, year):
        result = {}
        result['url'] = urlparse.urljoin(self.base_link, self.search_movie)
        result['post'] = {'engTitle':title, 'szukany':localtitle, 'rok':year}
        result['more'] = self.create_search_more(title, localtitle, year)
        return result
    
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        result = {}
        result['url'] = urlparse.urljoin(self.base_link, self.search_tvshow)
        result['post'] = {'title':localtvshowtitle}
        result['more'] = self.create_search_more(tvshowtitle, localtvshowtitle, year)
        return result

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        url['more']['se'] = season + '-' + episode
        url['post']['odcinek'] = episode
        url['post']['sezon'] = season
        return url
           

    def get_info_from_others(self, sources):
        infos = []
        for source in sources:
            info = source['info']
            if info :
                infos.append(info)
        infos.sort()
        if infos:            
            return infos[0]
        return ''
    
    def sources(self, url, hostDict, hostprDict):
        try:                                      
            search_url = url['url'] 
            post = url['post']
            search_more_post = url['more']
            result = client.request(search_url, post=post)
                   
            sources = []
            if not result.startswith('http'):
                return sources
            
            valid, host = source_utils.is_host_valid(result, hostDict)
            q = source_utils.check_sd_url(result)
            first_found = {'source': host, 'quality': q, 'language': 'pl', 'url': result, 'info': '', 'direct': False, 'debridonly': False}        
           
            search_url = urlparse.urljoin(self.base_link, self.search_more)
            result = client.request(search_url, post=search_more_post)
            result = dom_parser.parse_dom(result, 'a')            
            for el in result :
                desc = el.content
                info = desc[desc.find("(") + 1:desc.find(")")]
                lang = 'pl'
                if info.lower() == 'eng':
                    lang='en'
                    info=None
                link = el.attrs['href']                                 
                
                valid, host = source_utils.is_host_valid(link, hostDict)
                if not valid: continue
                q = source_utils.check_sd_url(link)
                
                sources.append({'source': host, 'quality': q, 'language': lang, 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            
            first_found['info'] = self.get_info_from_others(sources)
            sources.append(first_found)
            
            return sources
        except:
            return sources
        
    def resolve(self, url):
        return url        
