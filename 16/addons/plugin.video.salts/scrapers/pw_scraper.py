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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger()
QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}
BASE_URL = 'http://www.primewire.ag'

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
        return 'PrimeWire'

    def format_source_label(self, item):
        label = super(self.__class__, self).format_source_label(item)
        if item['verified']: label = '[COLOR yellow]%s[/COLOR]' % (label)
        return label

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        container_pattern = r'<table[^>]+class="movie_version[ "][^>]*>(.*?)</table>'
        item_pattern = (
            r'quality_(?!sponsored|unknown)([^>]*)></span>.*?'
            r'url=([^&]+)&(?:amp;)?domain=([^&]+)&(?:amp;)?(.*?)'
            r'"version_veiws"> ([\d]+) views</')
        max_index = 0
        max_views = -1
        for container in re.finditer(container_pattern, html, re.DOTALL | re.IGNORECASE):
            for i, source in enumerate(re.finditer(item_pattern, container.group(1), re.DOTALL)):
                qual, url, host, parts, views = source.groups()

                if host == 'ZnJhbWVndGZv': continue  # filter out promo hosts

                item = {'host': host.decode('base-64'), 'url': url.decode('base-64')}
                item['verified'] = source.group(0).find('star.gif') > -1
                item['quality'] = scraper_utils.get_quality(video, item['host'], QUALITY_MAP.get(qual.upper()))
                item['views'] = int(views)
                if item['views'] > max_views:
                    max_index = i
                    max_views = item['views']

                if max_views > 0: item['rating'] = item['views'] * 100 / max_views
                else: item['rating'] = None
                pattern = r'<a href=".*?url=(.*?)&(?:amp;)?.*?".*?>(part \d*)</a>'
                other_parts = re.findall(pattern, parts, re.DOTALL | re.I)
                if other_parts:
                    item['multi-part'] = True
                    item['parts'] = [part[0].decode('base-64') for part in other_parts]
                else:
                    item['multi-part'] = False
                item['class'] = self
                item['direct'] = False
                hosters.append(item)

        if max_views > 0:
            for i in xrange(0, max_index):
                hosters[i]['rating'] = hosters[i]['views'] * 100 / max_views

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/index.php')
        params = {'search_keywords': title, 'year': year}
        params['search_section'] = 2 if video_type == VIDEO_TYPES.TVSHOW else 1
        html = self. _http_get(self.base_url, cache_limit=8)
        match = re.search('input type="hidden" name="key" value="([0-9a-f]*)"', html)
        if match:
            params['key'] = match.group(1)

            html = self._http_get(search_url, params=params, cache_limit=1)
            pattern = r'class="index_item.+?href="(.+?)" title="Watch (.+?)"?\(?([0-9]{4})?\)?"?>'
            for match in re.finditer(pattern, html):
                url, title, year = match.groups('')
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': year}
                results.append(result)
        else:
            logger.log('Unable to locate PW search key', log_utils.LOGWARNING)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = '"href="([^"]+/season-%s-episode-%s)">' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+).*?class="tv_episode_name">\s+-\s+(?P<title>[^<]+)'
        airdate_pattern = 'href="([^"]+)(?:[^<]+<){3}span\s+class="tv_episode_airdate">\s+-\s+{year}-{p_month}-{p_day}'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'data-id': video.season, 'class': 'show_season'})
        return self._default_get_episode_url(fragment or html, video, episode_pattern, title_pattern, airdate_pattern)
