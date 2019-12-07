import sys, os
import json
from traceback import print_exc
from xbmcswift2 import xbmc, xbmcgui, xbmcplugin
from meta import plugin
from meta.gui import dialogs
from meta.utils.executor import execute
from meta.utils.properties import set_property
from meta.utils.text import to_unicode, urlencode_path, apply_parameters, to_utf8
from meta.library.tools import get_movie_from_library, get_episode_from_library
from meta.navigation.base import get_icon_path, get_background_path
from meta.play.players import get_players, patch
from meta.play.channelers import get_channelers
from meta.play.lister import Lister
from settings import *
from language import get_string as _

@plugin.cached(TTL=60, cache="trakt")
def get_trakt_ids(*args, **kwargs):
    try:
        from trakt import trakt
        return trakt.find_trakt_ids(*args, **kwargs)
    except: return None

def active_players(media, filters={}):
    if media == "movies": setting = SETTING_MOVIES_ENABLED_PLAYERS
    elif media == "tvshows": setting = SETTING_TV_ENABLED_PLAYERS
    elif media == "musicvideos": setting = SETTING_MUSICVIDEOS_ENABLED_PLAYERS
    elif media == "music": setting = SETTING_MUSIC_ENABLED_PLAYERS
    elif media == "live": setting = SETTING_LIVE_ENABLED_PLAYERS
    else: raise Exception("invalid parameter %s" % media)
    try: enabled = plugin.get_setting(setting, unicode)
    except: enabled = []
    return [p for p in get_players(media, filters) if p.id in enabled]

def active_channelers(media, filters={}):
    if media == "movies": setting = SETTING_MOVIES_ENABLED_CHANNELERS
    elif media == "tvshows": setting = SETTING_TV_ENABLED_CHANNELERS
    elif media == "musicvideos": setting = SETTING_MUSICVIDEOS_ENABLED_CHANNELERS
    elif media == "music": setting = SETTING_MUSIC_ENABLED_CHANNELERS
    elif media == "live": setting = SETTING_LIVE_ENABLED_CHANNELERS
    else: raise Exception("invalid parameter %s" % media)
    try: enabled = plugin.get_setting(setting, unicode)
    except: enabled = []
    return [p for p in get_channelers(media, filters) if p.id in enabled]

def action_cancel(clear_playlist=True):
    if clear_playlist: xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
    plugin.set_resolved_url()
    xbmc.executebuiltin('Dialog.Close(okdialog, true)')

def action_activate(link):
    xbmc.executebuiltin('Container.Update("%s")' % link)
    #action_cancel()

def action_run(link):
    if link.startswith("plugin://"): xbmc.executebuiltin('RunPlugin(%s)' % link)
    else: xbmc.executebuiltin('RunScript(%s)' % link)

def action_prerun(link):
#    xbmc.executebuiltin('ActivateWindow(10025,addons://user/xbmc.addon.video/plugin.video.zen/,return)')
    if link.startswith("plugin://"):
        id = link.split("/")
        xbmc.executebuiltin('RunAddon(%s)' % id[2])
        while xbmc.getInfoLabel('Container.PluginName') != id[2] or xbmc.getCondVisibility('Window.IsActive(busydialog)'): xbmc.sleep(250)
        xbmc.sleep(250)
        xbmc.executebuiltin('Container.Update("%s")' % link)


def action_play(item):
    #action_cancel()
    plugin.play_video(item)

def action_playmedia(item):
    xbmc.executebuiltin('PlayMedia("%s")'%item)

def action_resolve(item):
    #plugin.set_resolved_url(item)
    action_play(item)

def get_video_link(players, params, mode, use_simple=False):
    lister = Lister()
    # Extend parameters
    for lang, lang_params in params.items():
        for key, value in lang_params.items():
            if isinstance(value, basestring):
                params[lang][key + "_+"] = value.replace(" ", "+")
                params[lang][key + "_-"] = value.replace(" ", "-")
                params[lang][key + "_escaped"] = value.replace(" ", "%2520")
                params[lang][key + "_escaped+"] = value.replace(" ", "%252B")
    pDialog = None
    selection = None
    try:
        if len(players) > 1 and use_simple:
            index = dialogs.select(_("Play using..."), [player.title for player in players])
            if index == -1: return None
            players = [players[index]]
        resolve_f = lambda p : resolve_player(p, lister, params)
        if len(players) > 1:
            pool_size = plugin.get_setting(SETTING_POOL_SIZE, int)
            populator = lambda : execute(resolve_f, players, lister.stop_flag, pool_size)
            selection = dialogs.select_ext(_("Play using..."), populator, len(players))
        else:
            result = resolve_f(players[0])
            if result:
                title, links = result
                if len(links) == 1: selection = links[0]
                else:
                    index = dialogs.select(_("Play using..."), [x['label'] for x in links])
                    if index > -1: selection = links[index]
            else: dialogs.ok(_("Error"), _("%s not found") % _("Video"))
    finally: lister.stop()
    return selection

