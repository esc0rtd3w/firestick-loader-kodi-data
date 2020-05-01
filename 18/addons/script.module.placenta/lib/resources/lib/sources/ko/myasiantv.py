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


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['myasiantv.se']
        self.base_link = 'http://myasiantv.se'
        self.search_link = '/quicksearch/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            if url: url += 'watch/'
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            r = client.request(urlparse.urljoin(self.base_link, url))

            r = dom_parser.parse_dom(r, 'ul', attrs={'class': 'list-episode'})
            r = dom_parser.parse_dom(r, 'li')
            r = dom_parser.parse_dom(r, 'a', attrs={'href': re.compile('.*/episode-%s.*' % episode)}, req='href')[0].attrs['href']

            return source_utils.strip_domain(r)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'div', attrs={'id': 'player'})
            r = [i.attrs['src'] for i in dom_parser.parse_dom(r, 'iframe', req='src')]

            for i in r:
                try:
                    if 'vidnow.' in i:
                        i = client.request(i, referer=url)

                        gdata = [(match[1], match[0]) for match in re.findall('''["']?label\s*["']?\s*[:=]\s*["']?([^"',]+)["']?(?:[^}\]]+)["']?\s*file\s*["']?\s*[:=,]?\s*["']([^"']+)''', i, re.DOTALL)]
                        gdata += [(match[0], match[1]) for match in re.findall('''["']?\s*file\s*["']?\s*[:=,]?\s*["']([^"']+)(?:[^}>\]]+)["']?\s*label\s*["']?\s*[:=]\s*["']?([^"',]+)''', i, re.DOTALL)]
                        gdata = [(x[0].replace('\/', '/'), source_utils.label_to_quality(x[1])) for x in gdata]

                        for u, q in gdata:
                            try:
                                tag = directstream.googletag(u)

                                if tag:
                                    sources.append({'source': 'gvideo', 'quality': tag[0].get('quality', 'SD'), 'language': 'de', 'url': u, 'direct': True, 'debridonly': False})
                                else:
                                    sources.append({'source': 'CDN', 'quality': q, 'language': 'de', 'url': u, 'direct': True, 'debridonly': False})
                            except:
                                pass

                        i = dom_parser.parse_dom(i, 'div', attrs={'id': 'myElement'})
                        i = dom_parser.parse_dom(i, 'iframe', req='src')[0].attrs['src']

                    valid, host = source_utils.is_host_valid(i, hostDict)
                    if not valid: continue

                    urls = []
                    if 'google' in i: host = 'gvideo'; direct = True; urls = directstream.google(i);
                    if 'google' in i and not urls and directstream.googletag(i): host = 'gvideo'; direct = True; urls = [{'quality': directstream.googletag(i)[0]['quality'], 'url': i}]
                    elif 'ok.ru' in i: host = 'vk'; direct = True; urls = directstream.odnoklassniki(i)
                    elif 'vk.com' in i: host = 'vk'; direct = True; urls = directstream.vk(i)
                    else: direct = False; urls = [{'quality': 'SD', 'url': i}]

                    for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'ko', 'url': x['url'], 'direct': direct, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year):
        try:
            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query, XHR=True, referer=self.base_link)
            r = dom_parser.parse_dom(r, 'a', req='href')
            r = [(i.attrs['href'], i.content.lower()) for i in r if i]
            r = [(i[0], i[1], re.findall('(.+?) \(*(\d{4})', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return


