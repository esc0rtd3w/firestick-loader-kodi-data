#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"

'''*
	Copyright (C) 2015 DudeHere

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

import json
import sys
import os
import re
import cgi
import zlib
import random
try:
	import cPickle as _pickle
except:
	import pickle  as _pickle

pickle = _pickle.dumps

import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmc
from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING
import xbmcvfs
import urllib
import urlparse
from dudehere.routines import *
from dudehere.routines.vfs import VFSClass
vfs = VFSClass()

addon = xbmcaddon.Addon()
__get_setting = addon.getSetting
__set_setting = addon.setSetting
show_settings = addon.openSettings
open_settings = show_settings
sleep = xbmc.sleep
get_condition_visiblity = xbmc.getCondVisibility
__log = xbmc.log
__dispatcher = {}
__kargs = {}

default_context_menu_items = []
replace_context_menu_by_default = True

def unpickle(pickled):
	try:
		return _pickle.loads(pickled)
	except TypeError:
		return _pickle.loads(str(pickled))
	

def get_addon(addon_id):
	return xbmcaddon.Addon(addon_id)

def get_setting(k, addon_id=None):
	if addon_id is None:
		return __get_setting(k)
	else:
		return xbmcaddon.Addon(addon_id).getSetting(k)

def set_setting(k, v, addon_id=None):
	if addon_id is None:
		return __set_setting(k, v)
	else:
		return xbmcaddon.Addon(addon_id).setSetting(k, v)

def str2bool(v):
		if not v: return False
		return v.lower() in ("yes", "true", "t", "1")
	
def get_bool_setting( k):
	return(str2bool(get_setting(k)))
	
def raise_notify(title, message, timeout=3000):
	image = vfs.join( get_path(), 'icon.png')
	cmd = "XBMC.Notification(%s, %s, %s, %s)" % (title, message, timeout, image)
	xbmc.executebuiltin(cmd)

def raise_error(self, title, m1='', m2=''):
	dialog = xbmcgui.Dialog()
	dialog.ok("%s ERROR!" % ADDON_NAME, str(title), str(m1), str(m2))

def save_data(file, data, format='pickle', compress=False):
	if format == 'pickle':
		if compress:
			data =  zlib.compress(pickle(data))
		else:
			data = pickle(data)
		vfs.write_file(file, data, mode='b')
	else:
		data = json.dumps(data)
		if compress:
			data = zlib.compress(data)
		vfs.write_file(file, data)
	
	 
def load_data(file, format='pickle', compress=False):
	if format == 'pickle':
		try:
			data = vfs.read_file(file, mode='b')
			if compress:
				data = zlib.decompress(data)
			return unpickle(data)
		except Exception, e:
			log(e)
			return None
	else:
		try:
			data = vfs.read_file(file)
			if compress:
				data = zlib.decompress(data)
			return json.loads()
		except Exception, e:
			log(e)
			return None
def log(msg, level=LOGNOTICE):
	try:
		if isinstance(msg, unicode):
			msg = msg.encode('utf-8')
		__log('%s: %s' % (ADDON_NAME, msg), level)
	except Exception as e:
		try: __log('Logging Failure: %s' % (e), level)
		except: pass  # just give up

if get_setting('database_type')=='1':
	DB_NAME = get_setting('database_mysql_name')
	DB_USER = get_setting('database_mysql_user')
	DB_PASS = get_setting('database_mysql_pass')
	DB_PORT = get_setting('database_mysql_port')
	DB_ADDRESS = get_setting('database_mysql_host')
	DB_TYPE = 'mysql'
	from dudehere.routines.database import MySQLDatabase as DatabaseAPI

else:
	DB_TYPE = 'sqlite'
	DB_FILE = xbmc.translatePath(get_setting('database_sqlite_file'))
	from dudehere.routines.database import SQLiteDatabase as DatabaseAPI

class MyDatabaseAPI(DatabaseAPI):
	def _initialize(self):
		root = xbmcaddon.Addon('script.module.dudehere.routines').getAddonInfo('path')
		schema_file = vfs.join(root, 'resources/database/schema.%s.sql' % self.db_type)
		if self.run_script(schema_file, commit=False):
			self.execute('DELETE FROM version WHERE 1')
			self.execute('INSERT INTO version(db_version) VALUES(?)', [self.db_version])
			self.commit()
	
	def do_init(self):
		do_init = True
		try:
			test = self.query("SELECT 1 FROM version WHERE db_version >= ?", [self.db_version], silent=True)
			if test:
				do_init = False
		except:
			do_init = True
		return do_init


if DB_TYPE == 'mysql':
	DB=MyDatabaseAPI(DB_ADDRESS, DB_NAME, DB_USER, DB_PASS, DB_PORT, version=DB_VERSION, connect=False)
else:
	DB = MyDatabaseAPI(DB_FILE, version=DB_VERSION, connect=False)

def get_main_DB():
	addon_id = xbmc.getInfoLabel('Container.PluginName')
	if get_setting('database_type', addon_id=addon_id)=='1':
		DB_NAME = get_setting('database_mysql_name', addon_id=addon_id)
		DB_USER = get_setting('database_mysql_user', addon_id=addon_id)
		DB_PASS = get_setting('database_mysql_pass', addon_id=addon_id)
		DB_PORT = get_setting('database_mysql_port', addon_id=addon_id)
		DB_ADDRESS = get_setting('database_mysql_host', addon_id=addon_id)
		DB_TYPE = 'mysql'
		from dudehere.routines.database import MySQLDatabase as DatabaseAPI
	
	else:
		DB_TYPE = 'sqlite'
		DB_FILE = xbmc.translatePath(get_setting('database_sqlite_file', addon_id=addon_id))
		from dudehere.routines.database import SQLiteDatabase as DatabaseAPI
	
	class MyDatabaseAPI(DatabaseAPI):
		def _initialize(self):
			pass
		
		def do_init(self):
			pass
	
	if DB_TYPE == 'mysql':
		DB = MyDatabaseAPI(DB_ADDRESS, DB_NAME, DB_USER, DB_PASS, DB_PORT, version=DB_VERSION, connect=True)
	else:
		DB = MyDatabaseAPI(DB_FILE, version=DB_VERSION, connect=True)
	return DB	

def parse_query(query, q={'mode': 'main'}):
	if query.startswith('?'): query = query[1:]
	queries = urlparse.parse_qs(query)
	for key in queries:
		if len(queries[key]) == 1:
			q[key] = queries[key][0]
		else:
			q[key] = queries[key]
	return q
try:
	args = parse_query(sys.argv[2])
except:
	args = {"mode": "main"}
mode = args['mode']

def arg(k, default=None):
	if k in args:
		v = args[k]
		if v == '': return default
		if v == 'None': return default
		return v
	else:
		return default
	
def get_arg(k, default=None):
	return arg(k, default)

def check_version(previous, current):
	if not re.search('\d+\.\d+\.\d+', str(previous)): return True
	p = previous.split('.')
	c = current.split('.')	
	# test major version
	if int(p[0]) < int(c[0]): return True
	# test minor version
	if int(p[1]) < int(c[1]): return True
	# test sub minor version
	if int(p[2]) < int(c[2]): return True
	return False

def get_current_url():
	return str(sys.argv[0]) + str(sys.argv[2])

def get_path():
	return addon.getAddonInfo('path').decode('utf-8')

def get_profile():
	return addon.getAddonInfo('profile').decode('utf-8')

def translate_path(path):
	return xbmc.translatePath(path).decode('utf-8')

def set_setting(id, value):
	if not isinstance(value, basestring): value = str(value)
	addon.setSetting(id, value)

def get_version():
	return addon.getAddonInfo('version')

def get_id():
	return addon.getAddonInfo('id')

def get_name():
	return addon.getAddonInfo('name')

def get_property(k):
	p = xbmcgui.Window(10000).getProperty('GenericPlaybackService.' + k)
	if p == 'false': return False
	if p == 'true': return True
	return p
	
def set_property(k, v):
	xbmcgui.Window(10000).setProperty('GenericPlaybackService.' + k, v)

def clear_property(k):
	xbmcgui.Window(10000).clearProperty('GenericPlaybackService.' + k)

	
def show_window(window_id):
	xbmcgui.Window(window_id).show()

def hide_window(window_id):
	xbmcgui.Window(window_id).close()

def window_exists(window_id):
	try:
		xbmcgui.Window(window_id)
		return True
	except:
		return False

def get_plugin_url(queries, addon_id=None):
	try:
		query = urllib.urlencode(queries)
	except UnicodeEncodeError:
		for k in queries:
			if isinstance(queries[k], unicode):
				queries[k] = queries[k].encode('utf-8')
		query = urllib.urlencode(queries)
	addon_id = sys.argv[0] if addon_id is None else addon_id
	return addon_id + '?' + query

def build_plugin_url(queries, addon_id=None):
	return get_plugin_url(queries, addon_id)

def execute_query(query):
	plugin_url = get_plugin_url(query)
	execute_url(plugin_url)

def execute_url(plugin_url):
	cmd = 'XBMC.RunPlugin(%s)' % (plugin_url)
	run_command(cmd)

def navigate_to(self, query):
	plugin_url = get_plugin_url(query)
	go_to_url(plugin_url)
	
def go_to_url(plugin_url):
	cmd = "XBMC.Container.Update(%s)" % plugin_url
	xbmc.executebuiltin(cmd)

def install_addon(addon_id):
	cmd = "RunPlugin(plugin://%s)" % addon_id
	response = run_command(cmd)
	log(response)

def run_command(cmd):
	return xbmc.executebuiltin(cmd)	

def play_url(plugin_url, isFolder=False):
	if 'Custom Dialog' in get_setting('source_selection_mode') or 'Redbeard' in get_setting('source_selection_mode'):
		cmd = 'XBMC.RunPlugin(%s)' % (plugin_url)
	elif isFolder:
		cmd = 'XBMC.PlayMedia(%s,True)' % (plugin_url)
	else:
		cmd = 'XBMC.PlayMedia(%s)' % (plugin_url)
	run_command(cmd)
	
class ProgressBar(xbmcgui.DialogProgress):
	def __init__(self, *args, **kwargs):
		xbmcgui.DialogProgress.__init__(self, *args, **kwargs)
		self._silent = False
		self._index = 0
		self._total = 0
		self._percent = 0
		
	def new(self, heading, total):
		if not self._silent:
			self._index = 0
			self._total = total
			self._percent = 0
			self._heading = heading
			self.create(heading)
			self.update(0, heading, '')
			
	def update_subheading(self, subheading, subheading2="", percent=False):
		if percent: self._percent = percent
		self.update(self._percent, self._heading, subheading, subheading2)
		
	def next(self, subheading, subheading2=""):
		if not self._silent:
			self._index = self._index + 1
			self._percent = self._index * 100 / self._total
			self.update(self._percent, self._heading, subheading, subheading2)
	
	def is_canceled(self):
		return self.iscanceled()
		
class TextBox:
	# constants
	WINDOW = 10147
	CONTROL_LABEL = 1
	CONTROL_TEXTBOX = 5

	def __init__( self, *args, **kwargs):
		# activate the text viewer window
		xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
		# get window
		self.window = xbmcgui.Window( self.WINDOW )
		# give window time to initialize
		xbmc.sleep( 500 )


	def setControls( self ):
		#get header, text
		heading, text = self.message
		# set heading
		self.window.getControl( self.CONTROL_LABEL ).setLabel( "%s - %s v%s" % ( heading, get_name(), get_version()) )
		# set text
		self.window.getControl( self.CONTROL_TEXTBOX ).setText( text )

	def show(self, heading, text):
		# set controls

		self.message = heading, text
		self.setControls()

class ContextMenu:
	def __init__(self):
		self.commands = []

	def add(self, text, arguments={}, script=False, visible=True, priority=50):
		if hasattr(visible, '__call__'):
			if visible() is False: return
		else:
			if visible is False: return
		if isinstance( text, ( int, long ) ):
			text = i18n(text)
		cmd = self._build_url(arguments, script)
		self.commands.append((text, cmd, '', priority))
	
	def _build_url(self, arguments, script):
		try:
			plugin_url =  "%s?%s" % (ADDON_URL, urllib.urlencode(arguments))
		except UnicodeEncodeError:
			for k in arguments:
				if isinstance(arguments[k], unicode):
					arguments[k] = arguments[k].encode('utf-8')
			plugin_url =  "%s?%s" % (ADDON_URL, urllib.urlencode(arguments))
			
		if script:
			cmd = 'XBMC.RunPlugin(%s)' % (plugin_url)
		else:
			cmd = "XBMC.Container.Update(%s)" % plugin_url
		return cmd

	def get(self):
		return sorted(self.commands, key=lambda k: k[3])

def _eod(cache_to_disc=True):
	xbmcplugin.endOfDirectory(HANDLE_ID, cacheToDisc=cache_to_disc)

def eod(view=None, content=None, viewid=None, clear_search=False):
	if VIEWS and view is None:
		view = VIEWS.DEFAULT
	elif view is None:
		view = VIEWS.DEFAULT
	if view=='custom':
		set_view('custom', content=content, viewid=viewid)
	else:
		set_view(view,content=content)
	if clear_search:
		clear_property('search.query')
		clear_property('search.query.refesh')
	_eod()

def get_view():
		view_name = xbmc.getInfoLabel('Container.Viewmode')
		xml = vfs.read_file(vfs.join('special://skin/', 'addon.xml'))
		try: src = re.search('defaultresolution="([^"]+)', xml, re.DOTALL).group(1)
		except: src = re.search('<res.+?folder="([^"]+)', xml, re.DOTALL).group(1)
		src = vfs.join('special://skin/', src + '/MyVideoNav.xml')
		xml = vfs.read_file(src)
		match = re.search('<views>([^<]+)', xml, re.DOTALL)
		if match:
			views = match.group(1)
			for view in views.split(','):
				if xbmc.getInfoLabel('Control.GetLabel(%s)' % (view)):
					return view_name, view
		return False,False
	
def set_view(view, content=None, viewid=None):
	if get_setting('enable_default_views') == 'true':
		if content:
			xbmcplugin.setContent(HANDLE_ID, content)
		if viewid == 0:
			pass
		elif not viewid:
			viewid = view
		xbmc.executebuiltin("Container.SetViewMode(%s)" % viewid)
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_LABEL )
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_DATE )
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
		xbmcplugin.addSortMethod( handle=HANDLE_ID, sortMethod=xbmcplugin.SORT_METHOD_GENRE )

def add_menu_item(query, infolabels, total_items=0, image='', fanart='', menu=None, replace_menu=None, visible=True):
	if hasattr(visible, '__call__'):
		if visible() is False: return
	else:
		if visible is False: return
	if isinstance( infolabels['title'], ( int, long ) ):
		infolabels['title'] = i18n(infolabels['title'])
	if replace_menu is None:
		replace_menu = replace_context_menu_by_default
	if menu is None:
		menu = ContextMenu()
	for m in default_context_menu_items:
		menu.add(*m)
	if not fanart:
		fanart = get_path() + '/fanart.jpg'
	listitem = xbmcgui.ListItem(infolabels['title'], iconImage=image, thumbnailImage=image)
	cast = infolabels.pop('cast', None)
	try:
		if cast is not None: listitem.setCast(cast)
	except: pass
	listitem.setInfo('video', infolabels)
	listitem.setProperty('IsPlayable', 'false')
	listitem.setProperty('fanart_image', fanart)
	if menu:
		listitem.addContextMenuItems(menu.get(), replaceItems=replace_menu)

	plugin_url = get_plugin_url(query)
	xbmcplugin.addDirectoryItem(HANDLE_ID, plugin_url, listitem, isFolder=True, totalItems=total_items) 
	
def add_video_item(query, infolabels, total_items=0, image='', fanart='', menu=None, replace_menu=None, set_resume=False):
		listitem = xbmcgui.ListItem(infolabels['title'], iconImage=image, thumbnailImage=image)
		cast = infolabels.pop('cast', None)
		try:
			if cast is not None: listitem.setCast(cast)
		except: pass
		listitem.setInfo("video", infolabels)		
		
		if 'Custom Dialog' not in get_setting('source_selection_mode') and 'Redbeard' not in get_setting('source_selection_mode'):
			listitem.setProperty('IsPlayable', 'true')
		listitem.setProperty('fanart_image', fanart)
		if set_resume:
			listitem.setProperty('totaltime', '999999')
			listitem.setProperty('resumetime', str(set_resume))
			listitem.setProperty('percentplayed', '10')
		else:
			listitem.setProperty('totaltime', '0')
			listitem.setProperty('resumetime', '0')
			listitem.setProperty('percentplayed', '0')

		if replace_menu is None:
			replace_menu = replace_context_menu_by_default
		if menu is None:
			menu = ContextMenu()
		for m in default_context_menu_items:
			menu.add(*m)	
		if menu:
			listitem.addContextMenuItems(menu.get(), replaceItems=replace_menu)
		query['rand'] = random.random()
		plugin_url = build_plugin_url(query)
		xbmcplugin.addDirectoryItem(HANDLE_ID, plugin_url, listitem, isFolder=False, totalItems=total_items)

def dialog_input(title):
	kb = xbmc.Keyboard('', title, False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		if text != '':
			return text
	return None	

def open_busy_dialog():
	xbmc.executebuiltin( "ActivateWindow(busydialog)" )

def close_busy_dialog():
	xbmc.executebuiltin( "Dialog.Close(busydialog)" )

def show_textbox(heading, content):
		TextBox().show(heading, content)
	
def dialog_file_browser(title, mask=''):
	dialog = xbmcgui.Dialog()
	path = dialog.browse(1, title, 'files', mask)
	return path
	
def dialog_number(title, default=''):
	dialog = xbmcgui.Dialog()
	r = dialog.numeric(0, title, default)
	return r

def dialog_textbox(heading, content):
	TextBox().show(heading, content)

def dialog_ok(title="", m1="", m2="", m3=""):
	dialog = xbmcgui.Dialog()
	dialog.ok(title, m1, m2, m3)

def dialog_confirm(title, m1='', m2='', m3='', yes='', no=''):
	dialog = xbmcgui.Dialog()
	return dialog.yesno(title, m1, m2, m3, no, yes)

def dialog_select(heading, options):
	dialog = xbmcgui.Dialog()
	index = dialog.select(heading, options)
	if index >= 0:
		return index
	else: 
		return False

def notify(title, message, timeout=1500, image=vfs.join(get_path(), 'icon.png')):
	cmd = "XBMC.Notification(%s, %s, %s, %s)" % (title, message, timeout, image)
	xbmc.executebuiltin(cmd)
	
def error_message(title, message, timeout=2500, image=vfs.join(get_path(), 'icon.png')):
	cmd = "XBMC.Notification(%s, %s, %s, %s)" % (title, message , timeout, image)
	xbmc.executebuiltin(cmd)	
	
def refresh(plugin_url=None):
	query = get_property('search.query')
	if query:
		set_property('search.query.refesh', query)
		clear_property('search.query')
		
	if plugin_url is None:
		xbmc.executebuiltin("Container.Refresh")
	else:
		xbmc.executebuiltin("Container.Refresh(%s)" % plugin_url)
		
def exit():
	exit = xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	return exit

def kodi_json_request(method, params):
	jsonrpc =  json.dumps({ "jsonrpc": "2.0", "method": method, "params": params, "id": 1 })
	response = json.loads(xbmc.executeJSONRPC(jsonrpc))
	return response

def get_episode_id(title, year, season, episode):
		year = int(year)
		filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
		filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, year)
		cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libTvShows"}'
		command = cmd % (filter_str.format(search_title=title))
		data = json.loads(xbmc.executeJSONRPC(command))
		if 'result' in data and 'tvshows' in data['result']:
			tvshowid = False
			for r in data['result']['tvshows']:
				if r['year'] != year or r['title'] != title: continue
				tvshowid = r['tvshowid']
				break
			if tvshowid is False:
				return False, False
			cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"tvshowid": %s, "season": %s, "filter": {"field": "%s", "operator": "is", "value": "%s"}, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "season", "episode", "file", "playcount"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true }}, "id": "libTvShows"}'
			command = cmd % (tvshowid, season, 'episode', episode)
			data = json.loads(xbmc.executeJSONRPC(command))
			if 'result' in data and 'episodes' in data['result']:
				for episode in data['result']['episodes']:
					if episode['file'].endswith('.strm'):
						return episode['episodeid'], episode['playcount']
		return False, False
	
def get_movie_id(title, year):
	filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
	filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, year)
	cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year", "file", "playcount"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}'
	command = cmd % (filter_str.format(search_title=title))
	data = json.loads(xbmc.executeJSONRPC(command))
	if 'result' in data and 'movies' in data['result']:
		for r in data['result']['movies']:
			if r['file'].endswith('.strm'): 
				return r['movieid'], r['playcount']
	return False, False

def set_watched(media, title, year, season='', episode=''):
	if media == 'episode':
		episodeid, playcount = get_episode_id(title, year, season, episode)
		if episodeid:
			playcount += 1
			cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid": %s, "playcount": %s}, "id": "libTvShows"}' % (episodeid, playcount)
			response = json.loads(xbmc.executeJSONRPC(cmd))
			log(response)
	else:
		movieid, playcount = get_movie_id(title, year)
		if movieid:
			playcount += 1
			cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "playcount": %s}, "id": "libMovies"}' % (movieid, playcount)
			response = json.loads(xbmc.executeJSONRPC(cmd))
			log(response)

def set_attempt_status(status):
	_DB = get_main_DB()
	attempt_id = get_property("attempt.id")
	log("Successful attempt: %s" % attempt_id)
	SQL = "UPDATE host_stats SET %s=1 WHERE id=?" % status
	_DB.execute(SQL, [attempt_id])
	_DB.commit()
	_DB.disconnect()
	del _DB
	
def get_fileid(self, path=None):
	prams = {"file": "path"}
	response = kodi_json_request('Files.GetFileDetails', params)
	log(response)

def set_resume_point(hash_id):
	DB.connect(True)
	current_time = get_property('current_time')
	total_time = get_property('total_time')
	SQL = "REPLACE INTO playback_states(hash_id, current, total) VALUES(?,?,?)"
	DB.execute(SQL, [hash_id,current_time, total_time])
	DB.commit()
	DB.disconnect()

def get_resume_point(hash_id):
	DB.connect()
	resume = DB.query("SELECT current FROM playback_states WHERE hash_id=?", [hash_id])
	DB.disconnect()
	resume_point = False
	if resume:
		seconds = float(resume[0])
		if seconds < 60:
			return resume_point
		ok = dialog_confirm("Resume Playback?", "Resume playback from %s" % format_time(seconds), yes='Start from beginning', no='Resume') == 0
		if ok:
			resume_point = int(seconds)
	return resume_point

def has_resume_point(hash_id):
	DB.connect(True)
	resume = DB.query("SELECT current FROM playback_states WHERE hash_id=?", [hash_id])
	DB.disconnect()
	if resume:
		seconds = float(resume[0])
		if seconds > 60:
			return True
	return False
	
def format_time(seconds):
	seconds = int(seconds)
	minutes, seconds = divmod(seconds, 60)
	if minutes > 60:
		hours, minutes = divmod(minutes, 60)
		return "%02d:%02d:%02d" % (hours, minutes, seconds)
	else:
		return "%02d:%02d" % (minutes, seconds)
	
def get_hash_id(imdb_id='', season='', episode=''):
	import hashlib
	imdb_id = '' if imdb_id is None else str(imdb_id)
	hash_str = imdb_id+str(season)+str(episode)
	return hashlib.md5(hash_str).hexdigest()

def clear_resume_point(hash_id):
	DB.connect()
	DB.execute("DELETE FROM playback_states WHERE hash_id=?", [hash_id])
	DB.commit()
	DB.disconnect()

def is_playlist(plugin_url=ADDON_URL):
	media_type = get_arg('media_type', '')
	if media_type == 'stream':
		return True
	return False

def play_stream(url,  metadata={"cover_url": "", "title": ""}, title=None):
	if title is None: title = metadata['title']
	listitem = xbmcgui.ListItem(title, iconImage=metadata['cover_url'], thumbnailImage=metadata['cover_url'], path=url)
	listitem.setPath(url)
	listitem.setInfo("video", metadata)
	set_property('playing', "true")
	resume_point = False
	if get_setting('enable_resume') == 'true':
		if 'season' in metadata:
			hash_id = get_hash_id(metadata['imdb_id'], metadata['season'], metadata['episode'])
		else:
			hash_id = get_hash_id(metadata['imdb_id'], metadata['slug'])
		resume_point = get_resume_point(hash_id)
		if resume_point:
			listitem.setProperty('totaltime', '999999')
			listitem.setProperty('resumetime', str(resume_point))
	
	if  is_playlist() is False and ('Custom Dialog' in get_setting('source_selection_mode') or 'Redbeard' in get_setting('source_selection_mode')):
		if resume_point:
			set_property("playback.resume", str(resume_point))
		xbmc.Player().play(url, listitem)

	else:
		if is_playlist():
			if HANDLE_ID > -1:
				xbmcplugin.endOfDirectory(HANDLE_ID, True, False, False)
			xbmcplugin.setResolvedUrl(HANDLE_ID, True, listitem)
		else:
			listitem.setProperty('IsPlayable', 'true')
			xbmcplugin.setResolvedUrl(HANDLE_ID, True, listitem)
		while True:
			if xbmc.getCondVisibility('Window.IsActive(progressdialog)'):
				xbmc.executebuiltin('Dialog.close(progressdialog, True)')
				break
			sleep(50)	
	

	while get_property('playing'):
		sleep(100)
	__on_stream_stop()

def __on_stream_stop():
	on_playback_stop()
	
def get_property(k):
	p = xbmcgui.Window(10000).getProperty('GenericPlaybackService.' + k)
	if p == 'false': return False
	if p == 'true': return True
	return p

def set_property(k, v):
	xbmcgui.Window(10000).setProperty('GenericPlaybackService.' + str(k), str(v))

def clear_property(k):
	xbmcgui.Window(10000).clearProperty('GenericPlaybackService.' + k)
	
def show_window(window_id):
	xbmcgui.Window(window_id).show()

def hide_window(window_id):
	xbmcgui.Window(window_id).close()

def window_exists(window_id):
	try:
		xbmcgui.Window(window_id)
		return True
	except:
		return False
	
def get_stream_stop_times():
	percent = get_property('percent') if get_property('percent') else 0
	current_time = get_property('current_time')
	total_time = get_property('total_time')
	return {"percent": int(percent), "current": current_time, "total": total_time}

def on_playback_stop():
	'''*
	Overide this function with whatever you want to happen once playback has finished
	*'''
	pass


def initialize_settings(upgrade=False):
	from xml.etree import ElementTree as ET
	if not vfs.exists(DATA_PATH): vfs.mkdir(DATA_PATH)
	xml_in = vfs.join(ROOT_PATH, 'resources/settings.xml')
	xml_out = vfs.join(DATA_PATH, 'settings.xml')
	soup_in = vfs.read_file(xml_in, soup=True)
	document = ET.Element("settings")
	settings = soup_in.findAll('setting')
	for setting in settings:
		try:
			id = setting['id']
			if upgrade and get_setting(id):
				default = get_setting(id)
			else:
				default = setting['default']
			node = ET.SubElement(document, 'setting', id=id, default=default)
		except:
			pass
	et = ET.ElementTree(document)
	et.write(xml_out)

def first_run():
	pass
	
def update_run():
	pass

def register(mode, target, kargs=None):
	if isinstance(mode, list):
		for foo in mode:
			__dispatcher[foo] = target
			__kargs[foo] = kargs
	else:
		__dispatcher[mode] = target
		__kargs[mode] = kargs

def run():

	if get_setting('setup_run') != 'true':
	#	log("First Run")
		first_run()
	elif check_version(get_setting('version'), get_version()):
		#log("Update Run")
		update_run()	
		
	if __kargs[args['mode']] is None:
		__dispatcher[args['mode']]()

	else:
		__dispatcher[args['mode']](*__kargs[args['mode']])
	log("Executing with args: %s" % args)
