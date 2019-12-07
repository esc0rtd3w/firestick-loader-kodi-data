import re
import json
import urllib
import urllib2
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.trakt import TraktAPI


base_url = "http://%s:6544" % plugin.get_setting('mythtv_host')
		
def search(filename):
	trakt = TraktAPI()
	pattern = '\/Default\/([^\/]+)\/.*,\s(\d+_\d+)\.pvr'
	match = re.search(pattern, filename)
	if match:
		title, ts = match.groups()
	else:
		plugin.log(filename)
		return False, False, False, False
	slug = False
	imdb_id = False
	response = _call('/Dvr/GetRecordedList')
	test = ts.replace('_', '')
	for r in response['ProgramList']['Programs']:
		if r['Title'] == title and test in r['FileName']:
			season = int(r['Season'])
			episode = int(r['Episode'])
			tvdb_id = r['Inetref']
			imdb_id = trakt.translate_id(tvdb_id, "tvdb", "imdb", "show")
			break
	if imdb_id:
		uri = '/shows/%s/seasons/%s/episodes/%s' % (imdb_id, season, episode)
		eps = trakt._call(uri, params={}, auth=False, cache_limit=3600)
		if eps:
			trakt_id = eps['ids']['trakt']
			return imdb_id, season, episode, trakt_id
	del trakt
	return False, False, False, False

def mark_watched(trakt_id):
	trakt = TraktAPI()
	response = trakt.set_watched_state('episode', trakt_id, True)
	del trakt

def _call(uri):
	headers = {'Accept': 'application/json'}
	url = base_url + uri
	request = urllib2.Request(url, headers=headers)
	f = urllib2.urlopen(request)
	result = f.read()
	response = json.loads(result)
	return response
