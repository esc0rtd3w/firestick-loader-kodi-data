import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
import xbmcvfs
from libs import kodi
import threading
import urlresolver
from libs import log_utils,trakt
import time
import threading
from libs import kodi


from sqlite3 import dbapi2 as db_lib
from sqlite3 import OperationalError as OperationalError
from sqlite3 import DatabaseError as DatabaseError
trakt_api=trakt.TraktAPI()

addon_id=kodi.addon_id
db_dir = xbmc.translatePath("special://profile/addon_data/"+addon_id+'/Database')

db_path = os.path.join(db_dir, 'Velocity_watch.db')

if not xbmcvfs.exists(os.path.dirname(db_path)):
    try: xbmcvfs.mkdirs(os.path.dirname(db_path))
    except: os.mkdir(os.path.dirname(db_path))

conn =db_lib.connect(db_path)
conn.text_factory = str
conn.execute ('CREATE TABLE IF NOT EXISTS watch_cache (trakt_id text  NOT NULL, media text,name text, PRIMARY KEY(trakt_id, media))')

def get_watched_items():
    links = trakt_api.get_watched_history('shows')
    for e in links:# E also = Show imdb id
        watched = trakt_api.get_watched_shows(e)
        for e in watched:
            id = e['episode']['ids']['trakt']
            set_watch_cache(id,'shows')

    links = trakt_api.get_watched_history('movies')
    traktid = links['trakt']
    for trakt_id in traktid:
        set_watch_cache(trakt_id,'movies')


def set_watch_cache(trakt_id,media,name=None):
        if name == None:
            name = ''
        # print trakt_id
        # print "STARTING WATCH_CACHE INSERTION"
        sql = 'REPLACE INTO watch_cache (trakt_id,media,name) VALUES(?, ?, ?)'
        conn.execute(sql, (trakt_id,media,name))
        conn.commit()


def del_watch_cache(trakt_id,media,name=None):
        if name == None:
            name = ''
        # print trakt_id
        # print "STARTING WATCH_CACHE INSERTION"
        conn.execute("DELETE FROM watch_cache where trakt_id='"+trakt_id+"'")
        conn.commit()


def get_watched_cache(trakt_id):
        for row in conn.execute("SELECT trakt_id FROM watch_cache WHERE trakt_id =? ", (trakt_id,)):
                #print row
            if row:
                return row
            else:
                return 'None Found'
        conn.commit()
       # print 'DB Cache: Url: %s, Data: %s, Cache Hit: %s, created: %s, age: %s, limit: %s' % (url, data, bool(html), created, now - created, limit)
        #return watched_item


def get_watched_cacheOLD(trakt_id):
        #trakt_id = '90'
        if conn.execute("SELECT media FROM watch_cache WHERE trakt_id =? ", (trakt_id,)):
            return True
        else:
            return False
        conn.commit()


def flush_watched_cache():
        sql = 'DELETE FROM watch_cache'
        conn.execute(sql)
        conn.execute('VACUUM')

def format_watch_sql( sql):
    if sql[:7] == 'REPLACE':
        sql = 'INSERT OR ' + sql
    return sql


def repair_watched_items():
    flush_watched_cache()
    get_watched_items()






