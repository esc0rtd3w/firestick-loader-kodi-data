# Settings Module by: Blazetamer

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.moviedb'), '')
TMPATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.moviedb', ''))

def addon():
    return ADDON
	
def tmuser():
    return ADDON.getSetting('tmuser') 

def tmpass():
    return ADDON.getSetting('tmpass') 
	
def tmemail():
    return ADDON.getSetting('tmemail')
	
def enable_subscriptions():
    if ADDON.getSetting('enable_subscriptions') == "true":
        return True
    else:
        return False
	
def tv_directory():
    return ADDON.getSetting('tv_directory')
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
	
def subscription_file():
    return create_file(DATA_PATH, "subscriptions.list")
		
def cookie_jar():
    return create_file(TMPATH, "cookies.lwp")
	
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
		
