#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    script.tv.show.next.aired
    TV Show - Next Aired
    main_service.py
    Background service running the update task
'''

from utils import log_msg, ADDON_ID
import xbmc
import xbmcaddon


class MainService:
    '''our main background service running the update task'''

    def __init__(self):
        addon = xbmcaddon.Addon(ADDON_ID)
        addonname = addon.getAddonInfo('name').decode("utf-8")
        addonversion = addon.getAddonInfo('version').decode("utf-8")
        del addon
        kodimonitor = xbmc.Monitor()       
        log_msg('%s version %s started' % (addonname, addonversion), xbmc.LOGNOTICE)

        while not kodimonitor.abortRequested():
            
            # run update task every hour
            xbmc.executebuiltin("RunScript(script.tv.show.next.aired,update=True)")
            kodimonitor.waitForAbort(3600)

        # Abort was requested while waiting. Do cleanup
        del kodimonitor
        log_msg('%s version %s stopped' % (addonname, addonversion), xbmc.LOGNOTICE)