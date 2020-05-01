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
import datetime
import urllib
import re
import urlparse
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()

BASE_URL = 'http://tvshows-hdtv.org'
EP_PAGE = '/_new.episodes.%s.html'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.filter = int(kodi.get_setting('%s-filter' % (self.get_name())))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'TVHD'

    def get_sources(self, video):
        hosters = []
        sources = {}
        today = datetime.datetime.today().date()
        max_age = today - datetime.timedelta(days=self.filter)
        if video.ep_airdate and max_age < video.ep_airdate:
            day_after = video.ep_airdate + datetime.timedelta(days=1)
            for day in [day_after, video.ep_airdate]:
                if day < today:
                    page_url = EP_PAGE % (day.strftime('%Y.%m.%d'))
                    page_url = scraper_utils.urljoin(self.base_url, page_url)
                    html = self._http_get(page_url, require_debrid=True, cache_limit=30 * 24)
                    sources.update(self.__get_sources(video, html))
                if sources: break
                
            if not sources and kodi.get_setting('scraper_url'):
                page_url = scraper_utils.urljoin(self.base_url, '/index.html')
                html = self._http_get(page_url, require_debrid=True, cache_limit=2)
                sources.update(self.__get_sources(video, html))
            
        for source in sources:
            host = urlparse.urlparse(source).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source], 'direct': False}
            hosters.append(hoster)
        return hosters

    def __get_sources(self, video, html):
        sources = {}
        for match in re.finditer('<center>\s*<b>\s*(.*?)\s*</b>.*?<tr>(.*?)</tr>', html, re.DOTALL):
            release, links = match.groups()
            release = re.sub('</?[^>]*>', '', release)
            if scraper_utils.release_check(video, release):
                meta = scraper_utils.parse_episode_link(release)
                for match in re.finditer('href="([^"]+)', links):
                    sources[match.group(1)] = scraper_utils.height_get_quality(meta['height'])
        return sources

    def get_url(self, video):
        url = None
        result = self.db_connection().get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            logger.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            url = '/search?' + urllib.urlencode({'title': video.title, 'season': video.season, 'episode': video.episode, 'air_date': video.ep_airdate})
            self.db_connection().set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)
        return url

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="30" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        return []
