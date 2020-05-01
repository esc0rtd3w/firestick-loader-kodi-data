"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://www.iframetv.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'PirateJunkies'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        js_url = scraper_utils.urljoin(self.base_url, '/javascript/movies.js')
        html = self._http_get(js_url, cache_limit=48)
        if source_url.startswith('/'):
            source_url = source_url[1:]
        pattern = '''getElementById\(\s*"%s".*?play\(\s*'([^']+)''' % (source_url)
        match = re.search(pattern, html, re.I)
        if match:
            stream_url = match.group(1)
            if 'drive.google' in stream_url or 'docs.google' in stream_url:
                sources = scraper_utils.parse_google(self, stream_url)
            else:
                sources = [stream_url]
            
            for source in sources:
                stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                host = scraper_utils.get_direct_hostname(self, source)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(source)
                    direct = True
                elif 'youtube' in stream_url:
                    quality = QUALITIES.HD720
                    direct = False
                    host = 'youtube.com'
                else:
                    quality = QUALITIES.HIGH
                    direct = True
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        norm_title = scraper_utils.normalize_title(title)
        for movie in self.__get_movies():
            match_year = movie['year']
            if norm_title in scraper_utils.normalize_title(movie['title']) and (not year or not match_year or year == match_year):
                result = {'title': scraper_utils.cleanse_title(movie['title']), 'year': match_year, 'url': scraper_utils.pathify_url(movie['url'])}
                results.append(result)
        return results

    def __get_movies(self):
        url = scraper_utils.urljoin(self.base_url, '/javascript/pj.js')
        html = self._http_get(url, cache_limit=48)
        movies = []
        for match in re.finditer('(.*?)\.setAttribute\(\s*"class"\s*,\s*"poster ([^"]+)"\s*\)', html, re.I):
            title, attributes = match.groups()
            movie = {'title': self.__make_title(title), 'year': self.__get_year(attributes), 'url': title.strip()}
            movies.append(movie)
        return movies
    
    def __make_title(self, title):
        match = re.search('getElementById\("([^"]+)', title)
        if match:
            title = match.group(1)
        title = title.strip()
        title = title[0].upper() + title[1:]
        return ' '.join(re.findall('[A-Z0-9][^A-Z]*', title))
    
    def __get_year(self, attributes):
        match = re.search('(\d{4})', attributes)
        if match:
            return match.group(1)
        else:
            return ''
