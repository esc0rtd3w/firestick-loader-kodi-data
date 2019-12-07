import os
from xbmcswift2 import xbmc, xbmcvfs
from meta.gui import dialogs
from meta import plugin, LANG
from meta.play.base import active_players
from meta.play.players import ADDON_DEFAULT, ADDON_SELECTOR
from meta.play.channelers import ADDON_STANDARD, ADDON_PICKER
from meta.play.live import play_channel, play_channel_from_guide
from meta.navigation.base import get_icon_path, get_genre_icon, get_background_path, get_genres, get_tv_genres, caller_name, caller_args
from meta.library.live import setup_library, add_channel_to_library, library_channel_remove_strm
from meta.utils.text import to_unicode, to_utf8
from language import get_string as _
from settings import CACHE_TTL, SETTING_LIVE_LIBRARY_FOLDER, SETTING_LIVE_DEFAULT_AUTO_ADD

def get_channels():
    storage = plugin.get_storage("channels")
    channels = storage.get("list")
    if channels is None:
        channels = []
        storage["list"] = channels
    return channels

def get_library_channels():
    folder_path = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
    if not xbmcvfs.exists(folder_path):
        return []
    # get channels in library
    try:
        library_channels = xbmcvfs.listdir(folder_path)[0]
    except:
        library_channels = []
    return library_channels

@plugin.route('/live/clear_channels')
def clear_channels():
    channels = get_channels()
    del channels[:]
    xbmc.executebuiltin("Container.Refresh")
    
@plugin.route('/live/remove_channel/<channel>')
def remove_channel(channel):
    channels = get_channels()
    try:
        channels.remove(channel)
    except:
        pass
    xbmc.executebuiltin("Container.Refresh")

@plugin.route('/live/add_to_library/<channel>/<mode>')
def live_add_to_library(channel, mode):
    if mode != None and plugin.get_setting(SETTING_LIVE_DEFAULT_AUTO_ADD, bool):
        player = mode
    else:
        players = active_players("live", filters = {'network': channel.get('network')})
        players.insert(0, ADDON_SELECTOR)
        selection = dialogs.select(_("Play using..."), [p.title for p in players])
        if selection == -1:
            return
        player = players[selection]
    library_folder = setup_library(plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode))
    add_channel_to_library(library_folder, channel, player)

@plugin.route('/live/remove_from_library/<channel>')
def live_remove_from_channel(channel):
    folder = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
    library_channel_remove_strm(channel, folder)

@plugin.route('/live/move_channel_up/<channel>')
def move_channel_up(channel):
    channels = get_channels()
    old_index = channels.index(channel)
    new_index = old_index - 1
    if new_index >= 0:
        channels.insert(new_index, channels.pop(old_index))
    xbmc.executebuiltin("Container.Refresh")

@plugin.route('/live/move_channel_down/<channel>')
def move_channel_down(channel):
    channels = get_channels()
    old_index = channels.index(channel)
    new_index = old_index + 1
    if old_index >= 0:
        channels.insert(new_index, channels.pop(old_index))
    xbmc.executebuiltin("Container.Refresh")
    
@plugin.route('/live')
def live():
    """ Live TV directory """
    library_channels = get_library_channels()
    if library_channels: 
        items = [
            {
                'label': "{0} {1}".format(_("View your"), _("Channels").lower()),
                'path': plugin.url_for("browse_library_channels"),
                'icon': get_icon_path("library"),
            },
            {
                'label': "{0}: {1}".format(_("Search"), _("Channel")),
                'path': plugin.url_for("live_search"),
                'icon': get_icon_path("search"),
            },
        ]
    else:
        items = [
            {
                'label': "{0}: {1}".format(_("Search"), _("Channel")),
                'path': plugin.url_for("live_search"),
                'icon': get_icon_path("search"),
            },
        ]
    channels = get_channels()
    if channels:
        items.append({
            'label': _("Remove %s") % _("Channels").lower(),
            'path': plugin.url_for("clear_channels"),
            'icon': get_icon_path("clear"),
        })
    for (index, channel) in enumerate(channels):
        channelori = channel
        channel = to_utf8(channel)
        if channel in library_channels:
            context_menu = []
        else:
            context_menu = [
                (
                    _("Scan item to library"),
                    "RunPlugin({0})".format(plugin.url_for("live_add_to_library", channel=channel, mode="library"))
                )
            ]
        if channel in channels:
            context_menu.append(
                (
                    _("Remove %s") % _("Channel").lower(),
                    "RunPlugin({0})".format(plugin.url_for("remove_channel", channel=channel))
                )
            )
        if index != 0:
            context_menu.append(
                (
                    _("Move up"),
                    "RunPlugin({0})".format(plugin.url_for("move_channel_up", channel=channel))
                )
            )
        if index != len(channels) - 1:
            context_menu.append(
                (
                    _("Move down"),
                    "RunPlugin({0})".format(plugin.url_for("move_channel_down", channel=channel))
                )
            )
        items.append({
            'label': channel,
            'path': plugin.url_for("live_play", channel=channel, program="None", language="en", mode="external"),
            'icon': "DefaultVideo.png",
            'context_menu': context_menu,
        })
    return items

@plugin.route('/live/library')
def browse_library_channels():
    items = [
        {
            'label': _("New channel"),
            'path': plugin.url_for("live_search"),
            'icon': get_icon_path("search"),
        },
    ]
    library_channels = get_library_channels()
    if library_channels:
        for (index, library_channel) in enumerate(library_channels):
            if library_channel != None:
                items.append({
                    'label': str(library_channel),
                    'path': plugin.url_for("live_play", program="None", language="en", channel=library_channel, mode="library"),
                    'icon': get_icon_path("library"),
                    'context_menu': [
                        (
                            _("Remove %s") % _("Channel").lower(),
                            "RunPlugin({0})".format(plugin.url_for("live_remove_from_channel", channel=library_channel))
                        )]
                })
    return items

@plugin.route('/live/search')
def live_search():
    """ Activate channel search """
    term = plugin.keyboard(heading=_("Enter search string"))
    return live_search_term(term)

@plugin.route('/live/search_term/<term>')
def live_search_term(term):
    """ Perform search of a specified <term>"""
    term = to_utf8(term)
    channels = get_channels()
    if term not in channels:
        channels.append(term)
        xbmc.executebuiltin("Container.Refresh")
    return live_play(term)

@plugin.route('/live/<channel>/<program>/<language>/<mode>', options = {"program": "None", "language": "en", "mode": "external"})
def live_play(channel, program=None, language="en", mode="external"):
    """ Play <channel> """
    play_channel(channel, program, language, mode)

@plugin.route('/live_guide/<channel>/<program>/<language>/<mode>', options = {"program": "None", "language": "en", "mode": "external"})
def guide_live_play(channel, program=None, language="en", mode="external"):
    """ Play <channel> from a guide """
    play_channel_from_guide(channel, program, language, mode)
