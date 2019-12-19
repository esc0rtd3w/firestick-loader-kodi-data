import xbmc, xbmcgui
from resources.lib import Utils
from resources.lib import ImageTools
from resources.lib import TheMovieDB
from resources.lib.WindowManager import wm
from resources.lib.VideoPlayer import PLAYER
from resources.lib.OnClickHandler import OnClickHandler
from resources.lib.DialogBaseInfo import DialogBaseInfo

ch = OnClickHandler()

def get_season_window(window_type):

	class DialogSeasonInfo(DialogBaseInfo, window_type):

		def __init__(self, *args, **kwargs):
			if Utils.NETFLIX_VIEW == 'true':
				super(DialogSeasonInfo, self).__init__(*args, **kwargs)
				self.type = 'Season'
				self.tvshow_id = kwargs.get('tvshow_id')
				data = TheMovieDB.extended_season_info(tvshow_id=self.tvshow_id, season_number=kwargs.get('season'))
				if not data:
					return None
				self.info, self.data = data
				if 'dbid' not in self.info:
					self.info['poster'] = Utils.get_file(url=self.info.get('poster', ''))
				self.listitems = [
					(2000, self.data['episodes']),
					(1000, self.data['actors']),
					(750, self.data['crew']),
					(1250, self.data['images'])
					]
			else:
				super(DialogSeasonInfo, self).__init__(*args, **kwargs)
				self.type = 'Season'
				self.tvshow_id = kwargs.get('tvshow_id')
				data = TheMovieDB.extended_season_info(tvshow_id=self.tvshow_id, season_number=kwargs.get('season'))
				if not data:
					return None
				self.info, self.data = data
				if 'dbid' not in self.info:
					self.info['poster'] = Utils.get_file(url=self.info.get('poster', ''))
				self.info['ImageFilter'], self.info['ImageColor'] = ImageTools.filter_image(input_img=self.info.get('poster', ''), radius=25)
				self.listitems = [
					(2000, self.data['episodes']),
					(1150, self.data['videos']),
					(1000, self.data['actors']),
					(750, self.data['crew']),
					(1250, self.data['images'])
					]

		def onInit(self):
			self.get_youtube_vids('%s %s tv' % (self.info['TVShowTitle'], self.info['title']))
			super(DialogSeasonInfo, self).onInit()
			Utils.pass_dict_to_skin(data=self.info, prefix='movie.', window_id=self.window_id)
			self.fill_lists()

		def onClick(self, control_id):
			super(DialogSeasonInfo, self).onClick(control_id)
			ch.serve(control_id, self)

		def onAction(self, action):
			super(DialogSeasonInfo, self).onAction(action)
			ch.serve_action(action, self.getFocusId(), self)

		@ch.click(120)
		def browse_season(self):
			url = 'plugin://plugin.video.openmeta/tv/tvdb/%s/%s/' % (self.info['tvdb_id'], self.info['season'])
			self.close()
			xbmc.executebuiltin('ActivateWindow(videos,%s,return)' % url)

		@ch.click(750)
		@ch.click(1000)
		def open_actor_info(self):
			wm.open_actor_info(prev_window=self, actor_id=self.listitem.getProperty('id'))

		@ch.click(2000)
		def open_episode_info(self):
			wm.open_episode_info(prev_window=self, tvshow=self.info['TVShowTitle'], tvshow_id=self.tvshow_id, season=self.listitem.getProperty('season'), episode=self.listitem.getProperty('episode'))

		@ch.click(10)
		def play_season(self):
			url = 'plugin://plugin.video.openmeta/tv/play/%s/%s/1' % (self.info['tvdb_id'], self.info['season'])
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		@ch.action('contextmenu', 10)
		def play_season_choose_player(self):
			url = 'plugin://plugin.video.openmeta/tv/play_choose_player/%s/%s/1/False' % (self.info['tvdb_id'], self.info['season'])
			xbmc.executebuiltin('RunPlugin(%s)' % url)

		@ch.click(445)
		def show_manage_dialog(self):
			manage_list = []
			manage_list.append(["OpenInfo's settings", 'Addon.OpenSettings("script.extendedinfo")'])
			manage_list.append(["OpenMeta's settings", 'Addon.OpenSettings("plugin.video.openmeta")'])
			manage_list.append(["YouTube's settings", 'Addon.OpenSettings("plugin.video.youtube")'])
			selection = xbmcgui.Dialog().select(heading='Settings', list=[i[0] for i in manage_list])
			if selection > -1:
				for item in manage_list[selection][1].split('||'):
					xbmc.executebuiltin(item)

		@ch.click(132)
		def open_text(self):
			wm.open_textviewer(header='Overview', text=self.info['Plot'], color='FFFFFFFF')

		@ch.click(350)
		@ch.click(1150)
		def play_youtube_video(self):
			PLAYER.playtube(self.listitem.getProperty('youtube_id'), listitem=self.listitem, window=self)

	return DialogSeasonInfo