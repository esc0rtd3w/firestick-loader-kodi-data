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
import time
import re
import urlparse
import urllib
import base64
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import jsunfuck
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper
import xml.etree.ElementTree as ET

logger = log_utils.Logger.get_logger()

BASE_URL = 'https://yesmovies.to'
QP_URL = '/ajax/v2_movie_quick_play/{slug}/{movie_id}/{vid_type}.html'
SL_URL = '/ajax/v4_movie_episodes/{movie_id}'
PLAYLIST_URL1 = '/ajax/movie_embed/{ep_id}'
PLAYLIST_URL2 = '/ajax/movie_sources/{ep_id}'
TOKEN_URL = '/ajax/movie_token?eid={ep_id}&mid={movie_id}&_={ts}'

CODE = '''def retA():
    class Infix:
        def __init__(self, function):
            self.function = function
        def __ror__(self, other):
            return Infix(lambda x, self=self, other=other: self.function(other, x))
        def __or__(self, other):
            return self.function(other)
        def __rlshift__(self, other):
            return Infix(lambda x, self=self, other=other: self.function(other, x))
        def __rshift__(self, other):
            return self.function(other)
        def __call__(self, value1, value2):
            return self.function(value1, value2)
    def my_add(x, y):
        try: return x + y
        except Exception: return str(x) + str(y)
    x = Infix(my_add)
    return %s
param = retA()'''

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'YesMovies'

    def get_sources(self, video):
        hosters = []
        sources = {}
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        movie_id, watching_url, html = self.__get_source_page(video.video_type, page_url)
        
        links = []
        for match in dom_parser2.parse_dom(html, 'li', {'class': 'ep-item'}, req=['data-id', 'data-server']):
            label = dom_parser2.parse_dom(match.content, 'a', req='title')
            if not label: continue
            if video.video_type == VIDEO_TYPES.EPISODE and not self.__episode_match(video, label[0].attrs['title']):
                continue
            links.append((match.attrs['data-server'], match.attrs['data-id']))
            
        for link_type, link_id in links:
            if link_type in ['12', '13', '14', '15']:
                url = scraper_utils.urljoin(self.base_url, PLAYLIST_URL1.format(ep_id=link_id))
                sources.update(self.__get_link_from_json(url))
            elif kodi.get_setting('scraper_url'):
                url = scraper_utils.urljoin(self.base_url, PLAYLIST_URL2.format(ep_id=link_id))
                params = self.__get_params(movie_id, link_id, watching_url)
                if params is not None:
                    url += '?' + urllib.urlencode(params)
                sources.update(self.__get_links_from_json2(url, page_url, video.video_type))
            
        for source in sources:
            if not source.lower().startswith('http'): continue
            if sources[source]['direct']:
                host = scraper_utils.get_direct_hostname(self, source)
                if host != 'gvideo':
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                else:
                    stream_url = source
            else:
                host = urlparse.urlparse(source).hostname
                stream_url = source
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source]['quality'], 'views': None, 'rating': None, 'url': stream_url, 'direct': sources[source]['direct']}
            hosters.append(hoster)
                
        return hosters

    def __get_link_from_json(self, url):
        sources = {}
        html = self._http_get(url, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, url)
        if 'src' in js_result:
            sources[js_result['src']] = {'quality': QUALITIES.HIGH, 'direct': False}
        return sources
    
    def __get_links_from_json2(self, url, page_url, video_type):
        sources = {}
        headers = {'Referer': page_url}
        headers.update(XHR)
        html = self._http_get(url, headers=headers, cache_limit=0)
        js_data = scraper_utils.parse_json(html, url)
        try:
            playlist = js_data.get('playlist', [])
            for source in playlist[0].get('sources', []):
                stream_url = source['file']
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                elif 'label' in source:
                    quality = scraper_utils.height_get_quality(source['label'])
                else:
                    if video_type == VIDEO_TYPES.MOVIE:
                        meta = scraper_utils.parse_movie_link(stream_url)
                    else:
                        meta = scraper_utils.parse_episode_link(stream_url)
                    quality = scraper_utils.height_get_quality(meta['height'])
                sources[stream_url] = {'quality': quality, 'direct': True}
                logger.log('Adding stream: %s Quality: %s' % (stream_url, quality), log_utils.LOGDEBUG)
        except Exception as e:
            logger.log('Exception during yesmovies extract: %s' % (e), log_utils.LOGDEBUG)
        return sources
    
    def __get_links_from_xml(self, url, video, page_url, cookies):
        sources = {}
        try:
            headers = {'Referer': page_url}
            xml = self._http_get(url, cookies=cookies, headers=headers, cache_limit=.5)
            root = ET.fromstring(xml)
            for item in root.findall('.//item'):
                title = item.find('title').text
                if title and title.upper() == 'OOPS!': continue
                for source in item.findall('{http://rss.jwpcdn.com/}source'):
                    stream_url = source.get('file')
                    label = source.get('label')
                    if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    elif label:
                        quality = scraper_utils.height_get_quality(label)
                    elif title:
                        quality = scraper_utils.blog_get_quality(video, title, '')
                    else:
                        quality = scraper_utils.blog_get_quality(video, stream_url, '')
                    sources[stream_url] = {'quality': quality, 'direct': True}
                    logger.log('Adding stream: %s Quality: %s' % (stream_url, quality), log_utils.LOGDEBUG)
        except Exception as e:
            logger.log('Exception during YesMovies XML Parse: %s' % (e), log_utils.LOGWARNING)

        return sources
    
    def __get_source_page(self, video_type, page_url):
        match = re.search('/movie/(.*?)-(\d+)\.html', page_url)
        if not match: return '', '', ''
        slug, movie_id = match.groups()
        
        vid_type = 'movie' if video_type == VIDEO_TYPES.MOVIE else 'series'
        qp_url = QP_URL.format(slug=slug, movie_id=movie_id, vid_type=vid_type)
        qp_url = scraper_utils.urljoin(self.base_url, qp_url)
        headers = {'Referer': scraper_utils.urljoin(self.base_url, page_url)}
        headers.update(XHR)
        html = self._http_get(qp_url, headers=headers, cache_limit=8)
        watching_url = dom_parser2.parse_dom(html, 'a', {'title': re.compile('View all episodes')}, req='href')
        if not watching_url: return '', '', ''
        
        watching_url = watching_url[0].attrs['href']
        page_html = self._http_get(watching_url, headers={'Referer': scraper_utils.urljoin(self.base_url, page_url)}, cache_limit=8)
        for attrs, _content in dom_parser2.parse_dom(page_html, 'img', {'class': 'hidden'}, req='src'):
            _img = self._http_get(attrs['src'], headers={'Referer': watching_url}, cache_limit=8)
        
        sl_url = SL_URL.format(movie_id=movie_id)
        sl_url = scraper_utils.urljoin(self.base_url, sl_url)
        html = self._http_get(sl_url, headers=headers, cache_limit=8)
        js_data = scraper_utils.parse_json(html, sl_url)
        try: html = js_data['html']
        except: html = ''
        return movie_id, watching_url, html
        
    def _get_episode_url(self, season_url, video):
        _movie_id, _watching_url, html = self.__get_source_page(video.video_type, season_url)
        for attrs, _content in dom_parser2.parse_dom(html, 'a', {'href': 'javascript:void(0)'}, req='title'):
            if self.__episode_match(video, attrs['title']):
                return season_url
    
    def __episode_match(self, video, label):
        episode_pattern = 'Episode\s+0*%s(?!\d)' % (video.episode)
        if re.search(episode_pattern, label, re.I):
            return True
        
        if video.ep_title:
            match = re.search('Episode\s+\d+: (.*)', label)
            if match: label = match.group(1)
            if scraper_utils.normalize_title(video.ep_title) in scraper_utils.normalize_title(label):
                return True
        
        return False
        
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/')
        title = re.sub('[^A-Za-z0-9 ]', '', title)
        search_url += '%s.html' % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_title = dom_parser2.parse_dom(item, 'span', {'class': 'mli-info'})
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_year = re.search('class="jt-info">(\d{4})<', item)
            is_episodes = dom_parser2.parse_dom(item, 'span', {'class': 'mli-eps'})
            
            if (video_type == VIDEO_TYPES.MOVIE and not is_episodes) or (video_type == VIDEO_TYPES.SEASON and is_episodes):
                if not match_title or not match_url: continue
                
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                match_title = re.sub('</?h2>', '', match_title)
                match_title = re.sub('\s+\d{4}$', '', match_title)
                if video_type == VIDEO_TYPES.SEASON:
                    if season and not re.search('Season\s+0*%s$' % (season), match_title): continue
                    
                match_year = match_year.group(1) if match_year else ''
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

    def __get_params(self, movie_id, episode_id, page_url):
        params = None
        ts = int(time.time() * 1000)
        token_url = TOKEN_URL.format(ep_id=episode_id, movie_id=movie_id, ts=ts)
        token_url = scraper_utils.urljoin(self.base_url, token_url)
        headers = {'Referer': page_url}
        headers.update(XHR)
        script = self._http_get(token_url, headers=headers, cache_limit=0)
        if '$_$' in script:
            params = self.__uncensored1(script)
        elif script.startswith('[]') and script.endswith('()'):
            params = self.__uncensored2(script)
        else:
            params = self.__uncensored3(script)
            
        if params is None:
            logger.log('Unrecognized js in %s' % (token_url))

        return params
    
    def __uncensored(self, a, b):
        c = ''
        i = 0
        for i, d in enumerate(a):
            e = b[i % len(b) - 1]
            d = int(self.__jav(d) + self.__jav(e))
            c += chr(d)
    
        return base64.b64encode(c)
    
    def __jav(self, a):
        b = str(a)
        code = ord(b[0])
        if 0xD800 <= code and code <= 0xDBFF:
            c = code
            if len(b) == 1:
                return code
            d = ord(b[1])
            return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000
    
        if 0xDC00 <= code and code <= 0xDFFF:
            return code
        return code

    def __uncensored1(self, script):
        try:
            script = '(' + script.split("(_$$)) ('_');")[0].split("/* `$$` */")[-1].strip()
            script = script.replace('(__$)[$$$]', '\'"\'')
            script = script.replace('(__$)[_$]', '"\\\\"')
            script = script.replace('(o^_^o)', '3')
            script = script.replace('(c^_^o)', '0')
            script = script.replace('(_$$)', '1')
            script = script.replace('($$_)', '4')
            
            vGlobals = {"__builtins__": None, '__name__': __name__, 'str': str, 'Exception': Exception}
            vLocals = {'param': None}
            exec(CODE % script.replace('+', '|x|'), vGlobals, vLocals)
            data = vLocals['param'].decode('string_escape')
            x = re.search('''_x=['"]([^"']+)''', data).group(1)
            y = re.search('''_y=['"]([^"']+)''', data).group(1)
            logger.log('Used $_$ method to decode x/y: |%s|%s|' % (x, y))
            return {'x': x, 'y': y}
        except Exception as e:
            logger.log('Exception in x/y decode (1): %s' % (e), log_utils.LOGWARNING)

    def __uncensored2(self, script):
        try:
            js = jsunfuck.JSUnfuck(script).decode()
            x = re.search('''_x=['"]([^"']+)''', js).group(1)
            y = re.search('''_y=['"]([^"']+)''', js).group(1)
            logger.log('Used jsunfuck to decode x/y: |%s|%s|' % (x, y))
            return {'x': x, 'y': y}
        except Exception as e:
            logger.log('Exception in x/y decode (2): %s' % (e), log_utils.LOGWARNING)

    def __uncensored3(self, script):
        try:
            xx = re.search('''_x=['"]([^"']+)''', script).group(1)
            xy = re.search('''_y=['"]([^"']+)''', script).group(1)
            logger.log('script used decode xx/xy: |%s|%s|' % (xx, xy))
            return {'x': xx, 'y': xy}
        except Exception as e:
            logger.log('Exception in xx/xy decode (2): %s' % (e), log_utils.LOGWARNING)
