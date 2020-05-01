import sys, xbmc, json

try:
	from urlparse import parse_qsl
	from urllib import quote_plus
except:
	from urllib.parse import parse_qsl, quote_plus

if __name__ == '__main__':
	item = sys.listitem
	message = item.getLabel()
	path = item.getPath()
	plugin = 'plugin://plugin.video.venom/'
	args = path.split(plugin, 1)
	# xbmc.log('args = %s' % args, 2)
	params = dict(parse_qsl(args[1].replace('?', '')))

	if 'meta' in params:
		meta = json.loads(params['meta'])
		year = meta.get('year', '')
		imdb = meta.get('imdb', '')
		tmdb = meta.get('tmdb', '')
		tvdb = meta.get('tvdb', '')
		season = meta.get('season', '')
		episode = meta.get('episode', '')
		tvshowtitle = meta.get('tvshowtitle', '').encode('utf-8')
		systvshowtitle = quote_plus(tvshowtitle)

	else:
		year = params.get('year', '')
		imdb = params.get('imdb', '')
		tmdb = params.get('tmdb', '')
		tvdb = params.get('tvdb', '')
		season = params.get('season', '')
		episode = params.get('episode', '')
		tvshowtitle = params.get('tvshowtitle', '').encode('utf-8')
		systvshowtitle = quote_plus(tvshowtitle)


# to browse by Progress
	xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.venom/?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&season=%s&episode=%s,return)' % (systvshowtitle, year, imdb, tmdb, tvdb, season, episode))

# # to browse full episode list
	# xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.venom/?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&season=%s,return)' % (systvshowtitle, year, imdb, tmdb, tvdb, season))
