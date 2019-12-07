# -*- coding: utf-8 -*-

import os,xbmc,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs


region = xbmc.getRegion

lang = xbmcaddon.Addon().getLocalizedString

setting = xbmcaddon.Addon().getSetting

addon = xbmcaddon.Addon

addItem = xbmcplugin.addDirectoryItem

item = xbmcgui.ListItem

directory = xbmcplugin.endOfDirectory

content = xbmcplugin.setContent

property = xbmcplugin.setProperty

addonInfo = xbmcaddon.Addon().getAddonInfo

infoLabel = xbmc.getInfoLabel

condVisibility = xbmc.getCondVisibility

jsonrpc = xbmc.executeJSONRPC

window = xbmcgui.Window(10000)

dialog = xbmcgui.Dialog()

progressDialog = xbmcgui.DialogProgress()

windowDialog = xbmcgui.WindowDialog()

button = xbmcgui.ControlButton

image = xbmcgui.ControlImage

keyboard = xbmc.Keyboard

sleep = xbmc.sleep

execute = xbmc.executebuiltin

skin = xbmc.getSkinDir()

player = xbmc.Player()

playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

resolve = xbmcplugin.setResolvedUrl

openFile = xbmcvfs.File

makeFile = xbmcvfs.mkdir

deleteFile = xbmcvfs.delete

listDir = xbmcvfs.listdir

transPath = xbmc.translatePath

skinPath = xbmc.translatePath('special://skin/')

addonPath = xbmc.translatePath(addonInfo('path'))

dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')

settingsFile = os.path.join(dataPath, 'settings.xml')

databaseFile = os.path.join(dataPath, 'settings.db')

favouritesFile = os.path.join(dataPath, 'favourites.db')

sourcescacheFile = os.path.join(dataPath, 'sources.db')

cachemetaFile = os.path.join(dataPath, 'metacache.db')

libcacheFile = os.path.join(dataPath, 'library.db')

metacacheFile = os.path.join(dataPath, 'meta.db')

cacheFile = os.path.join(dataPath, 'cache.db')


def selectDialog(list, heading="TEST"):
    return dialog.select(heading, list)

def TEST():
    return 
