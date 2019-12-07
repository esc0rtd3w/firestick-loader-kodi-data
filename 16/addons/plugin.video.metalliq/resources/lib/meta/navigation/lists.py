import os
from xbmcswift2 import xbmc, xbmcplugin, xbmcvfs
from xbmcswift2.listitem import ListItem
from meta import plugin, import_tvdb, import_tmdb
from meta.navigation.movies import make_movie_item
from meta.navigation.tvshows import make_tvshow_item
from meta.info import get_tvshow_metadata_trakt, get_season_metadata_trakt, get_episode_metadata_trakt, get_trakt_movie_metadata
from meta.navigation.base import get_icon_path, get_background_path
from meta.navigation.movies import make_movie_item, movies_add_to_library
from meta.navigation.tvshows import make_tvshow_item, tv_play, tv_season, tv_add_to_library
import meta.navigation.people
from meta.gui import dialogs
from meta.utils.rpc import RPC
from meta.utils.text import to_utf8
from language import get_string as _
from trakt import trakt
from settings import SETTING_ITEMS_PER_PAGE, SETTING_FORCE_VIEW, SETTING_LIST_VIEW, SETTING_TRAKT_LIST_ARTWORK

if RPC.settings.get_setting_value(setting="filelists.ignorethewhensorting") == {u'value': True}:
    SORT = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_VIDEO_YEAR]
else:
    SORT = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL, xbmcplugin.SORT_METHOD_VIDEO_YEAR]
FORCE = plugin.get_setting(SETTING_FORCE_VIEW, bool)
VIEW  = plugin.get_setting(SETTING_LIST_VIEW, int)

@plugin.route('/lists')
def lists():
    """ Lists directory """
    items = [
        {
            'label': "{0} {1} (Trakt)".format("\"Liked\"", _("Playlists").lower()),
            'path': plugin.url_for("lists_trakt_liked_lists", page = 1),
            'icon': get_icon_path("traktlikedlists"),
            'thumbnail': get_icon_path("traktlikedlists"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_add_liked_to_library"))
                )
            ]
        },
        {
            'label': "{0} {1} (Trakt)".format(_("Watch your"), _("Playlists").lower()),
            'path': plugin.url_for("lists_trakt_my_lists"),
            'icon': get_icon_path("traktmylists"),
            'thumbnail': get_icon_path("traktmylists"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_add_my_lists_to_library"))
                )
            ]
        },
        {
            'label': "{0}: {1} (Trakt)".format(_("Search"), _("Playlist")),
            'path': plugin.url_for("lists_trakt_search_for_lists"),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
    ]
    fanart = plugin.addon.getAddonInfo('fanart')
    for item in items:
        item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.set_view_mode(VIEW); return items
    else: return items

@plugin.route('/lists/trakt/liked_lists/<page>', options = {"page": "1"})
def lists_trakt_liked_lists(page):
    lists, pages = trakt.trakt_get_liked_lists(page)
    items = []
    for list in lists:
        info = list["list"]
        name = info["name"]
        user = info["user"]["username"]
        slug = info["ids"]["slug"]
        items.append({
            'label': name,
            'path': plugin.url_for("lists_trakt_show_list", user = user, slug = slug),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_add_all_to_library", user=user, slug=slug))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_play_random", user=user, slug=slug))
                )
            ],
            'icon': get_icon_path("traktlikedlists"),
            'thumbnail': get_icon_path("traktlikedlists"),
        })
    if pages > page:
        items.append({
            'label': "{0} {1}".format(_("Next page"), ">>"),
            'path': plugin.url_for("lists_trakt_liked_lists", page = int(page) + 1),
            'icon': get_icon_path("item_next"),
            'thumbnail': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/lists/trakt/my_lists')
def lists_trakt_my_lists():
    lists = trakt.trakt_get_lists()
    items = []
    for list in lists:
        name = list["name"]
        user = list["user"]["username"]
        slug = list["ids"]["slug"]
        items.append({
            'label': name,
            'path': plugin.url_for("lists_trakt_show_list", user = user, slug = slug),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_add_all_to_library", user=user, slug=slug))
                ),
                (
                    "{0} ({1})".format(_("Play"), _("Random").lower()),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_play_random", user=user, slug=slug))
                )
            ],
            'icon': get_icon_path("traktmylists"),
            'thumbnail': get_icon_path("traktmylists"),
        })
        fanart = plugin.addon.getAddonInfo('fanart')
        for item in items:
            item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/lists/trakt_search_for_lists')
