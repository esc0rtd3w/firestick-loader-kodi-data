'''
    Ice Channel
'''
import os    
import sys
from addon import Addon
from md_tools import md

addon_id = 'script.icechannel'

md = md(addon_id)

try:
    addon = Addon(addon_id, sys.argv)
except:
    addon = Addon(addon_id)

addon_path = addon.get_path()
addon_version = addon.get_version()

lib_path = os.path.join(addon_path, 'lib', 'entertainment')
plugins_path = os.path.join(lib_path, 'plugins')
settings_file = os.path.join(addon_path, 'resources', 'settings.xml')

profile_path = addon.get_profile()

theme_name = addon.get_setting('theme')
theme_type = addon.get_setting(theme_name+'_themetype')
if theme_type == 'online':
    icon_path = addon.get_setting(theme_name+'_themeurl'+'icons')
    fanart_path = addon.get_setting(theme_name+'_themeurl'+'fanart')
else:
    theme_addon = Addon( addon.get_setting(theme_name+'_themeaddon') )
    icon_path = os.path.join(theme_addon.get_path(), 'theme', 'icons')
    fanart_path = os.path.join(theme_addon.get_path(), 'theme', 'fanart')

def get_themed_icon(icon_file_name):
    if icon_path.startswith('http'):
        icon = icon_path + icon_file_name
    else:
        icon = os.path.join(icon_path, icon_file_name)
        #if not os.path.exists( icon ):
        #    icon = 'https://istream-xbmc-repo.googlecode.com/svn/images/' + icon_file_name
    if not os.path.exists(icon):
        icon = os.path.join(icon_path, 'icon.png')
    return icon

def get_themed_fanart(fanart_file_name):
    if fanart_path.startswith('http'):
        fanart = fanart_path + fanart_file_name
    else:
        fanart = os.path.join(fanart_path, fanart_file_name)
    if not os.path.exists(fanart):
        fanart = os.path.join(fanart_path, 'fanart.jpg')
    return fanart
    
icon = get_themed_icon('icon.png')    
notify_icon = get_themed_icon('notifyicon.png')

# INDEXERS
indxr_Movies = 'movies'
indxr_TV_Shows = 'tv_shows'
indxr_Sports = 'sports'
indxr_Lists = 'lists'
indxr_Live_TV = 'live_tv'

# SOURECS
src_Movies = 'movies'
src_TV_Shows = 'tv_shows'
src_Sports = 'sports'
src_Live_TV = 'live_tv'

# SETTINGS
settings_Movies = 'movies'
settings_TV_Shows = 'tv_shows'
settings_Sports = 'sports'
settings_Lists = 'lists'
settings_About = 'about'
settings_XBMC_Integration = 'xbmcintegration'
settings_Live_TV = 'live_tv'
settings_Internet_Connection = 'internetconnection'

# MODES
mode_Main = 'main'
mode_Indexer = 'indexer'
mode_Section = 'section'
mode_Content = 'content'
mode_Info = 'info'
mode_File_Hosts = 'file_hosts'
mode_Play = 'play'
mode_Play_Trailer = 'play_trailer'
mode_Search = 'search'
mode_Settings = 'settings'
mode_Dummy = 'dummy'
mode_Sports = 'sports'
mode_Sports_Links = 'sports_links'
mode_Change_Watched = 'change_watched'
mode_Refresh_Meta = 'refresh_meta'
mode_Add_To_Favorites = 'add_to_favorites'
mode_Add_To_Library = 'add_to_library'
mode_Subscribe = 'subscribe'
mode_Unsubscribe = 'unsubscribe'
mode_Manage_Subs = 'manage_subs'
mode_Update_Subs = 'update_subs'
mode_Clean_Up_Subs = 'clean_up_subs'
mode_File_Stores = 'file_stores'
mode_Add_File_Store = 'add_file_stores'
mode_Add_Http_File_Store = 'add_http_file_stores'
mode_Add_Local_File_Store = 'add_local_file_stores'
mode_Read_File = 'read_file'
mode_Read_File_Item = 'read_file_item'
mode_Rename_File_Item = 'rename_file_item'
mode_Play_File_Item = 'play_file_item'
mode_Read_File_Item_2 = 'read_file_item_2'
mode_Add_File_Item = 'add_file_item'
mode_Remove_File_Item = 'remove_file_item'
mode_Remove_Play_List_Source = 'remove_playlist_source'
mode_Play_List_Sources = 'playlist_sources'
mode_Play_Lists = 'playlists'
mode_Live_TV = 'live_tv'
mode_Live_TV_Regions = 'live_tv_regions'
mode_Live_TV_Region = 'live_tv_region'
mode_Live_TV_Languages = 'live_tv_languages'
mode_Live_TV_Language = 'live_tv_language'
mode_Live_TV_Genres = 'live_tv_genres'
mode_Live_TV_Genre = 'live_tv_genre'
mode_Live_TV_Links = 'live_tv_links'
mode_Hide_Channel = 'hide_channel'
mode_Tools = 'tools'
mode_Installer = 'installer'
mode_EULA = 'EULA'
mode_iStream = 'istream'
mode_MyStream = 'mystream'
mode_Add_to_MyStream = 'add_to_mystream'
mode_Remove_from_MyStream = 'remove_from_mystream'
mode_Rename_MyStream_Item = 'rename_mystream_item'
mode_Reload_Plugins = 'reload_plugins'

