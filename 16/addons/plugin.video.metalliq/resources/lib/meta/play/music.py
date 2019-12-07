import re
import xbmc
from meta import plugin, LANG
from meta.utils.text import to_unicode
from meta.play.players import get_needed_langs, ADDON_SELECTOR
from meta.play.base import active_players, action_cancel, action_play, on_play_video

from settings import SETTING_USE_SIMPLE_SELECTOR, SETTING_MUSIC_DEFAULT_PLAYER, SETTING_MUSICVIDEOS_DEFAULT_PLAYER, SETTING_MUSIC_DEFAULT_PLAYER_FROM_LIBRARY, SETTING_MUSICVIDEOS_DEFAULT_PLAYER_FROM_LIBRARY, SETTING_MUSIC_DEFAULT_PLAYER_FROM_CONTEXT, SETTING_MUSICVIDEOS_DEFAULT_PLAYER_FROM_CONTEXT

def play_music(artist_name, track_name, album_name, mode = "default"):
    # Get players to use
    if mode == 'select':
        play_plugin = ADDON_SELECTOR.id
    elif mode == 'context':
        play_plugin = plugin.get_setting(SETTING_MUSIC_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = plugin.get_setting(SETTING_MUSIC_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default':
        play_plugin = plugin.get_setting(SETTING_MUSIC_DEFAULT_PLAYER, unicode)
    else:
        play_plugin = mode
    players = active_players("music")
    players = [p for p in players if p.id == play_plugin] or players
    if not players:
        xbmc.executebuiltin("Action(Info)")
        action_cancel()
        return

    # Get parameters
    params = {}
    for lang in get_needed_langs(players):
        params[lang] = get_music_parameters(artist_name, album_name, track_name)
        params[lang] = to_unicode(params[lang])

    # Go for it
    link = on_play_video(mode, players, params)
    if link:
        action_play({
            'label': "{0} - {1} - {2}".format(artist_name, album_name, track_name),
            'path': link,
            'is_playable': True,
            'info_type': 'music',
        })

def play_musicvideo(artist_name, track_name, album_name, mode = "default"):
    # Get players to use
    if mode == 'select':
        play_plugin = ADDON_SELECTOR.id
    elif mode == 'context':
        play_plugin = plugin.get_setting(SETTING_MUSICVIDEOS_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = plugin.get_setting(SETTING_MUSICVIDEOS_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default':
        play_plugin = plugin.get_setting(SETTING_MUSICVIDEOS_DEFAULT_PLAYER, unicode)
    else:
        play_plugin = mode
    players = active_players("musicvideos")
    players = [p for p in players if p.id == play_plugin] or players
    if not players:
        xbmc.executebuiltin("Action(Info)")
        action_cancel()
        return

    # Get parameters
    params = {}
    for lang in get_needed_langs(players):
        params[lang] = get_music_parameters(artist_name, album_name, track_name)
        params[lang] = to_unicode(params[lang])

    # Go for it
    link = on_play_video(mode, players, params)
    if link:
        action_play({
            'label': "{0} - {1} - {2}".format(artist_name, album_name, track_name),
            'path': link,
            'is_playable': True,
            'info_type': 'video',
        })


def get_music_parameters(artist_name, album_name, track_name):
    parameters = {}
    parameters["artist"] = artist_name
    parameters['clearartist'] = re.sub("(\(.*?\))", "", artist_name).strip()
    parameters["album"] = album_name
    parameters['clearalbum'] = re.sub("(\(.*?\))", "", album_name).strip()
    parameters["track"] = track_name
    parameters['cleartrack'] = re.sub("(\(.*?\))", "", track_name).strip()

    return parameters