def on_play_video(mode, players, params, trakt_ids=None):
    if plugin.get_setting(SETTING_AUTOPATCH, bool) == True: patch("auto")
    assert players
    # Cancel resolve
    action_cancel()
    # Get video link
    use_simple_selector = plugin.get_setting(SETTING_USE_SIMPLE_SELECTOR, bool)
    is_extended = not (use_simple_selector or len(players) == 1)
    if not is_extended: xbmc.executebuiltin("ActivateWindow(busydialog)")
    try: selection = get_video_link(players, params, mode, use_simple_selector)
    finally:
        if not is_extended: xbmc.executebuiltin("Dialog.Close(busydialog)")
    if not selection: return
    # Get selection details
    link = selection['path']
    action = selection.get('action', '')
    plugin.log.info('Playing url: %s' % to_utf8(link))
    # Activate link
    if action == "ACTIVATE": action_activate(link)
    elif action == "RUN": action_run(link)
    elif action == "PRERUN": action_prerun(link)
    elif action == "PLAYMEDIA": action_playmedia(link)
    elif action == "PRERUNRETURN": metaplayer().action_prerun(link)
    else:
        if trakt_ids: set_property('script.trakt.ids', json.dumps(trakt_ids))
        return link
    return None

def resolve_player(player, lister, params):
    results = []
    for command_group in player.commands:  
        if xbmc.abortRequested or not lister.is_active(): return
        command_group_results = []
        for command in command_group:
            if xbmc.abortRequested or not lister.is_active(): return
            lang = command.get("language", "en")
            if not lang in params: continue
            parameters = params[lang]
            try:
                link = apply_parameters(to_unicode(command["link"]), parameters)
            except:
                print_exc()
                continue
            if link == "movies" and player.media == "movies":
                video = get_movie_from_library(parameters['imdb'])
                if video:
                    command_group_results.append(video)
            elif link == "tvshows" and player.media == "tvshows":
                video = get_episode_from_library(parameters['id'], parameters['season'], parameters['episode'])
                if not video:
                    video = get_episode_from_library(parameters['tmdb'], parameters['season'], parameters['episode'])
                if video:
                    command_group_results.append(video)
            elif not command.get("steps"):
                command_group_results.append(
                    {
                        'label': player.title,
                        'path': urlencode_path(link),
                        'action': command.get("action", "PLAY")
                    }
                )
            else:
                steps = [to_unicode(step) for step in command["steps"]]
                files, dirs = lister.get(link, steps, parameters)
                if command.get("action", "PLAY") == "ACTIVATE":
                    files += dirs
                if files:
                    command_group_results += [
                        {
                            'label': f['label'],
                            'path': player.postprocess(f['path']),
                            'action': command.get("action", "PLAY")
                        } for f in files]
            if command_group_results:
                break
        results += command_group_results
    if results:
        return player.title, results


class metaplayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.returnlink = xbmc.getInfoLabel('Container.FolderPath')
        xbmc.log("returnlink: " + repr(self.returnlink), xbmc.LOGNOTICE)

    def action_prerun(self, link):
        #    xbmc.executebuiltin('ActivateWindow(10025,addons://user/xbmc.addon.video/plugin.video.zen/,return)')
        if link.startswith("plugin://"):
            id = link.split("/")
            xbmc.executebuiltin('RunAddon(%s)' % id[2])
            while xbmc.getInfoLabel('Container.PluginName') != id[2] or xbmc.getCondVisibility('Window.IsActive(busydialog)'): xbmc.sleep(250)
            xbmc.sleep(250)
            self.play(link)
        while xbmc.getInfoLabel('Container.PluginName') == id[2] and xbmc.getInfoLabel('Container.FolderPath') != "plugin://%s/" % id[2] and id[2] in xbmc.getInfoLabel('Container.FolderPath'):
            xbmc.sleep(250)
            if xbmc.getInfoLabel('Container.FolderPath') == "plugin://%s/" % id[2] or id[2] not in xbmc.getInfoLabel('Container.FolderPath'):
                break
        xbmc.executebuiltin('Container.Update("%s", replace)' % self.returnlink)

    def onPlayBackEnded(self):
        xbmc.executebuiltin('Container.Update("%s", replace)' % self.returnlink)

    def onPlayBackStopped(self):
        xbmc.executebuiltin('Container.Update("%s", replace)' % self.returnlink)