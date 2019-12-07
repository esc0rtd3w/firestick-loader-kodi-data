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
import random
import sys
import os
import re
import datetime
import time
import shutil
import xbmcplugin
import xbmcgui
import xbmc
import xbmcvfs
import json
import kodi
import log_utils
import utils
from url_dispatcher import URL_Dispatcher
from salts_lib.db_utils import DB_Connection, DatabaseRecoveryError
from salts_lib.srt_scraper import SRT_Scraper
from salts_lib.trakt_api import Trakt_API, TransientTraktError, TraktNotFoundError, TraktError, TraktAuthError
from salts_lib import salts_utils
from salts_lib import utils2
from salts_lib import gui_utils
from salts_lib import strings
from salts_lib import worker_pool
from salts_lib import image_scraper
from salts_lib.constants import *  # @UnusedWildImport
from salts_lib.utils2 import i18n
from scrapers import *  # import all scrapers into this namespace @UnusedWildImport
from scrapers import ScraperVideo

try:
    import urlresolver
except:
    kodi.notify(msg=i18n('smu_failed'), duration=5000)

logger = log_utils.Logger.get_logger()

TOKEN = kodi.get_setting('trakt_oauth_token')
use_https = kodi.get_setting('use_https') == 'true'
trakt_timeout = int(kodi.get_setting('trakt_timeout'))
list_size = int(kodi.get_setting('list_size'))
OFFLINE = kodi.get_setting('trakt_offline') == 'true'
trakt_api = Trakt_API(TOKEN, use_https, list_size, trakt_timeout, OFFLINE)

url_dispatcher = URL_Dispatcher()

