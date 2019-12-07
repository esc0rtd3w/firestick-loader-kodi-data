# -*- coding: utf-8 -*-
"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris
    Altered by Blazetamer for Velocity

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
from libs import kodi
import scraper_utils
import scrapeit
import main_scrape



def __enum(**enums):
    return type('Enum', (), enums)


FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')

BASE_URL = 'http://dl.hastidownload.biz/2'

class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('swatch_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SeriesWatch'

    def get_sources(self, video,video_type):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            if video_type == 'movies':
            #if video.video_type == VIDEO_TYPES.MOVIE:
                meta = scraper_utils.parse_movie_link(source_url)
                stream_url = source_url + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                quality = scraper_utils.height_get_quality(meta['height'])
                #source = {'hostname': 'RealMovies', 'url': stream_url, 'host': host, 'class': '', 'quality': quality,'views': None, 'rating': None, 'direct': False}
                hoster = {'hostname': 'SeriesWatch', 'host': self._get_direct_hostname(stream_url), 'class': '', 'quality': quality, 'views': None, 'rating': None, 'url': BASE_URL+stream_url, 'direct': True}
                if 'format' in meta: hoster['format'] = meta['format']
                hosters.append(hoster)
            else:
                for episode in self.__match_episode(source_url, video):
                    meta = scraper_utils.parse_episode_link(episode['title'])
                    stream_url = episode['url'] + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    stream_url = stream_url.replace(self.base_url, '')
                    quality = scraper_utils.height_get_quality(meta['height'])
                    #hoster = {'hostname': 'SeriesWatch', 'host': self._get_direct_hostname(stream_url), 'class': '','quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hoster = {'hostname': 'SeriesWatch', 'host': self._get_direct_hostname(stream_url), 'class':'', 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    if 'format' in meta: hoster['format'] = meta['format']
                    if 'size' in episode: hoster['size'] = scraper_utils.format_size(int(episode['size']))
                    hosters.append(hoster)
        main_scrape.apply_urlresolver(hosters)
        return hosters

    def _get_episode_url(self, show_url, video):
        #force_title = scraper_utils.force_title(video)
        if self.__match_episode(show_url, video):
            return scraper_utils.pathify_url(show_url)

    def __match_episode(self, show_url, video):
        episodes = []
        show_url = self.base_url + show_url
        for item in self._get_files(show_url, cache_limit=1):
            if re.search('[._ -]S%02d[._ -]?E%02d[._ -]' % (int(video.season), int(video.episode)), item['title'], re.I):
                episodes.append(item)
        return episodes
                
    def search(self, video_type, title, year, season=''):
        results = []
        if video_type == 'movies':
            results = self.__movie_search(title, year)
        else:
            norm_title = scraper_utils.normalize_title(title)
            html = self._http_get(self.base_url, cache_limit=48)
            for item in self._parse_directory(html):
                if norm_title in scraper_utils.normalize_title(item['title']) and item['directory']:
                    result = {'url': scraper_utils.pathify_url(item['link']), 'title': scraper_utils.cleanse_title(item['title']), 'year': ''}
                    results.append(result)
        return results
    
    def __movie_search(self, title, year,):
        results = []
        norm_title = scraper_utils.normalize_title(title)
        html = self._http_get(self.base_url, cache_limit=48)
        for item in self._parse_directory(html):
            if not item['directory']:
                meta = scraper_utils.parse_movie_link(item['title'])
                if meta['dubbed']: continue
                if (norm_title in scraper_utils.normalize_title(meta['title'])) and (not year or not meta['year'] or year == meta['year']):
                    match_title = meta['title'].replace('.', ' ')
                    match_title += ' [%sp.%s]' % (meta['height'], meta['extra'])
                    result = {'url': scraper_utils.pathify_url(item['link']), 'title': scraper_utils.cleanse_title(match_title), 'year': meta['year']}
                    results.append(result)
        return results
