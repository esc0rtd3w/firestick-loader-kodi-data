import os
import glob
import time
import xml.etree.ElementTree as ET
try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from xbmcswift2 import xbmc, xbmcvfs
from meta.utils.rpc import RPC
from meta.gui import dialogs
from meta import plugin
from settings import SETTING_MOVIES_LIBRARY_FOLDER, SETTING_TV_LIBRARY_FOLDER, SETTING_MUSIC_LIBRARY_FOLDER, SETTING_LIVE_LIBRARY_FOLDER

def scan_library(type="video", path=None):
    while not xbmc.abortRequested and \
     (xbmc.getCondVisibility('Library.IsScanning') or \
     xbmc.getCondVisibility('Window.IsActive(progressdialog)')):
        xbmc.sleep(1000)
    if not type or type == "":
        xbmc.executebuiltin('UpdateLibrary(video)')
        xbmc.executebuiltin('UpdateLibrary(music)')
    elif type == "video":
        xbmc.executebuiltin('UpdateLibrary(video)')
    elif type == "audio":
        xbmc.executebuiltin('UpdateLibrary(music)')
#    list_library()

def library_inventory(type="movies"):
    if type == "movies":
        LIBITEMS = RPC.VideoLibrary.GetMovies(properties=["imdbnumber", "title", "file", "year"])[type]
        lib = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
    elif type == "tvshows":
        LIBITEMS = RPC.VideoLibrary.GetTVShows(properties=["imdbnumber", "title", "file", "year"])[type]
        lib = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
    QITEMS = []
    LITEMS = []
    plugin.log.info("{0}".format(lib))
    for i in LIBITEMS:
        if lib in i['file']:
            player_file = xbmc.translatePath(os.path.join(lib, i['imdbnumber'], "player.info"))
            if os.path.exists(player_file):
                with open(player_file) as pf:
                    content = pf.read()
            else:
                with open(player_file, "w") as pf:
                    pf.write('library')
                    content = 'library'
            QITEMS.append(str([i['title'], i['year'], content, i['imdbnumber']]))
        else:
            LITEMS.append(str([i['title'], i['year'], i['file'], i['imdbnumber']]))
    lib_file = xbmc.translatePath(os.path.join(lib, "mqlib.info"))
    with open(lib_file, "w") as lf:
        lf.write('\n'.join(sorted(QITEMS, key=lambda s: s.strip('[u"').strip("[u'").lower())))
    if len(LIBITEMS) > len(QITEMS):
        lib_file = xbmc.translatePath(os.path.join(lib, "nqlib.info"))
        with open(lib_file, "w") as lf:
            lf.write('\n'.join(sorted(LITEMS, key=lambda s: s.strip('[u"').strip("[u'").lower())))

def channel_inventory():
    lib = plugin.get_setting(SETTING_LIVE_LIBRARY_FOLDER, unicode)
    LIBITEMS = os.listdir(xbmc.translatePath(lib))
    plugin.log.info("{0}".format(LIBITEMS))
    QITEMS = []
    for item in LIBITEMS:
        player_file = xbmc.translatePath(os.path.join(lib, item, "player.info"))
        if os.path.exists(player_file):
            with open(player_file) as pf:
                content = pf.read()
        elif item != 'mqlib.info':
            with open(player_file, "w") as pf:
                pf.write('library')
                content = 'library'
        QITEMS.append(str([item, content]))
    lib_file = xbmc.translatePath(os.path.join(lib, "mqlib.info"))
    with open(lib_file, "w") as lf:
        lf.write('\n'.join(sorted(QITEMS, key=lambda s: s.strip('[u"').strip("[u'").lower())))

def list_library():
    while not xbmc.abortRequested and \
     (xbmc.getCondVisibility('Library.IsScanning') or \
     xbmc.getCondVisibility('Window.IsActive(progressdialog)') or \
     xbmc.getCondVisibility('Window.IsActive(extendedprogressdialog)')):
        xbmc.sleep(100)
    xbmc.sleep(5000)
    library = {}
    medias = ["movies", "tvshows"]
#    medias = ["movies", "tvshows", "musicvideos", "music", "live"]
    for m in medias:
        if m == "movies":
            lib = plugin.get_setting(SETTING_MOVIES_LIBRARY_FOLDER, unicode)
            prite = RPC.videolibrary.get_movies(properties=["title","year","playcount","fanart","originaltitle","imdbnumber","thumbnail","file"])
            if "movies" in prite: ite = prite["movies"]
            else: ite = []
        elif m == "tvshows":
            lib = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
            prite = RPC.videolibrary.get_tvshows(properties=["title","year","playcount","fanart","originaltitle","imdbnumber","thumbnail","file"])
            if "tvshows" in prite: ite = prite["tvshows"]
            else: ite = []
#        elif m == "musicvideos":
#            lib = plugin.get_setting(SETTING_TV_LIBRARY_FOLDER, unicode)
#            ite = RPC.videolibrary.get_tvshows(properties=["title","year","playcount","fanart","originaltitle","imdbnumber","thumbnail","file"])["tvshows"]
        else: continue
        liq = xbmcvfs.listdir(lib)[0]
        for i in ite:
            try:
                f = xbmcvfs.File(os.path.join(lib, i["imdbnumber"], "player.info"))
                i["player"] = f.read()
                f.close()
            except: i["player"] = "na"
        f = xbmcvfs.File("{0}library.nfo".format(lib), 'w')
        f.write(str(ite))
        f.close()
        if len(ite) > 0: players = dict(zip(ite[0],zip(*[d.values() for d in ite])))["player"]
        else: players = "()"
        f = xbmcvfs.File("{0}players.nfo".format(lib), 'w')
        f.write(str(players))
        f.close()
