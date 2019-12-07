#Jor-EL Addon KoDIY

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockers.movie']
        self.base_link = 'https://www2.putlockerr.is'
        self.search_link = '/embed/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except:
            return
		
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('<iframe src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http,host,url in match: 
                    url = '%s://%s/%s' % (http,host,url)
                    sources.append({'source': host,'quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url