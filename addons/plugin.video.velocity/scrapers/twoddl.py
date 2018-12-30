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
from libs import kodi
from libs import dom_parser
import scraper_utils
from libs.constants import FORCE_NO_MATCH
from libs.constants import SHORT_MONS
from libs.constants import VIDEO_TYPES
import scrapeit
import main_scrape

BASE_URL = 'http://2ddl.io'
CATEGORIES = {VIDEO_TYPES.MOVIE: '/category/movies/', VIDEO_TYPES.TVSHOW: '/category/tv-shows/'}
EXCLUDE_LINKS = ['adf.ly', urlparse.urlparse(BASE_URL).hostname]

class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('2ddl_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return '2DDL'

    def get_sources(self, video, video_type):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, require_debrid=True, cache_limit=.5)
            if video_type == 'movies':
                pattern = '<singlelink>(.*?)(?=<hr\s*/>|download>|thanks_button_div)'
            else:
                pattern = '<hr\s*/>\s*<strong>(.*?)</strong>.*?<singlelink>(.*?)(?=<hr\s*/>|download>|thanks_button_div)'
            for match in re.finditer(pattern, html, re.DOTALL):
                if video_type == 'movies':
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
                    #source = {'hostname': 'IceFilms', 'multi-part': False, 'quality': quality, 'class': '','version': label,'rating': None, 'views': None, 'direct': False}
                    hoster = {'hostname': '2DDL','multi-part': False, 'host': host, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'quality': quality, 'direct': False}
                    hosters.append(hoster)
        main_scrape.apply_urlresolver(hosters)
        return hosters

    def _get_episode_url(self, show_url, video):
        force_title = scraper_utils.force_title(video)
        title_fallback = kodi.get_setting('title-fallback') == 'true'
        norm_title = scraper_utils.normalize_title(video.ep_title)
        page_url = [show_url]
        too_old = False
        while page_url and not too_old:
            url = urlparse.urljoin(self.base_url, page_url[0])
            html = self._http_get(url, require_debrid=True, cache_limit=1)
            posts = dom_parser.parse_dom(html, 'div', {'id': 'post-\d+'})
            for post in posts:
                if self.__too_old(post):
                    too_old = True
                    break
                if CATEGORIES[VIDEO_TYPES.TVSHOW] in post and show_url in post:
                    match = re.search('<a\s+href="([^"]+)[^>]+>(.*?)</a>', post)
                    if match:
                        url, title = match.groups()
                        if not force_title:
                            if scraper_utils.release_check(video, title, require_title=False):
                                return scraper_utils.pathify_url(url)
                        else:
                            if title_fallback and norm_title:
                                match = re.search('</strong>(.*?)</p>', post)
                                if match and norm_title == scraper_utils.normalize_title(match.group(1)):
                                    return scraper_utils.pathify_url(url)
                
            page_url = dom_parser.parse_dom(html, 'a', {'class': 'nextpostslink'}, ret='href')
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/')
        search_url += urllib.quote_plus(title)
        html = self._http_get(search_url, require_debrid=True, cache_limit=1)
        if video_type == 'shows':
            seen_urls = {}
            for post in dom_parser.parse_dom(html, 'div', {'id': 'post-\d+'}):
                if 'shows' in post:
                    match = re.search('<span>\s*TAGS:\s*</span>\s*<a\s+href="([^"]+)[^>]+>([^<]+)', post, re.I)
                    if match:
                        show_url, match_title = match.groups()
                        if show_url not in seen_urls:
                            result = {'url': scraper_utils.pathify_url(show_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                            seen_urls[show_url] = result
                            results.append(result)
        elif video_type == 'movies':
            headings = re.findall('<h2>\s*<a\s+href="([^"]+)[^>]+>(.*?)</a>', html)
            posts = dom_parser.parse_dom(html, 'div', {'id': 'post-\d+'})
            norm_title = scraper_utils.normalize_title(title)
            for heading, post in zip(headings, posts):
                if 'movies' in post and not self.__too_old(post):
                    post_url, post_title = heading
                    match = re.search('(.*?)\s*[.\[(]?(\d{4})[.)\]]?\s*(.*)', post_title)
                    if match:
                        match_title, match_year, extra_title = match.groups()
                        full_title = '%s [%s]' % (match_title, extra_title)
                    else:
                        full_title = match_title = post_title
                        match_year = ''
                    
                    match_norm_title = scraper_utils.normalize_title(match_title)
                    if (match_norm_title in norm_title or norm_title in match_norm_title) and (not year or not match_year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(post_url), 'title': scraper_utils.cleanse_title(full_title), 'year': match_year}
                        results.append(result)
        
        return results

    def __too_old(self, post):
        filter_days = datetime.timedelta(days=int(60))
        if filter_days:
            today = datetime.date.today()
            match = re.search('<a[^>]+title="posting time[^"]*">(.*?)\s+(\d+)\s*(\d{2,4})<', post)
            if match:
                try:
                    mon_name, post_day, post_year = match.groups()
                    post_year = int(post_year)
                    if post_year < 2000:
                        post_year += 2000
                    post_month = SHORT_MONS.index(mon_name) + 1
                    post_date = datetime.date(post_year, post_month, int(post_day))
                    if today - post_date > filter_days:
                        return True
                except ValueError:
                    return False
        
        return False
