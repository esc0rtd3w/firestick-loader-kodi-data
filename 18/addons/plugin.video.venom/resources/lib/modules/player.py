# -*- coding: utf-8 -*-

import sys
import urllib, hashlib, json
import xbmc

try:
	import AddonSignals
except:
	pass

from resources.lib.modules import cleantitle, control, playcount, log_utils

try:
	sysaddon = sys.argv[0]
	syshandle = int(sys.argv[1])
except:
	pass

try:
	from sqlite3 import dbapi2 as database
except:
	from pysqlite2 import dbapi2 as database

notificationSound = False if control.setting('notification.sound') == 'false' else True


class Player(xbmc.Player):
	def __init__(self):
		xbmc.Player.__init__(self)
		self.play_next_triggered = False
		self.media_type = None
		self.offset = '0'
		self.media_length = 0
		self.current_time = 0
		self.meta = {}
		self.playback_started = False
		self.scrobbled = False
		self.playback_resumed = False
		self.av_started = False


	def play_source(self, title, year, season, episode, imdb, tvdb, url, meta, select=None):
		try:
			if url is None:
				control.cancelPlayback()
				raise Exception

			control.sleep(200)
			self.media_type = 'movie' if season is None or episode is None else 'episode'
			self.title = title
			self.year = str(year)

			if self.media_type == 'movie':
				self.name = urllib.quote_plus(title) + urllib.quote_plus(' (%s)' % self.year) 
				self.season = None
				self.episode = None

			elif self.media_type == 'episode':
				self.name = urllib.quote_plus(title) + urllib.quote_plus(' S%02dE%02d' % (int(season), int(episode)))
				self.season = '%01d' % int(season)
				self.episode = '%01d' % int(episode)

			self.name = urllib.unquote_plus(self.name)

			self.DBID = None

			self.imdb = imdb if imdb is not None else '0'
			self.tvdb = tvdb if tvdb is not None else '0'
			self.ids = {'imdb': self.imdb, 'tvdb': self.tvdb}
			self.ids = dict((k, v) for k, v in self.ids.iteritems() if v != '0')

			self.meta = meta
			self.offset = Bookmarks().get(self.name, self.year)
			poster, thumb, season_poster, fanart, banner, clearart, clearlogo, discart, meta = self.getMeta(meta)

			item = control.item(path=url)

			if self.media_type == 'episode':
				self.episodeIDS = meta.get('episodeIDS', '0')
				item.setUniqueIDs(self.episodeIDS)
				if control.setting('disable.player.art') == 'true':
					item.setArt({'thumb': thumb, 'tvshow.poster': season_poster, 'season.poster': season_poster, 'tvshow.fanart': fanart})
				else:
					item.setArt({'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.discart': discart, 'thumb': thumb, 'tvshow.poster': season_poster, 'season.poster': season_poster, 'tvshow.fanart': fanart})
			else:
				item.setUniqueIDs(self.ids)
				if control.setting('disable.player.art') == 'true':
					item.setArt({'thumb': thumb, 'poster': poster, 'fanart': fanart})
				else:
					item.setArt({'clearart': clearart, 'clearlogo': clearlogo, 'discart': discart, 'thumb': thumb, 'poster': poster, 'fanart': fanart})

			# self.tvdb_key = 'N1I4U1paWDkwVUE5WU1CVQ=='
			# self.imdb_user = control.setting('imdb.user').replace('ur', '')
			# self.user = str(self.imdb_user) + str(self.tvdb_key)
			# self.lang = control.apiLanguage()['tvdb']
			# items = [{'imdb': imdb, 'tvdb': tvdb}]
			# list = metacache.fetch(items, self.lang, self.user)
			# if 'castandart' in str(list):
				# item.setCast(list[0].get('castandart', ''))

			# test = control.infoLabel('ListItem.thumb')
			# log_utils.log('thumb = %s' % test, __name__, log_utils.LOGDEBUG)

			if 'castandart' in meta:
				item.setCast(meta.get('castandart', ''))

			item.setInfo(type='video', infoLabels=control.metadataClean(meta))

			if 'plugin' not in control.infoLabel('Container.PluginName') or select != '1':
				if control.window.getProperty('infodialogs.active'):
					control.closeAll()
				control.resolve(syshandle, True, item)

			elif select == '1':
				control.closeAll()
				control.player.play(url, item)

			self.keepAlive()
			control.window.setProperty('script.trakt.ids', json.dumps(self.ids))
			control.window.clearProperty('script.trakt.ids')
		except:
			log_utils.error()
			return	control.cancelPlayback()


	def getMeta(self, meta):
		try:
			if meta is None:
				raise Exception()
			poster = meta.get('poster')
			thumb = meta.get('thumb')
			thumb = thumb or poster or control.addonThumb()
			season_poster = meta.get('season_poster') or poster
			fanart = meta.get('fanart')
			banner = meta.get('banner')
			clearart = meta.get('clearart')
			clearlogo = meta.get('clearlogo')
			discart = meta.get('discart')
			if 'mediatype' not in meta:
				meta.update({'mediatype': 'episode' if 'episode' in meta and meta['episode'] else 'movie'})

			return (poster, thumb, season_poster, fanart, banner, clearart, clearlogo, discart, meta)
		except:
			log_utils.error()
			pass

		try:
			raise Exception() #kodi seems to use scraped artwork so retrival from library not needed
			if self.media_type != 'movie':
				raise Exception()

			meta = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "originaltitle", "year", "genre", "studio", "country", "runtime", "rating", "votes", "mpaa", "director", "writer", "plot", "plotoutline", "tagline", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year) + 1), str(int(self.year) - 1)))
			meta = unicode(meta, 'utf-8', errors = 'ignore')
			meta = json.loads(meta)['result']['movies']

			t = cleantitle.get(self.title)
			meta = [i for i in meta if self.year == str(i['year']) and (t == cleantitle.get(i['title']) or t == cleantitle.get(i['originaltitle']))][0]
			if 'mediatype' not in meta:
				meta.update({'mediatype': 'movie'})

			for k, v in meta.iteritems():
				if type(v) == list:
					try:
						meta[k] = str(' / '.join([i.encode('utf-8') for i in v]))
					except:
						meta[k] = ''
				else:
					try:
						meta[k] = str(v.encode('utf-8'))
					except:
						meta[k] = str(v)

			if 'plugin' not in control.infoLabel('Container.PluginName'):
				self.DBID = meta.get('movieid')

			poster = thumb = meta.get('thumbnail')
			return (poster, '', '', '', '', '', '', '', meta)
		except:
			log_utils.error()
			pass

		try:
			raise Exception() #kodi seems to use scraped artwork so retrival from library not needed
			if self.media_type != 'episode':
				raise Exception()

			meta = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties" : ["title", "year", "thumbnail", "file"]}, "id": 1}' % (self.year, str(int(self.year)+1), str(int(self.year)-1)))
			meta = unicode(meta, 'utf-8', errors = 'ignore')
			meta = json.loads(meta)['result']['tvshows']

			t = cleantitle.get(self.title)
			meta = [i for i in meta if self.year == str(i['year']) and t == cleantitle.get(i['title'])][0]

			tvshowid = meta['tvshowid']
			poster = meta['thumbnail']

			meta = control.jsonrpc('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params":{ "tvshowid": %d, "filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "season", "episode", "showtitle", "firstaired", "runtime", "rating", "director", "writer", "plot", "thumbnail", "file"]}, "id": 1}' % (tvshowid, self.season, self.episode))
			meta = unicode(meta, 'utf-8', errors = 'ignore')
			meta = json.loads(meta)['result']['episodes'][0]

			if 'mediatype' not in meta:
				meta.update({'mediatype': 'episode'})

			for k, v in meta.iteritems():
				if type(v) == list:
					try:
						meta[k] = str(' / '.join([i.encode('utf-8') for i in v]))
					except:
						meta[k] = ''
				else:
					try:
						meta[k] = str(v.encode('utf-8'))
					except:
						meta[k] = str(v)

			if 'plugin' not in control.infoLabel('Container.PluginName'):
				self.DBID = meta.get('episodeid')

			thumb = meta['thumbnail']
			return (poster, '', '', '', '', '', '', '', meta)
		except:
			log_utils.error()
			pass
			poster, thumb, season_poster, fanart, banner, clearart, clearlogo, discart, meta = '', '', '', '', '', '', '', '', {'title': self.name}
			return (poster, thumb, season_poster, fanart, banner, clearart, clearlogo, discart, meta)


	def getWatchedPercent(self):
		if self.isPlayback():
			try:
				position = self.getTime()
				if position is not 0:
					self.current_time = position
				total_length = self.getTotalTime()
				if total_length is not 0:
					self.media_length = total_length
			except:
				pass

		current_position = self.current_time
		total_length = self.media_length
		watched_percent = 0

		if int(total_length) is not 0:
			try:
				watched_percent = float(current_position) / float(total_length) * 100
				if watched_percent > 100:
					watched_percent = 100
			except:
				log_utils.error()
				pass
		return watched_percent


	def keepAlive(self):
		pname = '%s.player.overlay' % control.addonInfo('id')
		control.window.clearProperty(pname)

		if self.media_type == 'movie':
			overlay = playcount.getMovieOverlay(playcount.getMovieIndicators(), self.imdb)

		elif self.media_type == 'episode':
			overlay = playcount.getEpisodeOverlay(playcount.getTVShowIndicators(), self.imdb, self.tvdb, self.season, self.episode)
		else:
			overlay = '6'

		for i in range(0, 240):
			if self.isPlayback():
				break
			xbmc.sleep(1000)

		while self.isPlayingVideo():
			try:
				if not self.playback_started:
					xbmc.sleep(1000)
					continue

				if not self.playback_started:
					self.start_playback()

				try:
					self.current_time = self.getTime()
					self.media_length = self.getTotalTime()
				except:
					pass

				watcher = (self.getWatchedPercent() >= 80)
				property = control.window.getProperty(pname)

				if self.media_type == 'movie':
					try:
						if watcher is True and property != '7':
							control.window.setProperty(pname, '7')
							playcount.markMovieDuringPlayback(self.imdb, '7')
						# elif watcher is False and property != '6':
							# control.window.setProperty(pname, '6')
							# playcount.markMovieDuringPlayback(self.imdb, '6')
					except:
						continue
					xbmc.sleep(2000)

				elif self.media_type == 'episode':
					try:
						if watcher is True and property != '7':
							control.window.setProperty(pname, '7')
							playcount.markEpisodeDuringPlayback(self.imdb, self.tvdb, self.season, self.episode, '7')
						# elif watcher is False and property != '6':
							# control.window.setProperty(pname, '6')
							# playcount.markEpisodeDuringPlayback(self.imdb, self.tvdb, self.season, self.episode, '6')
					except:
						continue
					xbmc.sleep(2000)

			except:
				log_utils.error()
				xbmc.sleep(1000)
				continue

		control.window.clearProperty(pname)
		# self.onPlayBackEnded()


	def start_playback(self):
		try:
			if self.playback_started:
				return
			if not self.isPlayback():
				return
			self.playback_started = True

			# control.execute('Dialog.Close(all,true)')
			self.current_time = self.getTime()
			self.media_length = self.getTotalTime()

			if self.media_type == 'episode' and control.setting('enable.upnext') == 'true':
				if int(control.playlist.getposition()) == -1:
					control.playlist.clear()
					return
				source_id = 'plugin.video.venom'
				return_id = 'plugin.video.venom_play_action'

				try:
					# if int(control.playlist.getposition()) < (control.playlist.size() - 1) and not int(control.playlist.getposition()) == -1:
					if int(control.playlist.getposition()) < (control.playlist.size() - 1):
						if self.media_type is None:
							return
						next_info = self.next_info()
						AddonSignals.sendSignal('upnext_data', next_info, source_id)
						AddonSignals.registerSlot('upnextprovider', return_id, self.signals_callback)

						# # Prescrape
						# from resources.lib.modules import sources
						# psources = sources.Sources().preScrape(title=next_info['next_episode']['title'], year=next_info['next_episode']['year'], imdb=next_info['next_episode']['tvshowimdb'], tvdb=next_info['next_episode']['tvshowid'], season=next_info['next_episode']['season'], episode=next_info['next_episode']['episode'], tvshowtitle=next_info['next_episode']['showtitle'], premiered=next_info['next_episode']['firstaired'])

				except:
					log_utils.error()
					pass

		except:
			log_utils.error()
			pass


	def libForPlayback(self):
		if self.DBID is None:
			return
		try:
			if self.media_type == 'movie':
				rpc = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "playcount": 1 }, "id": 1 }' % str(self.DBID)
			elif self.media_type == 'episode':
				rpc = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid": %s, "playcount": 1 }, "id": 1 }' % str(self.DBID)
			control.jsonrpc(rpc)
			control.refresh()
		except:
			log_utils.error()
			pass


	def isPlayback(self):
		# Kodi often starts playback where isPlaying() is true and isPlayingVideo() is false, since the video loading is still in progress, whereas the play is already started.
		return self.isPlaying() and self.isPlayingVideo() and self.getTime() >= 0


	def onPlayBackSeek(self, time, seekOffset):
		seekOffset /= 1000


	def onAVStarted(self):
		for i in range(0, 500):
			if self.isPlayback():
				self.av_started = True
				break
			else:
				xbmc.sleep(1000)

		if self.offset != '0' and self.playback_resumed is False:
			# log_utils.log('Seeking %.2f minutes' % (float(self.offset) / 60), __name__, log_utils.LOGDEBUG)
			self.seekTime(float(self.offset))
			self.playback_resumed = True

		if control.setting('subtitles') == 'true':
			Subtitles().get(self.name, self.imdb, self.season, self.episode)

		self.start_playback()
		xbmc.log('onAVStarted callback', 2)


	def onPlayBackStarted(self):
		if self.av_started:
			return
		for i in range(0, 500):
			if self.isPlayback():
				break
			else:
				xbmc.sleep(1000)

		if self.offset != '0' and self.playback_resumed is False:
			self.seekTime(float(self.offset))
			self.playback_resumed = True

		if control.setting('subtitles') == 'true':
			Subtitles().get(self.name, self.imdb, self.season, self.episode)

		self.start_playback()
		xbmc.log('onPlayBackStarted callback', 2)


	def onPlayBackStopped(self):
		Bookmarks().reset(self.current_time, self.media_length, self.name, self.year)
		try:
			if (self.current_time / self.media_length) >= .80:
				self.libForPlayback()
		except:
			pass
		if control.setting('crefresh') == 'true':
			xbmc.sleep(2000)
			xbmc.executebuiltin('Container.Refresh')
		# control.playlist.clear()
		control.trigger_widget_refresh()
		xbmc.log('onPlayBackStopped callback', 2)


	def onPlayBackEnded(self):
		Bookmarks().reset(self.current_time, self.media_length, self.name, self.year)
		self.libForPlayback()
		if control.setting('crefresh') == 'true':
			xbmc.sleep(2000)
			xbmc.executebuiltin('Container.Refresh')
		control.trigger_widget_refresh()
		xbmc.log('onPlayBackEnded callback', 2)


	def onPlayBackError(self):
		Bookmarks().reset(self.current_time, self.media_length, self.name, self.year)
		log_utils.error()
		sys.exit(1)
		xbmc.log('onPlayBackError callback', 2)


	def signals_callback(self, data):
		if not self.play_next_triggered:
			if not self.scrobbled:
				try:
					self.onPlayBackEnded()
					self.scrobbled = True
				except:
					pass
			self.play_next_triggered = True
			# Using a seek here as playnext causes Kodi gui to wig out. So we seek instead so it looks more graceful
			self.seekTime(self.media_length)


	def next_info(self):
		current_info = self.meta
		current_episode = {}
		current_episode["episodeid"] = current_info.get('episodeIDS', {}).get('trakt')
		current_episode["tvshowid"] = current_info.get('tvdb')
		current_episode["title"] = current_info.get('title')
		current_episode["art"] = {}
		current_episode["art"]["tvshow.poster"] = current_info.get('poster')
		current_episode["art"]["thumb"] = current_info.get('thumb')
		current_episode["art"]["tvshow.fanart"] = current_info.get('fanart')
		current_episode["art"]["tvshow.landscape"] = current_info.get('fanart')
		current_episode["art"]["tvshow.clearart"] = current_info.get('clearart')
		current_episode["art"]["tvshow.clearlogo"] = current_info.get('clearlogo')
		current_episode["plot"] = current_info.get('plot')
		current_episode["showtitle"] = current_info.get('tvshowtitle')
		current_episode["playcount"] = current_info.get('playcount')
		current_episode["season"] = current_info.get('season')
		current_episode["episode"] = current_info.get('episode')
		current_episode["rating"] = current_info.get('rating')
		current_episode["firstaired"] = current_info.get('tvshowyear')
		# log_utils.log('current_episode = %s' % current_episode, __name__, log_utils.LOGDEBUG)

		current_position = control.playlist.getposition()
		next_url = control.playlist[current_position + 1].getPath()

		try:
			from urlparse import parse_qsl
		except:
			from urllib.parse import parse_qsl
		params = dict(parse_qsl(next_url.replace('?', '')))
		next_info = json.loads(params.get('meta'))

		next_episode = {}
		next_episode["episodeid"] = next_info.get('episodeIDS', {}).get('trakt')
		next_episode["tvshowid"] = next_info.get('tvdb')
		next_episode["title"] = next_info.get('title')
		next_episode["art"] = {}
		next_episode["art"]["tvshow.poster"] = next_info.get('poster')
		next_episode["art"]["thumb"] = next_info.get('thumb')
		next_episode["art"]["tvshow.fanart"] = next_info.get('fanart')
		next_episode["art"]["tvshow.landscape"] = next_info.get('fanart')
		next_episode["art"]["tvshow.clearart"] = next_info.get('clearart')
		next_episode["art"]["tvshow.clearlogo"] = next_info.get('clearlogo')
		next_episode["plot"] = next_info.get('plot')
		next_episode["showtitle"] = next_info.get('tvshowtitle')
		next_episode["playcount"] = next_info.get('playcount')
		next_episode["season"] = next_info.get('season')
		next_episode["episode"] = next_info.get('episode')
		next_episode["rating"] = next_info.get('rating')
		next_episode["firstaired"] = next_info.get('tvshowyear')

		next_episode["tvshowimdb"] = next_info.get('imdb')
		next_episode["year"] = next_info.get('year')

		play_info = {}
		play_info["item_id"] = current_info.get('episodeIDS', {}).get('trakt')

		next_info = {
			"current_episode": current_episode,
			"next_episode": next_episode,
			"play_info": play_info,
			"notification_time": int(control.setting('upnext.time'))
		}
		return next_info


