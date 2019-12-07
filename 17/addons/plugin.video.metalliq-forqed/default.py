#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import sys, os
    reload(sys)
    sys.setdefaultencoding("utf-8")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))

import os
import time
import shutil
import traceback
import xbmcaddon
from xbmcswift2 import xbmcplugin, xbmcvfs
from meta import plugin
from meta.utils.properties import get_property, set_property, clear_property
from meta.utils.rpc import RPC
from meta.gui import dialogs
from meta.play import updater
from meta.play.base import active_players, get_players, active_channelers
from meta.play.players import get_players, ADDON_SELECTOR
from meta.play.channelers import get_channelers, ADDON_PICKER
from meta.navigation.base import get_icon_path, get_background_path
import meta.navigation.movies
import meta.navigation.tvshows
import meta.navigation.live
import meta.navigation.music
import meta.navigation.lists
import meta.library.tvshows
import meta.library.movies
import meta.library.music
import meta.library.live
from meta.library.tools import channel_inventory, library_inventory
from language import get_string as _
from settings import *
from audiodb import audiodb

FORCE = plugin.get_setting(SETTING_FORCE_VIEW, bool)
VIEW  = plugin.get_setting(SETTING_MAIN_VIEW, int)

addonid = 'plugin.video.metalliq-forqed'

@plugin.route('/')
def root():
    """ Root directory """
    items = [
        {
            'label': _("Movies"),
            'path': plugin.url_for("movies"),
            'icon': get_icon_path("movies"),
            'thumbnail': get_icon_path("movies"),
        },
        {
            'label': _("TV shows"),
            'path': plugin.url_for("tv"),
            'icon': get_icon_path("tv"),
            'thumbnail': get_icon_path("tv"),
        },
        {
            'label': _("Music"),
            'path': plugin.url_for("music"),
            'icon': get_icon_path("music"),
            'thumbnail': get_icon_path("music"),
        },
        {
            'label': _("TV channels"),
            'path': plugin.url_for("live"),
            'icon': get_icon_path("live"),
            'thumbnail': get_icon_path("live"),
        },
        {
            'label': _("Playlists"),
            'path': plugin.url_for("lists"),
            'icon': get_icon_path("lists"),
            'thumbnail': get_icon_path("lists"),
            'context_menu': [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("lists_trakt_add_all_lists_to_library"))
                )
            ],
        },
        {
            'label': _("Enter search string"),
            'path': plugin.url_for("root_search"),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        }
    ]
    fanart = plugin.addon.getAddonInfo('fanart')
    for item in items:
        item['properties'] = {'fanart_image' : get_background_path()}
    if FORCE == True: plugin.set_view_mode(VIEW); return items
    else: return items

@plugin.route('/clear_cache')
def clear_cache():
    """ Clear all caches """
    for filename in os.listdir(plugin.storage_path):
        file_path = os.path.join(plugin.storage_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception, e:
            traceback.print_exc()
    dialogs.notify(msg='Cache', title='Deleted', delay=5000, image=get_icon_path("metalliq"))

@plugin.route('/update_library')
def update_library():
    is_updating = get_property("updating_library")
    is_syncing = get_property("syncing_library")
    now = time.time()
    if is_syncing and now - int(is_syncing) < plugin.get_setting(SETTING_UPDATE_LIBRARY_INTERVAL, int) * 60:
        plugin.log.info("Skipping library sync")
    else:
        if plugin.get_setting(SETTING_LIBRARY_SYNC_COLLECTION, bool) == True or plugin.get_setting(
                SETTING_LIBRARY_SYNC_WATCHLIST, bool) == True:
            try:
                set_property("syncing_library", int(now))
                if plugin.get_setting(SETTING_LIBRARY_SYNC_COLLECTION, bool) == True:
                    meta.library.tvshows.sync_trakt_collection()
                    meta.library.movies.sync_trakt_collection()
                if plugin.get_setting(SETTING_LIBRARY_SYNC_WATCHLIST, bool) == True:
                    meta.library.tvshows.sync_trakt_watchlist()
                    meta.library.movies.sync_trakt_watchlist()
            except: plugin.log.info("something went wrong")
            finally: clear_property("syncing_library")
        else: clear_property("syncing_library")
    if is_updating and now - int(is_updating) < 120:
        plugin.log.debug("Skipping library update")
        return
    if plugin.get_setting(SETTING_LIBRARY_UPDATES, bool) == True:
        try:
            set_property("updating_library", int(now))
            meta.library.tvshows.update_library()
            meta.library.movies.update_library()
            meta.library.music.update_library()
        finally: clear_property("updating_library")
    else: clear_property("updating_library")

@plugin.route('/authenticate_trakt')
def trakt_authenticate():
    from trakt import trakt
    trakt.trakt_authenticate()

@plugin.route('/settings/players/<media>')
def settings_set_players(media):
    playericon = get_icon_path("player")
    medias = ["movies","tvshows","musicvideos","music","live"]
    if media == "all":
        for med in medias:
            mediatype = med.replace('es','e').replace('ws','w').replace('all','').replace('os','o').replace('vs','v s').replace('tv','TV').replace('musicvideo','Music video').replace('live','TV')
            players = get_players(med)
            selected = [p.id for p in players]
            if selected is not None:
                if med == "movies":
                    plugin.set_setting(SETTING_MOVIES_ENABLED_PLAYERS, selected)
                elif med == "tvshows":
                    plugin.set_setting(SETTING_TV_ENABLED_PLAYERS, selected)
                elif med == "musicvideos":
                    plugin.set_setting(SETTING_MUSICVIDEOS_ENABLED_PLAYERS, selected)
                elif med == "music":
                    plugin.set_setting(SETTING_MUSIC_ENABLED_PLAYERS, selected)
                elif med == "live":
                    plugin.set_setting(SETTING_LIVE_ENABLED_PLAYERS, selected)
                else:
                    raise Exception("invalid parameter %s" % media)
            dialogs.notify(msg="{0} {1}".format(_(mediatype).capitalize(), _("Player").lower()), title=_('Enabled'), delay=1000, image=get_icon_path("player"))
        dialogs.notify(msg="{0}".format(_("Player")), title="{0} {1}".format(_("All"), _('Enabled').lower()), delay=1000, image=get_icon_path("player"))
        return True
    elif media == "tvportal":
        players = get_players("live")
        selected = [p.id for p in players]
        plugin.set_setting(SETTING_LIVE_ENABLED_PLAYERS, selected)
        return
    else:
        mediatype = media.replace('es','e').replace('ws','w').replace('all','').replace('os','o').replace('vs','v s').replace('tv','TV').replace('musicvideo','Music video').replace('live','TV')
        players = get_players(media)
        preselected = [p.id for p in active_players(media)]
        players_list = [p.clean_title for p in players]
        if media == "movies":
            players_on = sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_MOVIES_ENABLED_PLAYERS, unicode)])
            players_off = sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_MOVIES_ENABLED_PLAYERS, unicode)])
        elif media == "tvshows":
            players_on = sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_TV_ENABLED_PLAYERS, unicode)])
            players_off = sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_TV_ENABLED_PLAYERS, unicode)])
        elif media == "musicvideos":
            players_on = sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_MUSICVIDEOS_ENABLED_PLAYERS, unicode)])
            players_off = sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_MUSICVIDEOS_ENABLED_PLAYERS, unicode)])
        elif media == "music":
            players_on = sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_MUSIC_ENABLED_PLAYERS, unicode)])
            players_off = sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_MUSIC_ENABLED_PLAYERS, unicode)])
        elif media == "live":
            players_on = sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_LIVE_ENABLED_PLAYERS, unicode)])
            players_off = sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_LIVE_ENABLED_PLAYERS, unicode)])
        players_total = players_off + players_on
        version = xbmc.getInfoLabel('System.BuildVersion')
        selected = None
        msg = "{0}: {1}?".format(_("Enable"), _("All"))
        if dialogs.yesno("{0} {1} ({2} = {3})".format(_("Enable"), _("Player").lower(), _("Type").lower(), _("%s" % mediatype)), msg):
            selected = [p.id for p in players]
        else:
            if int(version[0:2]) > 15:
                result = dialogs.multiselect("{0} {1} ({2} = {3})".format(_("Enable"), _("Player").lower(), _("Type").lower(), _("%s" % mediatype)), players_on + players_off)
                if result is not None: selected = [players[i].id for i in result]
            else:
                enabled = None
                while enabled != -1:
                    dialogs.notify(msg="Back / Close / Escape", title="To confirm, press:", delay=5000, image=get_icon_path("player"))
                    enabled = dialogs.select("[I]{0}[/I]  /  [B]{1}[/B] ".format(_("Disabled"), _("Enabled").lower()), players_off + players_on)
                    if (len(players_off) - 1) >= enabled > -1:
                        players_off.remove(players_total[enabled])
                        players_on.append(players_total[enabled].replace("I]","B]"))
                        players_on = sorted(players_on)
                        players_total = players_off + players_on
                    elif (len(players_total) - 1) >= enabled > (len(players_off) - 1):
                        players_on.remove(players_total[enabled])
                        players_off.append(players_total[enabled].replace("B]","I]"))
                        players_off = sorted(players_off)
                        players_total = players_off + players_on
                selected = [players[players_list.index(i.replace("[B]","").replace("[/B]",""))].id for i in players_on]
        if selected is not None and selected != preselected:
            if media == "movies":
                plugin.set_setting(SETTING_MOVIES_ENABLED_PLAYERS, selected)
            elif media == "tvshows":
                plugin.set_setting(SETTING_TV_ENABLED_PLAYERS, selected)
            elif media == "musicvideos":
                plugin.set_setting(SETTING_MUSICVIDEOS_ENABLED_PLAYERS, selected)
            elif media == "music":
                plugin.set_setting(SETTING_MUSIC_ENABLED_PLAYERS, selected)
            elif media == "live":
                plugin.set_setting(SETTING_LIVE_ENABLED_PLAYERS, selected)
            else:
                raise Exception("invalid parameter %s" % media)
            settings_set_default_player(media)

