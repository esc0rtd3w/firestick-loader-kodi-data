import sys
import xbmcgui, xbmcplugin
from resources.lib import process
from resources.lib import Utils

class Main:
	def __init__(self):
		xbmcgui.Window(10000).setProperty('extendedinfo_running', 'True')
		self._parse_argv()
		for info in self.infos:
			listitems = process.start_info_actions(self.infos, self.params)
			xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_TITLE)
			xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
			xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_DURATION)
			if info.endswith('shows'):
				xbmcplugin.setContent(self.handle, 'tvshows')
			elif info.endswith('movies'):
				xbmcplugin.setContent(self.handle, 'movies')
			else:
				xbmcplugin.setContent(self.handle, 'addons')
			Utils.pass_list_to_skin(name=info, data=listitems, prefix=self.params.get('prefix', ''), handle=self.handle, limit=self.params.get('limit', 20))
		else:
			items = [
				('popularmovies', 'Popular Movies'),
				('topratedmovies', 'Top Rated Movies'),
				('incinemamovies', 'In Theaters Movies'),
				('upcomingmovies', 'Upcoming Movies'),
				('libraryallmovies', 'My Movies (Library)'),
				('populartvshows', 'Popular TV Shows'),
				('topratedtvshows', 'Top Rated TV Shows'),
				('onairtvshows', 'Currently Airing TV Shows'),
				('airingtodaytvshows', 'Airing Today TV Shows'),
				('libraryalltvshows', 'My TV Shows (Library)')
				]
			NoFolder_items = [
				('allmovies', 'All Movies'),
				('alltvshows', 'All TV Shows'),
				('search_menu', 'Search...')
				]
			xbmcplugin.setContent(self.handle, 'addons')
			for key, value in items:
				thumb_path  = 'special://home/addons/script.extendedinfo/resources/skins/Default/media/tmdb/thumb.png'
				fanart_path = 'special://home/addons/script.extendedinfo/resources/skins/Default/media/tmdb/fanart.jpg'
				url = 'plugin://script.extendedinfo?info=%s&limit=0' % key
				li = xbmcgui.ListItem(label=value)
				li.setArt({'thumb': thumb_path, 'fanart': fanart_path})
				xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True)
			for key, value in NoFolder_items:
				thumb_path  = 'special://home/addons/script.extendedinfo/resources/skins/Default/media/tmdb/thumb.png'
				fanart_path = 'special://home/addons/script.extendedinfo/resources/skins/Default/media/tmdb/fanart.jpg'
				url = 'plugin://script.extendedinfo?info=%s' % key
				li = xbmcgui.ListItem(label=value)
				li.setArt({'thumb': thumb_path, 'fanart': fanart_path})
				xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=False)
			xbmcplugin.endOfDirectory(self.handle)
		xbmcgui.Window(10000).clearProperty('extendedinfo_running')

	def _parse_argv(self):
		args = sys.argv[2][1:]
		self.handle = int(sys.argv[1])
		self.infos = []
		self.params = {'handle': self.handle}
		if args.startswith('---'):
			delimiter = '&'
			args = args[3:]
		else:
			delimiter = '&'
		for arg in args.split(delimiter):
			param = arg.replace('"', '').replace("'", " ")
			if param.startswith('info='):
				self.infos.append(param[5:])
			else:
				try:
					self.params[param.split('=')[0].lower()] = '='.join(param.split('=')[1:]).strip()
				except:
					pass

if (__name__ == '__main__'):
	Main()

