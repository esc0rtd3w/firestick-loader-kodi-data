# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by Exodus in Exodus.

import re
from exoscrapers.modules import client
from exoscrapers.modules import cleantitle
from exoscrapers.modules import more_sources


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['couchtuner2.com']
        self.base_link = 'https://couchtuner2.com'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movietitle = cleantitle.geturl(title)
            url = self.base_link + '/%s/' % movietitle
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
            if url == None:
                return
            tvshowtitle = url
            url = self.base_link + '/episode/%s-season-%s-episode-%s/' % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            sourcePage = client.request(url)
            links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(sourcePage)
            for link in links:
                for source in more_sources.getMore(link, hostDict):
                    sources.append(source)
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


