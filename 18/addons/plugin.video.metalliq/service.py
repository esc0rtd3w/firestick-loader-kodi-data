#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))

import datetime
import glob
import re
import sqlite3
import xbmcgui
import xbmc

from xbmcswift2 import xbmc, xbmcvfs
from meta import plugin
from meta.play.players import patch
from meta.video_player import VideoPlayer
from meta.utils.properties import get_property, clear_property
from lastfm import lastfm
from default import update_library
from settings import SETTING_UPDATE_LIBRARY_INTERVAL, SETTING_MUSIC_LIBRARY_FOLDER, SETTING_TOTAL_SETUP_DONE, SETTING_AUTOPATCH
from language import get_string as _

player = VideoPlayer()

class Monitor(xbmc.Monitor):
    def onDatabaseUpdated(self, database):
        if database == "video":
            if get_property("clean_library"):
                xbmc.executebuiltin("CleanLibrary(video)")
                clear_property("clean_library")
        if database == "music":
            # need to manualy change the database file to add strm files to it
            music_directory = plugin.get_setting(SETTING_MUSIC_LIBRARY_FOLDER, unicode)
            self.add_folder_to_music_database(music_directory)

    def get_pathId(self,dirName, alternative = False):
        if not alternative:
          absDirName = os.path.abspath(dirName) + os.sep
          absDirName = absDirName.replace('kodi', 'Kodi')
        else:
          absDirName = dirName
        c.execute("SELECT * FROM path WHERE UPPER(strPath) = UPPER(?)", (absDirName,))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            return None

    def get_albumId(self,album, artist):
        c.execute("SELECT * FROM album WHERE strAlbum = ? AND strArtists = ?", (album, artist))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            album_info = lastfm.get_album_info(artist, album)
            if "wiki" in album_info:
                review = album_info["wiki"]["content"]
            else:
                review = ""
            c.execute("INSERT INTO album (strAlbum,strArtists,strReleaseType, strReview) VALUES (?,?,?,?)",
                      (album, artist, "album", review))

            id = c.lastrowid
            conn.commit()
            return id

    def get_artistId(self, artist):
        c.execute("SELECT * FROM artist WHERE strArtist = ?", (artist,))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            artist_info = lastfm.get_artist_info(artist)
            if "bio" in artist_info:
                biography = artist_info["bio"]["content"]
            else:
                biography = ""
            image = "<thumb preview={0}</thumb>".format(artist_info["image"][-1]["#text"])
            c.execute("INSERT INTO artist (strArtist,strBiography, strImage) VALUES (?,?,?)",
                      (artist, biography, image))
            id = c.lastrowid
            conn.commit()
            return id

    def get_songId(self, albumId, pathId, artist, song, song_number, filename):
        c.execute("SELECT * FROM song WHERE idAlbum = ? AND idPath = ? And strArtists = ? AND strTitle = ?",
                  (albumId, pathId, artist, song))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            c.execute("INSERT INTO song (idAlbum, idPath, strArtists, strTitle, itrack, strFilename) VALUES (?,?,?,?,?,?)",
                      (albumId, pathId, artist, song, song_number, filename))
            id = c.lastrowid
            conn.commit()
            return id

    def add_albumArtist(self, albumId, artistId, artist):
        c.execute("SELECT * FROM album_artist WHERE idArtist = ? AND idAlbum = ?", (artistId, albumId))
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO album_artist (idArtist, idAlbum, strArtist) VALUES (?,?,?)",
                      (artistId, albumId, artist))

    def add_songArtist(self, songId, artistId, artist):
        c.execute("SELECT * FROM song_artist WHERE idArtist = ? AND idSong = ?", (artistId, songId))
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO song_artist (idArtist, idSong, strArtist) VALUES (?,?,?)",
                      (artistId, songId, artist))


    def add_albumArt(self, albumId, dirName):
        c.execute("SELECT * FROM art WHERE media_id = ? AND media_type = ?", (albumId, "album"))
        row = c.fetchone()
        if not row:
            absDirName = os.path.abspath(dirName) + os.sep
            absDirName = absDirName.replace('kodi', 'Kodi')
            thumb = absDirName + "folder.jpg"
            c.execute("INSERT INTO art (media_id, media_type,type, url) VALUES (?,?,?,?)",
                      (albumId, "album", "thumb", thumb))

    def add_artistArt(self, artistId, dirName):
        c.execute("SELECT * FROM art WHERE media_id = ? AND media_type = ?", (artistId, "artist"))
        row = c.fetchone()
        if not row:
            absDirName = os.path.abspath(dirName) + os.sep
            absDirName = absDirName.replace('kodi', 'Kodi')
            thumb = absDirName + ".." + os.sep + "folder.jpg"
            c.execute("INSERT INTO art (media_id, media_type,type, url) VALUES (?,?,?,?)",
                      (artistId, "artist", "thumb", thumb))

    def add_folder_to_music_database(self, music_folder):
        import re
        info_regex = re.compile(r'.*?<title>(.*?)</title>.*?<artist>(.*?)</artist>.*?<album>(.*?)</album>.*?<track>(.*?)</track>.*',
                                re.IGNORECASE | re.UNICODE |  re.DOTALL) # regex to parse nfo file
        self.setup_database_connection()
        abs_music_folder = xbmc.translatePath(music_folder)  # translate from special:// to absolute
        for dirName, subdirList, fileList in os.walk(abs_music_folder):
            pathId = self.get_pathId(dirName)
            if not pathId:
                if music_folder[-1] != "/":
                  music_folder = music_folder + "/"
                special_dirname = dirName.replace(abs_music_folder, music_folder)
                if special_dirname[-1] != "/":
                  special_dirname = special_dirname + "/"
                pathId = self.get_pathId(special_dirname, True) # check on android
                if not pathId:
                  special_dirname = dirName.replace(abs_music_folder, music_folder).replace("profile", "userdata")
                  if special_dirname[-1] != "/":
                    special_dirname = special_dirname + "/"
                  pathId = self.get_pathId(special_dirname, True) # check on android
                if not pathId:
                    xbmc.log("pathid not found")
                    continue
            fname_index = 0
            for fname in fileList:
                if fname.endswith("strm"):
                    try:
                        nfo = fname.replace('.strm', '.nfo')
                        info_string = open(dirName+ os.sep + nfo,'r').read()
                        result = re.match(info_regex, info_string)
                        song = result.group(1)
                        artist = result.group(2)
                        album = result.group(3)
                        song_number = result.group(4)

                        artistId = self.get_artistId(artist)
                        self.add_artistArt(artistId, dirName)
                        albumId = self.get_albumId(album, artist)
                        self.add_albumArtist(albumId, artistId, artist)
                        self.add_albumArt(albumId, dirName)
                        songId = self.get_songId(albumId, pathId, artist, song, song_number, fname)
                        self.add_songArtist(songId, artistId, artist)
                    finally:
                        conn.commit()
                fname_index += 1

    def setup_database_connection(self):
        global c
        global conn
        # set up sqlite connection
        path = xbmc.translatePath('special://home/userdata/Database')
        files = glob.glob(os.path.join(path, 'MyMusic*.db'))
        ver = 0
        dbPath = ''
        # Find the highest version number of textures, it's always been textures13.db but you can never be too careful!
        for file in files:
            dbversion = int(re.compile('MyMusic(.+?).db').findall(file)[0])
            if ver < dbversion:
                ver = dbversion
                dbPath = file

        db = xbmc.translatePath(dbPath)
        conn = sqlite3.connect(db, timeout=10, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        conn.text_factory = str
        c = conn.cursor()
        c.row_factory = sqlite3.Row

monitor = Monitor()

def go_idle(duration):
    while not xbmc.abortRequested and duration > 0:
        if player.isPlayingVideo():
            player.currentTime = player.getTime()
        xbmc.sleep(1000)
        duration -= 1

def future(seconds):
    return datetime.datetime.now() + datetime.timedelta(seconds=seconds)

def main():
    go_idle(15)
    if plugin.get_setting(SETTING_TOTAL_SETUP_DONE, bool) == False:
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.metalliq/setup/total)')
        plugin.set_setting(SETTING_TOTAL_SETUP_DONE, "true")
    if plugin.get_setting(SETTING_AUTOPATCH, bool) == True:
        patch("auto")
    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq/movies/batch_add_to_library)")
    next_update = future(0)
    while not xbmc.abortRequested:
        if next_update <= future(0):
            next_update = future(plugin.get_setting(SETTING_UPDATE_LIBRARY_INTERVAL, int) * 60 * 60)
            update_library()
        go_idle(30*60)

if __name__ == '__main__':
    main()