import sys, xbmc, json

try:
	from urlparse import parse_qsl
except:
	from urllib.parse import parse_qsl

if __name__ == '__main__':
	item = sys.listitem
	message = item.getLabel()
	path = item.getPath()
	plugin = 'plugin://plugin.video.venom/'
	args = path.split(plugin, 1)
	params = dict(parse_qsl(args[1].replace('?', '')))
	name = params['tvshowtitle'] if 'tvshowtitle' in params else params['title']

	if 'meta' in params:
		meta = json.loads(params['meta'])
		imdb = meta.get('imdb', '')
		tvdb = meta.get('tvdb', '')
		season = meta.get('season', '')
		episode = meta.get('episode', '')

	else:
		imdb = params.get('imdb', '')
		tvdb = params.get('tvdb', '')
		season = params.get('season', '')
		episode = params.get('episode', '')

	path = 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&tvdb=%s&season=%s&episode=%s)' % (
				plugin, name, imdb, tvdb, season, episode)
	xbmc.executebuiltin(path)