# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 12-03-2018 by Exodus.

import re
from resources.lib.modules import source_utils,cleantitle,debrid,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123moviesfree.ws']
        self.base_link = 'https://www.123moviesfree.ws'
        self.tv_link = '/episode/%s-season-%s-episode-%s'
        self.movie_link = '/%s'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % title
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = cleantitle.geturl(tvshowtitle)
            url = tvshowtitle
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            tvshowtitle = url
            url = self.base_link + self.tv_link % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if debrid.status() == False: raise Exception()
            r = self.scraper.get(url).content
            r = re.findall('<iframe src="(.+?)"', r)
            for url in r:
                valid, host = source_utils.is_host_valid(url, hostDict)
                quality = source_utils.check_sd_url(url)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return


    def resolve(self, url):
        return url