def lists_trakt_search_for_lists():
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return lists_search_for_lists_term(term, 1)
    else: return

@plugin.route('/lists/search_for_lists_term/<term>/<page>')
def lists_search_for_lists_term(term, page):
    lists, pages = trakt.search_for_list(term, page)
    page = int(page)
    pages = int(pages)
    items = []
    for list in lists:
        if "list" in list:
            list_info = list["list"]
        else:
            continue
        name = list_info["name"]
        user = list_info["username"]
        slug = list_info["ids"]["slug"]
        total = list_info["item_count"]

        info = {}
        info['title'] = name
        if "description" in list_info: info["plot"] = list_info["description"]
        else: info["plot"] = _("No description available")
        if user != None and total != None and total != 0:
            items.append({
                'label': "{0} - {1} ({2})".format(to_utf8(name), to_utf8(user), total),
                'path': plugin.url_for("lists_trakt_show_list", user=user, slug=slug),
                'context_menu': [
                    (
                        _("Scan item to library"),
                        "RunPlugin({0})".format(plugin.url_for("lists_trakt_add_all_to_library", user=user, slug=slug))
                    ),
                   (
                        "{0} ({1})".format(_("Play"), _("Random").lower()),
                        "RunPlugin({0})".format(plugin.url_for("lists_trakt_play_random", user=user, slug=slug))
                    )
                ],
                'info': info,
                'icon': get_icon_path("traktlikedlists"),
                'thumbnail': get_icon_path("traktlikedlists"),
            })
            fanart = plugin.addon.getAddonInfo('fanart')
            for item in items:
                item['properties'] = {'fanart_image' : get_background_path()}
    if pages > page:
        items.append({
            'label': _("Next page").format() + "  >>  (%s/%s)" % (page + 1, pages),
            'path': plugin.url_for("lists_search_for_lists_term", term = term, page=page + 1),
            'icon': get_icon_path("item_next"),
            'thumbnail': get_icon_path("item_next"),
        })
    if FORCE == True: return plugin.finish(items=items, sort_methods=SORT, view_mode=VIEW)
    else: return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/lists/trakt/list_to_library/<user>/<slug>')
def lists_trakt_add_all_to_library(user, slug):
    items = lists_trakt_show_list(user, slug, raw=True)
    misc_ids, movie_ids, tv_ids = batch_find_list_ids(items)
    write_list_id_files(misc_ids, tv_ids, movie_ids, slug, user)
    write_batch_id_files(tv_ids, movie_ids, misc_ids)
    dialogs.notify(msg='Conversion done', title='starting batch-add', delay=3000, image=get_icon_path("metalliq"))
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/movies/batch_add_to_library)")

