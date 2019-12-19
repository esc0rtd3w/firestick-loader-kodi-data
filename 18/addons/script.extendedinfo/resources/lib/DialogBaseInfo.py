import xbmc, xbmcgui
from resources.lib import Utils
from resources.lib import YouTube
from resources.lib import TheMovieDB
from resources.lib.WindowManager import wm
from resources.lib.OnClickHandler import OnClickHandler

ch = OnClickHandler()

class DialogBaseInfo(object):

	ACTION_PREVIOUS_MENU = [92, 9]
	ACTION_EXIT_SCRIPT = [13, 10]

	def __init__(self, *args, **kwargs):
		super(DialogBaseInfo, self).__init__(*args, **kwargs)
		self.dbid = kwargs.get('dbid')
		self.bouncing = False
		self.data = None
		self.yt_listitems = []
		self.info = {}

	def onInit(self, *args, **kwargs):
		super(DialogBaseInfo, self).onInit()
		xbmcgui.Window(10000).setProperty('ImageColor', self.info.get('ImageColor', ''))
		self.window = xbmcgui.Window(self.window_id)
		self.window.setProperty('type', self.type)
		xbmcgui.Window(10000).setProperty('ExtendedInfo_fanart', self.info.get('fanart', ''))

	def onAction(self, action):
		ch.serve_action(action, self.getFocusId(), self)

	def onClick(self, control_id):
		ch.serve(control_id, self)

	def onFocus(self, control_id):
		if control_id == 20000:
			if not self.bouncing:
				self.bounce('up')
			self.setFocusId(self.last_focus)
			self.last_focus = control_id
		elif control_id == 20001:
			if not self.bouncing:
				self.bounce('down')
			self.setFocusId(self.last_focus)
			self.last_focus = control_id
		else:
			self.last_focus = control_id

	@Utils.run_async
	def bounce(self, identifier):
		self.bouncing = True
		self.window.setProperty('Bounce.' + identifier, 'true')
		xbmc.sleep(100)
		self.window.clearProperty('Bounce.' + identifier)
		self.bouncing = False

	def fill_lists(self):
		for container_id, listitems in self.listitems:
			try:
				self.getControl(container_id).reset()
				self.getControl(container_id).addItems(Utils.create_listitems(listitems))
			except:
				Utils.log('Notice: No container with id %i available' % container_id)

	@ch.click(1250)
	@ch.click(1350)
	def open_image(self):
		listitems = next((v for (i, v) in self.listitems if i == self.control_id), None)
		index = self.control.getSelectedPosition()
		pos = wm.open_slideshow(listitems=listitems, index=index)
		self.control.selectItem(pos)

	@ch.action('contextmenu', 1250)
	def thumbnail_options(self):
		if not self.info.get('dbid'):
			return None
		selection = xbmcgui.Dialog().select(heading='Artwork', list=['Use as thumbnail'])
		if selection == 0:
			path = self.listitem.getProperty('original')
			media_type = self.window.getProperty('type')
			params = '"art": {"poster": "%s"}' % path
			Utils.get_kodi_json(method='VideoLibrary.Set%sDetails' % media_type, params='{ %s, "%sid":%s }' % (params, media_type.lower(), self.info['dbid']))

	@ch.action('contextmenu', 1350)
	def fanart_options(self):
		if not self.info.get('dbid'):
			return None
		selection = xbmcgui.Dialog().select(heading='Fanart', list=['Use as fanart'])
		if selection == 0:
			path = self.listitem.getProperty('original')
			media_type = self.window.getProperty('type')
			params = '"art": {"fanart": "%s"}' % path
			Utils.get_kodi_json(method='VideoLibrary.Set%sDetails' % media_type, params='{ %s, "%sid":%s }' % (params, media_type.lower(), self.info['dbid']))

	@ch.action('parentdir', '*')
	@ch.action('parentfolder', '*')
	def previous_menu(self):
		onback = self.window.getProperty('%i_onback' % self.control_id)
		if onback:
			xbmc.executebuiltin(onback)
		else:
			self.close()
			wm.pop_stack()

	@ch.action('previousmenu', '*')
	def exit_script(self):
		self.close()

	@Utils.run_async
	def get_youtube_vids(self, search_str):
		try:
			youtube_list = self.getControl(350)
		except:
			return None
		result = YouTube.search_youtube(search_str, limit=10)
		if not self.yt_listitems:
			self.yt_listitems = result.get('listitems', [])
			if 'videos' in self.data:
				vid_ids = [item['key'] for item in self.data['videos']]
				self.yt_listitems = [i for i in self.yt_listitems if i['youtube_id'] not in vid_ids]
		youtube_list.reset()
		youtube_list.addItems(Utils.create_listitems(self.yt_listitems))

	def open_credit_dialog(self, credit_id):
		info = TheMovieDB.get_credit_info(credit_id)
		listitems = []
		if 'seasons' in info['media']:
			listitems += TheMovieDB.handle_tmdb_seasons(info['media']['seasons'])
		if 'episodes' in info['media']:
			listitems += TheMovieDB.handle_tmdb_episodes(info['media']['episodes'])
		if not listitems:
			listitems += [{'label': 'No information available'}]
		listitem, index = wm.open_selectdialog(listitems=listitems)
		if listitem['media_type'] == 'episode':
			wm.open_episode_info(prev_window=self, season=listitems[index]['season'], episode=listitems[index]['episode'], tvshow_id=info['media']['id'])
		elif listitem['media_type'] == 'season':
			wm.open_season_info(prev_window=self, season=listitems[index]['season'], tvshow_id=info['media']['id'])