@plugin.route('/settings/channelers')
def settings_set_channelers():
    medias = ["movies","tvshows","live"]
    for media in medias:
        channelers = get_channelers(media)
        selected = [p.id for p in channelers]
        if selected is not None:
            if media == "movies":
                plugin.set_setting(SETTING_MOVIES_ENABLED_CHANNELERS, selected)
            elif media == "tvshows":
                plugin.set_setting(SETTING_TV_ENABLED_CHANNELERS, selected)
            elif media == "live":
                plugin.set_setting(SETTING_LIVE_ENABLED_CHANNELERS, selected)
            else:
                raise Exception("invalid parameter %s" % media)
    print "MetalliQ Guidance: Movie, TV and Live players enabled"
    return True

@plugin.route('/settings/default_channeler/<media>')
def settings_set_default_channeler(media):
    channelers = active_channelers(media)
    channelers.insert(0, ADDON_PICKER)
    media = media.replace('es','e').replace('ws','w').replace('all','').replace('os','o').replace('vs','v s')
    selection = dialogs.select("{0}".format(_("Select %s") % "{0} {1}".format(_("Default").lower(), _("Player").lower())), [p.title for p in channelers])
    if selection >= 0:
        selected = channelers[selection].id
        if media == "movies":
            plugin.set_setting(SETTING_MOVIES_DEFAULT_CHANNELER, selected)
        elif media == "tvshows":
            plugin.set_setting(SETTING_TV_DEFAULT_CHANNELER, selected)
        elif media == "music":
            plugin.set_setting(SETTING_MUSIC_DEFAULT_CHANNELER, selected)
        elif media == "musicvideos":
            plugin.set_setting(SETTING_MUSICVIDEOS_DEFAULT_CHANNELER, selected)
        elif media == "live":
            plugin.set_setting(SETTING_LIVE_DEFAULT_CHANNELER, selected)
        else:
            raise Exception("invalid parameter %s" % media)

@plugin.route('/settings/default_player/<media>')
def settings_set_default_player(media):
    players = active_players(media)
    players.insert(0, ADDON_SELECTOR)
    selection = dialogs.select("{0}".format(_("Select %s") % "{0} {1}".format(_("Default").lower(), _("Player").lower())), [p.title for p in players])
    if selection >= 0:
        selected = players[selection].id
        if media == "movies":
            plugin.set_setting(SETTING_MOVIES_DEFAULT_PLAYER, selected)
        elif media == "tvshows":
            plugin.set_setting(SETTING_TV_DEFAULT_PLAYER, selected)
        elif media == "music":
            plugin.set_setting(SETTING_MUSIC_DEFAULT_PLAYER, selected)
        elif media == "musicvideos":
            plugin.set_setting(SETTING_MUSICVIDEOS_DEFAULT_PLAYER, selected)
        elif media == "live":
            plugin.set_setting(SETTING_LIVE_DEFAULT_PLAYER, selected)
        else:
            raise Exception("invalid parameter %s" % media)
    plugin.open_settings()

@plugin.route('/settings/default_player_fromlib/<media>')
def settings_set_default_player_fromlib(media):
    players = active_players(media)
    players.insert(0, ADDON_SELECTOR)
    selection = dialogs.select("{0}".format(_("Select %s") % "{0} {1}".format(_("Library").lower(), _("Player").lower())), [p.title for p in players])
    if selection >= 0:
        selected = players[selection].id
        if media == "movies":
            plugin.set_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, selected)
        elif media == "tvshows":
            plugin.set_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, selected)
        elif media == "musicvideos":
            plugin.set_setting(SETTING_MUSICVIDEOS_DEFAULT_PLAYER_FROM_LIBRARY, selected)
        elif media == "music":
            plugin.set_setting(SETTING_MUSIC_DEFAULT_PLAYER_FROM_LIBRARY, selected)
        elif media == "live":
            plugin.set_setting(SETTING_LIVE_DEFAULT_PLAYER_FROM_LIBRARY, selected)
        else:
            raise Exception("invalid parameter %s" % media)
    plugin.open_settings()

@plugin.route('/settings/default_player_fromcontext/<media>')
def settings_set_default_player_fromcontext(media):
    players = active_players(media)
    players.insert(0, ADDON_SELECTOR)
    selection = dialogs.select("{0}".format(_("Select %s") % "{0} {1}".format("context", _("Player").lower())), [p.title for p in players])
    if selection >= 0:
        selected = players[selection].id
        if media == "movies":
            plugin.set_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_CONTEXT, selected)
        elif media == "tvshows":
            plugin.set_setting(SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT, selected)
        elif media == "musicvideos":
            plugin.set_setting(SETTING_MUSICVIDEOS_DEFAULT_PLAYER_FROM_CONTEXT, selected)
        elif media == "music":
            plugin.set_setting(SETTING_MUSIC_DEFAULT_PLAYER_FROM_CONTEXT, selected)
        elif media == "live":
            plugin.set_setting(SETTING_LIVE_DEFAULT_PLAYER_FROM_CONTEXT, selected)
        else:
            raise Exception("invalid parameter %s" % media)
    plugin.open_settings()

@plugin.route('/update_players')
@plugin.route('/update_players/<url>', name='update_players_url')
def update_players(url = None):
    if url is None: url = plugin.get_setting(SETTING_PLAYERS_UPDATE_URL, unicode)
    if updater.update_players(url): dialogs.notify(msg=_('Update'), title=_('Updated for %s') % _('Player'), delay=1000, image=get_icon_path("player"))
    else: dialogs.notify(msg=_('Update'), title=_('Failed for %s') % _('Player'), delay=1000, image=get_icon_path("player"))
    plugin.open_settings()

@plugin.route('/setup/total')
def total_setup():
    dialogs.notify(msg='Total Setup', title=_("Start"), delay=1000, image=get_icon_path("metalliq"))
    if sources_setup() == True: pass
    if players_setup() == True: pass
    dialogs.notify(msg='Total Setup', title=_("Done"), delay=5000, image=get_icon_path("metalliq"))

@plugin.route('/setup/silent')
def silent_setup():
    set_property("running","totalmetalliq")
    movielibraryfolder = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
    try: meta.library.movies.auto_movie_setup(movielibraryfolder)
    except: pass
    tvlibraryfolder = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
    try: meta.library.tvshows.auto_tvshows_setup(tvlibraryfolder)
    except: pass
    musiclibraryfolder = plugin.get_setting(SETTING_MUSIC_LIBRARY_FOLDER, unicode)
    try: meta.library.music.auto_music_setup(musiclibraryfolder)
    except: pass
    livelibraryfolder = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
    try: meta.library.live.auto_live_setup(livelibraryfolder)
    except: pass
    clear_property("running")

