import copy, os
import urllib
import json
from xbmcswift2 import xbmc, xbmcgui, xbmcplugin, xbmcvfs
from meta import plugin, import_tmdb, LANG
from meta.info import get_movie_metadata, get_trakt_movie_metadata
from meta.gui import dialogs
from meta.utils.rpc import RPC
from meta.utils.text import page_redux, parse_year, date_to_timestamp, to_utf8
from meta.play.movies import play_movie, play_movie_from_guide
from meta.play.channelers import ADDON_STANDARD, ADDON_PICKER
from meta.play.players import ADDON_DEFAULT, ADDON_SELECTOR
from meta.library.movies import setup_library, add_movie_to_library, batch_add_movies_to_library
from meta.library.tools import scan_library
from meta.play.base import active_players, get_players, active_channelers
from meta.navigation.base import get_icon_path, get_genre_icon, get_background_path, get_base_genres, caller_name, caller_args
import meta.navigation.people
from language import get_string as _
from settings import CACHE_TTL, SETTING_MOVIES_LIBRARY_FOLDER, SETTING_MOVIES_PLAYED_BY_ADD, SETTING_FORCE_VIEW,\
    SETTING_MOVIES_VIEW, SETTING_ITEMS_PER_PAGE, SETTING_MOVIES_BATCH_ADD_FILE_PATH, SETTING_TV_BATCH_ADD_FILE_PATH,\
    SETTING_FORCE_VIEW, SETTING_MOVIES_VIEW, SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY,\
    SETTING_MOVIES_DEFAULT_AUTO_ADD, SETTING_RANDOM_PAGES, SETTING_SYNC_FOLDER

if RPC.settings.get_setting_value(setting="filelists.ignorethewhensorting") == {u'value': True}:
    SORT = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE,  xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT]
    SORTRAKT = [xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_GENRE,  xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT, xbmcplugin.SORT_METHOD_DURATION, xbmcplugin.SORT_METHOD_MPAA_RATING, xbmcplugin.SORT_METHOD_UNSORTED]
else:
    SORT = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_GENRE, xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT]
    SORTRAKT = [xbmcplugin.SORT_METHOD_VIDEO_YEAR, xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_GENRE, xbmcplugin.SORT_METHOD_VIDEO_RATING, xbmcplugin.SORT_METHOD_PLAYCOUNT, xbmcplugin.SORT_METHOD_DURATION, xbmcplugin.SORT_METHOD_MPAA_RATING, xbmcplugin.SORT_METHOD_UNSORTED]
FORCE = plugin.get_setting(SETTING_FORCE_VIEW, bool)
VIEW  = plugin.get_setting(SETTING_MOVIES_VIEW, int)

@plugin.route('/movies')
def movies():
    items = [{
            'label': "{0}: {1}".format(_("Search"), _("Movie")),
            'path': plugin.url_for("movies_search"),
            'icon': get_icon_path("search"),
        },
        {
            'label': "{0} ({1})".format("Blockbusters", "TMDb"),
            'path': plugin.url_for("tmdb_movies_blockbusters", page='1'),
            'icon': get_icon_path("most_voted"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_blockbusters_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_play_random_blockbuster"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format(_("Genres"), "TMDb"),
            'path': plugin.url_for("tmdb_movies_genres"),
            'icon': get_icon_path("genres"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_genre_to_library", id="28|12|16|35|80|99|18|10751|14|36|27|10402|9648|10749|878|10770|53|10752|37", page='1', confirm="yes"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("In theatres", "TMDb"),
            'path': plugin.url_for("tmdb_movies_now_playing", page='1'),
            'icon': get_icon_path("intheatres"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_now_playing_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_play_random_now_playing"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Popular", "TMDb"),
            'path': plugin.url_for("tmdb_movies_popular", page='1'),
            'icon': get_icon_path("popular"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_popular_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_play_random_popular"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Top rated", "TMDb"),
            'path': plugin.url_for("tmdb_movies_top_rated", page='1'),
            'icon': get_icon_path("top_rated"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_top_rated_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("tmdb_movies_play_random_top_rated"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Most played", "Trakt"),
            'path': plugin.url_for("trakt_movies_played", page='1'),
            'icon': get_icon_path("player"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_played_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_played"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Most watched", "Trakt"),
            'path': plugin.url_for("trakt_movies_watched", page='1'),
            'icon': get_icon_path("traktwatchlist"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_watched_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_watched"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Most collected", "Trakt"),
            'path': plugin.url_for("trakt_movies_collected", page='1'),
            'icon': get_icon_path("traktcollection"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_collected_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_collected"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Popular", "Trakt"),
            'path': plugin.url_for("trakt_movies_popular", page='1'),
            'icon': get_icon_path("traktrecommendations"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_popular_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_popular"))
                ),
            ],
        },
        {
            'label': "{0} ({1})".format("Trending", "Trakt"),
            'path': plugin.url_for("trakt_movies_trending", page='1'),
            'icon': get_icon_path("trending"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_trending_to_library", page='1', confirm="yes"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_trending"))
                ),
            ],
        },
        {
            'label': "{0} {1}".format(_("Use your"), "Trakt"),
            'path': plugin.url_for("trakt_my_movies"),
            'icon': get_icon_path("trakt"),
        }
    ]
    for item in items: item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.finish(items=items, view_mode=VIEW)
    else: return plugin.finish(items=items)


