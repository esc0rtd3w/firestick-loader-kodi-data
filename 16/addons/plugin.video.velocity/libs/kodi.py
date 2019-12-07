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
import urllib
import urlparse
import sys
import os
from libs import log_utils
import time
import random
import CustomProgressDialog
import re


WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
            'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
            'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
BR_VERS = [
    ['%s.0' % i for i in xrange(18, 43)],
    ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
     '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
     '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
    ['11.0']]

addon = xbmcaddon.Addon()

ICON_PATH = os.path.join(addon.getAddonInfo('path'), 'icon.png')

get_setting = addon.getSetting

show_settings = addon.openSettings

addon_id='plugin.video.velocity'   # <<Replace with YOUR addon ID

ADDON = xbmcaddon.Addon(id=addon_id)

execute = xbmc.executebuiltin

addonInfo = xbmcaddon.Addon().getAddonInfo

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))


sleep = xbmc.sleep




def get_profile():
    return addon.getAddonInfo('profile').decode('utf-8')

def translate_path(path):
    return xbmc.translatePath(path).decode('utf-8')


def get_path():
    return addon.getAddonInfo('path')




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

def addDir(name,url,mode,thumb,movie_title,total_items,trakt_id,media,cover = None,fanart=None,meta_data=None, is_folder=None, is_playable=None, menu_items=None, replace_menu=False, description=None, movie_meta =None,orig_ids=None):
            if orig_ids  is None:
                u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&movie_title=" + urllib.quote_plus(movie_title) + "&thumb=" + urllib.quote_plus(thumb) + "&trakt_id=" + urllib.quote_plus(trakt_id) + "&media=" + urllib.quote_plus(media)#+ "&orig_ids=" + urllib.quote_plus(orig_ids)
            else:
                u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&movie_title=" + urllib.quote_plus(movie_title) + "&thumb=" + urllib.quote_plus(thumb) + "&trakt_id=" + urllib.quote_plus(trakt_id) + "&media=" + urllib.quote_plus(media) + "&orig_ids=" + str(orig_ids)
            ok = True
            if fanart is None:
                fanart=''
            contextMenuItems = []
            #START METAHANDLER
            if meta_data is None:
                #meta_data =[]
                thumb=thumb
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
                list_item.setInfo('video', {'title': list_item.getLabel(),'plot':description})
                list_item.setArt({'poster': thumb, 'fanart_image': fanart, 'banner': 'banner.png'})
            else:
                list_item.setInfo('video', meta_data)
            try:
                list_item.setArt({'poster': meta_data['cover_url'],'fanart_image' : fanart, 'banner': 'banner.png'})
            except: pass
            list_item.setProperty('isPlayable', playable)
            list_item.addContextMenuItems(menu_items, replaceItems=replace_menu)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, list_item, isFolder=is_folder, totalItems=total_items)
            return ok

