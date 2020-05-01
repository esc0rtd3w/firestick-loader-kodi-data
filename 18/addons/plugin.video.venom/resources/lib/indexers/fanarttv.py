# -*- coding: utf-8 -*-

'''
	Venom Add-on
'''

import requests

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils


user = control.setting('fanart.tv.user')
if user == '' or user is None:
	user = 'cf0ebcc2f7b824bd04cf3a318f15c17d'

headers = {'api-key': '9f846e7ec1ea94fad5d8a431d1d26b43'}
if user != '':
	headers.update({'client-key': user})

base_url = "http://webservice.fanart.tv/v3/%s/%s"
lang = control.apiLanguage()['trakt']
error_codes = ['500 Internal Server Error', '502 Bad Gateway', '504 Gateway Timeout']


def get_request(url):
	try:
		try:
			result = requests.get(url, headers=headers, timeout=5)
		except requests.exceptions.SSLError:
			result = requests.get(url, headers=headers, verify=False)
	except requests.exceptions.ConnectionError:
		control.notification(title='default', message='FANART.TV server Problems')
		log_utils.error()
		return None

	if '200' in str(result):
		if '/tt' in url:
			log_utils.log('requests.get() found - FANART.TV URL: %s (FOUND in IMDB)' % url, log_utils.LOGDEBUG)
		return result.json() 

	elif 'Not found' in str(result.text):
		log_utils.log('requests.get() failed - FANART.TV URL: %s (NOT FOUND)' % url, log_utils.LOGDEBUG)
		return None

	else:
		title = client.parseDOM(result.text, 'title')[0]
		log_utils.log('requests.get() failed - FANART.TV URL: %s (%s)' % (url, title), log_utils.LOGDEBUG)
		return None


def get_movie_art(imdb, tmdb):
	url = base_url % ('movies', tmdb)
	art = get_request(url)

	if art is None:
		url = base_url % ('movies', imdb)
		art = get_request(url)

	if art is None:
		return None

	try:
		if 'movieposter' not in art: raise Exception()
		poster2 = art['movieposter']
		# poster2 = [(x['url'], x['likes']) for x in poster2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in poster2 if x.get('lang') == ''] + [(x['url'], x['likes']) for x in poster2 if x.get('lang') == '00']
		poster2 = [(x['url'], x['likes']) for x in poster2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in poster2 if x.get('lang') == '']
		poster2 = [(x[0], x[1]) for x in poster2]
		poster2 = sorted(poster2, key=lambda x: int(x[1]), reverse=True)
		poster2 = [x[0] for x in poster2][0]
	except:
		poster2 = '0'

	try:
		if 'moviebackground' in art:
			fanart2 = art['moviebackground']
		else:
			if 'moviethumb' not in art: raise Exception()
			fanart2 = art['moviethumb']
		fanart2 = [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == '']
		fanart2 = [(x[0], x[1]) for x in fanart2]
		fanart2 = sorted(fanart2, key=lambda x: int(x[1]), reverse=True)
		fanart2 = [x[0] for x in fanart2][0]
	except:
		fanart2 = '0'

	try:
		if 'moviebanner' not in art: raise Exception()
		banner2 = art['moviebanner']
		banner2 = [(x['url'], x['likes']) for x in banner2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in banner2 if x.get('lang') == '']
		banner2 = [(x[0], x[1]) for x in banner2]
		banner2 = sorted(banner2, key=lambda x: int(x[1]), reverse=True)
		banner2 = [x[0] for x in banner2][0]
	except:
		banner2 = '0'

	try:
		if 'hdmovielogo' in art:
			clearlogo = art['hdmovielogo']
		else:
			if 'movielogo' not in art: raise Exception()
			clearlogo = art['movielogo']
		clearlogo = [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == lang] + [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == '']
		clearlogo = [(x[0], x[1]) for x in clearlogo]
		clearlogo = sorted(clearlogo, key=lambda x: int(x[1]), reverse=True)
		clearlogo = [x[0] for x in clearlogo][0]
	except:
		clearlogo = '0'

	try:
		if 'hdmovieclearart' in art:
			clearart = art['hdmovieclearart']
		else:
			if 'movieart' not in art: raise Exception()
			clearart = art['movieart']
		clearart = [(x['url'], x['likes']) for x in clearart if x.get('lang') == lang] + [(x['url'], x['likes']) for x in clearart if x.get('lang') == '']
		clearart = [(x[0], x[1]) for x in clearart]
		clearart = sorted(clearart, key=lambda x: int(x[1]), reverse=True)
		clearart = [x[0] for x in clearart][0]
	except:
		clearart = '0'

	try:
		if 'moviedisc' not in art: raise Exception()
		discart = art['moviedisc']
		discart = [(x['url'], x['likes']) for x in discart if x.get('lang') == lang] + [(x['url'], x['likes']) for x in discart if x.get('lang') == '']
		discart = [(x[0], x[1]) for x in discart]
		discart = sorted(discart, key=lambda x: int(x[1]), reverse=True)
		discart = [x[0] for x in discart][0]
	except:
		discart = '0'

	try:
		if 'moviethumb' in art:
			landscape = art['moviethumb']
		else:
			if 'moviebackground' not in art: raise Exception()
			landscape = art['moviebackground']
		landscape = [(x['url'], x['likes']) for x in landscape if x.get('lang') == lang] + [(x['url'], x['likes']) for x in landscape if x.get('lang') == '']
		landscape = [(x[0], x[1]) for x in landscape]
		landscape = sorted(landscape, key=lambda x: int(x[1]), reverse=True)
		landscape = [x[0] for x in landscape][0]
	except:
		landscape = '0'

	# try:
		# keyart = art['movieposter']
		# keyart = [(x['url'], x['likes']) for x in keyart if x.get('lang') in ['00', 'None', None]]
		# keyart = [(x[0], x[1]) for x in keyart]
		# keyart = sorted(keyart, key=lambda x: int(x[1]), reverse=True)
		# keyart = [x[0] for x in keyart][0]
	# except:
		# keyart = '0'

	extended_art = {'extended': True, 'poster2': poster2, 'fanart2': fanart2, 'banner2': banner2, 'clearlogo': clearlogo, 'clearart': clearart, 'discart': discart, 'landscape': landscape}
	# extended_art = {'extended': True, 'poster2': poster2, 'fanart2': fanart2, 'banner2': banner2, 'clearlogo': clearlogo, 'clearart': clearart, 'discart': discart, 'landscape': landscape, 'keyart': keyart}
	return extended_art