@plugin.route('/movies/tmdb/blockbusters/<page>')
def tmdb_movies_blockbusters(page, raw=False):
    import_tmdb()
    result = tmdb.Discover().movie(language=LANG, append_to_response="external_ids,videos", **{'page': page, 'sort_by': 'revenue.desc'})
    if raw: return result
    else: return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/blockbusters_to_library/<page>/<confirm>')
def tmdb_movies_blockbusters_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Blockbusters", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in tmdb_movies_blockbusters(i, True)["results"] if m not in movies]
        items["results"] = movies
        movies_add_all_to_library(items)

@plugin.route('/movies/tmdb/random_blockbuster')
def tmdb_movies_play_random_blockbuster():
    result = {}
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.update(tmdb_movies_blockbusters(i, raw=True))
    tmdb_movies_play_random(result)


@plugin.route('/movies/tmdb/now_playing/<page>')
def tmdb_movies_now_playing(page, raw=False):
    import_tmdb()
    result = tmdb.Movies().now_playing(language=LANG, page=page, append_to_response="external_ids,videos")
    if raw: return result
    else: return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/now_playing_to_library/<page>/<confirm>')
def tmdb_movies_now_playing_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("In theatres", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in tmdb_movies_now_playing(i, True)["results"] if m not in movies]
        items["results"] = movies
        movies_add_all_to_library(items)

@plugin.route('/movies/tmdb/random_now_playing')
def tmdb_movies_play_random_now_playing():
    result = {}
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.update(tmdb_movies_now_playing(i, raw=True))
    tmdb_movies_play_random(result)


@plugin.route('/movies/tmdb/popular/<page>')
def tmdb_movies_popular(page, raw=False):
    """ Most popular movies """
    import_tmdb()    
    result = tmdb.Movies().popular(language=LANG, page=page, append_to_response="external_ids,videos")
    if raw: return result
    else: return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/popular_to_library/<page>/<confirm>')
def tmdb_movies_popular_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Popular", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in tmdb_movies_popular(i, True)["results"] if m not in movies]
        items["results"] = movies
        movies_add_all_to_library(items)

@plugin.route('/movies/tmdb/random_popular')
def tmdb_movies_play_random_popular():
    result = {}
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.update(tmdb_movies_popular(i, raw=True))
    tmdb_movies_play_random(result)


@plugin.route('/movies/tmdb/top_rated/<page>')
def tmdb_movies_top_rated(page, raw=False):
    import_tmdb()
    result = tmdb.Movies().top_rated(language=LANG, page=page, append_to_response="external_ids,videos")
    if raw: return result
    else: return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/top_rated_to_library/<page>/<confirm>')
def tmdb_movies_top_rated_to_library(page, confirm):
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Iop rated", "TMDb", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in tmdb_movies_top_rated(i, True)["results"] if m not in movies]
        items["results"] = movies
        movies_add_all_to_library(items)

@plugin.route('/movies/tmdb/random_top_rated')
def tmdb_movies_play_random_top_rated():
    result = {}
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.update(tmdb_movies_top_rated(i, raw=True))
    tmdb_movies_play_random(result)


@plugin.route('/movies/search')
def movies_search():
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return movies_search_term(term, 1)
    else: return

@plugin.route('/movies/search/edit/<term>')
def movies_search_edit(term):
    term = plugin.keyboard(default=term, heading=_("Enter search string"))
    if term != None and term != "": return movies_search_term(term, 1)
    else: return

