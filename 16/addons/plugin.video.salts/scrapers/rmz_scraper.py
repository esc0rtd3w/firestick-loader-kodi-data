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
import urllib
import re
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.utils2 import i18n
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
import scraper

logger = log_utils.Logger.get_logger()

BASE_URL = 'http://rmz.cr'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'RMZ'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, require_debrid=True, cache_limit=.5)
        if video.video_type == VIDEO_TYPES.MOVIE:
            page_url = self.__get_release(html, video)
            if page_url is None: return hosters
            
            page_url = scraper_utils.urljoin(self.base_url, page_url)
            html = self._http_get(page_url, require_debrid=True, cache_limit=.5)
            
        hevc = False
        for _attrs, content in dom_parser2.parse_dom(html, 'span', {'class': 'releaselabel'}):
            if re.search('(hevc|x265)', content, re.I):
                hevc = 'x265'
                
            match = re.search('(\d+)x(\d+)', content)
            if match:
                _width, height = match.groups()
                quality = scraper_utils.height_get_quality(height)
                break
        else:
            quality = QUALITIES.HIGH
        
        streams = [attrs['href'] for attrs, _content in dom_parser2.parse_dom(html, 'a', {'class': 'links'}, req='href')]
        streams += [content for _attrs, content in dom_parser2.parse_dom(html, 'pre', {'class': 'links'})]
        for stream_url in streams:
            if scraper_utils.excluded_link(stream_url): continue
            host = urlparse.urlparse(stream_url).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'quality': quality, 'direct': False}
            if hevc: hoster['format'] = hevc
            hosters.append(hoster)
                
        return hosters

    def __get_release(self, html, video):
        try: select = int(kodi.get_setting('%s-select' % (self.get_name())))
        except: select = 0
        ul_id = 'releases' if video.video_type == VIDEO_TYPES.MOVIE else 'episodes'
        fragment = dom_parser2.parse_dom(html, 'ul', {'id': ul_id})
        if fragment:
            best_qorder = 0
            best_page = None
            for _attrs, item in dom_parser2.parse_dom(fragment[0].content, 'li'):
                match = dom_parser2.parse_dom(item, 'span', req=['href', 'title'])
                if not match:
                    match = dom_parser2.parse_dom(item, 'a', req=['href', 'title'])
                    if not match: continue
                
                page_url, release = match[0].attrs['href'], match[0].attrs['title']
                match = dom_parser2.parse_dom(item, 'span', {'class': 'time'})
                if match and self.__too_old(match[0].content): break
                
                release = re.sub('^\[[^\]]*\]\s*', '', release)
                if video.video_type == VIDEO_TYPES.MOVIE:
                    meta = scraper_utils.parse_movie_link(release)
                else:
                    if not scraper_utils.release_check(video, release, require_title=False): continue
                    meta = scraper_utils.parse_episode_link(release)

                if select == 0:
                    best_page = page_url
                    break
                else:
                    quality = scraper_utils.height_get_quality(meta['height'])
                    logger.log('result: |%s|%s|%s|' % (page_url, quality, Q_ORDER[quality]), log_utils.LOGDEBUG)
                    if Q_ORDER[quality] > best_qorder:
                        logger.log('Setting best as: |%s|%s|%s|' % (page_url, quality, Q_ORDER[quality]), log_utils.LOGDEBUG)
                        best_page = page_url
                        best_qorder = Q_ORDER[quality]
            
            return best_page
    
    def __too_old(self, age):
        filter_days = int(kodi.get_setting('%s-filter' % (self.get_name())))
        if filter_days and scraper_utils.get_days(age) > filter_days:
            return True
        else:
            return False

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="60" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-4,true)"/>' % (name, i18n('auto_select')))
        return settings

    def _get_episode_url(self, show_url, video):
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, require_debrid=True, cache_limit=.5)
        return self.__get_release(html, video)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/')
        search_url = scraper_utils.urljoin(search_url, urllib.quote_plus(title))
        html = self._http_get(search_url, require_debrid=True, cache_limit=8)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'list'}):
            if not dom_parser2.parse_dom(fragment, 'div', {'class': 'lists_titles'}): continue
            for attrs, match_title_year in dom_parser2.parse_dom(fragment, 'a', {'class': 'title'}, req='href'):
                match_url = attrs['href']
                match_title_year = re.sub('</?[^>]*>', '', match_title_year)
                is_show = re.search('\(d{4|-\)', match_title_year)
                if (is_show and video_type == VIDEO_TYPES.MOVIE) or (not is_show and video_type == VIDEO_TYPES.TVSHOW): continue
                
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
            
        return results
