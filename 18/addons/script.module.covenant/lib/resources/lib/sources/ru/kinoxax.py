# -*- coding: utf-8 -*-

"""
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
"""

import re
import urllib
import urlparse

from resources.lib.sources.ru.lib import moonwalk
from resources.lib.sources.ru.lib import utils

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['ru']
        self.domains = ['kinoxa-x.net']
        self.base_link = 'http://kinoxa-x.net'
        self.search_link = '/index.php?do=search'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year)
            return urllib.urlencode({'url': url}) if url else None
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'aliases': aliases, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'season': season, 'episode': episode, 'year': re.findall('(\d{4})', premiered)[0]})
            return urllib.urlencode(data)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            url = data.get('url')
            year = data.get('year')
            season = data.get('season')
            episode = data.get('episode')

            if season and episode and not url:
                tvshowtitle = data.get('tvshowtitle')
                localtvshowtitle = data.get('localtvshowtitle')
                aliases = source_utils.aliases_to_array(eval(data['aliases']))

                url = self.__search([localtvshowtitle] + aliases, year, season)
                if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + aliases, year, season)
                if not url: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            r = dom_parser.parse_dom(r, 'iframe', attrs={'class': 'prerolllvid'}, req='src')
            r = [i.attrs['src'] for i in r]

            for link in r:
                try:
                    urls = []
                    if 'moonwalk.cc' in link: host = 'moonwalk'; direct = True; urls = moonwalk.moonwalk(link, url, season, episode)

                    for i in urls: sources.append({'source': host, 'quality': i['quality'], 'info': i.get('info', ''), 'language': 'ru', 'url': i['url'], 'direct': direct, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, year, season='0'):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            post = {'story': utils.uni2cp(titles[0]), 'titleonly': 3, 'do': 'search', 'subaction': 'search', 'search_start': 1, 'full_search': 0, 'result_from': 1}
            r = client.request(url, post=post)

            r = r.decode('cp1251').encode('utf-8')

            r = dom_parser.parse_dom(r, 'table', attrs={'class': 'eBlock'})
            r = [(dom_parser.parse_dom(i, 'div', attrs={'class': 'eTitle'}), dom_parser.parse_dom(i[1], 'a', attrs={'href': re.compile('.*\d+_goda/')})) for i in r]
            r = [(dom_parser.parse_dom(i[0][0], 'a', req='href'), [x.content for x in i[1] if re.match('\d{4}', x.content)][0] if i[1] else '0') for i in r if i[0]]
            r = [(i[0][0].attrs['href'], i[0][0].content, i[1]) for i in r if i[0]]
            r = [(i[0], i[1], i[2], re.findall('(.+?) \(*(\d{4})', i[1])) for i in r if i]
            r = [(i[0], i[3][0][0] if i[3] else i[1], i[2]) for i in r]
            r = [(i[0], i[1], i[2], re.findall(u'(.+?)\s+(\d+)\s+(?:сезон)', i[1])) for i in r]
            r = [(i[0], i[3][0][0] if len(i[3]) > 0 else i[1], i[2], i[3][0][1] if len(i[3]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y and int(i[3]) == int(season)][0]

            return source_utils.strip_domain(r)
        except:
            return