@plugin.route('/movies/search_term/<term>/<page>')
def movies_search_term(term, page):
    items = [
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
            'icon': get_icon_path("tv"),
            'thumbnail': get_icon_path("tv"),
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
            'label': "{0}: '{1}' ({2} - {3})".format(_("Search"), term, _("Movies"), plugin.addon.getAddonInfo('name')),
            'path': plugin.url_for("movies_search_term", term=term, page='1'),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
        {
            'label': "{0} {1}".format(_("Edit"), _("Search string").lower()),
            'path': plugin.url_for("movies_search_edit", term=term),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
    ]
    for item in items:
        item['properties'] = {'fanart_image' : get_background_path()}
    return items

@plugin.route('/movies/trakt/search')
def trakt_movies_search():
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return trakt_movies_search_term(term, 1)
    else: return

@plugin.route('/movies/trakt/search/<term>/<page>')
def trakt_movies_search_term(term, page):
    from trakt import trakt
    results, pages = trakt.search_for_movie_paginated(term, page)
    return list_trakt_search_items(results, pages, page)

@plugin.route('/movies/trakt/personal')
def trakt_my_movies():
    items = [
        {
            'label': "{0} ({1})".format(_("Library"), "Trakt Collection"),
            'path': plugin.url_for("trakt_movies_collection"),
            'icon': get_icon_path("traktcollection"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_collection_to_library"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_collection"))
                )
            ]
        },
        {
            'label': "{0} {1} ({2})".format(_("Unwatched"), _("movies"), "Trakt Watchlist"),
            'path': plugin.url_for("trakt_movies_watchlist"),
            'icon': get_icon_path("traktwatchlist"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_watchlist_to_library"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_watchlist"))
                )
            ]
        },
        {
            'label':"{0} ({1})".format(_("Find similar"), "Trakt Recommendations"),
            'path': plugin.url_for("trakt_movies_recommendations"),
            'icon': get_icon_path("traktrecommendations"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_recommendations_to_library"))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("trakt_movies_play_random_recommendation"))
                )
            ]
        }
    ]
    for item in items: item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.finish(items=items, view_mode=VIEW)
    else: return plugin.finish(items=items)


