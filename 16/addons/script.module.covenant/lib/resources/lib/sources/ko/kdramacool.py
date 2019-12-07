# -*- coding: utf-8 -*-

'''
    Covenant Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re,urllib,urlparse, json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ko']
        self.domains = ['tvcools.com']
        self.base_link = 'http://tvcools.com'
        self.search_link = '/wp-json/dooplay/search/?keyword=%s&nonce=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
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

            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')

            if season == 1 and episode == 1:
                season = episode = ''

            r = client.request(url)
            r = dom_parser.parse_dom(r, 'ul', attrs={'class': 'episodios'})
            r = dom_parser.parse_dom(r, 'a', attrs={'href': re.compile('[^\'"]*%s' % ('-%sx%s' % (season, episode)))})[0].attrs['href']

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

            rels = dom_parser.parse_dom(r, 'nav', attrs={'class': 'player'})
            rels = dom_parser.parse_dom(rels, 'ul', attrs={'class': 'idTabs'})
            rels = dom_parser.parse_dom(rels, 'li')
            rels = dom_parser.parse_dom(rels, 'a', attrs={'class': 'options'}, req='href')
            rels = [i.attrs['href'][1:] for i in rels]

            r = [dom_parser.parse_dom(r, 'div', attrs={'id': i}) for i in rels]

            links = re.findall('''(?:link|file)["']?\s*:\s*["'](.+?)["']''', ''.join([i[0].content for i in r]))
            links += [l.attrs['src'] for i in r for l in dom_parser.parse_dom(i, 'iframe', attrs={'class': 'metaframe'}, req='src')]
            links += [l.attrs['src'] for i in r for l in dom_parser.parse_dom(i, 'source', req='src')]

            for i in set(links):
                try:
                    i = re.sub('\[.+?\]|\[/.+?\]', '', i)
                    i = client.replaceHTMLCodes(i)

                    if 'videoapi.io' in i:
                        i = client.request(i, referer=url)

                        match = re.findall('videoApiPlayer\((.*?)\);', i)
                        if match:
                            i = client.request('https://videoapi.io/api/getlink/actionEmbed', post=json.loads(match[0]), XHR=True)
                            i = json.loads(i).get('sources', [])
                            i = [x.get('file', '').replace('\/', '/') for x in i]

                            for x in i:
                                gtag = directstream.googletag(x)
                                sources.append({'source': 'gvideo', 'quality': gtag[0]['quality'] if gtag else 'SD', 'language': 'ko', 'url': x, 'direct': True, 'debridonly': False})
                    else:
                        try:
                            valid, host = source_utils.is_host_valid(i, hostDict)
                            if not valid: continue

                            urls = []
                            if 'google' in i: host = 'gvideo'; direct = True; urls = directstream.google(i);
                            if 'google' in i and not urls and directstream.googletag(i):  host = 'gvideo'; direct = True; urls = [{'quality': directstream.googletag(i)[0]['quality'], 'url': i}]
                            elif 'ok.ru' in i: host = 'vk'; direct = True; urls = directstream.odnoklassniki(i)
                            elif 'vk.com' in i: host = 'vk'; direct = True; urls = directstream.vk(i)
                            else: direct = False; urls = [{'quality': 'SD', 'url': i}]

                            for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'ko', 'url': x['url'], 'direct': direct, 'debridonly': False})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year):
        try:
            n = cache.get(self.__get_nonce, 24)

            query = self.search_link % (urllib.quote_plus(cleantitle.query(titles[0])), n)
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query)
            r = json.loads(r)
            r = [(r[i].get('url'), r[i].get('title'), r[i].get('extra').get('date')) for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            return source_utils.strip_domain(r)
        except:
            return

    def __get_nonce(self):
        n = client.request(self.base_link)
        try: n = re.findall('nonce"?\s*:\s*"?([0-9a-zA-Z]+)', n)[0]
        except: n = '2cd195c35d'
        return n


