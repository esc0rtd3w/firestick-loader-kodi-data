#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"

'''*
	Copyright (C) 2016 DudeHere

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

*'''

import re
import json
import xbmc
import xbmcgui
import xbmcaddon
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.windows import BaseWindow
from dudehere.routines.constants import WINDOW_ACTIONS
from dudehere.routines.trakt import TraktAPI
trakt = TraktAPI()

CONTROLS = enum(
			SHOWS=80050,
			WORKING=85001,
			TOTALS=85002,
			CLOSE=82000,
			SET_LIST=82001,
			LISTS=91050,
			CONTEXT=84001,
			CONTEXT_WINDOW=84000
)

class ContextWindow(BaseWindow):
	height = False
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
	
	def onInit(self):
		self.choice = None
		for c in ["Mark Watched", "Go to Seasons", "Add-on Settings"]:
			liz = xbmcgui.ListItem(c, iconImage='')
			self.getControl(CONTROLS.CONTEXT).addItem(liz)
		if self.height:
			self.getControl(84002).setHeight(self.height)
				
	def onClick(self, controlID):
		if controlID==CONTROLS.CONTEXT:
			index = self.getControl(CONTROLS.CONTEXT).getSelectedPosition()
			liz = self.getControl(CONTROLS.CONTEXT).getSelectedItem()
			self.choice = liz.getLabel()
			self.close()
		elif controlID == '84005':
			self.close()	

