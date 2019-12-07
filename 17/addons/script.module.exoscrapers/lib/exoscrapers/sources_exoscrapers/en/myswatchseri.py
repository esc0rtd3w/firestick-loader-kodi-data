# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by Exodus in Exodus.

import re, base64
from exoscrapers.modules import cfscrape
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['swatchseries.to']
        self.base_link = 'https://www1.swatchseries.to'
        self.search_link = '/episode/%s_s%s_e%s.html'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            url = url.replace('-', '_')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = self.base_link + self.search_link % (url, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('cale\.html\?r=(.+?)" class="watchlink" title="(.+?)"').findall(r)
            for url, host in match:
                url  = base64.b64decode(url)
                valid, host = source_utils.is_host_valid(host, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