@plugin.route('/setup/players')
def players_setup():
    set_property("running","totalmetalliq")
    url = "http://cellardoortv.com/metalliq/players/"
    if updater.update_players(url): dialogs.notify(msg=_('Player'), title=_('Updated for %s') % _('Player'), delay=1000, image=get_icon_path("player"))
    else: dialogs.notify(msg=_('Player'), title=_('Failed for %s') % _('Player'), delay=1000, image=get_icon_path("player"))
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/settings/players/all/)")
    clear_property("running")
    return True

@plugin.route('/setup/sources')
def sources_setup():
    movielibraryfolder = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
    try:
        meta.library.movies.auto_movie_setup(movielibraryfolder)
        dialogs.notify(msg="{0}: {1} {2}".format(_('Movies'), _('Configure'), _("Library").lower()), title=_('Done'), delay=1000, image=get_icon_path("movies"))
    except: dialogs.notify(msg="{0}: {1} {2}".format(_("Movies"), _('Configure'), _("Library").lower()), title=_('Failed for %s') % _('Movies'), delay=1000, image=get_icon_path("movies"))
    tvlibraryfolder = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
    try:
        meta.library.tvshows.auto_tvshows_setup(tvlibraryfolder)
        dialogs.notify(msg="{0}: {1} {2}".format(_('TV shows'), _('Configure'), _("Library").lower()), title=_('Done'), delay=1000, image=get_icon_path("tv"))
    except: dialogs.notify(msg="{0}: {1} {2}".format(_("TV shows"), _('Configure'), _("Library").lower()), title=_('Failed for %s') % _('TV shows'), delay=1000, image=get_icon_path("tv"))
    musiclibraryfolder = plugin.get_setting(SETTING_MUSIC_LIBRARY_FOLDER, unicode)
    try:
        meta.library.music.auto_music_setup(musiclibraryfolder)
        dialogs.notify(msg="{0}: {1} {2}".format(_('Music'), _('Configure'), _("Library").lower()), title=_('Done'), delay=1000, image=get_icon_path("music"))
    except: dialogs.notify(msg="{0}: {1} {2}".format(_("Music"), _('Configure'), _("Library").lower()), title=_('Failed for %s') % _('Music'), delay=1000, image=get_icon_path("music"))
    livelibraryfolder = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
    try:
        meta.library.live.auto_live_setup(livelibraryfolder)
        dialogs.notify(msg="{0}: {1} {2}".format(_('TV'), _('Configure'), _("Library").lower()), title=_('Done'), delay=1000, image=get_icon_path("live"))
    except: dialogs.notify(msg="{0}: {1} {2}".format(_('TV'), _('Configure'), _("Library").lower()), title=_('Failed for %s') % _('TV'), delay=1000, image=get_icon_path("live"))
    return True

@plugin.route('/search')
def root_search():
    term = plugin.keyboard(heading=_("Enter search string"))
    if term != None and term != "": return root_search_term(term)
    else: return

@plugin.route('/search/edit/<term>')
def root_search_edit(term):
    term = plugin.keyboard(default=term, heading=_("Enter search string"))
    if term != None and term != "": return root_search_term(term)
    else: return

@plugin.route('/search_term/<term>', options = {"term": "None"})
def root_search_term(term):
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
            'label': "{0}: '{1}' ({2})".format(_("Search"), term, plugin.addon.getAddonInfo('name')),
            'path': plugin.url_for("root_search_term", term=term, page='1'),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
        {
            'label': "{0} {1}".format(_("Edit"), _("Search string").lower()),
            'path': plugin.url_for("root_search_edit", term=term),
            'icon': get_icon_path("search"),
            'thumbnail': get_icon_path("search"),
        },
    ]
    for item in items:
        item['properties'] = {'fanart_image' : get_background_path()}
    return items

@plugin.route('/toggle/preferred_toggle')
def toggle_preferred_toggle():
    if xbmc.getCondVisibility("Skin.HasSetting(Toggling)") != True: dialogs.notify(msg="Toggling", title="Switched on", delay=5000, image=get_icon_path("metalliq"))
    else: dialogs.notify(msg="Toggling", title="Switched off", delay=5000, image=get_icon_path("metalliq"))
    xbmc.executebuiltin("Skin.ToggleSetting(Toggling)")

@plugin.route('/toggle/context_player')
def toggle_context_player():
    if xbmc.getCondVisibility("Skin.HasSetting(Contexting)") != True: dialogs.notify(msg="Context player", title="Switched off", delay=5000, image=get_icon_path("metalliq"))
    else: dialogs.notify(msg="Context player", title="Switched on", delay=5000, image=get_icon_path("metalliq"))
    xbmc.executebuiltin("Skin.ToggleSetting(Contexting)")

@plugin.route('/toggle/acceleration')
def toggle_hardware_acceleration():
    if xbmc.getCondVisibility("System.Platform.Android") == 1:
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.useamcodec"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.useamcodec","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.useamcodec"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.useamcodec","value":true}, "id":1}')
        else: pass
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usestagefright"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usestagefright","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usestagefright"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usestagefright","value":true}, "id":1}')
        else: pass
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usemediacodec"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usemediacodec","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usemediacodec"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usemediacodec","value":true}, "id":1}')
        else: pass
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usemediacodecsurface"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usemediacodecsurface","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usemediacodecsurface"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usemediacodecsurface","value":true}, "id":1}')
        else: pass
    if xbmc.getCondVisibility("System.Platform.Linux.RaspberryPi") == 1:
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.useomxplayer"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.useomxplayer","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.useomxplayer"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.useomxplayer","value":true}, "id":1}')
        else: pass
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usemmal"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usemmal","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usemmal"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usemmal","value":true}, "id":1}')
        else: pass
    if xbmc.getCondVisibility("System.Platform.Windows") == 1:
        response = xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usedxva2"}, "id":1}')
        if xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usedxva2"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":true}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usedxva2","value":false}, "id":1}')
        elif xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"videoplayer.usedxva2"}, "id":1}') == '{"id":1,"jsonrpc":"2.0","result":{"value":false}}': xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"videoplayer.usedxva2","value":true}, "id":1}')
        else: pass

@plugin.route('/toggle/skin')
def toggle_between_skins():
    if xbmc.getCondVisibility("Skin.HasSetting(Contexting)") != True: contexting = False
    else: contexting = True
    if xbmc.getCondVisibility("Skin.HasSetting(Toggling)") != True: toggling = False
    else: toggling = True
    current_skin = str(xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"lookandfeel.skin"}, "id":1}')).replace('{"id":1,"jsonrpc":"2.0","result":{"value":"','').replace('"}}','')
    primary_skin = plugin.get_setting(SETTING_PRIMARY_SKIN, unicode)
    if primary_skin == "": plugin.set_setting(SETTING_PRIMARY_SKIN, current_skin)
    alternate_skin = plugin.get_setting(SETTING_ALTERNATE_SKIN, unicode)
    if alternate_skin == "":
        if primary_skin != "skin.confluence" and primary_skin != "": plugin.set_setting(SETTING_ALTERNATE_SKIN, "skin.confluence")
        else:
            dialogs.notify(msg="Alternate skin", title="Not set", delay=5000, image=get_icon_path("metalliq"))
            return openSettings(addonid, 5.7)
    if primary_skin != alternate_skin and primary_skin != "" and alternate_skin != "" and xbmc.getCondVisibility('System.HasAddon(%s)' % primary_skin) and xbmc.getCondVisibility('System.HasAddon(%s)' % alternate_skin):
        if current_skin != primary_skin:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"lookandfeel.skin","value":"%s"}, "id":1}' % primary_skin)
            xbmc.executebuiltin('SetFocus(11)')
            xbmc.executebuiltin('Action(Select)')
        else:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"lookandfeel.skin","value":"%s"}, "id":1}' % alternate_skin)
            xbmc.executebuiltin('SetFocus(11)')
            xbmc.executebuiltin('Action(Select)')
        xbmc.sleep(2000)
        if contexting == False and xbmc.getCondVisibility("Skin.HasSetting(Contexting)") == True: toggle_context_player()
        elif contexting == True and xbmc.getCondVisibility("Skin.HasSetting(Contexting)") == False: toggle_context_player()
        else: pass
        if toggling == False and xbmc.getCondVisibility("Skin.HasSetting(Toggling)") == True: toggle_preferred_toggle()
        elif toggling == True and xbmc.getCondVisibility("Skin.HasSetting(Toggling)") == False: toggle_preferred_toggle()
        else: pass

@plugin.route('/export')
def export_library():
    export_movies_library()
    export_tv_library()