@plugin.route('/movies/trakt/played/<page>')
def trakt_movies_played(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_played_movies_paginated(page)
    if raw: return results
    else: return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/played_to_library/<page>/<confirm>')
def trakt_movies_played_to_library(page, confirm, uncached=False):
    from trakt import trakt
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Most played", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in trakt_movies_played(i, True) if m not in movies]
        if uncached: movies_add_all_to_library(movies, True)
        else: movies_add_all_to_library(movies)

@plugin.route('/movies/trakt/random_played')
def trakt_movies_play_random_played():
    result = []
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.extend(trakt_movies_played(i, raw=True))
    trakt_movies_play_random(result)


@plugin.route('/movies/trakt/watched/<page>')
def trakt_movies_watched(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_watched_movies_paginated(page)
    if raw: return results
    else: return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/watched_to_library/<page>/<confirm>')
def trakt_movies_watched_to_library(page, confirm, uncached=False):
    from trakt import trakt
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Most watched", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in trakt_movies_watched(i, True) if m not in movies]
        if uncached: movies_add_all_to_library(movies, True)
        else: movies_add_all_to_library(movies)

@plugin.route('/movies/trakt/random_watched')
def trakt_movies_play_random_watched():
    result = []
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.extend(trakt_movies_watched(i, raw=True))
    trakt_movies_play_random(result)


@plugin.route('/movies/trakt/collected/<page>')
def trakt_movies_collected(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_collected_movies_paginated(page)
    if raw: return results
    else: return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/collected_to_library/<page>/<confirm>')
def trakt_movies_collected_to_library(page, confirm, uncached=False):
    from trakt import trakt
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Most collected", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in trakt_movies_collected(i, True) if m not in movies]
        if uncached: movies_add_all_to_library(movies, True)
        else: movies_add_all_to_library(movies)

@plugin.route('/movies/trakt/random_collected')
def trakt_movies_play_random_collected():
    result = []
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.extend(trakt_movies_collected(i, raw=True))
    trakt_movies_play_random(result)


@plugin.route('/movies/trakt/popular/<page>')
def trakt_movies_popular(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_popular_movies_paginated(page)
    if raw: return results
    else: return list_trakt_movies([{u'movie': m} for m in results], pages, page)

@plugin.route('/movies/trakt/popular_to_library/<page>/<confirm>')
def trakt_movies_popular_to_library(page, confirm, uncached=False):
    from trakt import trakt
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Popular", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in trakt_movies_popular(i, True) if m not in movies]
        if uncached: movies_add_all_to_library([{u'movie': m} for m in movies], True)
        else: movies_add_all_to_library([{u'movie': m} for m in movies])

@plugin.route('/movies/trakt/random_popular') 
def trakt_movies_play_random_popular():
    result = []
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.extend(trakt_movies_popular(i, raw=True))
    trakt_movies_play_random(result, True)


@plugin.route('/movies/trakt/trending/<page>')
def trakt_movies_trending(page, raw=False):
    from trakt import trakt
    results, pages = trakt.trakt_get_trending_movies_paginated(page)
    if raw: return results
    else: return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/trending_to_library/<page>/<confirm>')
def trakt_movies_trending_to_library(page, confirm, uncached=False):
    from trakt import trakt
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format("Trending", "Trakt", _("page"), ','.join([str(i) for i in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for i in pages: movies = movies + [m for m in trakt_movies_trending(i, True) if m not in movies]
        if uncached: movies_add_all_to_library(movies, True)
        else: movies_add_all_to_library(movies)

@plugin.route('/movies/trakt/random_trending')
def trakt_movies_play_random_trending():
    result = []
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages): result.extend(trakt_movies_trending(i, raw=True))
    trakt_movies_play_random(result)


@plugin.route('/movies/tmdb/search')
def tmdb_movies_search():
    """ Activate movie search """
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return tmdb_movies_search_term(term, 1)
    else: return

@plugin.route('/movies/tmdb/search_term/<term>/<page>')
def tmdb_movies_search_term(term, page):
    """ Perform search of a specified <term>"""
    import_tmdb()
    result = tmdb.Search().movie(query=term, language = LANG, page = page, append_to_response="external_ids,videos")
    return list_tmdb_items(result)


@plugin.route('/movies/trakt/personal/collection')
def trakt_movies_collection(raw=False):
    from trakt import trakt
    result = trakt.trakt_get_collection("movies")
    if raw: return result
    else: return list_trakt_movies(result, "1", "1")

@plugin.route('/movies/trakt/personal/random_collection')
def trakt_movies_play_random_collection():
    from meta.utils.playrandom import trakt_play_random
    movies = trakt_movies_collection(raw=True)
    for movie in movies:
        movie["type"] = "movie"
    trakt_play_random(movies)


@plugin.route('/movies/trakt/personal/watchlist')
def trakt_movies_watchlist(raw=False):
    from trakt import trakt
    result = trakt.trakt_get_watchlist("movies")
    if raw: return result
    else: return list_trakt_movies(result, "1", "1")

@plugin.route('/movies/trakt/personal/random_watchlist')
def trakt_movies_play_random_watchlist():
    trakt_movies_play_random(trakt_movies_watchlist(raw=True))

@plugin.route('/movies/trakt/personal/recommendations')
def trakt_movies_recommendations(raw=False):
    from trakt import trakt
    genres_dict = dict([(x['slug'], x['name']) for x in trakt.trakt_get_genres("movies")])
    result = trakt.get_recommendations("movies")
    if raw: return result
    else: return list_trakt_movies([{u'movie': m} for m in result], "1", "1")

@plugin.route('/movies/trakt/personal/random_recommendation')
def trakt_movies_play_random_recommendation():
    trakt_movies_play_random(trakt_movies_recommendations(raw=True), True)

@plugin.route('/movies/trakt/person/<person_id>')
def trakt_movies_person(person_id, raw=False):
    from trakt import trakt
    result = trakt.get_person_movies(person_id)['cast']
    if raw: return result
    else: return list_trakt_persons(result)

@plugin.route('/movies/tmdb/genres')
def tmdb_movies_genres():
    """ List all movie genres """
    genres = get_base_genres()
    items = sorted([{'label': name,
                     'icon': get_genre_icon(id),
                     'path': plugin.url_for("tmdb_movies_genre", id=id, page='1'),
                     'context_menu': [(
                                       _("Scan item to library"),
                                       "RunPlugin({0})".format(plugin.url_for("tmdb_movies_genre_to_library", id=id, page='1', confirm="yes"))
                                      ),
                                      (
                                       "{0} ({1})".format(_("Play"), _("Random").lower()),
                                       "RunPlugin({0})".format(plugin.url_for("tmdb_movies_play_random_genre", id = id))
                                      )]} for id, name in genres.items()], key=lambda k: k['label'])
    for item in items: item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/movies/genre/<id>/<page>')
def tmdb_movies_genre(id, page, raw=False):
    """ Movies by genre id """
    import_tmdb()
    result = tmdb.Genres(id).movies(id=id, language=LANG, page=page)
    if raw: return result
    else: return list_tmdb_movies(result)

@plugin.route('/movies/genre_to_library/<id>/<page>/<confirm>')
def tmdb_movies_genre_to_library(id, page, confirm):
    genre_names = get_base_genres()
    if "|" in id:
        genres = id.split("|")
        name = ' + '.join([genre_names.get(int(g), None) for g in genres])
    else:
        genres = [id]
        name = genre_names.get(int(id), None)
    try:
        page = int(page)
        pages = [page]
    except: pages = page_redux(page)
    if confirm == "no" or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}[CR]{2}".format(_("Library"), _("Add %s") % ("'{0} ({1}) {2} {3}'".format(name, "TMDb", _("page"), ','.join([str(p) for p in pages]))),_("Are you sure?"))):
        items = {}
        movies = []
        for g in genres:
            for p in pages: movies = movies + [m for m in tmdb_movies_genre(int(g), p, True)["results"] if m not in movies]
        items["results"] = movies
        movies_add_all_to_library(items)

@plugin.route('/movies/tmdb/random_genre/<id>')
def tmdb_movies_play_random_genre(id):
    result = {}
    pages = plugin.get_setting(SETTING_RANDOM_PAGES, int) + 1
    for i in range(1, pages):
        result.update(tmdb_movies_genre(id, i, raw=True))
    tmdb_movies_play_random(result)


@plugin.route('/movies/trakt/collection_to_library')
def trakt_movies_collection_to_library(preaprove=False, uncached = False):
    from trakt import trakt
    if preaprove  or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}".format(_("Add %s") % ("'{0} {1} {2}'".format("Trakt", _("movie"), _("Collection").lower())),_("Are you sure?"))):
        if uncached:
            movies_add_all_to_library(trakt.trakt_get_collection_uncached("movies"), True)
        else:
            movies_add_all_to_library(trakt.trakt_get_collection("movies"))

@plugin.route('/movies/trakt/watchlist_to_library')
def trakt_movies_watchlist_to_library(preaprove=False, uncached = False):
    from trakt import trakt
    if preaprove  or dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}".format(_("Add %s") % ("'{0} {1} {2}'".format("Trakt", _("movie"), _("Watchlist").lower())),_("Are you sure?"))):
        if uncached:
            movies_add_all_to_library(trakt.trakt_get_watchlist_uncached("movies"), True)
        else:
            movies_add_all_to_library(trakt.trakt_get_watchlist("movies"))

@plugin.route('/movies/trakt/recommendations_to_library')
def trakt_movies_recommendations_to_library():
    from trakt import trakt
    if dialogs.yesno(_("Scan item to library"), "{0}[CR]{1}".format(_("Add %s") % ("'{0} {1} {2}'".format("Trakt", _("movie"), _("Recommendations").lower())),_("Are you sure?"))):
        movies_add_all_to_library([{u'movie': i} for i in trakt.get_recommendations("movies")])

@plugin.route('/movies/set_library_player/<path>')
def set_movie_library_player(path):
    # get active players
    players = active_players("movies")
    players.insert(0, ADDON_SELECTOR)
    players.insert(0, ADDON_DEFAULT)
    # let the user select one player
    selection = dialogs.select("{0}".format(_("Select %s") % "{0} {1}".format(_("Default").lower(), _("Player").lower())), [p.title for p in players])
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

def movies_add_all_to_library(items, noscan=False):
    library_folder = setup_library(plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))
    if "results" in items: ids = '\n'.join([str(r["id"]) for r in items["results"]])
    else: ids = '\n'.join([i["movie"]["ids"]["imdb"] if i["movie"]["ids"]["imdb"] != None and i["movie"]["ids"]["imdb"] != "" else i["movie"]["ids"]["tmdb"] for i in items])
    movies_batch_add_file = plugin.get_setting(SETTING_MOVIES_BATCH_ADD_FILE_PATH, unicode)
    if xbmcvfs.exists(movies_batch_add_file):
        batch_add_file = xbmcvfs.File(movies_batch_add_file)
        pre_ids = batch_add_file.read()
        xids = pre_ids.split("\n")
        for id in xids:
            if id != "" and id != None and id not in ids: ids = ids + str(id) + '\n'
        batch_add_file.close()
        xbmcvfs.delete(movies_batch_add_file)
    batch_add_file = xbmcvfs.File(movies_batch_add_file, 'w')
    batch_add_file.write(str(ids))
    batch_add_file.close()
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/movies/batch_add_to_library)")

@plugin.route('/movies/add_to_library/<src>/<id>')
def movies_add_to_library(src, id):
    library_folder = setup_library(plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))
    if library_folder == False: return
    """ Add movie to library """
    date = None
    if src == "tmdb":
        import_tmdb()
        movie = tmdb.Movies(id).info()
        date = date_to_timestamp(movie.get('release_date'))
        imdb_id = movie.get('imdb_id')
        if imdb_id:
            src = "imdb"
            id = imdb_id
    players = active_players("movies")
    if plugin.get_setting(SETTING_MOVIES_DEFAULT_AUTO_ADD, bool) == True:
        player = plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    else:
        players.insert(0, ADDON_SELECTOR)
        players.insert(0, ADDON_DEFAULT)
        selection = dialogs.select(_("Play using..."), [p.title for p in players])
        if selection == -1:
            return
        player = players[selection]
    # add to library
    if plugin.get_setting(SETTING_MOVIES_DEFAULT_AUTO_ADD, bool) == True:
        add_movie_to_library(library_folder, src, id, play_plugin=plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, unicode))
    else:
        add_movie_to_library(library_folder, src, id, play_plugin=player.id)
        dialogs.notify(msg=player.id, title=_("%s not found").replace("%s ",""), delay=3000, image=get_icon_path("movies"))
    scan_library(type="video", path=plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))