#        dite = [dict(zip(lite,t)) for t in zip(*lite.values())]


def get_movie_from_library(imdbnumber):
    imdbnumber = str(imdbnumber)
    db_movies = RPC.video_library.get_movies(properties=['title', 'file', 'imdbnumber'])
    for movie in db_movies.get('movies', []):
        if movie['imdbnumber'] != imdbnumber:
            continue
        if movie['file'].endswith(".strm"):
            continue
        return {'label': movie['title'], 'path': movie['file']}
    return None

def get_episode_from_library(imdbnumber, season, episode):
    imdbnumber = str(imdbnumber)
    season = int(season)
    episode = int(episode)
    db_shows = RPC.video_library.get_tvshows(properties=['imdbnumber', 'file'])
    for show in db_shows.get('tvshows', []):
        if show['imdbnumber'] != imdbnumber:
            continue
        db_episodes = RPC.video_library.get_episodes(tvshowid=show["tvshowid"],\
            season=season, properties=['episode', 'file', 'title'])
        for ep in db_episodes.get('episodes', []):
            if ep['episode'] != episode:
                continue
            if ep['file'].endswith(".strm"):
                continue
            return {'label': ep['title'], 'path': ep['file']}
    return None

def add_source(source_name, source_path, source_content, source_thumbnail):    
    xml_file = xbmc.translatePath('special://profile/sources.xml')
    if not os.path.exists(xml_file):
        with open(xml_file, "w") as f:
            f.write("""<sources>
    <programs>
        <default pathversion="1" />
    </programs>
    <video>
        <default pathversion="1" />
    </video>
    <music>
        <default pathversion="1" />
    </music>
    <pictures>
        <default pathversion="1" />
    </pictures>
    <files>
        <default pathversion="1" />
    </files>
</sources>""")
    existing_source = _get_source_attr(xml_file, source_name, "path")
    if existing_source and existing_source != source_path:
        _remove_source_content(existing_source)
    if _add_source_xml(xml_file, source_name, source_path, source_thumbnail):
        _set_source_content(source_content)
#########   XML functions   #########

def _add_source_xml(xml_file, name, path, thumbnail):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sources = root.find('video')
    existing_source = None
    for source in sources.findall('source'):
        xml_name = source.find("name").text
        xml_path = source.find("path").text
        if source.find("thumbnail"): xml_thumbnail = source.find("thumbnail").text
        else: xml_thumbnail = ""
        if xml_name == name or xml_path == path:
            existing_source = source
            break
    if existing_source is not None:
        xml_name = source.find("name").text
        xml_path = source.find("path").text
        if source.find("thumbnail"): xml_thumbnail = source.find("thumbnail").text
        else: xml_thumbnail = ""
        if xml_name == name and xml_path == path and xml_thumbnail == thumbnail:
            return False
        elif xml_name == name:
            source.find("path").text = path
            source.find("thumbnail").text = thumbnail
        elif xml_path == path:
            source.find("name").text = name
            source.find("thumbnail").text = thumbnail
        else:
            source.find("path").text = path
            source.find("name").text = name
    else:
        new_source = ET.SubElement(sources, 'source')
        new_name = ET.SubElement(new_source, 'name')
        new_name.text = name
        new_path = ET.SubElement(new_source, 'path')
        new_thumbnail = ET.SubElement(new_source, 'thumbnail')
        new_allowsharing = ET.SubElement(new_source, 'allowsharing')
        new_path.attrib['pathversion'] = "1"
        new_thumbnail.attrib['pathversion'] = "1"
        new_path.text = path
        new_thumbnail.text = thumbnail
        new_allowsharing.text = "true"
    _indent_xml(root)
    tree.write(xml_file)
    return True

def _indent_xml(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent_xml(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def _get_source_attr(xml_file, name, attr):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    sources = root.find('video')
    for source in sources.findall('source'):
        xml_name = source.find("name").text
        if xml_name == name:
            return source.find(attr).text
    return None

#########   Database functions  #########

def _db_execute(db_name, command):
    databaseFile = _get_database(db_name)
    if not databaseFile:
        return False
    dbcon = database.connect(databaseFile)
    dbcur = dbcon.cursor()
    dbcur.execute(command)
    #try:
    #    dbcur.execute(command)
    #except database.Error as e:
    #    print "MySQL Error :", e.args[0], q.decode("utf-8")
    #    return False
    dbcon.commit()
    return True

def _get_database(db_name):
    path_db = "special://profile/Database/" + db_name
    filelist = glob.glob(xbmc.translatePath(path_db))
    if filelist:
        return filelist[-1]
    return None

def _remove_source_content(path):
    q = "DELETE FROM path WHERE strPath LIKE '%{0}%'".format(path)
    return _db_execute("MyVideos*.db", q)

def _set_source_content(content):    
    q = "INSERT OR REPLACE INTO path (strPath,strContent,strScraper,strHash,scanRecursive,useFolderNames,strSettings,noUpdate,exclude,dateAdded,idParentPath) VALUES "
    q += content
    return _db_execute("MyVideos*.db", q)