# SECTIONS
id_Section_Main = 'main'

# VIDEO TYPES FOR META-DATA
VideoType_Movies = 'movie'
VideoType_TV = 'tvshow'
VideoType_Season = 'season'
VideoType_Episode = 'episode'

# Global Peoperties
gb_Lib_Subs_Op_Running = 'lib_subs_op_running'
gb_Local_Proxy_Server_Running = 'local_proxy_server_running'

playlist_content_map = {
        'MovieSource':'_mvs',
        'LiveTVSource':'_ltvs'
    }

### PARTIAL PLUGIN LOADING

def loadplugins( interfaces=[] ):    

    import time
    if not interfaces or len(interfaces) <= 0: return
    
    plugin_dirs = [plugins_path]
    from glob import glob
    plugin_dirs.extend( glob( os.path.join( os.path.dirname(addon_path), addon_id + '.extn.*', 'plugins' ) ) )
    
    import plugnplay
    plugnplay.set_plugin_dirs(*plugin_dirs)

    len_ifcs = len(interfaces)
    if len_ifcs == 1:
        interface = interfaces[0]
        plugnplay.load_plugins(interface.filecode)
    elif len_ifcs > 1:
        ifcs = []
        for interface in interfaces:
            ifcs.append(interface.filecode)
        plugnplay.load_plugins(ifcs)

        
def loadpluginsNew(interfaces=[]):
    plugin_dirs = addon.get_setting("plugins_dirs").split(",")
    plugins_list = []
    
    for interface in interfaces:
        plugin_fc_dirs = addon.get_setting( "plugins_dirs"+interface.filecode).split(",")
        plugin_dirs.extend(plugin_fc_dirs)
        
        plugin_fc_list = addon.get_setting( "plugins"+interface.filecode).split(",")
        plugins_list.extend(plugin_fc_list)
    
    import plugnplay
    plugnplay.load_plugins_new(plugin_dirs, plugins_list)
        
def PreLoadiStreamPlugins(message_queue=None):

    plugin_dirs = [plugins_path]
    from glob import glob
    plugin_dirs.extend( glob( os.path.join( os.path.dirname(addon_path), addon_id + '.extn.*', 'plugins' ) ) )
    
    progress_step =  len( plugin_dirs )
    progress_step = 50 / progress_step
    
    
    plugins_dict = {}
    plugin_dirs_dict = {}
    
    filecodes = ['_xstrc','_xstrs','_tls','_prx','_wpx','_hrv','_prv','_chr','_lrv','_ffm','_cst','_ist','_lsi','_mvi','_tvi','_ltvi','_lspi','_mvs','_tvs','_ltvs','_lsps']
    
    i = 1
    found = 0
    for plugin_dir in plugin_dirs:
        for dirpath, dirnames, files in os.walk(plugin_dir):
            for f in files:
                if f.endswith('.py'):
                    for filecode in filecodes:
                        if filecode in f: 
                            found+=1
                            dirlist = plugin_dirs_dict.get(filecode, None)
                            if dirlist:
                                dirlist.append(dirpath)
                            else:
                                newdirlist = []
                                newdirlist.append(dirpath)
                                plugin_dirs_dict.update( { filecode:newdirlist } )
                                
                            plgnlist = plugins_dict.get(filecode, None)
                            if plgnlist:
                                plgnlist.append(f[:-3])
                            else:
                                newplgnlist = []
                                newplgnlist.append(f[:-3])
                                plugins_dict.update( { filecode:newplgnlist } )
        if i>5: i=3
        if message_queue:
            message_queue.put( {'line1':'Loading plugins... ', 
                    'line2':'[B]Searching%s[/B]' % (i*'...',), 
                    'line3':'[I][COLOR gray]Found: %s plugin(s)[/COLOR][/I]' % found,
                    'wait_time':100,
                    'percent_step':progress_step
                    } )
    addon.set_setting( "plugins_dirs", ','.join(plugin_dirs) )
    
    for k, v in plugin_dirs_dict.iteritems():
        addon.set_setting( "plugins_dirs"+k, ','.join(v) )
        
    for k, v in plugins_dict.iteritems():
        addon.set_setting( "plugins"+k, ','.join(v) )
        
    if message_queue:
        message_queue.put( 'done' )
    
