import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.audio.bbcpodcasts.rayw1986')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.bbcpodcasts.rayw1986'), '')
def addon():
    return ADDON

def data_path():
    create_directory(DATA_PATH, "")

def favourite_podcasts():
    return create_file(DATA_PATH, "my_podcasts.list")
	
def watched_videos_file():
    return create_file(DATA_PATH, "watched_videos.list")
	

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
        f = open(file_path, 'w+')
        f.write('')
        f.close()
    return file_path

def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None   
