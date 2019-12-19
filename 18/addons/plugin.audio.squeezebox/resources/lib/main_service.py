#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    plugin.audio.squeezebox
    Squeezelite Player for Kodi
    main_service.py
    Background service which launches the squeezelite binary and monitors the player
'''

from utils import log_msg, ADDON_ID, log_exception, get_mac, get_squeezelite_binary, get_audiodevice
from player_monitor import KodiPlayer
from lmsserver import LMSServer, LMSDiscovery
import xbmc
import xbmcaddon
import xbmcgui
import subprocess
import os
import sys
import xbmcvfs
import stat
import threading


class MainService(threading.Thread):
    '''our main background service running the various tasks'''
    exit = False
    event = None
    lmsserver = None
    addon = None
    win = None
    kodiplayer = None
    _sl_exec = None
    _prev_checksum = ""
    _temp_power_off = False

    def __init__(self, *args, **kwargs):
        self.win = xbmcgui.Window(10000)
        self.win.clearProperty("lmsexit")
        self.addon = xbmcaddon.Addon(id=ADDON_ID)
        self.kodimonitor = kwargs.get("kodimonitor")
        self._webport = kwargs.get("webport")
        self.event = threading.Event()
        threading.Thread.__init__(self, *args)

    def run(self):

        # get playerid based on mac address
        if self.addon.getSetting("disable_auto_mac") == "true" and self.addon.getSetting("manual_mac"):
            playerid = self.addon.getSetting("manual_mac").decode("utf-8")
        else:
            playerid = get_mac()

        # discover server
        if self.addon.getSetting("disable_auto_lms") == "true":
            # manual server
            lmshost = self.addon.getSetting("lms_hostname")
            lmsport = self.addon.getSetting("lms_port")
            self.lmsserver = LMSServer(lmshost, lmsport, playerid)
        else:
            # auto discovery
            while not self.lmsserver and not self.exit:
                servers = LMSDiscovery().all()
                log_msg("discovery: %s" % servers)
                if servers:
                    server = servers[0]  # for now, just use the first server discovered
                    lmshost = server.get("host")
                    lmsport = server.get("port")
                    self.lmsserver = LMSServer(lmshost, lmsport, playerid)
                    log_msg("LMS server discovered - host: %s - port: %s" % (lmshost, lmsport))
                else:
                    self.kodimonitor.waitForAbort(2)

        if self.lmsserver:
            # publish lmsdetails as window properties for the plugin entry
            self.win.setProperty("lmshost", lmshost)
            self.win.setProperty("lmsport", str(lmsport))
            self.win.setProperty("lmsplayerid", playerid)

            # start squeezelite executable
            self.start_squeezelite()

            # initialize kodi player monitor
            self.kodiplayer = KodiPlayer(lmsserver=self.lmsserver, webport=self._webport)

            # report player as awake
            self.lmsserver.send_command("power 1")

            # mainloop
            while not self.exit:
                # monitor the LMS state changes
                if not (xbmc.getCondVisibility("System.Platform.Android") and playerid.lower() == get_mac().lower()):
                    # TODO: implement fake OSD for android
                    self.monitor_lms()
                # sleep for 1 second
                self.kodimonitor.waitForAbort(1)

    def stop(self):
        '''stop running our background service '''
        if self.lmsserver:
            self.lmsserver.send_command("power 0")  # report player as powered off
        self.win.setProperty("lmsexit", "true")
        self.stop_squeezelite()
        if self.kodiplayer:
            self.kodiplayer.close()
            del self.kodiplayer
        self.exit = True
        self.event.set()
        self.event.clear()
        self.join(0.5)
        del self.win
        del self.addon

    def monitor_lms(self):
        '''monitor the state of the self.lmsserver/player'''
        # poll the status every interval
        self.lmsserver.update_status()

        if self.exit:
            return

        # make sure that the status is not actually changing right now
        if not self.lmsserver.state_changing and not self.kodiplayer.is_busy:

            # monitor LMS player and server details
            if self._sl_exec and (self.lmsserver.power ==
                                  1 or not self._temp_power_off) and xbmc.getCondVisibility("Player.HasVideo"):
                # turn off lms player when kodi is playing video
                self.lmsserver.send_command("power 0")
                self._temp_power_off = True
                self.kodiplayer.is_playing = False
                log_msg("Kodi started playing video - disabled the LMS player")
            elif self._temp_power_off and not xbmc.getCondVisibility("Player.HasVideo"):
                # turn on player again when video playback was finished
                self.lmsserver.send_command("power 1")
                self._temp_power_off = False
            elif self.kodiplayer.is_playing and self._prev_checksum != self.lmsserver.timestamp:
                # the playlist was modified
                self._prev_checksum = self.lmsserver.timestamp
                log_msg("playlist changed on lms server")
                self.kodiplayer.update_playlist()
                self.kodiplayer.play(self.kodiplayer.playlist, startpos=self.lmsserver.cur_index)
            elif not self.kodiplayer.is_playing and self.lmsserver.mode == "play":
                # playback started
                log_msg("play started by lms server")
                if not len(self.kodiplayer.playlist):
                    self.kodiplayer.update_playlist()
                self.kodiplayer.play(self.kodiplayer.playlist, startpos=self.lmsserver.cur_index)

            elif self.kodiplayer.is_playing:
                # monitor some conditions if the player is playing
                if self.kodiplayer.is_playing and self.lmsserver.mode == "stop":
                    # playback stopped
                    log_msg("stop requested by lms server")
                    self.kodiplayer.stop()
                elif xbmc.getCondVisibility("Playlist.IsRandom"):
                    # make sure that the kodi player doesnt have shuffle enabled
                    log_msg("Playlist is randomized! Reload to unshuffle....")
                    self.kodiplayer.playlist.unshuffle()
                    self.kodiplayer.update_playlist()
                    self.kodiplayer.play(self.kodiplayer.playlist, startpos=self.lmsserver.cur_index)
                elif xbmc.getCondVisibility("Player.Paused") and self.lmsserver.mode == "play":
                    # playback resumed
                    log_msg("resume requested by lms server")
                    xbmc.executebuiltin("PlayerControl(play)")
                elif not xbmc.getCondVisibility("Player.Paused") and self.lmsserver.mode == "pause":
                    # playback paused
                    log_msg("pause requested by lms server")
                    self.kodiplayer.pause()
                elif self.kodiplayer.playlist.getposition() != self.lmsserver.cur_index:
                    # other track requested
                    log_msg("other track requested by lms server")
                    self.kodiplayer.play(self.kodiplayer.playlist, startpos=self.lmsserver.cur_index)
                elif self.lmsserver.status["title"] != xbmc.getInfoLabel("MusicPlayer.Title").decode("utf-8"):
                    # monitor if title still matches
                    log_msg("title mismatch - updating playlist...")
                    self.kodiplayer.update_playlist()
                    self.kodiplayer.play(self.kodiplayer.playlist, startpos=self.lmsserver.cur_index)
                elif self.lmsserver.mode == "play" and not self.lmsserver.status["current_title"]:
                    # check if seeking is needed - if current_title has value, it means it's a radio stream so we ignore that
                    # we accept a difference of max 2 seconds
                    cur_time_lms = int(self.lmsserver.time)
                    cur_time_kodi = self.kodiplayer.cur_time()
                    if cur_time_kodi > 2:
                        if cur_time_kodi != cur_time_lms and abs(
                                cur_time_lms - cur_time_kodi) > 2 and not xbmc.getCondVisibility("Player.Paused"):
                            # seek started
                            log_msg("seek requested by lms server - kodi-time: %s  - lmstime: %s" %
                                    (cur_time_kodi, cur_time_lms))
                            self.kodiplayer.is_busy = True
                            self.kodiplayer.seekTime(cur_time_lms)
                            xbmc.sleep(250)
                            self.kodiplayer.is_busy = False

    def start_squeezelite(self):
        '''On supported platforms we include squeezelite binary'''
        playername = xbmc.getInfoLabel("System.FriendlyName").decode("utf-8")
        if self.addon.getSetting("disable_auto_squeezelite") != "true":
            sl_binary = get_squeezelite_binary()
            if sl_binary and self.lmsserver:
                try:
                    sl_output = get_audiodevice(sl_binary)
                    self.kill_squeezelite()
                    log_msg("Starting Squeezelite binary - Using audio device: %s" % sl_output)
                    args = [sl_binary, "-s", self.lmsserver.host, "-a", "80", "-C", "1", "-m",
                            self.lmsserver.playerid, "-n", playername, "-M", "Kodi", "-o", sl_output]
                    startupinfo = None
                    if os.name == 'nt':
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
                    self._sl_exec = subprocess.Popen(args, startupinfo=startupinfo, stderr=subprocess.STDOUT)
                except Exception as exc:
                    log_exception(__name__, exc)
        if not self._sl_exec:
            log_msg("The Squeezelite binary was not automatically started, "
                    "you should make sure of starting it yourself, e.g. as a service.")
            self._sl_exec = False

    def stop_squeezelite(self):
        '''stop squeezelite if supported'''
        if self._sl_exec:
            self._sl_exec.terminate()

    @staticmethod
    def kill_squeezelite():
        '''make sure we don't have any (remaining) squeezelite processes running before we start one'''
        if xbmc.getCondVisibility("System.Platform.Windows"):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(["taskkill", "/IM", "squeezelite-win.exe"], startupinfo=startupinfo, shell=True)
            subprocess.Popen(["taskkill", "/IM", "squeezelite.exe"], startupinfo=startupinfo, shell=True)
        else:
            os.system("killall squeezelite")
            os.system("killall squeezelite-i64")
            os.system("killall squeezelite-x86")
        xbmc.sleep(2000)
