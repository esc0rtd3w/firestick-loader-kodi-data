# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 12-31-2018 by Exodus.
#Created by Tempest

import re,requests
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movieshub.vip']
        self.base_link = 'https://123movieshub.vip'
        self.search_link = '/film/%s'


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
            r = requests.get(url).content
            qual = re.compile('class="quality">(.+?)<').findall(r)
            for i in qual:
                if '1080' in i:
                    quality = '1080p'
                elif '720' in i:
                    quality = '720p'
                else:
                    quality = 'SD'
            u = client.parseDOM(r, "div", attrs={"class": "pa-main anime_muti_link"})
            for t in u:
                u = re.findall('<li class=".+?" data-video="(.+?)"', t)
                for url in u:
                    if 'vidcloud' in url:
                        url = 'https:' + url
                        r = requests.get(url).content
                        t = re.findall('li data-status=".+?" data-video="(.+?)"', r)
                        for url in t:
                            if 'vidcloud' in url:
                                continue
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                    if 'vidcloud' in url:
                        continue
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return


    def resolve(self, url):
        return url

