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

import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['fr']
        self.domains = ['skstream.co']
        self.base_link = 'http://www.skstream.co'
        self.search_link = 'recherche?s=%s'
        self.protect_domain = 'dl-protect.co'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search(localtitle, year)
            if not url and title != localtitle: url = self.__search(title, year)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search(localtvshowtitle, year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search(tvshowtitle, year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url)
            r = dom_parser.parse_dom(r, 'a', attrs={'class': 'episode-block', 'href': re.compile('.*/saison-%s/episode-%s/.*' % (season, episode))}, req='href')
            r = [i.attrs['href'] for i in r][0]  # maybe also get the VF/VOSTFR to get the VF first

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        myList = []
        myLinks = []


        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            print url

            r = client.request(url)

            r0 = client.parseDOM(r, 'tr', attrs={'class': 'changeplayer sks'})
            r1 = client.parseDOM(r, 'tr', attrs={'class': 'changeplayer sks'}, ret='data-basicurl')
            r2 = client.parseDOM(r, 'tr', attrs={'class': 'changeplayer sks'}, ret='data-idvideo')
            r3 = client.parseDOM(r, 'tr', attrs={'class': 'changeplayer sks'}, ret='data-embedlien')
            r4 = re.compile('class=\"server player-(.+?)\"').findall(r)
            r5 = client.parseDOM(r0, 'span', attrs={'class': 'badge'})

            for i in range(0, len(r1)):
                myList.append((r1[i], r2[i], r3[i], r4[i], r5[i], url))


            for refer, videoid, link, hoster, language, theurl in myList:
                #valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                #if not valid: continue

                myLinks.append((link, refer, videoid, theurl))

                info = language

                sources.append({'source': hoster, 'quality': 'SD', 'language': 'fr', 'url': myLinks, 'info': info, 'direct': False, 'debridonly': False})
                myLinks = []

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            print url

            if self.protect_domain in url[0][0]:
                #post={'data-idvideo': '%s' % i}
                url = client.request(url[0][0], post={'data-idvideo': url[0][2]}, referer=url[0][3], output='geturl')

            return url
        except:
            return url

    def __search(self, title, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(title)))
            query = urlparse.urljoin(self.base_link, query)

            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'movie_single'})
            r = dom_parser.parse_dom(r, 'a', attrs={'class': 'unfilm'}, req='href')
            r = [(i.attrs['href'], dom_parser.parse_dom(r, 'div', attrs={'class': 'title'}), dom_parser.parse_dom(r, 'span', attrs={'class': 'post-year'})) for i in r]
            r = [(i[0], re.sub('<.+?>|</.+?>', '', i[1][0].content), i[2][0].content if i[2] else '0') for i in r if i[1]]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return
