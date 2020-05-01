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
import scraper
import urlparse
import os.path
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://kodimadman.site88.net'
XML_META = {
    '4kmovies.xml': {'quality': QUALITIES.HD1080, 'format': '4K'},
    '3dmovies.xml': {'quality': QUALITIES.HD1080, '3D': True},
    'oldskoolmovies.xml': {'quality': QUALITIES.HD720}
}

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
        return 'RealMovies'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        query = scraper_utils.parse_query(source_url)
        if 'link' in query:
            stream_url = query['link']
            host = urlparse.urlparse(stream_url).hostname
            if 'xml_file' in query:
                xml_meta = XML_META.get(query['xml_file'], {})
            else:
                xml_meta = {}

            quality = xml_meta.get('quality', QUALITIES.HD1080)
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
            if 'quality' in xml_meta: del xml_meta['quality']
            source.update(xml_meta)
            hosters.append(source)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        folders = ['/addons/real-movies/base.xml']
        norm_title = scraper_utils.normalize_title(title)
        for page_url in folders:
            xml_file = os.path.basename(page_url)
            page_url = scraper_utils.urljoin(self.base_url, page_url)
            xml = self._http_get(page_url, require_debrid=True, cache_limit=48)
            new_folders = re.findall('<folder>(.*?)</folder>', xml, re.I)
            if new_folders:
                folders += [folder for folder in new_folders if folder]
                
            for match in re.finditer('<item>(.*?)</item>', xml, re.I | re.DOTALL):
                item = match.group(1)
                match_title_year = re.search('<title>(.*?)</title>', item, re.I)
                match_url = re.search('<link>(.*?)</link>', item, re.I)
                if match_title_year and match_url:
                    match_title_year = match_title_year.group(1)
                    match_url = match_url.group(1)
                    if match_title_year and match_url:
                        match_title, match_year = scraper_utils.extra_year(match_title_year)
                        xml_file = xml_file.replace(' ', '').lower()
                        match_url = 'xml_file=%s&link=%s' % (xml_file, match_url)
                        if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                            if 'format' in XML_META.get(xml_file, {}):
                                match_title += ' (%s)' % (XML_META[xml_file]['format'])
                            result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': match_url}
                            results.append(result)

        return results
