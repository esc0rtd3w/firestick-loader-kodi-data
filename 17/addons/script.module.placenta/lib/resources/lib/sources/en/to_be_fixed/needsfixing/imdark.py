# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: MuadDib

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['imdark.com']
        self.base_link = 'http://imdark.com'
        self.search_link = '/?s=%s&darkestsearch=8c26461d68&_wp_http_referer=%2F&quality=&genre=&year=&lang=en'
        self.ajax_link = '/wp-admin/admin-ajax.php'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return None

    def sources(self, url, hostDict, locDict):
        sources = []

        try:
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            query = self.search_link % (urllib.quote_plus(title))
            #query = urlparse.urljoin(self.base_link, query)
            query = urlparse.urljoin(self.base_link, self.ajax_link)            
            post = urllib.urlencode({'action':'sufi_search', 'search_string': title})
            
            result = client.request(query)
            r = client.parseDOM(result, 'div', attrs={'id':'showList'})
            r = re.findall(r'<a\s+style="color:white;"\s+href="([^"]+)">([^<]+)', r[0])     
            r = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1]) and data['year'] in i[1]][0]
            url = r[0]                     
            result = client.request(url)
            r = re.findall(r'video\s+id="\w+.*?src="([^"]+)".*?data-res="([^"]+)',result,re.DOTALL)
            
            for i in r:                
                try:
                    q = source_utils.label_to_quality(i[1])
                    sources.append({'source': 'CDN', 'quality': q, 'language': 'en', 'url': i[0], 'direct': True, 'debridonly': False})                
                except:
                    pass

            return sources
        except Exception as e:
            return sources

    def resolve(self, url):
        return url