class Subtitles:
	def get(self, name, imdb, season, episode):
		import gzip, StringIO, codecs
		import xmlrpclib, os, re, base64

		try:
			langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}
			codePageDict = {'ara': 'cp1256', 'ar': 'cp1256', 'ell': 'cp1253', 'el': 'cp1253', 'heb': 'cp1255', 'he': 'cp1255', 'tur': 'cp1254', 'tr': 'cp1254', 'rus': 'cp1251', 'ru': 'cp1251'}
			quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
			langs = []

			try:
				try:
					langs = langDict[control.setting('subtitles.lang.1')].split(',')
				except:
					langs.append(langDict[control.setting('subtitles.lang.1')])
			except:
				pass

			try:
				try:
					langs = langs + langDict[control.setting('subtitles.lang.2')].split(',')
				except:
					langs.append(langDict[control.setting('subtitles.lang.2')])
			except:
				pass

			try:
				subLang = xbmc.Player().getSubtitles()
			except:
				subLang = ''

			if subLang == langs[0]:
				raise Exception()

			server = xmlrpclib.Server('https://api.opensubtitles.org/xml-rpc', verbose=0)
			token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')
			token = token['token']
			sublanguageid = ','.join(langs)
			imdbid = re.sub('[^0-9]', '', imdb)

			if not (season is None or episode is None):
				result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid, 'season': season, 'episode': episode}])['data']
				fmt = ['hdtv']
			else:
				result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid}])['data']
				try:
					vidPath = xbmc.Player().getPlayingFile()
				except:
					vidPath = ''
				fmt = re.split('\.|\(|\)|\[|\]|\s|\-', vidPath)
				fmt = [i.lower() for i in fmt]
				fmt = [i for i in fmt if i in quality]

			filter = []
			result = [i for i in result if i['SubSumCD'] == '1']

			for lang in langs:
				filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in fmt)]
				filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in quality)]
				filter += [i for i in result if i['SubLanguageID'] == lang]

			try:
				lang = xbmc.convertLanguage(filter[0]['SubLanguageID'], xbmc.ISO_639_1)
			except:
				lang = filter[0]['SubLanguageID']

			content = [filter[0]['IDSubtitleFile'],]
			content = server.DownloadSubtitles(token, content)
			content = base64.b64decode(content['data'][0]['data'])
			content = gzip.GzipFile(fileobj=StringIO.StringIO(content)).read()

			subtitle = xbmc.translatePath('special://temp/')
			subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)

			codepage = codePageDict.get(lang, '')
			if codepage and control.setting('subtitles.utf') == 'true':
				try:
					content_encoded = codecs.decode(content, codepage)
					content = codecs.encode(content_encoded, 'utf-8')
				except:
					pass

			file = control.openFile(subtitle, 'w')
			file.write(str(content))
			file.close()
			xbmc.sleep(1000)
			xbmc.Player().setSubtitles(subtitle)
		except:
			log_utils.error()
			pass


