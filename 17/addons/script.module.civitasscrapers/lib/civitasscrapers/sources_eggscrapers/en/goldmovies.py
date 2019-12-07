# -*- coding: utf-8 -*-

"""
    Eggman Add-on

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


import traceback

from resources.lib.modules import cfscrape, cleantitle, client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['goldmovies.xyz']
        self.base_link = 'http://goldmovies.xyz'
        self.search_movie = '/%s/'
        self.search_tv = '/episode/%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_movie % title
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.geturl(tvshowtitle)
            url = self.base_link + self.search_tv % title
            print url
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '-season-%s-episode-%s/' % (season, episode)
            print url
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            u = client.parseDOM(r, "div", attrs={"id": "lnk list-downloads"})
            for t in u:
                r = client.parseDOM(t, 'a', ret='href')
                for url in r:
                    if '2160p' in url:
                        quality = '2160p'
                    elif '1080p' in url:
                        quality = '1080p'
                    elif '720p' in url:
                        quality = '720p'
                    else:
                        quality = 'SD'
                    url = url.split('php?')[1]
                    print url
                    sources.append(
                        {'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': True,
                         'debridonly': False})
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoldMovies - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
