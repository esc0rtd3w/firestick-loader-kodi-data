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

db_path = os.path.join(db_dir, 'Velocity.db')

if not xbmcvfs.exists(os.path.dirname(db_path)):
    try: xbmcvfs.mkdirs(os.path.dirname(db_path))
    except: os.mkdir(os.path.dirname(db_path))

conn =db_lib.connect(db_path)
conn.text_factory = str

ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)


conn.execute ('CREATE TABLE IF NOT EXISTS url_cache (url VARCHAR(255) NOT NULL, data VARCHAR(255), response, timestamp, PRIMARY KEY(url, data))')
#conn.execute("INSERT INTO downloads VALUES ('"+name+"','"+url+"','"+thumb+"','"+ext+"','"+media+"')")
#cache_limit = int(kodi.get_setting('cache_limit'))


def set_cache_url(url, body, data=None):
        # print url
        # print body
        if data is None: data = ''
        print "STARTING URL_CACHE INSERTION"
        # print "BODY IS : "+ body
        # print "URL IS : "+url
        # truncate data if running mysql and greater than col size
        now = str(time.time())
        sql = 'REPLACE INTO url_cache (url,data,response,timestamp) VALUES(?, ?, ?, ?)'
        conn.execute(sql, (url, data, body, now,))
        conn.commit()


def get_cached_url(url, data=None):
        if data is None: data = ''
        html = ''
        created = 0
        now = time.time()
        limit = 60 * 60 * int(kodi.get_setting('cache_limit'))
        for row in conn.execute("SELECT timestamp, response FROM url_cache WHERE url =? ", (url,)):
                #print row
            if row:
                created = float(row[0])
                age = now - created
                now = time.time()
                # print "CACHE NOW TIME IS :"+str(now)
                # print "CACHE LIMIT IS : "+str(limit)
                # print "CACHE AGE IS :"+str(age)
                if age < limit:
                    html = row[1]
        conn.commit()
       # print 'DB Cache: Url: %s, Data: %s, Cache Hit: %s, created: %s, age: %s, limit: %s' % (url, data, bool(html), created, now - created, limit)
        return created, html

def flush_url_cache():
        sql = 'DELETE FROM url_cache'
        conn.execute(sql)
        conn.execute('VACUUM')

def format_sql( sql):
    if sql[:7] == 'REPLACE':
        sql = 'INSERT OR ' + sql
    return sql