@plugin.route('/export/movies')
def export_movies_library():
    folder_path = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
    if not xbmcvfs.exists(folder_path): return dialogs.notify(msg='Movies folder', title='Absent', delay=5000, image=get_icon_path("movies"))
    ids = ""
    movies = xbmcvfs.listdir(folder_path)[0]
    if len(movies) < 1: return dialogs.notify(msg='Movies folder', title='Empty', delay=5000, image=get_icon_path("movies"))
    else :
        for movie in movies: ids = ids + str(movie) + '\n'
    movies_backup_file_path = "special://profile/addon_data/plugin.video.metalliq-forqed/movies_to_add.bak"
    if xbmcvfs.exists(movies_backup_file_path): os.remove(xbmc.translatePath(movies_backup_file_path))
    if not xbmcvfs.exists(movies_backup_file_path):
        batch_add_file = xbmcvfs.File(movies_backup_file_path, 'w')
        batch_add_file.write(ids)
        batch_add_file.close()
    dialogs.notify(msg="Movies", title="Backed up", delay=5000, image=get_icon_path("movies"))

@plugin.route('/export/tv')
def export_tv_library():
    folder_path = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
    if not xbmcvfs.exists(folder_path): return dialogs.notify(msg='TVShows folder', title='Absent', delay=5000, image=get_icon_path("tv"))
    ids = ""
    shows = xbmcvfs.listdir(folder_path)[0]
    if len(shows) < 1: return dialogs.notify(msg='TVShows folder', title='Empty', delay=5000, image=get_icon_path("tv"))
    else :
        for show in shows: ids = ids + str(show) + '\n'
    shows_backup_file_path = "special://profile/addon_data/plugin.video.metalliq-forqed/shows_to_add.bak"
    if xbmcvfs.exists(shows_backup_file_path): os.remove(xbmc.translatePath(shows_backup_file_path))
    if not xbmcvfs.exists(shows_backup_file_path):
        batch_add_file = xbmcvfs.File(shows_backup_file_path, 'w')
        batch_add_file.write(ids)
        batch_add_file.close()
    dialogs.notify(msg="TVShows", title="Backed up", delay=5000, image=get_icon_path("tv"))

@plugin.route('/play/<label>')
def play_by_label(label):
    types = [_("Movies"), _("TV shows"), _("Channels")]
    selection = dialogs.select("{0} {1}".format(_("Choose"), _("Type").lower()), [item for item in types])
    if selection   == 0: xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/play_by_name/{0}/en)".format(label))
    elif selection == 1: xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/tv/play_by_name_only/{0}/en)".format(label))
    elif selection == 2: xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/live/{0}/None/en/context)".format(label))

@plugin.route('/cleartrakt')
def clear_trakt():
    msg = "{0} {1} {2}?".format(_("Remove"), "Trakt", _("Settings").lower())
    if dialogs.yesno("{0} {1}".format(_("Unlock"), "Trakt"), msg):
        plugin.set_setting(SETTING_TRAKT_ACCESS_TOKEN, "")
        plugin.set_setting(SETTING_TRAKT_REFRESH_TOKEN, "")
        plugin.set_setting(SETTING_TRAKT_EXPIRES_AT, "")

@plugin.route('/cleartraktcache')
def clear_trakt_cache():
    for filename in os.listdir(plugin.storage_path):
        if filename == "trakt":
            try:
                if os.path.isfile(file_path): os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception, e: traceback.print_exc()



@plugin.route('/printjson/<path>')
def printjson(path):
    response = RPC.files.get_directory(media="files", directory="plugin://plugin.video.crackler/?foldername=Movies&mode=movies_folder", properties=["title","artist","albumartist","genre","year","rating","album","track","duration","comment","lyrics","musicbrainztrackid","musicbrainzartistid","musicbrainzalbumid","musicbrainzalbumartistid","playcount","fanart","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","writer","studio","mpaa","cast","country","imdbnumber","premiered","productioncode","runtime","set","showlink","streamdetails","top250","votes","firstaired","season","episode","showtitle","thumbnail","file","resume","artistid","albumid","tvshowid","setid","watchedepisodes","disc","tag","art","genreid","displayartist","albumartistid","description","theme","mood","style","albumlabel","sorttitle","episodeguide","uniqueid","dateadded","size","lastmodified","mimetype"])
    xbmc.log("QQQQQ plugin://%s = %s" % (path.replace("%2f", "/"), str(response)))

