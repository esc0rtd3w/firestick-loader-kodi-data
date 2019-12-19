import os, shutil
import xbmc, xbmcvfs
from resources.lib import text
from resources.lib import tools
from resources.lib.rpc import RPC
from resources.lib.TheTVDB import TVDB
from resources.lib.xswift2 import plugin


def update_library():
	folder_path = plugin.get_setting('tv_library_folder', unicode)
	if not xbmcvfs.exists(folder_path):
		return
	library_folder = setup_library(folder_path)
	try:
		shows = xbmcvfs.listdir(library_folder)[0]
	except:
		shows = []
	clean_needed = False
	updated = 0
	for id in shows:
		try:
			id = int(id)
			with TVDB.session.cache_disabled():
				if add_tvshow_to_library(library_folder, TVDB[id]):
					clean_needed = True
		except:
			continue
		updated += 1
	if clean_needed:
		plugin.setProperty('plugin.video.openmeta.clean_library', 'true')
	if updated > 0:
		tools.scan_library(path=plugin.get_setting('tv_library_folder', unicode))

def sync_trakt_collection():
	from resources.lib import nav_tvshows
	nav_tvshows.lists_trakt_tv_collection_to_library()

def add_tvshow_to_library(library_folder, show):
	clean_needed = False
	id = show['id']
	showname = text.to_utf8(show['seriesname'])
	if showname == 'None' or showname == None:
		show_folder = os.path.join(library_folder, str(id) + '/')
		if os.path.isdir(show_folder):
			return shutil.rmtree(show_folder)
	enc_show = showname.translate(None, '\/:*?"<>|').strip('.')
	show_folder = os.path.join(library_folder, str(id) + '/')
	if not xbmcvfs.exists(show_folder):
		try:
			xbmcvfs.mkdir(show_folder)
		except:
			pass
		nfo_filepath = os.path.join(show_folder, 'tvshow.nfo')
		if not xbmcvfs.exists(nfo_filepath):
			nfo_file = xbmcvfs.File(nfo_filepath, 'w')
			content = 'http://thetvdb.com/?tab=series&id=%s' % str(id)
			nfo_file.write(content)
			nfo_file.close()
	ids = [id, show.get('imdb_id', None)]
	ids = [x for x in ids if x]
	try:
		libshows = RPC.VideoLibrary.GetTVShows(properties=['imdbnumber', 'title', 'year'])['tvshows']
		libshows = [i for i in libshows if str(i['imdbnumber']) in ids or (str(i['year']) == str(show.get('year', 0)) and text.equals(show['seriesname'], i['title']))]
		libshow = libshows[0]
		libepisodes = RPC.VideoLibrary.GetEpisodes(filter={'and': [ {'field': 'tvshow', 'operator': 'is', 'value': text.to_utf8(libshow['title'])}]}, properties=['season', 'episode', 'file'])['episodes']
		libepisodes = [(int(i['season']), int(i['episode'])) for i in libepisodes if not i['file'].endswith('.strm')]
	except:
		libepisodes = []
	for (season_num,season) in show.items():
		if season_num == 0:
			continue
		for (episode_num, episode) in season.items():
			if episode_num == 0:
				continue
			delete = False
			if not episode.has_aired(flexible=False):
				delete = True
			if delete or (season_num, episode_num) in libepisodes:
				if library_tv_remove_strm(show, show_folder, id, season_num, episode_num):
					clean_needed = True
			else:
				library_tv_strm(show, show_folder, id, season_num, episode_num)
	files, dirs = xbmcvfs.listdir(show_folder)
	if not dirs:
		shutil.rmtree(show_folder)
		clean_needed = True
	return clean_needed

def batch_add_tvshows_to_library(library_folder, show):
	id = show['id']
	showname = text.to_utf8(show['seriesname'])
	show_folder = os.path.join(library_folder, str(id) + '/')
	if not xbmcvfs.exists(show_folder):
		try:
			xbmcvfs.mkdir(show_folder)
		except:
			pass
	nfo_filepath = os.path.join(show_folder, 'tvshow.nfo')
	if not xbmcvfs.exists(nfo_filepath):
		nfo_file = xbmcvfs.File(nfo_filepath, 'w')
		content = 'https://thetvdb.com/?tab=series&id=%s' % str(id)
		nfo_file.write(content)
		nfo_file.close()
	clean_needed = True
	return clean_needed

