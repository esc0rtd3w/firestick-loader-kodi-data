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
import datetime
import kodi
import utils
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

BASE_URL = 'http://www.best-moviez.ws'

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
        return 'BestMoviez'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        post = dom_parser2.parse_dom(html, 'div', {'class': 'entry-content'})
        if not post: return hosters
        for match in re.finditer('(?:href="|>)(https?://[^"<]+)', post[0].content):
            stream_url = match.group(1)
            if scraper_utils.excluded_link(stream_url) or 'imdb.com' in stream_url: continue
            host = urlparse.urlparse(stream_url).hostname
            if video.video_type == VIDEO_TYPES.MOVIE:
                meta = scraper_utils.parse_movie_link(stream_url)
            else:
                meta = scraper_utils.parse_episode_link(stream_url)
            quality = scraper_utils.height_get_quality(meta['height'])
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'quality': quality, 'direct': False}
            hosters.append(hoster)
        return hosters
        
    def get_url(self, video):
        return self._blog_get_url(video)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="30" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-4,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        posts = []
        html = self._http_get(self.base_url, params={'s': title, 'submit': 'Search'}, require_debrid=True, cache_limit=2)
        for _attr, post in dom_parser2.parse_dom(html, 'article', {'id': re.compile('post-\d+')}):
            if self.__too_old(post): continue
            posts += [post.content for post in dom_parser2.parse_dom(post, 'h1', {'class': 'entry-title'})]
            
        return self._blog_proc_results('\n'.join(posts), 'href="(?P<url>[^"]+)[^>]+>(?P<post_title>.*?)</a>', '', video_type, title, year)

    def __too_old(self, post):
        filter_days = datetime.timedelta(days=int(kodi.get_setting('%s-filter' % (self.get_name()))))
        post_date = dom_parser2.parse_dom(post, 'time', {'class': 'entry-date'}, req='datetime')
        if filter_days and post_date:
            today = datetime.date.today()
            try:
                post_date = datetime.date.fromtimestamp(utils.iso_2_utc(post_date[0].content))
                if today - post_date > filter_days:
                    return True
            except ValueError:
                return False
        return False
