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
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

BASE_URL = 'http://www.rls-movies.com'
CATEGORIES = {VIDEO_TYPES.MOVIE: '/category/movies/"', VIDEO_TYPES.EPISODE: '/category/tvshows/"'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'rls-movies'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        for source, values in self.__get_post_links(html).iteritems():
            if scraper_utils.excluded_link(source): continue
            host = urlparse.urlparse(source).hostname
            release = values['release']
            quality = scraper_utils.blog_get_quality(video, release, host)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': quality, 'direct': False}
            if 'X265' in release or 'HEVC' in release:
                hoster['format'] = 'x265'
            hosters.append(hoster)
        return hosters

    def __get_post_links(self, html):
        sources = {}
        release = dom_parser2.parse_dom(html, 'span', {'itemprop': 'name'})
        release = release[0].content if release else ''
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'entry'})
        if fragment:
            for attrs, label in dom_parser2.parse_dom(fragment[0].content, 'a', req='href'):
                stream_url = attrs['href']
                if not label or re.search('single\s+link', label, re.I):
                    sources[stream_url] = {'release': release}
                elif any([ext for ext in ['.mp4', '.mkv', '.avi'] if ext in label]):
                    sources[stream_url] = {'release': label}
        return sources
        
    def get_url(self, video):
        return self._blog_get_url(video, delim=' ')

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="30" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-4,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, params={'s': title}, require_debrid=True, cache_limit=1)
        post_pattern = 'class="post-box-title">.*?href="(?P<url>[^"]+)[^>]*>(?P<post_title>[^<]+).*?<span>(?P<date>[^ ]+ 0*\d+, \d{4})'
        date_format = '%B %d, %Y'
        return self._blog_proc_results(html, post_pattern, date_format, video_type, title, year)
