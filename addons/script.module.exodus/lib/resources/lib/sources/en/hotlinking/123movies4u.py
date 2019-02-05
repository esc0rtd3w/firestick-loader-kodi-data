# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 12-31-2018 by Exodus.
#Created by Tempest

import re
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movies4u.ch']
        self.base_link = 'https://123movies4u.ch'
        self.search_link = '/movie/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.search_link % title
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            r = client.request(url)
            qual = re.compile('<span class="quality">(.+?)<').findall(r)
            if 'DVD' in qual:
                quality = '720p'
            else:
                quality = 'SD'
            u = client.parseDOM(r, "div", attrs={"id": "link_list"})
            for t in u:
                u = client.parseDOM(t, 'a', ret='href')
                for url in u:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if host not in hostDict:
                        continue
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return


    def resolve(self, url):
        return url

