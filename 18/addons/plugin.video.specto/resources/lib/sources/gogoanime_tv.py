# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

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


import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import trakt
from resources.lib.libraries import tvmaze


class source:
    def __init__(self):
        self.base_link = 'http://ww1.gogoanime.io'
        self.search_link = '/search.html?keyword=%s'
        self.episode_link = '/%s-episode-%s'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            r = 'search/tvdb/%s?type=show&extended=full' % tvdb
            r = json.loads(trakt.getTrakt(r))
            if not r: return '0'

            d = r[0]['show']['genres']
            if not ('anime' in d or 'animation' in d): return '0'

            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']

            t = cleantitle.get(tvshowtitle)

            q = urlparse.urljoin(self.base_link, self.search_link)
            q = q % urllib.quote_plus(tvshowtitle)

            r = client.request(q)
            print r

            r = client.parseDOM(r, 'ul', attrs={'class': 'items'})
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('\d{4}', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][-1]) for i in r if i[0] and i[1] and i[2]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            r = r[0][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            tv_maze = tvmaze.tvMaze()
            num = tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))

            url = [i for i in url.strip('/').split('/')][-1]
            url = self.episode_link % (url, num)
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            r = client.parseDOM(r, 'iframe', ret='src')

            for u in r:
                try:
                    if not u.startswith('http') and not 'vidstreaming' in u: raise Exception()

                    url = client.request(u)
                    url = client.parseDOM(url, 'source', ret='src')

                    for i in url:
                        try: sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'provider': 'GoGoAnime', 'url': i})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


