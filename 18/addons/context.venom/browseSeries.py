import sys, xbmc, json

try:
	from urlparse import parse_qsl
	from urllib import quote_plus
except:
	from urllib.parse import parse_qsl
	from urllib.parse import quote_plus

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
		tvshowtitle = meta.get('tvshowtitle', '').encode('utf-8')
		systvshowtitle = quote_plus(tvshowtitle)

	else:
		year = params.get('year', '')
		imdb = params.get('imdb', '')
		tmdb = params.get('tmdb', '')
		tvdb = params.get('tvdb', '')
		tvshowtitle = params.get('tvshowtitle', '').encode('utf-8')
		systvshowtitle = quote_plus(tvshowtitle)


	xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.venom/?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s,return)' % (systvshowtitle, year, imdb, tmdb, tvdb))