@plugin.route('/movies/add_to_library_parsed/<src>/<id>/<player>')
def movies_add_to_library_parsed(src, id, player):
    library_folder = setup_library(plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))
    date = None
    if src == "tmdb":
        import_tmdb()
        movie = tmdb.Movies(id).info()
        date = date_to_timestamp(movie.get('release_date'))
        imdb_id = movie.get('imdb_id')
        if imdb_id:
            if imdb_id != None and imdb_id != "":
                src = "imdb"
                id = imdb_id
    add_movie_to_library(library_folder, src, id, player)
    scan_library(type="video", path=plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))

@plugin.route('/movies/batch_add_to_library')
def movies_batch_add_to_library():
    """ Batch add movies to library """
    movie_batch_file = plugin.get_setting(SETTING_MOVIES_BATCH_ADD_FILE_PATH, unicode)
    if xbmcvfs.exists(movie_batch_file):
        try:
            f = open(xbmc.translatePath(movie_batch_file), 'r')
            r = f.read()
            f.close()
            ids = r.split('\n')
        except: return dialogs.notify(msg='Movies Batch Add File', title=_("%s not found").replace("%s ",""), delay=3000, image=get_icon_path("movies"))
        library_folder = setup_library(plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))
        import_tmdb()
        for id in ids:
            if "," in id:
                csvs = id.split(',')
                for csv in csvs:
                    if not str(csv).startswith("tt") and csv != "":
                        movie = tmdb.Movies(csv).info()
                        csv = movie.get('imdb_id')
                    batch_add_movies_to_library(library_folder, csv)
            else:
                if not str(id).startswith("tt") and id != "":
                    movie = tmdb.Movies(id).info()
                    id = movie.get('imdb_id')
                batch_add_movies_to_library(library_folder, id)
        os.remove(xbmc.translatePath(movie_batch_file))
        if xbmcvfs.exists(plugin.get_setting(SETTING_TV_BATCH_ADD_FILE_PATH, unicode)):
            xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/tv/batch_add_to_library)")
            return True
        else:
            xbmc.sleep(1000)
            dialogs.notify(msg='Starting library scan', title='Added movie strm-files', delay=5000, image=get_icon_path("movies"))
            scan_library(type="video", path=plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))
            return True
    if xbmcvfs.exists(plugin.get_setting(SETTING_TV_BATCH_ADD_FILE_PATH, unicode)): xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/tv/batch_add_to_library)")

