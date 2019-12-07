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


import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
import os,re,shutil,sys,urllib,urlparse

from metahandler import metahandlers
from common import Addon

metaget = metahandlers.MetaData()


class md:



	def __init__(self, addon_id, argv=None):

		self.addon = Addon(addon_id, sys.argv)
		if argv[0]:
			self.url = sys.argv[0]
			self.handle = int(sys.argv[1])
			self.args = self.parse_query(sys.argv[2][1:])




	def get_art(self):
		'''Returns the full path to the addon's art directory.
		must be a folder named art in resources within the addon
		 ``resources/art'''
		return os.path.join(self.addon.get_path(), 'resources', 'art', '')




	def get_media(self):
		'''Returns the full path to the addon's media directory.
		must be a folder named media in resources within the addon
		 ``resources/art'''
		return os.path.join(self.addon.get_path(), 'resources', 'media', '')




	def regex_from_to(self, text, from_string, to_string, excluding=True):
		if excluding:
			try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
			except: r = ''
		else:
			try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
			except: r = ''
		return r




	def regex_get_all(self, text, start_with, end_with):
		r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
		return r




	def PT(self, url):
		#currently not workng
		self.addon.log('Play Trailer %s' % url)
		notification(self.addon.get_name(), 'fetching trailer', self.addon.get_icon())
		xbmc.executebuiltin("PlayMedia(%s)"%url)




	def notification(self, title, message, icon):
		self.addon.show_small_popup(self.addon.get_name(), message.title(), 5000, self.addon.get_icon)
		return




	def add_fav(self, name, url, iconimage='', fanart=''):

	    favs = self.addon.get_setting('favs').split(",")

	    if title in favs:
		    addon.show_small_popup("[COLOR white][B]%s[/B][/COLOR]" %addon_name, "%s already in favorites." %title, image=img)
	    else:
		    favs.append(title)
		    selfAddon.setSetting('favs', ",".join(favs))
		    addon.show_small_popup("[COLOR white][B]%s[/B][/COLOR]" %addon_name, "%s added to favorites." %title, image=img)
	    xbmc.executebuiltin('Container.Refresh')




	def remove_fav(self, name, url, iconimage='', fanart=''):
	    favs = selfAddon.getSetting('favs').split(",")
	    if title not in favs:
		    addon.show_small_popup("[COLOR white][B]%s[/B][/COLOR]" %addon_name, "%s not in favorites." %title, image=img)
	    else:
		    favs.remove(title)
		    selfAddon.setSetting('favs', ",".join(favs))
		    addon.show_small_popup("[COLOR white][B]%s[/B][/COLOR]" %addon_name, "%s removed from favorites." %title, image=img)
	    xbmc.executebuiltin('Container.Refresh')




	def User_Agent(self):
		return 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'




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

			meta = metaget.get_meta('movie', simplename, year=simpleyear, imdb_id=code)

		elif content == 'tvshows':

                        meta = metaget.get_meta('tvshow',simplename, year=simpleyear, imdb_id=code)

                elif content == 'seasons':

			if season:
				
				meta.get_seasons(simplename,code,season)

			else:
				meta = metaget.get_meta('tvshow',simplename, year=simpleyear, imdb_id=code)

		elif content == 'episodes':

			if episode:

				meta = metaget.get_episode_meta(simplename,code,int(season),int(episode))

			else:
				meta = metaget.get_meta('tvshow',simplename, year=simpleyear, imdb_id=code)

		if not meta['cover_url']:
			meta['cover_url'] = fan_art['icon']

		if not meta['backdrop_url']:
			meta['backdrop_url'] = fan_art['fanart']

		return meta




	def addDir(self, queries, infolabels={}, fan_art={}, properties=None, contextmenu_items='',
                   context_replace=False, playlist=False, item_type='video', stream_info='',
                   is_folder=True, is_playable=True, item_count=0):

                play = self.addon.build_plugin_url(queries)
                infolabels = self.addon.unescape_dict(infolabels)
		name = queries['name'].replace('()','')

		if 'content' in queries:
                        content = queries['content']

                if 'icon' not in fan_art:
			fan_art['icon'] = self.addon.get_icon()

		if 'fanart' not in fan_art:
			fan_art['fanart'] = self.addon.get_fanart()

                try:
			metaset = self.addon.get_setting('enable_meta')
		

			if metaset == 'true':

				if 'sorttitle' not in infolabels:
					pass

				else:
					infolabels = self.fetch_meta(content, infolabels, fan_art)
					if not contextmenu_items:
						contextmenu_items = []
						contextmenu_items.append(('[COLOR gold]Plot Information[/COLOR]', 'XBMC.Action(Info)'))

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
						fanart['thumb'] = infolabels['cover_url']
					
			else:
				pass
		except:
			pass

		listitem=xbmcgui.ListItem(name, iconImage=fan_art['icon'], thumbnailImage=fan_art['icon']) #listItem iconimage and thumbnail no longer needed after kodi 15. setArt does it for you.
		listitem.setInfo(item_type, infoLabels=infolabels)
		listitem.setArt(fan_art)

		if not is_folder:
                        if is_playable and item_type=='video':
                                listitem.setProperty("IsPlayable","true")
                                listitem.addStreamInfo(item_type, stream_info)

                if properties:
			for prop in properties.items():
				listitem.setProperty(prop[0], prop[1])

		if contextmenu_items:
			listitem.addContextMenuItems(contextmenu_items, replaceItems=context_replace)

		if playlist is not False:
			self.addon.log_debug('adding item: %s - %s to playlist' % \
				       (name, play))
			playlist.add(play, listitem)
		else:
			self.addon.log_debug('adding item: %s - %s' % (name, play))
			xbmcplugin.addDirectoryItem(self.handle, play, listitem,
						    isFolder=is_folder, totalItems=item_count)




	def check_source(self):
		if xbmcvfs.exists(xbmc.translatePath('special://home/userdata/sources.xml')):
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
					self.addon.show_ok_dialog(addon_name, line1, line2, line3)
					delete_addon = self.addon.get_path()
					delete_repo = xbmc.translatePath('special://home/addons/repository.mdrepo')
					shutil.rmtree(delete_addon, ignore_errors=True)
					shutil.rmtree(delete_repo, ignore_errors=True)
					self.addon.log('===DELETING===ADDON===+===REPO===')
					self.addon.show_ok_dialog(self.addon.get_name(), line4, line5)
