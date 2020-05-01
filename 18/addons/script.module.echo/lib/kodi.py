"""
    tknorris shared module
    Copyright (C) 2016 tknorris

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
import json
import time
import CustomProgressDialog
from HTMLParser import HTMLParser

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
get_setting = addon.getSetting
show_settings = addon.openSettings
sleep = xbmc.sleep
_log = xbmc.log
dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
datafolder = xbmc.translatePath(os.path.join('special://profile/addon_data/', addon.getAddonInfo('id')))
addonfolder = xbmc.translatePath(os.path.join('special://home/addons/', addon.getAddonInfo('id')))
addonicon = xbmc.translatePath(os.path.join(addonfolder, 'icon.png'))
addonfanart = xbmc.translatePath(os.path.join(addonfolder, 'fanart.jpg'))
handle = int(sys.argv[1])
execute = xbmc.executebuiltin

def busy():
    return execute('ActivateWindow(busydialog)')

def idle():
    return execute('Dialog.Close(busydialog)')

def execute_jsonrpc(command):
    if not isinstance(command, basestring):
        command = json.dumps(command)
    response = xbmc.executeJSONRPC(command)
    return json.loads(response)

def get_path():
    return addon.getAddonInfo('path').decode('utf-8')

def get_profile():
    return addon.getAddonInfo('profile').decode('utf-8')

def translate_path(path):
    return xbmc.translatePath(path).decode('utf-8')

def set_setting(id, value):
    if not isinstance(value, basestring): value = str(value)
    addon.setSetting(id, value)

def accumulate_setting(setting, addend=1):
    cur_value = get_setting(setting)
    cur_value = int(cur_value) if cur_value else 0
    set_setting(setting, cur_value + addend)

def get_version():
    return addon.getAddonInfo('version')

def get_author():
    return addon.getAddonInfo('author')

def get_id():
    return addon.getAddonInfo('id')

def get_name():
    return addon.getAddonInfo('name')

def has_addon(addon_id):
    return xbmc.getCondVisibility('System.HasAddon(%s)' % (addon_id)) == 1
    
def get_kodi_version():
    class MetaClass(type):
        def __str__(self):
            return '|%s| -> |%s|%s|%s|%s|%s|' % (self.version, self.major, self.minor, self.tag, self.tag_version, self.revision)
        
    class KodiVersion(object):
        __metaclass__ = MetaClass
        version = xbmc.getInfoLabel('System.BuildVersion').decode('utf-8')
        match = re.search('([0-9]+)\.([0-9]+)', version)
        if match: major, minor = match.groups()
        match = re.search('-([a-zA-Z]+)([0-9]*)', version)
        if match: tag, tag_version = match.groups()
        match = re.search('\w+:(\w+-\w+)', version)
        if match: revision = match.group(1)
        
        try: major = int(major)
        except: major = 0
        try: minor = int(minor)
        except: minor = 0
        try: revision = revision.decode('utf-8')
        except: revision = u''
        try: tag = tag.decode('utf-8')
        except: tag = u''
        try: tag_version = int(tag_version)
        except: tag_version = 0
    return KodiVersion
        
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

def set_content(content):
    xbmcplugin.setContent(int(sys.argv[1]), content)
    
def create_item(queries, label, thumb='', fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None, replace_menu=False):
    if not thumb: thumb = os.path.join(get_path(), 'icon.png')
    list_item = xbmcgui.ListItem(label, iconImage=thumb, thumbnailImage=thumb)
    add_item(queries, list_item, fanart, is_folder, is_playable, total_items, menu_items, replace_menu)

def add_item(queries, list_item, fanart='', is_folder=None, is_playable=None, total_items=0, menu_items=None, replace_menu=False):
    if not fanart: fanart = os.path.join(get_path(), 'fanart.jpg')
    if menu_items is None: menu_items = []
    if is_folder is None:
        is_folder = False if is_playable else True

    if is_playable is None:
        playable = 'false' if is_folder else 'true'
    else:
        playable = 'true' if is_playable else 'false'

    liz_url = queries if isinstance(queries, basestring) else get_plugin_url(queries)
    if not list_item.getProperty('fanart_image'): list_item.setProperty('fanart_image', fanart)
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

def notify(header=None, msg='', duration=2000, sound=None, icon_path=None):
    if header is None: header = get_name()
    if sound is None: sound = get_setting('mute_notifications') == 'false'
    if icon_path is None: icon_path = os.path.join(get_path(), 'icon.png')
    try:
        xbmcgui.Dialog().notification(header, msg, icon_path, duration, sound)
    except:
        builtin = "XBMC.Notification(%s,%s, %s, %s)" % (header, msg, duration, icon_path)
        xbmc.executebuiltin(builtin)
    
def close_all():
    xbmc.executebuiltin('Dialog.Close(all)')
    
def get_current_view():
    window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    return str(window.getFocusId())

def kodiVersion():

    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version >= 11.0 and version <= 11.9:
        codename = 'Eden'
    elif version >= 12.0 and version <= 12.9:
        codename = 'Frodo'
    elif version >= 13.0 and version <= 13.9:
        codename = 'Gotham'
    elif version >= 14.0 and version <= 14.9:
        codename = 'Helix'
    elif version >= 15.0 and version <= 15.9:
        codename = 'Isengard'
    elif version >= 16.0 and version <= 16.9:
        codename = 'Jarvis'
    elif version >= 17.0 and version <= 17.9:
        codename = 'Krypton'
    else: codename = "Decline"

    return codename

def set_view(content, set_view=False, set_sort=False):
    # set content type so library shows more views and info
    if content:
        set_content(content)

    if set_view:
        view = get_setting('%s_view' % (content))
        if view and view != '0':
            _log('Setting View to %s (%s)' % (view, content), xbmc.LOGDEBUG)
            xbmc.executebuiltin('Container.SetViewMode(%s)' % (view))

    # set sort methods - probably we don't need all of them
    if set_sort:
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_GENRE)

def refresh_container():
    xbmc.executebuiltin("XBMC.Container.Refresh")
    
def update_container(url):
    xbmc.executebuiltin('Container.Update(%s)' % (url))
    
def get_keyboard(heading, default='', hidden=False):
    keyboard = xbmc.Keyboard()
    if hidden: keyboard.setHiddenInput(True)
    keyboard.setHeading(heading)
    if default: keyboard.setDefault(default)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return None

def ulib(string, enc=False):
    try:
        if enc: string = urllib.quote(string)
        else: string = urllib.unquote(string)
        return string
    except: return string

def unicodeEscape(string):
    try:
        string = string.decode("unicode-escape")
        return string
    except: return string

def sortX(string):
    try:
        string = re.sub(r'<.+?>','',string)
        string = string.replace('\\x','REPL').replace('\\','')
        string = re.sub("""REPL[0-f][0-f]""",'',str(part1)) 
        return string
    except: return string
            
def giveColor(text, color, isBold = False):
    if isBold: text = '[B]%s[/B]' % text
    return '[COLOR %s]%s[/COLOR]' % (color,text)

def stripColor(text):
    text = re.sub(r'(\[.+?\])','',text)
    return text
    
def countGitHubIssues(url):
    try:
        import client
        import cache
        import dom_parser2
        c = cache.get(client.request, 1, url)
        r = dom_parser2.parse_dom(c, 'div', {'class': re.compile('table-list-header-toggle\sstates\sfloat-left\spl-\d+')})
        r = dom_parser2.parse_dom(r, 'a')
        r = [re.sub('<.+?>','',i.content).replace('\n','').lstrip() for i in r]
        return 'Issues: %s - %s' % (r[0],r[1])
    except: return 'Issues: ? Open - ? Closed'

def githubLabel(text):

    if text == 'bug': text = '[COLOR orangered]%s[/COLOR]' % text
    if text == 'duplicate': text = '[COLOR grey]%s[/COLOR]' % text
    if text == 'enhancement': text = '[COLOR lightskyblue]%s[/COLOR]' % text
    if text == 'help wanted': text = '[COLOR seagreen]%s[/COLOR]' % text
    if text == 'invalid': text = '[COLOR grey]%s[/COLOR]' % text
    if text == 'question': text = '[COLOR deeppink]%s[/COLOR]' % text
    if text == 'wontfix': text = '[COLOR grey]%s[/COLOR]' % text

    return text

def convertSize(size):
   import math
   if (size == 0):
       return '0 MB'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '%s %s' % (s,size_name[i])
   
def TextBoxes(announce):
    class TextBox():
        WINDOW=10147
        CONTROL_LABEL=1
        CONTROL_TEXTBOX=5
        def __init__(self,*args,**kwargs):
            xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
            self.win=xbmcgui.Window(self.WINDOW) # get window
            xbmc.sleep(500) # give window time to initialize
            self.setControls()
        def setControls(self):
            self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR red]XXX-O-DUS[/COLOR]') # set heading
            try: f=open(announce); text=f.read()
            except: text=announce
            self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
            return
    TextBox()
    while xbmc.getCondVisibility('Window.IsVisible(10147)'):
        time.sleep(.5)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Translations(object):
    def __init__(self, strings):
        self.strings = strings
        
    def i18n(self, string_id):
        try:
            return addon.getLocalizedString(self.strings[string_id]).encode('utf-8', 'ignore')
        except Exception as e:
            xbmc.log('%s: Failed String Lookup: %s (%s)' % (get_name(), string_id, e), xbmc.LOGWARNING)
            return string_id

class WorkingDialog(object):
    wd = None
    
    def __init__(self):
        try:
            self.wd = xbmcgui.DialogBusy()
            self.wd.create()
            self.update(0)
        except:
            xbmc.executebuiltin('ActivateWindow(busydialog)')
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.wd is not None:
            self.wd.close()
        else:
            xbmc.executebuiltin('Dialog.Close(busydialog)')
            
    def is_canceled(self):
        if self.wd is not None:
            return self.wd.iscanceled()
        else:
            return False
        
    def update(self, percent):
        if self.wd is not None:
            self.wd.update(percent)

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
    pd = None
    
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

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
    
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
