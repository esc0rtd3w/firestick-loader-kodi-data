# -*- coding: utf-8 -*-


#      Copyright (C) 2017 Mucky Duck
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ast,operator,os,re,shutil,sys,string,time,urllib,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

from metahandler import metahandlers
from md_view import setView
from common import Addon

metaget = metahandlers.MetaData()
dialog = xbmcgui.Dialog()







class md:




	def __init__(self, addon_id, argv=None):
		

		if argv is not None:
			self.addon = Addon(addon_id, sys.argv)
		else:
			self.addon = Addon(addon_id)
		self.addon_name = '[COLOR white][B]%s[/B][/COLOR]' %self.addon.get_name()
		self.addon_id = self.addon.get_id()
		self.icon = self.addon.get_icon()
		
		try:
			if argv[0]:
				self.url = sys.argv[0]
				self.handle = int(sys.argv[1])
				self.args = self.parse_query(sys.argv[2][1:])
		except:pass




	def get_art(self):
		'''Returns the full path to the addon's art directory.
		must be a folder named art in resources within the addon
		 ``resources/art'''
		return os.path.join(self.addon.get_path(), 'resources', 'art', '')




	def get_media(self):
		'''Returns the full path to the addon's media directory.
		must be a folder named media in resources within the addon
		 ``resources/media'''
		return os.path.join(self.addon.get_path(), 'resources', 'media', '')




	def regex_from_to(self, text, from_string, to_string, excluding=True):
		if excluding:
			try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
			except: r = ''
		else:
			try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
			except: r = ''
		return r




	def regex_get_all(self, text, start_with, end_with, excluding=False):
		if excluding:
			r = re.findall("(?i)" + start_with + "([\S\s]+?)" + end_with, text)
		else:
			r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
		return r




	def PT(self, url):
		self.addon.log('Play Trailer %s' % url)
		notification('fetching trailer', self.icon)
		xbmc.executebuiltin("PlayMedia(%s)"%url)




	def dialog_yesno(self,message,yes,no):
		return dialog.yesno(self.addon_name, message, yeslabel=yes, nolabel=no)




	def dialog_select(self,header,choice):
		return dialog.select(header,choice)




	def sort_choice(self,data,name,value_name,value):

		if len(data) > 1:
			ret = self.dialog_select(name,value_name)
			if ret == -1:
				return
			elif ret > -1:
				choice = value[ret]
		else:
			choice = value[0]

		return choice




	def numeric_select(self,header,default_no):
		dialog = xbmcgui.Dialog()
		return dialog.numeric(0, header, default_no)




	def text_return(self,header):
		keyb = xbmc.Keyboard('', header)
		keyb.doModal()
		if (keyb.isConfirmed()):
			data = keyb.getText()
		return data




	def notification(self, message, icon):
		self.addon.show_small_popup(self.addon_name, message, 5000, icon)
		return




	def Exit(self):
		xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
		xbmc.executebuiltin("XBMC.ActivateWindow(Home)")




	'''def notification(self, title, message, icon):
		self.addon.show_small_popup(self.addon.get_name(), message.title(), 5000, icon)
		return'''




	def addon_search(self,content,query, fan_art='', infolabels='', item_type='video'):

		'''this function is still under construction and is for use by mucky ducks addons i dont mind
		people modifiying the code for yourself but please make sure you link it to your own addons
		if i find people using it in their addons to link to my addons i will send out code that removes it''' 

		query = query.partition('(')[0]

		if fan_art:
			fan_art = ast.literal_eval(fan_art)
		else:
			fanart = {}
		if infolabels:
			infolabels = ast.literal_eval(infolabels)
		else:
			infolabels = {}

		if content == 'movies':
			match = ['imperialstreams','123movies','m4u','pubfilm','cmovieshd','yesmovies','niter','movievault','hdbox','afdah','watch32hd']
		else:
			match = ['imperialstreams','123movies','m4u','pubfilm','cmovieshd','yesmovies','ws','luckytv']

		
		for addon_title in match:

			name = addon_title
			if name == 'ws':
				name = 'watchseries'

			if addon_title not in self.addon_id:
				title = '[COLOR white][COLOR red]Search[/COLOR] %s [COLOR red]For[/COLOR] %s[/COLOR]' %(name,query)
				listitem = xbmcgui.ListItem(title)
				listitem.setInfo(item_type, infoLabels=infolabels)
				listitem.setArt(fan_art)
				url = 'plugin://plugin.video.md%s/?url=url&content=%s&mode=search&query=%s' %(addon_title,content,query)
				xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(url, listitem, True,)])

		if content == 'movies':
			setView(self.addon_id, 'movies', 'movie-view')
		elif content == 'tvshows' or content == 'seasons' or content == 'episodes':
			setView(self.addon_id, 'tvshows', 'show-view')

		self.addon.end_of_directory()
		




	def search(self, space='+'):
		keyb = xbmc.Keyboard('', 'Search')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText().replace(' ',space)
		return search




	def replace_space(self, data, space=''):
		return re.sub(r'[\s+]', space, data)




	def space_before_cap(self, data):
		return re.sub(r'(\w)([A-Z])', r'\1 \2', data)




	def remove_punctuation(self, text):
		return str(text).translate(None, string.punctuation)




	def get_max_value_index(self, my_list):
		return max(enumerate(my_list), key=operator.itemgetter(1))




	def remove_from_file(self,name,path,dummy):
		with open(path,'r') as oldfile:
			with open(dummy, 'w') as newfile:
				for line in oldfile:
					if name not in line:
						newfile.write(line)
		os.remove(path)
		os.rename(dummy,path)
		if os.stat(path).st_size == 0:
			os.remove(path)
		try:
			if os.stat(dummy).st_size == 0:
				os.remove(dummy)
		except:
			pass
		return




	def append_file(self,path,data):
		with open(path, 'a') as f:
			f.write('%s\n' %data)
		return




	def get_fav_folder(self):
		path = os.path.join(self.addon.get_profile(), 'favs', '')
		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		return path




	def get_fav_path(self,content):
		self.get_fav_folder()
		filename = os.path.join(self.addon.get_profile(), 'favs', '%s.txt' %content)
		if not os.path.exists(filename):
			with open(filename, 'w'):
				pass

		return filename




	def fetch_favs(self,baseurl=''):

		path = self.get_fav_folder()
		from os.path import isfile, join
		onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
		dialog = xbmcgui.Dialog()

		fav_menu = []
		fav_path = []
		
		if not len(onlyfiles):
			self.notification('You have no favourites.', self.icon)
		else:
			for content in onlyfiles:
				if 'dummy' not in content:
					content = content.replace('.txt','')

					fav = '[B][I][COLOR gold]%s[/COLOR][/I][/B]' %content.upper()
					fav_menu.append(fav)
					fav_path.append(self.get_fav_path(content))
					
			path_to_favs = self.sort_choice(onlyfiles,'Select Section',fav_menu,fav_path)

			with open(path_to_favs, 'r') as f:

				data = f.readlines()
				items = len(data)

				for a in data:

					b = ast.literal_eval(a)

					if 'url' in b:
						url = b['url']
					else:
						url = 'url'
					if 'fan_art' in b:
						fanart = ast.literal_eval(b['fan_art'])
					else:
						fanart = {}
					if 'infolabels' in b:
						infolabels = ast.literal_eval(b['infolabels'])
					else:
						infolabels = {}
					if 'is_folder' in b:
						is_folder = ast.literal_eval(b['is_folder'])
					else:
						is_folder = True

					if baseurl and baseurl not in url and not url == 'url':
						change = url.split('//')[1].partition('/')[2]
						url = '%s/%s' %(baseurl,change)

					if 'contextmenu_items' not in b:
						contextmenu_items = []

					contextmenu_items.append(('[COLOR gold][B]Plot Information[/B][/COLOR]', 'XBMC.Action(Info)'))
					self.addDir(b, infolabels=infolabels, fan_art=fanart, is_folder=is_folder,
						    contextmenu_items=contextmenu_items, item_count=items)
			if content == 'movies':
				setView(self.addon_id, 'movies', 'movie-view')
			elif content == 'tvshows':
				setView(self.addon_id, 'tvshows', 'show-view')
			elif content == 'seasons':
				setView(self.addon_id, 'files', 'sea-view')
			elif content == 'episodes':
				setView(self.addon_id,'episodes', 'epi-view')
			else:
				setView(self.addon_id, 'files', 'menu-view')

			self.addon.end_of_directory()




	def add_remove_fav(self, name, url, infolabel, fan_art,
			   content, mode_id, is_folder):
		
		if content == '' or content == None:
			content = 'others'

		data = self.parse_query('mode=%s' %mode_id)
		dummy = self.get_fav_path('dummy')
		path = self.get_fav_path(content)
		
		if name in open(path).read():
			self.remove_from_file(name,path,dummy)
			self.notification('%s Removed from favourites.' %name, self.icon)
		else:
			self.append_file(path,data)
			self.notification('%s Added to favourites.' %name, self.icon)
			
		xbmc.executebuiltin('Container.Refresh')




	def add2fav(self, name, url, infolabel, fan_art,
		    content, mode_id, is_folder):

		if content == '' or content == None:
			content = 'others'

		data = self.parse_query('mode=%s' %mode_id)        
		path = self.get_fav_path(content)
		
		if name in open(path).read():
			self.notification('%s Already in favourites.' %name, self.icon)
		else:
			self.append_file(path,data)
			self.notification('%s Added to favourites.' %name, self.icon)

		xbmc.executebuiltin('Container.Refresh')




	def remove_fav(self, name, content):

		if content == '' or content == None:
			content = 'others'

		path = self.get_fav_path(content)
		dummy = self.get_fav_path('dummy')
		
		if name not in open(path).read():
			self.notification('%s not in favourites.' %name, self.icon)
		else:
			self.remove_from_file(name,path,dummy)
			self.notification('%s Removed from favourites.' %name, self.icon)

		xbmc.executebuiltin('Container.Refresh')




	def User_Agent(self):
		return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'




	def parse_query(self, query, defaults={'mode': None}):
		'''
		Parse a query string as used in a URL or passed to your addon by XBMC.
		
		Example:
		 
		>>> addon.parse_query('name=test&type=basic')
		{'mode': 'main', 'name': 'test', 'type': 'basic'} 
		    
		Args:
		    query (str): A query string.
		    
		Kwargs:
		    defaults (dict): A dictionary containing key/value pairs parsed 
		    from the query string. If a key is repeated in the query string
		    its value will be a list containing all of that keys values.  
		'''
		queries = urlparse.parse_qs(query)
		q = defaults
		for key, value in queries.items():
			if len(value) == 1:
				q[key] = value[0]
			else:
				q[key] = value
		return q



		'''

			dictionary for setting art
		values : dictionary - pairs of { label: value }.
		
		- Some default art values (any string possible):
		- thumb : string - image filename
		- poster : string - image filename
		- banner : string - image filename
		- fanart : string - image filename
		- clearart : string - image filename
		- clearlogo : string - image filename
		- landscape : string - image filename
		example:
			- self.list.getSelectedItem().setArt({ 'poster': 'poster.png', 'banner' : 'banner.png' })
		

			{'thumb':'', 'poster':'', 'banner':'', 'fanart':'',
			'clearart':'', 'clearlogo':'', 'landscape':'', 'icon':''}

		'''

	

		'''

			infolabels dictionary
		- General Values that apply to all types:
		- count : integer (12) - can be used to store an id for later, or for sorting purposes
		- size : long (1024) - size in bytes
		- date : string (d.m.Y / 01.01.2009) - file date
	 
		    - Video Values:
		- genre : string (Comedy)
		- year : integer (2009)
		- episode : integer (4)
		- season : integer (1)
		- top250 : integer (192)
		- tracknumber : integer (3)
		- rating : float (6.4) - range is 0..10
		- watched : depreciated - use playcount instead
		- playcount : integer (2) - number of times this item has been played
		- overlay : integer (2) - range is 0..8. See GUIListItem.h for values
		- cast : list (Michal C. Hall)
		- castandrole : list (Michael C. Hall|Dexter)
		- director : string (Dagur Kari)
		- mpaa : string (PG-13)
		- plot : string (Long Description)
		- plotoutline : string (Short Description)
		- title : string (Big Fan)
		- originaltitle : string (Big Fan)
		- sorttitle : string (Big Fan)
		- duration : string (3:18)
		- studio : string (Warner Bros.)
		- tagline : string (An awesome movie) - short description of movie
		- writer : string (Robert D. Siegel)
		- tvshowtitle : string (Heroes)
		- premiered : string (2005-03-04)
		- status : string (Continuing) - status of a TVshow
		- code : string (tt0110293) - IMDb code
		- aired : string (2008-12-07)
		- credits : string (Andy Kaufman) - writing credits
		- lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
		- album : string (The Joshua Tree)
		- artist : list (['U2'])
		- votes : string (12345 votes)
		- trailer : string (/home/user/trailer.avi)
		- dateadded : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
	 
		    - Music Values:
		- tracknumber : integer (8)
		- duration : integer (245) - duration in seconds
		- year : integer (1998)
		- genre : string (Rock)
		- album : string (Pulse)
		- artist : string (Muse)
		- title : string (American Pie)
		- rating : string (3) - single character between 0 and 5
		- lyrics : string (On a dark desert highway...)
		- playcount : integer (2) - number of times this item has been played
		- lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
	 
		    - Picture Values:
		- title : string (In the last summer-1)
		- picturepath : string (/home/username/pictures/img001.jpg)
		- exif : string (See CPictureInfoTag::TranslateString in PictureInfoTag.cpp for valid strings)
	 
	 
	 
		*example:
	 
		- self.list.getSelectedItem().setInfo('video', { 'Genre': 'Comedy' })n

		
			{'genre':'', 'year':'', 'episode':'', 'season':'', 'top250':'',
			'tracknumber':'', 'rating':'', 'watched':'',
			'playcount':'', 'overlay':'', 'cast':[], 'castandrole':[],
			'director':'', 'mpaa':'', 'plot':'', 'plotoutline':'',
			'title':'', 'originaltitle':'', 'sorttitle':'',
			'duration':'', 'studio':'', 'tagline':'', 'writer':'',
			'tvshowtitle':'', 'premiered':'', 'status':'', 'code':'',
			'credits':'', 'lastplayed':'', 'album':'', 'artist':[],
			'votes':'', 'trailer':'', 'dateadded':''}

		'''




	def fetch_meta(self, content, infolabels, fan_art={}):

		meta = {}

		if 'year' in infolabels:
			year = infolabels['year']
		else:
			year = ''
		if 'code' in infolabels:
			code = infolabels['code']
		else:
			code = ''
		if 'season' in infolabels:
			season = infolabels['season']
		else:
			season = ''
		if 'episode' in infolabels:
			episode = infolabels['episode']
		else:
			episode = ''

		season = re.sub('\D', '', season)
		episode = re.sub('\D', '', episode)

		if season.startswith('0'):
			season = season[1:].strip()

		if episode.startswith('0'):
			episode = episode[1:].strip()

		splitName = infolabels['sorttitle'].partition('(')
		simplename = ''
		simpleyear = ''

		if len(splitName)>0:
			simplename=splitName[0]
			simpleyear=splitName[2].partition(')')
		else:
			simplename = infolabels['sorttitle']

		if len(simpleyear)>0:
			simpleyear=simpleyear[0]

		if simpleyear == '':
			simpleyear = year

		simpleyear = re.sub('\D', '', simpleyear)
			
		if content == 'movies':

			if self.addon.get_setting('movie_meta') == 'true':
				meta = metaget.get_meta('movie', simplename, year=simpleyear, imdb_id=code)
			else:
				pass

		elif content == 'tvshows':

			if self.addon.get_setting('tv_show_meta') == 'true':
				meta = metaget.get_meta('tvshow',simplename, year=simpleyear, imdb_id=code)
			else:
				pass

		elif content == 'episodes':

			if self.addon.get_setting('episode_meta') == 'true':
				try:
					meta = metaget.get_episode_meta(simplename,code,season,episode)
				except:
					meta = metaget.get_meta('tvshow',simplename, year=simpleyear, imdb_id=code)
			else:
				pass

		if not meta['cover_url']:
			meta['cover_url'] = fan_art['icon']

		if not meta['backdrop_url']:
			meta['backdrop_url'] = fan_art['fanart']

		if meta['backdrop_url'] == 'http://thetvdb.com/banners/fanart/original/76703-10.jpg':
			meta['backdrop_url'] = fan_art['fanart']

		return meta




	def addDir(self, queries, infolabels={}, fan_art={}, properties=None, contextmenu_items='',
		   context_replace=False, playlist=False, item_type='video', stream_info='',
		   is_folder=True, is_playable=True, item_count=0, add_fav=True, add_search=True):

		infolabels = self.addon.unescape_dict(infolabels)
		name = queries['name'].replace('()','')

		sort_info = infolabels

		if 'content' in queries:
			content = queries['content']
		else:
			content = ''

		if 'icon' not in fan_art:
			fan_art['icon'] = self.icon

		if 'fanart' not in fan_art:
			fan_art['fanart'] = self.addon.get_fanart()

		try:
			metaset = self.addon.get_setting('enable_meta')
		

			if metaset == 'true':

				if 'sorttitle' not in infolabels:
					pass

				else:
					infolabels = self.fetch_meta(content, infolabels, fan_art)
					infolabels['sorttitle'] = sort_info['sorttitle']
					if not contextmenu_items:
						contextmenu_items = []
					contextmenu_items.append(('[COLOR gold][B]Plot Information[/B][/COLOR]', 'XBMC.Action(Info)'))
					infolabels['title'] = name
					fan_art['fanart'] = infolabels['backdrop_url']
					fan_art['poster'] = infolabels['cover_url']
					fan_art['icon'] = infolabels['cover_url']
					if infolabels['banner_url']:
						fan_art['banner'] = infolabels['banner_url']
					else:
						fan_art['banner'] = infolabels['cover_url']

					if infolabels['thumb_url']:
						fan_art['thumb'] = infolabels['thumb_url']
					else:
						fan_art['thumb'] = infolabels['cover_url']


					#if infolabels['trailer_url'] == '':
						#del infolabels['trailer_url']
					
			else:
				pass
		except:
			pass

		

		queries['infolabels'] = infolabels
		queries['fan_art'] = fan_art
		s_args = self.addon.build_plugin_url(queries)
		listitem=xbmcgui.ListItem(name, iconImage=fan_art['icon'], thumbnailImage=fan_art['icon']) #listItem iconimage and thumbnail no longer needed after kodi 15. setArt does it for you.
		listitem.setInfo(item_type, infoLabels=infolabels)
		listitem.setArt(fan_art)

		if not is_folder:
			if is_playable and item_type=='video':
				listitem.setProperty('IsPlayable','true')
				listitem.addStreamInfo(item_type, stream_info)

		if properties:
			for prop in properties.items():
				listitem.setProperty(prop[0], prop[1])

		if not contextmenu_items:
			contextmenu_items = []


		if 'sorttitle' in infolabels:
			contextmenu_items.append(('[B][COLOR gold]Duck Hunt[/COLOR][/B]', 'Container.Update(%s, True)' %
						  self.addon.build_plugin_url({'mode': 'addon_search', 'url':'url', 'content':content,
									       'query':sort_info['sorttitle'], 'fan_art':fan_art,
									       'infolabels':infolabels, 'item_type':item_type})))

		if add_search:
			contextmenu_items.append(('[B][COLOR gold]Search[/COLOR][/B]', 'Container.Update(%s, True)' %
						  self.addon.build_plugin_url({'mode': 'search', 'url':'url', 'content':content})))

		if add_fav:
			try:
				baseurl = self.addon.get_setting('base_url')
			except:
				baseurl = ''

			contextmenu_items.append(('[B][COLOR gold]My Favourites[/COLOR][/B]', 'Container.Update(%s, True)' %
						  self.addon.build_plugin_url({'mode': 'fetch_favs', 'url':baseurl, 'baseurl':baseurl})))
			fq = queries
			fq['mode_id'] = queries['mode']
			fq['mode'] = 'add_remove_fav'
			fq['is_folder'] = is_folder
			
			contextmenu_items.append(('[COLOR gold][B]Add/Remove Favourite[/B][/COLOR]', 'XBMC.RunPlugin(%s)'%
						  self.addon.build_plugin_url(fq)))
		if contextmenu_items:
			listitem.addContextMenuItems(contextmenu_items, replaceItems=context_replace)

		if playlist is not False:
			self.addon.log_debug('adding item: %s - %s to playlist' % (name, s_args))
			ok=playlist.add(s_args, listitem)

		else:
			self.addon.log_debug('adding item: %s - %s' % (name, s_args))
			ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=s_args,listitem=listitem,isFolder=is_folder,totalItems=int(item_count))
		return ok




	def resolved(self, url, name='', fan_art='', infolabels='', item_type='video'):
		listitem = xbmcgui.ListItem(name)
		listitem.setInfo(item_type, infoLabels=infolabels)
		listitem.setArt(fan_art)
		listitem.setProperty('IsPlayable','true')
		listitem.setPath(str(url))
		ok = xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		return ok




	def check_source(self):
		if os.path.exists(xbmc.translatePath('special://home/userdata/sources.xml')):
			with open(xbmc.translatePath('special://home/userdata/sources.xml'), 'r+') as f:
				my_file = f.read()
				if re.search(r'http://muckys.mediaportal4kodi.ml', my_file):
					self.addon.log('Muckys Source Found in sources.xml, Not Deleting.')
				else:
					line1 = "you have Installed The MDrepo From An"
					line2 = "Unofficial Source And Will Now Delete Please"
					line3 = "Install From [COLOR red]http://muckys.mediaportal4kodi.ml[/COLOR]"
					line4 = "Removed Repo And Addon"
					line5 = "successfully"
					self.addon.show_ok_dialog([line1, line2, line3], self.addon_name)
					delete_addon = self.addon.get_path()
					delete_repo = xbmc.translatePath('special://home/addons/repository.mdrepo')
					shutil.rmtree(delete_addon, ignore_errors=True)
					shutil.rmtree(delete_repo, ignore_errors=True)
					self.addon.log('===DELETING===ADDON===+===REPO===')
					self.addon.show_ok_dialog([line4, line5], self.addon_name)
	
		