@plugin.route('/mapall')
def mapall():
    exclusions = ["plugin.audio.dradio","plugin.audio.mixcloud","plugin.image.dilbert","plugin.video.chefkoch_de","plugin.video.goldpagemedia","plugin.video.youtube","plugin.audio.booksshouldbefree","plugin.audio.jambmc","plugin.video.7tv",]
    dones = ["plugin.audio.abradio.cz","plugin.audio.cherrymusic","plugin.audio.deejayIt.reloaded","plugin.audio.detektorfm","plugin.audio.di.fm","plugin.audio.diyfm","plugin.audio.dr.dk.netradio","plugin.audio.groove","plugin.audio.hongkongradio","plugin.audio.icecast","plugin.audio.internet.archive","plugin.audio.jazzradio.com","plugin.audio.listenliveeu","plugin.audio.modland","plugin.audio.mozart","plugin.audio.nectarine","plugin.audio.npr","plugin.audio.podcatcher","plugin.audio.qobuz","plugin.audio.radioma","plugin.audio.radiotunes.com","plugin.audio.radio_de","plugin.audio.rainymood.com","plugin.audio.ramfm","plugin.audio.rautemusik","plugin.audio.rdio","plugin.audio.releasefm","plugin.audio.relive","plugin.audio.shoutcast","plugin.audio.rockradio.com","plugin.audio.sgradio",]
    audio_addons = ["plugin.audio.abcradionational", "plugin.audio.abradio.cz", "plugin.audio.booksshouldbefree", "plugin.audio.cherrymusic", "plugin.audio.deejayIt.reloaded", "plugin.audio.detektorfm", "plugin.audio.di.fm", "plugin.audio.diyfm", "plugin.audio.dr.dk.netradio", "plugin.audio.dradio", "plugin.audio.groove", "plugin.audio.hongkongradio", "plugin.audio.icecast", "plugin.audio.internet.archive", "plugin.audio.jambmc", "plugin.audio.jazzradio.com", "plugin.audio.listenliveeu", "plugin.audio.mixcloud", "plugin.audio.modland", "plugin.audio.mozart", "plugin.audio.nectarine", "plugin.audio.npr", "plugin.audio.podcatcher", "plugin.audio.qobuz", "plugin.audio.radioma", "plugin.audio.radiotunes.com", "plugin.audio.radio_de", "plugin.audio.rainymood.com", "plugin.audio.ramfm", "plugin.audio.rautemusik", "plugin.audio.rdio", "plugin.audio.releasefm", "plugin.audio.relive", "plugin.audio.resetradio", "plugin.audio.rne", "plugin.audio.rockradio.com", "plugin.audio.sgradio", "plugin.audio.shoutcast", "plugin.audio.somafm", "plugin.audio.soundcloud", "plugin.audio.sverigesradio", "plugin.audio.tilos", "plugin.audio.tripler", "plugin.audio.vgpodcasts", "plugin.audio.wimp"]
    misc_addons = ["plugin.dbmc", "plugin.onedrive", "plugin.picture.bromix.break", "plugin.program.isybrowse", "plugin.program.jdownloader", "plugin.program.mceremote", "plugin.program.newgrounds", "plugin.program.rpcalendar", "plugin.program.super.favourites", "plugin.program.tvhighlights", "plugin.program.utorrent", "plugin.program.video.node.editor", "plugin.program.wienerlinien", "plugin.programm.xbmcmail"]
    image_addons = ["plugin.image.500px", "plugin.image.cheezburger_network", "plugin.image.cyanidehappiness", "plugin.image.dilbert", "plugin.image.flickr", "plugin.image.garfield", "plugin.image.google", "plugin.image.iphoto", "plugin.image.jpfoto", "plugin.image.moebooru", "plugin.image.xkcd", "plugin.image.xzen"]
    video_addons_take_too_long = ["plugin.video.clipfish.de", "plugin.video.7tv", "plugin.video.ardmediathek_de", "plugin.video.7tv", "plugin.video.ardmediathek_de", "plugin.video.comingsoon.it", "plugin.video.corbettreport", "plugin.video.espn_3", ] 
    video_addons_exclusions = ["plugin.video.docu", ] 
    video_addons_done = ["plugin.video.3bmeteo", "plugin.video.4players", "plugin.video.9gagtv", "plugin.video.abcradionational", "plugin.video.amaproracing", "plugin.video.ansa", "plugin.video.arretsurimages", "plugin.video.arteplussept", "plugin.video.arte_tv", "plugin.video.attactv", "plugin.video.borsentv.dk", "plugin.video.botchamania", "plugin.video.br3", "plugin.video.break_com", "plugin.video.btbn", "plugin.video.cessfull", "plugin.video.cnet.podcasts", "plugin.video.codigofacilito.com", "plugin.video.collegehumor", "plugin.video.comicvine", "plugin.video.confreaks", "plugin.video.corrieretv", "plugin.video.couchpotato_manager", "plugin.video.crackler", "plugin.video.creationtoday_org", "plugin.video.crunchyroll-takeout", "plugin.video.d17", "plugin.video.d8", "plugin.video.deredactie", "plugin.video.disclose_tv", "plugin.video.disneychannel_de", "plugin.video.dmax", "plugin.video.dmax_de", "plugin.video.dmi.dk", "plugin.video.dokumonster", "plugin.video.dr.dk.bonanza", "plugin.video.dr.dk.live", "plugin.video.dr.dk.podcast", "plugin.video.drnu", "plugin.video.dumpert", "plugin.video.dzango.tv", "plugin.video.earthtouch", "plugin.video.eevblog", "plugin.video.ekkofilm.dk", "plugin.video.elisa.viihde", "plugin.video.engadget", "plugin.video.enigmatv", "plugin.video.eredivisie-live", "plugin.video.esa", "plugin.video.eso", ] 
    video_addons = ["plugin.video.crackler"]
    video_addonsb = ["plugin.video.eyetv.parser", "plugin.video.fattoquotidianotv", "plugin.video.fernsehkritik", "plugin.video.filmarkivet", "plugin.video.filmsforaction", "plugin.video.floptv", "plugin.video.focus-online.de", "plugin.video.fox.news", "plugin.video.gaffa.tv", "plugin.video.gamegurumania", "plugin.video.gamestar", "plugin.video.geekandsundry", "plugin.video.gfq", "plugin.video.giantbomb", "plugin.video.glwiz", "plugin.video.godtube_com", "plugin.video.goldpagemedia", "plugin.video.golem.de", "plugin.video.gq", "plugin.video.greenpeace", "plugin.video.gronkh.de", "plugin.video.guardian", "plugin.video.hallmark", "plugin.video.hdtrailers_net", "plugin.video.heritagechannel", "plugin.video.hgtv", "plugin.video.hgtv.canada", "plugin.video.hollywoodreporter", "plugin.video.ign_com", "plugin.video.ilmeteo", "plugin.video.infowars", "plugin.video.iplayerwww", "plugin.video.irishtv", "plugin.video.itbn_org", "plugin.video.itunes_podcasts", "plugin.video.jeuxvideo.com", "plugin.video.johnlocker", "plugin.video.jupiterbroadcasting", "plugin.video.jwtv-unofficial", "plugin.video.khanacademy", "plugin.video.kino.dk", "plugin.video.kordkutters", "plugin.video.lachschon_de", "plugin.video.lacosa", "plugin.video.latelelibre_fr", "plugin.video.livestream", "plugin.video.manoto", "plugin.video.massengeschmack", "plugin.video.media-ccc-de", "plugin.video.mediacorp", "plugin.video.metacafe", "plugin.video.metalliq-forqed", "plugin.video.metalvideo", "plugin.video.mk", "plugin.video.mlg.tv", "plugin.video.mms", "plugin.video.moontv.fi", "plugin.video.mtv.it", "plugin.video.mtv_de", "plugin.video.musicvideojukebox_net", "plugin.video.mycanal", "plugin.video.mytv_bg", "plugin.video.myvevo", "plugin.video.myvideo_de", "plugin.video.nasa", "plugin.video.nbcsnliveextra", "plugin.video.nederland24", "plugin.video.netzkino_de", "plugin.video.nfl-teams", "plugin.video.nfl.com", "plugin.video.nfl.gamepass", "plugin.video.nhl-gamecenter-live", "plugin.video.nick_de", "plugin.video.nlhardwareinfo", "plugin.video.noco", "plugin.video.nolife", "plugin.video.nos", "plugin.video.npr", "plugin.video.nrk", "plugin.video.nrwision", "plugin.video.nytimes", "plugin.video.on_aol", "plugin.video.orftvthek", "plugin.video.oxygen", "plugin.video.pcloud-video-streaming", "plugin.video.photocasts", "plugin.video.pinkbike", "plugin.video.pixel.tv", "plugin.video.popcornflix", "plugin.video.popcorntv", "plugin.video.powerunlimited", "plugin.video.previewnetworks", "plugin.video.puls4", "plugin.video.putio", "plugin.video.radbox", "plugin.video.railscasts", "plugin.video.raitv", "plugin.video.realtimetvitalia", "plugin.video.reddit_tv", "plugin.video.retro_tv", "plugin.video.roosterteeth", "plugin.video.rt", "plugin.video.rtlxl", "plugin.video.rtpplay", "plugin.video.rts", "plugin.video.s04tv", "plugin.video.sagetv", "plugin.video.sapo", "plugin.video.sarpur", "plugin.video.schaetzederwelt", "plugin.video.science.friday", "plugin.video.serviziopubblico", "plugin.video.servustv_com", "plugin.video.sgtv", "plugin.video.si", "plugin.video.skytg24", "plugin.video.smithsonian", "plugin.video.snagfilms", "plugin.video.southpark_unofficial", "plugin.video.spiegel_tv", "plugin.video.sportube", "plugin.video.sprout", "plugin.video.spurs-tv", "plugin.video.srf_podcast_ch", "plugin.video.supertennis", "plugin.video.svtplay", "plugin.video.tagen.tv", "plugin.video.tagesschau", "plugin.video.tagesschauvideoblog", "plugin.video.ted.talks", "plugin.video.tekthing", "plugin.video.testtube", "plugin.video.theblaze", "plugin.video.thenewboston", "plugin.video.time_com", "plugin.video.tlc_de", "plugin.video.tmos", "plugin.video.toonjet", "plugin.video.trailer.addict", "plugin.video.trakt_list_manager", "plugin.video.travel", "plugin.video.tv2.dk", "plugin.video.tv2regionerne.dk", "plugin.video.tv3.cat", "plugin.video.tv3play.dk", "plugin.video.tvkc", "plugin.video.tvo", "plugin.video.tvokids", "plugin.video.tvvn", "plugin.video.tweakers", "plugin.video.twit", "plugin.video.udacity", "plugin.video.ukmvjb", "plugin.video.uzg", "plugin.video.vgtv", "plugin.video.videobash_com", "plugin.video.videovideo.dk", "plugin.video.viewster", "plugin.video.vimcasts", "plugin.video.vimeo", "plugin.video.vine", "plugin.video.virginradio.it", "plugin.video.vitaminl_tv", "plugin.video.voapersian", "plugin.video.vvvvid", "plugin.video.wabc", "plugin.video.watchmojo", "plugin.video.watson", "plugin.video.welt_der_wunder", "plugin.video.wimp", "plugin.video.wnbc", "plugin.video.worldstarhiphop", "plugin.video.wsj", "plugin.video.yogaglo", "plugin.video.youtube", "plugin.video.zattoobox", "plugin.video.zdf_de_lite", "plugin.video.zeemarathi", "plugin.video.zeetv"]
    i = 0
    for item in video_addons:
        if xbmc.getCondVisibility("System.HasAddon(%s)" % item):
            itemthread = threading.Thread(target=test(item, 2))
            itemthread.start()

