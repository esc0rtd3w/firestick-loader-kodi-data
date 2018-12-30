'''
    Animal TV Add-on

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
'''

import urllib, pickle, cgi
import os, sys, re, string, random
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs

reload(sys)  
sys.setdefaultencoding('utf8')

addon = xbmcaddon.Addon(id='plugin.video.animaltv')
plugin_path = addon.getAddonInfo('path')
ICON = os.path.join(plugin_path, 'icon.png')
FANART = os.path.join(plugin_path, 'fanart.jpg')

def log(msg, err=False):
    if err:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), 
                 xbmc.LOGERROR)    
    else:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), 
                    xbmc.LOGDEBUG)    
          
def ascii(string):
    if isinstance(string, basestring):
        if isinstance(string, unicode):
           string = string.encode('ascii', 'ignore')
    return string
    
def getProperty(str):
    return xbmcgui.Window(10000).getProperty(str)

def setProperty(str1, str2):
    xbmcgui.Window(10000).setProperty(str1, str2)

def clearProperty(str):
    xbmcgui.Window(10000).clearProperty(str)


def show_dialog(details, title='Animal TV', is_error=False):
    error = ['', '', '']
    text = ''
    for k, v in enumerate(details):
        error[k] = v
        text += v + ' '
    log(text, is_error)
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(title, error[0], error[1], error[2])
    
def get_setting(setting):
    return addon.getSetting(setting)
    
def set_setting(setting, string):
    return addon.setSetting(setting, string)
    
def get_string(string_id):
    return addon.getLocalizedString(string_id)   

def add_video_item(url, infolabels, img=ICON, fanart=FANART, total_items=0, 
                   cm=[], cm_replace=False, HD='Low', playable=True):
    infolabels = decode_dict(infolabels)
    if url.find('://') == -1:
        url = build_plugin_url({'play': url})
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, 
                                thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    if playable:
        listitem.setProperty('IsPlayable', 'true')
        log('Item playable: %s' % (infolabels['title']))
    else:
        listitem.setProperty('IsPlayable', 'false')
        log('Item unplayable: %s' % (infolabels['title']))
    listitem.setArt({'fanart': fanart, 'icon': img})
    if cm:
        listitem.addContextMenuItems(cm, cm_replace)
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, 
                                isFolder=False, totalItems=total_items)

def resolve_url(stream_url):
    xbmcplugin.setResolvedUrl(plugin_handle, True, 
                              xbmcgui.ListItem(path=stream_url))

def end_of_directory():
    xbmcplugin.endOfDirectory(plugin_handle, cacheToDisc=False)

def build_query(queries):
    return '&'.join([k+'='+urllib.quote(str(v)) for (k,v) in queries.items()])
                                
def build_plugin_url(queries):
    url = plugin_url + '?' + build_query(queries)
    return url

def parse_query(query, clean=True):
    queries = cgi.parse_qs(query)
    q = {}
    for key, value in queries.items():
        q[key] = value[0]
    if clean:
        q['mode'] = q.get('mode', 'main')
        q['play'] = q.get('play', '')

    return q

def get_input(title='', default=''):
    kb = xbmc.Keyboard(default, title, False)
    kb.doModal()
    if (kb.isConfirmed()):
        return kb.getText()
    else:
        return False

#http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931
def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data).strip()

def decode_dict(data):
    for k, v in data.items():
        if type(v) is str or type(v) is unicode:
            data[k] = decode(v)
    return data

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