def make_dir(mypath, dirname):
    ''' Creates sub-directories if they are not found. '''
    import xbmcvfs
    
    if not xbmcvfs.exists(mypath): 
        try:
            xbmcvfs.mkdirs(mypath)
        except:
            xbmcvfs.mkdir(mypath)
    
    subpath = os.path.join(mypath, dirname)
    
    if not xbmcvfs.exists(subpath): 
        try:
            xbmcvfs.mkdirs(subpath)
        except:
            xbmcvfs.mkdir(subpath)
            
    return subpath
    
cookies_path = make_dir(profile_path, 'cookies')    
captchas_path = make_dir(profile_path, 'captchas')
temp_path = make_dir(profile_path, 'temp')

def CleanText(text, strip=False, remove_non_ascii=False):
    from entertainment import htmlcleaner
    import urllib
    text = htmlcleaner.clean( urllib.unquote_plus(text), strip, remove_non_ascii )
    return text    
    
def CleanText2(text, strip=False, remove_non_ascii=False):
    from entertainment import htmlcleaner
    import urllib
    text = htmlcleaner.clean2( urllib.unquote_plus(text), strip, remove_non_ascii )
    return text    

def CreateIdFromString(str):
    str = CleanText(str, False, True)
    import re
    id = re.sub('[^0-9a-zA-Z]+', '_', str).lower()
    if id.endswith('_'): id = id[:-1]
    
    return id
    
def CleanTextForSearch(text, strip=False, remove_non_ascii=False):
    from entertainment import htmlcleaner
    import urllib
    text = htmlcleaner.clean( urllib.unquote_plus(text), strip, remove_non_ascii )
    return text
    
def GetDomainFromUrl(url):
    import re
    domain = re.sub('(http://|https://|http://www.|https://www.|www.)', '', url)
    domain = re.sub('/.*', '', domain)
    if domain[len(domain)-1] == ':': domain = domain[:-1]
    if re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', domain): domain = 'ip'
    return domain.upper()
    
def GetBaseUrlFromUrl(url):
    import re
    index = url.find('/', url.find('.')) + 1
    base_url = url[:index]
    if not base_url.endswith('/') : base_url = base_url + '/'
    return base_url
    
    
def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\r": "",            
                   "\n": "",
                   "\t": ""
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            import re
            text = re.sub(r"<!--.+?-->", "", text)    

        except TypeError:
            pass

        return text

def str_conv(data):
    if isinstance(data, str):
        # Must be encoded in UTF-8
        data = data.decode('utf8', 'ignore')
    import unicodedata
    data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
    data = data.decode('string-escape')
    return data
    
##### DECODE / ENCODE LIST
########## START
def encode_item_for_list(item):
    if isinstance(item, str) or isinstance(item, unicode) :
        if item.find(',') >= 0:
            item = item.replace(',', '<listcomma>')
    return item
    
def decode_item_for_list(item):
    if isinstance(item, str) or isinstance(item, unicode) :            
        if item.find('<listcomma>') >= 0:
            item = item.replace('<listcomma>', ',')
    return item
    
def encode_list(in_list):
    out_list = []
    for item in in_list:
        if isinstance(item, dict):
            out_list.append( encode_item_for_list( ConvertDictToString(item) ) )
        else:
            out_list.append( encode_item_for_list(item) )
        
    return out_list
    
def decode_list(in_list):
    out_list = []
    
    for item in in_list:
        if item[1] == '{' and item[len(item)-2] == '}': 
            item = item[1:len(item)-1]
            out_list.append( ConvertStringToDict( decode_item_for_list(item) ) )
        else:
            out_list.append( decode_item_for_list(item) )

    return out_list

def ConvertListToString(in_list):
    return str ( encode_list(in_list) )
    
