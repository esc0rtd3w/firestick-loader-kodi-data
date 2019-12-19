#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    plugin.audio.squeezebox
    Squeezelite Player for Kodi
    lmsserver.py
    Helper to communicate with LMS server using the json interface
'''

import xbmc
from utils import log_msg, log_exception, json, process_method_on_list
import requests
import thread
import socket
import threading
import re
from simplecache import SimpleCache

TAGS_FULL = "aAcCdegGijJKlostuxyRwk"  # full track/album details
TAGS_BASIC = "acdgjKluNxy"  # basic track details for initial listings
TAGS_ALBUM = "yjtiqwaal"


class LMSServer:
    ''' LMS Class containing our helper methods'''
    _host = None
    _port = None
    _playerid = None
    _state_changing = False
    _status = {}

    def __init__(self, host, port, playerid):
        self._host = host
        self._port = port
        self._playerid = playerid
        self._status = self.status_default()
        self.cache = SimpleCache()

    @property
    def host(self):
        return self._host

    @property
    def playerid(self):
        return self._playerid

    @property
    def state_changing(self):
        '''bool is set whenever a command is issued and we're waiting for the status to be updated'''
        return self._state_changing

    @property
    def mode(self):
        '''get the current mode for the player'''
        return self._status["mode"]

    @property
    def power(self):
        '''get the current mode for the player'''
        return self._status["power"]

    @staticmethod
    def status_default():
        '''default status info to return when player is not (yet) online or server error'''
        return {
            "current_title": "",
            "title": "",
            "playlist repeat": 0,
            "playlist_tracks": 0,
            "playlist shuffle": 0,
            "mode": "offline",
            "playlist_cur_index": 0,
            "power": 0,
            "time": 0,
            "url": "",
            "playlist_timestamp": 0
        }

    def update_status(self):
        '''set the current status of the player'''
        result = self.status_default()
        status = self.send_request("status - 1 tags:u")
        if status and "error" not in status:
            result.update(status)
            try:
                result["url"] = result["playlist_loop"][0]["url"]
                result["title"] = result["playlist_loop"][0]["title"]
            except:
                result["url"] = ""
        self._status = result

    @property
    def cur_title(self):
        '''get the current status of the player'''
        return self._status["current_title"]

    @property
    def cur_index(self):
        '''get the current index of the player'''
        return int(self._status["playlist_cur_index"])

    @property
    def timestamp(self):
        '''get the timestamp (checksum) for the playlist'''
        return self._status["playlist_timestamp"]

    @property
    def track_count(self):
        '''get the current status of the player'''
        return self._status["playlist_tracks"]

    @property
    def status(self):
        '''return the status'''
        return self._status

    def next_track(self):
        '''go to the next track of the playlist'''
        self.send_command("playlist jump +1")

    def pause(self):
        '''pause the player'''
        self.send_command("pause 1")

    def unpause(self):
        '''pause the player'''
        self.send_command("pause 0")

    def stop(self):
        '''stop the player'''
        self.send_command("stop")

    @property
    def time(self):
        '''current point in time of the player'''
        return self._status["time"]

    def send_command(self, cmd):
        '''send command to the player and update the status afterwards'''
        self._state_changing = True
        self.send_request(cmd)
        xbmc.sleep(500)
        self.update_status()
        xbmc.sleep(500)
        self._state_changing = False

    def synced_players(self):
        '''get the synced players'''
        result = []
        _result = self.send_request("sync ?")
        if _result:
            result = _result["_sync"].split(",")
        return result

    def cur_playlist(self, fulldetails=False):
        '''get the current tracks in the playlist'''
        result = []
        status = self.send_request("status 0 10000 tags:%s" % TAGS_BASIC)
        if status and "playlist_loop" in status:
            result = status["playlist_loop"]
            if fulldetails:
                result = self.process_trackdetails(result)
        return result

    def process_trackdetails(self, items):
        '''processes a list with songs to grab the full track details'''
        return process_method_on_list(self.trackdetails, items)

    def trackdetails(self, lms_song):
        '''gets the full track details and fixes the formatting for kodi compatability'''
        # check cache first
        cache_str = "lmssongdetails.%s.%s" % (lms_song.get("id"), lms_song["title"])
        cache = self.cache.get(cache_str, checksum=lms_song.get("lastUpdated"))
        if cache:
            # merge the details - do not overwrite the playlist index with value from cache
            cache["playlist index"] = lms_song.get("playlist index")
            return cache
        # grab rating, lyrics and comment field (these can't be grabbed from the
        # overall results as it causes strange issues)
        if "id" in lms_song and not int(lms_song.get("remote", 0)):
            result = self.send_request("songinfo 0 100 tags:%s track_id:%s" % (TAGS_FULL, lms_song["id"]))
            if result and result.get("songinfo_loop") and result["songinfo_loop"]:
                for item in result["songinfo_loop"]:
                    # merge results without overwriting
                    for key, value in item.iteritems():
                        if not (lms_song.get(key) or lms_song.get(key) == "0"):
                            lms_song[key] = value
        # correct some other weird stuff
        if not "track_number" in lms_song and "tracknum" in lms_song:
            lms_song["track_number"] = lms_song["tracknum"]
        if not "genres" in lms_song and "genre" in lms_song:
            lms_song["genres"] = lms_song["genre"]
        lms_song["genres"] = " / ".join(lms_song.get("genres", "").split(", "))
        if not "trackartist" in lms_song and "artist" in lms_song:
            lms_song["trackartist"] = lms_song["artist"]
        lms_song["trackartist"] = " / ".join(lms_song.get("trackartist", "").split(", "))
        # correct rating
        if "rating" in lms_song:
            lms_song["rating"] = str((int(lms_song["rating"]) / 100) * 5)
        # grab thumb
        lms_song["thumb"] = self.get_thumb(lms_song)
        if "id" in lms_song and not int(lms_song.get("remote", 0)):  # do not save radio streams to cache
            self.cache.set(cache_str, lms_song, checksum=lms_song.get("lastUpdated"))
        return lms_song

    def send_request(self, cmd):
        '''send request to lms server'''
        if isinstance(cmd, (str, unicode)):
            if "[SP]" in cmd:
                new_cmd = []
                for item in cmd.split():
                    new_cmd.append(item.replace("[SP]", " "))
                cmd = new_cmd
            else:
                cmd = cmd.split()
        url = "http://%s:%s/jsonrpc.js" % (self._host, self._port)
        cmd = [self._playerid, cmd]
        params = {"id": 1, "method": "slim.request", "params": cmd}
        result = self.get_json(url, params)
        return result

    @staticmethod
    def get_json(url, params):
        '''get info from json api'''
        result = {}
        try:
            response = requests.get(url, data=json.dumps(params), timeout=20)
            if response and response.content and response.status_code == 200:
                result = json.loads(response.content.decode('utf-8', 'replace'))
                if "result" in result:
                    result = result["result"]
            else:
                log_msg("Invalid or empty reponse from server - command: %s - server response: %s" %
                        (cmd, response.status_code))
        except Exception:
            log_exception(__name__, "Server is offline or connection error...")

        #log_msg("%s --> %s" %(params, result))
        return result

    def get_thumb(self, item):
        '''get thumb url from the item's properties'''
        thumb = ""
        if item.get("image"):
            thumb = item["image"]
        elif item.get("icon"):
            thumb = item["icon"]
        elif item.get("icon-id"):
            thumb = item["icon-id"]
        elif item.get("artwork_url"):
            thumb = item["artwork_url"]
        elif item.get("artwork_track_id"):
            thumb = "music/%s/cover.png" % item["artwork_track_id"]
        elif item.get("coverid"):
            thumb = "music/%s/cover.png" % item["coverid"]
        elif item.get("album_id"):
            thumb = "imageproxy/mai/album/%s/image.png" % item["album_id"]
        elif item.get("artist_id"):
            thumb = "imageproxy/mai/artist/%s/image.png" % item["artist_id"]
        elif "album" in item and "id" in item:
            thumb = "imageproxy/mai/album/%s/image.png" % item["id"]
        elif "artist" in item and "id" in item:
            thumb = "imageproxy/mai/artist/%s/image.png" % item["id"]
        elif "window" in item and "icon-id" in item["window"]:
            thumb = item["window"]["icon-id"]

        if thumb and not thumb.startswith("http"):
            server_url = "http://%s:%s" % (self._host, self._port)
            if thumb.startswith("/"):
                thumb = "%s%s" % (server_url, thumb)
            else:
                thumb = "%s/%s" % (server_url, thumb)
        return thumb



class LMSDiscovery(object):
    """Class to discover Logitech Media Servers connected to your network."""

    def __init__(self):
        self.entries = []
        self.last_scan = None
        self._lock = threading.RLock()

    def scan(self):
        """Scan the network for servers."""
        with self._lock:
            self.update()

    def all(self):
        """Scan and return all found entries as a list. Each server is a dict."""
        self.scan()
        return list(self.entries)

    def update(self):
        """update the server netry with details"""
        lms_ip = '<broadcast>'
        lms_port = 3483
        # JSON tag has the port number, it's all we need here.
        lms_msg = "eJSON\0"
        lms_timeout = 5
        entries = []
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(lms_timeout)
        sock.bind(('', 0))
        try:
            sock.sendto(lms_msg, (lms_ip, lms_port))
            while True:
                try:
                    data, server = sock.recvfrom(1024)
                    host, _ = server
                    if data.startswith(b'E'):
                        port = data.split("\x04")[1]
                        entries.append({'port': int(port),
                                        'data': data,
                                        'from': server,
                                        'host': host})
                except socket.timeout:
                    break
        finally:
            sock.close()
        self.entries = entries
