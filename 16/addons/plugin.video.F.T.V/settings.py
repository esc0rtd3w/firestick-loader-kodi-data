import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
#testing HLS setting
ADDON = xbmcaddon.Addon(id='plugin.video.F.T.V')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.F.T.V'), '')
FTV_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.F.T.V', ''))

def addon():
    return ADDON

def session_id():
    return ADDON.getSetting('session_id')
	
def keep_session_flag():
    return ADDON.getSetting('keep_session_flag')

def filmon_account():
    if ADDON.getSetting('filmon_account') == 'true':
        return True
    else:
        return False
		
def stream_type():
    quality = ADDON.getSetting('stream_type')
    if quality == '0':
        return 'HLS'
    else:
        return 'RTMP'
		
def hidden_file():
    return create_file(DATA_PATH, "hidden_links.list")
	
def favourite_channels():
    return create_file(DATA_PATH, "favourite_channels.list")
	
def favourite_movies():
    return create_file(DATA_PATH, "favourite_movies.list")
	
def filmon_user():
    return ADDON.getSetting('filmon_user') 

def filmon_pass():
    return ADDON.getSetting('filmon_pass') 

def filmon_quality():
    quality = ADDON.getSetting('filmon_quality')
    if quality == '0':
        return "480p"
    else:
        return "360p"
		
def auto_switch():
    if ADDON.getSetting('auto_switch') == 'true':
        return True
    else:
        return False
		
def show_ch_id():
    if ADDON.getSetting('show_ch_id') == 'true':
        return True
    else:
        return False
		
def root_channel():
    return ADDON.getSetting('root_channel') 

def download_path():
    return ADDON.getSetting('download_path')
	
def movie_directory():
    if ADDON.getSetting('movie_directory')=='set':
        return create_directory(DATA_PATH, "movies")
    else:
        return ADDON.getSetting('movie_directory')

def my_videos():
    if ADDON.getSetting('my_videos') == 'true':
        return True
    else:
        return False

def my_audio():
    if ADDON.getSetting('my_audio') == 'true':
        return True
    else:
        return False

def other_menu():
    if ADDON.getSetting('other_menu') == 'true':
        return True
    else:
        return False
		
def sort_alpha():
    if ADDON.getSetting('sort_alpha') == 'true':
        return True
    else:
        return False
	
def cookie_jar():
    return create_file(FTV_PATH, "cookiejar.lwp")
	
def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path
	
create_directory(DATA_PATH, "")

		
