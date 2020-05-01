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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://videomega.ch'
QUALITY_MAP = {'HD': QUALITIES.HIGH, 'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}

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
        return 'VKFlix'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        if video.video_type == VIDEO_TYPES.EPISODE:
            html = self.__get_episode_fragment(html, video)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'linkTr'}):
            stream_url = dom_parser2.parse_dom(item, 'div', {'class': 'linkHiddenUrl'})
            q_str = dom_parser2.parse_dom(item, 'div', {'class': 'linkQualityText'})
            if stream_url and q_str:
                stream_url = stream_url[0].content
                q_str = q_str[0].content
                host = urlparse.urlparse(stream_url).hostname
                base_quality = QUALITY_MAP.get(q_str, QUALITIES.HIGH)
                quality = scraper_utils.get_quality(video, host, base_quality)
                source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                hosters.append(source)

        return hosters

    def __get_episode_fragment(self, html, video):
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'season%s' % (video.season)})
        if fragment:
            fragment = fragment[0].content
            pattern = 'Season\s+%s\s+Series?\s+%s$' % (video.season, video.episode)
            for i, label in enumerate(dom_parser2.parse_dom(fragment, 'h3')):
                match = re.search(pattern, label.content, re.I)
                if match:
                    fragments = dom_parser2.parse_dom(fragment, 'div', {'class': 'tableLinks'})
                    if len(fragments) > i:
                        return fragments[i].content
                    else:
                        break
                
        return ''
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if video_type == VIDEO_TYPES.MOVIE:
            pages = [{'url': ''}, {'url': '/latest-movies'}, {'url': '/new-movies'}]
        else:
            pages = [{'url': '/free-tv-series-online'}, {'url': '/latest-episodes'}, {'url': '/new-episodes'}]
        
        for page in pages:
            results += self.__search(video_type, title, year, page)

        if not results:
            page = {'url': '/search', 'params': {'q': title}}
            results += self.__search(video_type, title, year, page)

        seen_urls = {}
        final_results = []
        for result in results:
            if result['url'] in seen_urls: continue
            seen_urls[result['url']] = True
            final_results.append(result)
            
        return final_results

    def __search(self, video_type, title, year, page):
        results = []
        url = scraper_utils.urljoin(self.base_url, page['url'])
        params = page['params'] if 'params' in page else None
        html = self._http_get(url, params=params, cache_limit=24)
        norm_title = scraper_utils.normalize_title(title)
        match_year = ''
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'id': re.compile('movie-+\d+')}):
            is_tvshow = dom_parser2.parse_dom(item, 'div', {'class': 'movieTV'})
            if (is_tvshow and video_type == VIDEO_TYPES.TVSHOW) or (not is_tvshow and video_type == VIDEO_TYPES.MOVIE):
                fragment = dom_parser2.parse_dom(item, 'h4', {'class': 'showRowName'})
                if fragment:
                    match = dom_parser2.parse_dom(fragment[0].content, 'a', req='href')
                    if match:
                        match_url, match_title = match[0].attrs['href'], match[0].content
                        if re.search('/-?\d{7,}/', match_url): continue
                        
                        match_norm_title = scraper_utils.normalize_title(match_title)
                        if (match_norm_title in norm_title or norm_title in match_norm_title) and (not year or not match_year or year == match_year):
                            result = {'title': scraper_utils.cleanse_title(match_title), 'url': scraper_utils.pathify_url(match_url), 'year': match_year}
                            results.append(result)
        return results
        
    def _get_episode_url(self, show_url, video):
        url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=8)
        pattern = '<h3>[^>]*Season\s+%s\s+Series?\s+%s<' % (video.season, video.episode)
        match = re.search(pattern, html, re.I)
        if match:
            return show_url