@plugin.route('/test/<id>/<maxdepth>')
def test(id, maxdepth):
    try: maxdepth = int(maxdepth)
    except: return
    dialogs.notify(msg='MaxDepth = %d' % maxdepth, title='Id = %s' % id, delay=5000, image=get_icon_path("metalliq"))
    import xbmcaddon
    import re
    from rpc import RPC
    INFOTYPES = ["author", "changelog", "description", "disclaimer", "fanart", "icon", "id", "name", "path", "profile", "stars", "summary", "type", "version"]
    ADDON = xbmcaddon.Addon(id)
    addon_info_string = ""
    for infotype in INFOTYPES: 
        addon_info_string += "# %-11s = %s\n" % (infotype, ADDON.getAddonInfo(infotype).replace("14.o\\portable_data\\",""))
    base = u'plugin://{0}/'.format(id)
    dirs_total = [u'plugin://{0}/'.format(id)]
    dirs_done = [u'plugin://{0}/'.format(id)]
    dirs_labels = [u'{0}'.format(re.sub(r'\[[^)].*?\]', '', ADDON.getAddonInfo("name")))]
    dirs_thumbs = [u'{0}'.format(re.sub(r'\[[^)].*?\]', '', ADDON.getAddonInfo("icon")))]
    dirs_backgr = [u'{0}'.format(re.sub(r'\[[^)].*?\]', '', ADDON.getAddonInfo("fanart")))]
    streams = {}
    depth = 0
    file_labels = []
    file_labels_raw = []
    response = RPC.files.get_directory(media="files", directory=base, properties=["thumbnail","fanart","description","plot","art"])
    if "files" in response:
        files = response["files"]
        links = {}
        thumbnails = {}
        backgrounds = {}
        descriptions = {}
        streams[base] = {}
        for f in files:
            if f["filetype"] == "directory":
                if f["file"] not in dirs_total:
                    dirs_total.append(f["file"])
                    if f["thumbnail"]: dirs_thumbs.append(f["thumbnail"])
                    else: dirs_thumbs.append("")
                    if f["fanart"]: dirs_thumbs.append(f["fanart"])
                    else: dirs_backgr.append("")
                    label = re.sub(r'\[[^)].*?\]', '', f["label"])
                    dirs_labels.append(label)
            if f["filetype"] == "file":
                file_labels_raw.append(f["label"])
                label = re.sub(r'\[[^)].*?\]', '', f["label"])
                file = f["file"]
                while (label in links):
                    label = "%s." % label
                links[label] = file
                if f["art"]: thumbnails[label] = f["art"] 
                elif f["thumbnail"]: thumbnails[label] = f["thumbnail"]
                else: thumbnails[label] = ""
                backgrounds[label] = f["fanart"]
                if "description" in response: descriptions[label] = f["description"].replace(" ", "+").replace('"', '&quot;').replace("'", "&apos;").replace(",", "%2c")
                elif "plot" in response: descriptions[label] = f["plot"].replace(" ", "+").replace('"', '&quot;').replace("'", "&apos;").replace(",", "%2c")
                else: descriptions[label] = ""
                file_labels.append(label)
    elif not 'error' in response: pass
    else: return
    while len(dirs_total) > len(dirs_done) and depth != maxdepth:
        depth = depth + 1
        dialogs.notify(msg='Depth', title='%d' % depth, delay=5000, image=get_icon_path("metalliq"))
        dirs = [x for x in dirs_total if x not in dirs_done and "search" not in x and "personal" not in x]
        for d in dirs:
            response = RPC.files.get_directory(media="files", directory=d, properties=["thumbnail","fanart","description","plot"])
            dirs_done.append(d)
            if "files" not in response: pass
            elif not 'error' in response:
                files = response["files"]
                links = {}
                thumbnails = {}
                backgrounds = {}
                descriptions = {}
                streams[d] = {}
                for f in files:
                    if f["filetype"] == "file":
                        if "/default" in f["file"]: pass
                        else:
                            file_labels_raw.append(f["label"])
                            label = re.sub(r'\[[^)].*?\]', '', f["label"])
                            label = label.strip(" ").replace("Stream - ", "").replace("stream - ", "")
                            file = f["file"]
                            while (label in links):
                                label = "%s.." % label
                            links[label] = file
                            if f["thumbnail"]: thumbnails[label] = f["thumbnail"]
                            else: thumbnails[label] = "http%3a%2f%2fmirrors.kodi.tv%2faddons%2fhelix%2f{0}%2ficon.png".format(ADDON.getAddonInfo("id"))
                            if f["fanart"]: backgrounds[label] = f["fanart"]
                            else: backgrounds[label] = "http%3a%2f%2fmirrors.kodi.tv%2faddons%2fhelix%2f{0}%2ffanart.jpg".format(ADDON.getAddonInfo("id"))
                            if "description" in response: descriptions[label] = f["description"]
                            else: descriptions[label] = ""
                            streams[d][label] = file
                            file_labels.append(label)
                    if f["filetype"] == "directory":
                        if "personal" in f["file"]: pass
                        else:
                            if f["file"] not in dirs_total:
                                dirs_total.append(f["file"])
                                label = re.sub(r'\[[^)].*?\]', '', f["label"])
                                dirs_labels.append(label)
                                if f["thumbnail"]: dirs_thumbs.append(f["thumbnail"])
                                else: dirs_thumbs.append("http%3a%2f%2fmirrors.kodi.tv%2faddons%2fhelix%2f{0}%2ficon.png".format(ADDON.getAddonInfo("id")))
                                if f["fanart"]: dirs_thumbs.append(f["fanart"])
                                else: dirs_thumbs.append("http%3a%2f%2fmirrors.kodi.tv%2faddons%2fhelix%2f{0}%2ffanart.jpg".format(ADDON.getAddonInfo("id")))
            else: pass
        if depth == maxdepth: break
    id_folder = xbmc.translatePath("special://profile/addon_data/plugin.program.super.favourites/Super Favourites/{0}/".format(ADDON.getAddonInfo("id")))
    name_folder = xbmc.translatePath("special://profile/addon_data/plugin.program.super.favourites/Super Favourites/{0}/".format(ADDON.getAddonInfo("name")))
    if not xbmcvfs.exists(id_folder): xbmcvfs.mkdir(id_folder)
    if not xbmcvfs.exists(name_folder): xbmcvfs.mkdir(name_folder)
    #id_file = "%-36s (%s)%s" % (ADDON.getAddonInfo("id"), ADDON.getAddonInfo("name"), ".ini")
    id_file = "%s (%s)%s" % (ADDON.getAddonInfo("id"), ADDON.getAddonInfo("name"), ".ini")
    name_file = "%s (%s)%s" % (ADDON.getAddonInfo("name"), ADDON.getAddonInfo("id"), ".ini")
    id_filename = os.path.join(id_folder, id_file)
    name_filename = os.path.join(name_folder, name_file)
    f = xbmcvfs.File(id_filename,"wb")
    g = xbmcvfs.File(name_filename,"wb")
    line = '%s' % addon_info_string
    f.write(line.encode("utf8"))
    g.write(line.encode("utf8"))
    for d in sorted(streams):
        num = dirs_total.index(d)
        line = '\n\n_dirs["{0}"] = {1}\n'.format(dirs_labels[num] , d)
        f.write(line.encode("utf8"))
        g.write(line.encode("utf8"))
        channels = streams[d]
        for channel in sorted(channels):
            url = channels[channel]
            if not channel.endswith(".."): label = channel
            elif channel.endswith(".."):
                ows = channel.count('..')
                prelabel = channel.rstrip("..")
                fws = prelabel.count('..')
                label = "{0} ({1})".format(prelabel, ows - fws)
            line = '\n_streams["%s"] = %s' % (label.replace('"','\\\"'), url)
            f.write(line.encode("utf8"))
            g.write(line.encode("utf8"))
    dirs_not_done = [x for x in dirs_total if x not in dirs_done]
    if len(dirs_not_done) > 0:
        f.write("\n\ndirs_not_done=")
        g.write("\n\ndirs_not_done=")
        line = str(dirs_not_done)
        f.write(line.encode("utf8"))
        g.write(line.encode("utf8"))
    f.close()
    g.close()

    #id_file = "%-36s (%s)%s" % (ADDON.getAddonInfo("id"), ADDON.getAddonInfo("name"), ".m3u")
    id_file = "%s (%s)%s" % (ADDON.getAddonInfo("id"), ADDON.getAddonInfo("name"), ".m3u")
    name_file = "%s (%s)%s" % (ADDON.getAddonInfo("name"), ADDON.getAddonInfo("id"), ".m3u")
    id_filename = os.path.join(id_folder, id_file)
    name_filename = os.path.join(name_folder, name_file)
    f = xbmcvfs.File(id_filename,"wb")
    g = xbmcvfs.File(name_filename,"wb")
    line = '#EXTM3U\n\n%s' % addon_info_string
    f.write(line.encode("utf8"))
    g.write(line.encode("utf8"))
    if "plugin.audio" in ADDON.getAddonInfo("id"): radio = ' radio="true"'
    else: radio = ''
    for d in sorted(streams):
        num = dirs_total.index(d)
        channels = streams[d]
        for channel in sorted(channels):
            url = channels[channel]
            try: thumb = thumbnails[channel]
            except: thumb = "http%3a%2f%2fmirrors.kodi.tv%2faddons%2fhelix%2f{0}%2ficon.png".format(ADDON.getAddonInfo("id"))
            if not channel.endswith(".."): label = channel
            elif channel.endswith(".."):
                ows = channel.count('..')
                prelabel = channel.rstrip("..")
                fws = prelabel.count('..')
                label = "{0} ({1})".format(prelabel, ows - fws)
            line = '\n#EXTINF:-1 tvg-id="{0}" tvg-name="{0}" tvg-logo="{1}" group-title="{2}"{3},{0}\n{4}'.format(label.replace(',',' -').replace('"','\''), thumb, ADDON.getAddonInfo("name").replace(',',' -'), radio, url)
            f.write(line.encode("utf8"))
            g.write(line.encode("utf8"))
    f.close()
    g.close()
    file = "favourites.xml"
    id_filename = os.path.join(id_folder, file)
    name_filename = os.path.join(name_folder, file)
    f = xbmcvfs.File(id_filename,"wb")
    g = xbmcvfs.File(name_filename,"wb")
    line = "<favourites>"
    f.write(line.encode("utf8"))
    g.write(line.encode("utf8"))
    for d in sorted(streams):
        num = dirs_total.index(d)
        channels = streams[d]
        for channel in sorted(channels):
            url = channels[channel]
            try: thumb = thumbnails[channel].rstrip("/")
            except: thumb = "http://mirrors.kodi.tv/addons/helix/{0}/icon.png".format(ADDON.getAddonInfo("id")).rstrip("/")
            if "image://" in thumb:
                thumb = thumb.replace("image://","").replace("%3a",":").replace("%2f","/").replace("%5c","\\")
                thumb = thumb.replace(ADDON.getAddonInfo("icon").replace("icon.png",""), "special://home/addons/{0}/".format(ADDON.getAddonInfo("id"))).replace("\\","/")
            try: fanart = backgrounds[channel]
            except: fanart = "http://mirrors.kodi.tv/addons/helix/{0}/fanart.jpg".format(ADDON.getAddonInfo("id"))
            if "image://" in fanart:
                fanart = fanart.replace("image://","").replace("%3a",":").replace("%2f","/").replace("%5c","\\")
                fanart = fanart.replace(ADDON.getAddonInfo("icon").replace("icon.png",""), "special://home/addons/{0}/".format(ADDON.getAddonInfo("id"))).replace("\\","/")
            try: description = descriptions[channel]
            except: description = ""
            if not channel.endswith(".."): label = channel
            elif channel.endswith(".."):
                ows = channel.count('..')
                prelabel = channel.rstrip("..")
                fws = prelabel.count('..')
                label = "{0} ({1})".format(prelabel, ows - fws)
