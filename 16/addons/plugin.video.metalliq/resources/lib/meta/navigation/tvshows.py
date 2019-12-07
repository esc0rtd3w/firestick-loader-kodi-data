import os
import copy
import time
import urllib
import json
from xbmcswift2 import xbmc, xbmcplugin, xbmcvfs
from meta import plugin, import_tmdb, import_tvdb, LANG
from meta.gui import dialogs
from meta.info import get_tvshow_metadata_tvdb, get_tvshow_metadata_tmdb, get_season_metadata_tvdb, get_episode_metadata_tvdb, get_tvshow_metadata_trakt, get_season_metadata_trakt, get_episode_metadata_trakt
from meta.utils.text import page_redux, parse_year, is_ascii, to_utf8
from meta.utils.executor import execute
from meta.utils.properties import set_property
from meta.utils.rpc import RPC
from meta.library.tvshows import setup_library, add_tvshow_to_library, batch_add_tvshows_to_library, update_library
from meta.library.tools import scan_library
from meta.play.base import active_players, get_players, active_channelers
from meta.play.tvshows import play_episode, play_episode_from_guide, tmdb_play_episode, trakt_play_episode, tvmaze_play_episode
from meta.play.channelers import ADDON_STANDARD, ADDON_PICKER
from meta.play.players import ADDON_DEFAULT, ADDON_SELECTOR
from meta.navigation.base import get_icon_path, get_genre_icon, get_background_path, get_genres, get_tv_genres, caller_name, caller_args
from language import get_string as _
from settings import CACHE_TTL, SETTING_TV_LIBRARY_FOLDER, SETTING_TV_DEFAULT_AUTO_ADD, SETTING_TV_PLAYED_BY_ADD, SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, SETTING_TV_BATCH_ADD_FILE_PATH, SETTING_MOVIES_BATCH_ADD_FILE_PATH, SETTING_FORCE_VIEW, SETTING_MAIN_VIEW, SETTING_TVSHOWS_VIEW, SETTING_SEASONS_VIEW, SETTING_EPISODES_VIEW, SETTING_AIRED_UNKNOWN, SETTING_INCLUDE_SPECIALS

if RPC.settings.get_setting_value(setting="filelists.ignorethewhensorting") == {u'value': True}:
    SORT = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE,  xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT]
    SORTRAKT = [xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE,  xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_DURATION, xbmcplugin.SORT_METHOD_MPAA_RATING, xbmcplugin.SORT_METHOD_UNSORTED]
else:
    SORT = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE, xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT]
    SORTRAKT = [xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE, xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT, xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_DURATION, xbmcplugin.SORT_METHOD_MPAA_RATING, xbmcplugin.SORT_METHOD_UNSORTED]