def library_tv_remove_strm(show, folder, id, season, episode):
	enc_season = ('Season %s' % season).translate(None, '\/:*?"<>|').strip('.')
	enc_name = '%s - S%02dE%02d.strm' % (text.clean_title(show['seriesname']), season, episode)
	season_folder = os.path.join(folder, enc_season)
	stream_file = os.path.join(season_folder, enc_name)
	if xbmcvfs.exists(stream_file):
		xbmcvfs.delete(stream_file)
		while not xbmc.Monitor().abortRequested() and xbmcvfs.exists(stream_file):
			xbmc.sleep(1000)
		a,b = xbmcvfs.listdir(season_folder)
		if not a and not b:
			xbmcvfs.rmdir(season_folder)
		return True
	return False

def library_tv_strm(show, folder, id, season, episode):
	enc_season = ('Season %s' % season).translate(None, '\/:*?"<>|').strip('.')
	folder = os.path.join(folder, enc_season)
	try:
		xbmcvfs.mkdir(folder)
	except:
		pass
	enc_name = '%s - S%02dE%02d.strm' % (text.clean_title(show['seriesname']), season, episode)
	stream = os.path.join(folder, enc_name)
	if not xbmcvfs.exists(stream):
		file = xbmcvfs.File(stream, 'w')
		content = plugin.url_for('tv_play', id=id, season=season, episode=episode)
		file.write(str(content))
		file.close()

def setup_library(library_folder):
	if library_folder[-1] != '/':
		library_folder += '/'
	if not xbmcvfs.exists(library_folder):
		xbmcvfs.mkdir(library_folder)
		msg = 'Would you like to automatically set OpenMeta as a tv shows source?'
		if plugin.yesno('Library setup', msg):
			try:
				source_thumbnail = plugin.get_media_icon('tv')
				source_name = 'OpenMeta TV shows'
				source_content = "('%s','tvshows','metadata.tvdb.com','',0,0,'<settings version=\"2\"><setting id=\"absolutenumber\" default=\"true\">false</setting><setting id=\"alsoimdb\">true</setting><setting id=\"dvdorder\" default=\"true\">false</setting><setting id=\"fallback\">true</setting><setting id=\"fallbacklanguage\">es</setting><setting id=\"fanart\">true</setting><setting id=\"language\" default=\"true\">en</setting><setting id=\"RatingS\" default=\"true\">TheTVDB</setting><setting id=\"usefallbacklanguage1\">true</setting></settings>',0,0,NULL,NULL)" % library_folder
				tools.add_source(source_name, library_folder, source_content, source_thumbnail)
			except:
				pass
	return xbmc.translatePath(library_folder)

def auto_tvshows_setup(library_folder):
	if library_folder[-1] != '/': library_folder += '/'
	try:
		xbmcvfs.mkdir(library_folder)
		source_thumbnail = plugin.get_media_icon('tv')
		source_name = 'OpenMeta TV shows'
		source_content = "('%s','tvshows','metadata.tvdb.com','',0,0,'<settings version=\"2\"><setting id=\"absolutenumber\" default=\"true\">false</setting><setting id=\"alsoimdb\">true</setting><setting id=\"dvdorder\" default=\"true\">false</setting><setting id=\"fallback\">true</setting><setting id=\"fallbacklanguage\">es</setting><setting id=\"fanart\">true</setting><setting id=\"language\" default=\"true\">en</setting><setting id=\"RatingS\" default=\"true\">TheTVDB</setting><setting id=\"usefallbacklanguage1\">true</setting></settings>',0,0,NULL,NULL)" % library_folder
		tools.add_source(source_name, library_folder, source_content, source_thumbnail)
		return True
	except:
		False