def batch_find_list_ids(items):
    tv_ids = []
    misc_ids = []
    movie_ids = []
    import_tvdb()
    for item in items:
        if not isinstance(item, type):
            if "'tvdb': " in str(item) or "'tvdb_id': " in str(item):
                if "'tvdb': " in str(item): pre_tvdb = str(item).split("'tvdb': ")
                elif "'tvdb_id': " in str(item): pre_tvdb = str(item).split("'tvdb_id': ")
                if len(pre_tvdb) == 2: pro_tvdb = str(pre_tvdb[1]).split(",")
                elif len(pre_tvdb) == 3: pro_tvdb = str(pre_tvdb[2]).split(",")
                tvdb_id = str(pro_tvdb[0])
                if not tvdb_id or tvdb_id == None or tvdb_id =="None":
                    pre_imdb = str(item).split("u'imdb': u'")
                    pro_imdb = str(pre_imdb[1]).split("'")
                    imdb = str(pro_imdb[0])
                    tvdb_id = tvdb.search_by_imdb(imdb)
                    if not tvdb_id: misc_ids.append(imdb)
                if not tvdb_id in tv_ids and tvdb_id != None and tvdb_id !="None": tv_ids.append(tvdb_id)
            elif "'tmdb': " in str(item):
                pre_tmdb = str(item).split("'tmdb': ")
                pro_tmdb = str(pre_tmdb[1]).split(",")
                tmdb = str(pro_tmdb[0])
                if not tmdb or tmdb == None or tmdb =="None":
                    pre_imdb = str(item).split("u'imdb': u'")
                    pro_imdb = str(pre_imdb[1]).split("'")
                    imdb = str(pro_imdb[0])
                    tvdb_id = tvdb.search_by_imdb(imdb)
                    if not imdb and not tvdb_id:
                        return dialogs.notify(msg="No id found for item", title='', delay=3000, image=get_icon_path("metalliq"))
                    if imdb and not tvdb_id:
                        if imdb not in movie_ids and imdb != None and imdb !="None": movie_ids.append(imdb)
                    elif tvdb_id:
                        if not tvdb_id in tv_ids and tvdb_id != None and tvdb_id !="None": tv_ids.append(tvdb_id)
                if not tmdb in movie_ids and tmdb != None and tmdb !="None": movie_ids.append(tmdb)
        else:
            if "tvshowtitle" in str(item["info"]):
                if item["info"]["tvdb_id"] != None and item["info"]["tvdb_id"] != "" and str(item["info"]["tvdb_id"]) not in tv_ids: tv_ids.append(str(item["info"]["tvdb_id"]))
                elif item["info"]["imdb_id"] != None and item["info"]["imdb_id"] != "" and str(item["info"]["imdb_id"]) not in tv_ids: tv_ids.append(str(item["info"]["imdb_id"]))
            else:
                if item["info"]["tmdb"] != None and item["info"]["tmdb"] != "" and str(item["info"]["tmdb"]) not in movie_ids: movie_ids.append(str(item["info"]["tmdb"]))
                elif item["info"]["imdb_id"] != None and item["info"]["imdb_id"] != "" and str(item["info"]["imdb_id"]) not in movie_ids: movie_ids.append(str(item["info"]["imdb_id"]))
    return misc_ids, movie_ids, tv_ids

def write_list_id_files(misc_ids, tv_ids, movie_ids, slug, user):
    if len(misc_ids) > 0:
        misc_list_file_path = "special://profile/addon_data/plugin.video.metalliq/misc_from_" + slug + "_by_" + user + ".txt"
        if xbmcvfs.exists(misc_list_file_path): os.remove(xbmc.translatePath(misc_list_file_path))
        misc_id_list = ""
        for id in misc_ids:
            misc_id_list = misc_id_list + str(id) + '\n'
        if not xbmcvfs.exists(misc_list_file_path):
            batch_add_file = xbmcvfs.File(misc_list_file_path, 'w')
            batch_add_file.write(misc_id_list)
            batch_add_file.close()
    if len(tv_ids) > 0:
        shows_list_file_path = "special://profile/addon_data/plugin.video.metalliq/shows_from_" + slug + "_by_" + user + ".txt"
        if xbmcvfs.exists(shows_list_file_path): os.remove(xbmc.translatePath(shows_list_file_path))
        tv_id_list = ""
        for id in tv_ids:
            tv_id_list = tv_id_list + str(id) + '\n'
        if not xbmcvfs.exists(shows_list_file_path):
            batch_add_file = xbmcvfs.File(shows_list_file_path, 'w')
            batch_add_file.write(tv_id_list)
            batch_add_file.close()
    if len(movie_ids) > 0:
        movies_list_file_path = "special://profile/addon_data/plugin.video.metalliq/movies_from_" + slug + "_by_" + user + ".txt"
        if xbmcvfs.exists(movies_list_file_path): os.remove(xbmc.translatePath(movies_list_file_path))
        movie_id_list = ""
        for id in movie_ids:
            movie_id_list = movie_id_list + str(id) + '\n'
        if not xbmcvfs.exists(movies_list_file_path):
            batch_add_file = xbmcvfs.File(movies_list_file_path, 'w')
            batch_add_file.write(movie_id_list)
            batch_add_file.close()

