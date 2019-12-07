"""
    SALTS XBMC Addon
    Copyright (C) 2015 tknorris

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
import datetime
import xbmc
import xbmcgui
import xbmcvfs
import log_utils
import kodi
import utils
import utils2
import image_scraper
from constants import *  # @UnusedWildImport
from trakt_api import Trakt_API
from db_utils import DB_Connection
from scrapers import *  # import all scrapers into this namespace @UnusedWildImport

logger = log_utils.Logger.get_logger(__name__)
logger.disable()

db_connection = DB_Connection()
last_check = datetime.datetime.fromtimestamp(0)
TOKEN = kodi.get_setting('trakt_oauth_token')
use_https = kodi.get_setting('use_https') == 'true'
trakt_timeout = int(kodi.get_setting('trakt_timeout'))
list_size = int(kodi.get_setting('list_size'))
offline = kodi.get_setting('trakt_offline') == 'true'
trakt_api = Trakt_API(TOKEN, use_https, list_size, trakt_timeout, offline)
GENRES = {}

def make_info(item, show=None, people=None):
    if people is None: people = {}
    if show is None: show = {}
    # logger.log('Making Info: Show: %s' % (show), log_utils.LOGDEBUG)
    # logger.log('Making Info: Item: %s' % (item), log_utils.LOGDEBUG)
    info = {}
    info['originaltitle'] = info['title'] = item['title']
    if 'originaltitle' in item: info['originaltitle'] = item['originaltitle']
    info['mediatype'] = 'tvshow' if 'aired_episodes' in item else 'movie'
    if 'overview' in item: info['plot'] = info['plotoutline'] = item['overview']
    if 'runtime' in item and item['runtime'] is not None: info['duration'] = item['runtime'] * 60
    if 'certification' in item: info['mpaa'] = item['certification']
    if 'year' in item: info['year'] = item['year']
    if 'season' in item: info['season'] = item['season']
    if 'episode' in item: info['episode'] = item['episode']
    if 'number' in item: info['episode'] = item['number']
    if 'genres' in item and item['genres']:
        genres = get_genres()
        item_genres = [genres[genre] for genre in item['genres'] if genre in genres]
        info['genre'] = ', '.join(item_genres)
    if 'network' in item: info['studio'] = item['network']
    if 'status' in item: info['status'] = item['status']
    if 'tagline' in item: info['tagline'] = item['tagline']
    if 'watched' in item and item['watched']: info['playcount'] = 1
    if 'plays' in item and item['plays']: info['playcount'] = item['plays']
    if 'rating' in item: info['rating'] = item['rating']
    if 'votes' in item: info['votes'] = item['votes']
    if 'released' in item: info['premiered'] = item['released']
    if 'trailer' in item and item['trailer']: info['trailer'] = utils2.make_trailer(item['trailer'])
    if 'first_aired' in item: info['aired'] = info['premiered'] = utils2.make_air_date(item['first_aired'])
    info.update(utils2.make_ids(item))

    if 'aired_episodes' in item:
        info['episode'] = info['TotalEpisodes'] = item['aired_episodes']
        info['WatchedEpisodes'] = item['watched_count'] if 'watched_count' in item else 0
        info['UnWatchedEpisodes'] = info['TotalEpisodes'] - info['WatchedEpisodes']

    # override item params with show info if it exists
    if 'certification' in show: info['mpaa'] = show['certification']
    if 'year' in show: info['year'] = show['year']
    if 'runtime' in show and show['runtime'] is not None: info['duration'] = show['runtime'] * 60
    if 'title' in show: info['tvshowtitle'] = show['title']
    if 'network' in show: info['studio'] = show['network']
    if 'status' in show: info['status'] = show['status']
    if 'trailer' in show and show['trailer']: info['trailer'] = utils2.make_trailer(show['trailer'])
    if show: info['mediatype'] = 'episode'
    info.update(utils2.make_ids(show))
    info.update(utils2.make_people(people))
    return info

def get_genres():
    global GENRES
    if not GENRES:
        GENRES = dict((genre['slug'], genre['name']) for genre in trakt_api.get_genres(SECTIONS.TV))
        GENRES.update(dict((genre['slug'], genre['name']) for genre in trakt_api.get_genres(SECTIONS.MOVIES)))
    return GENRES

def make_cast(ids, people, cached=True):
    cast = []
    cast_enable = kodi.get_setting('cast_enable') == 'true'
    for person in people.get('cast', []):
        if cast_enable:
            art = image_scraper.get_person_images(ids, person, cached)
        else:
            art = {'thumb': ''}
            
        cast.append({'name': person['person']['name'], 'role': person['character'], 'thumbnail': art['thumb']})
    
    return cast

def update_url(video, source, old_url, new_url):
    logger.log('Setting Url: %s -> |%s|%s|%s|' % (video, source, old_url, new_url), log_utils.LOGDEBUG)
    if new_url:
        db_connection.set_related_url(video.video_type, video.title, video.year, source, new_url, video.season, video.episode)
    else:
        db_connection.clear_related_url(video.video_type, video.title, video.year, source, video.season, video.episode)

    # clear all episode local urls if tvshow or season url changes
    if new_url != old_url:
        if video.video_type == VIDEO_TYPES.TVSHOW:
            db_connection.clear_related_url(VIDEO_TYPES.EPISODE, video.title, video.year, source)
        elif video.video_type == VIDEO_TYPES.SEASON:
            db_connection.clear_related_url(VIDEO_TYPES.EPISODE, video.title, video.year, source, video.season)
            
def make_source_sort_key():
    sso = kodi.get_setting('source_sort_order')
    # migrate sso to kodi setting
    if not sso:
        sso = db_connection.get_setting('source_sort_order')
        sso = kodi.set_setting('source_sort_order', sso)
        db_connection.set_setting('source_sort_order', '')
        
    sort_key = {}
    i = 0
    scrapers = relevant_scrapers(include_disabled=True)
    scraper_names = [scraper.get_name() for scraper in scrapers]
    if sso:
        sources = sso.split('|')
        sort_key = {}
        for i, source in enumerate(sources):
            if source in scraper_names:
                sort_key[source] = -i

    for j, scraper in enumerate(scrapers):
        if scraper.get_name() not in sort_key:
            sort_key[scraper.get_name()] = -(i + j)

    return sort_key

def get_source_sort_key(item):
    sort_key = make_source_sort_key()
    return -sort_key[item.get_name()]

def parallel_search(scraper, video_type, title, year, season):
    results = scraper.search(video_type, title, year, season)
    return {'name': scraper.get_name(), 'results': results}

def parallel_get_progress(trakt_id, cached, cache_limit):
    progress = trakt_api.get_show_progress(trakt_id, full=True, cached=cached, cache_limit=cache_limit)
    progress['trakt'] = trakt_id  # add in a hacked show_id to be used to match progress up to the show its for
    logger.log('Got progress for Trakt ID: %s' % (trakt_id), log_utils.LOGDEBUG)
    return progress

def parallel_get_url(scraper, video):
    url = scraper.get_url(video)
    logger.log('%s returned url %s' % (scraper.get_name(), url), log_utils.LOGDEBUG)
    if not url: url = ''
    if url == FORCE_NO_MATCH:
        label = '[%s] [COLOR green]%s[/COLOR]' % (scraper.get_name(), utils2.i18n('force_no_match'))
    else:
        label = '[%s] %s' % (scraper.get_name(), url)
    related = {'class': scraper, 'url': url, 'name': scraper.get_name(), 'label': label}
    return related

def parallel_get_sources(scraper, video):
    start = time.time()
    hosters = scraper.get_sources(video)
    if hosters is None: hosters = []
    if kodi.get_setting('filter_direct') == 'true':
        hosters = [hoster for hoster in hosters if not hoster['direct'] or utils2.test_stream(hoster)]

    found = False
    for hoster in hosters:
        if hoster['host'] is None:
            logger.log('Hoster missing host: %s - %s' % (scraper.get_name(), hoster), log_utils.LOGWARNING)
            found = True
        elif not hoster['direct']:
            hoster['host'] = hoster['host'].lower().strip()
            if isinstance(hoster['host'], unicode):
                hoster['host'] = hoster['host'].encode('utf-8')
    
    if found:
        hosters = [hoster for hoster in hosters if hoster['host'] is not None]
        
    logger.log('%s returned %s sources in %.2fs' % (scraper.get_name(), len(hosters), time.time() - start), log_utils.LOGDEBUG)
    result = {'name': scraper.get_name(), 'hosters': hosters}
    return result

# Run a task on startup. Settings and mode values must match task name
def do_startup_task(task):
    run_on_startup = kodi.get_setting('auto-%s' % task) == 'true' and kodi.get_setting('%s-during-startup' % task) == 'true'
    if run_on_startup and not xbmc.abortRequested:
        logger.log('Service: Running startup task [%s]' % (task), log_utils.LOGNOTICE)
        now = datetime.datetime.now()
        xbmc.executebuiltin('RunPlugin(plugin://%s/?mode=%s)' % (kodi.get_id(), task))
        db_connection.set_setting('%s-last_run' % (task), now.strftime("%Y-%m-%d %H:%M:%S.%f"))

# Run a recurring scheduled task. Settings and mode values must match task name
def do_scheduled_task(task, isPlaying):
    global last_check
    now = datetime.datetime.now()
    if kodi.get_setting('auto-%s' % task) == 'true':
        if last_check < now - datetime.timedelta(minutes=1):
            # logger.log('Check Triggered: Last: %s Now: %s' % (last_check, now), log_utils.LOGDEBUG)
            next_run = get_next_run(task)
            last_check = now
        else:
            # hack next_run to be in the future
            next_run = now + datetime.timedelta(seconds=1)

        # logger.log("Update Status on [%s]: Currently: %s Will Run: %s Last Check: %s" % (task, now, next_run, last_check), log_utils.LOGDEBUG)
        if now >= next_run:
            is_scanning = xbmc.getCondVisibility('Library.IsScanningVideo')
            if not is_scanning:
                during_playback = kodi.get_setting('%s-during-playback' % (task)) == 'true'
                if during_playback or not isPlaying:
                    logger.log('Service: Running Scheduled Task: [%s]' % (task), log_utils.LOGNOTICE)
                    builtin = 'RunPlugin(plugin://%s/?mode=%s)' % (kodi.get_id(), task)
                    xbmc.executebuiltin(builtin)
                    db_connection.set_setting('%s-last_run' % task, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                else:
                    logger.log('Service: Playing... Busy... Postponing [%s]' % (task), log_utils.LOGDEBUG)
            else:
                logger.log('Service: Scanning... Busy... Postponing [%s]' % (task), log_utils.LOGDEBUG)

def get_next_run(task):
    last_run_string = db_connection.get_setting(task + '-last_run')
    if not last_run_string: last_run_string = LONG_AGO
    last_run = utils2.to_datetime(last_run_string, "%Y-%m-%d %H:%M:%S.%f")
    interval = datetime.timedelta(hours=float(kodi.get_setting(task + '-interval')))
    return (last_run + interval)

def keep_search(section, search_text):
    head = int(kodi.get_setting('%s_search_head' % (section)))
    new_head = (head + 1) % SEARCH_HISTORY
    logger.log('Setting %s to %s' % (new_head, search_text), log_utils.LOGDEBUG)
    db_connection.set_setting('%s_search_%s' % (section, new_head), search_text)
    kodi.set_setting('%s_search_head' % (section), str(new_head))

def bookmark_exists(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        if TOKEN:
            bookmark = trakt_api.get_bookmark(trakt_id, season, episode)
        else:
            bookmark = None
        return bookmark is not None
    else:
        return db_connection.bookmark_exists(trakt_id, season, episode)

# returns true if user chooses to resume, else false
def get_resume_choice(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        resume_point = '%s%%' % (trakt_api.get_bookmark(trakt_id, season, episode))
        header = utils2.i18n('trakt_bookmark_exists')
    else:
        resume_point = utils.format_time(db_connection.get_bookmark(trakt_id, season, episode))
        header = utils2.i18n('local_bookmark_exists')
    question = utils2.i18n('resume_from') % (resume_point)
    dialog = xbmcgui.Dialog()
    try:
        return dialog.contextmenu([question, utils2.i18n('start_from_beginning')]) == 0
    except:
        return dialog.yesno(header, question, '', '', utils2.i18n('start_from_beginning'), utils2.i18n('resume')) == 1

def get_bookmark(trakt_id, season, episode):
    if kodi.get_setting('trakt_bookmark') == 'true':
        if TOKEN:
            bookmark = trakt_api.get_bookmark(trakt_id, season, episode)
        else:
            bookmark = None
    else:
        bookmark = db_connection.get_bookmark(trakt_id, season, episode)
    return bookmark

def relevant_scrapers(video_type=None, include_disabled=False, order_matters=False, as_dict=False):
    classes = scraper.Scraper.__class__.__subclasses__(scraper.Scraper)
    classes += proxy.Proxy.__class__.__subclasses__(proxy.Proxy)
    relevant = {} if as_dict else []
    for cls in classes:
        if cls.get_name() and not cls.has_proxy() and (video_type is None or video_type in cls.provides()):
            if include_disabled or utils2.scraper_enabled(cls.get_name()):
                    if as_dict:
                        relevant[cls.get_name()] = cls
                    else:
                        relevant.append(cls)

    if order_matters and not as_dict:
        relevant.sort(key=get_source_sort_key)
    return relevant

def url_exists(video):
    """
    check each source for a url for this video; return True as soon as one is found. If none are found, return False
    """
    max_timeout = int(kodi.get_setting('source_timeout'))
    logger.log('Checking for Url Existence: |%s|' % (video), log_utils.LOGDEBUG)
    for cls in relevant_scrapers(video.video_type):
        if kodi.get_setting('%s-sub_check' % (cls.get_name())) == 'true':
            scraper_instance = cls(max_timeout)
            url = scraper_instance.get_url(video)
            if url:
                logger.log('Found url for |%s| @ %s: %s' % (video, cls.get_name(), url), log_utils.LOGDEBUG)
                return True

    logger.log('No url found for: |%s|' % (video), log_utils.LOGDEBUG)
    return False

def do_disable_check():
    auto_disable = kodi.get_setting('auto-disable')
    disable_limit = int(kodi.get_setting('disable-limit'))
    cur_failures = utils2.get_failures()
    for cls in relevant_scrapers():
        fails = cur_failures.get(cls.get_name(), 0)
        if fails >= disable_limit:
            if auto_disable == DISABLE_SETTINGS.ON:
                kodi.set_setting('%s-enable' % (cls.get_name()), 'false')
                kodi.notify(msg='[COLOR blue]%s[/COLOR] %s' % (cls.get_name(), utils2.i18n('scraper_disabled')), duration=5000)
                cur_failures[cls.get_name()] = 0
            elif auto_disable == DISABLE_SETTINGS.PROMPT:
                dialog = xbmcgui.Dialog()
                line1 = utils2.i18n('disable_line1') % (cls.get_name(), fails)
                line2 = utils2.i18n('disable_line2')
                line3 = utils2.i18n('disable_line3')
                ret = dialog.yesno('SALTS', line1, line2, line3, utils2.i18n('keep_enabled'), utils2.i18n('disable_it'))
                if ret:
                    kodi.set_setting('%s-enable' % (cls.get_name()), 'false')
                    cur_failures[cls.get_name()] = 0
                else:
                    cur_failures[cls.get_name()] = -1
    utils2.store_failures(cur_failures)

def record_sru_failures(fails, total_scrapers, related_list):
    utils2.record_failures(fails)
    timeouts = len(fails)
    timeout_msg = utils2.i18n('scraper_timeout') % (timeouts, total_scrapers) if timeouts else ''
    if timeout_msg:
        kodi.notify(msg=timeout_msg, duration=5000)
        for related in related_list:
            if related['name'] in fails:
                related['label'] = '[COLOR darkred]%s[/COLOR]' % (related['label'])

def is_salts():
    plugin_name = xbmc.getInfoLabel('Container.PluginName')
    logger.log('Is_Salts Test (1): |%s|' % (plugin_name))
    if plugin_name == kodi.get_id():
        return True
    elif not plugin_name:
        path = xbmc.getInfoLabel('ListItem.FileNameAndPath')
        if not path:
            path = xbmc.getInfoLabel('ListItem.Path')
        
        logger.log('Is_Salts Test (2): |%s|' % (path))
        if path:
            try:
                lines = xbmcvfs.File(path).read()
                logger.log('Is_Salts Test (3): |%s|%s|' % (lines, kodi.get_id()))
                if lines:
                    return lines.startswith('plugin://%s' % (kodi.get_id()))
            except:
                return True
        return True
    else:
        return False

def clear_thumbnails(images):
    for url in images.itervalues():
        crc = utils2.crc32(url)
        for ext in ['jpg', 'png']:
            file_name = crc + '.' + ext
            file_path = os.path.join('special://thumbnails', file_name[0], file_name)
            if xbmcvfs.delete(file_path):
                break
            else:
                try:
                    file_path = kodi.translate_path(file_path)
                    os.remove(file_path)
                    break
                except OSError:
                    pass
        else:
            continue
        
        logger.log('Removed thumbnail: %s' % (file_path))
