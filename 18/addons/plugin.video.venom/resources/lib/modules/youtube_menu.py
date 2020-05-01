# -*- coding: utf-8 -*-

import sys
import re
# import urllib
import urllib2

from resources.lib.modules import control

syshandle = int(sys.argv[1])


class youtube_menu(object):
	def __init__(self):
		self.agent = 'VGFudHJ1bUFkZG9uQWdlbnQ='.decode('base64')
		self.key_id = 'QUl6YVN5QTU2ckhCQXlLMENsMFA0dURNXzEyc05Pd1VtQWFhczhF'.decode('base64')


	def openMenuFile(self, menuFile):
		req = urllib2.Request(menuFile)
		req.add_header('User-Agent', self.agent)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link


	def processMenuFile(self, menuFile):
		link = self.openMenuFile(menuFile).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?ection="(.+?)".+?earch="(.+?)".+?ubid="(.+?)".+?laylistid="(.+?)".+?hannelid="(.+?)".+?ideoid="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
		return match


	def addMenuItem(self, name, action, subid, iconimage, fanart, description='', isFolder=True):
		u = sys.argv[0] + "?action=" + action + "&subid=" + subid
		liz = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo(type='video', infoLabels={'title': name, 'plot': description})
		liz.setProperty('Fanart_Image', fanart)
		control.addItem(handle=syshandle, url=u, listitem=liz, isFolder=isFolder)


	def addSectionItem(self, name, iconimage, fanart):
		u = sys.argv[0] + "?action=sectionItem"
		liz = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('Fanart_Image', fanart)
		control.addItem(handle=syshandle, url=u, listitem=liz, isFolder=False)


	def addSearchItem(self, name, search_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/kodion/search/query/?q=%s" % search_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addChannelItem(self, name, channel_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/channel/%s/" % channel_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addUserItem(self, name, channel_id, icon, fanart):
		user = channel_id
		work_url = "plugin://plugin.video.youtube/user/%s/" % user
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addPlaylistItem(self, name, playlist_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/playlist/%s/" % playlist_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addVideoItem(self, name, video_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		# liz.setPath(work_url)
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		liz.setProperty('IsPlayable', 'true')
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=False)