def get_tvshow_art(tvdb):
	if tvdb == '0':
		return None

	url = base_url % ('tv', tvdb)
	art = get_request(url)

	if art is None:
		return None

	try:
		if 'tvposter' not in art: raise Exception()
		poster2 = art['tvposter']
		poster2 = [(x['url'], x['likes']) for x in poster2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in poster2 if x.get('lang') == ''] + [(x['url'], x['likes']) for x in poster2 if x.get('lang') == '00']
		poster2 = [(x[0], x[1]) for x in poster2]
		poster2 = sorted(poster2, key=lambda x: int(x[1]), reverse=True)
		poster2 = [x[0] for x in poster2][0]
	except:
		poster2 = '0'

	try:
		if 'showbackground' not in art: raise Exception()
		fanart2 = art['showbackground']
		fanart2 = [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == ''] + [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == '00']
		fanart2 = [(x[0], x[1]) for x in fanart2]
		fanart2 = sorted(fanart2, key=lambda x: int(x[1]), reverse=True)
		fanart2 = [x[0] for x in fanart2][0]
	except:
		fanart2= '0'

	try:
		if 'tvbanner' not in art: raise Exception()
		banner2 = art['tvbanner']
		banner2 = [(x['url'], x['likes']) for x in banner2 if x.get('lang') == lang] + [(x['url'], x['likes']) for x in banner2 if x.get('lang') == ''] + [(x['url'], x['likes']) for x in banner2 if x.get('lang') == '00']
		banner2 = [(x[0], x[1]) for x in banner2]
		banner2 = sorted(banner2, key=lambda x: int(x[1]), reverse=True)
		banner2 = [x[0] for x in banner2][0]
	except:
		banner2 = '0'

	try:
		if 'hdtvlogo' in art:
			clearlogo = art['hdtvlogo']
		else:
			if 'clearlogo' not in art: raise Exception()
			clearlogo = art['clearlogo']
		clearlogo = [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == lang] + [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == ''] + [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == '00']
		clearlogo = [(x[0], x[1]) for x in clearlogo]
		clearlogo = sorted(clearlogo, key=lambda x: int(x[1]), reverse=True)
		clearlogo = [x[0] for x in clearlogo][0]
	except:
		clearlogo = '0'

	try:
		if 'hdclearart' in art:
			clearart = art['hdclearart']
		else:
			if 'clearart' not in art: raise Exception()
			clearart = art['clearart']
		clearart = [(x['url'], x['likes']) for x in clearart if x.get('lang') == lang] + [(x['url'], x['likes']) for x in clearart if x.get('lang') == ''] + [(x['url'], x['likes']) for x in clearart if x.get('lang') == '00']
		clearart = [(x[0], x[1]) for x in clearart]
		clearart = sorted(clearart, key=lambda x: int(x[1]), reverse=True)
		clearart = [x[0] for x in clearart][0]
	except:
		clearart = '0'

	try:
		if 'tvthumb' in art:
			landscape = art['tvthumb']
		else:
			if 'showbackground' not in art: raise Exception()
			landscape = art['showbackground']
		landscape = [(x['url'], x['likes']) for x in landscape if x.get('lang') == lang] + [(x['url'], x['likes']) for x in landscape if x.get('lang') == ''] + [(x['url'], x['likes']) for x in landscape if x.get('lang') == '00']
		landscape = [(x[0], x[1]) for x in landscape]
		landscape = sorted(landscape, key=lambda x: int(x[1]), reverse=True)
		landscape = [x[0] for x in landscape][0]
	except:
		landscape = '0'

	extended_art = {'extended': True, 'poster2': poster2, 'banner2': banner2, 'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape}
	return extended_art