FORCE = plugin.get_setting(SETTING_FORCE_VIEW, bool)
VIEW_MAIN  = plugin.get_setting(SETTING_MAIN_VIEW, int)
VIEW  = plugin.get_setting(SETTING_TVSHOWS_VIEW, int)
VIEW_TVSHOWS  = plugin.get_setting(SETTING_TVSHOWS_VIEW, int)
VIEW_SEASONS  = plugin.get_setting(SETTING_SEASONS_VIEW, int)
VIEW_EPISODES  = plugin.get_setting(SETTING_EPISODES_VIEW, int)
# 10751|10762|10763|
@plugin.route('/tv')
def tv():
    items = [
        {
            'label': "{0}: {1}".format(_("Search"), _("TV show")),
            'path': plugin.url_for("tv_search"),
            'icon': get_icon_path("search"),
        },
        {
            'label': "{0} ({1})".format(_("Genres"), "TMDb"),
            'path': plugin.url_for("tmdb_tv_genres"),
            'icon': get_icon_path("genres"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_tv_genre_to_library", id="10759|16|35|80|99|18|9648|10764|10765|10766|10767|10768|37", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("On the air", "TMDb"),
            'path': plugin.url_for("tmdb_tv_now_playing", page='1'),
            'icon': get_icon_path("ontheair"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_tv_now_playing_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Popular", "TMDb"),
            'path': plugin.url_for("tmdb_tv_most_popular", page='1'),
            'icon': get_icon_path("popular"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_tv_most_popular_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Top rated", "TMDb"),
            'path': plugin.url_for("tmdb_tv_top_rated", page='1'),
            'icon': get_icon_path("top_rated"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_tv_top_rated_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Most played", "Trakt"),
            'path': plugin.url_for("trakt_tv_played", page='1'),
            'icon': get_icon_path("player"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_played_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Most watched", "Trakt"),
            'path': plugin.url_for("trakt_tv_watched", page='1'),
            'icon': get_icon_path("traktwatchlist"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_watched_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Most collected", "Trakt"),
            'path': plugin.url_for("trakt_tv_collected", page='1'),
            'icon': get_icon_path("traktcollection"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_collected_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Popular", "Trakt"),
            'path': plugin.url_for("tv_trakt_popular", page='1'),
            'icon': get_icon_path("traktrecommendations"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_popular_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Trending", "Trakt"),
            'path': plugin.url_for("trakt_tv_trending", page='1'),
            'icon': get_icon_path("trending"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_trending_to_library", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} {1}".format(_("Use your"), "Trakt"),
            'path': plugin.url_for("trakt_my_tv"),
            'icon': get_icon_path("trakt"),
        }
    ]
    for item in items: item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.finish(items=items, view_mode=VIEW)
    else: return plugin.finish(items=items)

@plugin.route('/tv/trakt/search')
def trakt_tv_search():
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return trakt_tv_search_term(term, 1)
    else: return

@plugin.route('/tv/trakt/search_term/<term>/<page>')
def trakt_tv_search_term(term, page):
    from trakt import trakt
    results, pages = trakt.search_for_tvshow_paginated(term, page)
    return list_trakt_search_items(results, pages, page)

def list_trakt_search_items(results, pages, page):
    from trakt import trakt
    shows = [get_tvshow_metadata_trakt(item["show"], None) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    page = int(page)
    pages = int(pages)
    if pages > 1:
        args = caller_args()
        nextpage = page + 1
        args['page'] = page + 1
        items.append({
            'label': _("Next page").format() + "  >>  (%d/%d)" % (nextpage, pages),
            'path': plugin.url_for(caller_name(), **args),
            'icon': get_icon_path("item_next"),
            'properties' : {'fanart_image' : get_background_path()}})
    if FORCE == True: plugin.finish(items=items, view_mode=VIEW)
    else: return plugin.finish(items=items)

@plugin.route('/tv/trakt/personal')
def trakt_my_tv():
    items = [
        {
            'label': "{0} ({1})".format(_("Library"), "Trakt Collection"),
            'path': plugin.url_for("trakt_tv_collection"),
            'icon': get_icon_path("traktcollection"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_collection_to_library"))
                )
            ],
        },
        {
            'label': "{0} {1} ({2})".format(_("Unwatched"), _("TV shows").lower(), "Trakt watchlist"),
            'path': plugin.url_for("trakt_tv_watchlist"),
            'icon': get_icon_path("traktwatchlist"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_watchlist_to_library"))
                )
            ],
        },
        {
            'label': "{0}{1} ({2})".format(_("Next recording").replace(_("Recording").lower(), ""), _("episodes"), "Trakt Next Episodes"),
            'path': plugin.url_for("trakt_tv_next_episodes"),
            'icon': get_icon_path("traktnextepisodes"),
            'context_menu': [
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_play_random_next_episode"))
                )
            ]
        },
        {
            'label': "{0}{1} ({2})".format(_("Upcoming recordings").replace(_("Recordings").lower(), ""), _("episodes"), "Trakt Calendar"),
            'path': plugin.url_for("trakt_tv_calendar"),
            'icon': get_icon_path("traktcalendar"),
        },
        {
            'label':"{0} ({1})".format(_("Find similar"), "Trakt Recommendations"),
            'path': plugin.url_for("trakt_tv_recommendations"),
            'icon': get_icon_path("traktrecommendations"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_tv_recommendations_to_library"))
                )
            ],
        },
    ]
    for item in items: item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/aired_yesterday/<page>')
def trakt_tv_aired_yesterday(page):
    from trakt import trakt
    result = trakt.trakt_get_aired_yesterday(page)
    return list_aired_episodes(result)

@plugin.route('/tv/trakt/premiered_last_week/<page>')
def trakt_tv_premiered_last_week(page):
    from trakt import trakt
    result = trakt.trakt_get_premiered_last_week(page)
    return list_aired_episodes(result)

def list_aired_episodes(result):
    genres_dict = trakt_get_genres()
    items = []
    count = 1
    if not result:
        return None
    for day in result.iteritems():
        day_nr = 1
        for episode in day[1]:
            banner = episode["show"]["images"]["banner"]["full"]
            fanart = episode["show"]["images"]["fanart"]["full"]
            poster = episode["show"]["images"]["poster"]["full"]
            if episode["episode"]["title"] != None:
                episode_title = (episode["episode"]["title"]).encode('utf-8')
            elif episode["episode"]["title"] == None:
                episode_title = "TBA"
            try: id = episode["show"]["ids"].get("tvdb")
            except: id = episode["show"]["ids"]["tvdb"]
            if not id:
                continue
            season_num = episode["episode"]["season"]
            episode_num = episode["episode"]["number"]
            tvshow_title = (episode["show"]["title"]).encode('utf-8')
            info = get_tvshow_metadata_trakt(episode["show"], genres_dict)
            info['season'] = episode["episode"]["season"] 
            info['episode'] = episode["episode"]["number"]
            info['title'] = episode["episode"]["title"]
            info['aired'] = episode["episode"].get('first_aired','')
            info['premiered'] = episode["episode"].get('first_aired','')
            info['rating'] = episode["episode"].get('rating', '')
            info['plot'] = episode["episode"].get('overview','')
            info['tagline'] = episode["episode"].get('tagline')
            info['votes'] = episode["episode"].get('votes','')
            info['showtitle'] = episode["show"]["title"]
            #info['poster'] = episode['images']['poster']['thumb']
            label = "{0} - S{1:02d}E{2:02d} - {3}".format(tvshow_title, season_num, episode_num, episode_title)
            context_menu = [
                 (
                  "{0} {1}...".format(_("Select"), _("Stream").lower()),
                  "PlayMedia({0})".format(plugin.url_for("tv_play", id=id, season=season_num, episode=episode_num, mode='select'))
                 ),
                 (
                  _("TV show information"),
                  'Action(Info)'
                 ),
                 (
                  _("Add to playlist"),
                  "RunPlugin({0})".format(plugin.url_for("lists_add_episode_to_list", src='tvdb', id=id,
                                                         season=season_num, episode=episode_num))
                 ),
            ]
            items.append({'label': label,
                          'path': plugin.url_for("tv_play", id=id, season=season_num, episode=episode_num, mode='default'),
                          'context_menu': context_menu,
                          'info': info,
                          'is_playable': True,
                          'info_type': 'video',
                          'stream_info': {'video': {}},
                          'thumbnail': info['poster'],
                          'poster': info['poster'],
                          'icon': "DefaultVideo.png",
                          'properties' : {'fanart_image' : info['fanart']},
                          })
            day_nr = day_nr +1
        plugin.set_content('episodes')
        if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
        else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/played/<page>')
def trakt_tv_played(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_played_shows_paginated(page)
    plugin.log.info(results)
    if raw: return results
    else: return list_trakt_tvshows_played_paginated(results, pages, page)

@plugin.route('/tv/trakt/played_to_library/<page>/<confirm>')
def trakt_tv_played_to_library(page, confirm, uncached=False):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Most played", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in trakt_tv_played(i, True) if m not in tv]
        if uncached: tv_add_all_to_library(tv, True)
        else: tv_add_all_to_library(tv)

def list_trakt_tvshows_played_paginated(results, total_items, page):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["show"]["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item["show"], genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    nextpage = int(page) + 1
    pages = int(total_items) // 99 + (int(total_items) % 99 > 0)
    if int(pages) > int(page):
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (nextpage, pages),
            'path': plugin.url_for("trakt_tv_played", page=int(page) + 1),
            'icon': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/watched/<page>')
def trakt_tv_watched(page, raw=False):
    from trakt import trakt
    results, total_items = trakt.trakt_get_watched_shows_paginated(page)
    if raw: return results
    else: return list_trakt_tvshows_watched_paginated(results, total_items, page)

@plugin.route('/tv/trakt/watched_to_library/<page>/<confirm>')
def trakt_tv_watched_to_library(page, confirm, uncached=False):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Most watched", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in trakt_tv_watched(i, True) if m not in tv]
        if uncached: tv_add_all_to_library(tv, True)
        else: tv_add_all_to_library(tv)

def list_trakt_tvshows_watched_paginated(results, total_items, page):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["show"]["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item["show"], genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    nextpage = int(page) + 1
    pages = int(total_items) // 99 + (int(total_items) % 99 > 0)
    if int(pages) > int(page):
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (nextpage, pages),
            'path': plugin.url_for("trakt_tv_watched", page=int(page) + 1),
            'icon': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/collected/<page>')
def trakt_tv_collected(page, raw=False):
    from trakt import trakt
    results, total_items = trakt.trakt_get_collected_shows_paginated(page)
    if raw: return results
    else: return list_trakt_tvshows_watched_paginated(results, total_items, page)

@plugin.route('/tv/trakt/collected_to_library/<page>/<confirm>')
def trakt_tv_collected_to_library(page, confirm, uncached=False):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Most collected", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in trakt_tv_collected(i, True) if m not in tv]
        if uncached: tv_add_all_to_library(tv, True)
        else: tv_add_all_to_library(tv)

def list_trakt_tvshows_collected_paginated(results, total_items, page):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["show"]["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item["show"], genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    nextpage = int(page) + 1
    pages = int(total_items) // 99 + (int(total_items) % 99 > 0)
    if int(pages) > int(page):
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (nextpage, pages),
            'path': plugin.url_for("trakt_tv_collected", page=int(page) + 1),
            'icon': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/popular/<page>')
def tv_trakt_popular(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_popular_shows_paginated(page)
    if raw: return results
    else: return list_trakt_tvshows_popular_paginated(results, pages, page)

@plugin.route('/tv/trakt/popular_to_library/<page>/<confirm>')
def trakt_tv_popular_to_library(page, confirm, uncached=False):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Popular", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in tv_trakt_popular(i, True) if m not in tv]
        if uncached: tv_add_all_to_library([{u'show': m} for m in tv], True)
        else: tv_add_all_to_library([{u'show': m} for m in tv])

def list_trakt_tvshows_popular_paginated(results, pages, page):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item, genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    nextpage = int(page) + 1
    if pages > page:
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (nextpage, pages),
            'path': plugin.url_for("tv_trakt_popular", page=int(page) + 1),
            'icon': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/trending/<page>')
def trakt_tv_trending(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_trending_shows_paginated(page)
    if raw: return results
    else: list_trakt_tvshows_trending_paginated(results, pages, page)

@plugin.route('/tv/trakt/trending_to_library/<page>/<confirm>')
def trakt_tv_trending_to_library(page, confirm, uncached=False):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Trending", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in trakt_tv_trending(i, True) if m not in tv]
        if uncached: tv_add_all_to_library(tv, True)
        else: tv_add_all_to_library(tv)

def list_trakt_tvshows_trending_paginated(results, pages, page):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["show"]["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item["show"], genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    nextpage = int(page) + 1
    if pages > page:
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (nextpage, pages),
            'path': plugin.url_for("trakt_tv_trending", page=int(page) + 1),
            'icon': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/search')
def tv_search():
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return tv_search_term(term, 1)
    else: return

@plugin.route('/tv/search/edit/<term>')
def tv_search_edit(term):
    term = plugin.keyboard(default=term, heading=_("Enter search string"))
    if term != None and term != "": return tv_search_term(term, 1)
    else: return

@plugin.route('/tv/search_term/<term>/<page>')
def tv_search_term(term, page):
    items = [
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("TV shows"), "TMDb"),
            'path': plugin.url_for("tmdb_tv_search_term", term=term, page='1'),
            'icon': get_icon_path("tv"),
            'thumbnail': get_icon_path("tv"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("TV shows"), "Trakt"),
            'path': plugin.url_for("trakt_tv_search_term", term=term, page='1'),
            'icon': get_icon_path("tv"),
            'thumbnail': get_icon_path("tv"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("TV shows"), "TVDb"),
            'path': plugin.url_for("tvdb_tv_search_term", term=term, page='1'),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Albums"), "LastFM"),
            'path': plugin.url_for("music_search_album_term", term=term, page='1'),
            'icon': get_icon_path("music"),
            'thumbnail': get_icon_path("music"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Artists"), "LastFM"),
            'path': plugin.url_for("music_search_artist_term", term=term, page='1'),
            'icon': get_icon_path("music"),
            'thumbnail': get_icon_path("music"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Tracks"), "LastFM"),
            'path': plugin.url_for("music_search_track_term", term=term, page='1'),
            'icon': get_icon_path("music"),
            'thumbnail': get_icon_path("music"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Channels"), "Live addons"),
            'path': plugin.url_for("live_search_term", term=term),
            'icon': get_icon_path("live"),
            'thumbnail': get_icon_path("live"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Playlists"), "Trakt"),
            'path': plugin.url_for("lists_search_for_lists_term", term=term, page='1'),
            'icon': get_icon_path("lists"),
            'thumbnail': get_icon_path("lists"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Movies"), "TMDb"),
            'path': plugin.url_for("tmdb_movies_search_term", term=term, page='1'),
            'icon': get_icon_path("movies"),
            'thumbnail': get_icon_path("movies"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("Movies"), "Trakt"),
            'path': plugin.url_for("trakt_movies_search_term", term=term, page='1'),
            'icon': get_icon_path("movies"),
            'thumbnail': get_icon_path("movies"),
        },
        {
            'label': "{0}: '{1}' - {2} ({3})".format(_("Search"), term, _("TV shows"), plugin.addon.getAddonInfo('name')),
            'path': plugin.url_for("tv_search_term", term=term, page='1'),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
        {
            'label': "{0} {1}".format(_("Edit"), _("Search string").lower()),
            'path': plugin.url_for("tv_search_edit", term=term),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
    ]
    for item in items:
        item['properties'] = {'fanart_image' : get_background_path()}
    return items

@plugin.route('/tv/tmdb/search')
def tmdb_tv_search():
    """ Activate t search """
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return tmdb_tv_search_term(term, 1)
    else: return

@plugin.route('/tv/tmdb/search_term/<term>/<page>')
def tmdb_tv_search_term(term, page):
    """ Perform search of a specified <term>"""
    import_tmdb()
    result = tmdb.Search().tv(query=term, language = LANG, page = page)
    items = list_tvshows(result)
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.cached_route('/tv/tmdb/genres', TTL=CACHE_TTL)
def tmdb_tv_genres():
    """ TV genres list """
    genres = get_tv_genres()
    items = sorted([{'label': name,
                     'icon': get_genre_icon(id),
                     'path': plugin.url_for("tmdb_tv_genre", id=id, page='1'),
                     'context_menu': [(
                                       _("Scan item to library"),
                                       "RunPlugin({0})".format(plugin.url_for("tmdb_tv_genre_to_library", id=id, page='1', confirm="yes"))
                                      )]} for id, name in genres.items()], key=lambda k: k['label'])
    for item in items: item['properties'] = {'fanart_image' : get_background_path()}
    return items

@plugin.cached_route('/tv/genre/<id>/<page>', TTL=CACHE_TTL)
def tmdb_tv_genre(id, page, raw=False):
    """ Shows by genre """
    if FORCE == True: plugin.set_view_mode(VIEW)
    import_tmdb()
    result = tmdb.Discover().tv(with_genres=id, page=page, language=LANG)
    if raw: return result
    else: return list_tvshows(result)

@plugin.route('/tv/genre_to_library/<id>/<page>/<confirm>')
def tmdb_tv_genre_to_library(id, page, confirm):
    genre_names = get_tv_genres()
    if "|" in id:
        genres = id.split("|")
        name = ' + '.join([genre_names.get(int(i), None) for i in genres])
    else:
        genres = [id]
        name = genre_names.get(int(id), None)
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format(name, "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for g in genres:
            for i in pages: tv = tv + [m for m in tmdb_tv_genre(g, i, True)["results"] if m not in tv]
        items["results"] = tv
        tv_add_all_to_library(items)

@plugin.cached_route('/tv/tmdb/now_playing/<page>', TTL=CACHE_TTL)
def tmdb_tv_now_playing(page, raw=False):
    """ On the air shows """
    if FORCE == True: plugin.set_view_mode(VIEW)
    import_tmdb()
    result = tmdb.TV().on_the_air(page=page, language=LANG)
    if raw: return result
    else: return list_tvshows(result)

@plugin.route('/tv/tmdb/now_playing_to_library/<page>/<confirm>')
def tmdb_tv_now_playing_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("On the air", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in tmdb_tv_now_playing(i, True)["results"] if m not in tv]
        items["results"] = tv
        tv_add_all_to_library(items)

@plugin.cached_route('/tv/tmdb/most_popular/<page>', TTL=CACHE_TTL)
def tmdb_tv_most_popular(page, raw=False):
    """ Most popular shows """
    if FORCE == True: plugin.set_view_mode(VIEW)
    import_tmdb()
    result = tmdb.TV().popular(page=page, language=LANG)
    if raw: return result
    else: return list_tvshows(result)

@plugin.route('/tv/tmdb/most_popular_to_library/<page>/<confirm>')
def tmdb_tv_most_popular_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Popular", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in tmdb_tv_most_popular(i, True)["results"] if m not in tv]
        items["results"] = tv 
        tv_add_all_to_library(items)

@plugin.cached_route('/tv/tmdb/top_rated/<page>', TTL=CACHE_TTL)
def tmdb_tv_top_rated(page, raw=False):
    """ Top rated shows """
    if FORCE == True: plugin.set_view_mode(VIEW)
    import_tmdb()
    result = tmdb.TV().top_rated(page=page, language=LANG)
    if raw: return result
    else: return list_tvshows(result)

@plugin.route('/tv/tmdb/top_rated_to_library/<page>/<confirm>')
def tmdb_tv_top_rated_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Top rated", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        tv = []
        for i in pages: tv = tv + [m for m in tmdb_tv_top_rated(i, True)["results"] if m not in tv]
        items["results"] = tv 
        tv_add_all_to_library(items)


@plugin.route('/tv/tvdb/search')
def tvdb_tv_search():
    """ Activate tv search """
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return tvdb_tv_search_term(term, 1)
    else: return

@plugin.route('/tv/tvdb/search_term/<term>/<page>')
def tvdb_tv_search_term(term, page):
    """ Perform search of a specified <term>"""
    if FORCE == True: plugin.set_view_mode(VIEW)
    import_tvdb()
    search_results = tvdb.search(term, language=LANG)
    items = []
    load_full_tvshow = lambda tvshow : tvdb.get_show(tvshow['id'], full=True)
    for tvdb_show in execute(load_full_tvshow, search_results, workers=10):
        info = build_tvshow_info(tvdb_show)
        items.append(make_tvshow_item(info))
    return items

@plugin.route('/tv/trakt/personal/collection')
def trakt_tv_collection():
    from trakt import trakt
    result = trakt.trakt_get_collection("shows")
    items = list_trakt_tvshows(result)
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/personal/watchlist')
def trakt_tv_watchlist():
    from trakt import trakt
    result = trakt.trakt_get_watchlist("shows")
    items = list_trakt_tvshows(result)
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/tv/trakt/personal/next_episodes')
def trakt_tv_next_episodes(raw=False):
    from trakt import trakt
    list = []
    result = trakt.trakt_get_next_episodes()
    for episode in result:
        trakt_id = episode["show"]["ids"]["trakt"]
        episode_info = trakt.get_episode(trakt_id, episode["season"], episode["number"])
        first_aired_string = episode_info["first_aired"]
        episode["first_aired"] = first_aired_string
        if int(first_aired_string[:4]) < 1970:
            list.append(episode)
        elif first_aired_string:
            first_aired = time.mktime(time.strptime(first_aired_string[:19], "%Y-%m-%dT%H:%M:%S"))
            if first_aired < time.time():
                list.append(episode)
    if raw: return list
    else: items = list_trakt_episodes(list, with_time=True)

@plugin.route('/tv/trakt/personal/random_next_episode')
def trakt_tv_play_random_next_episode():
    from meta.utils.playrandom import trakt_play_random
    episodes = trakt_tv_next_episodes(raw=True)
    for episode in episodes:
        episode["type"] = "episode"
    trakt_play_random(episodes)

@plugin.route('/tv/trakt/personal/calendar')
def trakt_tv_calendar(raw=False):
    from trakt import trakt
    result = trakt.trakt_get_calendar()
    if raw: return result
    else: items = list_trakt_episodes(result, with_time=True)

@plugin.route('/tv/trakt/personal/recommendations')
def trakt_tv_recommendations():
    from trakt import trakt
    genres_dict = trakt.trakt_get_genres("tv")
    shows = trakt.get_recommendations("shows")
    items = []
    for show in shows:
        items.append(make_tvshow_item(get_tvshow_metadata_trakt(show, genres_dict)))
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

def get_tvdb_id_from_name(name, lang):
    import_tvdb()
    search_results = tvdb.search(name, language=lang)
    if not search_results:
        dialogs.ok(_("%s not found") % _("TV show"), "{0} {1} in tvdb".format(_("no show information found for"), to_utf8(name)))
        return
    items = []
    for show in search_results:
        if "firstaired" in show:
            show["year"] = int(show['firstaired'].split("-")[0].strip())
        else:
            show["year"] = 0
        items.append(show)
    if len(items) > 1:
        selection = dialogs.select(_("Choose Show"), ["{0} ({1})".format(
            to_utf8(s["seriesname"]), s["year"]) for s in items])
    else:
        selection = 0
    if selection != -1:
        return items[selection]["id"]

def get_tvdb_id_from_imdb_id(imdb_id):
    import_tvdb()
    tvdb_id = tvdb.search_by_imdb(imdb_id)
    if not tvdb_id:
        dialogs.ok(_("%s not found") % _("TV show"), "{0} {1} in tvdb".format(_("no show information found for"), imdb_id))
        return
    return tvdb_id

@plugin.route('/tv/trakt/personal/collection_to_library')
def trakt_tv_collection_to_library(preaprove=False, uncached=False):
    from trakt import trakt
    if preaprove or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}".format(_("Add %s") % ("'{0} {1} {2}'".format("Trakt", _("TV"), _("Collection").lower())),_("Are you sure?"))):
        if uncached: tv_add_all_to_library(trakt.trakt_get_collection_uncached("shows"), True)
        else: tv_add_all_to_library(trakt.trakt_get_collection("shows"))

@plugin.route('/tv/trakt/personal/watchlist_to_library')
def trakt_tv_watchlist_to_library(preaprove=False, uncached=False):
    from trakt import trakt
    if preaprove or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}".format(_("Add %s") % ("'{0} {1} {2}'".format("Trakt", _("TV"), _("Watchlist").lower())),_("Are you sure?"))):
        if uncached: tv_add_all_to_library(trakt.trakt_get_watchlist_uncached("shows"), True)
        else: tv_add_all_to_library(trakt.trakt_get_watchlist("shows"))

@plugin.route('/tv/trakt/personal/recommendations_to_library')
def trakt_tv_recommendations_to_library():
    from trakt import trakt
    if dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}".format(_("Add %s") % ("'{0} {1} {2}'".format("Trakt", _("TV"), _("Recommendations").lower())),_("Are you sure?"))):
        if uncached: tv_add_all_to_library(trakt.get_recommendations("shows"), True)
        else: tv_add_all_to_library(trakt.get_recommendations("shows"))

@plugin.route('/tv/trakt/updated/<page>')
def tv_trakt_updated(page):
    from trakt import trakt
    results, pages = trakt.trakt_updated_shows(page)
    return list_trakt_tvshows_trending_paginated(results, pages, page)

def list_trakt_tvshows_updated_paginated(results, pages, page):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["show"]["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item["show"], genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    nextpage = int(page) + 1
    if pages > page:
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (nextpage, pages),
            'path': plugin.url_for("tv_trakt_updated", page=int(page) + 1),
            'icon': get_icon_path("item_next"),
        })
    if FORCE == True: plugin.set_view_mode(VIEW); return items
    else: return items

@plugin.route('/tv/play_by_name/<name>/<season>/<episode>/<lang>/<mode>', options = {"lang": "en", "mode": "context"})
def tv_play_by_name(name, season, episode, lang, mode):
    """ Activate tv search """
    tvdb_id = get_tvdb_id_from_name(name, lang)
    if tvdb_id:
        tv_play(tvdb_id, season, episode, mode)
        if plugin.get_setting(SETTING_TV_PLAYED_BY_ADD, bool) == True:
            tv_add_to_library(tvdb_id)

@plugin.route('/tv/play_by_source/<source>/<id>/<season>/<episode>/<mode>')
def tv_play_by_source(source, id, season, episode, mode):
    if source == "tmdb": tmdb_play_episode(id, season, episode, mode)
    elif source == "trakt": trakt_play_episode(id, season, episode, mode)
    elif source == "tvmaze": tvmaze_play_episode(id, season, episode, mode)
    else: play_episode(id, season, episode, mode)

@plugin.route('/tv/play_by_name_guide/<name>/<season>/<episode>/<lang>', options = {"lang": "en"})
def guide_tv_play_by_name(name, season, episode, lang):
    """ Activate tv search """
    tvdb_id = get_tvdb_id_from_name(name, lang)
    if tvdb_id:
        guide_tv_play(tvdb_id, season, episode, "default")
        if plugin.get_setting(SETTING_TV_PLAYED_BY_ADD, bool) == True:
            tv_add_to_library(tvdb_id)

@plugin.route('/tv/play_by_name_only/<name>/<lang>', options = {"lang": "en"})
def tv_play_by_name_only(name, lang):
    tvdb_id = get_tvdb_id_from_name(name, lang)
    if tvdb_id:
        season = None
        episode = None
        show = tv_tvshow(tvdb_id)
        while season is None or episode is None:  # don't exit completely if pressing back from episode selector
            selection = dialogs.select(_("Choose season"), [item["label"] for item in show])
            if selection != -1:
                season = show[selection]["info"]["season"]
                season = int(season)
            else:
                return
            items = []
            episodes = tv_season(tvdb_id, season)
            for item in episodes:
                label = "S{0}E{1} - {2}".format(item["info"]["season"], item["info"]["episode"],
                                                to_utf8(item["info"]["title"]))
                if item["info"]["plot"] is not None:
                    label += " - {0}".format(to_utf8(item["info"]["plot"]))
                items.append(label)
            selection = dialogs.select(_("Choose episode"), items)
            if selection != -1:
                episode = episodes[selection]["info"]["episode"]
                episode = int(episode)
                tv_play(tvdb_id, season, episode, "context")
                if plugin.get_setting(SETTING_TV_PLAYED_BY_ADD, bool) == True:
                    tv_add_to_library(tvdb_id)

@plugin.route('/tv/play_by_name_only_guide/<name>/<lang>', options = {"lang": "en"})
def guide_tv_play_by_name_only(name, lang):
    tvdb_id = get_tvdb_id_from_name(name, lang)
    if tvdb_id:
        season = None
        episode = None
        show = tv_tvshow(tvdb_id)
        while season is None or episode is None:
            selection = dialogs.select(_("Choose season"), [item["label"] for item in show])
            if selection != -1:
                season = show[selection]["info"]["season"]
                season = int(season)
            else:
                return
            items = []
            episodes = tv_season(tvdb_id, season)
            for item in episodes:
                label = "S{0}E{1} - {2}".format(item["info"]["season"], item["info"]["episode"],
                                                to_utf8(item["info"]["title"]))
                if item["info"]["plot"] is not None:
                    label += " - {0}".format(to_utf8(item["info"]["plot"]))
                items.append(label)
            selection = dialogs.select(_("Choose episode"), items)
            if selection != -1:
                episode = episodes[selection]["info"]["episode"]
                episode = int(episode)
                guide_tv_play(tvdb_id, season, episode, "default")
                if plugin.get_setting(SETTING_TV_PLAYED_BY_ADD, bool) == True:
                    tv_add_to_library(tvdb_id)

@plugin.route('/tv/play_latest/<id>/<mode>', options = {"mode": "default"})
def tv_play_latest_episode(id, mode):
    from trakt import trakt
    episode = trakt.get_latest_episode(id)
    show = trakt.get_show(id)
    if show['ids']['tvdb']: tv_play(show['ids']['tvdb'], episode['season'], episode['number'], mode)
    elif show['ids']['tmdb']: tv_play_by_source("tmdb", show['ids']['tmdb'], episode['season'], episode['season'], mode)
    elif show['ids']['trakt']: tv_play_by_source("trakt", show['ids']['tmdb'], episode['season'], episode['season'], mode)
    else: dialogs.notify(msg='No tvdb/tmdb/trakt-id', title='Available', delay=3000, image=get_icon_path("tv"))

@plugin.route('/tv/guide_play_latest/<id>')
def guide_tv_play_latest_episode(id):
    from trakt import trakt
    episode = trakt.get_latest_episode(id)
    show = trakt.get_show(id)
    if show['ids']['tvdb']:
        dialogs.notify(msg='%s' % show['title'], title='S%sE%s - %s' % (episode['season'], episode['number'], episode['title']), delay=5000, image=get_icon_path("tv"))
        tv_play(show['ids']['tvdb'], episode['season'], episode['number'], "default")
    else: dialogs.notify(msg='No tvdb id', title='Available', delay=3000, image=get_icon_path("tv"))

@plugin.route('/tv/tvdb/<id>')
def tv_tvshow(id):
    """ All seasons of a TV show """
    plugin.set_content('seasons')
    if FORCE == True: return plugin.finish(items=list_seasons_tvdb(id), sort_methods=SORT, view_mode=VIEW_SEASONS)
    else: return plugin.finish(items=list_seasons_tvdb(id), sort_methods=SORT)


@plugin.route('/tv/tvdb/<id>/<season_num>')
def tv_season(id, season_num):
    """ All episodes of a TV season """
    plugin.set_content('episodes')
    if FORCE == True: return plugin.finish(items=list_episodes_tvdb(id, season_num), sort_methods=SORT, view_mode=VIEW_EPISODES)
    else: return plugin.finish(items=list_episodes_tvdb(id, season_num), sort_methods=SORT)

def set_library_player(path, players):
    players.insert(0, ADDON_SELECTOR)
    players.insert(0, ADDON_DEFAULT)
    # let the user select one player
    selection = dialogs.select(_("Select default player"), [p.title for p in players])
    if selection == -1:
        return
    # get selected player
    player = players[selection]
    # Create play with file
    player_filepath = os.path.join(path, 'player.info')
    player_file = xbmcvfs.File(player_filepath, 'w')
    content = "{0}".format(player.id)
    player_file.write(content)
    player_file.close()

@plugin.route('/tv/set_library_player/<path>')
def set_tv_library_player(path):
    # get active players
    players = active_players("tvshows")
    set_library_player(path, players)

@plugin.route('/tv/set_live_library_player/<path>')
def set_live_tv_library_player(path):
    # get active players
    players = active_players("live")
    set_library_player(path, players)

def set_live_library_player(path):
    # get active players
    players = active_players("live")
    players.insert(0, ADDON_SELECTOR)
    players.insert(0, ADDON_DEFAULT)
    # let the user select one player
    selection = dialogs.select(_("Select default player"), [p.title for p in players])
    if selection == -1:
        return
    # get selected player
    player = players[selection]
    # Create play with file
    player_filepath = os.path.join(path, 'player.info')
    player_file = xbmcvfs.File(player_filepath, 'w')
    content = "{0}".format(player.id)
    player_file.write(content)
    player_file.close()

def tv_add_all_to_library(items, noscan = False):
    library_folder = setup_library(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))
    ids = ""
    import_tvdb()
    if "results" in items: ids = '\n'.join([str(show["id"]) for show, item in execute(tmdb_to_tvdb, items["results"], workers=10)])
    else: ids = '\n'.join([str(i["show"]["ids"]["tvdb"]) if i["show"]["ids"]["tvdb"] != None and i["show"]["ids"]["tvdb"] != "" else i["show"]["ids"]["imdb"] for i in items])
    shows_batch_add_file = plugin.get_setting(SETTING_TV_BATCH_ADD_FILE_PATH, unicode)
    if xbmcvfs.exists(shows_batch_add_file):
        batch_add_file = xbmcvfs.File(shows_batch_add_file)
        pre_ids = batch_add_file.read()
        xids = pre_ids.split("\n")
        for id in xids:
            if id != "" and id != None and id not in ids: ids = ids + str(id) + '\n'
        batch_add_file.close()
        xbmcvfs.delete(shows_batch_add_file)
    batch_add_file = xbmcvfs.File(shows_batch_add_file, 'w')
    batch_add_file.write(str(ids))
    batch_add_file.close()
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/tv/batch_add_to_library)")


@plugin.route('/tv/add_to_library_parsed/<id>/<player>')
def tv_add_to_library_parsed(id, player):
    import_tvdb()
    if id.startswith("tt"):
        try: id = tvdb.search_by_imdb(id)
        except: return dialogs.ok(_("%s not found") % _("TV show"), "{0} {1} in TheTVDb".format(_("no show information found for"), id))
    library_folder = setup_library(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))
    show = tvdb[int(id)]
    imdb = show['imdb_id']
    library_folder = setup_library(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))
    # add to library
    if add_tvshow_to_library(library_folder, show, player): set_property("clean_library", 1)
    scan_library(type="video", path=plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))

@plugin.route('/tv/add_to_library/<id>')
def tv_add_to_library(id):
    import_tvdb()
    library_folder = setup_library(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))
    show = tvdb[int(id)]
    imdb = show['imdb_id']
    # get active players
    players = active_players("tvshows", filters = {'network': show.get('network')})
    # get selected player
    if plugin.get_setting(SETTING_TV_DEFAULT_AUTO_ADD, bool) == True:
        player = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    else:
        players.insert(0, ADDON_SELECTOR)
        players.insert(0, ADDON_DEFAULT)
        selection = dialogs.select(_("Play with..."), [p.title for p in players])
        if selection == -1:
            return
        player = players[selection]
    # setup library folder
    library_folder = setup_library(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))
    # add to library
    if plugin.get_setting(SETTING_TV_DEFAULT_AUTO_ADD, bool) == True:
        if add_tvshow_to_library(library_folder, show, player):
            set_property("clean_library", 1)
    else:
        if add_tvshow_to_library(library_folder, show, player.id):
            set_property("clean_library", 1)
    # start scan
    scan_library(type="video", path=plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))


@plugin.route('/tv/batch_add_to_library')
def tv_batch_add_to_library():
    """ Batch add tv shows to library """
    tv_batch_file = plugin.get_setting(SETTING_TV_BATCH_ADD_FILE_PATH, unicode)
    if xbmcvfs.exists(tv_batch_file):
        try:
            f = open(xbmc.translatePath(tv_batch_file), 'r')
            r = f.read()
            f.close()
            ids = r.split('\n')
        except: return dialogs.notify(msg='TVShows Batch Add File', title=_("%s not found").replace("%s ",""), delay=3000, image=get_icon_path("tv"))
        library_folder = setup_library(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))
        import_tvdb()
        import xbmcgui
        ids_index = 0
        ids_size = len(ids)
        dialogs.notify(msg='Adding ' + str(ids_size) + " items", title="To Kodi library", delay=500, image=get_icon_path("tv"))
        for id in ids:
            items_left = ids_size - ids_index
            if str(items_left).endswith("0"): dialogs.notify(msg=str(items_left), title="Items left", delay=8000, image=get_icon_path("tv"))
            if id == None or id == "None": pass
            elif "," in id:
                csvs = id.split(',')
                for csv in csvs:
                    if csv == None or csv == "None": pass
                    elif str(csv).startswith("tt") and csv != "": tvdb_id = get_tvdb_id_from_imdb_id(csv)
                    else: tvdb_id = csv
                    show = tvdb[int(tvdb_id)]
                    batch_add_tvshows_to_library(library_folder, show)
            else:
                if id == None or id == "None" or id == "": pass
                elif str(id).startswith("tt"): tvdb_id = get_tvdb_id_from_imdb_id(id)
                else: tvdb_id = id
                try:
                    show = tvdb[int(tvdb_id)]
                    batch_add_tvshows_to_library(library_folder, show)
                except: 
                    dialogs.notify(msg='failed to add', title='%s' % id, delay=3000, image=get_icon_path("tv"))
                    xbmc.log("MetalliQ failed to add: {0}".format(id),xbmc.LOGNOTICE)
            ids_index += 1
        if xbmcvfs.exists(tv_batch_file): os.remove(xbmc.translatePath(tv_batch_file))
        dialogs.notify(msg='Starting library scan afterwards', title='Adding tvshow strm-files', delay=5000, image=get_icon_path("tv"))
        update_library()
        return True

@plugin.route('/tv/play/<id>/<season>/<episode>/<mode>')
def tv_play(id, season, episode, mode):
    play_episode(id, season, episode, mode)

@plugin.route('/tv/play_guide/<id>/<season>/<episode>/<mode>')
def guide_tv_play(id, season, episode, mode):  
    play_episode_from_guide(id, season, episode, mode)

def list_tvshows(response):
    if FORCE == True: plugin.set_view_mode(VIEW)
    """ TV shows listing """
    import_tvdb()
    # Attach TVDB data to TMDB results
    items = []
    results = response['results']
    for tvdb_show, tmdb_show in execute(tmdb_to_tvdb, results, workers=10):
        if tvdb_show is not None:
            info = build_tvshow_info(tvdb_show, tmdb_show)
            items.append(make_tvshow_item(info))
    if xbmc.abortRequested:
        return
    # Paging
    if 'page' in response:
        page = response['page']
        args = caller_args()
        if page < response['total_pages']:
            args['page'] = str(page + 1)
            items.append({
                'label': _("Next page").format() + "  >>  (%s/%s)" % (page + 1, response['total_pages']),
                'icon': get_icon_path("item_next"),
                'path': plugin.url_for(caller_name(), **args)
            })
    return items

def trakt_get_genres():
    from trakt import trakt
    genres_dict = dict([(x['slug'], x['name']) for x in trakt.trakt_get_genres("movies")])
    genres_dict.update(dict([(x['slug'], x['name']) for x in trakt.trakt_get_genres("shows")]))
    return genres_dict

def list_trakt_tvshows(results):
    from trakt import trakt
    results = sorted(results,key=lambda item: item["show"]["title"].lower().replace("the ", ""))
    genres_dict = trakt_get_genres()
    shows = [get_tvshow_metadata_trakt(item["show"], genres_dict) for item in results]
    items = [make_tvshow_item(show) for show in shows if show.get('tvdb_id')]
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

def list_trakt_episodes(result, with_time=False):
    genres_dict = trakt_get_genres()
    items = []
    for item in result:
        if 'episode' in item: episode = item['episode']
        else: episode = item
        if "show" in item: show = item['show']
        try: id = episode["show"]["ids"]["tvdb"]
        except: id = episode["ids"].get("tvdb")
        if not id: continue
        try: season_num = episode["season"]
        except: season_num = episode.get("season")
        try: episode_num = episode["number"]
        except: episode_num = episode.get("number")
        if show: tvshow_title = (show.get("title")).encode('utf-8')
        else:
            try: tvshow_title = (episode["show"]["title"]).encode('utf-8')
            except: tvshow_title = str(episode.get("title")).encode('utf-8')
        if episode["title"] != None:
            try: episode_title = (episode["title"]).encode('utf-8')
            except: episode_title = (episode.get("title")).encode('utf-8')
        else: episode_title = "TBA"
        info = get_tvshow_metadata_trakt(item["show"], genres_dict)
        info['season'] = episode["season"] 
        info['episode'] = episode["number"]
        info['title'] = episode["title"]
        info['aired'] = episode.get('first_aired','')
        info['premiered'] = episode.get('first_aired','')
        info['rating'] = episode.get('rating', '')
        info['plot'] = episode.get('overview','')
        info['tagline'] = episode.get('tagline')
        info['votes'] = episode.get('votes','')
        #info['poster'] = episode['images']['poster']['thumb']
        label = "{0} - S{1:02d}E{2:02d} - {3}".format(tvshow_title, season_num, episode_num, episode_title)
        if with_time and info['premiered']:
            airtime = time.strptime(item["first_aired"], "%Y-%m-%dt%H:%M:%S.000Z")
            airtime = time.strftime("%Y-%m-%d %H:%M", airtime)
            label = "{0} - S{1:02d}E{2:02d} - {3}".format(tvshow_title, season_num, episode_num, episode_title)
        context_menu = [
             (
              "{0} {1}...".format(_("Select"), _("Stream").lower()),
              "PlayMedia({0})".format(plugin.url_for("tv_play", id=id, season=season_num, episode=episode_num, mode='select'))
             ),
             (
              "%s %s" % (_("Episode"), _("Information").lower()),
              'Action(Info)'
             ),
             (
              _("Add to playlist"),
              "RunPlugin({0})".format(plugin.url_for("lists_add_episode_to_list", src='tvdb', id=id,
                                                     season=season_num, episode=episode_num))
             ),
        ]
        items.append({'label': label,
                      'path': plugin.url_for("tv_play", id=id, season=season_num, episode=episode_num, mode='default'),
                      'context_menu': context_menu,
                      'info': info,
                      'is_playable': True,
                      'info_type': 'video',
                      'stream_info': {'video': {}},
                      'thumbnail': info['poster'],
                      'poster': info['poster'],
                      'icon': "DefaultVideo.png",
                      'properties' : {'fanart_image' : info['fanart']},
                      })
    plugin.set_content('episodes')
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORTRAKT, view_mode=VIEW, cache_to_disc=False, update_listing=True)
    else: return plugin.finish(items=items, sort_methods=SORTRAKT, cache_to_disc=False, update_listing=True)

def build_tvshow_info(tvdb_show, tmdb_show=None):
    tvdb_info = get_tvshow_metadata_tvdb(tvdb_show)
    tmdb_info = get_tvshow_metadata_tmdb(tmdb_show)
    info = {}
    info.update(tvdb_info)
    info.update(dict((k,v) for k,v in tmdb_info.iteritems() if v))
    # Prefer translated info
    if LANG != "en":
        for key in ('name', 'title', 'plot'):
            if is_ascii(info.get(key,'')) and not is_ascii(tvdb_info.get(key,'')):
                info[key] = tvdb_info[key]
    return info

def make_tvshow_item(info):
    try: tvdb_id = info['tvdb']
    except: tvdb_id = ""
    if tvdb_id == "": 
        try: tvdb_id = info['tvdb_id']
        except: tvdb_id = ""
    try: tmdb_id = info['tmdb']
    except: tmdb_id = ""
    if tmdb_id == "": 
        try: tmdb_id = info['id']
        except: tmdb_id = ""
    try: imdb_id = info['imdb_id']
    except: imdb_id = ""
    if imdb_id == "": 
        try: imdb_id = info['imdb']
        except: imdb_id = ""
    if not info['poster']: info['poster'] = None
    if not info['fanart']: info['fanart'] = None
    if info['poster'] == None or info['poster'] == "":
        if tmdb_id != None and tmdb_id != "":
            import_tmdb()
            show = tmdb.TV(tmdb_id).info()
            if show['poster_path'] != None and show['poster_path'] != "": info['poster'] = u'%s%s' % ("http://image.tmdb.org/t/p/w500", show['poster_path'])
            if info['fanart'] == None or info['fanart'] == "":
                if show['backdrop_path'] != None and show['backdrop_path'] != "": info['fanart'] = u'%s%s' % ("http://image.tmdb.org/t/p/original", show['backdrop_path'])
    if info['poster'] == None or info['poster'] == "":
        if tvdb_id != None and tvdb_id != "":
            import_tvdb()
            show = tvdb.get_show(int(tvdb_id), full=False)
            if show != None:
                if show['seriesname'] != None and show['seriesname'] != "":
                    if show.get('poster', '') != None and show.get('poster', '') != "": info['poster'] = show.get('poster', '')
                    if info['fanart'] == None or info['fanart'] == "":
                        if show.get('fanart', '') != None and show.get('fanart', '') != "": info['fanart'] = show.get('fanart', '')
    if info['poster'] == None or info['poster'] == "":
        if imdb_id != None and imdb_id != "":
            import_tmdb()
            preshow = tmdb.Find(imdb_id).info(external_source="imdb_id")
            proshow = preshow['tv_results']
            if proshow != []: show = proshow[0]
            else: show = []
            if show != []:
                if show['poster_path'] != None and show['poster_path'] != "": info['poster'] = u'%s%s' % ("http://image.tmdb.org/t/p/w500", show['poster_path'])
                if info['fanart'] == None or info['fanart'] == "":
                    if show['backdrop_path'] != None and show['backdrop_path'] != "": info['fanart'] = u'%s%s' % ("http://image.tmdb.org/t/p/original", show['backdrop_path'])
    if info['poster'] == None or info['poster'] == "": info['poster'] = "https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable.png"
    if info['fanart'] == None or info['fanart'] == "": info['fanart'] = get_background_path()
    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"): context_menu = [(_("Scan item to library"),"RunPlugin({0})".format(plugin.url_for("tv_add_to_library", id=tvdb_id))), ("%s %s" % (_("TV"), _("Trailer").lower()),"RunScript(script.qlickplay,info=playtvtrailer,tvdb_id={0})".format(tvdb_id)), ("[COLOR ff0084ff]Q[/COLOR]lick[COLOR ff0084ff]P[/COLOR]lay", "RunScript(script.qlickplay,info=tvinfo,tvdb_id={0})".format(tvdb_id)), ("%s %s (%s)" % ("Recommended", _("TV shows"), "TMDb"),"ActivateWindow(10025,plugin://script.qlickplay/?info=similartvshows&tvdb_id={0})".format(tvdb_id))]
    elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"): context_menu = [(_("Scan item to library"),"RunPlugin({0})".format(plugin.url_for("tv_add_to_library", id=tvdb_id))), ("%s %s" % (_("TV"), _("Trailer").lower()),"RunScript(script.extendedinfo,info=playtvtrailer,tvdb_id={0})".format(tvdb_id)), (_("Extended TV show info"), "RunScript(script.extendedinfo,info=extendedtvinfo,tvdb_id={0})".format(tvdb_id)), ("%s %s (%s)" % ("Recommended", _("TV shows"), "TMDb"),"ActivateWindow(10025,plugin://script.extendedinfo/?info=similartvshows&tvdb_id={0})".format(tvdb_id))]
    else: context_menu = [(_("Scan item to library"),"RunPlugin({0})".format(plugin.url_for("tv_add_to_library", id=tvdb_id)))]
    context_menu.append((_("Add to playlist"), "RunPlugin({0})".format(plugin.url_for("lists_add_show_to_list", src='tvdb', id=tvdb_id))))
    context_menu.append((_("TV show information"),'Action(Info)'))
    return {'label': to_utf8(info['title']),
            'path': plugin.url_for("tv_tvshow", id=tvdb_id),
            'context_menu': context_menu,
            'thumbnail': info['poster'],
            'icon': "DefaultVideo.png",
            'poster': info['poster'],
            'properties' : {'fanart_image' : info['fanart']},
            'info_type': 'video',
            'stream_info': {'video': {}},
            'info': info}

@plugin.cached(TTL=CACHE_TTL)
def list_seasons_tvdb(id):
    import_tvdb()
    id = int(id)
    show = tvdb[id]
    show_info = get_tvshow_metadata_tvdb(show, banners=False)
    title = show_info['name']
    items = []
    for (season_num, season) in show.items():
        if season_num == 0 and not plugin.get_setting(SETTING_INCLUDE_SPECIALS, bool): continue
        elif not season.has_aired(flexible=plugin.get_setting(SETTING_AIRED_UNKNOWN, bool) ): continue
        season_info = get_season_metadata_tvdb(show_info, season)
        if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"): context_menu = [("[COLOR ff0084ff]Q[/COLOR]lick[COLOR ff0084ff]P[/COLOR]lay", "RunScript(script.qlickplay,info=seasoninfo,tvshow={0},season={1})".format(title, season_num)), ("%s %s" % (_("TV"), _("Trailer").lower()),"RunScript(script.qlickplay,info=playtvtrailer,tvdb_id={0})".format(id)), (_("Recommended tv shows") + " (TMDb)","ActivateWindow(10025,plugin://script.qlickplay/?info=similartvshows&tvdb_id={0})".format(id))]
        elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"): context_menu = [(_("Extended season info"), "RunScript(script.extendedinfo,info=seasoninfo,tvshow={0},season={1})".format(title, season_num)), ("%s %s" % (_("TV"), _("Trailer").lower()),"RunScript(script.extendedinfo,info=playtvtrailer,tvdb_id={0})".format(id)), (_("Recommended tv shows") + " (TMDb)","ActivateWindow(10025,plugin://script.extendedinfo/?info=similartvshows&tvdb_id={0})".format(id))]
        else: context_menu = []
        items.append({'label': u"%s %d" % (_("Season"), season_num),
                      'path': plugin.url_for("tv_season", id=id, season_num=season_num),
                      'context_menu': context_menu,
                      'info': season_info,
                      'thumbnail': season_info['poster'],
                      'icon': "DefaultVideo.png",
                      'poster': season_info['poster'],
                      'properties' : {'fanart_image' : season_info['fanart']},
                      })
    if FORCE == True: plugin.set_view_mode(VIEW); return items
    else: return items

@plugin.cached(TTL=CACHE_TTL)
def list_episodes_tvdb(id, season_num):
    import_tvdb()
    id = int(id)
    season_num = int(season_num)
    show = tvdb[id]
    show_info = get_tvshow_metadata_tvdb(show, banners=False)
    title = show_info['name']
    season = show[season_num]
    season_info = get_season_metadata_tvdb(show_info, season, banners=True)
    items = []
    for (episode_num, episode) in season.items():
        if not season_num == 0 and not episode.has_aired(flexible=plugin.get_setting(SETTING_AIRED_UNKNOWN, bool)): break
        episode_info = get_episode_metadata_tvdb(season_info, episode)
        if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"): context_menu = [("[COLOR ff0084ff]Q[/COLOR]lick[COLOR ff0084ff]P[/COLOR]lay", "RunScript(script.qlickplay,info=episodeinfo,tvshow={0},season={1},episode={2})".format(title, season_num, episode_num)), ("%s %s" % (_("TV"), _("Trailer").lower()),"RunScript(script.qlickplay,info=playtvtrailer,tvdb_id={0})".format(id)), (_("Recommended tv shows") + " (TMDb)","ActivateWindow(10025,plugin://script.qlickplay/?info=similartvshows&tvdb_id={0})".format(id))]
        elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"): context_menu = [(_("Extended episode info"), "RunScript(script.extendedinfo,info=episodeinfo,tvshow={0},season={1},episode={2})".format(title, season_num, episode_num)), ("%s %s" % (_("TV"), _("Trailer").lower()),"RunScript(script.extendedinfo,info=playtvtrailer,tvdb_id={0})".format(id)), (_("Recommended tv shows") + " (TMDb)","ActivateWindow(10025,plugin://script.extendedinfo/?info=similartvshows&tvdb_id={0})".format(id))]
        else: context_menu = []
        context_menu.append(("{0} {1}...".format(_("Select"), _("Stream").lower()),"PlayMedia({0})".format(plugin.url_for("tv_play", id=id, season=season_num, episode=episode_num, mode='select'))))
        context_menu.append((_("Add to playlist"), "RunPlugin({0})".format(plugin.url_for("lists_add_episode_to_list", src='tvdb', id=id, season=season_num, episode = episode_num))))
        context_menu.append(("%s %s" % (_("Episode"), _("Information").lower()),'Action(Info)'))
        items.append({'label': episode_info.get('title'),
                      'path': plugin.url_for("tv_play", id=id, season=season_num, episode=episode_num, mode='default'),
                      'context_menu': context_menu,
                      'info': episode_info,
                      'is_playable': True,
                      'info_type': 'video',
                      'stream_info': {'video': {}},
                      'thumbnail': episode_info['poster'],
                      'poster': season_info['poster'],
                      'icon': "DefaultVideo.png",
                      'properties' : {'fanart_image' : episode_info['fanart']},
                      })
    return items

def tmdb_to_tvdb(tmdb_show):
    tvdb_show = None
    # Search by name and year
    name = tmdb_show['original_name']
    try: year = int(parse_year(tmdb_show['first_air_date']))
    except: year = ""
    results = [x['id'] for x in tvdb.search(name, year)]
    # Get by id if not a single result
    if len(results) != 1:
        id = tmdb.TV(tmdb_show['id']).external_ids().get('tvdb_id', None)
        if id:
            results = [id]
    # Use first result if still have many
    if results:
        tvdb_show = tvdb[results[0]]
    return tvdb_show, tmdb_show
