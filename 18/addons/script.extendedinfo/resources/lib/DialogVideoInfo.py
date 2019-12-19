import os, shutil, threading
import xbmc, xbmcgui
from resources.lib import Utils
from resources.lib import ImageTools
from resources.lib import TheMovieDB
from resources.lib.WindowManager import wm
from resources.lib.VideoPlayer import PLAYER
from resources.lib.OnClickHandler import OnClickHandler
from resources.lib.DialogBaseInfo import DialogBaseInfo

ch = OnClickHandler()

def get_movie_window(window_type):

	class DialogVideoInfo(DialogBaseInfo, window_type):

		def __init__(self, *args, **kwargs):
			if Utils.NETFLIX_VIEW == 'true':
				super(DialogVideoInfo, self).__init__(*args, **kwargs)
				self.type = 'Movie'
				data = TheMovieDB.extended_movie_info(movie_id=kwargs.get('id'), dbid=self.dbid)
				if not data:
					return None
				self.info, self.data = data
				sets_thread = SetItemsThread(self.info['SetId'])
				sets_thread.start()
				if 'dbid' not in self.info:
					self.info['poster'] = Utils.get_file(self.info.get('poster', ''))
				sets_thread.join()
				self.setinfo = sets_thread.setinfo
				self.data['similar'] = [i for i in self.data['similar'] if i['id'] not in sets_thread.id_list]
				self.listitems = [
					(250, sets_thread.listitems),
					(1000, self.data['actors']),
					(750, Utils.merge_dict_lists(self.data['crew'])),
					(150, self.data['similar']),
					(550, self.data['studios']),
					(850, self.data['genres']),
					(1050, self.data['reviews']),
					(1250, self.data['images']),
					(1350, self.data['backdrops'])
					]
			else:
				super(DialogVideoInfo, self).__init__(*args, **kwargs)
				self.type = 'Movie'
				data = TheMovieDB.extended_movie_info(movie_id=kwargs.get('id'), dbid=self.dbid)
				if not data:
					return None
				self.info, self.data = data
				sets_thread = SetItemsThread(self.info['SetId'])
				filter_thread = ImageTools.FilterImageThread(self.info.get('thumb', ''), 25)
				for thread in [sets_thread, filter_thread]:
					thread.start()
				if 'dbid' not in self.info:
					self.info['poster'] = Utils.get_file(self.info.get('poster', ''))
				sets_thread.join()
				self.setinfo = sets_thread.setinfo
				self.data['similar'] = [i for i in self.data['similar'] if i['id'] not in sets_thread.id_list]
				filter_thread.join()
				self.info['ImageFilter'] = filter_thread.image
				self.info['ImageColor'] = filter_thread.imagecolor
				self.listitems = [
					(250, sets_thread.listitems),
					(150, self.data['similar']),
					(1150, self.data['videos']),
					(1000, self.data['actors']),
					(750, Utils.merge_dict_lists(self.data['crew'])),
					(550, self.data['studios']),
					(650, TheMovieDB.merge_with_cert_desc(self.data['releases'], 'movie')),
					(850, self.data['genres']),
					(1050, self.data['reviews']),
					(1250, self.data['images']),
					(1350, self.data['backdrops'])
					]
				

		def onInit(self):
			super(DialogVideoInfo, self).onInit()
			Utils.pass_dict_to_skin(data=self.info, prefix='movie.', window_id=self.window_id)
			Utils.pass_dict_to_skin(data=self.setinfo, prefix='movie.set.', window_id=self.window_id)
			self.get_youtube_vids('%s %s, movie' % (self.info['Label'], self.info['year']))
			self.fill_lists()

		def onClick(self, control_id):
			super(DialogVideoInfo, self).onClick(control_id)
			ch.serve(control_id, self)

		def onAction(self, action):
			super(DialogVideoInfo, self).onAction(action)
			ch.serve_action(action, self.getFocusId(), self)

		@ch.click(1000)
		@ch.click(750)
		def open_actor_info(self):
			wm.open_actor_info(prev_window=self, actor_id=self.listitem.getProperty('id'))

		@ch.click(150)
		@ch.click(250)
		def open_movie_info(self):
			wm.open_movie_info(prev_window=self, movie_id=self.listitem.getProperty('id'), dbid=self.listitem.getProperty('dbid'))

		@ch.click(550)
		def open_company_list(self):
			filters = [
				{
					'id': self.listitem.getProperty('id'),
					'type': 'with_companies',
					'typelabel': 'Studios',
					'label': self.listitem.getLabel().decode('utf-8')
				}]
			wm.open_video_list(prev_window=self, filters=filters)

		@ch.click(1050)
		def show_review(self):
			author = self.listitem.getProperty('author')
			text = '[B]%s[/B][CR]%s' % (author, Utils.clean_text(self.listitem.getProperty('content')))
			wm.open_textviewer(header='Plot', text=text, color='FFFFFFFF')

		@ch.click(850)
		def open_genre_list(self):
			filters = [
				{
					'id': self.listitem.getProperty('id'),
					'type': 'with_genres',
					'typelabel': 'Genres',
					'label': self.listitem.getLabel().decode('utf-8')
				}]
			wm.open_video_list(prev_window=self, filters=filters)

		@ch.click(650)
		def open_cert_list(self):
			filters = [
				{
					'id': self.listitem.getProperty('iso_3166_1'),
					'type': 'certification_country',
					'typelabel': 'Certification country',
					'label': self.listitem.getProperty('iso_3166_1')
				},
				{
					'id': self.listitem.getProperty('certification'),
					'type': 'certification',
					'typelabel': 'Certification',
					'label': self.listitem.getProperty('certification')
				},
				{
					'id': self.listitem.getProperty('year'),
					'type': 'year',
					'typelabel': 'Year',
					'label': self.listitem.getProperty('year')
				}]
			wm.open_video_list(prev_window=self, filters=filters)

		@ch.click(120)
		def search_in_meta_by_title(self):
			url = 'plugin://plugin.video.openmeta/movies/tmdb/search_term/%s/1/' % self.info.get('title', '')
			self.close()
			xbmc.executebuiltin('ActivateWindow(videos,%s,return)' % url)

		@ch.click(132)
		def show_plot(self):
			wm.open_textviewer(header='Plot', text=self.info['Plot'], color='FFFFFFFF')

		@ch.click(8)
		def play_movie(self):
			if self.dbid and int(self.dbid) > 0:
				dbid = self.dbid
				url = ''
				PLAYER.play_from_button(url, listitem=None, window=self, type='movieid', dbid=dbid)
			else:
				url = 'plugin://plugin.video.openmeta/movies/play/tmdb/%s' % self.info.get('id', '')
				xbmc.executebuiltin('RunPlugin(%s)' % url)

		@ch.action('contextmenu', 8)
		def play_movie_choose_player(self):
			if self.dbid and int(self.dbid) > 0:
				dbid = self.dbid
				url = ''
				PLAYER.play_from_button(url, listitem=None, window=self, type='movieid', dbid=dbid)
			else:
				url = 'plugin://plugin.video.openmeta/movies/play_choose_player/tmdb/%s/False' % self.info.get('id', '')
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

		@ch.click(18)
		def add_movie_to_library(self):
			if not xbmc.getCondVisibility('System.HasAddon(plugin.video.openmeta)'):
				xbmc.executebuiltin('RunPlugin(plugin://plugin.video.openmeta/setup/total)')
			if xbmcgui.Dialog().yesno('OpenInfo', 'Add [B]%s[/B] to library?' % self.info['title']):
				xbmc.executebuiltin('RunPlugin(plugin://plugin.video.openmeta/movies/add_to_library/tmdb/%s)' % self.info.get('id', ''))
				Utils.after_add(type='movie')
				Utils.notify(header='[B]%s[/B] added to library' % self.info['title'], message='Exit & re-enter to refresh', icon=self.info['poster'], time=5000, sound=False)

		@ch.click(19)
		def remove_movie_from_library(self):
			if not xbmc.getCondVisibility('System.HasAddon(plugin.video.openmeta)'):
				xbmc.executebuiltin('RunPlugin(plugin://plugin.video.openmeta/setup/total)')
			if xbmcgui.Dialog().yesno('OpenInfo', 'Remove [B]%s[/B] from library?' % self.info['title']):
				if os.path.exists(xbmc.translatePath('%s%s/' % (Utils.OPENMETA_MOVIE_FOLDER, self.info['imdb_id']))):
					Utils.get_kodi_json(method='VideoLibrary.RemoveMovie', params='{"movieid": %d}' % int(self.info['dbid']))
					shutil.rmtree(xbmc.translatePath('%s%s/' % (Utils.OPENMETA_MOVIE_FOLDER, self.info['imdb_id'])))
					Utils.after_add(type='movie')
					Utils.notify(header='Removed [B]%s[/B] from library' % self.info.get('title', ''), message='Exit & re-enter to refresh', icon=self.info['poster'], time=5000, sound=False)

		@ch.click(350)
		@ch.click(1150)
		def play_youtube_video(self):
			PLAYER.playtube(self.listitem.getProperty('youtube_id'), listitem=self.listitem, window=self)

		@ch.click(28)
		def play_movie_trailer_button(self):
			TheMovieDB.play_movie_trailer(self.info['id'])

		@ch.click(29)
		def stop_movie_trailer_button(self):
			xbmc.executebuiltin('PlayerControl(Stop)')

	class SetItemsThread(threading.Thread):

		def __init__(self, set_id=''):
			threading.Thread.__init__(self)
			self.set_id = set_id

		def run(self):
			if self.set_id:
				self.listitems, self.setinfo = TheMovieDB.get_set_movies(self.set_id)
				self.id_list = [item['id'] for item in self.listitems]
			else:
				self.id_list = []
				self.listitems = []
				self.setinfo = {}

	return DialogVideoInfo