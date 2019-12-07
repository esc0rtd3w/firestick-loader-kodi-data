# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 12-21-2018 by JewBMX in Scrubs.

import re
from resources.lib.modules import cleantitle,source_utils,debrid,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['playmovies.es']
        self.base_link = 'http://playmovies.es'
        self.search_link = '/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_link % title
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if debrid.status() == False: raise Exception()
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).content
            try:
                qual = re.compile('class="quality">(.+?)<').findall(r)
                print qual
                for i in qual:
                    if 'HD' in i:
                        quality = '1080p'
                    else:
                        quality = 'SD'
                match = re.compile('<iframe src="(.+?)"').findall(r)
                for url in match:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host,'quality': quality,'language': 'en','url': url,'direct': False,'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

