
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
import xbmcvfs
from libs import kodi
import threading
import urlresolver
from libs import log_utils
import time
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon

from sqlite3 import dbapi2 as db_lib
from sqlite3 import OperationalError as OperationalError
from sqlite3 import DatabaseError as DatabaseError


addon_id=kodi.addon_id
db_dir = xbmc.translatePath("special://profile/addon_data/"+addon_id+'/Database')

db_path = os.path.join(db_dir, 'Velocity_dl.db')

if not xbmcvfs.exists(os.path.dirname(db_path)):
    try: xbmcvfs.mkdirs(os.path.dirname(db_path))
    except: os.mkdir(os.path.dirname(db_path))

conn =db_lib.connect(db_path)

ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)


artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
fanart = artwork+'fanart.jpg'
download_path = kodi.get_setting('download_folder')



#========================Alternate Param Stuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
repourl = addon.queries.get('repourl', '')
gomode = addon.queries.get('gomode', '')
page = addon.queries.get('page', '')
key = addon.queries.get('key', '')
iconimage = addon.queries.get('iconimage', '')
sound = addon.queries.get('sound', '')
media = addon.queries.get('media', '')

#======================== END Alternate Param Stuff=======================

############## Start DownloadThread Class ################
class downloadThread (threading.Thread):
    def __init__(self, name, url, thumb, media, ext):
        threading.Thread.__init__(self)
        self.thumb = thumb
        self.name =name
        self.url = url
        self.ext = ext
        self.media = media

    def run(self):
            self.path = download_path + self.media
            if not os.path.exists(self.path):
                os.makedirs(self.path)

            self.file_name = self.name + self.ext

            addon.show_small_popup(title='[COLOR gold]Downloads Started[/COLOR]', msg=self.name + ' Is Downloading', delay=int(7000), image=self.thumb)
            u = urllib.urlopen(self.url)
            f = open(os.path.join(self.path,self.file_name), 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])

            file_size_dl = 0
            block_sz = 8192



            while True:
               buffer = u.read(block_sz)
               if not buffer:
                   break

               file_size_dl += len(buffer)
               f.write(buffer)
               status = int( file_size_dl * 1000. / file_size)
               # if status > 99 and status < 101:
               #       #addon.show_small_popup(title=self.name, msg='10% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='10% Complete',icon=self.thumb, duration=3000, sound=None)
               #
               # elif status > 199 and status < 201:
               #       #addon.show_small_popup(title=self.name, msg='20% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='20% Complete',icon=self.thumb, duration=3000, sound=None)
               #
               # elif status > 299 and status < 301:
               #       #addon.show_small_popup(title=self.name, msg='30% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='30% Complete',icon=self.thumb, duration=3000, sound=None)
               #
               # elif status > 399 and status < 401:
               #       #addon.show_small_popup(title=self.name, msg='40% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='40% Complete',icon=self.thumb, duration=3000, sound=None)

               if status > 499 and status < 501:
                     #addon.show_small_popup(title=self.name, msg='50% Complete',delay=int(10), image=self.thumb)
                     kodi.dl_notify(header=self.name, msg='50% Complete',icon=self.thumb, duration=3000, sound=None)

               # elif status > 599 and status < 601:
               #       #addon.show_small_popup(title=self.name, msg='60% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='60% Complete',icon=self.thumb, duration=3000, sound=None)
               #
               # elif status > 699 and status < 701:
               #       #addon.show_small_popup(title=self.name, msg='70% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='70% Complete',icon=self.thumb, duration=3000, sound=None)
               #
               # elif status > 799 and status < 801:
               #       #addon.show_small_popup(title=self.name, msg='80% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='80% Complete',icon=self.thumb, duration=3000, sound=None)
               #
               # elif status > 899 and status < 901:
               #       #addon.show_small_popup(title=self.name, msg='90% Complete',delay=int(10), image=self.thumb)
               #       kodi.dl_notify(header=self.name, msg='90% Complete',icon=self.thumb, duration=3000, sound=None)

               elif status > 997 and status < 999:
                     #addon.show_small_popup(title=self.name, msg='95% Complete',delay=int(10), image=self.thumb)
                     kodi.dl_notify(header='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed',icon=self.thumb, duration=3000, sound=True)


            f.close()

            removeFromDLQueue(self.name)


            try:
                #addon.show_small_popup(title='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed', delay=int(5000), image=self.thumb)
                kodi.dl_notify(header='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed',icon=self.thumb, duration=3000, sound=True)
            except:
                #addon.show_small_popup(title='Error', msg=self.name + ' Failed To Download File', delay=int(5000), image=self.thumb)
                kodi.dl_notify(header='ERROR', msg=self.name + ' Failed To Download File',icon=self.thumb, duration=3000, sound=True)
                print 'ERROR - File Failed To Download'


            #addon.show_small_popup(title='[COLOR gold]Process Complete[/COLOR]', msg=self.name + ' is in your downloads folder', delay=int(5000), image=self.thumb)




