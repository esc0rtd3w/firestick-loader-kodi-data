# Settings Module by: Blazetamer

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os,re
from libs import kodi
import re,unicodedata


addon_id=kodi.addon_id
ADDON = xbmcaddon.Addon(id=kodi.addon_id)
DATA_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/'+addon_id), '')
AOPATH = xbmc.translatePath(os.path.join('special://home/addons/'+addon_id, ''))
LOGPATH  = (xbmc.translatePath("special://logpath"))


def addon():
    return ADDON
	
def username():
    return ADDON.getSetting('user') 

def password():
    return ADDON.getSetting('password') 
	
def email():
    return ADDON.getSetting('email')
	
def enable_subscriptions():
    if ADDON.getSetting('enable_subscriptions') == "true":
        return True
    else:
        return False
	
def download_dir():
    return ADDON.getSetting('download_dir')

def log_path():
    return LOGPATH
	
def favourites_file():
    return create_file(DATA_PATH, "favourites.list")
	
def subscription_file():
    return create_file(DATA_PATH, "subscriptions.list")
		
def cookie_jar():
    return create_file(AOPATH, "cookies.lwp")
	
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

def append_file(dir_path, file_name, file_content):
    
    #if file_content not in myfile:
      myfile= dir_path+"/"+file_name
      source= open( myfile, mode = 'r' )
      link = source . read( )
      source . close ( )
      if file_content not in link:
        f = open(myfile,'a')
        f.write(file_content+'\n') # python will convert \n to os.linesep
        f.close() # you can omit in most cases as the destructor will call it
        return 

def get_hostname(url):
    if '//' not in url and '/' not in url:
        url = '//'+url+'/blank'
    r = re.search('//(.+?)/([0-9a-zA-Z/]+)', url)
    if r:
        hostname =  r.groups()[0]
    else:
        hostname = "NAME UNKNOWN"
    host = hostname
    if host.endswith('.com'):
        host = host[:-4]
    if host.endswith('.org'):
        host = host[:-4]
    if host.endswith('.eu'):
        host = host[:-3]
    if host.endswith('.ch'):
        host = host[:-3]
    if host.endswith('.in'):
        host = host[:-3]
    if host.endswith('.es'):
        host = host[:-3]
    if host.endswith('.tv'):
        host = host[:-3]
    if host.endswith('.net'):
        host = host[:-4]
    if host.endswith('.me'):
        host = host[:-3]
    if host.endswith('.ws'):
        host = host[:-3]
    if host.endswith('.sx'):
        host = host[:-3]
    if host.endswith('.co'):
        host = host[:-3]
    if host.endswith('.us'):
        host = host[:-3]
    if host.endswith('.io'):
        host = host[:-3]
    if host.endswith('.tt'):
        host = host[:-3]
    if host.endswith('.cc'):
        host = host[:-3]
    if host.endswith('.to'):
        host = host[:-3]
    if host.startswith('www.'):
        host = host[4:]
    return host


def name_cleaner(name):
          name = name.replace('&#8211;','')
          name = name.replace("&#8217;","")
          name = name.replace("&#039;s","'s")
          #name = unicode(name, errors='ignore')
          return(name)

def make_trailer(trailer_url):
    match = re.search('\?v=(.*)', trailer_url)
    if match:
        #return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1)) ##OLD WAY
        return 'plugin://plugin.video.youtube/play/?video_id=%s' % (match.group(1))


def get(title):
    if title == None: return
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass

        t = ''
        for i in title:
            c = unicodedata.normalize('NFKD',unicode(i,"ISO-8859-1"))
            c = c.encode("ascii","ignore").strip()
            if i == ' ': c = i
            t += c

        return t.encode("utf-8")
    except:
        return title





'''
def get_host(self):
        r = re.search('//(.+?)/([0-9a-zA-Z/]+)', self._url)
        if r:
            self._host =  r.groups()[0]
        else:
            self._host = "NO NAME"
        return self._host

'''

DATABASE_DIR=create_directory(DATA_PATH, "Database")
# SOURCE_DIR = create_directory(DATA_PATH, "Data_Logging/Sources")
# MISC_DIR = create_directory(DATA_PATH, "Misc")
COOKIE_PATH = create_directory(AOPATH, "All_Cookies")

#append_file(settings.DATA_PATH +"Misc","testfile.txt",file_content)
		