class Bookmarks:
	def __init__(self):
		self.offset = '0'


	def get(self, name, year='0', ck=False):
		if control.setting('bookmarks') != 'true':
			return self.offset

		idFile = hashlib.md5()

		for i in name:
			idFile.update(str(i))

		for i in year:
			idFile.update(str(i))

		idFile = str(idFile.hexdigest())

		dbcon = database.connect(control.bookmarksFile)
		dbcur = dbcon.cursor()
		dbcur.execute("CREATE TABLE IF NOT EXISTS bookmark (""idFile TEXT, ""timeInSeconds TEXT, ""Name TEXT, ""year TEXT, ""UNIQUE(idFile)"");")
		dbcur.execute("SELECT * FROM bookmark WHERE idFile = '%s'" % idFile)
		match = dbcur.fetchone()
		dbcon.close()

		if match is None:
			return self.offset

		self.offset = str(match[1])

		if ck:
			return self.offset

		minutes, seconds = divmod(float(self.offset), 60)
		hours, minutes = divmod(minutes, 60)

		label = '%02d:%02d:%02d' % (hours, minutes, seconds)
		label = (control.lang(32502) % label).encode('utf-8')

		if control.setting('bookmarks.auto') == 'false':
			yes = control.yesnoDialog(label, '', '', str(name), control.lang(32503).encode('utf-8'), control.lang(32501).encode('utf-8'))

			if yes:
				self.offset = '0'
		return self.offset


	def reset(self, current_time, media_length, name, year='0'):
		if control.setting('bookmarks') != 'true' or media_length == 0 or current_time == 0:
			return

		timeInSeconds = str(current_time)

		ok = (int(current_time) > 180 and (current_time / media_length) <= .92)

		idFile = hashlib.md5()

		for i in name:
			idFile.update(str(i))

		for i in year:
			idFile.update(str(i))

		idFile = str(idFile.hexdigest())

		control.makeFile(control.dataPath)
		dbcon = database.connect(control.bookmarksFile)
		dbcur = dbcon.cursor()
		dbcur.execute("CREATE TABLE IF NOT EXISTS bookmark (""idFile TEXT, ""timeInSeconds TEXT, ""Name TEXT, ""year TEXT, ""UNIQUE(idFile)"");")
		dbcur.execute("DELETE FROM bookmark WHERE idFile = '%s'" % idFile)

		if ok:
			dbcur.execute("INSERT INTO bookmark Values (?, ?, ?, ?)", (idFile, timeInSeconds, name, year))

			minutes, seconds = divmod(float(timeInSeconds), 60)
			hours, minutes = divmod(minutes, 60)

			label = ('%02d:%02d:%02d' % (hours, minutes, seconds)).encode('utf-8')
			message = control.lang(32660).encode('utf-8')

			control.notification(title=name, message=message + '(' + label + ')', icon='INFO', sound=notificationSound)
		dbcur.connection.commit()
		dbcon.close()