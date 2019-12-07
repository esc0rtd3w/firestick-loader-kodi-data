import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.audio.jango')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.jango'), '')

def cookie_jar():
    return create_file(DATA_PATH, "cookiejar.lwp")
	
def addon():
    return ADDON
	
def jango_account():
    if ADDON.getSetting('jango_account') == "true":
        return True
    else:
        return False
		
def username():
    return ADDON.getSetting('username') 

def password():
    return ADDON.getSetting('password') 

def current_playlist():
    return create_file(DATA_PATH, "current_playlist.list")		

def favourites_file_artist():
    return create_file(DATA_PATH, "favourites_artist.list")
	
def favourites_file_album():
    return create_file(DATA_PATH, "favourites_album.list")
	
def download_list():
    return create_file(DATA_PATH, "downloads.list")
	
def favourites_file_songs():
    return create_file(DATA_PATH, "favourites_songs.list")
	
def playlist_file():
    return create_file(DATA_PATH, "playlist_file.list")
	
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
create_directory(DATA_PATH, "")
   