#            prethumb = url.split("v_id=")[1]
#            line = '\n    <favourite name="{0}" thumb="http://images-us-az.crackle.com/profiles/channels/{1}/OneSheetImage_800x1200.jpg">PlayMedia(&quot;{2}&amp;sf_options=fanart%3D{3}&amp;desc%3D{4}%26_options_sf&quot;)</favourite>'.format(label.replace("'","&apos;").replace('"',"&quot;"), url.split("v_id=")[1], url, fanart, description)
            line = '\n    <favourite name="{0}" thumb="{1}">PlayMedia(&quot;{2}&amp;sf_options=fanart%3D{3}&amp;desc%3D{4}%26_options_sf&quot;)</favourite>'.format(label.replace("'","&apos;").replace('"',"&quot;"), thumb, url, fanart, description)
            f.write(line.encode("utf8"))
            g.write(line.encode("utf8"))
    line = "\n</favourites>"
    f.write(line.encode("utf8"))
    g.write(line.encode("utf8"))
    f.close()
    g.close()
    dialogs.notify(msg='Mapping Finished', title='%d total %d done' % (len(dirs_total), len(dirs_done)), delay=5000, image=get_icon_path("metalliq"))


@plugin.route('/testing')
def testing():
    results = {}    
    for i in ["search", "searchalbum", "searchtrack", "searchmdvd", "discography", "discography-mb"]:
        results[i] = audiodb.search(mode=i, artist=artist_name, album=album_name, track=track_name)
    lib = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
    f = xbmcvfs.File("{0}artist.nfo".format(lib), 'w')
    f.write(str(results))
    f.close()
    dialogs.notify(msg='Done', title='and Done', delay=5000, image=get_icon_path("metalliq"))

@plugin.route('/testingbakbak')
def testingbakbak():
    library = {}
    medias = ["movies", "tvshows", "musicvideos", "music", "live"]
    for m in medias:
        if m == "movies":
            lib = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
            ite = RPC.videolibrary.get_movies(properties=["title","year","playcount","fanart","originaltitle","imdbnumber","thumbnail","file"])["movies"]
        elif m == "tvshows":
            lib = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
            ite = RPC.videolibrary.get_tvshows(properties=["title","year","playcount","fanart","originaltitle","imdbnumber","thumbnail","file"])["tvshows"]
#        elif m == "musicvideos":
#           lib = plugin.get_setting(SETTING_MUSIC_LIBRARY_FOLDER, unicode)
#            ite = RPC.videolibrary.get_musicvideos(properties=["title","year","playcount","fanart","originaltitle","imdbnumber","thumbnail","file"])["musicvideos"]
        else: continue
        liq = xbmcvfs.listdir(lib)[0]
        for i in ite:
            try:
                f = xbmcvfs.File(os.path.join(lib, i["imdbnumber"], "player.info"))
                i["player"] = f.read()
                f.close()
            except: i["player"] = "na"
        f = xbmcvfs.File("{0}library.nfo".format(lib), 'w')
        f.write(str(ite))
        f.close()
    dialogs.notify(msg='Done', title='and Done', delay=5000, image=get_icon_path("metalliq"))

#            movie_items = RPC.videolibrary.get_movies(properties=["title","genre","year","rating","playcount","fanart","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","writer","studio","mpaa","cast","country","imdbnumber","set","showlink","streamdetails","top250","votes","thumbnail","file","resume","setid","tag","art","sorttitle","dateadded"])["movies"]
 #           tvshow_items = RPC.videolibrary.get_tvshows(properties=["title","genre","year","rating","playcount","fanart","director","plot","originaltitle","lastplayed","studio","mpaa","imdbnumber","premiered","season","episode","file","watchedepisodes","tag","art","sorttitle","episodeguide","dateadded"])["tvshows"]

#        if m == "movies":
#            lib_folder = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
#            movie_items = RPC.videolibrary.get_movies(properties=["title","genre","year","rating","playcount","fanart","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","writer","studio","mpaa","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","thumbnail","file","resume","setid","tag","sorttitle"])["movies"]
#        if m == "tvshows":
#            lib_folder = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
#            tvshow_items = RPC.videolibrary.get_tvshows(properties=["title","genre","year","rating","playcount","fanart","director","plot","originaltitle","lastplayed","studio","mpaa","imdbnumber","premiered","season","episode","file","watchedepisodes","tag","art","sorttitle","episodeguide","dateadded"])["tvshows"]

def testing2(type):
    lib_folder = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
    lib_items = xbmcvfs.listdir(lib_folder)[0]
    players_tot = [p.id for p in get_players("movies")]
    players_act = [p.id for p in active_players("movies")]
    players_dis = []
    for i in players_tot:
        if i not in players_act: players_dis.append(i)
    players_lib = {}
    for x in lib_items:
        player_file = xbmcvfs.File(os.path.join(lib_folder, x, "player.info"))
        content = player_file.read()
        player_file.close()
        players_lib[x] = content
        player_file.close()
    plugin.log.info("lib_movies  = {0}".format(lib_items))
    plugin.log.info("tot_players = {0}".format(players_tot))
    plugin.log.info("act_players = {0}".format(players_act))
    plugin.log.info("dis_players = {0}".format(players_dis))
    plugin.log.info("lib_players = {0}".format(players_lib))
    tvshows_in_lib = RPC.videolibrary.get_tvshows(properties=["originaltitle", "imdbnumber", "year"])["tvshows"]
    movies_in_lib = RPC.videolibrary.get_movies(properties=["originaltitle", "imdbnumber", "year"])["movies"]
    plugin.log.info("tvshows_in_lib = {0}".format(tvshows_in_lib))
    plugin.log.info("movies_in_lib = {0}".format(movies_in_lib))
    sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_MOVIES_ENABLED_PLAYERS, unicode)])
    sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_MOVIES_ENABLED_PLAYERS, unicode)])
    dialogs.notify(msg='Done', title='and Done', delay=5000, image=get_icon_path("metalliq"))

