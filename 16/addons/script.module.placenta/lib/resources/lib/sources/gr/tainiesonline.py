# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import urllib, urlparse, re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['gr']
        self.domains = ['tainiesonline.top']
        self.base_link = 'http://tainiesonline.top'
        self.search_link = 'search/?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year, 'movies')
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(
                aliases),year, 'movies')
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year, 'series')
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(
                [tvshowtitle] + source_utils.aliases_to_array(aliases), year, 'series')
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = url[:-1] if url.endswith('/') else url
            url += '/seasons/%d/episodes/%d' % (int(season), int(episode))
            return url
        except:
            return

    def __search(self, titles, year, content):
        try:

            query = self.search_link % (urllib.quote_plus(cleantitle.getsearch(titles[0])))

            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i][0] #cleantitle.get(titles[0])

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'tab-content clearfix'})

            if content == 'movies':
                r = client.parseDOM(r, 'div', attrs={'id': 'movies'})
            else:
                r = client.parseDOM(r, 'div', attrs={'id': 'series'})

            data = dom_parser.parse_dom(r, 'figcaption')

            for i in data:
                title = i[0]['title']
                title = cleantitle.get(title)
                if title in t:
                    x = dom_parser.parse_dom(i, 'a', req='href')
                    return source_utils.strip_domain(x[0][0]['href'])
                else:
                    url = dom_parser.parse_dom(i, 'a', req='href')
                    data = client.request(url[0][0]['href'])
                    data = re.findall('<h1><a.+?">(.+?)\((\d{4})\).*?</a></h1>', data, re.DOTALL)[0]
                    if titles[0] in data[0] and year == data[1]: return source_utils.strip_domain(url[0][0]['href'])

            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            query = urlparse.urljoin(self.base_link, url)
            r = client.request(query)
            links = client.parseDOM(r, 'tr', attrs={'data-id': '\d+'})
            for i in links:
                url = re.findall( "data-bind=.+?site\(\'([^']+)\'", i, re.DOTALL)[0]
                quality = 'SD'
                lang, info = 'gr', 'SUB'
                valid, host = source_utils.is_host_valid(url, hostDict)

                sources.append({'source': host, 'quality': quality, 'language': lang, 'url': url, 'info': info,
                                'direct':False,'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url