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
import urllib
import re
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import aa_decoder
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger()

BASE_URL = 'https://watch5s.rs'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD-720P': QUALITIES.HD720}

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
        return 'Watch5s'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, headers=headers, cache_limit=2)
        if video.video_type == VIDEO_TYPES.MOVIE:
            sources.update(self.__scrape_sources(html, page_url))
            pages = set([r.attrs['href'] for r in dom_parser2.parse_dom(html, 'a', {'class': 'btn-eps'}, req='href')])
            active = set([r.attrs['href'] for r in dom_parser2.parse_dom(html, 'a', {'class': 'active'}, req='href')])
            for page in list(pages - active):
                page_url = scraper_utils.urljoin(self.base_url, page)
                html = self._http_get(page_url, headers=headers, cache_limit=2)
                sources.update(self.__scrape_sources(html, page_url))
        else:
            for page in self.__match_episode(video, html):
                page_url = scraper_utils.urljoin(self.base_url, page)
                html = self._http_get(page_url, headers=headers, cache_limit=2)
                sources.update(self.__scrape_sources(html, page_url))
        
        for source, values in sources.iteritems():
            if not source.lower().startswith('http'): continue
            if values['direct']:
                host = scraper_utils.get_direct_hostname(self, source)
                if host != 'gvideo':
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                else:
                    stream_url = source
            else:
                host = urlparse.urlparse(source).hostname
                stream_url = source
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': values['quality'], 'views': None, 'rating': None, 'url': stream_url, 'direct': values['direct']}
            hosters.append(hoster)

        return hosters

    def __scrape_sources(self, html, page_url):
        sources = {}
        headers = {'Referer': page_url, 'Origin': self.base_url}
        match = re.search('player_type\s*:\s*"([^"]+)', html)
        player_type = match.group(1) if match else ''
        if player_type == 'embed':
            sources = self.__get_embed_sources(html)
        else:
            grab_url = self.__get_grab_url(html, page_url)
            if grab_url:
                sources = self.__get_links_from_playlist(grab_url, headers)

        return sources
    
    def __get_embed_sources(self, html):
        sources = {}
        for match in re.finditer('embed_src\s*:\s*"([^"]+)', html):
            sources[match.group(1)] = {'quality': QUALITIES.HIGH, 'direct': False}
        return sources
    
    def __get_grab_url(self, html, page_url):
        grab_url = ''
        episode_id = dom_parser2.parse_dom(html, 'input', {'name': 'episodeID'}, req='value')
        movie_id = re.search('\s+id:\s*"([^"]+)', html)
        if not episode_id or not movie_id: return grab_url
        
        episode_id = episode_id[0].attrs['value']
        movie_id = movie_id.group(1)
        hostname = urlparse.urlparse(page_url).hostname
        headers = {'Referer': page_url}
        for js_url in self.__get_js_url(html):
            if 'watch5s' in js_url:
                match = re.search('''ajax\(\{url:"([^"]+grab[^"]+)''', self.__get_js(js_url, headers, hostname), re.DOTALL | re.I)
                if not match: continue
                hash_id, token, ts = self.__get_params(match.group(1), episode_id, movie_id, page_url)
                if hash_id and token and ts:
                    params = {'hash': hash_id, 'token': token, '_': ts}
                    grab_url = match.group(1) + episode_id + '?' + urllib.urlencode(params)
                    break
            
        return grab_url
    
    def __get_params(self, grab_url, episode_id, movie_id, page_url):
        hash_id, token, ts = None, None, None
        url = scraper_utils.urljoin(grab_url, '/token_v2.php', replace_path=True)
        headers = {'Referer': page_url}
        params = {'eid': episode_id, 'mid': movie_id, '_': int(time.time() * 1000)}
        html = self._http_get(url, params=params, headers=headers, cache_limit=0)
        if aa_decoder.is_aaencoded(html):
            html = aa_decoder.decode(html)
            match1 = re.search("hash\s*=\s*'([^']+)", html)
            match2 = re.search("token\s*=\s*'([^']+)", html)
            match3 = re.search("_\s*=\s*'([^']+)", html)
            if match1 and match2 and match3:
                hash_id = match1.group(1)
                token = match2.group(1)
                ts = match3.group(1)
        else:
            js_data = scraper_utils.parse_json(html, url)
            hash_id, token, ts = js_data.get('hash'), js_data.get('token'), js_data.get('_')
        
        return hash_id, token, ts
    
    def __get_js_url(self, html):
        urls = []
        for match in re.finditer('''<script[^>]*src\s*=\s*(["'])(.*?)\\1''', html, re.I):
            js_url = match.group(2).strip()
            js_url = re.sub('''['"]''', '', js_url)
            if '/' not in js_url:
                js_url = js_url.strip('+')
                pattern = '''var\s+%s\s*=\s*(['"])(.*?)\\1''' % (js_url)
                match = re.search(pattern, html)
                if match:
                    js_url = match.group(2)
            urls.append(js_url)
        return urls
         
    def __get_js(self, js_url, headers, hostname):
        js = ''
        if js_url.startswith('//'):
            js_url = 'https:' + js_url
        elif not js_url.startswith('http'):
            base_url = 'https://' + hostname
            js_url = scraper_utils.urljoin(base_url, js_url)
         
        logger.log('Getting JS: |%s| - |%s|' % (js_url, headers))
        try: js = self._http_get(js_url, headers=headers)
        except: js = ''
        return js
    
    def __get_links_from_playlist(self, grab_url, headers):
        sources = {}
        grab_url = grab_url.replace('\\', '')
        grab_html = self._http_get(grab_url, headers=headers, cache_limit=.5)
        js_data = scraper_utils.parse_json(grab_html, grab_url)
        try: playlist = js_data['playlist'][0]['sources']
        except: playlist = []
        for item in playlist:
            stream_url = item.get('file')
            if stream_url:
                if stream_url.startswith('/'):
                    stream_url = scraper_utils.urljoin(self.base_url, stream_url)
                    redir_url = self._http_get(stream_url, headers=headers, allow_redirect=False, method='HEAD')
                    if redir_url.startswith('http'):
                        stream_url = redir_url
                
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                elif 'label' in item:
                    quality = scraper_utils.height_get_quality(item['label'])
                else:
                    quality = QUALITIES.HIGH
                
                logger.log('Adding stream: %s Quality: %s' % (stream_url, quality), log_utils.LOGDEBUG)
                sources[stream_url] = {'quality': quality, 'direct': True}
                if not kodi.get_setting('scraper_url'): break
        return sources
        
    def _get_episode_url(self, season_url, video):
        url = scraper_utils.urljoin(self.base_url, season_url)
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        html = self._http_get(url, headers=headers, cache_limit=8)
        if self.__match_episode(video, html):
            return scraper_utils.pathify_url(season_url)
        
    def __match_episode(self, video, html):
        matches = []
        for attrs, ep_label in dom_parser2.parse_dom(html, 'a', {'class': 'btn-eps'}, req="href"):
            match = re.search('Ep(?:isode)?\s+(\d+)', ep_label, re.I)
            if match:
                ep_num = match.group(1)
                try: ep_num = int(ep_num)
                except: ep_num = 0
                if int(video.episode) == ep_num:
                    matches.append(attrs['href'])
        return matches
        
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/')
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        html = self._http_get(search_url, params={'q': title}, headers=headers, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_title = dom_parser2.parse_dom(item, 'span', {'class': 'mli-info'})
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            year_frag = dom_parser2.parse_dom(item, 'img', req='alt')
            is_episodes = dom_parser2.parse_dom(item, 'span', {'class': 'mli-eps'})
            
            if (video_type == VIDEO_TYPES.MOVIE and not is_episodes) or (video_type == VIDEO_TYPES.SEASON and is_episodes):
                if match_title and match_url:
                    match_url = match_url[0].attrs['href']
                    match_title = match_title[0].content
                    match_title = re.sub('</?h2>', '', match_title)
                    match_title = re.sub('\s+\d{4}$', '', match_title)
                    if video_type == VIDEO_TYPES.SEASON:
                        if season and not re.search('Season\s+0*%s$' % (season), match_title): continue
                        
                    if not match_url.endswith('/'): match_url += '/'
                    match_url = scraper_utils.urljoin(match_url, 'watch/')
                    match_year = ''
                    if video_type == VIDEO_TYPES.MOVIE and year_frag:
                        match = re.search('\s*-\s*(\d{4})$', year_frag[0].attrs['alt'])
                        if match:
                            match_year = match.group(1)
    
                    match_norm_title = scraper_utils.normalize_title(match_title)
                    title_match = (norm_title in match_norm_title) or (match_norm_title in norm_title)
                    if title_match and (not year or not match_year or year == match_year):
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results