class OnNextWindow(BaseWindow):
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
	
	def onInit(self):
		self.getControl(CONTROLS.WORKING).setVisible(True)
		self.getControl(CONTROLS.SHOWS).reset()
		resume_imdb_id = plugin.get_property('Resume.imdb_id')
		resume_index = None
		plugin.clear_property('Resume.imdb_id')
		default_list = plugin.get_setting("default_trakt_list")
		if plugin.get_arg('slug'):
			shows = trakt.get_progress(plugin.get_arg('slug'))
		elif default_list:
			shows = trakt.get_progress(default_list)
		else:
			lists = trakt.get_custom_lists()
			shows = []
			for li in lists:
				shows += trakt.get_progress(li['ids']['slug'])
		total_episodes = 0
		watched_episodes = 0
		
		regex = re.compile("^(A )|(An )|(The )", re.IGNORECASE)
		def sort_show(show):
			title = regex.sub('', show['show']['title'], re.IGNORECASE)
			return title.lower()
		
		shows.sort(key=lambda k: sort_show(k))
		for show in shows:
			if int(show['progress']['show']['percent']) == 1: continue
			liz = xbmcgui.ListItem('[B]' + show['show']['title'] + '[/B]')

			progress = "%s of %s" % (show['progress']['show']['watched'], show['progress']['show']['total'])
			percent = "progress/%s.png" % int(show['progress']['show']['percent']*100)
			if show['progress']['next']:
				if show['show']['ids']['imdb'] == resume_imdb_id:
					resume_index = self.getControl(CONTROLS.SHOWS).size()
				episode = show['episodes'][show['progress']['next']['season']][show['progress']['next']['number']-1]
				next = "%sx%s - %s" % (show['progress']['next']['season'], show['progress']['next']['number'], show['progress']['next']['title'])
				liz.setProperty("next", next)

				liz.setProperty("description", episode['overview'])
				liz.setProperty("imdb_id", show['show']['ids']['imdb'])
				liz.setProperty("trakt_id", str(show['progress']['next']['ids']['trakt']))
				liz.setProperty("slug", show['show']['ids']['slug'])
				liz.setProperty("showtitle", show['show']['title'])
				liz.setProperty("season", str(show['progress']['next']['season']))
				liz.setProperty("episode", str(show['progress']['next']['number']))
				liz.setProperty("fanart", show['show']['images']['fanart']['full'])
				screenshot = episode['images']['screenshot']['thumb']
				if not screenshot:
					screenshot = 'off_air.jpg'
				liz.setIconImage(screenshot)
			else: 
				continue
			liz.setProperty("seasons", "Seasons: %s" % show['season_count'])
			liz.setProperty("progress", progress)
			liz.setProperty("percent", percent)
			total_episodes += show['progress']['show']['total']
			watched_episodes += show['progress']['show']['watched']
			self.getControl(CONTROLS.SHOWS).addItem(liz)
		if resume_index is not None:
			self.getControl(CONTROLS.SHOWS).selectItem(resume_index)	
		progress = "%s of %s" % (watched_episodes, total_episodes)
		self.getControl(CONTROLS.TOTALS).setLabel(progress)
		self.getControl(CONTROLS.WORKING).setVisible(False)	

	def onAction(self, action):
		action = action.getId()
		if action in [WINDOW_ACTIONS.ACTION_PREVIOUS_MENU, WINDOW_ACTIONS.ACTION_NAV_BACK]:
			self._close()
		
		try:
			if action in [WINDOW_ACTIONS.ACTION_SHOW_INFO, WINDOW_ACTIONS.ACTION_CONTEXT_MENU]:
				skin_path = plugin.get_addon('script.module.dudehere.routines').getAddonInfo('path')
				controlID = self.getFocus().getId()
				index = self.getControl(CONTROLS.SHOWS).getSelectedPosition()
				liz = self.getControl(CONTROLS.SHOWS).getSelectedItem()
				CTX = ContextWindow("context.xml", skin_path)
				CTX.height = 165
				CTX.doModal()
				
				choice = CTX.choice
				del CTX
				if choice == 'Go to Seasons':
					params = {"mode": "season_list", "imdb_id": liz.getProperty('imdb_id'), "fanart":  liz.getProperty('fanart'), "title": liz.getProperty('showtitle')}
					plugin_url = plugin.build_plugin_url(params)
					self.close()
					plugin.go_to_url(plugin_url)
				elif choice == 'Mark Watched':
					params = {"mode": "set_watched", "media": "episode", "id": liz.getProperty('trakt_id'), "imdb_id": liz.getProperty('imdb_id'), "season": liz.getProperty('season'), "episode": liz.getProperty('episode')}
					plugin.execute_query(params)
					plugin.sleep(2000)
					self.onInit()
				elif choice == 'Add-on Settings':
					plugin.open_settings()
				elif choice == 'Change Lists':
					skin_path = plugin.get_addon('script.module.dudehere.routines').getAddonInfo('path')
					LI = SetListWindow("setlist.xml", skin_path)
					LI.doModal()
					del LI	
		except:
			pass
		
	def onClick(self, controlID):
		if controlID==CONTROLS.CLOSE:
			self._close()

		elif controlID == CONTROLS.SHOWS:
			liz = self.getControl(CONTROLS.SHOWS).getSelectedItem()
			params = {"mode": "play_episode", 
					"media_type": "stream", 
					"showtitle": liz.getProperty('showtitle'), 
					"display": liz.getProperty('showtitle'), 
					"imdb_id": liz.getProperty('imdb_id'), 
					"slug": liz.getProperty('slug'), 
					"season":liz.getProperty('season'),  
					"episode": liz.getProperty('episode'),
					"year": 2001
			}
			
			plugin.set_property('Resume.Page', PLUGIN_URL)
			plugin.set_property('Resume.imdb_id', liz.getProperty('imdb_id'))
			plugin_url = plugin.build_plugin_url(params)
			self.close()
			if plugin.get_setting('custom_stream_dialog') == 'true':
				plugin.execute_url(plugin_url)
			else:
				plugin.play_url(plugin_url)
				
class SetListWindow(BaseWindow):
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
	
	def onInit(self):
		lists = trakt.get_custom_lists()
		items = []
		default_list = plugin.get_setting('default_list')
		for li in lists:
			icon = 'checked.png' if li['ids']['slug'] == default_list else ''
			liz = xbmcgui.ListItem(li['name'], iconImage=icon)
			liz.setProperty("slug", li['ids']['slug'])
			items.append(liz)
		self.getControl(CONTROLS.LISTS).addItems(items)
	
	def onClick(self, controlID):
		if controlID==CONTROLS.LISTS:
			index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
			liz = self.getControl(CONTROLS.LISTS).getSelectedItem()
			for i in xrange(self.getControl(CONTROLS.LISTS).size()):
				self.getControl(CONTROLS.LISTS).getListItem(i).setIconImage('')
			self.getControl(CONTROLS.LISTS).getListItem(index).setIconImage('checked.png')
			plugin.set_setting('default_list', liz.getProperty("slug"))