def ConvertStringToList(in_string):

    in_string = in_string.replace(' , ', ',')
    in_string = in_string.replace(', ', ',')
    in_string = in_string.replace(' ,', ',')
    in_string = in_string[1:len(in_string)-1]

    return decode_list ( in_string.split(',') )

########## END
##### ENCODE / DECODE LIST


##### ENCODE / DECODE DICT
########## START
def encode_dict(dict):
    out_dict = {}
    for k, v in dict.iteritems():
        if isinstance(k, str) or isinstance(k, unicode) :            
            k = str_conv(k)
            if k.find(',') >= 0:
                k = k.replace(',', '<dictcomma>')
            if k.find("'") >= 0:
                k = k.replace("'", '<squot>')
            if k.find('"') >= 0:
                k = k.replace('"', '<dquot>')
            if k.find('{') >= 0:
                k = k.replace('{', '<ltbrc>')
            if k.find('}') >= 0:
                k = k.replace('}', '<rtbrc>')
            if k.find(':') >= 0:
                k = k.replace(':', '<colon>')
        if isinstance(v, str) or isinstance(v, unicode) :            
            v = str_conv(v)
            if v.find(',') >= 0:
                v = v.replace(',', '<dictcomma>')
            if v.find("'") >= 0:
                v = v.replace("'", '<squot>')
            if v.find('"') >= 0:
                v = v.replace('"', '<dquot>')
            if v.find('{') >= 0:
                v = v.replace('{', '<ltbrc>')
            if v.find('}') >= 0:
                v = v.replace('}', '<rtbrc>')
            if v.find(':') >= 0:
                v = v.replace(':', '<colon>')
        out_dict[k] = v
    return out_dict
    
def decode_dict(dict):
    out_dict = {}
    for k, v in dict.iteritems():
        if isinstance(k, str) or isinstance(k, unicode):
            k = str_conv(k)
            if k.find('<dictcomma>') >= 0:
                k = k.replace('<dictcomma>', ',')
            if k.find("<squot>") >= 0:
                k = k.replace("<squot>", "'")
            if k.find('<dquot>') >= 0:
                k = k.replace("<dquot>", '"')
            if k.find('<ltbrc>') >= 0:
                k = k.replace('<ltbrc>', '{')
            if k.find('<rtbrc>') >= 0:
                k = k.replace('<rtbrc>', '}')
            if k.find('<colon>') >= 0:
                k = k.replace('<colon>', ':')
        if isinstance(v, str) or isinstance(v, unicode):
            v = str_conv(v)
            if v.find('<dictcomma>') >= 0:
                v = v.replace('<dictcomma>', ',')
            if v.find("<squot>") >= 0:
                v = v.replace("<squot>", "'")
            if v.find('<dquot>') >= 0:
                v = v.replace("<dquot>", '"')
            if v.find('<ltbrc>') >= 0:
                v = v.replace('<ltbrc>', '{')
            if v.find('<rtbrc>') >= 0:
                v = v.replace('<rtbrc>', '}')
            if v.find('<colon>') >= 0:
                v = v.replace('<colon>', ':')        
        out_dict[k] = v
    return out_dict    

def ConvertDictToString(in_dict):
    return str ( encode_dict(in_dict) )
    
def ConvertStringToDict(in_string):
    
    try:
        import json
    except:
        import simplejson as json
        
    import re
        
    return decode_dict ( json.loads(re.sub(r",\s*(\w+)", r", '\1'", re.sub(r"\{(\w+)", r"{'\1'", in_string.replace('\\','\\\\'))).replace("'", '"')) )
    
def dict_to_paramstr(dict):
    out_dict = {}
    for k, v in dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    
    import urllib    
    return urllib.urlencode(out_dict)
    
def parse_query(query):
    import cgi
    queries = cgi.parse_qs(query)
    q = {}
    for key, value in queries.items():
        if len(value) == 1:
            q[key] = value[0]
        else:
            q[key] = value
    return q
########## END
##### ENCODE / DECODE DICT

def ttTTtt(i, t1, t2=[]):
    t = ''
    for c in t1:
        t += chr(c)
        i += 1
        if i > 1:
            t = t[:-1]
            i = 0  
    for c in t2:
        t += chr(c)
        i += 1
        if i > 1:
            t = t[:-1]
            i = 0
    return t

# TIMEZONE OFFSET
def get_gmt_offset():
    import time
    t = time.time()
    
    gmt_offset = 0
    
    if time.localtime(t).tm_isdst and time.daylight:
        gmt_offset = time.altzone
    else:
        gmt_offset = time.timezone
        
    gmt_offset = gmt_offset / 60 / 60 * -1
    
    return gmt_offset
    