def addQDir(name,url,mode,thumb,ext,media):
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'media':media, 'ext':ext}
     contextMenuItems = []
     #print download_path+media+'/'+name+ext
     if os.path.exists(download_path+media+'/'+name+ext) :
         name = '[COLOR green]'+name+' Downloading[/COLOR]'
         contextMenuItems.append(('[COLOR green]Downloaded Status[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'download_stats', 'name': name,'url': url,'thumb': thumb,'ext': ext,'media': media})))
     else:
         contextMenuItems.append(('[COLOR green]Download This Now[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'download_now', 'name': name,'url': url,'thumb': thumb,'ext': ext,'media': media})))

     contextMenuItems.append(('[COLOR red]Remove From Queue[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removeFromQueue', 'name': name,'url': url,'thumb': thumb,'ext': ext,'media': media})))
     addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)

def add_to_queue(name,url,thumb,ext,media):
    try:
        try:
            conn.execute('''CREATE TABLE downloads(name text unique, url text, thumb text, ext text, media text)''')
        except:
            print "Velocity says: Downloads DB Table Already exists"

        # Insert a row of data or return already there
        try:
            conn.execute("INSERT INTO downloads VALUES ('"+name+"','"+url+"','"+thumb+"','"+ext+"','"+media+"')")
            addon.show_small_popup(title='[COLOR gold]Item Added To Your Queue [/COLOR]', msg=name + ' Was Added To Your Download Queue', delay=int(5000), image=thumb)
        except Exception as e:
            addon.show_small_popup(title='[COLOR red]Item Already In Your Queue[/COLOR]', msg=name + ' Is Already In Your Download Queue', delay=int(5000), image=thumb)
            print 'Error [%s]  %s' % (str(e), '')
        # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
    except Exception as e:
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='Downloads',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


def viewQueue():
    #kodi.addDir("Start All Downloads",'','download',artwork+'start_downloads.png','',1,'','',fanart=fanart)
    try:
        for row in conn.execute('SELECT * FROM downloads '):
            if row:
                print row
                # name = row[0]
                # url = row[1]
                # thumb = row[2]
                # ext = row[3]
                # media = row[4]

                addQDir(row[0],row[1],'download_now',row[2],row[3],row[4])

    except Exception as e:
                print 'Error [%s]  %s' % (str(e), '')
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def removeFromDLQueue(name):
    print "NAME PASSED BACK IS = "+name
    try:
        print name
        name = name.replace('[COLOR green]','').replace(' Downloading[/COLOR]','')
        conn.execute("DELETE FROM downloads where name='"+name+"'")
    except Exception as e:
                print 'Error [%s]  %s' % (str(e), '')
    conn.commit()
    xbmc.executebuiltin("XBMC.Container.Refresh")
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def removeFromQueue(name,url,thumb,ext,media):
    try:
        print name
        name = name.replace('[COLOR green]','').replace(' Downloading[/COLOR]','')
        conn.execute("DELETE FROM downloads where name='"+name+"'")
    except Exception as e:
                print 'Error [%s]  %s' % (str(e), '')
    conn.commit()
    xbmc.executebuiltin("XBMC.Container.Refresh")
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()



# def download():
#     download_path = kodi.get_setting('download_folder')
#     if download_path == '':
#       addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='')
#     else:
#      for row in conn.execute('SELECT * FROM downloads '):
#         if row:
#             print row
#             name = row[0]
#             url = row[1]
#             thumb = row[2]
#             ext = row[3]
#             media = row[4]
#             #viewQueue()
#             dlThread = downloadThread(name, url, thumb, media, ext)
#             dlThread.start()

                   

def download_now(name, url, thumb, ext, media):
    print name
    print url
    print thumb
    print ext
    print media
    download_path = kodi.get_setting('download_folder')
    if download_path == '':
      addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='')
    else:
        dlThread = downloadThread(name, url, thumb, media, ext)
        dlThread.start()
        #xbmc.executebuiltin("XBMC.Container.Refresh")



def setup_download(name,url,thumb,medias,movie_title):

    hmf = urlresolver.HostedMediaFile(url)
    host = ''
    if hmf:
        urls = urlresolver.resolve(url)

    else: urls = url

    if '.mp4' in urls:
            ext = '.mp4'
    elif '.flv' in urls:
            ext = '.flv'
    elif '.avi' in urls:
            ext = '.avi'

    elif '.mkv' in urls:
            ext = '.mkv'

    elif '.m3u8' in urls:
            ext = '.m3u8'

    else:
      ext = '.flv'

    if medias =='movies':
        media = 'Movies'
    elif medias == 'shows':
        media = 'TV Shows/'+movie_title+'/'

    xbmc.sleep(1000)
    add_to_queue(name,urls,thumb,ext,media)

#=============END DLFUNCTION======================================================================================================================

# TODO Add Stats boxes
def download_stats(name, url, thumb, ext, media):
    name = name.replace('[COLOR green]','').replace(' Downloading[/COLOR]','')
    #print"DOWNLOAD STATS NOT COMPLETE"
    current_size = os.path.getsize(download_path+media+'/'+name+ext)

    total_current_size = current_size /1000000
    if total_current_size < 1000:
        total_current_size = str(total_current_size) +"MB"
    else  :
     total_current_size = current_size /float(1000)
     total_current_size = str(total_current_size) +"GB"

    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
    u = opener.open(url)
    meta = u.info()
    if meta.getheaders("Content-Length"):
        full_size = int(meta.getheaders("Content-Length")[0])
        total_full_size = full_size /1000000
        if total_full_size < 1000:

            total_full_size = str(total_full_size) +"MB"
        else  :
            total_full_size = total_full_size /float(1000)
            total_full_size = str(total_full_size) +"GB"
    else:
        total_full_size = 'Unknown'
        print 'Unable to retrieve Total File size'

    kodi.okDialog(name, 'Downloaded: '+total_current_size, 'Total File Size: '+total_full_size, heading=name)