def write_batch_id_files(tv_ids, movie_ids, misc_ids):
    if len(tv_ids) > 0:
        shows_import_file_path = "special://profile/addon_data/plugin.video.metalliq/shows_to_add.txt"
        if xbmcvfs.exists(shows_import_file_path): os.remove(xbmc.translatePath(shows_import_file_path))
        tv_id_list = ""
        for id in tv_ids:
            tv_id_list = tv_id_list + str(id) + '\n'
        if not xbmcvfs.exists(shows_import_file_path):
            batch_add_file = xbmcvfs.File(shows_import_file_path, 'w')
            batch_add_file.write(tv_id_list)
            batch_add_file.close()
        dialogs.notify(msg='Converting tvshows, seasons & episodes', title='to id-list for batch-adding', delay=3000, image=get_icon_path("tvshows"))
    if len(movie_ids) > 0:
        movies_import_file_path = "special://profile/addon_data/plugin.video.metalliq/movies_to_add.txt"
        if xbmcvfs.exists(movies_import_file_path): os.remove(xbmc.translatePath(movies_import_file_path))
        movie_id_list = ""
        for id in movie_ids:
            movie_id_list = movie_id_list + str(id) + '\n'
        if not xbmcvfs.exists(movies_import_file_path):
            batch_add_file = xbmcvfs.File(movies_import_file_path, 'w')
            batch_add_file.write(movie_id_list)
            batch_add_file.close()
        dialogs.notify(msg='Converting movies', title='to id-list for batch-adding', delay=3000, image=get_icon_path("movies"))
    if len(misc_ids) > 0:
        misc_import_file_path = "special://profile/addon_data/plugin.video.metalliq/misc_to_add.txt"
        if xbmcvfs.exists(misc_import_file_path): os.remove(xbmc.translatePath(misc_import_file_path))
        misc_id_list = ""
        for id in misc_ids:
            misc_id_list = misc_id_list + str(id) + '\n'
        if not xbmcvfs.exists(misc_import_file_path):
            batch_add_file = xbmcvfs.File(misc_import_file_path, 'w')
            batch_add_file.write(misc_id_list)
            batch_add_file.close()
        dialogs.notify(msg='Converting miscellaneous', title='to id-list for batch-adding', delay=3000, image=get_icon_path("tvshows"))

