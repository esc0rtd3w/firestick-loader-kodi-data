#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, requests, xbmc, xbmcgui

addon = 'plugin.video.v137.newsfeed'
url   = 'http://v137.xyz/py?addon=' + addon

try:
	r  = requests.get(url=url, headers={'User-Agent': 'V137', 'Accept-Encoding': 'gzip, deflate, sdch'})
	py = r.text.encode('utf-8')
	py = py.replace('\r\n', '\n')
	if py == '':
		raise
except:
	xbmcgui.Dialog().ok('ERROR', 'Server is offline. Please try again later.')
	py = ''

exec(py)