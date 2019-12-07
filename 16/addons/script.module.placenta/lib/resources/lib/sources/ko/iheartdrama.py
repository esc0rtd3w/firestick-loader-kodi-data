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
from resources.lib.modules import directstream
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['iheartdrama.tv']
        self.base_link = 'http://iheartdrama.tv'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases))
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases))
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases))
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = urlparse.urljoin(self.base_link, url)

            episode = tvmaze.tvMaze().episodeAbsoluteNumber(tvdb, int(season), int(episode))

            r = client.request(url)

            r = dom_parser.parse_dom(r, 'article')
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'entry-content'})
            r = dom_parser.parse_dom(r, 'li')
            r = dom_parser.parse_dom(r, 'a', attrs={'href': re.compile('.*-episode-%s-.*' % episode)}, req='href')[0].attrs['href']

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = client.request(urlparse.urljoin(self.base_link, url))
            r = dom_parser.parse_dom(r, 'article')
            r = dom_parser.parse_dom(r, 'div', attrs={'class': 'entry-content'})

            links = re.findall('''(?:link|file)["']?\s*:\s*["'](.+?)["']''', ''.join([i.content for i in r]))
            links += [l.attrs['src'] for i in r for l in dom_parser.parse_dom(i, 'iframe', req='src')]
            links += [l.attrs['src'] for i in r for l in dom_parser.parse_dom(i, 'source', req='src')]

            for i in links:
                try:
                    valid, hoster = source_utils.is_host_valid(i, hostDict)
                    if not valid: continue

                    urls = []
                    if 'google' in i: host = 'gvideo'; direct = True; urls = directstream.google(i);
                    if 'google' in i and not urls and directstream.googletag(i): host = 'gvideo'; direct = True; urls = [{'quality': directstream.googletag(i)[0]['quality'], 'url': i}]
                    elif 'ok.ru' in i: host = 'vk'; direct = True; urls = directstream.odnoklassniki(i)
                    elif 'vk.com' in i: host = 'vk'; direct = True; urls = directstream.vk(i)
                    else: host = hoster; direct = False; urls = [{'quality': 'SD', 'url': i}]

                    for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'ko', 'url': x['url'], 'direct': direct, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(titles[0]))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]

            r = client.request(query)

            r = dom_parser.parse_dom(r, 'article')
            r = dom_parser.parse_dom(r, 'h2', attrs={'class': 'entry-title'})
            r = dom_parser.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], i.content) for i in r]
            r = [(i[0]) for i in r if cleantitle.get(i[1]) in t][0]

            return source_utils.strip_domain(r)
        except:
            return
