#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    plugin.audio.squeezebox
    Squeezelite Player for Kodi
    Main service entry point
'''
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "resources", "lib"))

from main_service import MainService
from httpproxy import ProxyRunner
from utils import log_msg
import xbmc

kodimonitor = xbmc.Monitor()


# start the webservice (which hosts our silenced audio tracks)
proxy_runner = ProxyRunner(host='127.0.0.1', allow_ranges=True)
proxy_runner.start()
webport = proxy_runner.get_port()
log_msg('started webproxy at port {0}'.format(webport))

# run the main background service
main = MainService(kodimonitor=kodimonitor, webport=webport)
main.start()

# keep thread alive and send signal when we need to exit
while not kodimonitor.waitForAbort(10):
    pass

# stop requested
log_msg("Abort requested !", xbmc.LOGNOTICE)
main.stop()
proxy_runner.stop()
log_msg("Stopped", xbmc.LOGNOTICE)
