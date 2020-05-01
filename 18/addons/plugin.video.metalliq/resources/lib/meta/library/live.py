import os
import shutil

from xbmcswift2 import xbmc, xbmcvfs

from meta import plugin, LANG
from meta.utils.text import to_utf8, date_to_timestamp, equals
from meta.utils.rpc import RPC
from meta.utils.properties import set_property
from meta.library.tools import add_source
from meta.gui import dialogs
from meta.navigation.base import get_icon_path, get_background_path

from settings import SETTING_LIVE_LIBRARY_FOLDER, SETTING_LIBRARY_SET_DATE, SETTING_LIVE_PLAYLIST_FOLDER
from language import get_string as _

def update_library():    
    folder_path = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
    if not xbmcvfs.exists(folder_path):
        return
    # get library folder
    library_folder = setup_library(folder_path)
    # get shows in library
    try:
        channels = xbmcvfs.listdir(library_folder)[0]
    except:
        channels = []
    # update each show
    clean_needed = False
    updated = 0

def add_channel_to_library(library_folder, channel, play_plugin = None):
    changed = False
    # create channel folder
    channel_folder = os.path.join(library_folder, str(channel)+'/')
    if not xbmcvfs.exists(channel_folder):
        try: 
            xbmcvfs.mkdir(channel_folder)
        except:
            pass
    # create nfo file
    nfo_filepath = os.path.join(channel_folder, str(channel)+".nfo")
    if not xbmcvfs.exists(nfo_filepath):
        changed = True
        nfo_file = xbmcvfs.File(nfo_filepath, 'w')
        content = "%s" % str(channel)
        nfo_file.write(content)
        nfo_file.close()
    # Create play with file
    if play_plugin is not None:
        player_filepath = os.path.join(channel_folder, 'player.info')
        player_file = xbmcvfs.File(player_filepath, 'w')
        content = "{0}".format(play_plugin)
        player_file.write(content)
        player_file.close()
    # create strm file
    strm_filepath = os.path.join(channel_folder, str(channel)+".strm")
    if not xbmcvfs.exists(strm_filepath):
        changed = True
        strm_file = xbmcvfs.File(strm_filepath, 'w')
        content = plugin.url_for("live_play", channel=channel, program="None", language="en", mode="library")
        strm_file.write(content)
        strm_file.close()
    return changed

def library_channel_remove_strm(channel, folder):
    channel_folder = os.path.join(folder, channel)
    stream_file = os.path.join(channel_folder, channel + '.strm')
    info_file = os.path.join(channel_folder, 'player.info')
    nfo_file = os.path.join(channel_folder, channel + '.nfo')
    if xbmcvfs.exists(stream_file):
        xbmcvfs.delete(stream_file)
        xbmcvfs.delete(info_file)
        xbmcvfs.delete(nfo_file)
        xbmcvfs.rmdir(channel_folder)
        return True
    return False

def get_player_plugin_from_library(library_channel):
    # Specified by user
    try:
        library_folder = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
        player_file = xbmcvfs.File(os.path.join(library_folder, str(channel), "player.info"))
        content = player_file.read()
        player_file.close()
        if content:
            return content
    except:
        pass

def setup_library(library_folder):
    if library_folder[-1] != "/":
        library_folder += "/"
    metalliq_playlist_folder = "special://profile/playlists/mixed/MetalliQ/"
    if not xbmcvfs.exists(metalliq_playlist_folder): xbmcvfs.mkdir(metalliq_playlist_folder)
    playlist_folder = plugin.get_setting(SETTING_LIVE_PLAYLIST_FOLDER, unicode)
    # create folders
    if not xbmcvfs.exists(playlist_folder): xbmcvfs.mkdir(playlist_folder)
    if not xbmcvfs.exists(library_folder):
        # create folder
        xbmcvfs.mkdir(library_folder)
        # auto configure folder
        msg = _("Would you like to automatically set MetalliQ as a channel video source?")
        if dialogs.yesno("{0} {1}".format(_("Library"), "setup"), msg):
            source_thumbnail = get_icon_path("live")
            source_name = "MetalliQ " + _("Channels")
            source_content = "('{0}','','','',0,0,'<settings></settings>',0,0,NULL,NULL)".format(library_folder)
            add_source(source_name, library_folder, source_content, source_thumbnail)
    # return translated path
    return xbmc.translatePath(library_folder)

def auto_live_setup(library_folder):
    if library_folder[-1] != "/":
        library_folder += "/"
    if not xbmcvfs.exists(library_folder):
        try:
            xbmcvfs.mkdir(library_folder)
            source_thumbnail = get_icon_path("live")
            source_name = "MetalliQ " + _("Channels")
            source_content = "('{0}','','','',0,0,'<settings></settings>',0,0,NULL,NULL)".format(library_folder)
            add_source(source_name, library_folder, source_content, source_thumbnail)
            return True
        except:
            False