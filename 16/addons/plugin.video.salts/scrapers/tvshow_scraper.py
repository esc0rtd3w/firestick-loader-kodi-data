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
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.utils2 import i18n
import scraper

BASE_URL = 'http://www.tvshow.me'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'TVShow.me'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        title = dom_parser2.parse_dom(html, 'title')
        if title:
            title = title[0].content
            title = re.sub('^\[ST\]\s*&#8211;\s*', '', title)
            meta = scraper_utils.parse_episode_link(title)
            page_quality = scraper_utils.height_get_quality(meta['height'])
        else:
            page_quality = QUALITIES.HIGH
        
        fragment = dom_parser2.parse_dom(html, 'section', {'class': 'entry-content'})
        if fragment:
            for _attrs, section in dom_parser2.parse_dom(fragment[0].content, 'p'):
                match = re.search('([^<]*)', section)
                meta = scraper_utils.parse_episode_link(match.group(1))
                if meta['episode'] != '-1' or meta['airdate']:
                    section_quality = scraper_utils.height_get_quality(meta['height'])
                else:
                    section_quality = page_quality
                    
                if Q_ORDER[section_quality] < Q_ORDER[page_quality]:
                    quality = section_quality
                else:
                    quality = page_quality
                    
                for attrs, _content in dom_parser2.parse_dom(section, 'a', req='href'):
                    stream_url = attrs['href']
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'quality': quality, 'direct': False}
                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        return self._blog_get_url(video, delim=' ')

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="60" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-4,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, params={'s': title}, require_debrid=True, cache_limit=1)
        post_pattern = '<h\d+[^>]+class="entry-title[^>]*>\s*<[^>]+href="(?P<url>[^"]*/(?P<date>\d{4}/\d{1,2}/\d{1,2})[^"]*)[^>]+>(?:\[ST\]\s+&#8211;\s*)?(?P<post_title>[^<]+)'
        date_format = '%Y/%m/%d'
        return self._blog_proc_results(html, post_pattern, date_format, video_type, title, year)