class Threaded_Notification:
    def __init__(self, duration=1000, msg='Working', msg2=''):
        import threading
        self._task_complete = threading.Event()
        
        self._title = '[COLOR white]' + msg + '[/COLOR]' 
        self._msg2 = '[COLOR orange]' + msg2 + '[/COLOR]'
        self._duration = duration
        self._icon = notify_icon
        
        self._completion_msg1 = ''
        self._completion_msg2 = ''
        
        self._progress_symbol = '*'
        self._progress_count = 5
        self._progress_current_index = 0
        
        threading.Thread(target=self.show_xunity_working_notification).start()
        
    def SetTaskCompletionMessage(self, msg1, msg2):
        self._completion_msg1 = '[COLOR white]' + msg1 + '[/COLOR]'
        self._completion_msg2 = '[COLOR orange]' + msg2 + '[/COLOR]'
    
    def SetTaskCompletion(self, completion_msg1='Completed', completion_msg2=''):
        self.SetTaskCompletionMessage(completion_msg1, completion_msg2)
        self._task_complete.set()
        
    def SetMessage2(self, msg):
        self._msg2 = '[COLOR orange]' + msg + '[/COLOR]'
        
    def _check_exit_status(self):
        import xbmc
        return ( self._task_complete.isSet() or xbmc.abortRequested)
        
    def _generate_indicator(self):
        if self._progress_current_index > self._progress_count:
            self._progress_current_index = 1
        else:    
            self._progress_current_index += 1
        return ' [B][[COLOR gray]' + ( (self._progress_current_index-1) * self._progress_symbol) + '[/COLOR][COLOR cyan]' + self._progress_symbol + '[/COLOR][COLOR gray]' + ( (self._progress_count-(self._progress_current_index-1)) * self._progress_symbol) + '[/COLOR]][/B]'
                
    def show_xunity_working_notification(self):
        import xbmc
        
        msg = self._generate_indicator()
        addon.show_small_popup(self._title + msg, self._msg2, self._duration, self._icon)
        
        while not self._check_exit_status():
            xbmc.sleep(self._duration)
            msg = self._generate_indicator()
            if self._check_exit_status(): break;
            addon.show_small_popup(self._title + msg, self._msg2, self._duration, self._icon)
            
        addon.show_small_popup(self._completion_msg1, self._completion_msg2, self._duration, self._icon)
            

    
def notify(addon_id, typeq, title, message, times, line2='', line3=''):
    import xbmc
    addon_tmp = Addon(addon_id)
    if title == '' :
        title='[B]' + addon_tmp.get_name() + '[/B]'
    if typeq == 'small':
        if times == '':
           times='5000'
        smallicon= notify_icon
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+smallicon+")")
    elif typeq == 'big':
        dialog = xbmcgui.Dialog()
        dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok(' '+title+' ', ' '+message+' ')        
        
def SetScriptOnAlarm(name, path, args='1', duration=1440):    
    import xbmc
    cmd       = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, path, args, duration)
    xbmc.executebuiltin(cmd)
    
def GetTotalMinutesFromTimeDelta(td):
    td_total_mins = ( td.days * 24 * 60 ) + ( td.seconds / 60 )    
    td_total_mins = int(td_total_mins)
    if td_total_mins <= 0: td_total_mins = 1
    return td_total_mins
    
def SetGlobalProperty(id, value):
    import xbmcgui
    win = xbmcgui.Window(10000)
    win.setProperty(addon_id + '.' + id, str(value) )
    
def GetGlobalProperty(id):
    import xbmcgui
    win = xbmcgui.Window(10000)
    return win.getProperty(addon_id + '.' + id)
    
def ClearGlobalProperty(id):
    import xbmcgui
    win = xbmcgui.Window(10000)
    win.clearProperty(addon_id + '.' + id)
    
def GetEpochStr():
    import datetime
    time_now=datetime.datetime.now()
    
    import time
    epoch=time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
    
    epoch_str = str('%f' % epoch)
    epoch_str = epoch_str.replace('.','')
    epoch_str = epoch_str[:-3]

    return epoch_str