def addItem(name,url,mode,iconimage,fanart=None,description=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo('video', {'title': liz.getLabel(),'plot':description})
    liz.setProperty( "fanart_image", fanart )
    liz.setArt({'poster': iconimage,'fanart_image' : fanart, 'banner': 'banner.png'})
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok



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


# def auto_view(content):
#         if content:
#                 if get_setting('auto-view') == 'true':
#                     viewsetter.set_view(content)
#                 else:
#                     viewsetter.set_view('sets')


# LIST="list"
# THUMBNAIL="thumbnail"
# MOVIES="movies"
# TV_SHOWS="tvshows"
# SEASONS="seasons"
# EPISODES="episodes"
# OTHER="other"

# def set_content(content):
#     xbmcplugin.setContent(int(sys.argv[1]), content)
#
# def auto_view(content):
#     # set content type so library shows more views and info
#     if content:
#         set_content(content)
#         # xbmcplugin.setContent(int(sys.argv[1]), content)
#
#     view = get_setting('%s_view' % (content))
#     if view != '0':
#         log_utils.log('Setting View to %s (%s)' % (view, content), log_utils.LOGDEBUG)
#         xbmc.executebuiltin('Container.SetViewMode(%s)' % (view))


def slog(msg, level=xbmc.LOGNOTICE):
	name = 'Velocity Scrapers'
	level = xbmc.LOGNOTICE
	try: xbmc.log('%s: %s' % (name, msg), level)
	except:
		try: xbmc.log('Logging Failure', level)
		except: pass  # just give up

def log(msg, level=xbmc.LOGNOTICE):
	name = 'Velocity Information'
	level = xbmc.LOGNOTICE
	try: xbmc.log('%s: %s' % (name, msg), level)
	except:
		try: xbmc.log('Logging Failure', level)
		except: pass  # just give up



def get_ua():
    try: last_gen = int(get_setting('last_ua_create'))
    except: last_gen = 0
    if not get_setting('current_ua') or last_gen < (time.time() - (7 * 24 * 60 * 60)):
        index = random.randrange(len(RAND_UAS))
        user_agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
        log_utils.log('Creating New User Agent: %s' % (user_agent), log_utils.LOGDEBUG)
        set_setting('current_ua', user_agent)
        set_setting('last_ua_create', str(int(time.time())))
    else:
        user_agent = get_setting('current_ua')
    return user_agent



def make_progress_msg(video):
    progress_msg = '%s: %s' % (video.video_type, video.title)
    if video.year: progress_msg += ' (%s)' % (video.year)
    if video.video_type == VIDEO_TYPES.EPISODE:
        progress_msg += ' - S%02dE%02d' % (int(video.season), int(video.episode))
    return progress_msg



def get_keyboard(heading, default=''):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading(heading)
    if default: keyboard.setDefault(default)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return None


class WorkingDialog(object):
    def __init__(self):
        xbmc.executebuiltin('ActivateWindow(busydialog)')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        xbmc.executebuiltin('Dialog.Close(busydialog)')


class ProgressDialog(object):
    pd = None


    def __init__(self, heading, line1='', line2='', line3='', background=False, active=True, timer=0):
        self.begin = time.time()
        self.timer = timer
        self.background = background
        self.heading = heading
        if active and not timer:
            self.pd = self.__create_dialog(line1, line2, line3)
            self.pd.update(0)
        else:
            self.pd = None

    def __create_dialog(self, line1, line2, line3):
        if self.background:
            pd = xbmcgui.DialogProgressBG()
            msg = line1 + line2 + line3
            pd.create(self.heading, msg)
        else:
            if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
                pd = CustomProgressDialog.ProgressDialog()
            else:
                pd = xbmcgui.DialogProgress()
            pd.create(self.heading, line1, line2, line3)
        return pd

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd

    def is_canceled(self):
        if self.pd is not None and not self.background:
            return self.pd.iscanceled()
        else:
            return False

    def update(self, percent, line1='', line2='', line3=''):
        if self.pd is None and self.timer and (time.time() - self.begin) >= self.timer:
            self.pd = self.__create_dialog(line1, line2, line3)

        if self.pd is not None:
            if self.background:
                msg = line1 + line2 + line3
                self.pd.update(percent, self.heading, msg)
            else:
                self.pd.update(percent, line1, line2, line3)


class CountdownDialog(object):
    __INTERVALS = 5

    def __init__(self, heading, line1='', line2='', line3='', active=True, countdown=60, interval=5):
        self.heading = heading
        self.countdown = countdown
        self.interval = interval
        self.line3 = line3
        if active:
            if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
                pd = CustomProgressDialog.ProgressDialog()
            else:
                pd = xbmcgui.DialogProgress()
            if not self.line3: line3 = 'Expires in: %s seconds' % (countdown)
            pd.create(self.heading, line1, line2, line3)
            pd.update(100)
            self.pd = pd
        else:
            self.pd = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd

    def start(self, func, args=None, kwargs=None):
        if args is None: args = []
        if kwargs is None: kwargs = {}
        result = func(*args, **kwargs)
        if result:
            return result

        start = time.time()
        expires = time_left = int(self.countdown)
        interval = self.interval
        while time_left > 0:
            for _ in range(CountdownDialog.__INTERVALS):
                sleep(interval * 1000 / CountdownDialog.__INTERVALS)
                if self.is_canceled(): return
                time_left = expires - int(time.time() - start)
                if time_left < 0: time_left = 0
                progress = time_left * 100 / expires
                line3 = 'Expires in: %s seconds' % (time_left) if not self.line3 else ''
                self.update(progress, line3=line3)

            result = func(*args, **kwargs)
            if result:
                return result

    def is_canceled(self):
        if self.pd is None:
            return False
        else:
            return self.pd.iscanceled()

    def update(self, percent, line1='', line2='', line3=''):
        if self.pd is not None:
            self.pd.update(percent, line1, line2, line3)


# class CountdownDialog(object):
#     __INTERVALS = 5
#     pd = None
#
#     def __init__(self, heading, line1='', line2='', line3='', active=True, countdown=60, interval=5):
#         self.heading = heading
#         self.countdown = countdown
#         self.interval = interval
#         self.line3 = line3
#         if active:
#             if xbmc.getCondVisibility('Window.IsVisible(progressdialog)'):
#                 pd = CustomProgressDialog.ProgressDialog()
#             else:
#                 pd = xbmcgui.DialogProgress()
#             if not self.line3: line3 = 'Expires in: %s seconds' % (countdown)
#             pd.create(self.heading, line1, line2, line3)
#             pd.update(100)
#             self.pd = pd
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, type, value, traceback):
#         if self.pd is not None:
#             self.pd.close()
#
#     def start(self, func, args=None, kwargs=None):
#         if args is None: args = []
#         if kwargs is None: kwargs = {}
#         result = func(*args, **kwargs)
#         if result:
#             return result
#
#         start = time.time()
#         expires = time_left = int(self.countdown)
#         interval = self.interval
#         while time_left > 0:
#             for _ in range(CountdownDialog.__INTERVALS):
#                 sleep(interval * 1000 / CountdownDialog.__INTERVALS)
#                 if self.is_canceled(): return
#                 time_left = expires - int(time.time() - start)
#                 if time_left < 0: time_left = 0
#                 progress = time_left * 100 / expires
#                 line3 = 'Expires in: %s seconds' % (time_left) if not self.line3 else ''
#                 self.update(progress, line3=line3)
#
#             result = func(*args, **kwargs)
#             if result:
#                 return result
#
#     def is_canceled(self):
#         if self.pd is None:
#             return False
#         else:
#             return self.pd.iscanceled()
#
#     def update(self, percent, line1='', line2='', line3=''):
#         if self.pd is not None:
#             self.pd.update(percent, line1, line2, line3)


def to_slug(username):
    username = username.strip()
    username = username.lower()
    username = re.sub('[^a-z0-9_]', '-', username)
    username = re.sub('--+', '-', username)
    return username


def message(text1, text2="", text3=""):
    if text3 == "":
        xbmcgui.Dialog().ok(text1, text2)
    elif text2 == "":
        xbmcgui.Dialog().ok("", text1)
    else:
        xbmcgui.Dialog().ok(text1, text2, text3)
