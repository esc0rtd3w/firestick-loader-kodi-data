import xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
import xbmcvfs
from libs import kodi
import time
from sqlite3 import dbapi2 as db_lib
import json
import log_utils
import kodi

COMPONENT = __name__

addon_id=kodi.addon_id
db_dir = xbmc.translatePath("special://profile/addon_data/"+addon_id+'/Database')

db_path = os.path.join(db_dir, 'Velocity_images.db')

if not xbmcvfs.exists(os.path.dirname(db_path)):
    try: xbmcvfs.mkdirs(os.path.dirname(db_path))
    except: os.mkdir(os.path.dirname(db_path))

conn =db_lib.connect(db_path)
#conn.text_factory = str

ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon_id=kodi.addon_id

conn.execute('CREATE TABLE IF NOT EXISTS image_cache (trakt_id INTEGER NOT NULL, season TEXT NOT NULL, episode TEXT NOT NULL,timestamp, banner TEXT, fanart TEXT, thumb TEXT, poster TEXT, clearart TEXT, clearlogo TEST, PRIMARY KEY(trakt_id, season, episode))')
conn.execute('CREATE TABLE IF NOT EXISTS url_cache (url VARCHAR(255) NOT NULL, data VARCHAR(255), response, res_header, timestamp,PRIMARY KEY(url, data))')


#########################
def cache_images(trakt_id, art_dict, season='', episode=''):
    now = time.time()
    for key in art_dict:
        if not art_dict[key]:
            art_dict[key] = None

    sql = 'REPLACE INTO image_cache (trakt_id, season, episode, timestamp, banner, fanart, thumb, poster, clearart, clearlogo) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    conn.execute(sql, (trakt_id, season, episode, now, art_dict.get('banner'), art_dict.get('fanart'), art_dict.get('thumb'),art_dict.get('poster'), art_dict.get('clearart'), art_dict.get('clearlogo')))
    conn.commit()

def get_cached_images(trakt_id, season='', episode='', cache_limit=30 * 24):
    art_dict = {}
    sql = 'SELECT timestamp, banner, fanart, thumb, poster, clearart, clearlogo FROM image_cache WHERE trakt_id = ? and season=? and episode=?'
    conn.execute(sql, (trakt_id, season, episode))

    #
    for row in conn.execute('SELECT timestamp, banner, fanart, thumb, poster, clearart, clearlogo FROM image_cache WHERE trakt_id = ? and season=? and episode=?', (trakt_id, season, episode)):
        if row:
            created = float(row[0])
            banner =row[1]
            fanart = row[2]
            thumb = row[3]
            poster = row[4]
            clearart = row[5]
            clearlogo = row[6]
            if time.time() - float(created) < cache_limit * 60 * 60:
                art_dict = {'banner': banner, 'fanart': fanart, 'thumb': thumb, 'poster': poster, 'clearart': clearart,'clearlogo': clearlogo}
        return art_dict


def cache_url(url, body, data=None, res_header=None):
    now = time.time()
    if data is None: data = ''
    if res_header is None: res_header = []
    res_header = json.dumps(res_header)
    if isinstance(body, unicode):
        body = body.encode('utf-8')
    body = buffer(body)
    sql = 'REPLACE INTO url_cache (url, data, response, res_header, timestamp) VALUES(?, ?, ?, ?, ?)'
    conn.execute(sql, (url, data, body, res_header, now))
    conn.commit()

def delete_cached_url(url, data=''):
    if data is None: data = ''
    sql = 'DELETE FROM url_cache WHERE url = ? and data= ?'
    conn.execute(sql, (url, data))
    conn.commit()

def get_cached_url(url, data='', cache_limit=8):
    if data is None: data = ''
    html = ''
    res_header = []
    created = 0
    now = time.time()
    age = now - created
    limit = 60 * 60 * cache_limit
    for row in conn.execute('SELECT timestamp, response, res_header FROM url_cache WHERE url = ? and data=?', (url,data)):
        if row:
            created = float(row[0])
            age = now - created
            res_header = json.loads(row[2])
            now = time.time()
            if age < limit:
                html = row[1]
    log_utils.log('Image Cache: Url: %s, Data: %s, Cache Hit: %s, created: %s, age: %.2fs (%.2fh), limit: %ss' % (url, data, bool(html), created, age, age / (60 * 60), limit), log_utils.LOGDEBUG, COMPONENT)
    return created, res_header, str(html)


def flush_image_cache():
    sql = 'DELETE FROM image_cache'
    conn.execute(sql)
    conn.execute('VACUUM')


##########################