@plugin.route('/lists/trakt/liked_lists_to_library')
def lists_trakt_add_liked_to_library():
    lists, pages = trakt.trakt_get_liked_lists(1)
    misc_ids = []
    movie_ids = []
    tv_ids = []
    import xbmcgui
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('MetalliQ', 'Creating batch import files')
    for page in range(0, int(pages)):
        lists, ignore = trakt.trakt_get_liked_lists(page)
        list_number = 1
        if (pDialog.iscanceled()): return
        percent = (int(page) / int(pages)) * 100
        pDialog.update(int(percent), '{0} {1} of {2} ...        '.format(_("Scanning for new content"), page, pages))
        for list in lists:
            list_number += 1
            pDialog.update(int(percent), '{0} {1} of {2} ...        '.format(_("Scanning for new content"), page, pages), 'list {0} of {1} on page'.format(list_number, len(lists) + 1))
            info = list["list"]
            user = info["user"]["username"]
            slug = info["ids"]["slug"]
            items = lists_trakt_show_list(user, slug)
            list_misc_ids, list_movie_ids, list_tv_ids = batch_find_list_ids(items)
            write_list_id_files(list_misc_ids, list_movie_ids, list_tv_ids, slug, user)
            misc_ids.extend(list_misc_ids)
            movie_ids.extend(list_movie_ids)
            tv_ids.extend(list_tv_ids)
    pDialog.close()
    write_batch_id_files(tv_ids, movie_ids, misc_ids)
    dialogs.notify(msg='Generating', title='.strm-files', delay=3000, image=get_icon_path("metalliq"))
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/movies/batch_add_to_library)")

@plugin.route('/lists/trakt/my_lists_to_library')
def lists_trakt_add_my_lists_to_library():
    misc_ids = []
    movie_ids = []
    tv_ids = []
    import xbmcgui
    lists = trakt.trakt_get_lists()
    dialogs.notify(msg='Adding ' + str(len(lists)) + " lists", title='to Kodi library', delay=3000, image=get_icon_path("metalliq"))
    for list in lists:
        user = list["user"]["username"]
        slug = list["ids"]["slug"]
        items = lists_trakt_show_list(user, slug)
        list_misc_ids, list_movie_ids, list_tv_ids = batch_find_list_ids(items)
        write_list_id_files(list_misc_ids, list_tv_ids, list_movie_ids, slug, user)
        misc_ids.extend(list_misc_ids)
        movie_ids.extend(list_movie_ids)
        tv_ids.extend(list_tv_ids)
    write_batch_id_files(tv_ids, movie_ids, misc_ids)
    dialogs.notify(msg='Generating', title='.strm-files', delay=3000, image=get_icon_path("metalliq"))
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/movies/batch_add_to_library)")

@plugin.route('/lists/trakt/all_lists_to_library')
def lists_trakt_add_all_lists_to_library():
    lists_trakt_add_liked_to_library()
    lists_trakt_add_my_lists_to_library()

@plugin.route('/lists/trakt/show_list/<user>/<slug>')
def lists_trakt_show_list(user, slug, raw = False):
    list_items = trakt.get_list(user, slug)
    if raw: return list_items
    return _lists_trakt_show_list(list_items)

