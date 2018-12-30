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
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://cyro.se'

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
        return 'DayT.se'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=1)
        iframes = dom_parser2.parse_dom(html, 'iframe', req='src')
        for attrs, _content in iframes:
            iframe_url = attrs['src']
            if 'docs.google.com' in iframe_url:
                sources = scraper_utils.parse_google(self, iframe_url)
                break
            else:
                iframe_url = scraper_utils.urljoin(self.base_url, iframe_url)
                html = self._http_get(iframe_url, cache_limit=1)
                iframes += dom_parser2.parse_dom(html, 'iframe', req='src')
        
        for source in sources:
            host = scraper_utils.get_direct_hostname(self, source)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.gv_get_quality(source), 'views': None, 'rating': None, 'url': source, 'direct': True}
            hosters.append(hoster)
    
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]*[Ss]0*%s[Ee]0*%s(?!\d)[^"]*)"' % (video.season, video.episode)
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        return self._default_get_episode_url(html, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        page_url = scraper_utils.urljoin(self.base_url, '/tvseries/search.php')
        html = self._http_get(page_url, params={'dayq': title}, cache_limit=48)
        html = re.sub('<!--.*?-->', '', html)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, td in dom_parser2.parse_dom(html, 'td', {'class': 'topic_content'}):
            match_url = dom_parser2.parse_dom(td, 'a', req='href')
            match_title_year = dom_parser2.parse_dom(td, 'img', req='alt')
            if not match_url or not match_title_year: continue

            match_url = match_url[0].attrs['href']
            match_title_year = match_title_year[0].attrs['alt']
            if not match_url.startswith('/'): match_url = '/tvseries/' + match_url
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if (norm_title in scraper_utils.normalize_title(match_title)) and (not year or not match_year or year == match_year):
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results
