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
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['gr']
        self.domains = ['gamatotv.me']
        self.base_link = 'http://gamatotv.me/'
        self.search_link = '/groups/group/search?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases),year)
            if not url: url = self.__search(self.search_link + trakt.getMovieTranslation(imdb, 'el'), year)
            return url
        except:
            return

    def __search(self, titles, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.getsearch(titles[0]+' '+year)))

            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i][0]

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs={'class': 'bd'})

            for i in r:
                r = dom_parser.parse_dom(i, 'h3')
                r = dom_parser.parse_dom(r, 'a')
                title = r[0][1]
                y = re.findall('(\d{4})', title, re.DOTALL)[0]
                title = cleantitle.get(title.split('(')[0])

                if title in t and year == y:
                    return source_utils.strip_domain(r[0][0]['href'])
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
            links = client.parseDOM(r, 'div', attrs={'class': 'xg_user_generated'})
            links = dom_parser.parse_dom(links, 'a')

            for i in links:
                url = i[0]['href']
                if 'youtube' in url: continue
                quality = 'SD'
                lang, info = 'gr', 'SUB'
                valid, host = source_utils.is_host_valid(url, hostDict)
                if 'hdvid' in host: valid = True
                if not valid: continue

                sources.append({'source': host, 'quality': quality, 'language': lang, 'url': url, 'info': info,
                                'direct':False,'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url