@plugin.route('/lists/trakt/_show_list/<list_items>')
def _lists_trakt_show_list(list_items):
    genres_dict = trakt.trakt_get_genres("tv")
    if type(list_items) == str:
        import urllib
        list_items = eval(urllib.unquote(list_items))
    items = []
    for list_item in list_items:
        item = None
        item_type = list_item["type"]
        if item_type == "show":
            tvdb_id = list_item["show"]["ids"]["tvdb"]
            if tvdb_id != "" and tvdb_id != None:
                show = list_item["show"]
                info = get_tvshow_metadata_trakt(show, genres_dict)
                context_menu = [
                    (
                        _("Scan item to library"),
                        "RunPlugin({0})".format(plugin.url_for("tv_add_to_library", id=tvdb_id))
                    ),
                    (
                        _("TV show information"), 'Action(Info)'
                    ),
                    (
                        "{0}".format(_("Remove from library").replace(_("Library").lower(),_("Playlist").lower())),
                        "RunPlugin({0})".format(plugin.url_for("lists_remove_show_from_list", src="tvdb", id=tvdb_id))
                    )
                ]
                if plugin.get_setting(SETTING_TRAKT_LIST_ARTWORK, bool) == False:
                    item = ({
                        'label': info['title'],
                        'path': plugin.url_for("tv_tvshow", id=tvdb_id),
                        'context_menu': context_menu,
                        'thumbnail': info['poster'],
                        'icon': get_icon_path("tv"),
                        'poster': info['poster'],
                        'properties' : {'fanart_image' : info['fanart']},
                        'info_type': 'video',
                        'stream_info': {'video': {}},
                        'info': info
                    })
                else: item = make_tvshow_item(info)
            else: item = None
        elif item_type == "season":
            tvdb_id = list_item["show"]["ids"]["tvdb"]
            season = list_item["season"]
            show = list_item["show"]
            show_info = get_tvshow_metadata_trakt(show, genres_dict)
            season_info = get_season_metadata_trakt(show_info,season, genres_dict)
            label = "{0} - Season {1}".format(show["title"],season["number"])
            context_menu = [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("tv_add_to_library", id=tvdb_id))
                ),
                (
                    "%s %s" % (_("Season"), _("Information").lower()), 'Action(Info)'
                ),
                (
                    "{0}".format(_("Remove from library").replace(_("Library").lower(),_("Playlist").lower())),
                    "RunPlugin({0})".format(plugin.url_for("lists_remove_season_from_list", src="tvdb",
                                                           id=tvdb_id, season=list_item["season"]["number"]))
                )
            ]
            item = ({
                'label': label,
                'path': plugin.url_for("tv_season", id=tvdb_id, season_num=list_item["season"]["number"]),
                'context_menu': context_menu,
                'info': season_info,
                'thumbnail': season_info['poster'],
                'icon': get_icon_path("tv"),
                'poster': season_info['poster'],
                'properties': {'fanart_image': season_info['fanart']},
            })
        elif item_type == "episode":
            tvdb_id = list_item["show"]["ids"]["tvdb"]
            episode = list_item["episode"]
            show = list_item["show"]
            season_number = episode["season"]
            episode_number = episode["number"]
            show_info = get_tvshow_metadata_trakt(show, genres_dict)
            episode_info = get_episode_metadata_trakt(show_info, episode)
            label = "{0} - S{1}E{2} - {3}".format(show_info["title"], season_number,
                                                  episode_number, episode_info["title"])
            context_menu = [
                (
                    "{0} {1}...".format(_("Select"), _("Stream").lower()),
                    "PlayMedia({0})".format(
                        plugin.url_for("tv_play", id=tvdb_id, season=season_number,
                                       episode=episode_number, mode='select'))
                ),
                (
                    "%s %s" % (_("Episode"), _("Information").lower()),
                    'Action(Info)'
                ),
                (
                    _("Add to playlist"),
                    "RunPlugin({0})".format(plugin.url_for("lists_add_episode_to_list", src='tvdb', id=tvdb_id,
                                                           season=season_number, episode=episode_number))
                ),
                (
                    "{0}".format(_("Remove from library").replace(_("Library").lower(),_("Playlist").lower())),
                    "RunPlugin({0})".format(plugin.url_for("lists_remove_season_from_list", src="tvdb", id=tvdb_id,
                                                           season=season_number, episode = episode_number))
                )
            ]
            item = ({
                'label': label,
                'path': plugin.url_for("tv_play", id=tvdb_id, season=season_number,
                                       episode=episode_number, mode='default'),
                'context_menu': context_menu,
                'info': episode_info,
                'is_playable': True,
                'info_type': 'video',
                'stream_info': {'video': {}},
                'thumbnail': episode_info['poster'],
                'poster': episode_info['poster'],
                'icon': get_icon_path("tv"),
                'properties': {'fanart_image': episode_info['fanart']},
                })
        elif item_type == "movie":
            movie = list_item["movie"]
            movie_info = get_trakt_movie_metadata(movie)
            try: tmdb_id = movie_info['tmdb']
            except: tmdb_id = ""
            try: imdb_id = movie_info['imdb']
            except: imdb_id = ""
            if tmdb_id != None and tmdb_id != "":
                src = "tmdb"
                id = tmdb_id
            elif imdb_id != None and mdb_id != "":
                src = "imdb"
                id = imdb_id
            else:
                src = ""
                id = ""
            if src == "": item = None
            else:
                if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
                    context_menu = [( _("Scan item to library"), "RunPlugin({0})".format(plugin.url_for("movies_add_to_library", src=src, id=id))), 
                                    ("%s %s" % (_("Movie"), _("Trailer").lower()), "RunScript(script.qlickplay,info=playtrailer,id={0})".format(id)), 
                                    ("[COLOR ff0084ff]Q[/COLOR]lick[COLOR ff0084ff]P[/COLOR]lay", "RunScript(script.qlickplay,info=movieinfo,id={0})".format(id)), 
                                    ("%s %s (%s)" % ("Recommended", _("movies"), "TMDb"), "ActivateWindow(10025,plugin://script.qlickplay/?info=similarmovies&id={0})".format(id))]
                elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
                    context_menu = [( _("Scan item to library"), "RunPlugin({0})".format(plugin.url_for("movies_add_to_library", src=src, id=id))),
                                    ("%s %s" % (_("Movie"), _("Trailer").lower()), "RunScript(script.extendedinfo,info=playtrailer,id={0})".format(id)), (
                                    (_("Extended movie info"),_("Extended movie info"), "RunScript(script.extendedinfo,info=extendedinfo,id={0})".format(id)), 
                                    ("%s %s (%s)" % ("Recommended", _("movies"), "TMDb"), "ActivateWindow(10025,plugin://script.extendedinfo/?info=similarmovies&id={0})".format(id)))]
                else:
                    context_menu = [( _("Scan item to library"), "RunPlugin({0})".format(plugin.url_for("movies_add_to_library", src=src, id=id)))]
                    context_menu.append(("%s %s (%s)" % ("Related", _("movies"), "Trakt"), "ActivateWindow(10025,{0})".format(plugin.url_for("movies_related", id=id, page=1))))
                    context_menu.append(("{0} {1}...".format(_("Select"), _("Stream").lower()), "PlayMedia({0})".format(plugin.url_for("movies_play", src=src, id=id, mode='select'))))
                    context_menu.append((_("Add to playlist"), "RunPlugin({0})".format(plugin.url_for("lists_add_movie_to_list", src=src, id=id))))
                    context_menu.append((_("Movie information"), 'Action(Info)'))
                if imdb_id != None and imdb_id != "":
                    context_menu.append(("Show Actors", "ActivateWindow(10025,{0})".format(plugin.url_for("people_list_movie_people", id=imdb_id, source="imdb", fanart=get_background_path()))))
                elif tmdb_id != None and tmdb_id != "":
                    context_menu.append(("Show Actors", "ActivateWindow(10025,{0})".format(plugin.url_for("people_list_movie_people", id=tmdb_id, source="tmdb", fanart=get_background_path()))))
            item = make_movie_item(movie_info, True)
        elif item_type == "person":
            person_id = list_item['person']['ids']['trakt']
            person_tmdb_id = list_item['person']['ids']['tmdb']
            context_menu= []
            try:
                import_tmdb()
                person_images = tmdb.People(person_tmdb_id).images()['profiles']
                person_image = 'https://image.tmdb.org/t/p/w640' + person_images[0]['file_path']
            except: person_image = ''
            person_name = to_utf8(list_item['person']['name'])
            item = ({
                'label': person_name,
                'path': plugin.url_for("trakt_movies_person", person_id=person_id),
                'context_menu': context_menu,
                #'info': season_info,
                'thumbnail': person_image,
                'icon': get_icon_path("movies"),
                'poster': person_image,
                'properties': {'fanart_image': person_image},
            })
        if item is not None:
            items.append(item)
    for item in items:
        item['properties'] = {'fanart_image' : get_background_path()}
    return items

