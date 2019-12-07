#Jor-EL Addon KoDIY

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['uktv.co.uk']
        self.base_link = 'https://uktvplay.uktv.co.uk'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            http = 'https://uktvplay.uktv.co.uk/shows/' + url + '/watch-online/'
            r = client.request(http)
            try:
                match = re.compile('Series ' + season + ', \n            Episode ' + episode + '.+?<h5 class="teaser-title" itemprop="name">.+?<a href="/shows/' + url + '/watch-online/\?video=(.+?)" class="series-episode vod-play-episode" title="Watch Series ' + season + ', Episode ' + episode + ' of',re.DOTALL).findall(r)
                for url in match: return url
            except:
                return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            url = 'http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=' + url
            sources.append({'source': 'Official','quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False}) 
            return sources
        except Exception:
            return

    def resolve(self, url):
        return url