from entertainment import odict
quality_dict = odict.odict({
    'ts'            : 'TS',
    'hdts'          : 'TS',
    'tsrip'         : 'TS',
    'cam'           : 'CAM',
    'camrip'        : 'CAM',
    'hdcam'         : 'CAM',
    'dvdscr'        : 'DVD',
    'dvdrip'        : 'DVD',
    'dvd'           : 'DVD',
    'brrip'         : 'HD',
    'bdrip'         : 'HD',
    'bluray'        : 'HD',
    'hd'            : 'HD',
    '720p'          : '720P',
    '1080p'         : '1080P',
    '3d'            : '3D',
    '4k'            : '3K'
    })
    
movie_container_dict = odict.odict( {    
    'mkv'           : 'MKV',
    'mp4'           : 'MP4',
    'avi'           : 'AVI'
    })
        
def RemoveNonAscii(text):
    import re
    cleaned = re.sub(r'[^\x00-\x7F]+',' ', text)
    return cleaned
    
def makeGUID():
    import random
    guid = ''
    for i in range(8):
        number = "%X" % (int( ( 1.0 + random.random() ) * 0x10000) | 0)
        guid += number[1:]
    return guid
    
def AES(key):
    from crypto.cipher.base import padWithPadLen
    from crypto.cipher.rijndael import Rijndael
    return Rijndael(key, keySize=32, blockSize=16, padding=padWithPadLen())

def AES_CBC(key):
    from crypto.cipher.cbc import CBC
    return CBC(blockCipherInstance=AES(key))    
    
def handle_captcha(url, html, params=None):
    '''
    return dict, possible values
    1. {'status':'none'} - No captcha Found.
    2. {'status':'error', 'message':'<error message>', 'captch_type':'<which captcha was found>'} 
    3. {'status':'error', 'message':'<error message>', 'captch_type':'<which captcha was found>, 
            'captcha':<the self resolved or user entered captcha value>, 
            ... (any other paramters found to go with captcha for e.g adcopy_challenge:hugekey incase of solvemedia)
        } 
    '''
    captcha_dict = {'status':'none'}
    captcha_resolved = False
    
    from entertainment.plugnplay.interfaces import CaptchaHandler
    for ch in CaptchaHandler.implementors():
        captcha_resolved = ch.CanHandle(url, html, params=params)
        if captcha_resolved == True:
            captcha_dict = ch.Handle(url, html, params=params)
            if captcha_dict:
                break
            else:
                captcha_resolved = False
                
    return captcha_dict
    
def start_local_proxy(op, code):
    SetGlobalProperty(gb_Local_Proxy_Server_Running, 'True')
    filestring = 'XBMC.RunScript(' + os.path.join(lib_path,'proxy.py') + ',' + op + ',' + code + ', 12345)'
    import xbmc
    xbmc.executebuiltin(filestring) 
    import time
    time.sleep(20)
    return 'http://localhost:12345/'
    
def stop_local_proxy():
    is_local_proxy_server_running = GetGlobalProperty(gb_Local_Proxy_Server_Running)
    if is_local_proxy_server_running and is_local_proxy_server_running == 'True':
        import time
        time.sleep(10)
        from entertainment.net import Net
        net = Net(cached=False)
        try: net.http_GET('http://localhost:12345/stop')
        except: pass
        ClearGlobalProperty(gb_Local_Proxy_Server_Running)

def GetiStreamSettings(type=None, id=None):
    if not type: return ''
    
    ret_val = ''
    from plugnplay.interfaces import iStreamSettings
    for cs in iStreamSettings.implementors(): 
        cs.Initialize()
        if cs.type == type:
            try:
                cs.Get()
            except:
                import xbmc
                xbmc.executebuiltin('UpdateLocalAddons ')
            
            if not id:
                ret_val = cs
            elif id:
                ret_val = cs.Settings().get_setting(id)
            break
            
    return ret_val
    
def custom_item_sort(name):
    name = name.lower()
    import re
    name = re.sub('\[/?(?:color|b|i)[^\]]*\]', '', name)
    return name
    
def ShowFeatureNotAvlblDialog(header='iStream: Feature Not Available'):
    from istreams.dialogs import DialogiStreamFeatureNotAvlbl
    DialogiStreamFeatureNotAvlbl.show(header=header)
    
