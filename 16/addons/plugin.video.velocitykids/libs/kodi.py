"""
    Kodi Addon
    Copyright (C) 2015 Blazetamer
    Thanks to tknorris
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmc
import xbmcvfs
import urllib
import urlparse
import sys
import os
import re
from libs import log_utils
#from tm_libs import watched_cache

addon = xbmcaddon.Addon()

ICON_PATH = os.path.join(addon.getAddonInfo('path'), 'icon.png')

get_setting = addon.getSetting

show_settings = addon.openSettings

addon_id='plugin.video.velocitykids'   # <<Replace with YOUR addon ID

ADDON = xbmcaddon.Addon(id=addon_id)

execute = xbmc.executebuiltin

addonInfo = xbmcaddon.Addon().getAddonInfo

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))


def get_path():
    return addon.getAddonInfo('path')

def get_profile():
    return addon.getAddonInfo('profile')

def set_setting(id, value):
    #print "SETTING IS =" +value
    if not isinstance(value, basestring): value = str(value)
    addon.setSetting(id, value)

def get_version():
    return addon.getAddonInfo('version')

def get_id():
    return addon.getAddonInfo('id')

def get_name():
    return addon.getAddonInfo('name')

def get_plugin_url(queries):
    try:
        query = urllib.urlencode(queries)
    except UnicodeEncodeError:
        for k in queries:
            if isinstance(queries[k], unicode):
                queries[k] = queries[k].encode('utf-8')
        query = urllib.urlencode(queries)
    return sys.argv[0] + '?' + query

def end_of_directory(cache_to_disc=True):
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=cache_to_disc)


def LogNotify(title,message,times,icon):
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def addDir(name,url,mode,thumb,movie_title,total_items,trakt_id,media,fanart=None,meta_data=None, is_folder=None, is_playable=None, menu_items=None, replace_menu=False):
        #try:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&movie_title="+urllib.quote_plus(movie_title)+"&thumb="+urllib.quote_plus(thumb)+"&trakt_id="+urllib.quote_plus(trakt_id)+"&media="+urllib.quote_plus(media)
            ok=True

            if fanart is None:
                fanart=''
            contextMenuItems = []
            #START METAHANDLER
            if meta_data is None:
                meta_data =[]
            else:
                thumb = meta_data['cover_url']
                fanart = meta_data['backdrop_url']
            if ADDON.getSetting('debug') == "true":
                print u
            if menu_items is None: menu_items = []

            if is_folder is None:
                is_folder = False if is_playable else True

            if is_playable is None:
                playable = 'false' if is_folder else 'true'
            else:
                playable = 'true' if is_playable else 'false'
            list_item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
            list_item.setProperty('fanart_image', fanart)
            if meta_data is None:
                list_item.setInfo('video', {'title': list_item.getLabel()})
            else:
                list_item.setInfo( type="Video", infoLabels=meta_data )
            list_item.setProperty('isPlayable', playable)
            list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, list_item, isFolder=is_folder, totalItems=total_items)
            return ok
        # except Exception as e:
        #     log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        #     if get_setting('error_notify') == "true":
        #         notify(header='List Error',msg='Some items not loaded',duration=5000,sound=None)

def create_item(queries, label, thumb='', fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None, replace_menu=False):
    list_item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
    add_item(queries, list_item, fanart, is_folder, is_playable, total_items, menu_items, replace_menu)

def add_item(queries, list_item, fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None, replace_menu=False):
    if menu_items is None: menu_items = []
    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'

    liz_url = get_plugin_url(queries)
    if fanart: list_item.setProperty('fanart_image', fanart)
    list_item.setInfo('video', {'title': list_item.getLabel()})
    list_item.setProperty('isPlayable', playable)
    list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), liz_url, list_item, isFolder=is_folder, totalItems=total_items)

def parse_query(query):
    q = {'mode': 'main'}
    if query.startswith('?'): query = query[1:]
    queries = urlparse.parse_qs(query)
    for key in queries:
        if len(queries[key]) == 1:
            q[key] = queries[key][0]
        else:
            q[key] = queries[key]
    return q


def notify(header=None, msg='', duration=2000, sound=None):
    if header is None: header = get_name()
    if sound is None:
        sound = get_setting('mute_notifications')
        if sound == 'true':
            sound = False
        else: sound = True
    xbmcgui.Dialog().notification(header, msg, ICON_PATH, duration, sound)
    
def dl_notify(header=None, msg='',icon=None, duration=2000, sound=None):
    if header is None: header = get_name()
    if sound is None:
        sound = get_setting('mute_notifications')
        if sound == 'true':
            sound = False
        else: sound = True
    xbmcgui.Dialog().notification(header, msg, icon, duration, sound)

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)


def addonIcon():
     return artwork+'icon.png'

def infoDialog(message, heading=addonInfo('name'), icon=addonIcon(), time=3000):
    try: dialog.notification(heading, message, icon, time, sound=False)
    except: execute("Notification(%s,%s, %s, %s)" % (heading, message, time, icon))


def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
    return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def okDialog(line1, line2, line3, heading=addonInfo('name')):
    return dialog.ok(heading, line1, line2, line3)

def selectDialog(list, heading=addonInfo('name')):
    return dialog.select(heading, list)


def version():
    num = ''
    try: version = addon('xbmc.addon').getAddonInfo('version')
    except: version = '999'
    for i in version:
        if i.isdigit(): num += i
        else: break
    return int(num)


def refresh():
    return execute('Container.Refresh')


def idle():
    return execute('Dialog.Close(busydialog)')


def queueItem():
    return execute('Action(Queue)')


def openPlaylist():
    return execute('ActivateWindow(VideoPlaylist)')




def openSettings(addon_id, id1=None, id2=None):
    execute('Addon.OpenSettings(%s)' % addon_id)
    if id1 != None:
        execute('SetFocus(%i)' % (id1 + 200))
    if id2 != None:
        execute('SetFocus(%i)' % (id2 + 100))


def auto_view(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if get_setting('auto-view') == 'true':

                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('movies-view') )
                        if content == 'tvshows':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('tvshows-view') )

                        if content == 'episode':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('episode-view') )
                        if content == 'season':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('season-view') )
                        if content == 'menu':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('menu-view') )

                # else:
                #         xbmc.executebuiltin("Container.SetViewMode(%s)" % get_setting('default-view') )
