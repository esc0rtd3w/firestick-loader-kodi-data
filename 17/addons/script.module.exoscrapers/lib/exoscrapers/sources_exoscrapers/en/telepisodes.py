# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by Exodus in Exodus.

import re
from exoscrapers.modules import client
from exoscrapers.modules import cleantitle
from exoscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['telepisodes.org']
        self.base_link = 'https://telepisodes.org'
        self.tvshow_link = '/tv-series/%s/season-%s/episode-%s/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = self.base_link + self.tvshow_link % (url, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            page = client.request(url, headers=self.headers)
            match = re.compile('rel="nofollow ugc" title="(.+?)" target="_blank" href="(.+?)">', flags=re.DOTALL|re.IGNORECASE).findall(page)
            for hoster, url in match:
                url = self.base_link + url
                valid, host = source_utils.is_host_valid(hoster, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            page2 = client.request(url, headers=self.headers)
            match2 = re.compile('href="/open/site/(.+?)"', flags=re.DOTALL|re.IGNORECASE).findall(page2)
            for link in match2:
                link = self.base_link + "/open/site/" + link
                link = client.request(link, timeout='10', output='geturl')
                return link
        except:
            return