@plugin.route('/movies/related/<id>/<page>')
def movies_related(id, page):
    import_tmdb()
    movie = tmdb.Movies(id).info()
    imdb_id = movie.get('imdb_id')
    from trakt import trakt
    results, pages = trakt.trakt_get_related_movies_paginated(imdb_id, page)
    return list_trakt_movies([{u'movie': m} for m in results], "1", "1")

def list_tmdb_movies(result):
    if FORCE == True: plugin.set_view_mode(VIEW)
    genres_dict = get_base_genres()
    movies = [get_movie_metadata(item, genres_dict) for item in result['results']]
    items = [make_movie_item(movie) for movie in movies]
    if 'page' in result:
        page = int(result['page'])
        pages = int(result['total_pages'])
        args = caller_args()
        if pages > page:
            args['page'] = str(page + 1)
            args['confirm'] = "yes"
            items.append({
                'label': "{0}  >>  ({1}/{2})".format(_("Next page"), page + 1, "1000"),
                'icon': get_icon_path("item_next"),
                'path': plugin.url_for(caller_name(), **args),
                'properties' : {'fanart_image' : get_background_path()},
                'context_menu': [(_("Scan item to library"), "RunPlugin({0})".format(plugin.url_for("{0}{1}".format(caller_name(),"_to_library"), **args)))]})
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

def list_tmdb_items(result):
    if FORCE == True: plugin.set_view_mode(VIEW)
    genres_dict = get_base_genres()
    movies = [get_movie_metadata(item, None) for item in result['results']]
    items = [make_movie_item(movie) for movie in movies]
    if 'page' in result:
        page = int(result['page'])
        pages = int(result['total_pages'])
        args = caller_args()
        if pages > page:
            args['page'] = str(page + 1)
            items.append({
                'label': "{0}  >>  ({1}/{2})".format(_("Next page"), page + 1, "1000"),
                'icon': get_icon_path("item_next"),
                'path': plugin.url_for(caller_name(), **args),
                'properties' : {'fanart_image' : get_background_path()}})
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