@plugin.route('/testingbak2')
def testingbak2():
    library = {}
    medias = ["movies", "tvshows", "musicvideos", "music", "live"]
    lists  = ["id", "imdb", "title", "otitle", "player"]
    for m in medias:
        library[m] = {}
        if m == "movies":
            lib_folder = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
            items = RPC.videolibrary.get_movies(properties=["originaltitle", "imdbnumber", "year"])["movies"]
        elif m == "tvshows":
            lib_folder = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
            items = RPC.videolibrary.get_tvshows(properties=["originaltitle", "imdbnumber", "year"])["tvshows"]
#        elif m == "musicvideos":
#            lib_folder = plugin.get_setting(SETTING_MUSICVIDEOS_LIBRARY_FOLDER, unicode)
#            items = RPC.videolibrary.get_musicvideos(properties=["originaltitle", "imdbnumber", "year"])["musicvideos"]
#        elif m == "music":
#            lib_folder = plugin.get_setting(SETTING_MUSIC_LIBRARY_FOLDER, unicode)
#            items = RPC.audiolibrary.get_artists(properties=["title","artist","albumartist","genre","year","rating","album","track","duration","comment","lyrics","musicbrainztrackid","musicbrainzartistid","musicbrainzalbumid","musicbrainzalbumartistid","playcount","fanart","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","writer","studio","mpaa","cast","country","imdbnumber","premiered","productioncode","runtime","set","showlink","streamdetails","top250","votes","firstaired","season","episode","showtitle","thumbnail","file","resume","artistid","albumid","tvshowid","setid","watchedepisodes","disc","tag","art","genreid","displayartist","albumartistid","description","theme","mood","style","albumlabel","sorttitle","episodeguide","uniqueid","dateadded","size","lastmodified","mimetype"])["artists"]
        else: continue
        library[m]["metalliq"] = xbmcvfs.listdir(lib_folder)[0]
        for l in lists: library[m][l] = []
        for i in items:
            if i["imdbnumber"] not in library[m]["metalliq"]: library[m]["player"].append("na")
            else:
                f = xbmcvfs.File(os.path.join(lib_folder, i["imdbnumber"], "player.info"))
                library[m]["player"].append(f.read())
                f.close()
            if m == "movies": library[m]["id"].append(i["movieid"])
            elif m == "tvshows": library[m]["id"].append(i["tvshowid"])
            library[m]["imdb"].append(i["imdbnumber"])
            library[m]["otitle"].append(i["originaltitle"].lower())
            library[m]["title"].append(i["label"].lower())
    plugin.log.info("movies_in_lib = {0}".format(library))
    dialogs.notify(msg='Done', title='and Done', delay=5000, image=get_icon_path("metalliq"))

@plugin.route('/testingbak')
def testingbak():
    movies_id_list = []
    movies_imdb_list = []
    movies_otitle_list = []
    movies_title_list = []
    movies_player_list = []
    movies_metalliq_list = xbmcvfs.listdir(plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode))[0]
    movies_in_lib = RPC.videolibrary.get_movies(properties=["originaltitle", "imdbnumber", "year"])["movies"]
    for item in movies_in_lib:
        if item["imdbnumber"] not in movies_metalliq_list: movies_player_list.append("na")
        else:
            player_file = xbmcvfs.File(os.path.join(plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode), item, "player.info"))
            content = player_file.read()
            movies_player_list.append(content)
            player_file.close()
        movies_id_list.append(item["movieid"])
        movies_id_list.append(item["movieid"])
        movies_imdb_list.append(item["imdbnumber"])
        movies_otitle_list.append(item["originaltitle"].lower())
        movies_title_list.append(item["label"].lower())
    tvshows_id_list = []
    tvshows_imdb_list = []
    tvshows_otitle_list = []
    tvshows_title_list = []
    tvshows_player_list = []
    tvshows_metalliq_list = xbmcvfs.listdir(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode))[0]
    tvshows_in_lib = RPC.videolibrary.get_tvshows(properties=["originaltitle", "imdbnumber", "year"])["tvshows"]
    for item in tvshows_in_lib:
        if item["imdbnumber"] not in tvshows_metalliq_list: tvshows_player_list.append("na")
        else:
            player_file = xbmcvfs.File(os.path.join(plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode), item, "player.info"))
            content = player_file.read()
            movies_player_list.append(content)
            player_file.close()
        tvshows_id_list.append(item["tvshowid"])
        tvshows_imdb_list.append(item["imdbnumber"])
        tvshows_otitle_list.append(item["originaltitle"].lower())
        tvshows_title_list.append(item["label"].lower())
    players_tot = [p.id for p in get_players("movies")]
    players_act = [p.id for p in active_players("movies")]
    players_dis = []
    for i in players_tot:
        if i not in players_act: players_dis.append(i)
    players_lib = {}
    for x in lib_items:
        player_file = xbmcvfs.File(os.path.join(lib_folder, x, "player.info"))
        content = player_file.read()
        player_file.close()
        players_lib[x] = content
        player_file.close()
    plugin.log.info("lib_movies  = {0}".format(lib_items))
    plugin.log.info("tot_players = {0}".format(players_tot))
    plugin.log.info("act_players = {0}".format(players_act))
    plugin.log.info("dis_players = {0}".format(players_dis))
    plugin.log.info("lib_players = {0}".format(players_lib))
    plugin.log.info("tvshows_in_lib = {0}".format(tvshows_in_lib))
    plugin.log.info("movies_in_lib = {0}".format(movies_in_lib))
    sorted(["[B]{0}[/B]".format(p.clean_title) for p in players if p.id in plugin.get_setting(SETTING_MOVIES_ENABLED_PLAYERS, unicode)])
    sorted(["[I]{0}[/I]".format(p.clean_title) for p in players if p.id not in plugin.get_setting(SETTING_MOVIES_ENABLED_PLAYERS, unicode)])
    dialogs.notify(msg='Done', title='and Done', delay=5000, image=get_icon_path("metalliq"))


@plugin.route('/settings')
def settings_general():
    openSettings(addonid, 0.0)

@plugin.route('/settings/movies')
def settings_movies():
    openSettings(addonid, 1.2)

@plugin.route('/settings/tv')
def settings_tv():
    openSettings(addonid, 2.2)

@plugin.route('/settings/music')
def settings_music():
    openSettings(addonid, 3.3)

@plugin.route('/settings/live')
def settings_live():
    openSettings(addonid, 4.2)

@plugin.route('/settings/advanced/')
def settings_advanced():
    openSettings(addonid, 5.0)

@plugin.route('/settings/toggling/')
def settings_toggling():
    openSettings(addonid, 5.3)

@plugin.route('/settings/appearance/')
def settings_appearance():
    openSettings(addonid, 6.0)

@plugin.route('/.*extrafanart/')
def extra_fanart():
    return

@plugin.route('/.*extrathumbs/')
def extra_thumbs():
    return

@plugin.route('/.*nomedia')
def mo_media():
    return

def openSettings(addonid, focus=None):
    try:
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonid)
        value1, value2 = str(focus).split('.')
        xbmc.executebuiltin('SetFocus(%d)' % (int(value1) + 100))
        xbmc.executebuiltin('SetFocus(%d)' % (int(value2) + 200))
    except: return

def clickSettings(addonid, focus=None):
    try:
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonid)
        value1, value2 = str(focus).split('.')
        xbmc.executebuiltin('SetFocus(%d)' % (int(value1) + 100))
        xbmc.executebuiltin('SetFocus(%d)' % (int(value2) + 200))
        xbmc.executebuiltin('SendClick(%d)' % (int(value2) + 200))
    except: return
#########   Main    #########

def main():
    if '/movies' in sys.argv[0]:
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    elif '/tv/play' in sys.argv[0]:
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    elif '/tvdb' in sys.argv[0] and sys.argv[0].count('/') < 6:
        xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
    elif '/tvdb' in sys.argv[0] and sys.argv[0].count('/') > 5:
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    elif '/tv' in sys.argv[0] and not '/settings' in sys.argv[0]:
        xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
    elif '/music' in sys.argv[0]:
        xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
    elif '/live' in sys.argv[0]:
        xbmcplugin.setContent(int(sys.argv[1]), 'LiveTV')
    elif '/list' in sys.argv[0]:
        xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    plugin.run()

if __name__ == '__main__':
    main()