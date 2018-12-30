import json
import urllib
import urllib2
from dudehere.routines import *

class OMDBapi():
	def __init__(self):
		self.base_url = 'http://www.omdbapi.com/?'
		self.search_uri = '/?s=%s&y=%s&type=%s&plot=short&r=json'
	
	def search(self, title, year, media='series'):
		response = self._call(media, title, year)
		if 'Response' in response:
			response = self._call(media, title)
		if 'Response' in response:
			return None
		return response['Search'][0]['imdbID']
		
	def query_id(self, title, year='', media='series'):
		return self.search(title, year, media=media)
		
	def _call(self, media, title, year=''):
		query = {"plot": "short", "r": "json", "s": title, "y": year, "type": media}
		url = self.base_url + urllib.urlencode(query)
		request = urllib2.Request(url)
		f = urllib2.urlopen(request)
		result = f.read()
		response = json.loads(result)
		return response