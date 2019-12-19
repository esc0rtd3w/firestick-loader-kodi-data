import sys
import xbmc

if __name__ == '__main__':
	base = 'plugin://plugin.video.openmeta'
	info = sys.listitem.getVideoInfoTag()
	type = info.getMediaType()
	imdb = info.getIMDBNumber()
	if type == 'episode':
		url = '%s/tv/play_by_name_choose_player/%s/%s/%s/en/False' % (base, info.getTVShowTitle(), info.getSeason(), info.getEpisode())
	elif type == 'movie':
		if imdb.startswith('tt'):
			url = '%s/movies/play_choose_player/imdb/%s/False' % (base, imdb)
		else:
			url = '%s/movies/play_by_name_choose_player/%s/en/False' % (base, info.getTitle())
	xbmc.executebuiltin('RunPlugin(%s)' % url)