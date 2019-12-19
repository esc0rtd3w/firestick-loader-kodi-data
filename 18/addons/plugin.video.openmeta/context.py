import sys
import xbmc

if __name__ == '__main__':
	base = 'plugin://plugin.video.openmeta'
	info = sys.listitem.getVideoInfoTag()
	type = info.getMediaType()
	imdb = info.getIMDBNumber()
	if type == 'episode':
		url = '%s/tv/play_by_name/%s/%s/%s/en' % (base, info.getTVShowTitle(), info.getSeason(), info.getEpisode())
	elif type == 'movie':
		if imdb.startswith('tt'):
			url = '%s/movies/play/imdb/%s' % (base, imdb)
		else:
			url = '%s/movies/play_by_name/%s/en' % (base, info.getTitle())
	xbmc.executebuiltin('RunPlugin(%s)' % url)