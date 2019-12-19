import re, urllib
import xbmc, xbmcgui, xbmcaddon
from resources.lib import Utils

class WindowManager(object):

	window_stack = []

	def __init__(self):
		self.reopen_window = False
		self.last_control = None
		self.active_dialog = None

	def add_to_stack(self, window):
		self.window_stack.append(window)

	def pop_stack(self):
		if self.window_stack:
			self.active_dialog = self.window_stack.pop()
			xbmc.sleep(250)
			self.active_dialog.doModal()
		elif self.reopen_window:
			xbmc.sleep(500)
			xbmc.executebuiltin('Action(Info)')
			if self.last_control:
				xbmc.sleep(100)
				xbmc.executebuiltin('SetFocus(%s)' % self.last_control)

	def open_movie_info(self, prev_window=None, movie_id=None, dbid=None, name=None, imdb_id=None):
		Utils.show_busy()
		from resources.lib.TheMovieDB import get_movie_tmdb_id, play_movie_trailer
		from resources.lib.DialogVideoInfo import get_movie_window
		if not movie_id:
			movie_id = get_movie_tmdb_id(imdb_id=imdb_id, dbid=dbid, name=name)
		movieclass = get_movie_window(DialogXML)
		if Utils.NETFLIX_VIEW == 'true':
			dialog = movieclass(u'script.extendedinfo-DialogVideoInfo-Netflix.xml', Utils.ADDON_PATH, id=movie_id, dbid=dbid)
			if Utils.AUTOPLAY_TRAILER == 'true' and not xbmc.getCondVisibility('VideoPlayer.IsFullscreen') and not xbmc.Player().isPlayingAudio():
				play_movie_trailer(movie_id)
		else:
			if Utils.SKIN_DIR == 'skin.estuary':
				dialog = movieclass(u'script.extendedinfo-DialogVideoInfo-Estuary.xml', Utils.ADDON_PATH, id=movie_id, dbid=dbid)
			elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
				dialog = movieclass(u'script.extendedinfo-DialogVideoInfo-Aura.xml', Utils.ADDON_PATH, id=movie_id, dbid=dbid)
			else:
				dialog = movieclass(u'script.extendedinfo-DialogVideoInfo.xml', Utils.ADDON_PATH, id=movie_id, dbid=dbid)
		Utils.hide_busy()
		self.open_dialog(dialog, prev_window)

	def open_tvshow_info(self, prev_window=None, tmdb_id=None, dbid=None, tvdb_id=None, imdb_id=None, name=None):
		Utils.show_busy()
		dbid = int(dbid) if dbid and int(dbid) > 0 else None
		from resources.lib.TheMovieDB import get_show_tmdb_id, search_media, play_tv_trailer
		from resources.lib.DialogTVShowInfo import get_tvshow_window
		from resources.lib.local_db import get_imdb_id_from_db
		if tmdb_id:
			pass
		elif tvdb_id:
			tmdb_id = get_show_tmdb_id(tvdb_id)
		elif imdb_id:
			tmdb_id = get_show_tmdb_id(tvdb_id=imdb_id, source='imdb_id')
		elif dbid:
			tvdb_id = get_imdb_id_from_db(media_type='tvshow', dbid=dbid)
			if tvdb_id:
				tmdb_id = get_show_tmdb_id(tvdb_id)
		elif name:
			tmdb_id = search_media(media_name=name, year='', media_type='tv')
		tvshow_class = get_tvshow_window(DialogXML)
		if Utils.NETFLIX_VIEW == 'true':
			dialog = tvshow_class(u'script.extendedinfo-DialogVideoInfo-Netflix.xml', Utils.ADDON_PATH, tmdb_id=tmdb_id, dbid=dbid)
			if Utils.AUTOPLAY_TRAILER == 'true' and not xbmc.getCondVisibility('VideoPlayer.IsFullscreen') and not xbmc.Player().isPlayingAudio():
				play_tv_trailer(tmdb_id)
		else:
			if Utils.SKIN_DIR == 'skin.estuary':
				dialog = tvshow_class(u'script.extendedinfo-DialogVideoInfo-Estuary.xml', Utils.ADDON_PATH, tmdb_id=tmdb_id, dbid=dbid)
			elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
				dialog = tvshow_class(u'script.extendedinfo-DialogVideoInfo-Aura.xml', Utils.ADDON_PATH, tmdb_id=tmdb_id, dbid=dbid)
			else:
				dialog = tvshow_class(u'script.extendedinfo-DialogVideoInfo.xml', Utils.ADDON_PATH, tmdb_id=tmdb_id, dbid=dbid)
		Utils.hide_busy()
		self.open_dialog(dialog, prev_window)

	def open_season_info(self, prev_window=None, tvshow_id=None, season=None, tvshow=None, dbid=None):
		Utils.show_busy()
		from resources.lib.TheMovieDB import get_tmdb_data
		from resources.lib.DialogSeasonInfo import get_season_window
		if not tvshow_id:
			response = get_tmdb_data('search/tv?query=%s&language=%s&' % (Utils.url_quote(tvshow), xbmcaddon.Addon().getSetting('LanguageID')), 30)
			if response['results']:
				tvshow_id = str(response['results'][0]['id'])
			else:
				tvshow = re.sub('\(.*?\)', '', tvshow)
				response = get_tmdb_data('search/tv?query=%s&language=%s&' % (Utils.url_quote(tvshow), xbmcaddon.Addon().getSetting('LanguageID')), 30)
				if response['results']:
					tvshow_id = str(response['results'][0]['id'])
		season_class = get_season_window(DialogXML)
		if Utils.NETFLIX_VIEW == 'true':
			dialog = season_class(u'script.extendedinfo-DialogVideoInfo-Netflix.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, dbid=dbid)
		else:
			if Utils.SKIN_DIR == 'skin.estuary':
				dialog = season_class(u'script.extendedinfo-DialogVideoInfo-Estuary.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, dbid=dbid)
			elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
				dialog = season_class(u'script.extendedinfo-DialogVideoInfo-Aura.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, dbid=dbid)
			else:
				dialog = season_class(u'script.extendedinfo-DialogVideoInfo.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, dbid=dbid)
		Utils.hide_busy()
		self.open_dialog(dialog, prev_window)

	def open_episode_info(self, prev_window=None, tvshow_id=None, tvdb_id=None, season=None, episode=None, tvshow=None, dbid=None):
		Utils.show_busy()
		from resources.lib.TheMovieDB import get_tmdb_data, get_show_tmdb_id
		from resources.lib.DialogEpisodeInfo import get_episode_window
		if not tvshow_id:
			if tvdb_id:
				tvshow_id = get_show_tmdb_id(tvdb_id)
			else:
				response = get_tmdb_data('search/tv?query=%s&language=%s&' % (Utils.url_quote(tvshow), xbmcaddon.Addon().getSetting('LanguageID')), 30)
				if response['results']:
					tvshow_id = str(response['results'][0]['id'])
				else:
					tvshow = re.sub('\(.*?\)', '', tvshow)
					response = get_tmdb_data('search/tv?query=%s&language=%s&' % (Utils.url_quote(tvshow), xbmcaddon.Addon().getSetting('LanguageID')), 30)
					if response['results']:
						tvshow_id = str(response['results'][0]['id'])
		ep_class = get_episode_window(DialogXML)
		if Utils.NETFLIX_VIEW == 'true':
			dialog = ep_class(u'script.extendedinfo-DialogVideoInfo-Netflix.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, episode=episode, dbid=dbid)
		else:
			if Utils.SKIN_DIR == 'skin.estuary':
				dialog = ep_class(u'script.extendedinfo-DialogVideoInfo-Estuary.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, episode=episode, dbid=dbid)
			elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
				dialog = ep_class(u'script.extendedinfo-DialogVideoInfo-Aura.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, episode=episode, dbid=dbid)
			else:
				dialog = ep_class(u'script.extendedinfo-DialogVideoInfo.xml', Utils.ADDON_PATH, tvshow_id=tvshow_id, season=season, episode=episode, dbid=dbid)
		Utils.hide_busy()
		self.open_dialog(dialog, prev_window)

	def open_actor_info(self, prev_window=None, actor_id=None, name=None):
		from resources.lib.DialogActorInfo import get_actor_window
		from resources.lib.TheMovieDB import get_person_info
		if not actor_id:
			name = name.decode('utf-8').split(' ' + 'as' + ' ')
			names = name[0].strip().split(' / ')
			if len(names) > 1:
				ret = xbmcgui.Dialog().select(heading='Select person', list=names)
				if ret == -1:
					return None
				name = names[ret]
			else:
				name = names[0]
			Utils.show_busy()
			actor_info = get_person_info(name)
			if actor_info:
				actor_id = actor_info['id']
			else:
				return None
		else:
			Utils.show_busy()
		actor_class = get_actor_window(DialogXML)
		if Utils.SKIN_DIR == 'skin.estuary':
			dialog = actor_class(u'script.extendedinfo-DialogInfo-Estuary.xml', Utils.ADDON_PATH, id=actor_id)
		elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
			dialog = actor_class(u'script.extendedinfo-DialogInfo-Aura.xml', Utils.ADDON_PATH, id=actor_id)
		else:
			dialog = actor_class(u'script.extendedinfo-DialogInfo.xml', Utils.ADDON_PATH, id=actor_id)
		Utils.hide_busy()
		self.open_dialog(dialog, prev_window)

	def open_video_list(self, prev_window=None, listitems=None, filters=[], mode='filter', list_id=False, filter_label='', media_type='movie', search_str=''):
		Utils.show_busy()
		from resources.lib.DialogVideoList import get_tmdb_window
		browser_class = get_tmdb_window(DialogXML)
		if Utils.NETFLIX_VIEW == 'true':
			dialog = browser_class(u'script.extendedinfo-VideoList-Netflix.xml', Utils.ADDON_PATH, listitems=listitems, filters=filters, mode=mode, list_id=list_id, filter_label=filter_label, type=media_type, search_str=search_str)
		else:
			if Utils.SKIN_DIR == 'skin.estuary':
				dialog = browser_class(u'script.extendedinfo-VideoList-Estuary.xml', Utils.ADDON_PATH, listitems=listitems, filters=filters, mode=mode, list_id=list_id, filter_label=filter_label, type=media_type, search_str=search_str)
			elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
				dialog = browser_class(u'script.extendedinfo-VideoList-Aura.xml', Utils.ADDON_PATH, listitems=listitems, filters=filters, mode=mode, list_id=list_id, filter_label=filter_label, type=media_type, search_str=search_str)
			else:
				dialog = browser_class(u'script.extendedinfo-VideoList.xml', Utils.ADDON_PATH, listitems=listitems, filters=filters, mode=mode, list_id=list_id, filter_label=filter_label, type=media_type, search_str=search_str)
		if prev_window:
			self.add_to_stack(prev_window)
			prev_window.close()
		Utils.hide_busy()
		dialog.doModal()

	def open_slideshow(self, listitems, index):
		if Utils.SKIN_DIR == 'skin.estuary':
			slideshow = SlideShow(u'script.extendedinfo-SlideShow-Estuary.xml', Utils.ADDON_PATH, listitems=listitems, index=index)
		elif Utils.SKIN_DIR == 'skin.aura' or 'skin.auramod':
			slideshow = SlideShow(u'script.extendedinfo-SlideShow-Aura.xml', Utils.ADDON_PATH, listitems=listitems, index=index)
		else:
			slideshow = SlideShow(u'script.extendedinfo-SlideShow.xml', Utils.ADDON_PATH, listitems=listitems, index=index)
		slideshow.doModal()
		return slideshow.position

	def open_textviewer(self, header='', text='', color='FFFFFFFF'):
		dialog = TextViewerDialog('DialogTextViewer.xml', Utils.ADDON_PATH, header=header, text=text, color=color)
		dialog.doModal()

	def open_selectdialog(self, listitems):
		dialog = SelectDialog('DialogSelect.xml', Utils.ADDON_PATH, listing=listitems)
		dialog.doModal()
		return dialog.listitem, dialog.index

	def open_dialog(self, dialog, prev_window):
		if dialog.data:
			self.active_dialog = dialog
			if xbmc.getCondVisibility('Window.IsVisible(movieinformation)'):
				self.reopen_window = True
				self.last_control = xbmc.getInfoLabel('System.CurrentControlId').decode('utf-8')
				xbmc.executebuiltin('Dialog.Close(movieinformation)')
			if prev_window:
				if xbmc.Player().isPlayingVideo() and not xbmc.getCondVisibility('VideoPlayer.IsFullscreen'):
					xbmc.Player().stop()
				self.add_to_stack(prev_window)
				prev_window.close()
			dialog.doModal()
		else:
			self.active_dialog = None
			Utils.notify('Could not find item at MovieDB')

wm = WindowManager()

class DialogXML(xbmcgui.WindowXMLDialog):

	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self)
		self.window_type = 'dialog'

	def onInit(self):
		self.window_id = xbmcgui.getCurrentWindowDialogId()
		self.window = xbmcgui.Window(self.window_id)

class TextViewerDialog(xbmcgui.WindowXMLDialog):

	ACTION_PREVIOUS_MENU = [9, 92, 10]

	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self)
		self.text = kwargs.get('text')
		self.header = kwargs.get('header')
		self.color = kwargs.get('color')

	def onInit(self):
		window_id = xbmcgui.getCurrentWindowDialogId()
		xbmcgui.Window(window_id).setProperty('WindowColor', self.color)
		self.getControl(1).setLabel(self.header)
		self.getControl(5).setText(self.text)

	def onAction(self, action):
		if action in self.ACTION_PREVIOUS_MENU:
			self.close()

	def onClick(self, control_id):
		pass

	def onFocus(self, control_id):
		pass

class SlideShow(DialogXML):

	ACTION_PREVIOUS_MENU = [9, 92, 10]

	def __init__(self, *args, **kwargs):
		self.images = kwargs.get('listitems')
		self.index = kwargs.get('index')
		self.image = kwargs.get('image')
		self.action = None

	def onInit(self):
		super(SlideShow, self).onInit()
		if not self.images:
			return None
		self.getControl(10001).addItems(Utils.create_listitems(self.images))
		self.getControl(10001).selectItem(self.index)
		self.setFocusId(10001)

	def onAction(self, action):
		if action in self.ACTION_PREVIOUS_MENU:
			self.position = self.getControl(10001).getSelectedPosition()
			self.close()

class SelectDialog(xbmcgui.WindowXMLDialog):

	ACTION_PREVIOUS_MENU = [9, 92, 10]

	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self)
		self.items = kwargs.get('listing')
		self.listitems = Utils.create_listitems(self.items)
		self.listitem = None
		self.index = -1

	def onInit(self):
		self.list = self.getControl(6)
		self.getControl(3).setVisible(False)
		self.getControl(5).setVisible(False)
		self.getControl(1).setLabel('Choose option')
		self.list.addItems(self.listitems)
		self.setFocus(self.list)

	def onAction(self, action):
		if action in self.ACTION_PREVIOUS_MENU:
			self.close()

	def onClick(self, control_id):
		if control_id == 6 or control_id == 3:
			self.index = int(self.list.getSelectedItem().getProperty('index'))
			self.listitem = self.items[self.index]
			self.close()

	def onFocus(self, control_id):
		pass