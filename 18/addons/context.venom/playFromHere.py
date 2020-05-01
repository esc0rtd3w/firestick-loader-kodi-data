import sys, xbmc, json

try:
	from urlparse import parse_qsl
	from urllib import quote_plus
except:
	from urllib.parse import parse_qsl, quote_plus

xbmc.log('__name__= %s' % __name__, 2)
xbmc.log('__package__= %s' % __package__, 2)


# sys.path = []
# if __name__ == '__main__' and __package__ is None:
    # from os import sys, path
    # test = sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    # xbmc.log('test= %s' % test, 2)


if __name__ == '__main__':
	item = sys.listitem
	message = item.getLabel()
	path = item.getPath()
	xbmc.log('path = %s' % path, 2)

	plugin = 'plugin://plugin.video.venom/'
	args = path.split(plugin, 1)
	xbmc.log('args = %s' % args, 2)

	params = dict(parse_qsl(args[1].replace('?', '')))
	xbmc.log('playlist = %s' % len(xbmc.PlayList(xbmc.PLAYLIST_VIDEO)), 2)

	if 'meta' in params:
		meta = json.loads(params['meta'])
		year = meta.get('year', '')
		imdb = meta.get('imdb', '')
		tmdb = meta.get('tmdb', '')
		tvdb = meta.get('tvdb', '')
		season = meta.get('season', '')
		episode = meta.get('episode', '')
		tvshowtitle = meta.get('tvshowtitle', '')

	else:
		year = params.get('year', '')
		imdb = params.get('imdb', '')
		tmdb = params.get('tmdb', '')
		tvdb = params.get('tvdb', '')
		season = params.get('season', '')
		episode = params.get('episode', '')
		tvshowtitle = params.get('tvshowtitle', '')


		# items = seasons.Seasons().tvdb_list(item['tvshowtitle'], item['year'], item['imdb'], item['tmdb'], item['tvdb'], control.apiLanguage()['tvdb'], '-1') # fetch new meta (uncached)

		# for item in items:

	# path = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&season=%s&episode=%s' % (
				# plugin, tvshowtitle, year, imdb, tmdb, tvdb, season, episode)


	# path = 'PlayMedia(%s?action=playAll)' % plugin
	path = 'RunPlugin(%s?action=playAll)' % plugin


	xbmc.executebuiltin(path)
