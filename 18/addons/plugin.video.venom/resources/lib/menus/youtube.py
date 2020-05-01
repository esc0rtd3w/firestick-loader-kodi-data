# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

import sys

from resources.lib.modules import control
from resources.lib.modules import youtube_menu

thishandle = int(sys.argv[1])


class yt_index:  # initializes as musicvids, functions can override based on action and subid.
	def __init__(self):
		self.action = 'musicvids'
		self.base_url = 'https://raw.githubusercontent.com/123venom/xml/master/youtube/'
		self.mainmenu = self.base_url + 'musicvids.txt'
		self.submenu = '%s/%s.txt'
		self.default_icon = '%s/icons/music_video_folder_icon.png'
		self.default_fanart = '%s/icons/music_video_folder_fanart.jpg'

	def init_vars(self, action):
		try:
			if action == 'youtube':
				self.action = 'youtube'
				self.base_url = 'https://raw.githubusercontent.com/123venom/xml/master/youtube/'
				self.mainmenu = self.base_url + 'ytmain.txt'
			self.submenu = self.submenu % (self.base_url, '%s')
			self.default_icon = self.default_icon % (self.base_url)
			self.default_fanart = self.default_fanart % (self.base_url)
		except:
			pass


	def root(self, action):
		try:
			self.init_vars(action)

			menuItems = youtube_menu.youtube_menu().processMenuFile(self.mainmenu)

			for name, section, searchid, subid, playlistid, channelid, videoid, iconimage, fanart, description in menuItems:
				if subid != 'false': # Means this item points to a submenu
					youtube_menu.youtube_menu().addMenuItem(name, self.action, subid, iconimage, fanart, description, True)
				elif searchid != 'false': # Means this is a search term
					youtube_menu.youtube_menu().addSearchItem(name, searchid, iconimage, fanart)
				elif videoid != 'false': # Means this is a video id entry
					youtube_menu.youtube_menu().addVideoItem(name, videoid, iconimage, fanart)
				elif channelid != 'false': # Means this is a channel id entry
					if channelid.startswith('UC'):
						youtube_menu.youtube_menu().addChannelItem(name, channelid, iconimage, fanart)
					else:
						# This really needs it's own userid created in the .txt files
						youtube_menu.youtube_menu().addUserItem(name, channelid, iconimage, fanart)
				elif playlistid != 'false': # Means this is a playlist id entry
					youtube_menu.youtube_menu().addPlaylistItem(name, playlistid, iconimage, fanart)
				elif section != 'false': # Means this is a section placeholder/info line
					youtube_menu.youtube_menu().addSectionItem(name, self.default_icon, self.default_fanart)
			self.endDirectory()
		except:
			pass


	def get(self, action, subid):
		try:
			self.init_vars(action)

			thisMenuFile = self.submenu % (subid)
			menuItems = youtube_menu.youtube_menu().processMenuFile(thisMenuFile)

			for name, section, searchid, subid, playlistid, channelid, videoid, iconimage, fanart, description in menuItems:
				if subid != 'false': # Means this item points to a submenu
					youtube_menu.youtube_menu().addMenuItem(name, self.action, subid, iconimage, fanart, description, True)
				elif searchid != 'false': # Means this is a search term
					youtube_menu.youtube_menu().addSearchItem(name, searchid, iconimage, fanart)
				elif videoid != 'false': # Means this is a video id entry
					youtube_menu.youtube_menu().addVideoItem(name, videoid, iconimage, fanart)
				elif channelid != 'false': # Means this is a channel id entry
					if channelid.startswith('UC'):
						youtube_menu.youtube_menu().addChannelItem(name, channelid, iconimage, fanart)
					else:
						# This really needs it's own userid created in the .txt files
						youtube_menu.youtube_menu().addUserItem(name, channelid, iconimage, fanart)
				elif playlistid != 'false': # Means this is a playlist id entry
					youtube_menu.youtube_menu().addPlaylistItem(name, playlistid, iconimage, fanart)
				elif section != 'false': # Means this is a section placeholder/info line
					youtube_menu.youtube_menu().addSectionItem(name, self.default_icon, self.default_fanart)
			self.endDirectory()
		except:
			pass


	def endDirectory(self):
		control.directory(thishandle, cacheToDisc=True)