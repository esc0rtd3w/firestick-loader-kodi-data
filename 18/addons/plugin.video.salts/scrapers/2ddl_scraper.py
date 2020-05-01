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
import urllib
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib.utils2 import i18n
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import SHORT_MONS
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'http://2ddl.download'
CATEGORIES = {VIDEO_TYPES.MOVIE: '/category/movies/', VIDEO_TYPES.TVSHOW: '/category/tv-shows/'}
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
        return '2DDL'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        
        html = self._http_get(source_url, require_debrid=True, cache_limit=.5)
        if video.video_type == VIDEO_TYPES.MOVIE:
            pattern = '<singlelink>(.*?)(?=<hr\s*/>|download>|thanks_button_div)'
        else:
            pattern = '<hr\s*/>\s*<strong>(.*?)</strong>.*?<singlelink>(.*?)(?=<hr\s*/>|download>|thanks_button_div)'
            
        for match in re.finditer(pattern, html, re.DOTALL):
            if video.video_type == VIDEO_TYPES.MOVIE:
                links = match.group(1)
                match = re.search('<h2>\s*<a[^>]+>(.*?)</a>', html)
                if match:
                    title = match.group(1)
                else:
                    title = ''
            else:
                title, links = match.groups()
                
            for match in re.finditer('href="([^"]+)', links):
                stream_url = match.group(1).lower()
                if any(link in stream_url for link in EXCLUDE_LINKS): continue
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.blog_get_quality(video, title, host)
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
            html = self._http_get(page_url[0], require_debrid=True, cache_limit=1)
            for _attr, post in dom_parser2.parse_dom(html, 'div', {'id': re.compile('post-\d+')}):
                if self.__too_old(post):
                    too_old = True
                    break
                if CATEGORIES[VIDEO_TYPES.TVSHOW] in post and show_url in post:
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
        search_url = '/search/' + urllib.quote_plus(title)
        html = self._http_get(search_url, require_debrid=True, cache_limit=1)
        if video_type == VIDEO_TYPES.TVSHOW:
            seen_urls = {}
            for _attr, post in dom_parser2.parse_dom(html, 'div', {'id': re.compile('post-\d+')}):
                if CATEGORIES[video_type] not in post: continue
                match = re.search('<span>\s*TAGS:\s*</span>\s*<a\s+href="([^"]+)[^>]+>([^<]+)', post, re.I)
                if match:
                    show_url, match_title = match.groups()
                    if show_url in seen_urls: continue
                    result = {'url': scraper_utils.pathify_url(show_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    seen_urls[show_url] = result
                    results.append(result)
        elif video_type == VIDEO_TYPES.MOVIE:
            norm_title = scraper_utils.normalize_title(title)
            headings = re.findall('<h2>\s*<a\s+href="([^"]+)[^>]+>(.*?)</a>', html)
            posts = [result.content for result in dom_parser2.parse_dom(html, 'div', {'id': re.compile('post-\d+')})]
            for heading, post in zip(headings, posts):
                if CATEGORIES[video_type] not in post or self.__too_old(post): continue
                post_url, post_title = heading
                meta = scraper_utils.parse_movie_link(post_title)
                full_title = '%s [%s] (%sp)' % (meta['title'], meta['extra'], meta['height'])
                match_year = meta['year']
                
                match_norm_title = scraper_utils.normalize_title(meta['title'])
                if (match_norm_title in norm_title or norm_title in match_norm_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(post_url), 'title': scraper_utils.cleanse_title(full_title), 'year': match_year}
                    results.append(result)
            
        return results

    def _http_get(self, url, params=None, data=None, multipart_data=None, headers=None, cookies=None, allow_redirect=True, method=None, require_debrid=False, read_error=False, cache_limit=8):
        real_url = scraper_utils.urljoin(self.base_url, url)
        html = super(self.__class__, self)._http_get(real_url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies,
                                                     allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error,
                                                     cache_limit=cache_limit)
        if self.__update_base_url(html):
            real_url = scraper_utils.urljoin(self.base_url, url)
            html = super(self.__class__, self)._http_get(real_url, params=params, data=data, multipart_data=multipart_data, headers=headers,
                                                         cookies=cookies, allow_redirect=allow_redirect, method=method, require_debrid=require_debrid,
                                                         read_error=read_error, cache_limit=cache_limit)
        
        return html
    
    def __update_base_url(self, html):
        if re.search('new domain', html, re.I):
            match = dom_parser2.parse_dom(html, 'a', {'rel': 'nofollow'}, req='href')
            if match:
                html = super(self.__class__, self)._http_get(match[0].attrs['href'], require_debrid=True, cache_limit=24)
                        
        match = dom_parser2.parse_dom(html, 'link', {'rel': 'canonical'}, req='href')
        if match:
            new_base = match[0].attrs['href']
            parts = urlparse.urlparse(new_base)
            new_base = parts.scheme + '://' + parts.hostname
            if new_base not in self.base_url:
                logger.log('Updating 2DDL Base Url from: %s to %s' % (self.base_url, new_base))
                self.base_url = new_base
                kodi.set_setting('%s-base_url' % (self.get_name()), new_base)
                return True
        
        return False
    
    def __too_old(self, post):
        try:
            filter_days = datetime.timedelta(days=int(kodi.get_setting('%s-filter' % (self.get_name()))))
            if filter_days:
                today = datetime.date.today()
                match = re.search('<a[^>]+title="posting time[^"]*">(.*?)\s+(\d+)\s*(\d{2,4})<', post)
                mon_name, post_day, post_year = match.groups()
                post_year = int(post_year)
                if post_year < 2000: post_year += 2000
                post_month = SHORT_MONS.index(mon_name) + 1
                post_date = datetime.date(post_year, post_month, int(post_day))
                if today - post_date > filter_days:
                    return True
        except ValueError:
            return False
        
        return False