@url_dispatcher.register(MODES.MAIN)
def main_menu():
    db_connection.init_database(None)
    if kodi.get_setting('auto-disable') != DISABLE_SETTINGS.OFF:
        salts_utils.do_disable_check()

    kodi.create_item({'mode': MODES.BROWSE, 'section': SECTIONS.MOVIES}, i18n('movies'), thumb=utils2.art('movies.png'), fanart=utils2.art('fanart.jpg'))
    kodi.create_item({'mode': MODES.BROWSE, 'section': SECTIONS.TV}, i18n('tv_shows'), thumb=utils2.art('television.png'), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('settings'): kodi.create_item({'mode': MODES.SETTINGS}, i18n('settings'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    if TOKEN:
        profile = trakt_api.get_user_profile()
        kodi.set_setting('trakt_user', '%s (%s)' % (profile['username'], profile['name']))
            
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.SETTINGS)
def settings_menu():
    kodi.create_item({'mode': MODES.SCRAPERS}, i18n('scraper_sort_order'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    kodi.create_item({'mode': MODES.RES_SETTINGS}, i18n('url_resolver_settings'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.create_item({'mode': MODES.ADDON_SETTINGS}, i18n('addon_settings'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.create_item({'mode': MODES.AUTO_CONF}, i18n('auto_config'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.create_item({'mode': MODES.RESET_BASE_URL}, i18n('reset_base_url'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.create_item({'mode': MODES.AUTH_TRAKT}, i18n('auth_salts'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.create_item({'mode': MODES.REPAIR_URLRESOLVER}, i18n('repair_urlresolver'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    kodi.create_item({'mode': MODES.SHOW_VIEWS}, i18n('set_default_views'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    kodi.create_item({'mode': MODES.BROWSE_URLS}, i18n('remove_cached_urls'), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    kodi.create_item({'mode': MODES.SETTINGS}, 'This addon developed and supported at www.tvaddons.ag', thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.BROWSE, ['section'])
def browse_menu(section):
    section_params = utils2.get_section_params(section)
    section_label = section_params['label_plural']
    section_label2 = section_params['label_single']
    if utils2.menu_on('trending'): kodi.create_item({'mode': MODES.TRENDING, 'section': section}, i18n('trending') % (section_label), thumb=utils2.art('trending.png'), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('popular'): kodi.create_item({'mode': MODES.POPULAR, 'section': section}, i18n('popular') % (section_label), thumb=utils2.art('popular.png'), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('anticipated'): kodi.create_item({'mode': MODES.ANTICIPATED, 'section': section}, i18n('anticipated') % (section_label), thumb=utils2.art('anticipated.png'), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('recent'): kodi.create_item({'mode': MODES.RECENT, 'section': section}, i18n('recently_updated') % (section_label), thumb=utils2.art('recent.png'), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('mosts'): kodi.create_item({'mode': MODES.MOSTS, 'section': section}, i18n('mosts') % (section_label2), thumb=utils2.art('mosts.png'), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('genres'): kodi.create_item({'mode': MODES.GENRES, 'section': section}, i18n('genres'), thumb=utils2.art('genres.png'), fanart=utils2.art('fanart.jpg'))
    add_section_lists(section)
    if TOKEN:
        if utils2.menu_on('on_deck'): kodi.create_item({'mode': MODES.SHOW_BOOKMARKS, 'section': section}, i18n('trakt_on_deck'), thumb=utils2.art('on_deck.png'), fanart=utils2.art('fanart.jpg'))
        if utils2.menu_on('recommended'): kodi.create_item({'mode': MODES.RECOMMEND, 'section': section}, i18n('recommended') % (section_label), thumb=utils2.art('recommended.png'), fanart=utils2.art('fanart.jpg'))
        if utils2.menu_on('collection'): add_refresh_item({'mode': MODES.SHOW_COLLECTION, 'section': section}, i18n('my_collection') % (section_label), utils2.art('collection.png'), utils2.art('fanart.jpg'))
        if utils2.menu_on('history'): kodi.create_item({'mode': MODES.SHOW_HISTORY, 'section': section}, i18n('watched_history'), thumb=utils2.art('watched_history.png'), fanart=utils2.art('fanart.jpg'))
        if utils2.menu_on('favorites'): kodi.create_item({'mode': MODES.SHOW_FAVORITES, 'section': section}, i18n('my_favorites'), thumb=utils2.art('my_favorites.png'), fanart=utils2.art('fanart.jpg'))
        if utils2.menu_on('subscriptions'): add_refresh_item({'mode': MODES.MANAGE_SUBS, 'section': section}, i18n('my_subscriptions'), utils2.art('my_subscriptions.png'), utils2.art('fanart.jpg'))
        if utils2.menu_on('watchlist'): add_refresh_item({'mode': MODES.SHOW_WATCHLIST, 'section': section}, i18n('my_watchlist'), utils2.art('my_watchlist.png'), utils2.art('fanart.jpg'))
        if utils2.menu_on('my_lists'): kodi.create_item({'mode': MODES.MY_LISTS, 'section': section}, i18n('my_lists'), thumb=utils2.art('my_lists.png'), fanart=utils2.art('fanart.jpg'))
        if utils2.menu_on('liked_lists'): add_refresh_item({'mode': MODES.LIKED_LISTS, 'section': section}, i18n('liked_lists'), utils2.art('liked_lists.png'), utils2.art('fanart.jpg'))
    if utils2.menu_on('other_lists'): kodi.create_item({'mode': MODES.OTHER_LISTS, 'section': section}, i18n('other_lists'), thumb=utils2.art('other_lists.png'), fanart=utils2.art('fanart.jpg'))
    if section == SECTIONS.TV:
        if TOKEN:
            if utils2.menu_on('progress'): add_refresh_item({'mode': MODES.SHOW_PROGRESS}, i18n('my_next_episodes'), utils2.art('my_progress.png'), utils2.art('fanart.jpg'))
            if utils2.menu_on('rewatch'): add_refresh_item({'mode': MODES.SHOW_REWATCH}, i18n('my_rewatches'), utils2.art('my_rewatch.png'), utils2.art('fanart.jpg'))
            if utils2.menu_on('my_cal'): add_refresh_item({'mode': MODES.MY_CAL}, i18n('my_calendar'), utils2.art('my_calendar.png'), utils2.art('fanart.jpg'))
        if utils2.menu_on('general_cal'): add_refresh_item({'mode': MODES.CAL}, i18n('general_calendar'), utils2.art('calendar.png'), utils2.art('fanart.jpg'))
        if utils2.menu_on('premiere_cal'): add_refresh_item({'mode': MODES.PREMIERES}, i18n('premiere_calendar'), utils2.art('premiere_calendar.png'), utils2.art('fanart.jpg'))
    if utils2.menu_on('search'): kodi.create_item({'mode': MODES.SEARCH, 'section': section}, i18n('search'), thumb=utils2.art(section_params['search_img']), fanart=utils2.art('fanart.jpg'))
    if utils2.menu_on('search'): add_search_item({'mode': MODES.RECENT_SEARCH, 'section': section}, i18n('recent_searches'), utils2.art(section_params['search_img']), MODES.CLEAR_RECENT)
    if utils2.menu_on('search'): add_search_item({'mode': MODES.SAVED_SEARCHES, 'section': section}, i18n('saved_searches'), utils2.art(section_params['search_img']), MODES.CLEAR_SAVED)
    if OFFLINE:
        kodi.notify(msg='[COLOR blue]***[/COLOR][COLOR red] %s [/COLOR][COLOR blue]***[/COLOR]' % (i18n('trakt_api_offline')))
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()


@url_dispatcher.register(MODES.GENRES, ['section'])
def browse_genres(section):
    for genre in trakt_api.get_genres(section):
        if genre['slug'] == 'none': continue
        kodi.create_item({'mode': MODES.SHOW_GENRE, 'genre': genre['slug'], 'section': section}, genre['name'], utils2.art('%s.png' % (genre['slug'])), fanart=utils2.art('fanart.jpg'))
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.SHOW_GENRE, ['genre', 'section'], ['page'])
def show_genre(genre, section, page=1):
    filters = {'genres': genre}
    genre_list = int(kodi.get_setting('%s_genre_list' % (section)))
    if genre_list == GENRE_LIST.TRENDING:
        list_data = trakt_api.get_trending(section, page, filters=filters)
    elif genre_list == GENRE_LIST.POPULAR:
        list_data = trakt_api.get_popular(section, page, filters=filters)
    elif genre_list == GENRE_LIST.ANTICIPATED:
        list_data = trakt_api.get_anticipated(section, page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_WATCHED_WEEK:
        list_data = trakt_api.get_most_watched(section, 'weekly', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_WATCHED_MONTH:
        list_data = trakt_api.get_most_watched(section, 'monthly', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_WATCHED_ALL:
        list_data = trakt_api.get_most_watched(section, 'all', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_PLAYED_WEEK:
        list_data = trakt_api.get_most_played(section, 'weekly', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_PLAYED_MONTH:
        list_data = trakt_api.get_most_played(section, 'monthly', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_PLAYED_ALL:
        list_data = trakt_api.get_most_played(section, 'all', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_COLLECTED_WEEK:
        list_data = trakt_api.get_most_collected(section, 'weekly', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_COLLECTED_MONTH:
        list_data = trakt_api.get_most_collected(section, 'monthly', page, filters=filters)
    elif genre_list == GENRE_LIST.MOST_COLLECTED_ALL:
        list_data = trakt_api.get_most_collected(section, 'all', page, filters=filters)
    else:
        logger.log('Unrecognized genre list: %s' % (genre_list), log_utils.LOGWARNING)
        list_data = []
        
    make_dir_from_list(section, list_data, query={'mode': MODES.SHOW_GENRE, 'genre': genre, 'section': section}, page=page)

@url_dispatcher.register(MODES.SHOW_BOOKMARKS, ['section'])
def view_bookmarks(section):
    section_params = utils2.get_section_params(section)
    for bookmark in trakt_api.get_bookmarks(section, full=True):
        queries = {'mode': MODES.DELETE_BOOKMARK, 'bookmark_id': bookmark['id']}
        runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
        menu_items = [(i18n('delete_bookmark'), runstring,)]
        
        if bookmark['type'] == 'movie':
            liz, liz_url = make_item(section_params, bookmark['movie'], menu_items=menu_items)
        else:
            liz, liz_url = make_episode_item(bookmark['show'], bookmark['episode'], show_subs=False, menu_items=menu_items)
            label = liz.getLabel()
            label = '%s - %s' % (bookmark['show']['title'], label)
            liz.setLabel(label)
            
        label = liz.getLabel()
        pause_label = ''
        if kodi.get_setting('trakt_bookmark') == 'true':
            pause_label = '[COLOR blue]%.2f%%[/COLOR] %s ' % (bookmark['progress'], i18n('on'))
        paused_at = time.strftime('%Y-%m-%d', time.localtime(utils.iso_2_utc(bookmark['paused_at'])))
        pause_label += '[COLOR deeppink]%s[/COLOR]' % (utils2.make_day(paused_at, use_words=False))
        label = '[%s] %s ' % (pause_label, label)
        liz.setLabel(label)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False, totalItems=0)
    content_type = CONTENT_TYPES.EPISODES if section == SECTIONS.TV else CONTENT_TYPES.MOVIES
    kodi.set_view(content_type, True)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.DELETE_BOOKMARK, ['bookmark_id'])
def delete_bookmark(bookmark_id):
    trakt_api.delete_bookmark(bookmark_id)
    kodi.notify(msg=i18n('bookmark_deleted'))
    kodi.refresh_container()

@url_dispatcher.register(MODES.SHOW_VIEWS)
def show_views():
    for content_type in ['movies', 'tvshows', 'seasons', 'episodes', 'files']:
        kodi.create_item({'mode': MODES.BROWSE_VIEW, 'content_type': content_type}, i18n('set_default_x_view') % (content_type.capitalize()),
                         thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'))
    kodi.end_of_directory()

@url_dispatcher.register(MODES.BROWSE_VIEW, ['content_type'])
def browse_view(content_type):
    kodi.create_item({'mode': MODES.SET_VIEW, 'content_type': content_type}, i18n('set_view_instr') % (content_type.capitalize()), thumb=utils2.art('settings.png'),
                     fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.set_view(content_type, True)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.SET_VIEW, ['content_type'])
def set_default_view(content_type):
    current_view = kodi.get_current_view()
    if current_view:
        kodi.set_setting('%s_view' % (content_type), current_view)
        view_name = xbmc.getInfoLabel('Container.Viewmode')
        kodi.notify(msg=i18n('view_set') % (content_type.capitalize(), view_name))

@url_dispatcher.register(MODES.BROWSE_URLS)
def browse_urls():
    urls = db_connection.get_all_urls(order_matters=True)
    kodi.create_item({'mode': MODES.FLUSH_CACHE}, '***%s***' % (i18n('delete_cache')), thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    for url in urls:
        if url[1]:
            label = '%s (%s)' % (url[0], url[1])
        else:
            label = url[0]
        kodi.create_item({'mode': MODES.DELETE_URL, 'url': url[0], 'data': url[1]}, label, thumb=utils2.art('settings.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    kodi.set_content(CONTENT_TYPES.FILES)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.DELETE_URL, ['url'], ['data'])
def delete_url(url, data=''):
    db_connection.delete_cached_url(url, data)
    kodi.refresh_container()

@url_dispatcher.register(MODES.RES_SETTINGS)
def resolver_settings():
    urlresolver.display_settings()

@url_dispatcher.register(MODES.ADDON_SETTINGS)
def addon_settings():
    kodi.show_settings()

@url_dispatcher.register(MODES.AUTH_TRAKT)
def auth_trakt():
    utils.auth_trakt(Trakt_API, kodi.Translations(strings.STRINGS))

@url_dispatcher.register(MODES.INSTALL_THEMES)
def install_themepak():
    xbmc.executebuiltin('RunPlugin(plugin://script.salts.themepak)')

@url_dispatcher.register(MODES.INSTALL_CACHE)
def install_cache():
    xbmc.executebuiltin('RunPlugin(plugin://script.module.image_cache)')

@url_dispatcher.register(MODES.REPAIR_URLRESOLVER)
def repair_urlresolver():
    try:
        path = os.path.join(kodi.translate_path('special://home'), 'addons', 'script.module.urlresolver')
        shutil.rmtree(path)
        dlg = xbmcgui.Dialog()
        dlg.ok(i18n('repair_urlresolver'), i18n('repair_line_1'))
    except:
        xbmc.executebuiltin('RunPlugin(plugin://script.module.urlresolver)')

@url_dispatcher.register(MODES.RESET_BASE_URL)
def reset_base_url():
    with kodi.WorkingDialog():
        utils2.reset_base_url()
    kodi.notify(msg=i18n('reset_complete'))

@url_dispatcher.register(MODES.AUTO_CONF)
def auto_conf():
    gui_utils.do_auto_config()
    
def add_section_lists(section):
    main_list = []
    main_str = kodi.get_setting('%s_main' % (section))
    if main_str:
        main_list = main_str.split('|')
        other_dict = dict(('%s@%s' % (item[1], item[0]), item) for item in db_connection.get_other_lists(section))
        if TOKEN:
            lists_dict = dict((user_list['ids']['slug'], user_list) for user_list in trakt_api.get_lists())
    
    for list_str in main_list:
        if '@' not in list_str:
            if TOKEN:
                fake_list = {'name': list_str, 'ids': {'slug': list_str}}
                user_list = lists_dict.get(list_str, fake_list)
                add_list_item(section, user_list)
        else:
            other_list = other_dict.get(list_str, list(reversed(list_str.split('@'))))
            #add_other_list_item(MODES.BROWSE, section, other_list)

def add_refresh_item(queries, label, thumb, fanart):
    refresh_queries = {'mode': MODES.FORCE_REFRESH, 'refresh_mode': queries['mode']}
    if 'section' in queries: refresh_queries.update({'section': queries['section']})
    menu_items = [(i18n('force_refresh'), 'RunPlugin(%s)' % (kodi.get_plugin_url(refresh_queries)))]
    kodi.create_item(queries, label, thumb=thumb, fanart=fanart, is_folder=True, menu_items=menu_items)

def add_search_item(queries, label, thumb, clear_mode):
    menu_queries = {'mode': clear_mode, 'section': queries['section']}
    menu_items = [(i18n('clear_all') % (label), 'RunPlugin(%s)' % (kodi.get_plugin_url(menu_queries)))]
    kodi.create_item(queries, label, thumb=thumb, fanart=utils2.art('fanart.jpg'), is_folder=True, menu_items=menu_items)
    
@url_dispatcher.register(MODES.FORCE_REFRESH, ['refresh_mode'], ['section', 'slug', 'username'])
def force_refresh(refresh_mode, section=None, slug=None, username=None):
    kodi.notify(msg=i18n('forcing_refresh'))
    logger.log('Forcing refresh for mode: |%s|%s|%s|%s|' % (refresh_mode, section, slug, username), log_utils.LOGDEBUG)
    now = datetime.datetime.now()
    offset = int(kodi.get_setting('calendar-day'))
    start_date = now + datetime.timedelta(days=offset)
    start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
    if refresh_mode == MODES.SHOW_COLLECTION:
        trakt_api.get_collection(section, cached=False)
    elif refresh_mode == MODES.SHOW_PROGRESS:
        try:
            workers, _progress = get_progress(cached=False)
        finally:
            try: worker_pool.reap_workers(workers, None)
            except: pass
    elif refresh_mode == MODES.MY_CAL:
        trakt_api.get_my_calendar(start_date, 8, cached=False)
    elif refresh_mode == MODES.CAL:
        trakt_api.get_calendar(start_date, 8, cached=False)
    elif refresh_mode == MODES.PREMIERES:
        trakt_api.get_premieres(start_date, 8, cached=False)
    elif refresh_mode == MODES.SHOW_LIST:
        get_list(section, slug, username, cached=False)
    elif refresh_mode == MODES.SHOW_WATCHLIST:
        get_list(section, WATCHLIST_SLUG, username, cached=False)
    elif refresh_mode == MODES.MANAGE_SUBS:
        slug = kodi.get_setting('%s_sub_slug' % (section))
        if slug:
            get_list(section, slug, username, cached=False)
    elif refresh_mode == MODES.LIKED_LISTS:
        trakt_api.get_liked_lists(cached=False)
    elif refresh_mode == MODES.SHOW_REWATCH:
        try:
            workers, _rewatches = get_rewatches(cached=False)
        finally:
            try: worker_pool.reap_workers(workers, None)
            except: pass
    else:
        logger.log('Force refresh on unsupported mode: |%s|' % (refresh_mode), log_utils.LOGWARNING)
        return

    logger.log('Force refresh complete: |%s|%s|%s|%s|' % (refresh_mode, section, slug, username), log_utils.LOGDEBUG)
    kodi.notify(msg=i18n('force_refresh_complete'))

@url_dispatcher.register(MODES.MOSTS, ['section'])
def mosts_menu(section):
    modes = [(MODES.PLAYED, 'most_played_%s'), (MODES.WATCHED, 'most_watched_%s'), (MODES.COLLECTED, 'most_collected_%s')]
    for mode in modes:
        for period in ['weekly', 'monthly', 'all']:
            kodi.create_item({'mode': mode[0], 'section': section, 'period': period}, i18n(mode[1] % (period)), thumb=utils2.art('%s.png' % (mode[1] % (period))), fanart=utils2.art('fanart.jpg'))
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.PLAYED, ['mode', 'section', 'period'], ['page'])
@url_dispatcher.register(MODES.WATCHED, ['mode', 'section', 'period'], ['page'])
@url_dispatcher.register(MODES.COLLECTED, ['mode', 'section', 'period'], ['page'])
def browse_mosts(mode, section, period, page=1):
    if mode == MODES.PLAYED:
        items = trakt_api.get_most_played(section, period, page)
    elif mode == MODES.WATCHED:
        items = trakt_api.get_most_watched(section, period, page)
    elif mode == MODES.COLLECTED:
        items = trakt_api.get_most_collected(section, period, page)
    make_dir_from_list(section, items, query={'mode': mode, 'section': section, 'period': period}, page=page)

@url_dispatcher.register(MODES.SCRAPERS)
def scraper_settings():
    scrapers = salts_utils.relevant_scrapers(None, True, True)
    if kodi.get_setting('toggle_enable') == 'true':
        label = '**%s**' % (i18n('enable_all_scrapers'))
    else:
        label = '**%s**' % (i18n('disable_all_scrapers'))
    kodi.create_item({'mode': MODES.TOGGLE_ALL}, label, thumb=utils2.art('scraper.png'), fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
    COLORS = ['green', 'limegreen', 'greenyellow', 'yellowgreen', 'yellow', 'orange', 'darkorange', 'orangered', 'red', 'darkred']
    fail_limit = int(kodi.get_setting('disable-limit'))
    cur_failures = utils2.get_failures()
    for i, cls in enumerate(scrapers):
        name = cls.get_name()
        label = '%s (Provides: %s)' % (name, str(list(cls.provides())).replace("'", ""))
        if not utils2.scraper_enabled(name):
            label = '[COLOR darkred]%s[/COLOR]' % (label)
            toggle_label = i18n('enable_scraper')
        else:
            toggle_label = i18n('disable_scraper')
        failures = cur_failures.get(cls.get_name(), 0)
        if failures == -1:
            failures = 'N/A'
            index = 0
        else:
            index = min([(int(failures) * (len(COLORS) - 1) / fail_limit), len(COLORS) - 1])
            
        label = '%s. %s [COLOR %s][FL: %s][/COLOR]:' % (i + 1, label, COLORS[index], failures)

        menu_items = []
        if i > 0:
            queries = {'mode': MODES.MOVE_SCRAPER, 'name': name, 'direction': DIRS.UP, 'other': scrapers[i - 1].get_name()}
            menu_items.append([i18n('move_up'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))])
        if i < len(scrapers) - 1:
            queries = {'mode': MODES.MOVE_SCRAPER, 'name': name, 'direction': DIRS.DOWN, 'other': scrapers[i + 1].get_name()}
            menu_items.append([i18n('move_down'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))])
        queries = {'mode': MODES.MOVE_TO, 'name': name}
        menu_items.append([i18n('move_to'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))])
        queries = {'mode': MODES.RESET_FAILS, 'name': name}
        menu_items.append([i18n('reset_fails'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))])
        queries = {'mode': MODES.RESET_REL_URLS, 'name': name}
        menu_items.append([i18n('reset_rel_urls'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))])
        queries = {'mode': MODES.TOGGLE_SCRAPER, 'name': name}
        menu_items.append([toggle_label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))])
        
        queries = {'mode': MODES.TOGGLE_SCRAPER, 'name': name}
        kodi.create_item(queries, label, thumb=utils2.art('scraper.png'), fanart=utils2.art('fanart.jpg'), is_folder=False,
                         is_playable=False, menu_items=menu_items, replace_menu=True)
    kodi.set_content(CONTENT_TYPES.FILES)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.RESET_REL_URLS, ['name'])
def reset_rel_urls(name):
    db_connection.clear_scraper_related_urls(name)
    kodi.notify(msg=i18n('scraper_url_reset') % (name))
    
@url_dispatcher.register(MODES.RESET_FAILS, ['name'])
def reset_fails(name):
    failures = utils2.get_failures()
    failures[name] = 0
    utils2.store_failures(failures)
    kodi.refresh_container()

@url_dispatcher.register(MODES.MOVE_TO, ['name'])
def move_to(name):
    dialog = xbmcgui.Dialog()
    sort_key = salts_utils.make_source_sort_key()
    new_pos = dialog.numeric(0, i18n('new_pos') % (len(sort_key)))
    if new_pos:
        new_pos = int(new_pos)
        old_key = sort_key[name]
        new_key = -new_pos + 1
        if (new_pos <= 0 or new_pos > len(sort_key)) or old_key == new_key:
            return

        for key in sort_key:
            this_key = sort_key[key]
            # moving scraper up
            if new_key > old_key:
                # move everything between the old and new down
                if this_key > old_key and this_key <= new_key:
                    sort_key[key] -= 1
            # moving scraper down
            else:
                # move everything between the old and new up
                if this_key > new_key and this_key <= new_key:
                    sort_key[key] += 1

        sort_key[name] = new_key
    kodi.set_setting('source_sort_order', utils2.make_source_sort_string(sort_key))
    kodi.refresh_container()

@url_dispatcher.register(MODES.MOVE_SCRAPER, ['name', 'direction', 'other'])
def move_scraper(name, direction, other):
    sort_key = salts_utils.make_source_sort_key()
    if direction == DIRS.UP:
        sort_key[name] += 1
        sort_key[other] -= 1
    elif direction == DIRS.DOWN:
        sort_key[name] -= 1
        sort_key[other] += 1
    kodi.set_setting('source_sort_order', utils2.make_source_sort_string(sort_key))
    kodi.refresh_container()

@url_dispatcher.register(MODES.TOGGLE_ALL)
def toggle_scrapers():
    cur_toggle = kodi.get_setting('toggle_enable')
    scrapers = salts_utils.relevant_scrapers(None, True, True)
    for scraper in scrapers:
        kodi.set_setting('%s-enable' % (scraper.get_name()), cur_toggle)

    new_toggle = 'false' if cur_toggle == 'true' else 'true'
    kodi.set_setting('toggle_enable', new_toggle)
    kodi.refresh_container()

@url_dispatcher.register(MODES.TOGGLE_SCRAPER, ['name'])
def toggle_scraper(name):
    if utils2.scraper_enabled(name):
        setting = 'false'
    else:
        setting = 'true'
    kodi.set_setting('%s-enable' % (name), setting)
    kodi.refresh_container()

@url_dispatcher.register(MODES.TRENDING, ['section'], ['page'])
def browse_trending(section, page=1):
    list_data = trakt_api.get_trending(section, page)
    make_dir_from_list(section, list_data, query={'mode': MODES.TRENDING, 'section': section}, page=page)

@url_dispatcher.register(MODES.POPULAR, ['section'], ['page'])
def browse_popular(section, page=1):
    list_data = trakt_api.get_popular(section, page)
    make_dir_from_list(section, list_data, query={'mode': MODES.POPULAR, 'section': section}, page=page)

@url_dispatcher.register(MODES.ANTICIPATED, ['section'], ['page'])
def browse_anticipated(section, page=1):
    list_data = trakt_api.get_anticipated(section, page)
    make_dir_from_list(section, list_data, query={'mode': MODES.ANTICIPATED, 'section': section}, page=page)

@url_dispatcher.register(MODES.RECENT, ['section'], ['page'])
def browse_recent(section, page=1):
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days=7)
    start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
    list_data = trakt_api.get_recent(section, start_date, page)
    make_dir_from_list(section, list_data, query={'mode': MODES.RECENT, 'section': section}, page=page)

@url_dispatcher.register(MODES.RECOMMEND, ['section'])
def browse_recommendations(section):
    list_data = trakt_api.get_recommendations(section)
    make_dir_from_list(section, list_data)

@url_dispatcher.register(MODES.SHOW_HISTORY, ['section'], ['page'])
def show_history(section, page=1):
    section_params = utils2.get_section_params(section)
    history = trakt_api.get_history(section, full=True, page=page)
    totalItems = len(history)
    for item in history:
        if section == SECTIONS.MOVIES:
            item['movie']['watched'] = True
            liz, liz_url = make_item(section_params, item['movie'])
        else:
            show = item['show']
            item['episode']['watched'] = True
            menu_items = []
            queries = {'mode': MODES.SEASONS, 'trakt_id': show['ids']['trakt'], 'title': show['title'], 'year': show['year'], 'tvdb_id': show['ids']['tvdb']}
            menu_items.append((i18n('browse_seasons'), 'Container.Update(%s)' % (kodi.get_plugin_url(queries))),)
            liz, liz_url = make_episode_item(show, item['episode'], show_subs=False, menu_items=menu_items)
            label = liz.getLabel()
            label = '%s - %s' % (show['title'], label)
            liz.setLabel(label)
            
        label = liz.getLabel()
        watched_at = time.strftime('%Y-%m-%d', time.localtime(utils.iso_2_utc(item['watched_at'])))
        header = '[COLOR deeppink]%s[/COLOR]' % (utils2.make_day(watched_at, use_words=False))
        label = '[%s] %s' % (header, label)
        liz.setLabel(label)
        
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False, totalItems=totalItems)
    if page and totalItems >= int(kodi.get_setting('list_size')):
        query = {'mode': MODES.SHOW_HISTORY, 'section': section, 'page': int(page) + 1}
        label = '%s >>' % (i18n('next_page'))
        kodi.create_item(query, label, thumb=utils2.art('nextpage.png'), fanart=utils2.art('fanart.jpg'), is_folder=True)
    content_type = CONTENT_TYPES.EPISODES if section == SECTIONS.TV else CONTENT_TYPES.MOVIES
    kodi.set_view(content_type, True)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.MY_CAL, ['mode'], ['start_date'])
@url_dispatcher.register(MODES.CAL, ['mode'], ['start_date'])
@url_dispatcher.register(MODES.PREMIERES, ['mode'], ['start_date'])
def browse_calendar(mode, start_date=None):
    if start_date is None:
        now = datetime.datetime.now()
        offset = int(kodi.get_setting('calendar-day'))
        start_date = now + datetime.timedelta(days=offset)
        start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
    if mode == MODES.MY_CAL:
        days = trakt_api.get_my_calendar(start_date, 8)
    elif mode == MODES.CAL:
        days = trakt_api.get_calendar(start_date, 8)
    elif mode == MODES.PREMIERES:
        days = trakt_api.get_premieres(start_date, 8)
    make_dir_from_cal(mode, start_date, days)

@url_dispatcher.register(MODES.MY_LISTS, ['section'])
def browse_lists(section):
    lists = trakt_api.get_lists()
    lists.insert(0, {'name': 'watchlist', 'ids': {'slug': salts_utils.WATCHLIST_SLUG}})
    total_items = len(lists)
    for user_list in lists:
        add_list_item(section, user_list, total_items)
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

def add_list_item(section, user_list, total_items=0):
    ids = user_list['ids']
    menu_items = []
    queries = {'mode': MODES.SET_FAV_LIST, 'slug': ids['slug'], 'section': section}
    menu_items.append((i18n('set_fav_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_SUB_LIST, 'slug': ids['slug'], 'section': section}
    menu_items.append((i18n('set_sub_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_REWATCH_LIST, 'slug': ids['slug'], 'section': SECTIONS.TV}
    menu_items.append((i18n('set_rewatch_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.COPY_LIST, 'slug': COLLECTION_SLUG, 'section': section, 'target_slug': ids['slug']}
    menu_items.append((i18n('import_collection'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.FORCE_REFRESH, 'refresh_mode': MODES.SHOW_LIST, 'section': section, 'slug': ids['slug']}
    menu_items.append((i18n('force_refresh'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    if ids['slug'] != salts_utils.WATCHLIST_SLUG:
        if ids['slug'] in kodi.get_setting('%s_main' % (section)).split('|'):
            label = i18n('remove_from_main')
            action = 'remove'
        else:
            label = i18n('add_to_main')
            action = 'add'
        queries = {'mode': MODES.TOGGLE_TO_MENU, 'action': action, 'section': section, 'slug': ids['slug']}
        menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    
    queries = {'mode': MODES.SHOW_LIST, 'section': section, 'slug': ids['slug']}
    kodi.create_item(queries, user_list['name'], thumb=utils2.art('list.png'), fanart=utils2.art('fanart.jpg'), is_folder=True,
                     total_items=total_items, menu_items=menu_items, replace_menu=False)

@url_dispatcher.register(MODES.LIKED_LISTS, ['section'], ['page'])
def browse_liked_lists(section, page=1):
    liked_lists = trakt_api.get_liked_lists(page=page)
    total_items = len(liked_lists)
    for liked_list in liked_lists:
        list_item = (liked_list['list']['user']['username'], liked_list['list']['ids']['slug'])
        add_other_list_item(MODES.LIKED_LISTS, section, list_item, total_items)

    query = {'mode': MODES.LIKED_LISTS, 'section': section}
    if query and page and total_items >= int(kodi.get_setting('list_size')):
        query['page'] = int(page) + 1
        label = '%s >>' % (i18n('next_page'))
        kodi.create_item(query, label, thumb=utils2.art('nextpage.png'), fanart=utils2.art('fanart.jpg'), is_folder=True)
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.OTHER_LISTS, ['section'])
def browse_other_lists(section):
    kodi.create_item({'mode': MODES.ADD_OTHER_LIST, 'section': section}, i18n('add_other_list'), thumb=utils2.art('add_other.png'),
                     fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)

    lists = db_connection.get_other_lists(section)
    total_items = len(lists)
    for other_list in lists:
        add_other_list_item(MODES.OTHER_LISTS, section, other_list, total_items)
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

def add_other_list_item(mode, section, other_list, total_items=0):
    try:
        header = trakt_api.get_list_header(other_list[1], other_list[0], bool(TOKEN))
    except (TraktNotFoundError, TraktAuthError) as e:
        logger.log('List Access Failure: %s' % (e), log_utils.LOGWARNING)
        header = None

    if header:
        if len(other_list) >= 3 and other_list[2]:
            name = other_list[2]
        else:
            name = header['name']
    else:
        name = other_list[1]

    menu_items = []
    if header:
        queries = {'mode': MODES.FORCE_REFRESH, 'refresh_mode': MODES.SHOW_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
        menu_items.append((i18n('force_refresh'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        queries = {'mode': MODES.COPY_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
        menu_items.append((i18n('copy_to_my_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    list_str = '%s@%s' % (other_list[1], other_list[0])
    if list_str in kodi.get_setting('%s_main' % (section)).split('|'):
        label = i18n('remove_from_main')
        action = 'remove'
    else:
        label = i18n('add_to_main')
        action = 'add'
    queries = {'mode': MODES.TOGGLE_TO_MENU, 'action': action, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
    menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    
    if mode == MODES.OTHER_LISTS:
        queries = {'mode': MODES.ADD_OTHER_LIST, 'section': section, 'username': other_list[0]}
        menu_items.append((i18n('add_more_from') % (other_list[0]), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        queries = {'mode': MODES.REMOVE_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
        menu_items.append((i18n('remove_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        queries = {'mode': MODES.RENAME_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0], 'name': name}
        menu_items.append((i18n('rename_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    if header:
        queries = {'mode': MODES.SHOW_LIST, 'section': section, 'slug': other_list[1], 'username': other_list[0]}
    else:
        queries = {'mode': MODES.OTHER_LISTS, 'section': section}
    label = '[[COLOR blue]%s[/COLOR]] %s' % (other_list[0], name)

    kodi.create_item(queries, label, thumb=utils2.art('list.png'), fanart=utils2.art('fanart.jpg'), is_folder=True, total_items=total_items, menu_items=menu_items, replace_menu=True)

@url_dispatcher.register(MODES.TOGGLE_TO_MENU, ['action', 'section', 'slug'], ['username'])
def toggle_to_menu(action, section, slug, username=None):
    if username is None:
        list_str = slug
    else:
        list_str = '%s@%s' % (slug, username)

    setting = '%s_main' % (section)
    main_str = kodi.get_setting(setting)
    if main_str:
        main_list = main_str.split('|')
    else:
        main_list = []
         
    if action == 'add':
        main_list.append(list_str)
    else:
        for i, item in enumerate(main_list):
            if item == list_str:
                del main_list[i]
                break

    main_str = '|'.join(main_list)
    kodi.set_setting(setting, main_str)
    kodi.refresh_container()

@url_dispatcher.register(MODES.REMOVE_LIST, ['section', 'username', 'slug'])
def remove_list(section, username, slug):
    db_connection.delete_other_list(section, username, slug)
    kodi.refresh_container()

@url_dispatcher.register(MODES.RENAME_LIST, ['section', 'slug', 'username', 'name'])
def rename_list(section, slug, username, name):
    new_name = kodi.get_keyboard(i18n('new_name_heading'), name)
    if new_name is not None:
        db_connection.rename_other_list(section, username, slug, new_name)
    kodi.refresh_container()

@url_dispatcher.register(MODES.ADD_OTHER_LIST, ['section'], ['username'])
def add_other_list(section, username=None):
    if username is None:
        username = kodi.get_keyboard(i18n('username_list_owner'))
        
    if username is not None:
        slug = pick_list(None, section, username)
        if slug:
            db_connection.add_other_list(section, username, slug)
            kodi.refresh_container()

def get_rewatches(cached=True):
    rewatches = []
    workers = []
    list_data = get_list(SECTIONS.TV, kodi.get_setting('rewatch_slug'))
    if list_data is not None:
        begin = time.time()
        history = dict((item['show']['ids']['trakt'], item) for item in trakt_api.get_watched(SECTIONS.TV, cached=cached))
        list_order = dict((item['ids']['trakt'], i) for i, item in enumerate(list_data))
        timeout = max_timeout = int(kodi.get_setting('trakt_timeout'))
        try:
            wp = worker_pool.WorkerPool()
            list_size = len(list_data)
            shows = {}
            for show in list_data:
                trakt_id = show['ids']['trakt']
                plays = utils2.make_plays(history.get(trakt_id, {}))
                wp.request(salts_utils.parallel_get_progress, [trakt_id, cached, None])
                shows[trakt_id] = {'show': show, 'plays': plays}
            
            while len(rewatches) < list_size:
                try:
                    logger.log('Waiting on progress - Timeout: %s' % (timeout), log_utils.LOGDEBUG)
                    progress = wp.receive(timeout)
                    trakt_id = progress['trakt']
                    next_episode = utils2.get_next_rewatch(trakt_id, plays, progress)
                    show = shows[trakt_id]['show']
                    logger.log('Next Rewatch: %s (%s) - %s - %s' % (show['title'], show['year'], trakt_id, next_episode), log_utils.LOGDEBUG)
                    if next_episode:
                        rewatch = {'episode': next_episode}
                        rewatch.update(shows[trakt_id])
                        rewatches.append(rewatch)
                    
                    if max_timeout > 0:
                        timeout = max_timeout - (time.time() - begin)
                        if timeout < 0: timeout = 0
                except worker_pool.Empty:
                    logger.log('Get Progress Process Timeout', log_utils.LOGWARNING)
                    timeout = True
                    break
            else:
                logger.log('All progress results received', log_utils.LOGDEBUG)
                timeout = False
                
            if timeout:
                timeout_msg = i18n('progress_timeouts') % (list_size - len(rewatches), list_size)
                kodi.notify(msg=timeout_msg, duration=5000)
                logger.log(timeout_msg, log_utils.LOGWARNING)
            
            rewatches.sort(key=lambda x: list_order[x['show']['ids']['trakt']])
        finally:
            workers = wp.close()

    return workers, rewatches
    
@url_dispatcher.register(MODES.SHOW_REWATCH)
def show_rewatch():
    slug = kodi.get_setting('rewatch_slug')
    if not slug:
        kodi.create_item({'mode': MODES.PICK_REWATCH_LIST, 'section': SECTIONS.TV}, i18n('pick_rewatch_list'), is_folder=False, is_playable=False)
        kodi.set_content(CONTENT_TYPES.ADDONS)
        kodi.end_of_directory()
    else:
        try:
            workers, rewatches = get_rewatches()
            total_items = len(rewatches)
            for rewatch in rewatches:
                show = rewatch['show']
                trakt_id = show['ids']['trakt']
                plays = rewatch['plays']
                next_episode = rewatch['episode']
                episode = trakt_api.get_episode_details(trakt_id, next_episode['season'], next_episode['episode'])
                episode['watched'] = plays.get(next_episode['season'], {}).get(next_episode['episode'], 0) > 0
                
                menu_items = []
                queries = {'mode': MODES.SEASONS, 'trakt_id': trakt_id, 'title': show['title'], 'year': show['year'], 'tvdb_id': show['ids']['tvdb']}
                menu_items.append((i18n('browse_seasons'), 'Container.Update(%s)' % (kodi.get_plugin_url(queries))),)
                label, new_method = utils2.get_next_rewatch_method(trakt_id)
                queries = {'mode': MODES.MANAGE_REWATCH, 'trakt_id': trakt_id, 'new_method': new_method}
                menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
                if episode['watched']:
                    queries = {'mode': MODES.TOGGLE_WATCHED, 'section': SECTIONS.TV, 'season': episode['season'], 'episode': episode['number'], 'watched': True}
                    queries.update(utils2.show_id(show))
                    menu_items.append((i18n('mark_as_watched'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
                
                liz, liz_url = make_episode_item(show, episode, show_subs=False, menu_items=menu_items)
                label = liz.getLabel()
                label = '%s - %s' % (show['title'], label)
                liz.setLabel(label)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False, totalItems=total_items)
            kodi.set_content(CONTENT_TYPES.EPISODES)
            kodi.end_of_directory(cache_to_disc=False)
        finally:
            try: worker_pool.reap_workers(workers, None)
            except UnboundLocalError: pass
            
@url_dispatcher.register(MODES.MANAGE_REWATCH, ['trakt_id', 'new_method'])
def manage_rewatch(trakt_id, new_method):
    min_list = utils2.get_min_rewatch_list()
    max_list = utils2.get_max_rewatch_list()
    if new_method == REWATCH_METHODS.LEAST_WATCHED:
        if trakt_id not in min_list: min_list.append(trakt_id)
        if trakt_id in max_list: max_list.remove(trakt_id)
    elif new_method == REWATCH_METHODS.MOST_WATCHED:
        if trakt_id in min_list: min_list.remove(trakt_id)
        if trakt_id not in max_list: max_list.append(trakt_id)
    else:
        if trakt_id in min_list: min_list.remove(trakt_id)
        if trakt_id in max_list: max_list.remove(trakt_id)
    kodi.set_setting('rewatch_min_list', '|'.join(min_list))
    kodi.set_setting('rewatch_max_list', '|'.join(max_list))
    kodi.refresh_container()
    
@url_dispatcher.register(MODES.SHOW_LIST, ['section', 'slug'], ['username'])
def show_list(section, slug, username=None):
    items = get_list(section, slug, username)
    if items is not None:
        make_dir_from_list(section, items, slug)

@url_dispatcher.register(MODES.SHOW_WATCHLIST, ['section'])
def show_watchlist(section):
    show_list(section, salts_utils.WATCHLIST_SLUG)

@url_dispatcher.register(MODES.SHOW_COLLECTION, ['section'])
def show_collection(section):
    items = trakt_api.get_collection(section)
    sort_key = int(kodi.get_setting('sort_collection'))
    if sort_key == 1:
        items.reverse()
    elif sort_key == 2:
        items.sort(key=lambda x: utils2.title_key(x['title']))
    elif sort_key == 3:
        items.sort(key=lambda x: x['year'])

    # hack aired_episodes to override w/ collected_episodes to workaround trakt.tv cache issue
    if section == SECTIONS.TV:
        for item in items:
            collected_episodes = len([e for s in item['seasons'] if s['number'] != 0 for e in s['episodes']])
            logger.log('%s/%s: Collected: %s - Aired: %s' % (item['ids']['trakt'], item['ids']['slug'], collected_episodes, item['aired_episodes']), log_utils.LOGDEBUG)
            if collected_episodes > item['aired_episodes']:
                item['aired_episodes'] = collected_episodes

    make_dir_from_list(section, items, COLLECTION_SLUG)

def get_progress(cached=True):
    if cached:
        in_cache, result = db_connection.get_cached_function(get_progress.__name__, cache_limit=15 * 60)
        if in_cache:
            return [], utils2.sort_progress(result, sort_order=SORT_MAP[int(kodi.get_setting('sort_progress'))])

    workers = []
    episodes = []
    with kodi.ProgressDialog(i18n('discover_mne'), background=True) as pd:
        begin = time.time()
        timeout = max_timeout = int(kodi.get_setting('trakt_timeout'))
        pd.update(0, line1=i18n('retr_history'))
        progress_list = trakt_api.get_watched(SECTIONS.TV, full=True, noseasons=True, cached=cached)
        if kodi.get_setting('include_watchlist_next') == 'true':
            pd.update(5, line1=i18n('retr_watchlist'))
            watchlist = trakt_api.show_watchlist(SECTIONS.TV)
            watchlist = [{'show': item} for item in watchlist]
            progress_list += watchlist
    
        pd.update(10, line1=i18n('retr_hidden'))
        hidden = set([item['show']['ids']['trakt'] for item in trakt_api.get_hidden_progress(cached=cached)])
        
        shows = {}
        filter_list = set(utils2.get_progress_skip_list())
        force_list = set(utils2.get_force_progress_list())
        use_exclusion = kodi.get_setting('use_cached_exclusion') == 'true'
        progress_size = len(progress_list)
        try:
            wp = worker_pool.WorkerPool(max_workers=50)
            for i, show in enumerate(progress_list):
                trakt_id = show['show']['ids']['trakt']
                # skip hidden shows
                if trakt_id in hidden:
                    continue
                
                # skip cached ended 100% shows
                if use_exclusion and str(trakt_id) in filter_list and str(trakt_id) not in force_list:
                    logger.log('Skipping %s (%s) as cached MNE ended exclusion' % (trakt_id, show['show']['title']), log_utils.LOGDEBUG)
                    continue
        
                percent = (i + 1) * 25 / progress_size + 10
                pd.update(percent, line1=i18n('req_progress') % (show['show']['title']))
                wp.request(salts_utils.parallel_get_progress, [trakt_id, cached, .08])
                shows[trakt_id] = show['show']
            
            total_shows = len(shows)
            progress_count = 0
            while progress_count < total_shows:
                try:
                    logger.log('Waiting for Progress - Timeout: %s' % (timeout), log_utils.LOGDEBUG)
                    progress = wp.receive(timeout)
                    progress_count += 1
                    trakt_id = progress['trakt']
                    show = shows[trakt_id]
                    percent = (progress_count * 65 / total_shows) + 35
                    pd.update(percent, line1=i18n('rec_progress') % (show['title']))
                    if 'next_episode' in progress and progress['next_episode']:
                        episode = {'show': show, 'episode': progress['next_episode']}
                        episode['last_watched_at'] = progress['last_watched_at']
                        episode['percent_completed'] = (progress['completed'] * 100) / progress['aired'] if progress['aired'] > 0 else 0
                        episode['completed'] = progress['completed']
                        episodes.append(episode)
                    else:
                        ended = show['status'] and show['status'].upper() == 'ENDED'
                        completed = progress['completed'] == progress['aired']
                        if ended and completed and str(trakt_id) not in filter_list and str(trakt_id) not in force_list:
                            logger.log('Adding %s (%s) (%s - %s) to MNE exclusion list' % (trakt_id, show['title'], progress['completed'], progress['aired']), log_utils.LOGDEBUG)
                            manage_progress_cache(ACTIONS.ADD, progress['trakt'])
                    
                    if max_timeout > 0:
                        timeout = max_timeout - (time.time() - begin)
                        if timeout < 0: timeout = 0
                except worker_pool.Empty:
                    logger.log('Get Progress Process Timeout', log_utils.LOGWARNING)
                    timeout = True
                    break
            else:
                logger.log('All progress results received', log_utils.LOGDEBUG)
                timeout = False
        finally:
            workers = wp.close()
        
        if timeout:
            timeouts = total_shows - progress_count
            timeout_msg = i18n('progress_timeouts') % (timeouts, total_shows)
            kodi.notify(msg=timeout_msg, duration=5000)
            logger.log(timeout_msg, log_utils.LOGWARNING)
        else:
            # only cache the results if all results were successful
            db_connection.cache_function(get_progress.__name__, result=episodes)
        
    return workers, utils2.sort_progress(episodes, sort_order=SORT_MAP[int(kodi.get_setting('sort_progress'))])

@url_dispatcher.register(MODES.SHOW_PROGRESS)
def show_progress():
    try:
        workers, progress = get_progress()
        for episode in progress:
            logger.log('Episode: Sort Keys: Tile: |%s| Last Watched: |%s| Percent: |%s%%| Completed: |%s|' % (episode['show']['title'], episode['last_watched_at'], episode['percent_completed'], episode['completed']), log_utils.LOGDEBUG)
            first_aired_utc = utils.iso_2_utc(episode['episode']['first_aired'])
            if kodi.get_setting('show_unaired_next') == 'true' or first_aired_utc <= time.time():
                show = episode['show']
                date = utils2.make_day(utils2.make_air_date(episode['episode']['first_aired']))
                if kodi.get_setting('mne_time') != '0':
                    date_time = '%s@%s' % (date, utils2.make_time(first_aired_utc, 'mne_time'))
                else:
                    date_time = date
    
                menu_items = []
                queries = {'mode': MODES.SEASONS, 'trakt_id': show['ids']['trakt'], 'title': show['title'], 'year': show['year'], 'tvdb_id': show['ids']['tvdb']}
                menu_items.append((i18n('browse_seasons'), 'Container.Update(%s)' % (kodi.get_plugin_url(queries))),)
                liz, liz_url = make_episode_item(show, episode['episode'], show_subs=False, menu_items=menu_items)
                label = liz.getLabel()
                label = '[[COLOR deeppink]%s[/COLOR]] %s - %s' % (date_time, show['title'], label)
                liz.setLabel(label)
    
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False)
        kodi.set_content(CONTENT_TYPES.EPISODES)
        kodi.end_of_directory(cache_to_disc=False)
    finally:
        try: worker_pool.reap_workers(workers, None)
        except UnboundLocalError: pass

@url_dispatcher.register(MODES.MANAGE_SUBS, ['section'])
def manage_subscriptions(section):
    slug = kodi.get_setting('%s_sub_slug' % (section))
    if slug:
        next_run = salts_utils.get_next_run(MODES.UPDATE_SUBS)
        label = i18n('update_subs')
        if kodi.get_setting('auto-' + MODES.UPDATE_SUBS) == 'true':
            color = 'green'
            run_str = next_run.strftime("%Y-%m-%d %I:%M:%S %p")
        else:
            color = 'red'
            run_str = i18n('disabled')
        kodi.create_item({'mode': MODES.UPDATE_SUBS, 'section': section}, label % (color, run_str), thumb=utils2.art('update_subscriptions.png'),
                         fanart=utils2.art('fanart.jpg'), is_folder=False, is_playable=False)
        if section == SECTIONS.TV:
            kodi.create_item({'mode': MODES.CLEAN_SUBS}, i18n('cleanup_subs'), thumb=utils2.art('clean_up.png'), fanart=utils2.art('fanart.jpg'),
                             is_folder=False, is_playable=False)
    show_pickable_list(slug, i18n('pick_sub_list'), MODES.PICK_SUB_LIST, section)

@url_dispatcher.register(MODES.SHOW_FAVORITES, ['section'])
def show_favorites(section):
    slug = kodi.get_setting('%s_fav_slug' % (section))
    show_pickable_list(slug, i18n('pick_fav_list'), MODES.PICK_FAV_LIST, section)

@url_dispatcher.register(MODES.PICK_SUB_LIST, ['mode', 'section'])
@url_dispatcher.register(MODES.PICK_FAV_LIST, ['mode', 'section'])
@url_dispatcher.register(MODES.PICK_REWATCH_LIST, ['mode', 'section'])
def pick_list(mode, section, username=None):
    slug, _name = utils.choose_list(Trakt_API, kodi.Translations(strings.STRINGS), username)
    if slug:
        if mode == MODES.PICK_FAV_LIST:
            set_list(MODES.SET_FAV_LIST, slug, section)
        elif mode == MODES.PICK_SUB_LIST:
            set_list(MODES.SET_SUB_LIST, slug, section)
        elif mode == MODES.PICK_REWATCH_LIST:
            set_list(MODES.SET_REWATCH_LIST, slug, SECTIONS.TV)
        else:
            return slug
        kodi.refresh_container()

@url_dispatcher.register(MODES.SET_SUB_LIST, ['mode', 'slug', 'section'])
@url_dispatcher.register(MODES.SET_FAV_LIST, ['mode', 'slug', 'section'])
@url_dispatcher.register(MODES.SET_REWATCH_LIST, ['mode', 'slug', 'section'])
def set_list(mode, slug, section):
    if mode == MODES.SET_FAV_LIST:
        setting = '%s_fav_slug' % (section)
    elif mode == MODES.SET_SUB_LIST:
        setting = '%s_sub_slug' % (section)
    elif mode == MODES.SET_REWATCH_LIST:
        setting = 'rewatch_slug'
    kodi.set_setting(setting, slug)

@url_dispatcher.register(MODES.SEARCH, ['section'])
def search(section, search_text=None):  # @UnusedVariable
    section_params = utils2.get_section_params(section)
    heading = '%s %s' % (i18n('search'), section_params['label_plural'])
    search_text = kodi.get_keyboard(heading)
    if search_text == '':
        kodi.notify(msg=i18n('blank_searches'), duration=5000)
    elif search_text is not None:
        salts_utils.keep_search(section, search_text)
        queries = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': search_text}
        plugin_url = kodi.get_plugin_url(queries)
        kodi.update_container(plugin_url)

@url_dispatcher.register(MODES.RECENT_SEARCH, ['section'])
def recent_searches(section):
    section_params = utils2.get_section_params(section)
    head = int(kodi.get_setting('%s_search_head' % (section)))
    for i in reversed(range(0, SEARCH_HISTORY)):
        index = (i + head + 1) % SEARCH_HISTORY
        search_text = db_connection.get_setting('%s_search_%s' % (section, index))
        if not search_text:
            break

        menu_items = []
        menu_queries = {'mode': MODES.SAVE_SEARCH, 'section': section, 'query': search_text}
        menu_items.append((i18n('save_search'), 'RunPlugin(%s)' % (kodi.get_plugin_url(menu_queries))),)
        menu_queries = {'mode': MODES.DELETE_RECENT, 'section': section, 'index': index}
        menu_items.append((i18n('remove_from_recent'), 'RunPlugin(%s)' % (kodi.get_plugin_url(menu_queries))),)

        queries = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': search_text}
        label = '[%s %s] %s' % (section_params['label_single'], i18n('search'), search_text)
        kodi.create_item(queries, label, thumb=utils2.art(section_params['search_img']), fanart=utils2.art('fanart.png'), is_folder=True, menu_items=menu_items)
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.SAVED_SEARCHES, ['section'])
def saved_searches(section):
    section_params = utils2.get_section_params(section)
    for search in db_connection.get_searches(section, order_matters=True):
        menu_items = []
        refresh_queries = {'mode': MODES.DELETE_SEARCH, 'search_id': search[0]}
        menu_items.append((i18n('delete_search'), 'RunPlugin(%s)' % (kodi.get_plugin_url(refresh_queries))),)
        queries = {'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': search[1]}
        label = '[%s %s] %s' % (section_params['label_single'], i18n('search'), search[1])
        kodi.create_item(queries, label, thumb=utils2.art(section_params['search_img']), fanart=utils2.art('fanart.png'), is_folder=True, menu_items=menu_items)
    kodi.set_content(CONTENT_TYPES.ADDONS)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.CLEAR_RECENT, ['section'])
def clear_recent(section):
    for i in range(0, SEARCH_HISTORY):
        db_connection.set_setting('%s_search_%s' % (section, i), '')
    kodi.notify(msg=i18n('recent_cleared'), duration=2500)

@url_dispatcher.register(MODES.DELETE_RECENT, ['section', 'index'])
def delete_recent(section, index):
    index = int(index)
    head = int(kodi.get_setting('%s_search_head' % (section)))
    logger.log('Head is: %s' % (head), log_utils.LOGDEBUG)
    for i in range(SEARCH_HISTORY, 0, -1):
        pos = (i - 1 + index) % SEARCH_HISTORY
        last_pos = (pos + 1) % SEARCH_HISTORY
        if pos == head:
            break
        
        search_text = db_connection.get_setting('%s_search_%s' % (section, pos))
        logger.log('Moving %s to position %s' % (search_text, last_pos), log_utils.LOGDEBUG)
        db_connection.set_setting('%s_search_%s' % (section, last_pos), search_text)

    logger.log('Blanking position %s' % (last_pos), log_utils.LOGDEBUG)
    db_connection.set_setting('%s_search_%s' % (section, last_pos), '')
    kodi.refresh_container()

@url_dispatcher.register(MODES.SAVE_SEARCH, ['section', 'query'])
def save_search(section, query):
    db_connection.save_search(section, query)

@url_dispatcher.register(MODES.DELETE_SEARCH, ['search_id'])
def delete_search(search_id):
    db_connection.delete_search(search_id)
    kodi.refresh_container()

@url_dispatcher.register(MODES.CLEAR_SAVED, ['section'])
def clear_saved(section):
    for search in db_connection.get_searches(section):
        db_connection.delete_search(search[0])
    kodi.notify(msg=i18n('saved_cleared'), duration=2500)

@url_dispatcher.register(MODES.SEARCH_RESULTS, ['section', 'query'], ['page'])
def search_results(section, query, page=1):
    results = trakt_api.search(section, query, page)
    make_dir_from_list(section, results, query={'mode': MODES.SEARCH_RESULTS, 'section': section, 'query': query}, page=page)

@url_dispatcher.register(MODES.SEASONS, ['trakt_id', 'title', 'year'], ['tvdb_id'])
def browse_seasons(trakt_id, title, year, tvdb_id=None):
    seasons = sorted(trakt_api.get_seasons(trakt_id), key=lambda x: x['number'])
    info = {}
    if TOKEN:
        progress = trakt_api.get_show_progress(trakt_id, hidden=True, specials=True)
        info = utils2.make_seasons_info(progress)

    total_items = len(seasons)
    for season in seasons:
        if kodi.get_setting('show_season0') == 'true' or season['number'] != 0:
            season_info = info.get(str(season['number']), {'season': season['number']})
            liz = make_season_item(season, season_info, trakt_id, title, year, tvdb_id)
            queries = {'mode': MODES.EPISODES, 'trakt_id': trakt_id, 'season': season['number'], 'random': time.time()}
            kodi.add_item(queries, liz, is_folder=True, total_items=total_items)
    kodi.set_view(CONTENT_TYPES.SEASONS, True)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.EPISODES, ['trakt_id', 'season'])
def browse_episodes(trakt_id, season):
    show = trakt_api.get_show_details(trakt_id)
    episodes = trakt_api.get_episodes(trakt_id, season)
    if TOKEN:
        progress = trakt_api.get_show_progress(trakt_id, hidden=True, specials=True)
        episodes = utils2.make_episodes_watched(episodes, progress)

    totalItems = len(episodes)
    now = time.time()
    for episode in episodes:
        utc_air_time = utils.iso_2_utc(episode['first_aired'])
        if kodi.get_setting('show_unaired') == 'true' or utc_air_time <= now:
            if kodi.get_setting('show_unknown') == 'true' or utc_air_time:
                liz, liz_url = make_episode_item(show, episode)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False, totalItems=totalItems)
    kodi.set_view(CONTENT_TYPES.EPISODES, True)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.GET_SOURCES, ['mode', 'video_type', 'title', 'year', 'trakt_id'], ['season', 'episode', 'ep_title', 'ep_airdate'])
@url_dispatcher.register(MODES.SELECT_SOURCE, ['mode', 'video_type', 'title', 'year', 'trakt_id'], ['season', 'episode', 'ep_title', 'ep_airdate'])
@url_dispatcher.register(MODES.DOWNLOAD_SOURCE, ['mode', 'video_type', 'title', 'year', 'trakt_id'], ['season', 'episode', 'ep_title', 'ep_airdate'])
@url_dispatcher.register(MODES.AUTOPLAY, ['mode', 'video_type', 'title', 'year', 'trakt_id'], ['season', 'episode', 'ep_title', 'ep_airdate'])
def get_sources(mode, video_type, title, year, trakt_id, season='', episode='', ep_title='', ep_airdate=''):
    cool_down_active = kodi.get_setting('cool_down') == 'true'
    if not salts_utils.is_salts() or cool_down_active:
        kodi.notify(msg=i18n('playback_limited'))
        return False
    
    timeout = max_timeout = int(kodi.get_setting('source_timeout'))
    if max_timeout == 0: timeout = None
    max_results = int(kodi.get_setting('source_results'))
    begin = time.time()
    fails = set()
    counts = {}
    video = ScraperVideo(video_type, title, year, trakt_id, season, episode, ep_title, ep_airdate)
    active = False if kodi.get_setting('pd_force_disable') == 'true' else True
    cancelled = False
    with kodi.ProgressDialog(i18n('getting_sources'), utils2.make_progress_msg(video), active=active) as pd:
        try:
            wp = worker_pool.WorkerPool()
            scrapers = salts_utils.relevant_scrapers(video_type)
            total_scrapers = len(scrapers)
            for i, cls in enumerate(scrapers):
                if pd.is_canceled(): return False
                scraper = cls(max_timeout)
                wp.request(salts_utils.parallel_get_sources, [scraper, video])
                progress = i * 25 / total_scrapers
                pd.update(progress, line2=i18n('requested_sources_from') % (cls.get_name()))
                fails.add(cls.get_name())
                counts[cls.get_name()] = 0
    
            hosters = []
            result_count = 0
            while result_count < total_scrapers:
                try:
                    logger.log('Waiting on sources - Timeout: %s' % (timeout), log_utils.LOGDEBUG)
                    result = wp.receive(timeout)
                    result_count += 1
                    hoster_count = len(result['hosters'])
                    counts[result['name']] = hoster_count
                    logger.log('Got %s Source Results from %s' % (hoster_count, result['name']), log_utils.LOGDEBUG)
                    progress = (result_count * 75 / total_scrapers) + 25
                    hosters += result['hosters']
                    fails.remove(result['name'])
                    if pd.is_canceled():
                        cancelled = True
                        break
                    
                    if len(fails) > 5:
                        line3 = i18n('remaining_over') % (len(fails), total_scrapers)
                    else:
                        line3 = i18n('remaining_under') % (', '.join([name for name in fails]))
                    pd.update(progress, line2=i18n('received_sources_from') % (hoster_count, len(hosters), result['name']), line3=line3)
    
                    if max_results > 0 and len(hosters) >= max_results:
                        logger.log('Exceeded max results: %s/%s' % (max_results, len(hosters)), log_utils.LOGDEBUG)
                        fails = {}
                        break
    
                    if max_timeout > 0:
                        timeout = max_timeout - (time.time() - begin)
                        if timeout < 0: timeout = 0
                except worker_pool.Empty:
                    logger.log('Get Sources Scraper Timeouts: %s' % (', '.join(fails)), log_utils.LOGWARNING)
                    break
    
            else:
                logger.log('All source results received', log_utils.LOGDEBUG)
        finally:
            workers = wp.close()
            
        try:
            timeout_msg = ''
            if not cancelled:
                utils2.record_failures(fails, counts)
                timeouts = len(fails)
                if timeouts > 4:
                    timeout_msg = i18n('scraper_timeout') % (timeouts, total_scrapers)
                elif timeouts > 0:
                    timeout_msg = i18n('scraper_timeout_list') % ('/'.join([name for name in fails]))
            
            if not hosters:
                logger.log('No Sources found for: |%s|' % (video), log_utils.LOGWARNING)
                msg = i18n('no_sources')
                msg += ' (%s)' % timeout_msg if timeout_msg else ''
                kodi.notify(msg=msg, duration=5000)
                return False
        
            if timeout_msg:
                kodi.notify(msg=timeout_msg, duration=7500)
            
            if not fails: line3 = ' '
            pd.update(100, line2=i18n('applying_source_filters'), line3=line3)
            hosters = utils2.filter_exclusions(hosters)
            hosters = utils2.filter_quality(video_type, hosters)
            hosters = apply_urlresolver(hosters)
            if kodi.get_setting('enable_sort') == 'true':
                SORT_KEYS['source'] = salts_utils.make_source_sort_key()
                hosters.sort(key=utils2.get_sort_key)
            else:
                random.shuffle(hosters)
                local_hosters = []
                for i, item in enumerate(hosters):
                    if isinstance(item['class'], local_scraper.Scraper):
                        local_hosters.append(item)
                        hosters[i] = None
                hosters = local_hosters + [item for item in hosters if item is not None]
                
        finally:
            workers = worker_pool.reap_workers(workers)
    
    try:
        if not hosters:
            logger.log('No Usable Sources found for: |%s|' % (video), log_utils.LOGDEBUG)
            msg = ' (%s)' % timeout_msg if timeout_msg else ''
            kodi.notify(msg=i18n('no_useable_sources') % (msg), duration=5000)
            return False
        
        pseudo_tv = xbmcgui.Window(10000).getProperty('PseudoTVRunning').lower()
        if pseudo_tv == 'true' or (mode == MODES.GET_SOURCES and kodi.get_setting('auto-play') == 'true') or mode == MODES.AUTOPLAY:
            auto_play_sources(hosters, video_type, trakt_id, season, episode)
        else:
            plugin_name = xbmc.getInfoLabel('Container.PluginName')
            if kodi.get_setting('source-win') == 'Dialog' or plugin_name == '':
                stream_url, direct = pick_source_dialog(hosters)
                return play_source(mode, stream_url, direct, video_type, trakt_id, season, episode)
            else:
                pick_source_dir(mode, hosters, video_type, trakt_id, season, episode)
    finally:
        try: worker_pool.reap_workers(workers, None)
        except UnboundLocalError: pass

def apply_urlresolver(hosters):
    filter_unusable = kodi.get_setting('filter_unusable') == 'true'
    show_debrid = kodi.get_setting('show_debrid') == 'true'
    if not filter_unusable and not show_debrid:
        return hosters
    
    debrid_resolvers = [resolver() for resolver in urlresolver.relevant_resolvers(order_matters=True) if resolver.isUniversal()]
    filtered_hosters = []
    debrid_hosts = {}
    unk_hosts = {}
    known_hosts = {}
    for hoster in hosters:
        if 'direct' in hoster and hoster['direct'] is False and hoster['host']:
            host = hoster['host']
            if filter_unusable:
                if host in unk_hosts:
                    # logger.log('Unknown Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                    unk_hosts[host] += 1
                    continue
                elif host in known_hosts:
                    # logger.log('Known Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                    known_hosts[host] += 1
                    filtered_hosters.append(hoster)
                else:
                    hmf = urlresolver.HostedMediaFile(host=host, media_id='12345678901')  # use dummy media_id to force host validation
                    if hmf:
                        # logger.log('Known Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                        known_hosts[host] = known_hosts.get(host, 0) + 1
                        filtered_hosters.append(hoster)
                    else:
                        # logger.log('Unknown Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                        unk_hosts[host] = unk_hosts.get(host, 0) + 1
                        continue
            else:
                filtered_hosters.append(hoster)
            
            if host in debrid_hosts:
                # logger.log('Debrid cache found for %s: %s' % (host, debrid_hosts[host]), log_utils.LOGDEBUG)
                hoster['debrid'] = debrid_hosts[host]
            else:
                temp_resolvers = [resolver.name[:3].upper() for resolver in debrid_resolvers if resolver.valid_url('', host)]
                # logger.log('%s supported by: %s' % (host, temp_resolvers), log_utils.LOGDEBUG)
                debrid_hosts[host] = temp_resolvers
                if temp_resolvers:
                    hoster['debrid'] = temp_resolvers
        else:
            filtered_hosters.append(hoster)
            
    logger.log('Discarded Hosts: %s' % (sorted(unk_hosts.items(), key=lambda x: x[1], reverse=True)), log_utils.LOGDEBUG)
    return filtered_hosters

@url_dispatcher.register(MODES.RESOLVE_SOURCE, ['mode', 'class_url', 'direct', 'video_type', 'trakt_id', 'class_name'], ['season', 'episode'])
@url_dispatcher.register(MODES.DIRECT_DOWNLOAD, ['mode', 'class_url', 'direct', 'video_type', 'trakt_id', 'class_name'], ['season', 'episode'])
def resolve_source(mode, class_url, direct, video_type, trakt_id, class_name, season='', episode=''):
    for cls in salts_utils.relevant_scrapers(video_type):
        if cls.get_name() == class_name:
            scraper_instance = cls()
            break
    else:
        logger.log('Unable to locate scraper with name: %s' % (class_name), log_utils.LOGWARNING)
        return False

    hoster_url = scraper_instance.resolve_link(class_url)
    if mode == MODES.DIRECT_DOWNLOAD:
        kodi.end_of_directory()
    return play_source(mode, hoster_url, direct, video_type, trakt_id, season, episode)

@url_dispatcher.register(MODES.PLAY_TRAILER, ['stream_url'])
def play_trailer(stream_url):
    xbmc.Player().play(stream_url)

def download_subtitles(language, title, year, season, episode):
    srt_scraper = SRT_Scraper()
    tvshow_id = srt_scraper.get_tvshow_id(title, year)
    if tvshow_id is None:
        return

    subs = srt_scraper.get_episode_subtitles(language, tvshow_id, season, episode)
    sub_labels = [utils2.format_sub_label(sub) for sub in subs]

    index = 0
    if len(sub_labels) > 1 and kodi.get_setting('subtitle-autopick') == 'false':
        dialog = xbmcgui.Dialog()
        index = dialog.select(i18n('choose_subtitle'), sub_labels)

    if subs and index > -1:
        return srt_scraper.download_subtitle(subs[index]['url'])

def play_source(mode, hoster_url, direct, video_type, trakt_id, season='', episode=''):
    if hoster_url is None:
        if direct is not None:
            kodi.notify(msg=i18n('resolve_failed') % (i18n('no_stream_found')), duration=7500)
        return False

    with kodi.WorkingDialog() as wd:
        if direct:
            logger.log('Treating hoster_url as direct: %s' % (hoster_url), log_utils.LOGDEBUG)
            stream_url = hoster_url
        else:
            wd.update(25)
            hmf = urlresolver.HostedMediaFile(url=hoster_url)
            if not hmf:
                logger.log('Indirect hoster_url not supported by urlresolver: %s' % (hoster_url), log_utils.LOGDEBUG)
                stream_url = hoster_url
            else:
                try:
                    stream_url = hmf.resolve()
                    if not stream_url or not isinstance(stream_url, basestring):
                        try: msg = stream_url.msg
                        except: msg = hoster_url
                        raise Exception(msg)
                except Exception as e:
                    try: msg = str(e)
                    except: msg = hoster_url
                    kodi.notify(msg=i18n('resolve_failed') % (msg), duration=7500)
                    return False
        wd.update(50)
    
    resume_point = 0
    pseudo_tv = xbmcgui.Window(10000).getProperty('PseudoTVRunning').lower()
    if pseudo_tv != 'true' and mode not in [MODES.DOWNLOAD_SOURCE, MODES.DIRECT_DOWNLOAD]:
        if salts_utils.bookmark_exists(trakt_id, season, episode):
            if salts_utils.get_resume_choice(trakt_id, season, episode):
                resume_point = salts_utils.get_bookmark(trakt_id, season, episode)
                logger.log('Resume Point: %s' % (resume_point), log_utils.LOGDEBUG)
    
    with kodi.WorkingDialog() as wd:
        from_library = xbmc.getInfoLabel('Container.PluginName') == ''
        wd.update(50)
        win = xbmcgui.Window(10000)
        win.setProperty('salts.playing', 'True')
        win.setProperty('salts.playing.trakt_id', str(trakt_id))
        win.setProperty('salts.playing.season', str(season))
        win.setProperty('salts.playing.episode', str(episode))
        win.setProperty('salts.playing.library', str(from_library))
        if resume_point > 0:
            if kodi.get_setting('trakt_bookmark') == 'true':
                win.setProperty('salts.playing.trakt_resume', str(resume_point))
            else:
                win.setProperty('salts.playing.salts_resume', str(resume_point))

        art = {'thumb': '', 'fanart': ''}
        info = {}
        show_meta = {}
        try:
            if video_type == VIDEO_TYPES.EPISODE:
                path = kodi.get_setting('tv-download-folder')
                file_name = utils2.filename_from_title(trakt_id, VIDEO_TYPES.TVSHOW)
                file_name = file_name % ('%02d' % int(season), '%02d' % int(episode))
    
                ep_meta = trakt_api.get_episode_details(trakt_id, season, episode)
                show_meta = trakt_api.get_show_details(trakt_id)
                win.setProperty('script.trakt.ids', json.dumps(show_meta['ids']))
                people = trakt_api.get_people(SECTIONS.TV, trakt_id) if kodi.get_setting('include_people') == 'true' else None
                info = salts_utils.make_info(ep_meta, show_meta, people)
                art = image_scraper.get_images(VIDEO_TYPES.EPISODE, show_meta['ids'], season, episode)
    
                path = make_path(path, VIDEO_TYPES.TVSHOW, show_meta['title'], season=season)
                file_name = utils2.filename_from_title(show_meta['title'], VIDEO_TYPES.TVSHOW)
                file_name = file_name % ('%02d' % int(season), '%02d' % int(episode))
            else:
                path = kodi.get_setting('movie-download-folder')
                file_name = utils2.filename_from_title(trakt_id, video_type)
    
                movie_meta = trakt_api.get_movie_details(trakt_id)
                win.setProperty('script.trakt.ids', json.dumps(movie_meta['ids']))
                people = trakt_api.get_people(SECTIONS.MOVIES, trakt_id) if kodi.get_setting('include_people') == 'true' else None
                info = salts_utils.make_info(movie_meta, people=people)
                art = image_scraper.get_images(VIDEO_TYPES.MOVIE, movie_meta['ids'])
    
                path = make_path(path, video_type, movie_meta['title'], movie_meta['year'])
                file_name = utils2.filename_from_title(movie_meta['title'], video_type, movie_meta['year'])
        except TransientTraktError as e:
            logger.log('During Playback: %s' % (str(e)), log_utils.LOGWARNING)  # just log warning if trakt calls fail and leave meta and art blank
        wd.update(75)

    if mode in [MODES.DOWNLOAD_SOURCE, MODES.DIRECT_DOWNLOAD]:
        utils.download_media(stream_url, path, file_name, kodi.Translations(strings.STRINGS))
        return True

    with kodi.WorkingDialog() as wd:
        wd.update(75)
        if video_type == VIDEO_TYPES.EPISODE and utils2.srt_download_enabled() and show_meta:
            srt_path = download_subtitles(kodi.get_setting('subtitle-lang'), show_meta['title'], show_meta['year'], season, episode)
            if utils2.srt_show_enabled() and srt_path:
                logger.log('Setting srt path: %s' % (srt_path), log_utils.LOGDEBUG)
                win.setProperty('salts.playing.srt', srt_path)
    
        listitem = xbmcgui.ListItem(path=stream_url, iconImage=art['thumb'], thumbnailImage=art['thumb'])
        listitem.setProperty('fanart_image', art['fanart'])
        try: listitem.setArt(art)
        except: pass
        listitem.setPath(stream_url)
        listitem.setInfo('video', info)
        wd.update(100)

    if mode == MODES.RESOLVE_SOURCE or from_library or utils2.from_playlist():
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmc.Player().play(stream_url, listitem)
    return True

def auto_play_sources(hosters, video_type, trakt_id, season, episode):
    total_hosters = len(hosters)
    active = False if kodi.get_setting('pd_force_disable') == 'true' else True
    with kodi.ProgressDialog(i18n('trying_autoplay'), active=active) as pd:
        prev = ''
        for i, item in enumerate(hosters):
            if item['multi-part']:
                continue
    
            percent = i * 100 / total_hosters
            current = i18n('trying_source') % (item['quality'], item['host'], item['class'].get_name())
            pd.update(percent, current, prev)
            if pd.is_canceled(): return False
            hoster_url = item['class'].resolve_link(item['url'])
            logger.log('Auto Playing: %s' % (hoster_url), log_utils.LOGDEBUG)
            if play_source(MODES.GET_SOURCES, hoster_url, item['direct'], video_type, trakt_id, season, episode):
                return True
            if pd.is_canceled(): return False
            prev = i18n('failed_source') % (item['quality'], item['host'], item['class'].get_name())
        else:
            msg = i18n('all_sources_failed')
            logger.log(msg, log_utils.LOGERROR)
            kodi.notify(msg=msg, duration=5000)

def pick_source_dialog(hosters):
    for item in hosters:
        if item['multi-part']:
            continue
        item['label'] = utils2.format_source_label(item)

    dialog = xbmcgui.Dialog()
    index = dialog.select(i18n('choose_stream'), [item['label'] for item in hosters if 'label' in item])
    if index > -1:
        try:
            hoster = hosters[index]
            if hoster['url']:
                hoster_url = hoster['class'].resolve_link(hoster['url'])
                logger.log('Attempting to play url: %s as direct: %s from: %s' % (hoster_url, hoster['direct'], hoster['class'].get_name()), log_utils.LOGNOTICE)
                return hoster_url, hoster['direct']
        except Exception as e:
            logger.log('Error (%s) while trying to resolve %s' % (str(e), hoster['url']), log_utils.LOGERROR)

    return None, None

def pick_source_dir(prev_mode, hosters, video_type, trakt_id, season, episode):
    db_connection.cache_sources(hosters)
    queries = {'mode': MODES.BUILD_SOURCE_DIR, 'prev_mode': prev_mode, 'video_type': video_type, 'trakt_id': trakt_id, 'season': season, 'episode': episode}
    plugin_url = kodi.get_plugin_url(queries)
    kodi.update_container(plugin_url)
    
@url_dispatcher.register(MODES.BUILD_SOURCE_DIR, ['prev_mode', 'video_type', 'trakt_id'], ['season', 'episode'])
def build_source_dir(prev_mode, video_type, trakt_id, season='', episode=''):
    if prev_mode == MODES.DOWNLOAD_SOURCE:
        next_mode = MODES.DIRECT_DOWNLOAD
        playable = False
    else:
        next_mode = MODES.RESOLVE_SOURCE
        playable = True

    scrapers = salts_utils.relevant_scrapers(video_type, as_dict=True)
    hosters = db_connection.get_cached_sources()
    hosters_len = len(hosters)
    for item in hosters:
        if item['name'] in scrapers:
            item['class'] = scrapers[item['name']]()
        else:
            logger.log('Skipping hoster with unknown name: %s' % (item))
            continue

        if item['multi-part']:
            continue

        menu_items = []
        item['label'] = utils2.format_source_label(item)
        queries = {'mode': MODES.SET_VIEW, 'content_type': CONTENT_TYPES.FILES}
        menu_items.append((i18n('set_as_sources_view'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        if next_mode == MODES.RESOLVE_SOURCE:
            queries = {'mode': MODES.DIRECT_DOWNLOAD, 'class_url': item['url'], 'direct': item['direct'], 'video_type': video_type, 'trakt_id': trakt_id,
                       'season': season, 'episode': episode, 'class_name': item['class'].get_name()}
            menu_items.append((i18n('download_source'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        
        queries = {'mode': next_mode, 'class_url': item['url'], 'direct': item['direct'], 'video_type': video_type, 'trakt_id': trakt_id,
                   'season': season, 'episode': episode, 'class_name': item['class'].get_name()}
        kodi.create_item(queries, utils2.cleanse_title(item['label']), is_folder=False, is_playable=playable, total_items=hosters_len, menu_items=menu_items)
    kodi.set_view(CONTENT_TYPES.FILES, True)
    kodi.end_of_directory()

@url_dispatcher.register(MODES.SET_URL_MANUAL, ['mode', 'video_type', 'title', 'year', 'trakt_id'], ['season', 'episode', 'ep_title', 'ep_airdate'])
@url_dispatcher.register(MODES.SET_URL_SEARCH, ['mode', 'video_type', 'title', 'year', 'trakt_id'], ['season', 'episode', 'ep_title', 'ep_airdate'])
def set_related_url(mode, video_type, title, year, trakt_id, season='', episode='', ep_title='', ep_airdate=''):
    try:
        video = ScraperVideo(video_type, title, year, trakt_id, season, episode, ep_title, ep_airdate)
        workers, related_list = get_related_urls(video)
        while True:
            dialog = xbmcgui.Dialog()
            if mode == MODES.SET_URL_SEARCH:
                select_list = [('***%s' % (i18n('manual_search_all')))]
                adjustment = 2
            else:
                adjustment = 1
                select_list = []
            select_list += ['***%s' % (i18n('rescrape_all'))]
            select_list += [related['label'] for related in related_list]
            
            index = dialog.select(i18n('url_to_change') % (video_type), select_list)
            if index == 0:
                if mode == MODES.SET_URL_SEARCH:
                    related_list = sru_search_all(video, related_list)
                else:
                    related_list = reset_all_urls(video, related_list)
            elif index == 1 and mode == MODES.SET_URL_SEARCH:
                related_list = reset_all_urls(video, related_list)
            elif index > adjustment - 1:
                index = index - adjustment
                if mode == MODES.SET_URL_MANUAL:
                    related = related_list[index]
                    heading = i18n('rel_url_at') % (video_type, related['name'])
                    new_url = kodi.get_keyboard(heading, related['url'])
                    if new_url is not None:
                        salts_utils.update_url(video, related['name'], related['url'], new_url)
                        kodi.notify(msg=i18n('rel_url_set') % (related['name']), duration=5000)
                        related['label'] = '[%s] %s' % (related['name'], new_url)
                elif mode == MODES.SET_URL_SEARCH:
                    sru_search(video, related_list[index])
            else:
                break
    finally:
        try: worker_pool.reap_workers(workers, None)
        except UnboundLocalError: pass
    
def sru_search_all(video, related_list):
    blank_list = [related for related in related_list if not related['url']]
    if not blank_list: return related_list
    
    temp_title, temp_year, temp_season = get_search_fields(video.video_type, video.title, video.year, video.season)
    timeout = max_timeout = int(kodi.get_setting('source_timeout'))
    if max_timeout == 0: timeout = None
    begin = time.time()
    with kodi.ProgressDialog(i18n('set_related_url'), utils2.make_progress_msg(video)) as pd:
        try:
            wp = worker_pool.WorkerPool()
            total_scrapers = len(blank_list)
            for i, related in enumerate(blank_list):
                logger.log('Searching for: |%s|%s|%s|%s|' % (related['name'], temp_title, temp_year, temp_season), log_utils.LOGDEBUG)
                wp.request(salts_utils.parallel_search, [related['class'], video.video_type, temp_title, temp_year, temp_season])
                progress = i * 50 / total_scrapers
                pd.update(progress, line2=i18n('req_result') % (related['name']))
    
            fails = set([item['name'] for item in blank_list])
            result_count = 0
            while result_count < total_scrapers:
                try:
                    logger.log('Waiting for Urls - Timeout: %s' % (timeout), log_utils.LOGDEBUG)
                    results = wp.receive(timeout)
                    fails.remove(results['name'])
                    result_count += 1
                    logger.log('Got result: %s' % (results), log_utils.LOGDEBUG)
                    if results['results']:
                        for i, item in enumerate(related_list):
                            if item['name'] == results['name']:
                                first = results['results'][0]
                                salts_utils.update_url(video, item['name'], item['url'], first['url'])
                                item['url'] = first['url']
                                item['label'] = '[%s] %s' % (item['name'], first['url'])
                                
                    progress = (result_count * 50 / total_scrapers) + 50
                    if len(fails) > 5:
                        line3 = i18n('remaining_over') % (len(fails), total_scrapers)
                    else:
                        line3 = i18n('remaining_under') % (', '.join(fails))
                    pd.update(progress, line2=i18n('recv_result') % (results['name']), line3=line3)
                    
                    if max_timeout > 0:
                        timeout = max_timeout - (time.time() - begin)
                        if timeout < 0: timeout = 0
                except worker_pool.Empty:
                    logger.log('Get Url Timeout', log_utils.LOGWARNING)
                    break
            else:
                logger.log('All source results received', log_utils.LOGDEBUG)
        finally:
            workers = wp.close()
    
    salts_utils.record_sru_failures(fails, total_scrapers, related_list)
    worker_pool.reap_workers(workers, None)
    return related_list

def reset_all_urls(video, related_list):
    for related in related_list:
        salts_utils.update_url(video, related['name'], related['url'], '')
    
    try:
        workers, related_list = get_related_urls(video)
        return related_list
    finally:
        try: worker_pool.reap_workers(workers, None)
        except UnboundLocalError: pass

def get_related_urls(video):
    timeout = max_timeout = int(kodi.get_setting('source_timeout'))
    if max_timeout == 0: timeout = None
    begin = time.time()
    with kodi.ProgressDialog(i18n('set_related_url'), utils2.make_progress_msg(video)) as pd:
        try:
            wp = worker_pool.WorkerPool()
            scrapers = salts_utils.relevant_scrapers(video.video_type, order_matters=True)
            related_list = []
            total_scrapers = len(scrapers)
            for i, cls in enumerate(scrapers):
                scraper = cls(max_timeout)
                wp.request(salts_utils.parallel_get_url, [scraper, video])
                related_list.append({'class': scraper, 'url': '', 'name': cls.get_name(), 'label': '[%s]' % (cls.get_name())})
                progress = i * 50 / total_scrapers
                pd.update(progress, line2=i18n('req_result') % (cls.get_name()))
            
            fails = set([item['name'] for item in related_list])
            result_count = 0
            while result_count < total_scrapers:
                try:
                    logger.log('Waiting for Urls - Timeout: %s' % (timeout), log_utils.LOGDEBUG)
                    result = wp.receive(timeout)
                    result_count += 1
                    logger.log('Got result: %s' % (result), log_utils.LOGDEBUG)
                    for i, item in enumerate(related_list):
                        if item['name'] == result['name']:
                            related_list[i] = result
                            fails.remove(result['name'])
                    progress = (result_count * 50 / total_scrapers) + 50
                    if len(fails) > 5:
                        line3 = i18n('remaining_over') % (len(fails), total_scrapers)
                    else:
                        line3 = i18n('remaining_under') % (', '.join(fails))
                    pd.update(progress, line2=i18n('recv_result') % (result['name']), line3=line3)
                    
                    if max_timeout > 0:
                        timeout = max_timeout - (time.time() - begin)
                        if timeout < 0: timeout = 0
                except worker_pool.Empty:
                    logger.log('Get Url Timeout', log_utils.LOGWARNING)
                    break
            else:
                logger.log('All source results received', log_utils.LOGDEBUG)
                            
        finally:
            workers = wp.close()
            
    salts_utils.record_sru_failures(fails, total_scrapers, related_list)
    return workers, related_list
    
def sru_search(video, related):
    temp_title, temp_year, temp_season = video.title, video.year, video.season
    while True:
        dialog = xbmcgui.Dialog()
        choices = [i18n('manual_search'), '[COLOR green]%s[/COLOR]' % (i18n('force_no_match'))]
        try:
            logger.log('Searching for: |%s|%s|%s|' % (temp_title, temp_year, temp_season), log_utils.LOGDEBUG)
            results = related['class'].search(video.video_type, temp_title, temp_year, temp_season)
            choices += ['%s (%s)' % (result['title'], result['year']) if result['year'] else result['title'] for result in results]
            results_index = dialog.select(i18n('select_related'), choices)
            if results_index == 0:
                temp_title, temp_year, temp_season = get_search_fields(video.video_type, temp_title, temp_year, temp_season)
            elif results_index >= 1:
                if results_index == 1:
                    salts_utils.update_url(video, related['name'], related['url'], FORCE_NO_MATCH)
                    related['label'] = '[%s] [COLOR green]%s[/COLOR]' % (related['name'], i18n('force_no_match'))
                else:
                    salts_utils.update_url(video, related['name'], related['url'], results[results_index - 2]['url'])
                    related['label'] = '[%s] %s' % (related['name'], results[results_index - 2]['url'])
                kodi.notify(msg=i18n('rel_url_set') % (related['name']), duration=5000)
                break
            else:
                break
        except NotImplementedError:
            logger.log('%s Scraper does not support searching.' % (related['class'].get_name()), log_utils.LOGDEBUG)
            kodi.notify(msg=i18n('scraper_no_search'), duration=5000)
            break
    
def get_search_fields(video_type, search_title, search_year, search_season):
    text = search_title
    if search_year: text = '%s (%s)' % (text, search_year)
    if video_type == VIDEO_TYPES.SEASON and search_season:
        text += ' Season %s' % (search_season)
    search_text = kodi.get_keyboard(i18n('enter_search'), text)
    if search_text is not None:
        match = re.match('(.*?)\(?(\d{4})\)?', search_text)
        if match:
            search_title, search_year = match.groups()
            search_title = search_title.strip()
        else:
            search_title = search_text
            search_year = ''
        
        match = re.search('Season\s+(\d+)', search_text)
        try: search_season = match.group(1)
        except: search_season = ''
    return search_title, search_year, search_season
    
@url_dispatcher.register(MODES.RATE, ['section', 'id_type', 'show_id'], ['season', 'episode'])
def rate_media(section, id_type, show_id, season='', episode=''):
    # disabled until fixes for rating are made in official addon
    if id_type == 'imdb' and xbmc.getCondVisibility('System.HasAddon(script.trakt)'):
        run = 'RunScript(script.trakt, action=rate, media_type=%s, remoteid=%s'
        if section == SECTIONS.MOVIES:
            run = (run + ')') % ('movie', show_id)
        else:
            if season and episode:
                run = (run + ', season=%s, episode=%s)') % ('episode', show_id, season, episode)
            elif season:
                run = (run + ', season=%s)') % ('season', show_id, season)
            else:
                run = (run + ')') % ('show', show_id)
        xbmc.executebuiltin(run)
    else:
        item = {id_type: show_id}
        while True:
            rating = kodi.get_keyboard(i18n('enter_rating'))
            if rating is not None:
                rating = rating.lower()
                if rating in ['unrate'] + [str(i) for i in range(1, 11)]:
                    break
            else:
                return

        if rating == 'unrate': rating = None
        trakt_api.rate(section, item, rating, season, episode)

@url_dispatcher.register(MODES.EDIT_TVSHOW_ID, ['title'], ['year'])
def edit_tvshow_id(title, year=''):
    tvshow_id = SRT_Scraper().get_tvshow_id(title, year)
    new_id = kodi.get_keyboard(i18n('input_tvshow_id'), tvshow_id)
    if new_id is not None:
        db_connection.set_related_url(VIDEO_TYPES.TVSHOW, title, year, SRT_SOURCE, new_id)

@url_dispatcher.register(MODES.REM_FROM_LIST, ['slug', 'section', 'id_type', 'show_id'])
def remove_from_list(slug, section, id_type, show_id):
    item = {'type': TRAKT_SECTIONS[section][:-1], id_type: show_id}
    remove_many_from_list(section, item, slug)
    kodi.refresh_container()

def remove_many_from_list(section, items, slug):
    if slug == utils.WATCHLIST_SLUG:
        response = trakt_api.remove_from_watchlist(section, items)
    else:
        response = trakt_api.remove_from_list(section, slug, items)
    return response

@url_dispatcher.register(MODES.ADD_TO_COLL, ['mode', 'section', 'id_type', 'show_id'])
@url_dispatcher.register(MODES.REM_FROM_COLL, ['mode', 'section', 'id_type', 'show_id'])
def manage_collection(mode, section, id_type, show_id):
    item = {id_type: show_id}
    if mode == MODES.ADD_TO_COLL:
        trakt_api.add_to_collection(section, item)
        msg = i18n('item_to_collection')
    else:
        trakt_api.remove_from_collection(section, item)
        msg = i18n('item_from_collection')
    kodi.notify(msg=msg)
    kodi.refresh_container()

@url_dispatcher.register(MODES.ADD_TO_LIST, ['section', 'id_type', 'show_id'], ['slug'])
def add_to_list(section, id_type, show_id, slug=None):
    response = add_many_to_list(section, {id_type: show_id}, slug)
    if response is not None:
        kodi.notify(msg=i18n('item_to_list'))

def add_many_to_list(section, items, slug=None):
    if not slug:
        result = utils.choose_list(Trakt_API, kodi.Translations(strings.STRINGS))
        if result:
            slug, _name = result
            
    if slug == utils.WATCHLIST_SLUG:
        response = trakt_api.add_to_watchlist(section, items)
    elif slug:
        response = trakt_api.add_to_list(section, slug, items)
    else:
        response = None
    return response

@url_dispatcher.register(MODES.COPY_LIST, ['section', 'slug'], ['username', 'target_slug'])
def copy_list(section, slug, username=None, target_slug=None):
    if slug == COLLECTION_SLUG:
        items = trakt_api.get_collection(section)
    else:
        items = trakt_api.show_list(slug, section, username)
    copy_items = []
    for item in items:
        query = utils2.show_id(item)
        copy_item = {'type': TRAKT_SECTIONS[section][:-1], query['id_type']: query['show_id']}
        copy_items.append(copy_item)
    response = add_many_to_list(section, copy_items, target_slug)
    if response:
        added = sum(response['added'].values())
        exists = sum(response['existing'].values())
        not_found = sum([len(item) for item in response['not_found'].values()])
        kodi.notify(msg=i18n('list_copied') % (added, exists, not_found), duration=5000)

@url_dispatcher.register(MODES.TOGGLE_TITLE, ['trakt_id'])
def toggle_title(trakt_id):
    trakt_id = str(trakt_id)
    filter_list = utils2.get_force_title_list()
    if trakt_id in filter_list:
        del filter_list[filter_list.index(trakt_id)]
    else:
        filter_list.append(trakt_id)
    filter_str = '|'.join(filter_list)
    kodi.set_setting('force_title_match', filter_str)
    kodi.refresh_container()

@url_dispatcher.register(MODES.MANAGE_PROGRESS, ['action', 'trakt_id'])
def manage_progress_cache(action, trakt_id):
    trakt_id = str(trakt_id)
    filter_list = utils2.get_progress_skip_list()
    force_list = utils2.get_force_progress_list()
    filtered = trakt_id in filter_list
    forced = trakt_id in force_list
    
    if action == ACTIONS.REMOVE and filtered:
        del filter_list[filter_list.index(trakt_id)]
        force_list.append(trakt_id)
    elif action == ACTIONS.ADD and not filtered and not forced:
        filter_list.append(trakt_id)

    filter_str = '|'.join(filter_list)
    kodi.set_setting('progress_skip_cache', filter_str)
    force_str = '|'.join(force_list)
    kodi.set_setting('force_include_progress', force_str)
    if action == ACTIONS.REMOVE:
        kodi.refresh_container()

@url_dispatcher.register(MODES.TOGGLE_WATCHED, ['section', 'id_type', 'show_id'], ['watched', 'season', 'episode'])
def toggle_watched(section, id_type, show_id, watched=True, season='', episode=''):
    logger.log('In Watched: |%s|%s|%s|%s|%s|%s|' % (section, id_type, show_id, season, episode, watched), log_utils.LOGDEBUG)
    item = {id_type: show_id}
    trakt_api.set_watched(section, item, season, episode, watched)
    w_str = i18n('watched') if watched else i18n('unwatched')
    kodi.notify(msg=i18n('marked_as') % (w_str), duration=5000)
    kodi.refresh_container()

@url_dispatcher.register(MODES.URL_EXISTS, ['trakt_id'])
def toggle_url_exists(trakt_id):
    trakt_id = str(trakt_id)
    show_str = kodi.get_setting('exists_list')
    if show_str:
        show_list = show_str.split('|')
    else:
        show_list = []

    if trakt_id in show_list:
        show_list.remove(trakt_id)
    else:
        show_list.append(trakt_id)

    show_str = '|'.join(show_list)
    kodi.set_setting('exists_list', show_str)
    kodi.refresh_container()

@url_dispatcher.register(MODES.UPDATE_SUBS)
def update_subscriptions():
    logger.log('Updating Subscriptions', log_utils.LOGDEBUG)
    active = kodi.get_setting(MODES.UPDATE_SUBS + '-notify') == 'true'
    with kodi.ProgressDialog(kodi.get_name(), line1=i18n('updating_subscriptions'), background=True, active=active) as pd:
        update_strms(SECTIONS.TV, pd)
        if kodi.get_setting('include_movies') == 'true':
            update_strms(SECTIONS.MOVIES, pd)
        if kodi.get_setting('library-update') == 'true':
            xbmc.executebuiltin('UpdateLibrary(video)')
        if kodi.get_setting('cleanup-subscriptions') == 'true':
            clean_subs()
    
        now = datetime.datetime.now()
        db_connection.set_setting('%s-last_run' % MODES.UPDATE_SUBS, now.strftime("%Y-%m-%d %H:%M:%S.%f"))
    
        if active and kodi.get_setting('auto-' + MODES.UPDATE_SUBS) == 'true':
            kodi.notify(msg=i18n('next_update') % (float(kodi.get_setting(MODES.UPDATE_SUBS + '-interval'))), duration=5000)
    kodi.refresh_container()

def update_strms(section, dialog=None):
    section_params = utils2.get_section_params(section)
    slug = kodi.get_setting('%s_sub_slug' % (section))
    if not slug:
        return
    elif slug == utils.WATCHLIST_SLUG:
        items = trakt_api.show_watchlist(section)
    else:
        items = trakt_api.show_list(slug, section)

    length = len(items)
    for i, item in enumerate(items):
        percent_progress = (i + 1) * 100 / length
        title = re.sub('\s+\(\d{4}\)$', '', item['title'])
            
        dialog.update(percent_progress, '%s %s: %s (%s)' % (i18n('updating'), section, title, item['year']))
        try:
            add_to_library(section_params['video_type'], item['title'], item['year'], item['ids']['trakt'])
        except Exception as e:
            logger.log('Subscription Update Exception: |%s|%s|%s|%s| - %s' % (section_params['video_type'], item['title'], item['year'], item['ids']['trakt'], e), log_utils.LOGDEBUG)

@url_dispatcher.register(MODES.CLEAN_SUBS)
def clean_subs():
    slug = kodi.get_setting('TV_sub_slug')
    if not slug:
        return
    elif slug == utils.WATCHLIST_SLUG:
        items = trakt_api.show_watchlist(SECTIONS.TV)
    else:
        items = trakt_api.show_list(slug, SECTIONS.TV)

    del_items = []
    for item in items:
        show = trakt_api.get_show_details(item['ids']['trakt'])
        if show['status'].upper() in ['ENDED', 'CANCELED', 'CANCELLED']:
            show_id = utils2.show_id(item)
            del_items.append({show_id['id_type']: show_id['show_id']})

    if del_items:
        if slug == utils.WATCHLIST_SLUG:
            trakt_api.remove_from_watchlist(SECTIONS.TV, del_items)
        else:
            trakt_api.remove_from_list(SECTIONS.TV, slug, del_items)

@url_dispatcher.register(MODES.REFRESH_IMAGES, ['video_type', 'ids'], ['season', 'episode'])
def refresh_images(video_type, ids, season='', episode=''):
    ids = json.loads(ids)
    images = image_scraper.get_images(video_type, ids, season, episode)
    salts_utils.clear_thumbnails(images)
    image_scraper.clear_cache(video_type, ids, season, episode)
    
    image_scraper.get_images(video_type, ids, season, episode, cached=False)
    kodi.refresh_container()

@url_dispatcher.register(MODES.FLUSH_CACHE)
def flush_cache():
    dlg = xbmcgui.Dialog()
    ln1 = i18n('flush_cache_line1')
    ln2 = i18n('flush_cache_line2')
    ln3 = ''
    yes = i18n('keep')
    no = i18n('delete')
    if dlg.yesno(i18n('flush_web_cache'), ln1, ln2, ln3, yes, no):
        with kodi.WorkingDialog() as wd:
            start = None
            while not xbmc.abortRequested:
                days_left = db_connection.prune_cache(prune_age=0)
                if start is None: start = days_left
                if days_left:
                    wd.update(100 * (start - days_left) / start)
                else:
                    # call flush_cache at the end to trigger vacuum for SQLITE
                    wd.update(100)
                    db_connection.flush_cache()
                    break
            
        kodi.refresh_container()

@url_dispatcher.register(MODES.FLUSH_IMAGES)
def flush_image_cache():
    dlg = xbmcgui.Dialog()
    ln1 = i18n('flush_image_line1')
    ln2 = i18n('flush_image_line2')
    ln3 = ''
    yes = i18n('keep')
    no = i18n('delete')
    if dlg.yesno(i18n('flush_image_cache'), ln1, ln2, ln3, yes, no):
        with kodi.WorkingDialog():
            db_connection.flush_image_cache()
            kodi.notify(msg=i18n('flush_complete'))

@url_dispatcher.register(MODES.PRUNE_CACHE)
def prune_cache():
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        if xbmc.getInfoLabel('Container.PluginName') != kodi.get_id():
            if not db_connection.prune_cache():
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                db_connection.set_setting('%s-last_run' % (MODES.PRUNE_CACHE), now)
                logger.log('Prune Completed Successfully @ %s' % (now), log_utils.LOGDEBUG)
                break
        else:
            logger.log('SALTS Active... Busy... Postponing [%s]' % (MODES.PRUNE_CACHE), log_utils.LOGDEBUG)
            if monitor.waitForAbort(30000):
                break

@url_dispatcher.register(MODES.RESET_DB)
def reset_db():
    if db_connection.reset_db():
        message = i18n('db_reset_success')
    else:
        message = i18n('db_on_sqlite')
    kodi.notify(msg=message)

@url_dispatcher.register(MODES.EXPORT_DB)
def export_db():
    try:
        dialog = xbmcgui.Dialog()
        export_path = dialog.browse(0, i18n('select_export_dir'), 'files').encode('utf-8')
        if export_path:
            export_path = kodi.translate_path(export_path)
            export_filename = kodi.get_keyboard(i18n('enter_export_name'), 'export.csv')
            if export_filename is not None:
                export_file = export_path + export_filename
                db_connection.export_from_db(export_file)
                kodi.notify(header=i18n('export_successful'), msg=i18n('exported_to') % (export_file), duration=5000)
    except Exception as e:
        logger.log('Export Failed: %s' % (e), log_utils.LOGERROR)
        kodi.notify(header=i18n('export'), msg=i18n('export_failed'))

@url_dispatcher.register(MODES.IMPORT_DB)
def import_db():
    try:
        dialog = xbmcgui.Dialog()
        import_file = dialog.browse(1, i18n('select_import_file'), 'files').encode('utf-8')
        if import_file:
            import_file = kodi.translate_path(import_file)
            db_connection.import_into_db(import_file)
            kodi.notify(header=i18n('import_success'), msg=i18n('imported_from') % (import_file))
    except Exception as e:
        logger.log('Import Failed: %s' % (e), log_utils.LOGERROR)
        kodi.notify(header=i18n('import'), msg=i18n('import_failed'))

@url_dispatcher.register(MODES.ADD_TO_LIBRARY, ['video_type', 'title', 'year', 'trakt_id'])
def man_add_to_library(video_type, title, year, trakt_id):
    try:
        if video_type == VIDEO_TYPES.MOVIE and year:
            msg = '%s (%s)' % (title, year)
        else:
            msg = title
        add_to_library(video_type, title, year, trakt_id)
    except Exception as e:
        kodi.notify(msg=i18n('not_added_to_lib') % (msg, e), duration=5000)
        return
    
    kodi.notify(msg=i18n('added_to_lib') % (msg), duration=5000)

def add_to_library(video_type, title, year, trakt_id):
    logger.log('Creating .strm for |%s|%s|%s|%s|' % (video_type, title, year, trakt_id), log_utils.LOGDEBUG)
    scraper = local_scraper.Scraper()
    exclude_local = kodi.get_setting('exclude_local') == 'true'
    create_nfo = int(kodi.get_setting('create_nfo'))  # 0 = None | 1 = Won't scrape | 2 = All

    if video_type == VIDEO_TYPES.TVSHOW:
        save_path = kodi.get_setting('tvshow-folder')
        save_path = kodi.translate_path(save_path)
        show = trakt_api.get_show_details(trakt_id)
        show['title'] = re.sub(' \(\d{4}\)$', '', show['title'])  # strip off year if it's part of show title
        seasons = trakt_api.get_seasons(trakt_id)
        include_unknown = kodi.get_setting('include_unknown') == 'true'

        if not seasons:
            logger.log('No Seasons found for %s (%s)' % (show['title'], show['year']), log_utils.LOGERROR)
        else:
            if create_nfo > 0:
                show_path = make_path(save_path, video_type, show['title'], show['year'])
                if ((create_nfo == 1) and (show['title'] not in show_path)) or create_nfo == 2:
                    write_nfo(show_path, video_type, show['ids'])

        for season in seasons:
            season_num = season['number']
            if kodi.get_setting('include_specials') == 'true' or season_num != 0:
                episodes = trakt_api.get_episodes(trakt_id, season_num)
                for episode in episodes:
                    ep_num = episode['number']
                    air_date = utils2.make_air_date(episode['first_aired'])
                    if exclude_local:
                        ep_url = scraper.get_url(ScraperVideo(VIDEO_TYPES.EPISODE, title, year, trakt_id, season_num, ep_num, episode['title'], air_date))
                        if ep_url and ep_url != FORCE_NO_MATCH:
                            continue
                    
                    if utils2.show_requires_source(trakt_id):
                        require_source = True
                    else:
                        if (episode['first_aired'] is not None and utils.iso_2_utc(episode['first_aired']) <= time.time()) or (include_unknown and episode['first_aired'] is None):
                            require_source = False
                        else:
                            continue

                    filename = utils2.filename_from_title(show['title'], video_type) + '.strm'
                    filename = filename % ('%02d' % int(season_num), '%02d' % int(ep_num))
                    final_path = os.path.join(make_path(save_path, video_type, show['title'], show['year'], season=season_num), filename)
                    strm_string = kodi.get_plugin_url({'mode': MODES.GET_SOURCES, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': year, 'season': season_num,
                                                       'episode': ep_num, 'trakt_id': trakt_id, 'ep_title': episode['title'], 'ep_airdate': air_date})
                    write_strm(strm_string, final_path, VIDEO_TYPES.EPISODE, show['title'], show['year'], trakt_id, season_num, ep_num, require_source=require_source)

    elif video_type == VIDEO_TYPES.MOVIE:
        if exclude_local:
            movie_url = scraper.get_url(ScraperVideo(video_type, title, year, trakt_id))
            if movie_url and movie_url != FORCE_NO_MATCH:
                raise Exception(i18n('local_exists'))
        
        save_path = kodi.get_setting('movie-folder')
        save_path = kodi.translate_path(save_path)
        if create_nfo > 0:
            movie_path = make_path(save_path, video_type, title, year)
            if ((create_nfo == 1) and (title not in movie_path)) or create_nfo == 2:
                movie = trakt_api.get_movie_details(trakt_id)
                write_nfo(movie_path, video_type, movie['ids'])
        strm_string = kodi.get_plugin_url({'mode': MODES.GET_SOURCES, 'video_type': video_type, 'title': title, 'year': year, 'trakt_id': trakt_id})
        filename = utils2.filename_from_title(title, VIDEO_TYPES.MOVIE, year) + '.strm'
        final_path = os.path.join(make_path(save_path, video_type, title, year), filename)
        write_strm(strm_string, final_path, VIDEO_TYPES.MOVIE, title, year, trakt_id, require_source=kodi.get_setting('require_source') == 'true')

def make_path(base_path, video_type, title, year='', season=''):
    show_folder = re.sub(r'[^\w\-_\. ]', '_', title)
    show_folder = '%s (%s)' % (show_folder, year) if year else show_folder
    path = os.path.join(base_path, show_folder)
    if (video_type == VIDEO_TYPES.TVSHOW) and season:
        path = os.path.join(path, 'Season %s' % (season))
    return path

def nfo_url(video_type, ids):
    tvdb_url = 'http://thetvdb.com/?tab=series&id=%s'
    tmdb_url = 'https://www.themoviedb.org/%s/%s'
    imdb_url = 'http://www.imdb.com/title/%s/'

    if 'tvdb' in ids:
        return tvdb_url % (str(ids['tvdb']))
    elif 'tmdb' in ids:
        if video_type == VIDEO_TYPES.TVSHOW:
            media_string = 'tv'
        else:
            media_string = 'movie'
        return tmdb_url % (media_string, str(ids['tmdb']))
    elif 'imdb' in ids:
        return imdb_url % (str(ids['imdb']))
    else:
        return ''

def write_nfo(path, video_type, meta_ids):
    nfo_string = nfo_url(video_type, meta_ids)
    if nfo_string:
        filename = video_type.lower().replace(' ', '') + '.nfo'
        path = os.path.join(path, filename)
        path = xbmc.makeLegalFilename(path)
        if not xbmcvfs.exists(os.path.dirname(path)):
            try:
                try: xbmcvfs.mkdirs(os.path.dirname(path))
                except: os.makedirs(os.path.dirname(path))
            except Exception as e:
                logger.log('Failed to create directory %s: %s' % (path, str(e)), log_utils.LOGERROR)

            old_nfo_string = ''
            try:
                f = xbmcvfs.File(path, 'r')
                old_nfo_string = f.read()
                f.close()
            except: pass

            if nfo_string != old_nfo_string:
                try:
                    logger.log('Writing nfo: %s' % nfo_string, log_utils.LOGDEBUG)
                    file_desc = xbmcvfs.File(path, 'w')
                    file_desc.write(nfo_string)
                    file_desc.close()
                except Exception as e:
                    logger.log('Failed to create .nfo file (%s): %s' % (path, e), log_utils.LOGERROR)

def write_strm(stream, path, video_type, title, year, trakt_id, season='', episode='', require_source=False):
    path = xbmc.makeLegalFilename(path)
    if not xbmcvfs.exists(os.path.dirname(path)):
        try:
            try: xbmcvfs.mkdirs(os.path.dirname(path))
            except: os.makedirs(os.path.dirname(path))
        except Exception as e:
            logger.log('Failed to create directory %s: %s' % (path, str(e)), log_utils.LOGERROR)

    try:
        f = xbmcvfs.File(path, 'r')
        old_strm_string = f.read()
        f.close()
    except:
        old_strm_string = ''

    # print "Old String: %s; New String %s" %(old_strm_string,strm_string)
    # string will be blank if file doesn't exist or is blank
    if stream != old_strm_string:
        try:
            if not require_source or salts_utils.url_exists(ScraperVideo(video_type, title, year, trakt_id, season, episode)):
                logger.log('Writing strm: %s' % stream, log_utils.LOGDEBUG)
                file_desc = xbmcvfs.File(path, 'w')
                file_desc.write(stream)
                file_desc.close()
            else:
                logger.log('No strm written for |%s|%s|%s|%s|%s|' % (video_type, title, year, season, episode), log_utils.LOGWARNING)
        except Exception as e:
            logger.log('Failed to create .strm file (%s): %s' % (path, e), log_utils.LOGERROR)

def show_pickable_list(slug, pick_label, pick_mode, section):
    if not slug:
        kodi.create_item({'mode': pick_mode, 'section': section}, pick_label, is_folder=False, is_playable=False)
        kodi.set_content(CONTENT_TYPES.ADDONS)
        kodi.end_of_directory()
    else:
        show_list(section, slug)

def make_dir_from_list(section, list_data, slug=None, query=None, page=None):
    section_params = utils2.get_section_params(section)
    watched = {}
    in_collection = {}
    if TOKEN:
        for item in trakt_api.get_watched(section):
            if section == SECTIONS.MOVIES:
                watched[item['movie']['ids']['trakt']] = item['plays'] > 0
            else:
                watched[item['show']['ids']['trakt']] = len([e for s in item['seasons'] if s['number'] != 0 for e in s['episodes']])
                
        if slug == COLLECTION_SLUG:
            in_collection = dict.fromkeys([show['ids']['trakt'] for show in list_data], True)
        else:
            collection = trakt_api.get_collection(section, full=False)
            in_collection = dict.fromkeys([show['ids']['trakt'] for show in collection], True)
            
    total_items = len(list_data)
    for show in list_data:
        menu_items = []
        show_id = utils2.show_id(show)
        trakt_id = show['ids']['trakt']
        if slug and slug != COLLECTION_SLUG:
            queries = {'mode': MODES.REM_FROM_LIST, 'slug': slug, 'section': section}
            queries.update(show_id)
            menu_items.append((i18n('remove_from_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

        sub_slug = kodi.get_setting('%s_sub_slug' % (section))
        if TOKEN and sub_slug:
            if sub_slug != slug:
                queries = {'mode': MODES.ADD_TO_LIST, 'section': section_params['section'], 'slug': sub_slug}
                queries.update(show_id)
                menu_items.append((i18n('subscribe'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
            elif section == SECTIONS.TV:
                if utils2.show_requires_source(trakt_id):
                    label = i18n('require_aired_only')
                else:
                    label = i18n('require_page_only')
                queries = {'mode': MODES.URL_EXISTS, 'trakt_id': trakt_id}
                menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

        if section == SECTIONS.MOVIES:
            show['watched'] = watched.get(trakt_id, False)
        else:
            try:
                logger.log('%s/%s: Watched: %s - Aired: %s' % (trakt_id, show['ids']['slug'], watched.get(trakt_id, 'NaN'), show['aired_episodes']), log_utils.LOGDEBUG)
                show['watched'] = watched[trakt_id] >= show['aired_episodes']
                show['watched_count'] = watched[trakt_id]
            except: show['watched'] = False

        show['in_collection'] = in_collection.get(trakt_id, False)

        liz, liz_url = make_item(section_params, show, menu_items)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=section_params['folder'], totalItems=total_items)

    if query and page and total_items >= int(kodi.get_setting('list_size')):
        query['page'] = int(page) + 1
        label = '%s >>' % (i18n('next_page'))
        kodi.create_item(query, label, thumb=utils2.art('nextpage.png'), fanart=utils2.art('fanart.jpg'), is_folder=True)

    kodi.set_view(section_params['content_type'], True)
    kodi.end_of_directory()

def make_dir_from_cal(mode, start_date, days):
    start_date = utils2.to_datetime(start_date, '%Y-%m-%d')
    last_week = start_date - datetime.timedelta(days=7)
    next_week = start_date + datetime.timedelta(days=7)
    last_str = datetime.datetime.strftime(last_week, '%Y-%m-%d')
    next_str = datetime.datetime.strftime(next_week, '%Y-%m-%d')

    label = '<< %s' % (i18n('previous_week'))
    kodi.create_item({'mode': mode, 'start_date': last_str}, label, thumb=utils2.art('previous.png'), fanart=utils2.art('fanart.jpg'), is_folder=True)

    watched = {}
    if TOKEN:
        watched_history = trakt_api.get_watched(SECTIONS.TV)
        for item in watched_history:
            trakt_id = item['show']['ids']['trakt']
            watched[trakt_id] = {}
            for season in item['seasons']:
                watched[trakt_id][season['number']] = {}
                for episode in season['episodes']:
                    watched[trakt_id][season['number']][episode['number']] = True

    totalItems = len(days)
    for item in days:
        episode = item['episode']
        show = item['show']
        utc_secs = utils.iso_2_utc(episode['first_aired'])
        show_date = datetime.date.fromtimestamp(utc_secs)

        try: episode['watched'] = watched[show['ids']['trakt']][episode['season']][episode['number']]
        except: episode['watched'] = False

        if show_date < start_date.date():
            logger.log('Skipping show date |%s| before start: |%s|' % (show_date, start_date.date()), log_utils.LOGDEBUG)
            continue
        elif show_date >= next_week.date():
            logger.log('Stopping because show date |%s| >= end: |%s|' % (show_date, next_week.date()), log_utils.LOGDEBUG)
            break

        date = utils2.make_day(datetime.date.fromtimestamp(utc_secs).isoformat())
        if kodi.get_setting('calendar_time') != '0':
            date_time = '%s@%s' % (date, utils2.make_time(utc_secs, 'calendar_time'))
        else:
            date_time = date

        menu_items = []
        queries = {'mode': MODES.SEASONS, 'trakt_id': show['ids']['trakt'], 'title': show['title'], 'year': show['year'], 'tvdb_id': show['ids']['tvdb']}
        menu_items.append((i18n('browse_seasons'), 'Container.Update(%s)' % (kodi.get_plugin_url(queries))),)

        liz, liz_url = make_episode_item(show, episode, show_subs=False, menu_items=menu_items)
        label = liz.getLabel()
        label = '[[COLOR deeppink]%s[/COLOR]] %s - %s' % (date_time, show['title'], label)
        if episode['season'] == 1 and episode['number'] == 1:
            label = '[COLOR green]%s[/COLOR]' % (label)
        liz.setLabel(label)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, liz, isFolder=False, totalItems=totalItems)

    label = '%s >>' % (i18n('next_week'))
    kodi.create_item({'mode': mode, 'start_date': next_str}, label, thumb=utils2.art('next.png'), fanart=utils2.art('fanart.jpg'), is_folder=True)
    kodi.set_content(CONTENT_TYPES.EPISODES)
    kodi.end_of_directory()

def make_season_item(season, info, trakt_id, title, year, tvdb_id):
    label = '%s %s' % (i18n('season'), season['number'])
    ids = {'trakt': trakt_id, 'tvdb': tvdb_id}
    art = image_scraper.get_images(VIDEO_TYPES.SEASON, ids, season['number'])
    liz = utils.make_list_item(label, season, art)
    logger.log('Season Info: %s' % (info), log_utils.LOGDEBUG)
    info['mediatype'] = 'season'
    liz.setInfo('video', info)
    menu_items = []

    if 'playcount' in info and info['playcount']:
        watched = False
        label = i18n('mark_as_unwatched')
    else:
        watched = True
        label = i18n('mark_as_watched')

    if TOKEN:
        queries = {'mode': MODES.RATE, 'section': SECTIONS.TV, 'season': season['number'], 'id_type': 'trakt', 'show_id': trakt_id}
        menu_items.append((i18n('rate_on_trakt'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        queries = {'mode': MODES.TOGGLE_WATCHED, 'section': SECTIONS.TV, 'season': season['number'], 'id_type': 'trakt', 'show_id': trakt_id, 'watched': watched}
        menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    queries = {'mode': MODES.SET_VIEW, 'content_type': CONTENT_TYPES.SEASONS}
    menu_items.append((i18n('set_as_season_view'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.REFRESH_IMAGES, 'video_type': VIDEO_TYPES.SEASON, 'ids': json.dumps(ids), 'season': season['number']}
    menu_items.append((i18n('refresh_images'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_URL_SEARCH, 'video_type': VIDEO_TYPES.SEASON, 'title': title, 'year': year, 'trakt_id': trakt_id, 'season': season['number']}
    menu_items.append((i18n('set_rel_url_search'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_URL_MANUAL, 'video_type': VIDEO_TYPES.SEASON, 'title': title, 'year': year, 'trakt_id': trakt_id, 'season': season['number']}
    menu_items.append((i18n('set_rel_url_manual'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    liz.addContextMenuItems(menu_items, replaceItems=True)
    return liz

def make_episode_item(show, episode, show_subs=True, menu_items=None):
    # logger.log('Make Episode: Show: %s, Episode: %s, Show Subs: %s' % (show, episode, show_subs), log_utils.LOGDEBUG)
    # logger.log('Make Episode: Episode: %s' % (episode), log_utils.LOGDEBUG)
    if menu_items is None: menu_items = []
    show['title'] = re.sub(' \(\d{4}\)$', '', show['title'])
    if episode['title'] is None:
        label = '%sx%s' % (episode['season'], episode['number'])
    else:
        label = '%sx%s %s' % (episode['season'], episode['number'], episode['title'])

    if 'first_aired' in episode: utc_air_time = utils.iso_2_utc(episode['first_aired'])
    try: time_str = time.asctime(time.localtime(utc_air_time))
    except: time_str = i18n('unavailable')

    logger.log('First Aired: Title: %s S/E: %s/%s fa: %s, utc: %s, local: %s' %
                  (show['title'], episode['season'], episode['number'], episode['first_aired'], utc_air_time, time_str), log_utils.LOGDEBUG)

    if kodi.get_setting('unaired_indicator') == 'true' and (not episode['first_aired'] or utc_air_time > time.time()):
        label = '[I][COLOR chocolate]%s[/COLOR][/I]' % (label)

    if show_subs and utils2.srt_indicators_enabled():
        srt_scraper = SRT_Scraper()
        language = kodi.get_setting('subtitle-lang')
        tvshow_id = srt_scraper.get_tvshow_id(show['title'], show['year'])
        if tvshow_id is not None:
            srts = srt_scraper.get_episode_subtitles(language, tvshow_id, episode['season'], episode['number'])
        else:
            srts = []
        label = utils2.format_episode_label(label, episode['season'], episode['number'], srts)

    meta = salts_utils.make_info(episode, show)
    art = image_scraper.get_images(VIDEO_TYPES.EPISODE, show['ids'], episode['season'], episode['number'])
    liz = utils.make_list_item(label, meta, art)
    liz.setInfo('video', meta)
    air_date = ''
    if episode['first_aired']:
        air_date = utils2.make_air_date(episode['first_aired'])
    queries = {'mode': MODES.GET_SOURCES, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 'episode': episode['number'],
               'ep_title': episode['title'], 'ep_airdate': air_date, 'trakt_id': show['ids']['trakt'], 'random': time.time()}
    liz_url = kodi.get_plugin_url(queries)

    queries = {'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 'episode': episode['number'],
               'ep_title': episode['title'], 'ep_airdate': air_date, 'trakt_id': show['ids']['trakt']}
    if kodi.get_setting('auto-play') == 'true':
        queries['mode'] = MODES.SELECT_SOURCE
        label = i18n('select_source')
        if kodi.get_setting('source-win') == 'Dialog':
            runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % kodi.get_plugin_url(queries)
    else:
        queries['mode'] = MODES.AUTOPLAY
        runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
        label = i18n('auto-play')
    menu_items.insert(0, (label, runstring),)

    if kodi.get_setting('show_download') == 'true':
        queries = {'mode': MODES.DOWNLOAD_SOURCE, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'], 'episode': episode['number'],
                   'ep_title': episode['title'], 'ep_airdate': air_date, 'trakt_id': show['ids']['trakt']}
        if kodi.get_setting('source-win') == 'Dialog':
            runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % kodi.get_plugin_url(queries)
        menu_items.append((i18n('download_source'), runstring),)

    show_id = utils2.show_id(show)
    queries = {'mode': MODES.ADD_TO_LIST, 'section': SECTIONS.TV}
    queries.update(show_id)
    menu_items.append((i18n('add_show_to_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    if episode.get('watched', False):
        watched = False
        label = i18n('mark_as_unwatched')
    else:
        watched = True
        label = i18n('mark_as_watched')

    queries = {'mode': MODES.REFRESH_IMAGES, 'video_type': VIDEO_TYPES.EPISODE, 'ids': json.dumps(show['ids']), 'season': episode['season'], 'episode': episode['number']}
    menu_items.append((i18n('refresh_images'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    if TOKEN:
        show_id = utils2.show_id(show)
        queries = {'mode': MODES.RATE, 'section': SECTIONS.TV, 'season': episode['season'], 'episode': episode['number']}
        # favor imdb_id for ratings to work with official trakt addon
        if show['ids'].get('imdb'):
            queries.update({'id_type': 'imdb', 'show_id': show['ids']['imdb']})
        else:
            queries.update(show_id)
        menu_items.append((i18n('rate_on_trakt'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

        queries = {'mode': MODES.TOGGLE_WATCHED, 'section': SECTIONS.TV, 'season': episode['season'], 'episode': episode['number'], 'watched': watched}
        queries.update(show_id)
        menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    queries = {'mode': MODES.SET_URL_SEARCH, 'video_type': VIDEO_TYPES.TVSHOW, 'title': show['title'], 'year': show['year'], 'trakt_id': show['ids']['trakt']}
    menu_items.append((i18n('set_rel_show_url_search'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_URL_SEARCH, 'video_type': VIDEO_TYPES.SEASON, 'title': show['title'], 'year': show['year'], 'trakt_id': show['ids']['trakt'], 'season': episode['season']}
    menu_items.append((i18n('set_rel_season_url_search'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_URL_MANUAL, 'video_type': VIDEO_TYPES.EPISODE, 'title': show['title'], 'year': show['year'], 'season': episode['season'],
               'episode': episode['number'], 'ep_title': episode['title'], 'ep_airdate': air_date, 'trakt_id': show['ids']['trakt']}
    menu_items.append((i18n('set_rel_url_manual'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    liz.addContextMenuItems(menu_items, replaceItems=True)
    return liz, liz_url

def make_item(section_params, show, menu_items=None):
    if menu_items is None: menu_items = []
    if not isinstance(show['title'], basestring): show['title'] = ''
    show['title'] = re.sub(' \(\d{4}\)$', '', show['title'])
    label = '%s (%s)' % (show['title'], show['year'])
    trakt_id = show['ids']['trakt']
    art = image_scraper.get_images(section_params['video_type'], show['ids'])
    if kodi.get_setting('include_people') == 'true':
        people = trakt_api.get_people(section_params['section'], trakt_id)
        cast = salts_utils.make_cast(show['ids'], people)
    else:
        people = None
        cast = None
        
    liz = utils.make_list_item(label, show, art, cast)
    liz.setProperty('trakt_id', str(trakt_id))
    info = salts_utils.make_info(show, people=people)
    
    # mix-in cast in liz metadata if the setCast method doesn't exist
    if cast and getattr(liz, 'setCast', None) is None:
        info['castandrole'] = info['cast'] = [(person['name'], person['role']) for person in cast]

    if 'TotalEpisodes' in info:
        liz.setProperty('TotalEpisodes', str(info['TotalEpisodes']))
        liz.setProperty('WatchedEpisodes', str(info['WatchedEpisodes']))
        liz.setProperty('UnWatchedEpisodes', str(info['UnWatchedEpisodes']))

    if section_params['section'] == SECTIONS.TV:
        queries = {'mode': section_params['next_mode'], 'trakt_id': trakt_id, 'title': show['title'], 'year': show['year'], 'tvdb_id': show['ids']['tvdb']}
        info['TVShowTitle'] = info['title']
    else:
        queries = {'mode': section_params['next_mode'], 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'trakt_id': trakt_id}
    queries['random'] = time.time()

    liz.setInfo('video', info)
    liz_url = kodi.get_plugin_url(queries)

    queries = {'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'trakt_id': trakt_id}
    if section_params['next_mode'] == MODES.GET_SOURCES:
        if kodi.get_setting('auto-play') == 'true':
            queries['mode'] = MODES.SELECT_SOURCE
            label = i18n('select_source')
            if kodi.get_setting('source-win') == 'Dialog':
                runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
            else:
                runstring = 'Container.Update(%s)' % kodi.get_plugin_url(queries)
        else:
            queries['mode'] = MODES.AUTOPLAY
            runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
            label = i18n('auto-play')
        menu_items.insert(0, (label, runstring),)

    if section_params['next_mode'] == MODES.GET_SOURCES and kodi.get_setting('show_download') == 'true':
        queries = {'mode': MODES.DOWNLOAD_SOURCE, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'trakt_id': trakt_id}
        if kodi.get_setting('source-win') == 'Dialog':
            runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
        else:
            runstring = 'Container.Update(%s)' % kodi.get_plugin_url(queries)
        menu_items.append((i18n('download_source'), runstring),)

    if TOKEN:
        show_id = utils2.show_id(show)
        if show.get('in_collection', False):
            queries = {'mode': MODES.REM_FROM_COLL, 'section': section_params['section']}
            queries.update(show_id)
            menu_items.append((i18n('remove_from_collection'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
        else:
            queries = {'mode': MODES.ADD_TO_COLL, 'section': section_params['section']}
            queries.update(show_id)
            menu_items.append((i18n('add_to_collection'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

        queries = {'mode': MODES.ADD_TO_LIST, 'section': section_params['section']}
        queries.update(show_id)
        menu_items.append((i18n('add_to_list'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

        queries = {'mode': MODES.RATE, 'section': section_params['section']}
        # favor imdb_id for ratings to work with official trakt addon
        if show['ids'].get('imdb'):
            queries.update({'id_type': 'imdb', 'show_id': show['ids']['imdb']})
        else:
            queries.update(show_id)
        menu_items.append((i18n('rate_on_trakt'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    queries = {'mode': MODES.ADD_TO_LIBRARY, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'trakt_id': trakt_id}
    menu_items.append((i18n('add_to_library'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.REFRESH_IMAGES, 'video_type': section_params['video_type'], 'ids': json.dumps(show['ids'])}
    menu_items.append((i18n('refresh_images'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    if TOKEN:
        if show.get('watched', False):
            watched = False
            label = i18n('mark_as_unwatched')
        else:
            watched = True
            label = i18n('mark_as_watched')

        if watched or section_params['section'] == SECTIONS.MOVIES:
            queries = {'mode': MODES.TOGGLE_WATCHED, 'section': section_params['section'], 'watched': watched}
            queries.update(show_id)
            menu_items.append((label, 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    if section_params['section'] == SECTIONS.TV and kodi.get_setting('enable-subtitles') == 'true':
        queries = {'mode': MODES.EDIT_TVSHOW_ID, 'title': show['title'], 'year': show['year']}
        runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
        menu_items.append((i18n('set_addicted_tvshowid'), runstring,))

    if section_params['section'] == SECTIONS.TV:
        if str(trakt_id) in utils2.get_progress_skip_list():
            queries = {'mode': MODES.MANAGE_PROGRESS, 'action': ACTIONS.REMOVE, 'trakt_id': trakt_id}
            runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
            menu_items.append((i18n('include_in_mne'), runstring,))
        else:
            if str(trakt_id) in utils2.get_force_title_list():
                label = i18n('use_def_ep_matching')
            else:
                label = i18n('use_ep_title_match')
            queries = {'mode': MODES.TOGGLE_TITLE, 'trakt_id': trakt_id}
            runstring = 'RunPlugin(%s)' % kodi.get_plugin_url(queries)
            menu_items.append((label, runstring,))

    queries = {'mode': MODES.SET_URL_SEARCH, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'trakt_id': trakt_id}
    menu_items.append((i18n('set_rel_url_search'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)
    queries = {'mode': MODES.SET_URL_MANUAL, 'video_type': section_params['video_type'], 'title': show['title'], 'year': show['year'], 'trakt_id': trakt_id}
    menu_items.append((i18n('set_rel_url_manual'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    if len(menu_items) < 10 and 'trailer' in info:
        queries = {'mode': MODES.PLAY_TRAILER, 'stream_url': info['trailer']}
        menu_items.insert(-3, (i18n('play_trailer'), 'RunPlugin(%s)' % (kodi.get_plugin_url(queries))),)

    liz.addContextMenuItems(menu_items, replaceItems=True)

    liz.setProperty('resumetime', str(0))
    liz.setProperty('totaltime', str(1))
    return liz, liz_url

def get_list(section, slug, username=None, cached=True):
    if slug == utils.WATCHLIST_SLUG:
        items = trakt_api.show_watchlist(section, cached=cached)
    else:
        try:
            items = trakt_api.show_list(slug, section, username, auth=bool(TOKEN), cached=cached)
        except TraktNotFoundError:
            msg = i18n('list_not_exist') % (slug)
            kodi.notify(msg=msg, duration=5000)
            logger.log(msg, log_utils.LOGWARNING)
            return
    
    return items
    
def main(argv=None):
    if sys.argv: argv = sys.argv
    queries = kodi.parse_query(sys.argv[2])
    logger.log('Version: |%s| Queries: |%s|' % (kodi.get_version(), queries), log_utils.LOGNOTICE)
    logger.log('Args: |%s|' % (argv), log_utils.LOGNOTICE)

    # don't process params that don't match our url exactly. (e.g. plugin://plugin.video.1channel/extrafanart)
    plugin_url = 'plugin://%s/' % (kodi.get_id())
    if argv[0] != plugin_url:
        return

    try:
        global db_connection
        db_connection = DB_Connection()
        mode = queries.get('mode', None)
        url_dispatcher.dispatch(mode, queries)
    except (TransientTraktError, TraktError, TraktAuthError) as e:
        logger.log(str(e), log_utils.LOGERROR)
        kodi.notify(msg=str(e), duration=5000)
    except DatabaseRecoveryError as e:
        logger.log('Attempting DB recovery due to Database Error: %s' % (e), log_utils.LOGWARNING)
        db_connection.attempt_db_recovery()

if __name__ == '__main__':
    sys.exit(main())
