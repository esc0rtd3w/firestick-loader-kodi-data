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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
from salts_lib.utils2 import i18n
import scraper

BASE_URL = 'http://rlsbb.ru'
SEARCH_BASE_URL = 'http://search.rlsbb.ru'
CATEGORIES = {VIDEO_TYPES.MOVIE: '/category/movies/"', VIDEO_TYPES.EPISODE: '/category/tv-shows/"'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    def __add_host(self, url, host):
        parts = urlparse.urlparse(url)
        return '%s://%s.%s' % (parts.scheme, host, parts.netloc)
    
    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'ReleaseBB'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, require_debrid=True, cache_limit=.5)
        if not html:
            url = scraper_utils.urljoin(self.old_base_url, source_url)
            html = self._http_get(url, require_debrid=True, cache_limit=.5)
            
        sources.update(self.__get_post_links(html, video))
        
        if kodi.get_setting('%s-include_comments' % (self.get_name())) == 'true':
            for _attrs, comment in dom_parser2.parse_dom(html, 'div', {'id': re.compile('commentbody-\d+')}):
                sources.update(self.__get_comment_links(comment, video))

        for source in sources:
            if scraper_utils.excluded_link(source): continue
            host = urlparse.urlparse(source).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'views': None, 'url': source, 'rating': None, 'quality': sources[source], 'direct': False}
            hosters.append(hoster)
        return hosters

    def __get_comment_links(self, comment, video):
        sources = {}
        for attrs, _content in dom_parser2.parse_dom(comment, 'a', req='href'):
            stream_url = attrs['href']
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.blog_get_quality(video, stream_url, host)
            sources[stream_url] = quality
        return sources
    
    def __get_post_links(self, html, video):
        sources = {}
        post = dom_parser2.parse_dom(html, 'div', {'class': 'postContent'})
        if post:
            post = post[0].content
            results = re.findall('<p\s+style="text-align:\s*center;">(?:\s*<strong>)*(.*?)<br(.*?)</p>', post, re.DOTALL)
            if not results:
                match = re.search('>Release Name\s*:(.*?)<br', post, re.I)
                release = match.group(1) if match else ''
                match = re.search('>Download\s*:(.*?)</p>', post, re.DOTALL | re.I)
                links = match.group(1) if match else ''
                results = [(release, links)]
            
            for result in results:
                release, links = result
                release = re.sub('</?[^>]*>', '', release)
                for attrs, hostname in dom_parser2.parse_dom(links, 'a', req='href'):
                    stream_url = attrs['href']
                    if hostname.upper() in ['TORRENT SEARCH', 'VIP FILE']: continue
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.blog_get_quality(video, release, host)
                    sources[stream_url] = quality
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
        settings.append('         <setting id="%s-include_comments" type="bool" label="     %s" default="false" visible="eq(-5,true)"/>' % (name, i18n('include_comments')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        referer = scraper_utils.urljoin(SEARCH_BASE_URL, '/search/')
        headers = {'Referer': referer + urllib.quote_plus(title)}
        headers.update(XHR)
        search_url = scraper_utils.urljoin(SEARCH_BASE_URL, '/lib/search526049.php')
        params = {'phrase': title, 'pindex': 1}
        html = self._http_get(search_url, params=params, headers=headers, require_debrid=True, cache_limit=1)
        js_data = scraper_utils.parse_json(html, search_url)
        for post in js_data.get('results', []):
            if self.__too_old(post): continue
            result = self._blog_proc_results(post.get('post_title', ''), '(?P<post_title>.+)(?P<url>.*?)', '', video_type, title, year)
            if result:
                result[0]['url'] = scraper_utils.pathify_url(post['post_name'])
                results.append(result[0])
        return results

    def __too_old(self, post):
        filter_days = datetime.timedelta(days=int(kodi.get_setting('%s-filter' % (self.get_name()))))
        post_date = post.get('post_date', '')
        if filter_days and post_date:
            today = datetime.date.today()
            try:
                post_date = scraper_utils.to_datetime(post_date, '%Y-%m-%d %H:%M:%S').date()
                if today - post_date > filter_days:
                    return True
            except ValueError:
                return False
        return False