def list_trakt_persons(results):
    from trakt import trakt
    genres_dict = dict([(x['slug'], x['name']) for x in trakt.trakt_get_genres("movies")])
    movies = [get_trakt_movie_metadata(item["movie"], genres_dict) for item in results]
    items = [make_movie_item(movie) for movie in movies]
    if FORCE == True: return plugin.finish(items=items, view_mode=VIEW)
    else: return plugin.finish(items=items)

def list_trakt_search_items(results, pages, page):
    from trakt import trakt
    movies = [get_trakt_movie_metadata(item["movie"], None) for item in results]
    items = [make_movie_item(movie) for movie in movies]
    page = int(page)
    pages = int(pages)
    if pages > 1:
        args = caller_args()
        args['page'] = page + 1
        items.append({
            'label': "{0}  >>  ({1}/{2})".format(_("Next page"), page + 1, pages),
            'path': plugin.url_for(caller_name(), **args),
            'icon': get_icon_path("item_next"),
            'properties' : {'fanart_image' : get_background_path()}})
    if FORCE == True: return  plugin.finish(items=items, view_mode=VIEW)
    else: return plugin.finish(items=items)

def list_trakt_movies(results, pages, page):
    from trakt import trakt
    genres_dict = dict([(x['slug'], x['name']) for x in trakt.trakt_get_genres("movies")])
    movies = [get_trakt_movie_metadata(item["movie"], genres_dict) for item in results]
    items = [make_movie_item(movie) for movie in movies]
    page = int(page)
    pages = int(pages)
    if pages > 1:
        args = caller_args()
        args['page'] = page + 1
        args['confirm'] = "yes"
        items.append({
            'label': "{0}  >>  ({1}/{2})".format(_("Next page"), page + 1, pages),
            'path': plugin.url_for(caller_name(), **args),
            'icon': get_icon_path("item_next"),
            'properties' : {'fanart_image' : get_background_path()},
            'context_menu': [(
                              _("Scan item to library"),
                              "RunPlugin({0})".format(plugin.url_for("{0}{1}".format(caller_name(),"_to_library"), **args)))]})
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORTRAKT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORTRAKT)

@plugin.route('/movies/play/<src>/<id>/<mode>')
def movies_play(src, id, mode):
    import_tmdb()
    tmdb_id = None
    if src == "tmdb": tmdb_id = id
    elif src == "imdb":
        info = tmdb.Find(id).info(external_source="imdb_id")
        try: tmdb_id = info["movie_results"][0]["id"]
        except (KeyError, TypeError): pass
    if tmdb_id: play_movie(tmdb_id, mode)
    else: plugin.set_resolved_url()

@plugin.route('/movies/play_guide/<src>/<id>/<mode>')
def guide_movies_play(src, id, mode):
    import_tmdb()
    tmdb_id = None
    if src == "tmdb": tmdb_id = id
    elif src == "imdb":
        info = tmdb.Find(id).info(external_source="imdb_id")
        try: tmdb_id = info["movie_results"][0]["id"]
        except (KeyError, TypeError): pass
    if tmdb_id: play_movie_from_guide(tmdb_id, mode)
    else: plugin.set_resolved_url()

@plugin.route('/movies/play_by_name/<name>/<lang>')
def movies_play_by_name(name, lang = "en"):
    """ Activate tv search """
    import_tmdb()
    from meta.utils.text import parse_year
    items = tmdb.Search().movie(query=name, language=lang, page=1)["results"]
    if not items: return dialogs.ok(_("%s not found") % _("Movie"), "{0} {1}".format(_("No movie information found on TMDB for"), name))
    if len(items) > 1:
        selection = dialogs.select("{0}".format(_("Choose thumbnail").replace(_("Thumbnail").lower(),_("Movie").lower())), ["{0} ({1})".format(
            to_utf8(s["title"]),
            parse_year(s["release_date"])) for s in items])
    else: selection = 0
    if selection != -1:
        id = items[selection]["id"]
        movies_play("tmdb", id, "context")
        if plugin.get_setting(SETTING_MOVIES_PLAYED_BY_ADD, bool) == True: movies_add_to_library("tmdb", id)

@plugin.route('/movies/play_by_name_guide/<name>/<lang>')
def guide_movies_play_by_name(name, lang = "en"):
    import_tmdb()
    from meta.utils.text import parse_year
    items = tmdb.Search().movie(query=name, language=lang, page=1)["results"]
    if not items: return dialogs.ok(_("%s not found") % _("Movie"), "{0} {1}".format(_("No movie information found on TMDB for"), name))
    if len(items) > 1:
        selection = dialogs.select("{0}".format(_("Choose thumbnail").replace(_("Thumbnail").lower(),_("Movie").lower())), ["{0} ({1})".format(
            to_utf8(s["title"]),
            parse_year(s["release_date"])) for s in items])
    else: selection = 0
    if selection != -1:
        id = items[selection]["id"]
        guide_movies_play("tmdb", id, "default")
        if plugin.get_setting(SETTING_MOVIES_PLAYED_BY_ADD, bool) == True: movies_add_to_library("tmdb", id)

