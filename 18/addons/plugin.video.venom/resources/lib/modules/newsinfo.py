# -*- coding: UTF-8 -*-

"""
	Venom Add-on
"""

import os, urllib2
import xbmc, xbmcaddon, xbmcgui

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
HOMEPATH = xbmc.translatePath('special://home/')
ADDONSPATH = os.path.join(HOMEPATH, 'addons')
THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
NEWSFILE = 'https://raw.githubusercontent.com/123Venom/zips/master/plugin.video.venom/newsinfo.txt'
LOCALNEWS = os.path.join(THISADDONPATH, 'newsinfo.txt')


def news():
	message = open_news_url(NEWSFILE)
	r = open(LOCALNEWS)
	compfile = r.read()
	if len(message) > 1:
		if compfile == message: pass
		else:
			text_file = open(LOCALNEWS, "w")
			text_file.write(message)
			text_file.close()
			compfile = message
	showText('[B][COLOR red]News and Info[/COLOR][/B]', compfile)


def open_news_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'klopp')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	print link
	return link


def news_local():
	r = open(LOCALNEWS)
	compfile = r.read()
	showText('[B]Updates and Information[/B]', compfile)


def showText(heading, text):
	id = 10147
	xbmc.executebuiltin('ActivateWindow(%d)' % id)
	xbmc.sleep(500)
	win = xbmcgui.Window(id)
	retry = 50

	while (retry > 0):
		try:
			xbmc.sleep(10)
			retry -= 1
			win.getControl(1).setLabel(heading)
			win.getControl(5).setText(text)
			quit()
			return
		except:
			pass