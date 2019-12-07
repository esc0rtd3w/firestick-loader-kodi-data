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

addonid = 'plugin.video.metalliq'

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
            'label': _("Channels"),
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
            'label': _("Search"),
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

@plugin.route('/manage/library/<type>')
def manage_library_players(type):
    from collections import Counter
    if type == "movies":
        ITEMS = RPC.VideoLibrary.GetMovies(properties=["imdbnumber", "title", "file", "year"])["movies"]
        folder = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
        default = plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif type == "tvshows":
        ITEMS = RPC.VideoLibrary.GetTVShows(properties=["imdbnumber", "title", "file", "year"])["tvshows"]
        folder = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
        default = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    LIBRARY_PLAYERS = []
    ALL_PLAYERS = [p for p in get_players(type)]
    IDS = [p.id for p in get_players(type)]
    NAMES = [p.clean_title for p in get_players(type)]
    ENABLED = active_players(type)
    name = NAMES[IDS.index(default)] if default in IDS else default
    for item in ITEMS:
        if folder in item['file']:
            player_file = xbmc.translatePath(os.path.join(folder, item['imdbnumber'], "player.info"))
            if os.path.exists(player_file):
                with open(player_file) as f:
                    content = f.read()
                if not content or content == "":
                    content = default
                    with open(player_file, "w") as f:
                        f.write(content)
            else:
                with open(player_file, "w") as f:
                    content = default
                    f.write(content)
            LIBRARY_PLAYERS.append(content)
            item['player'] = content
#        Counter(directors).most_common(1)[0][0] 
    COMMON_PLAYERS = Counter(LIBRARY_PLAYERS).most_common()
    PLAYERS = ["({0}) {1}".format(player[1], NAMES[IDS.index(player[0])] if player[0] in IDS else player[0]) for player in COMMON_PLAYERS]
    msg1 = "{0} {1}".format(_("Choose"), _("By group").replace(_("Group").lower(), _("Player")).lower())
    stage1 = dialogs.select(msg1, PLAYERS)
    if stage1 == -1:
        return
    else:
        picked = PLAYERS[stage1].split(" ", 1)[1]
        if picked in NAMES:
            picked_id = IDS[NAMES.index(picked)]
        else:
            picked_id = picked
        msg2 = '{0} "{1}"{2}'.format(_("Edit"), picked, _("%s to %s").replace("%s", ""))
        types = ['{0} [{1}]'.format(name, _("Preferred mode").replace(_("Mode").lower(), _("Player").lower())), 
                 '{0} ({1})'.format(_("Enabled"), len(ENABLED)),
                 '{0} ({1})'.format(_("All"), len(NAMES)),
                 '{0} {1}'.format(_("Enter search string").replace(_("Search string").lower(), _("Custom").lower()), "id")]
        stage2 = dialogs.select(msg2, types)
        if stage2 == -1:
            return
        else:
            new = ""
            if stage2 == 0:
                new = plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
            elif stage2 == 1:
                msg3 = "{0} {1} {2}".format(_("Choose"), _("Enabled").lower(), _("Player").lower())
                stage3 = dialogs.select(msg3, [e.clean_title for e in ENABLED])
                if stage3 == -1:
                    return
                else:
                    new = ENABLED[stage3].id
            elif stage2 == 2:
                msg3 = "{0} {1}".format(_("Choose"), _("Player").lower())
                stage3 = dialogs.select(msg3, [e.clean_title for e in ALL_PLAYERS])
                if stage3 == -1:
                    return
                else:
                    new = ALL_PLAYERS[stage3].id
            elif stage2 == 3:
                new = plugin.keyboard(heading="{0}".format(_("Enter number").replace(_("Number").lower(), '{0}-{1}(!)'.format(_("Player").lower(), "id"))))
                if not new:
                    return
                elif new == "":
                    new = default
            if new in IDS:
                new_name = NAMES[IDS.index(new)]
            else:
                new_name = new
            msg5 = '{0} "{1}"[CR]{2} "{3}".[CR]{4}'.format(_("Edit"), picked, _("%s to %s").replace("%s ", "").replace("%s", ""), new_name, _("Are you sure?"))
            if dialogs.yesno('{0} {1} {2}'.format(_("Edit"), _("Library").lower(), _("Player").lower()), msg5):
                for item in ITEMS:
                    if item['player'] and item['player'] == picked_id:
                        lib_file = xbmc.translatePath(os.path.join(folder, item['imdbnumber'], "player.info"))
                        plugin.log.info("QQQQQ lib_file = {0}".format(lib_file))
                        with open(lib_file, "w") as lf:
                            lf.write(new)
            dialogs.notify(msg=_("Done"), title=_("Manage...").replace(".", ""), delay=5000, image=get_icon_path("metalliq"))

@plugin.route('/manage/tv/players')
def manage_tv_players():
    library_inventory(type="movies")
    library_inventory(type="tvshows")
    channel_inventory()

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
#            meta.library.movies.update_library()
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
    xbmc.executebuiltin('SetProperty(running,totalmetalliq,home)')
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
    xbmc.executebuiltin('ClearProperty(running,home)')

@plugin.route('/setup/players')
def players_setup():
    set_property("running","totalmetalliq")
    url = "https://api.github.com/repos/OpenELEQ/verified-metalliq-players/zipball"
    if updater.update_players(url): dialogs.notify(msg=_('Player'), title=_('Updated for %s') % _('Player'), delay=1000, image=get_icon_path("player"))
    else: dialogs.notify(msg=_('Player'), title=_('Failed for %s') % _('Player'), delay=1000, image=get_icon_path("player"))
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/settings/players/all/)")
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
    if term == " " or term == None or term == "": term = plugin.keyboard(heading=_("Enter search string"))
    else: term = plugin.keyboard(default=term, heading=_("Enter search string"))
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
    movies_backup_file_path = "special://profile/addon_data/plugin.video.metalliq/movies_to_add.bak"
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
    shows_backup_file_path = "special://profile/addon_data/plugin.video.metalliq/shows_to_add.bak"
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
    if selection   == 0: xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/movies/play_by_name/{0}/en)".format(label))
    elif selection == 1: xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/tv/play_by_name_only/{0}/en)".format(label))
    elif selection == 2: xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/live/{0}/None/en/context)".format(label))

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

def dump(obj):
  for attr in dir(obj):
    plugin.log.warning("obj.%s = %s" % (attr, getattr(obj, attr)))

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