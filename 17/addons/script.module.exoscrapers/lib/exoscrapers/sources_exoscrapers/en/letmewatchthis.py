# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by Exodus in Exodus.

import re
from exoscrapers.modules import client
from exoscrapers.modules import cleantitle
from exoscrapers.modules import jsunpack
from exoscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['letmewatchthis.fun']
        self.base_link = 'http://m.letmewatchthis.fun'
        self.search_link = '/?search&search_keywords=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = self.base_link + self.search_link % (search_id.replace(' ', '+').replace('-', '+').replace('++', '+'))
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            items = client.parseDOM(page, 'div', attrs={'class': 'index_item index_item_ie'})
            for item in items:
                match = re.compile('<a href="(.+?)" title="(.+?)">', re.DOTALL).findall(item)
                for row_url, row_title in match:
                    if cleantitle.get(title) in cleantitle.get(row_title) and year in str(row_title):
                        row_url = self.base_link + row_url
                        return row_url
            return
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(tvshowtitle)
            url = self.base_link + self.search_link % (search_id.replace(' ', '+').replace('-', '+').replace('++', '+'))
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            items = client.parseDOM(page, 'div', attrs={'class': 'index_item index_item_ie'})
            for item in items:
                match = re.compile('<a href="(.+?)" title="(.+?)">', re.DOTALL).findall(item)
                for row_url, row_title in match:
                    if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
                        return row_url
            return
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url.replace('/watch-', '/tv-').replace('-online', '',)
            url = self.base_link + url + '/season-' + season + '-episode-' + episode
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            links = client.parseDOM(page, 'table', attrs={'class': 'movie_version'})
            for link in links:
                try:
                    qual = re.compile('<span class="quality_(.+?)"></span>', re.DOTALL).findall(link)[0]
                    hoster = re.compile('<span class="version_host">(.+?)</span>', re.DOTALL).findall(link)[0]
                    href = re.compile('<a href="(.+?)" class=', re.DOTALL).findall(link)[0]
                    vlink = self.base_link + href
                    valid, host = source_utils.is_host_valid(hoster, hostDict)
                    if valid and host not in str(sources):
                        quality, info = source_utils.get_release_quality(qual, qual)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': vlink, 'info': info, 'direct': False, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            unpacked = self.unpacked(url)
            if unpacked:
                link = re.compile("'http(.+?)\'", re.DOTALL).findall(unpacked)[0]
                url = 'http' + client.replaceHTMLCodes(link)
            return url
        except:
            return


    def unpacked(self, url):
        try:
            unpacked = ''
            html = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            if jsunpack.detect(html):
                unpacked = jsunpack.unpack(html)
            return unpacked
        except:
            return


