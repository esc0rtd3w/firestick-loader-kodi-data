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



class source:
    def __init__(self):
        self.priority = 1
        self.language = ['gr']
        self.domains = ['tainiomania.ucoz.com']
        self.base_link = 'http://tainiomania.ucoz.com'
        self.search_link = 'search/?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(
                aliases),year)
            if not url: url = self.__search(trakt.getMovieTranslation(imdb, 'el'), year)
            return url
        except:
            return

    def __search(self, titles, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.getsearch(titles[0]+' '+year)))

            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i][0]

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'v_pict'})

            for i in r:
                title = re.findall('alt="(.+?)"',i[1], re.DOTALL)[0]
                y = re.findall('(\d{4})', title, re.DOTALL)[0]
                title = re.sub('<\w+>|</\w+>','',title)
                title = cleantitle.get(title)
                title = re.findall('(\w+)', cleantitle.get(title))[0]

                if title in t and year == y:
                    url = re.findall('href="(.+?)"',i[1], re.DOTALL)[0]
                    return source_utils.strip_domain(url)
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            query = urlparse.urljoin(self.base_link, url)
            data = client.request(query)

            url = re.findall('file:"([^"]+)"', data, re.DOTALL)[0]
            quality = 'SD'
            lang, info = 'gr', 'SUB'
            if url.endswith('.mp4'): direct = True
            else: direct = False

            sources.append({'source': 'tainiomania', 'quality': quality, 'language': lang, 'url': url, 'info': info,
                            'direct':direct,'debridonly': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        return url