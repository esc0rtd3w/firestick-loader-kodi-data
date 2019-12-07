#!/usr/bin/python
# -*- coding: utf-8 -*-
##┌──────────────────────────────────────
##│  YouTube 3D v0.0.6 (2016/02/23)
##│  Copyright (c) Inpane
##│  plugin.video.youtube.3d
##│  http://xbmc.inpane.com/
##│  info@inpane.com
##└──────────────────────────────────────
##
## [ 更新履歴 ]
## 2016/02/23 -> v0.0.6
##  再生前の処理を変更
##
## 2016/01/28 -> v0.0.5
##  JSONの取得に変更
##
## 2016/01/27 -> v0.0.4
##  JSONの取得に変更
##
## 2016/01/25 -> v0.0.3
##  フィードの取得を変更
##
## 2016/01/25 -> v0.0.2
##  フィードの取得を変更
##
## 2014/07/19 -> v0.0.1
##  テスト版公開
##
##==============================================================================
## 設定値をここに記載する。
import sys, os, string

__script_path__    = os.path.abspath( os.path.dirname(__file__) )
__resources_path__ = __script_path__ + '/resources'
__module_path__    = __resources_path__ + '/module'
#-------------------------------------------------------------------------------
sys.path.append (__module_path__)
import re
import threading, time
import httplib, urllib, urllib2, cookielib
import struct, zlib, xml.dom.minidom
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
try:    import json
except: import simplejson as json

import glob, sqlite3
import datetime, calendar
#-------------------------------------------------------------------------------
__addon_id__ = 'plugin.video.youtube.3d'
__settings__ = xbmcaddon.Addon(__addon_id__)

__youtube_url__  = 'plugin://plugin.video.youtube/?action=play_video&videoid='
__youtube_json__ = 'http://kodi.inpane.com/common/cgi/youtube.php?videoDimension=3d'
__keyword__ = 'SBS|stereoscopic|side'

try:    __xbmc_version__ = xbmc.getInfoLabel('System.BuildVersion')
except: __xbmc_version__ = 'Unknown'
class AppURLopener(urllib.FancyURLopener):
	version = 'XBMC/' + __xbmc_version__ + ' - Download and play (' + os.name + ')'
urllib._urlopener = AppURLopener()

IN  = {}
OUT = {}
#-------------------------------------------------------------------------------
def getParams():
	ParamDict = {}
	try:
		#print "getParams() argv=", sys.argv
		if sys.argv[2] : ParamPairs = sys.argv[2][1:].split( "&" )
		for ParamsPair in ParamPairs : 
			ParamSplits = ParamsPair.split('=')
			if (len(ParamSplits)) == 2 : ParamDict[ParamSplits[0]] = ParamSplits[1]
	except : pass
	return ParamDict

#-------------------------------------------------------------------------------
def main():
	global IN
	global OUT
	IN = getParams()

	IN[ 'handle' ] = int(sys.argv[1])
	OUT[ 'handle' ] = IN[ 'handle' ]

	if IN.has_key('ope') and IN['ope'] == "play" :

		# 3D再生形式のダイアログを自動表示しない
		query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"videoplayer.stereoscopicplaybackmode","value":1},"id":1}'
		result = xbmc.executeJSONRPC(query)

		# 3D再生形式の選択を自動的になしに戻さない
		query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"videoplayer.quitstereomodeonstop","value":false},"id":1}'
		result = xbmc.executeJSONRPC(query)

		# 3D再生形式が設定されていなければ、自動的にアナグラフ形式にする。
		query = '{"jsonrpc":"2.0","method":"Settings.GetSettingValue","params":{"setting":"videoscreen.stereoscopicmode"},"id":1}'
		result = xbmc.executeJSONRPC(query)
		rjson = json.loads(result)
		if not rjson['result'].has_key('value') or rjson['result']['value'] == 0:
			query = '{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"videoscreen.stereoscopicmode","value":3},"id":1}'
			result = xbmc.executeJSONRPC(query)

		youtube_url = __youtube_url__ + IN['id']
		addon = youtube_url
		addon = addon.replace('%', '$%$')
		addon = addon.replace('_', '$_$')

		# 一回目の再生：youtubeアドオンから再生用URLを得る
		xbmc.Player().play(youtube_url) # sao
		while not xbmc.Player().isPlaying():
			xbmc.sleep(1)
		url = xbmc.Player().getPlayingFile() + '&_3D_SBS_'
		path, file = os.path.split( url )
		if path: path += ( "/", "\\" )[ not path.count( "/" ) ]
		file = file.replace('%', '$%$')
		file = file.replace('_', '$_$')

		while True:
			xbmc.sleep(1)
			tit  = xbmc.getInfoLabel("Player.Title")
			thum = xbmc.getInfoLabel("Player.Art(thumb)")
			if xbmc.Player().isPlayingVideo() and tit:
				xbmc.Player().pause()
				break

		# レリゴー
		li = xbmcgui.ListItem(tit, "", thum, thum, url)
		xbmc.Player().play(url, li)

		xbmcplugin.endOfDirectory(handle = OUT[ 'handle' ], succeeded = False)

	else : 
		json_url = __youtube_json__
		if '__keyword__' in globals(): json_url = json_url + '&q=' + urllib.quote_plus(__keyword__)
		if IN.has_key('pageToken'): json_url = json_url + '&pageToken=' + IN['pageToken']
		res  = urllib2.urlopen(json_url).read()
		#print res

		rjson = json.loads(res)
		for ItemId in rjson['items']:
			title  = ItemId['snippet']['title']
			thum   = ItemId['snippet']['thumbnails']['medium']['url']
			id     = ItemId['id']['videoId']

			url = 'plugin://' + __addon_id__ + '?ope=play&id=%(id)s' % locals()
			li = xbmcgui.ListItem( title, "", thum, thum )

			commands = []
			commands.append(( 'runme', 'XBMC.RunPlugin(plugin://video/' + __addon_id__ + ')', 'ope=play&id=%(id)s' % locals()))
			li.addContextMenuItems( commands )
			#li.setInfo(type="Video", infoLabels={"Title":title})
			ok = xbmcplugin.addDirectoryItem(OUT[ 'handle' ], url, listitem = li, isFolder=True)

		if rjson.has_key('nextPageToken'): 
			url = 'plugin://' + __addon_id__ + '?ope=list&pageToken=%s' % rjson['nextPageToken']
			li = xbmcgui.ListItem('Next Page', "", "DefaultFolder.png", "DefaultFolder.png", url)
			li.setInfo(type="Video", infoLabels={"Title":'Next Page'})
			xbmcplugin.addDirectoryItem(OUT[ 'handle' ], url, li, isFolder=True)

		xbmcplugin.endOfDirectory(handle = OUT[ 'handle' ], succeeded = True)

#-------------------------------------------------------------------------------
if __name__  == '__main__': main()