@plugin.route('/lists/add_movie_to_list/<src>/<id>')
def lists_add_movie_to_list(src, id):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if (src == "tmdb" or src == "trakt"): #trakt seems to want integers unless imdb
            id = int(id)
        data = {
            "movies": [
                {
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.add_to_list(user, slug, data)

@plugin.route('/lists/add_show_to_list/<src>/<id>')
def lists_add_show_to_list(src, id):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if src == "tvdb" or src == "trakt":  # trakt seems to want integers
            id = int(id)
        data = {
            "shows": [
                {
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.add_to_list(user, slug, data)

@plugin.route('/lists/add_season_to_list/<src>/<id>/<season>')
def lists_add_season_to_list(src, id, season):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if src == "tvdb" or src == "trakt":  # trakt seems to want integers
            season = int(season)
            id = int(id)
        data = {
            "shows": [
                {
                    "seasons": [
                        {
                            "number": season,
                        }
                    ],
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.add_to_list(user, slug, data)

@plugin.route('/lists/add_episode_to_list/<src>/<id>/<season>/<episode>')
def lists_add_episode_to_list(src, id, season, episode):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if src == "tvdb" or src == "trakt": #trakt seems to want integers
            season = int(season)
            episode = int(episode)
            id = int(id)
        data = {
                "shows": [
                    {
                        "seasons": [
                            {
                                "number": season,
                                "episodes": [
                                    {
                                        "number": episode
                                    }
                                ]
                            }
                        ],
                        "ids": {
                            src: id
                        }
                    }
                ]
            }
        trakt.add_to_list(user, slug, data)

@plugin.route('/lists/remove_movie_from_list/<src>/<id>')
def lists_remove_movie_from_list(src, id):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if (src == "tmdb" or src == "trakt"):  # trakt seems to want integers unless imdb
            id = int(id)
        data = {
            "movies": [
                {
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.remove_from_list(user, slug, data)

@plugin.route('/lists/remove_show_from_list/<src>/<id>')
def lists_remove_show_from_list(src, id):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if src == "tvdb" or src == "trakt":  # trakt seems to want integers
            id = int(id)
        data = {
            "shows": [
                {
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.remove_from_list(user, slug, data)

@plugin.route('/lists/remove_season_from_list/<src>/<id>/<season>')
def lists_remove_season_from_list(src, id, season):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if src == "tvdb" or src == "trakt":  # trakt seems to want integers
            season = int(season)
            id = int(id)
        data = {
            "shows": [
                {
                    "seasons": [
                        {
                            "number": season,
                        }
                    ],
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.remove_from_list(user, slug, data)

@plugin.route('/lists/remove_episode_from_list/<src>/<id>/<season>/<episode>')
def lists_remove_episode_from_list(src, id, season, episode):
    selected = get_list_selection()
    if selected is not None:
        user = selected['user']
        slug = selected['slug']
        if src == "tvdb" or src == "trakt":  # trakt seems to want integers
            season = int(season)
            episode = int(episode)
            id = int(id)
        data = {
            "shows": [
                {
                    "seasons": [
                        {
                            "number": season,
                            "episodes": [
                                {
                                    "number": episode
                                }
                            ]
                        }
                    ],
                    "ids": {
                        src: id
                    }
                }
            ]
        }
        trakt.remove_from_list(user, slug, data)

def get_list_selection():
    trakt_lists = trakt.trakt_get_lists()
    my_lists = []
    for list in trakt_lists:
        my_lists.append({
            'name': list["name"],
            'user': list["user"]["username"],
            'slug': list["ids"]["slug"]
        })
    selection = dialogs.select(_("Select playlist"), [l["name"] for l in my_lists])
    if selection >= 0:
        return my_lists[selection]
    return None


@plugin.route('/lists/trakt/play_random/<user>/<slug>')
def lists_trakt_play_random(user, slug):
    from meta.utils.playrandom import trakt_play_random
    items = lists_trakt_show_list(user, slug, True)
    trakt_play_random(items)
