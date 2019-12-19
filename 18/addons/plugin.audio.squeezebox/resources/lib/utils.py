#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    plugin.audio.squeezebox
    Squeezelite Player for Kodi
    utils.py
    Various helper methods
'''

import xbmc
import xbmcvfs
import xbmcaddon
import subprocess
import os
import stat
import sys
import urllib
from traceback import format_exc
import requests

try:
    import simplejson as json
except Exception:
    import json


ADDON_ID = "plugin.audio.squeezebox"
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])
KODILANGUAGE = xbmc.getLanguage(xbmc.ISO_639_1)

try:
    from multiprocessing.pool import ThreadPool
    SUPPORTS_POOL = True
except Exception:
    SUPPORTS_POOL = False


def log_msg(msg, loglevel=xbmc.LOGNOTICE):
    '''log message to kodi log'''
    if isinstance(msg, unicode):
        msg = msg.encode('utf-8')
    xbmc.log("%s --> %s" % (ADDON_ID, msg), level=loglevel)


def log_exception(modulename, exceptiondetails):
    '''helper to properly log an exception'''
    log_msg(format_exc(sys.exc_info()), xbmc.LOGDEBUG)
    log_msg("Exception in %s ! --> %s" % (modulename, exceptiondetails), xbmc.LOGWARNING)


def get_mac():
    '''helper to obtain the mac address of the kodi machine'''
    count = 0
    mac = ""
    monitor = xbmc.Monitor()
    while ":" not in mac and count < 360 and not monitor.abortRequested():
        log_msg("Waiting for mac address...")
        mac = xbmc.getInfoLabel("Network.MacAddress").lower()
        count += 1
        monitor.waitForAbort(1)
    del monitor
    if not mac:
        log_msg("Mac detection failed!")
    else:
        log_msg("Detected Mac-Address: %s" % mac)
    return mac
    
def get_squeezelite_binary():
    '''find the correct squeezelite binary belonging to the platform'''
    sl_binary = ""
    addon = xbmcaddon.Addon(id=ADDON_ID)
    custom_path = addon.getSetting("squeezelite_path").decode("utf-8")
    del addon
    if custom_path:
        sl_binary = custom_path
    elif xbmc.getCondVisibility("System.Platform.Windows"):
        sl_binary = os.path.join(os.path.dirname(__file__), "bin", "win32", "squeezelite-win.exe")
    elif xbmc.getCondVisibility("System.Platform.OSX"):
        sl_binary = os.path.join(os.path.dirname(__file__), "bin", "osx", "squeezelite")
        st = os.stat(sl_binary)
        os.chmod(sl_binary, st.st_mode | stat.S_IEXEC)
    elif xbmcvfs.exists("/storage/.kodi/addons/virtual.multimedia-tools/bin/squeezelite"):
        # libreelec has squeezelite preinstalled with the multimedia tools
        sl_binary = "/storage/.kodi/addons/virtual.multimedia-tools/bin/squeezelite"
    elif xbmc.getCondVisibility("System.Platform.Linux.RaspberryPi"):
        sl_binary = os.path.join(os.path.dirname(__file__), "bin", "linux", "squeezelite-arm")
        st = os.stat(sl_binary)
        os.chmod(sl_binary, st.st_mode | stat.S_IEXEC)
    elif xbmc.getCondVisibility("System.Platform.Linux"):
        if sys.maxsize > 2**32:
            sl_binary = os.path.join(os.path.dirname(__file__), "bin", "linux", "squeezelite-i64")
        else:
            sl_binary = os.path.join(os.path.dirname(__file__), "bin", "linux", "squeezelite-x86")
        st = os.stat(sl_binary)
        os.chmod(sl_binary, st.st_mode | stat.S_IEXEC)
    else:
        log_msg("Unsupported platform! - for iOS and Android you need to install a squeezeplayer app yourself and make sure it's running in the background.")
    return sl_binary

def get_audiodevices(sl_binary=None):
    ''' get available audio devices for squeezelite'''
    result = []
    if not sl_binary:
        sl_binary = get_squeezelite_binary()
    args = [sl_binary, "-l"]
    startupinfo = None
    if xbmc.getCondVisibility("System.Platform.Windows"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
    sl_exec = subprocess.Popen(args, startupinfo=startupinfo, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    stdout, stderr = sl_exec.communicate()
    for line in stdout.split("\n"):
        line = line.strip()
        if line and not "Output devices:" in line:
            result.append(line)
    return result
    
def get_audiodevice(sl_binary):
    '''get the audiodevice to use for squeezelite'''
    addon = xbmcaddon.Addon(id=ADDON_ID)
    user_device = addon.getSetting("output_device").decode("utf-8")
    del addon
    if user_device and user_device != "auto":
        return user_device
    
    args = [sl_binary, "-l"]
    startupinfo = None
    if xbmc.getCondVisibility("System.Platform.Windows"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
    sl_exec = subprocess.Popen(args, startupinfo=startupinfo, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    stdout, stderr = sl_exec.communicate()
    for line in get_audiodevices():
        if "default" in line:
            return line.split("-")[0].strip()
    return "default"

def process_method_on_list(method_to_run, items):
    '''helper method that processes a method on each listitem with pooling if the system supports it'''
    all_items = []
    if SUPPORTS_POOL:
        pool = ThreadPool()
        try:
            all_items = pool.map(method_to_run, items)
        except Exception:
            # catch exception to prevent threadpool running forever
            log_msg(format_exc(sys.exc_info()))
            log_msg("Error in %s" % method_to_run)
        pool.close()
        pool.join()
    else:
        all_items = [method_to_run(item) for item in items]
    all_items = filter(None, all_items)
    return all_items


def parse_duration(durationobj):
    '''
        lms is a mess with typing,
        I've seen the duration being returned as string, float and int
        This will try to parse the result from LMS into a int
    '''
    result = 0
    try:
        result = int(durationobj)
    except ValueError:
        try:
            result = float(durationobj)
            result = int(result)
        except ValueError:
            log_exception(__name__, "Error parsing track duration")
    return result
