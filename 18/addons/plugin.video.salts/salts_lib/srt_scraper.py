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
import os
import time
import urllib2
import re
import xbmcvfs
import log_utils
import kodi
from salts_lib import utils2
from constants import VIDEO_TYPES
from constants import SRT_SOURCE
from constants import USER_AGENT
from db_utils import DB_Connection

logger = log_utils.Logger.get_logger(__name__)
logger.disable()

BASE_URL = 'http://www.addic7ed.com'

class SRT_Scraper():
    def __init__(self):
        self.db_connection = DB_Connection()

    def get_tvshow_id(self, title, year=None):
        match_title = title.lower()
        rows = self.db_connection.get_related_url(VIDEO_TYPES.TVSHOW, title, year, SRT_SOURCE)
        if rows:
            tvshow_id = rows[0][0]
            logger.log('Returning local tvshow id: |%s|%s|%s|' % (title, year, tvshow_id), log_utils.LOGDEBUG)
            return tvshow_id

        html = self.__get_cached_url(BASE_URL, 24)
        regex = re.compile('option\s+value="(\d+)"\s*>(.*?)</option')
        site_matches = []
        for item in regex.finditer(html):
            tvshow_id, site_title = item.groups()

            # strip year off title and assign it to year if it exists
            r = re.search('(\s*\((\d{4})\))$', site_title)
            if r:
                site_title = site_title.replace(r.group(1), '')
                site_year = r.group(2)
            else:
                site_year = None

            # print 'show: |%s|%s|%s|' % (tvshow_id, site_title, site_year)
            if match_title == site_title.lower():
                if year is None or year == site_year:
                    self.db_connection.set_related_url(VIDEO_TYPES.TVSHOW, title, year, SRT_SOURCE, tvshow_id)
                    return tvshow_id

                site_matches.append((tvshow_id, site_title, site_year))

        if not site_matches:
            return None
        elif len(site_matches) == 1:
            self.db_connection.set_related_url(VIDEO_TYPES.TVSHOW, title, year, SRT_SOURCE, site_matches[0][0])
            return site_matches[0][0]
        else:
            # there were multiple title matches and year was passed but no exact year matches found
            for match in site_matches:
                # return the match that has no year specified
                if match[2] is None:
                    self.db_connection.set_related_url(VIDEO_TYPES.TVSHOW, title, year, SRT_SOURCE, match[0])
                    return match[0]

    def get_season_subtitles(self, language, tvshow_id, season):
        url = BASE_URL + '/ajax_loadShow.php?show=%s&season=%s&langs=&hd=%s&hi=%s' % (tvshow_id, season, 0, 0)
        html = self.__get_cached_url(url, .25)
        # print html.decode('ascii', 'ignore')
        req_hi = kodi.get_setting('subtitle-hi') == 'true'
        req_hd = kodi.get_setting('subtitle-hd') == 'true'
        items = []
        regex = re.compile('<td>(\d+)</td><td>(\d+)</td><td>.*?</td><td>(.*?)</td><td.*?>(.*?)</td>.*?<td.*?>(.+?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?><a\s+href="(.*?)">.+?</td>',
                           re.DOTALL)
        for match in regex.finditer(html):
            season, episode, srt_lang, version, completed, hi, corrected, hd, srt_url = match.groups()
            if not language or language == srt_lang and (not req_hi or hi) and (not req_hd or hd):
                item = {}
                item['season'] = season
                item['episode'] = episode
                item['language'] = srt_lang
                item['version'] = version

                if completed.lower() == 'completed':
                    item['completed'] = True
                    item['percent'] = '100'
                else:
                    item['completed'] = False
                    r = re.search('([\d.]+)%', completed)
                    if r:
                        item['percent'] = r.group(1)
                    else:
                        item['percent'] = '0'

                item['hi'] = True if hi else False
                item['corrected'] = True if corrected else False
                item['hd'] = True if hd else False
                item['url'] = srt_url
                items.append(item)
        return items

    def get_episode_subtitles(self, language, tvshow_id, season, episode):
        subtitles = self.get_season_subtitles(language, tvshow_id, season)
        items = []
        for subtitle in subtitles:
            if subtitle['episode'] == str(episode):
                items.append(subtitle)

        return items

    def download_subtitle(self, url):
        url = BASE_URL + url
        (response, srt) = self.__get_url(url)
        if not hasattr(response, 'info') or 'Content-Disposition' not in response.info():
            return

        cd = response.info()['Content-Disposition']
        r = re.search('filename="(.*)"', cd)
        if r:
            filename = r.group(1)
        else:
            filename = 'addic7ed_subtitle.srt'
        filename = re.sub('[^\x00-\x7F]', '', filename)
        filename = re.sub('[<>:"/\\|?*]', '_', filename)
        filename = re.sub('_+', '_', filename)

        final_path = os.path.join(kodi.get_setting('subtitle-folder'), filename)
        final_path = kodi.translate_path(final_path)
        if not xbmcvfs.exists(os.path.dirname(final_path)):
            try:
                try: xbmcvfs.mkdirs(os.path.dirname(final_path))
                except: os.makedirs(os.path.dirname(final_path))
            except:
                logger.log('Failed to create directory %s' % os.path.dirname(final_path), log_utils.LOGERROR)
                raise

        with open(final_path, 'w') as f:
            f.write(srt)
        return final_path

    def __get_url(self, url):
        try:
            req = urllib2.Request(url)
            host = BASE_URL.replace('http://', '')
            req.add_header('User-Agent', USER_AGENT)
            req.add_header('Host', host)
            req.add_header('Referer', BASE_URL)
            response = urllib2.urlopen(req, timeout=10)
            body = response.read()
            body = utils2.cleanse_title(body)
            body = body.encode('utf-8')
        except Exception as e:
            kodi.notify(msg='Failed to connect to URL: %s' % (url), duration=5000)
            logger.log('Failed to connect to URL %s: (%s)' % (url, e), log_utils.LOGERROR)
            return ('', '')

        return (response, body)

    def __get_cached_url(self, url, cache=8):
        logger.log('Fetching Cached URL: %s' % url, log_utils.LOGDEBUG)
        before = time.time()

        _created, _res_header, html = self.db_connection.get_cached_url(url, cache_limit=cache)
        if html:
            logger.log('Returning cached result for: %s' % (url), log_utils.LOGDEBUG)
            return html.decode('utf-8')

        logger.log('No cached url found for: %s' % url, log_utils.LOGDEBUG)
        req = urllib2.Request(url)

        host = BASE_URL.replace('http://', '')
        req.add_header('User-Agent', USER_AGENT)
        req.add_header('Host', host)
        req.add_header('Referer', BASE_URL)
        try:
            response = urllib2.urlopen(req, timeout=10)
            html = response.read()
            html = utils2.cleanse_title(html)
        except Exception as e:
            kodi.notify(msg='Failed to connect to URL: %s' % (url), duration=5000)
            logger.log('Failed to connect to URL %s: (%s)' % (url, e), log_utils.LOGERROR)
            return ''

        self.db_connection.cache_url(url, html)
        after = time.time()
        logger.log('Cached Url Fetch took: %.2f secs' % (after - before), log_utils.LOGDEBUG)
        return html
