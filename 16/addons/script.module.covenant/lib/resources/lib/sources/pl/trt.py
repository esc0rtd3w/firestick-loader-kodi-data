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


import re, urllib, urlparse, base64, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['trt.pl']
        
        self.base_link = 'http://www.trt.pl/'
        self.search_link = 'szukaj-filmy/%s'
           
    def movie(self, imdb, title, localtitle, aliases, year):
        return title + ' ' + year
    
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return tvshowtitle;

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return url + ' s' + season.zfill(2) + 'e' + episode.zfill(2)
        
    def contains_word(self, str_to_check, word):
        return re.search(r'\b' + word + r'\b', str_to_check, re.IGNORECASE)
    
    def contains_all_wors(self, str_to_check, words):
        for word in words:
            if not self.contains_word(str_to_check, word):
                return False
        return True
    
    def sources(self, url, hostDict, hostprDict):
        try:
                                    
            words = cleantitle.getsearch(url).split(' ')
                            
            search_url = urlparse.urljoin(self.base_link, self.search_link) % urllib.quote_plus(url);
            result = client.request(search_url)

            sources = []
            
            result = client.parseDOM(result, 'div', attrs={'class':'tile-container'})
            for el in result :                      
                
                main = client.parseDOM(el, 'h3');
                
                link = client.parseDOM(main, 'a', ret='href')[0];
                found_title = client.parseDOM(main, 'a')[0];                      
                   
                if not self.contains_all_wors(found_title, words):
                    continue
                
                quality = client.parseDOM(el, 'a', attrs={'class':'qualityLink'});
                q = 'SD'
                if quality:
                    if(quality[0] == '720p'):
                        q='HD'
                    if(quality[0]=='1080p'):
                        q='1080p'                        
                                                              
                lang, info = self.get_lang_by_type(found_title)
                 
                sources.append({'source': 'trt', 'quality': q, 'language': lang, 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            
            return sources
        except:
            return sources
        
    def get_lang_by_type(self, lang_type):
        if self.contains_word(lang_type, 'lektor') :
            return 'pl', 'Lektor'
        if self.contains_word(lang_type, 'Dubbing') :        
            return 'pl', 'Dubbing'
        if self.contains_word(lang_type, 'Napisy') :        
            return 'pl', 'Napisy'
        if self.contains_word(lang_type, 'Polski') :         
            return 'pl', None
        return 'en', None

    def resolve(self, url):
        try:
            return urlparse.urljoin(self.base_link, url);
        except:
            return
