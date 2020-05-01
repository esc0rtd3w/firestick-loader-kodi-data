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
import re
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib.utils2 import i18n
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import MONTHS
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://myddl.pw'
EXCLUDE_LINKS = ['adf.ly', urlparse.urlparse(BASE_URL).hostname]

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
        return 'MyDDL'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'post-cont'})
        if not fragment: return hosters
        
        match = re.search('<p>\s*<strong>(.*?)<script', fragment[0].content, re.DOTALL)
        if not match: return hosters
        
        for attrs, _content in dom_parser2.parse_dom(match.group(1), 'a', req='href'):
            stream_url = attrs['href']
            if scraper_utils.excluded_link(stream_url): continue
            if video.video_type == VIDEO_TYPES.MOVIE:
                meta = scraper_utils.parse_movie_link(stream_url)
            else:
                meta = scraper_utils.parse_episode_link(stream_url)
            
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.get_quality(video, host, scraper_utils.height_get_quality(meta['height']))
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'quality': quality, 'direct': False}
            hosters.append(hoster)
                
        return hosters

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="60" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        return settings

    def _get_episode_url(self, show_url, video):
        force_title = scraper_utils.force_title(video)
        title_fallback = kodi.get_setting('title-fallback') == 'true'
        norm_title = scraper_utils.normalize_title(video.ep_title)
        page_url = [show_url]
        too_old = False
        while page_url and not too_old:
            url = scraper_utils.urljoin(self.base_url, page_url[0])
            html = self._http_get(url, require_debrid=True, cache_limit=1)
            for _attrs, post in dom_parser2.parse_dom(html, 'div', {'id': re.compile('post-\d+')}):
                if self.__too_old(post):
                    too_old = True
                    break
                if show_url not in post: continue
                match = dom_parser2.parse_dom(post, 'a', req='href')
                if match:
                    url, title = match[0].attrs['href'], match[0].content
                    if not force_title:
                        if scraper_utils.release_check(video, title, require_title=False):
                            return scraper_utils.pathify_url(url)
                    else:
                        if title_fallback and norm_title:
                            match = re.search('</strong>(.*?)</p>', post)
                            if match and norm_title == scraper_utils.normalize_title(match.group(1)):
                                return scraper_utils.pathify_url(url)
                
            page_url = dom_parser2.parse_dom(html, 'a', {'class': 'nextpostslink'}, req='href')
            if page_url: page_url = [page_url[0].attrs['href']]
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if video_type == VIDEO_TYPES.TVSHOW and title:
            test_url = '/tv-show/%s/' % (scraper_utils.to_slug(title))
            test_url = scraper_utils.urljoin(self.base_url, test_url)
            html = self._http_get(test_url, require_debrid=True, cache_limit=24)
            posts = dom_parser2.parse_dom(html, 'div', {'id': re.compile('post-\d+')})
            if posts:
                result = {'url': scraper_utils.pathify_url(test_url), 'title': scraper_utils.cleanse_title(title), 'year': ''}
                results.append(result)
        elif video_type == VIDEO_TYPES.MOVIE:
            search_title = re.sub('[^A-Za-z0-9 ]', '', title.lower())
            html = self._http_get(self.base_url, params={'s': search_title}, require_debrid=True, cache_limit=1)
            norm_title = scraper_utils.normalize_title(title)
            for _attrs, post in dom_parser2.parse_dom(html, 'div', {'id': re.compile('post-\d+')}):
                match = re.search('<h\d+[^>]*>\s*<a\s+href="([^"]+)[^>]*>(.*?)</a>', post)
                if match:
                    post_url, post_title = match.groups()
                    if '/tv-show/' in post or self.__too_old(post): continue
                    post_title = re.sub('<[^>]*>', '', post_title)
                    meta = scraper_utils.parse_movie_link(post_title)
                    full_title = '%s [%s] (%sp)' % (meta['title'], meta['extra'], meta['height'])
                    match_year = meta['year']
                    
                    match_norm_title = scraper_utils.normalize_title(meta['title'])
                    if (match_norm_title in norm_title or norm_title in match_norm_title) and (not year or not match_year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(post_url), 'title': scraper_utils.cleanse_title(full_title), 'year': match_year}
                        results.append(result)
            
        return results

    def __to_slug(self, title):
        slug = title.lower()
        slug = re.sub('[^A-Za-z0-9 -]', ' ', slug)
        slug = re.sub('\s\s+', ' ', slug)
        slug = re.sub(' ', '-', slug)
        return slug
        
    def __too_old(self, post):
        try:
            filter_days = datetime.timedelta(days=int(kodi.get_setting('%s-filter' % (self.get_name()))))
            if filter_days:
                today = datetime.date.today()
                match = re.search('<span\s+class="date">(.*?)\s+(\d+)(?:\w+)?,[^<]+(\d{4})<', post)
                mon_name, post_day, post_year = match.groups()
                post_month = MONTHS.index(mon_name.upper()) + 1
                post_date = datetime.date(int(post_year), post_month, int(post_day))
                if today - post_date > filter_days:
                    return True
        except ValueError:
            return False
        
        return False
