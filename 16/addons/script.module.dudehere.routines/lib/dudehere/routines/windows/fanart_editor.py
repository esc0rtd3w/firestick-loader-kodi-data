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


CONTROLS = enum(
			CLOSE=82000,
			CLOSE2=82001,
			POSTERS=91050,
			FANARTS=91051,
			PREVIEW = 92050,
			TOGGLE_UP=90007,
			TOGGLE_DOWN=90008,
			TOGGLE=90009,
			LOADING=90010,
			SCROLL1=91052,
			SCROLL2=91053
)

class FanartEditor(BaseWindow):
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
	
	def onInit(self):
		self.getControl(CONTROLS.POSTERS).setVisible(False)
		self.getControl(CONTROLS.FANARTS).setVisible(False)
		self.getControl(CONTROLS.LOADING).setVisible(True)
		
		self.ART = 'poster'
		from dudehere.routines import fanart
		from dudehere.routines.trakt import DB as TraktDB
		fanart.DB = TraktDB
		self.DB = TraktDB
		if plugin.mode == 'update_series_fanart':
			results = fanart.get_all_show_art(plugin.args['trakt_id'])
		else:
			results = fanart.get_all_movie_art(plugin.args['trakt_id'])

		posters = [r for r in results['poster']]
		fanart = [r for r in results['fanart']]
		i=0
		self.getControl(CONTROLS.FANARTS).setVisible(False)
		for p in posters:
			i += 1
			liz = xbmcgui.ListItem('Poster: %s' % i, iconImage='')
			liz.setProperty("url", p)
			self.getControl(CONTROLS.POSTERS).addItem(liz)
		i = 0	
		for f in fanart:
			i += 1
			liz = xbmcgui.ListItem('Fanart: %s' % i, iconImage='')
			liz.setProperty("url", f)
			self.getControl(CONTROLS.FANARTS).addItem(liz)	
		plugin.sleep(500)
		self.getControl(CONTROLS.LOADING).setVisible(False)
		self.getControl(CONTROLS.POSTERS).setVisible(True)
	
	def onEvent(self, event, controlID):
		if controlID==CONTROLS.POSTERS:
			if event in [WINDOW_ACTIONS.ACTION_MOVE_UP, WINDOW_ACTIONS.ACTION_MOVE_DOWN, WINDOW_ACTIONS.ACTION_MOUSE_WHEEL_UP, WINDOW_ACTIONS.ACTION_MOUSE_WHEEL_DOWN, WINDOW_ACTIONS.ACTION_MOUSE_MOVE]:
				img = self.getControl(CONTROLS.POSTERS).getSelectedItem().getProperty("url")
				self.getControl(CONTROLS.PREVIEW).setImage(img)		

		elif controlID==CONTROLS.FANARTS:
			if event in [WINDOW_ACTIONS.ACTION_MOVE_UP, WINDOW_ACTIONS.ACTION_MOVE_DOWN, WINDOW_ACTIONS.ACTION_MOUSE_WHEEL_UP, WINDOW_ACTIONS.ACTION_MOUSE_WHEEL_DOWN, WINDOW_ACTIONS.ACTION_MOUSE_MOVE]:
				img = self.getControl(CONTROLS.FANARTS).getSelectedItem().getProperty("url")
				self.getControl(CONTROLS.PREVIEW).setImage(img)

			
	def onClick(self, controlID):
		media = 'shows' if plugin.mode == 'update_series_fanart' else 'movies'
		key_id = 'tvdb_id' if plugin.mode == 'update_series_fanart' else 'imdb_id'
		id = plugin.args[key_id]
		
		if controlID in [CONTROLS.POSTERS, CONTROLS.FANARTS]:
			index = self.getControl(controlID).getSelectedPosition()
			liz = self.getControl(controlID).getSelectedItem()
			for i in xrange(self.getControl(controlID).size()):
				self.getControl(controlID).getListItem(i).setIconImage('')
			self.getControl(controlID).getListItem(index).setIconImage('checked.png')
			if controlID == CONTROLS.POSTERS:
				img = self.getControl(CONTROLS.POSTERS).getSelectedItem().getProperty("url")
				SQL = "UPDATE fanart_%s SET poster=? WHERE %s=?" %(media, key_id)
			else:
				img = self.getControl(CONTROLS.FANARTS).getSelectedItem().getProperty("url")
				SQL = "UPDATE fanart_%s SET poster=? WHERE %s=?" %(media, key_id)

				
			self.DB.execute(SQL, [img, id])
			
			meta = self.DB.query("SELECT metadata FROM metadata_%s WHERE trakt_id=? " % media, [plugin.args['trakt_id']])
			meta = json.loads(meta[0])
			art = 'cover_url' if self.ART == 'poster' else 'backdrop_url'
			meta[art] = img
			self.DB.execute("UPDATE metadata_%s SET metadata=? WHERE trakt_id=? " % media, [json.dumps(meta), plugin.args['trakt_id']])
			self.DB.commit()
			
		elif controlID in [CONTROLS.CLOSE, CONTROLS.CLOSE2]:
			self.close()
		elif controlID in [ CONTROLS.TOGGLE_UP, CONTROLS.TOGGLE_DOWN]:
			self.getControl(CONTROLS.PREVIEW).setImage('')
			if self.ART == 'poster':
				self.ART = 'fanart'
				self.getControl(CONTROLS.TOGGLE).setLabel("Fanart")
				self.getControl(CONTROLS.FANARTS).setVisible(True)
				self.getControl(CONTROLS.POSTERS).setVisible(False)
				self.getControl(CONTROLS.TOGGLE_UP).controlDown(self.getControl(CONTROLS.FANARTS))
				self.getControl(CONTROLS.TOGGLE_DOWN).controlDown(self.getControl(CONTROLS.FANARTS))
				self.getControl(CONTROLS.CLOSE2).controlUp(self.getControl(CONTROLS.FANARTS))
			else:
				self.ART = 'poster'
				self.getControl(CONTROLS.TOGGLE).setLabel("Poster")
				self.getControl(CONTROLS.TOGGLE_UP).controlDown(self.getControl(CONTROLS.POSTERS))
				self.getControl(CONTROLS.TOGGLE_DOWN).controlDown(self.getControl(CONTROLS.POSTERS))
				self.getControl(CONTROLS.FANARTS).setVisible(False)
				self.getControl(CONTROLS.POSTERS).setVisible(True)
				self.getControl(CONTROLS.CLOSE2).controlUp(self.getControl(CONTROLS.POSTERS))
