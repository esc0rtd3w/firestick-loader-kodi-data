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
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://www.watchepisodes4.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'WatchEpisodes'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.25)
        for _attrs, link in dom_parser2.parse_dom(html, 'div', {'class': 'ldr-item'}):
            stream_url = dom_parser2.parse_dom(link, 'a', req='data-actuallink')
            
            try:
                watched = dom_parser2.parse_dom(link, 'div', {'class': 'click-count'})
                match = re.search(' (\d+) ', watched[0].content)
                views = match.group(1)
            except:
                views = None
                    
            try:
                score = dom_parser2.parse_dom(link, 'div', {'class': 'point'})
                score = int(score[0].content)
                rating = score * 10 if score else None
            except:
                rating = None
            
            if stream_url:
                stream_url = stream_url[0].attrs['data-actuallink'].strip()
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': rating, 'url': stream_url, 'direct': False}
                hosters.append(hoster)

        return hosters

    def _get_episode_url(self, show_url, video):
        url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=2)
        if html:
            force_title = scraper_utils.force_title(video)
            episodes = dom_parser2.parse_dom(html, 'div', {'class': 'el-item'})
            if not force_title:
                episode_pattern = 'href="([^"]*-[sS]%02d[eE]%02d(?!\d)[^"]*)' % (int(video.season), int(video.episode))
                match = re.search(episode_pattern, html)
                if match:
                    return scraper_utils.pathify_url(match.group(1))
                
                if kodi.get_setting('airdate-fallback') == 'true' and video.ep_airdate:
                    airdate_pattern = '%02d-%02d-%d' % (video.ep_airdate.day, video.ep_airdate.month, video.ep_airdate.year)
                    for episode in episodes:
                        episode = episode.content
                        ep_url = dom_parser2.parse_dom(episode, 'a', req='href')
                        ep_airdate = dom_parser2.parse_dom(episode, 'div', {'class': 'date'})
                        if ep_url and ep_airdate:
                            ep_airdate = ep_airdate[0].content.strip()
                            if airdate_pattern == ep_airdate:
                                return scraper_utils.pathify_url(ep_url[0].attrs['href'])

            if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title:
                norm_title = scraper_utils.normalize_title(video.ep_title)
                for episode in episodes:
                    episode = episode.content
                    ep_url = dom_parser2.parse_dom(episode, 'a', req='href')
                    ep_title = dom_parser2.parse_dom(episode, 'div', {'class': 'e-name'})
                    if ep_url and ep_title and norm_title == scraper_utils.normalize_title(ep_title[0].content):
                        return scraper_utils.pathify_url(ep_url[0].attrs['href'])

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/ajax_search')
        html = self._http_get(search_url, params={'q': title}, headers=XHR, cache_limit=1)
        js_result = scraper_utils.parse_json(html, search_url)
        match_year = ''
        for series in js_result.get('series', []):
            match_url = series.get('seo')
            match_title = series.get('label')
            if match_url and match_title and (not year or not match_year or year == match_year):
                result = {'url': scraper_utils.pathify_url('/' + match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results