def _update_settings_xml():
    '''
    This function writes a new ``resources/settings.xml`` file which contains
    all settings for this addon and its plugins.
    '''
    try:
        try:
            os.makedirs(os.path.dirname(settings_file))
        except OSError:
            pass
            
        account_settings = ''

        f = open(settings_file, 'w')
        try:
            f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write('<settings>\n')    
                        
            f.write('<category label="General">\n')                        
            f.write('<setting type="sep" visible="false"/>\n')
            f.write('<setting id="istream_first_run" type="bool" label="iStream First Run" default="true" visible="false"/>\n')
            
            f.write('<setting id="plugin_load_timestamp" type="text" label="Plugin Load Timestamp" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs" type="text" label="Plugins Dirs" default="" visible="false"/>\n')
            
            f.write('<setting id="plugins_xstrc" type="text" label="Plugins_xstrc" default="" visible="false"/>\n')
            f.write('<setting id="plugins_xstrs" type="text" label="Plugins_xstrs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_tls" type="text" label="Plugins_tls" default="" visible="false"/>\n')
            f.write('<setting id="plugins_prx" type="text" label="Plugins_prx" default="" visible="false"/>\n')
            f.write('<setting id="plugins_wpx" type="text" label="Plugins_wpx" default="" visible="false"/>\n')
            f.write('<setting id="plugins_hrv" type="text" label="Plugins_hrv" default="" visible="false"/>\n')
            f.write('<setting id="plugins_prv" type="text" label="Plugins_prv" default="" visible="false"/>\n')
            f.write('<setting id="plugins_chr" type="text" label="Plugins_chr" default="" visible="false"/>\n')
            f.write('<setting id="plugins_lrv" type="text" label="Plugins_lrv" default="" visible="false"/>\n')
            f.write('<setting id="plugins_ffm" type="text" label="Plugins_ffm" default="" visible="false"/>\n')
            f.write('<setting id="plugins_cst" type="text" label="Plugins_cst" default="" visible="false"/>\n')
            f.write('<setting id="plugins_ist" type="text" label="Plugins_ist" default="" visible="false"/>\n')
            f.write('<setting id="plugins_lsi" type="text" label="Plugins_lsi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_mvi" type="text" label="Plugins_mvi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_tvi" type="text" label="Plugins_tvi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_ltvi" type="text" label="Plugins_ltvi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_lspi" type="text" label="Plugins_lspi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_mvs" type="text" label="Plugins_mvs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_tvs" type="text" label="Plugins_tvs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_ltvs" type="text" label="Plugins_ltvs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_lsps" type="text" label="Plugins_lsps" default="" visible="false"/>\n')
                                                                                            
            f.write('<setting id="plugins_dirs_xstrc" type="text" label="Plugins Dirs_xstrc" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_xstrs" type="text" label="Plugins Dirs_xstrs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_tls" type="text" label="Plugins Dirs_tls" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_prx" type="text" label="Plugins Dirs_prx" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_wpx" type="text" label="Plugins Dirs_wpx" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_hrv" type="text" label="Plugins Dirs_hrv" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_prv" type="text" label="Plugins Dirs_prv" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_chr" type="text" label="Plugins Dirs_chr" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_lrv" type="text" label="Plugins Dirs_lrv" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_ffm" type="text" label="Plugins Dirs_ffm" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_cst" type="text" label="Plugins Dirs_cst" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_ist" type="text" label="Plugins Dirs_ist" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_lsi" type="text" label="Plugins Dirs_lsi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_mvi" type="text" label="Plugins Dirs_mvi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_tvi" type="text" label="Plugins Dirs_tvi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_ltvi" type="text" label="Plugins Dirs_ltvi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_lspi" type="text" label="Plugins Dirs_lspi" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_mvs" type="text" label="Plugins Dirs_mvs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_tvs" type="text" label="Plugins Dirs_tvs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_ltvs" type="text" label="Plugins Dirs_ltvs" default="" visible="false"/>\n')
            f.write('<setting id="plugins_dirs_lsps" type="text" label="Plugins Dirs_lsps" default="" visible="false"/>\n')

            
            f.write('<setting id="Default_themetype" type="text" label="Theme Type" default="online" visible="false"/>\n')
            f.write('<setting id="Default_themeurl" type="text" label="Theme URL" default="https://raw.githubusercontent.com/mucky-duck/istream/master/images/default/" visible="false"/>\n')
            f.write('<setting id="Default_themeaddon" type="text" label="Theme Addon" default="" visible="false"/>\n')            
            
            themes = 'Default'
            
            from glob import glob
            import re
            theme_infos = glob( os.path.join( os.path.dirname(addon_path), addon_id + '.theme.*', 'theme', 'theme.info' ) ) 
            for theme_info in theme_infos:
                info_Obj = open(theme_info, 'r')
                info = info_Obj.read()
                info_Obj.close()
                
                theme_name = re.search('name=(.*)', info).group(1)                
                theme_online = re.search('online=(.*)', info).group(1).lower()                
                
                theme_addon_id = re.search('addon_id=(.*)', info)
                if theme_addon_id: theme_addon_id = theme_addon_id.group(1)
                
                theme_url = re.search('url=(.*)', info)
                if theme_url: theme_url = theme_url.group(1)
                
                if theme_addon_id or theme_url:
                    themes += '|' + theme_name
                    f.write('<setting id="%s_themetype" type="text" label="Theme Type" default="%s" visible="false"/>\n' % (theme_name, 'online' if theme_online=='yes' else 'disk') )
                    if theme_url: f.write('<setting id="%s_themeurl" type="text" label="Theme URL" default="%s" visible="false"/>\n' % (theme_name, theme_url))
                    elif theme_addon_id: f.write('<setting id="%s_themeaddon" type="text" label="Theme Addon" default="%s" visible="false"/>\n' % (theme_name, theme_addon_id) )
            
            f.write('<setting id="theme" type="labelenum" values="%s" label="Theme" default="Default" visible="true"/>\n' % themes)
            
            f.write('<setting type="sep"/>\n')
            f.write('<setting id="mystream_default" type="bool" label="Go directly to [COLOR royalblue]my[/COLOR]Stream" default="false"/>\n')
            f.write('<setting type="sep"/>\n')
            f.write('<setting id="timeformat" type="enum" values="12-Hour|24-Hour" label="Time Format" default="0"/>\n')
            f.write('<setting id="timezonesource" type="enum" values="Auto Detect|Custom" label="Time Zone" default="0"/>\n')
            f.write('<setting id="timezone" enable="eq(-1,1)" type="labelenum" values="-12|-11|-10|-9|-8|-7|-6|-5|-4|-3|-2|-1|0|+1|+2|+3|+4|+5|+6|+7|+8|+9|+10|+11|+12" label="     GMT Offset" default="0"/>\n')
            f.write('<setting type="sep"/>\n')
            f.write('<setting id="search_history" default="true"/>\n')
            f.write('<setting type="sep"/>\n')
            f.write('<setting id="cache_retention" type="labelenum" values="2|5|10|15|20" label="Cache Retention Time (in Hours)" default="2"/>\n')
            f.write('<setting id="cache_playlists" type="bool" label="     Cache Playlists" default="false"/>\n')
            f.write('</category>\n')
            
            f.write('<category label="Auto-View">\n')	
            f.write('<setting id="auto-view" type="bool" label="Enable Automatic View" default="true"/>\n')
            f.write('<setting id="default-view" type="number" label="     Default View" default="50" enable="!eq(-1,false)"/>\n')
            f.write('<setting id="livetv-view" type="number" label="     Live TV View" default="500" enable="!eq(-2,false)"/>\n')   
            f.write('<setting id="movie-view" type="number" label="     Movies View" default="52" enable="!eq(-3,false)"/>\n')   
            f.write('<setting id="tvshow-view" type="number" label="     TV Shows View" default="52" enable="!eq(-4,false)"/>\n')
            f.write('<setting id="season-view" type="number" label="     Seasons View" default="503" enable="!eq(-5,false)"/>\n')
            f.write('<setting id="episode-view" type="number" label="     Episodes View" default="503" enable="!eq(-6,false)"/>\n')
            f.write('</category>\n')
            
            f.write('<category label="Database">\n')
            f.write('<setting id="local_db_location" type="folder" label="Local DB Location" default="special://profile/addon_data/script.icechannel/databases"/>\n')
            f.write('<setting id="use_remote_db" type="bool" 	label="Use a remote MySQL DB" default="false"/>\n')
            f.write('<setting id="db_address" type="text" 	label="     Address" enable="eq(-1,true)" default="" />\n')
            f.write('<setting id="db_port" 	 type="integer" label="     Port" enable="eq(-2,true)" default="" />\n')
            f.write('<setting id="db_user" 	 type="text" 	label="     Username" enable="eq(-3,true)" default="" />\n')
            f.write('<setting id="db_pass"	 type="text" 	label="     Password" enable="eq(-4,true)" default="" option="hidden"/>\n')
            f.write('<setting id="db_name"	 type="text" 	label="     Database" enable="eq(-5,true)" default="iStream" />\n')
            f.write('</category>\n')
            
            f.write('</settings>')
        finally:            
            f.close
    except IOError:
        addon.log_error('error writing ' + settings_file)
