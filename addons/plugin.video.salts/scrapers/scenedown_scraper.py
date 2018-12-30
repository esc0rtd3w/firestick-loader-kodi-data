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
import base64
import urllib
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import SHORT_MONS
from salts_lib.utils2 import i18n
import scraper

BASE_URL = 'http://scenedown.in'
SEARCH_URL = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxNjA3NTg1ODQxODU0MjAzNDgxODpiX21vd3ZnZDFkbSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.headers = {'User-Agent': USER_AGENT}

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SceneDown'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, headers=self.headers, require_debrid=True, cache_limit=.5)
        sources = self.__get_post_links(html, video)
        for source in sources:
            if scraper_utils.excluded_link(source): continue
            host = urlparse.urlparse(source).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source], 'direct': False}
            hosters.append(hoster)
        return hosters

    def __get_post_links(self, html, video):
        sources = {}
        post = dom_parser2.parse_dom(html, 'div', {'class': 'postContent'})
        if post:
            post = post[0].content
            for fragment in re.finditer('(<strong>.*?)(?=<strong>|$)', post, re.DOTALL):
                fragment = fragment.group(1)
                release = dom_parser2.parse_dom(fragment, 'strong')
                if release:
                    release = release[0].content
                    meta = scraper_utils.parse_episode_link(release)
                    release_quality = scraper_utils.height_get_quality(meta['height'])
                    for attrs, _content in dom_parser2.parse_dom(fragment, 'a', req='href'):
                        link = attrs['href']
                        host = urlparse.urlparse(link).hostname
                        quality = scraper_utils.get_quality(video, host, release_quality)
                        sources[link] = quality
        return sources
        
    def get_url(self, video):
        return self._blog_get_url(video)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-filter" type="slider" range="0,180" option="int" label="     %s" default="60" visible="eq(-3,true)"/>' % (name, i18n('filter_results_days')))
        settings.append('         <setting id="%s-select" type="enum" label="     %s" lvalues="30636|30637" default="0" visible="eq(-4,true)"/>' % (name, i18n('auto_select')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = base64.decodestring(SEARCH_URL) % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=2)
        if html:
            js_data = scraper_utils.parse_json(html)
            search_meta = scraper_utils.parse_episode_link(title)
            for item in js_data.get('results', []):
                metatags = item.get('richSnippet', {}).get('metatags', {})
                post_date = metatags.get('articlePublishedTime')
                if post_date:
                    post_date = re.sub('[+-]\d+:\d+$', '', post_date)
                    post_date = scraper_utils.to_datetime(post_date, '%Y-%m-%dT%H:%M:%S').date()
                    if self.__too_old(post_date): continue
                
                match_title = metatags.get('ogTitle', '')
                if not match_title:
                    match_title = item['titleNoFormatting']
                    match_title = re.sub(re.compile('\s*-\s*Scene\s*Down$', re.I), '', match_title)
                match_url = item['url']
                match_year = ''
                item_meta = scraper_utils.parse_episode_link(match_title)
                if scraper_utils.meta_release_check(video_type, search_meta, item_meta):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        
        if not results:
            results = self.__site_search(video_type, title, year)
            
        return results

    def __site_search(self, video_type, title, year):
        results = []
        html = self._http_get(self.base_url, params={'s': title, 'submit': 'Find'}, headers=self.headers, require_debrid=True, cache_limit=1)
        post_pattern = 'class="postTitle">.*?href="(?P<url>[^"]+)[^>]*>(?P<post_title>[^<]+)'
        for _attrs, post in dom_parser2.parse_dom(html, 'div', {'class': 'post'}):
            if self.__too_old(post): continue
            results += self._blog_proc_results(post, post_pattern, '', video_type, title, year)
        return results
    
    def __too_old(self, post):
        try:
            filter_days = datetime.timedelta(days=int(kodi.get_setting('%s-filter' % (self.get_name()))))
            if filter_days:
                post_date = re.search('class="postMonth"\s+title="(\d+)[^>]*>([^<]+).*?class="postDay"[^>]*>(\d+)', post, re.DOTALL)
                year, mon_name, day = post_date.groups()
                post_date = '%s-%s-%s' % (year, SHORT_MONS.index(mon_name) + 1, day)
                post_date = scraper_utils.to_datetime(post_date, '%Y-%m-%d').date()
                if datetime.date.today() - post_date > filter_days:
                    return True
        except:
            return False
        
        return False
