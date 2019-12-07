# -*- coding: utf-8 -*-

"""
    context.py --- functions to generate a context menu for jen items
    Copyright (C) 2017, Jen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, ordepends
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import __builtin__

import resources.lib.external.tvdb_api as tvdb_api
import xbmc
import xbmcaddon
from language import get_string as _
from resources.lib.plugin import run_hook
from resources.lib.util.url import get_addon_url


ADDON = xbmcaddon.Addon()
if ADDON.getSetting("language_id") == "system":
    LANG = xbmc.getLanguage(
        xbmc.ISO_639_1)
else:
    LANG = ADDON.getSetting("language_id")

tvdb = tvdb_api.Tvdb(
    __builtin__.tvdb_api_key,
    language=LANG,
    cache=xbmc.translatePath(ADDON.getAddonInfo("profile")))


def get_context_items(item):
    """generate context menu for item
    Keyword Arguments:
    item -- JenItem to generate menu for
    """
    context = []
    content = item["content"]
    # cache
    if content == "":
        context.append((_("Try Uncached"),
                        "Container.Update({0})".format(
                            get_addon_url("get_list_uncached", item["link"]))))
    # information
    context.append((xbmcaddon.Addon().getLocalizedString(30708),
                    "XBMC.Action(Info)"))

    # view modes
    if content == "movie":
        context.append((_("Set Movie View"),
                        "RunPlugin({0})".format(
                            get_addon_url("save_view_mode", "movies"))))
    elif content == "tvshow":
        context.append((_("Set TV Show View"),
                        "RunPlugin({0})".format(
                            get_addon_url("save_view_mode", "tvshows"))))
    elif content == "season":
        context.append((_("Set Season View"),
                        "RunPlugin({0})".format(
                            get_addon_url("save_view_mode", "seasons"))))
    elif content == "episode":
        context.append((_("Set Episode View"),
                        "RunPlugin({0})".format(
                            get_addon_url("save_view_mode", "episodes"))))
    else:
        context.append((_("Set View"),
                        "RunPlugin({0})".format(
                            get_addon_url("save_view_mode", "other"))))

    # extended info mod/qlickplay
    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)") or \
       xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
        if content == "movie":
            context.append((_("Extended info"),
                            "RunPlugin({0})".format(
                                get_addon_url("movie_extended_info",
                                              item["imdb"]))))
        elif content == "tvshow":
            context.append((_("Extended info"),
                            "RunPlugin({0})".format(
                                get_addon_url("tvshow_extended_info",
                                              item["imdb"]))))
        elif content == "season":
            url = "{'imdb': '%s', 'season': %s}" %\
                  (item["imdb"], item["season"])
            context.append((_("Extended info"),
                            "RunPlugin({0})".format(
                                get_addon_url("season_extended_info",
                                              url))))
        elif content == "episode":
            url = "{'imdb': '%s', 'season': %s, 'episode': %s}" %\
                  (item["imdb"], item["season"], item["episode"])
            context.append((_("Extended info"),
                            "RunPlugin({0})".format(
                                get_addon_url("episode_extended_info",
                                              url))))

    # queue
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    if playlist.size() > 0:
        context.append((_("Play Queue"),
                        "RunPlugin({0})".format(
                            get_addon_url("play_queue"))))
        context.append((_('Show Queue'),
                        'Action("Playlist")'))
        context.append((_("Clear Queue"),
                        "RunPlugin({0})".format(
                            get_addon_url("clear_queue"))))
    try:
        if content == "movie":
            context.append((_("Queue Movie"),
                            "RunPlugin({0})".format(
                                get_addon_url("queue",
                                              item.item_string))))
        elif content == "tvshow":
            context.append((_("Queue TV Show"),
                            "RunPlugin({0})".format(
                                get_addon_url("queue",
                                              item.item_string))))
        elif content == "season":
            context.append((_("Queue Season"),
                            "RunPlugin({0})".format(
                                get_addon_url("queue",
                                              item.item_string))))
        elif content == "episode":
            context.append((_("Queue Episode"),
                            "RunPlugin({0})".format(
                                get_addon_url("queue",
                                              item.item_string))))
        else:
            context.append((_("Queue Item"),
                            "RunPlugin({0})".format(
                                get_addon_url("queue",
                                              item.item_string))))
    except:
        pass

    hook_result = run_hook("get_context_items", item, context)
    if hook_result:
        return hook_result

    return context