def trakt_movies_play_random(movies, convert_list = False):
    from meta.utils.playrandom import trakt_play_random
    for movie in movies:
        movie["type"] = "movie"
        if convert_list:
            movie["movie"] = movie
    trakt_play_random(movies)

def tmdb_movies_play_random(list):
    from meta.utils.playrandom import tmdb_play_random
    movies = list["results"]
    for movie in movies:
        movie["type"] = "movie"
    tmdb_play_random(movies)

def make_movie_item(movie_info, is_list = False):
    try: tmdb_id = movie_info.get('tmdb')
    except: tmdb_id = ""
    if tmdb_id == "": 
        try: tmdb_id = info['tmdb']
        except: tmdb_id = False
    try: imdb_id = movie_info.get('imdb')
    except: imdb_id = ""
    if imdb_id == "": 
        try: imdb_id = info['imdb']
        except: imdb_id = False
    if movie_info['poster'] == None or movie_info['poster'] == "": movie_info['poster'] = "https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable.png"
    if movie_info['fanart'] == None or movie_info['fanart'] == "": movie_info['fanart'] = get_background_path()
    if tmdb_id:
        id = tmdb_id 
        src = 'tmdb'
    elif imdb_id:
        id = imdb_id 
        src = 'imdb'
    else: dialogs.notify(msg="tmdb or imdb id", title=_("%s not found").replace("%s ",""), delay=3000, image=get_icon_path("movies"))
    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"): context_menu = [(_("Scan item to library"),"RunPlugin({0})".format(plugin.url_for("movies_add_to_library", src=src, id=id))), ("%s %s" % (_("Movie"), _("Trailer").lower()),"RunScript(script.qlickplay,info=playtrailer,id={0})".format(id)), ("[COLOR ff0084ff]Q[/COLOR]lick[COLOR ff0084ff]P[/COLOR]lay", "RunScript(script.qlickplay,info=movieinfo,id={0})".format(id)), ("%s %s (%s)" % ("Recommended", _("movies"), "TMDb"),"ActivateWindow(10025,plugin://script.qlickplay/?info=similarmovies&id={0})".format(id))]
    elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"): context_menu = [(_("Scan item to library"),"RunPlugin({0})".format(plugin.url_for("movies_add_to_library", src=src, id=id))), ("%s %s" % (_("Movie"), _("Trailer").lower()),"RunScript(script.extendedinfo,info=playtrailer,id={0})".format(id)), (_("Extended movie info"), "RunScript(script.extendedinfo,info=extendedinfo,id={0})".format(id)), ("%s %s (%s)" % ("Recommended", _("movies"), "TMDb"),"ActivateWindow(10025,plugin://script.extendedinfo/?info=similarmovies&id={0})".format(id))]
    else: context_menu = [(_("Scan item to library"),"RunPlugin({0})".format(plugin.url_for("movies_add_to_library", src=src, id=id)))]
    context_menu.append(("%s %s (%s)" % ("Related", _("movies"), "Trakt"),"ActivateWindow(10025,{0})".format(plugin.url_for("movies_related", id=id, page=1))))
    context_menu.append(("{0} {1}...".format(_("Select"), _("Stream").lower()),"PlayMedia({0})".format(plugin.url_for("movies_play", src=src, id=id, mode='select'))))
    context_menu.append((_("Add to playlist"),"RunPlugin({0})".format(plugin.url_for("lists_add_movie_to_list", src=src, id=id))))
    context_menu.append((_("Movie information"),'Action(Info)'))
    if is_list:
        context_menu.append(
            (
                "{0}".format(_("Remove from library").replace(_("Library").lower(),_("Playlist").lower())),
                "RunPlugin({0})".format(plugin.url_for("lists_remove_movie_from_list", src=src, id=id))
            )
        )
    return {
        'label': movie_info['title'],
        'path': plugin.url_for("movies_play", src=src, id=id, mode='default'),
        'context_menu': context_menu,
        'thumbnail': movie_info['poster'],
        'icon': movie_info['poster'],
        'banner': movie_info['fanart'],
        'poster': movie_info['poster'],
        'properties' : {'fanart_image' : movie_info['fanart']},
        'is_playable': True,
        'info_type': 'video',
        'stream_info': {'video': {}},
        'info': movie_info
    }
