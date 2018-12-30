import json
import urllib
import urllib2
import requests
import cookielib
try:
	from dudehere.routines import *
	from dudehere.routines import plugin
	COOKIE_PATH = vfs.join(DATA_PATH,'cookies')
except:
	from lib.dudehere.routines import *

class PremiumizeError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		try:
			s = self.value
		except Exception,e:
			print "-----",type(e),e
		return s


class PremiumizeAPI():
	def __init__(self):
		self.base_url = ' http://http.premiumize.me'
		self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'pl-PL,pl;q=0.8',
			'Connection': 'keep-alive'
		}
		self.boundry = 'X-X-X'
		id = 'script.module.urlresolver'
		urlresolver = xbmcaddon.Addon(id)
		self.username = urlresolver.getSetting('PremiumizeMeResolver_username')
		self.password = urlresolver.getSetting('PremiumizeMeResolver_password')
	
	def check_login(self, username, password):
		self.username = username
		self.password = password
		test = self.list()
		if 'status' in test:
			if test['status'] == 'success':
				return True
		return False
		
	def list(self):
		uri = '/api/transfer/list'
		results = self._call(uri)
		return results
	
	def file_list(self, id=None):
		uri = '/api/folder/list'
		if id is None:
			data = None
		else:	
			data ={"id": id}
		results = self._call(uri, data)
		return results
	
	def browse(self, hash):
		uri = "/api/torrent/browse"
		data = {"hash": hash}
		results = self._call(uri, data)
		return results
	
	def list_file(self, hash):
		results = self.browse(hash)
		if 'content' not in results:
			return [results]
		content = results['content']
		keys = content.keys()
		results = content[keys[0]]
		final = []
		if 'items' in results:
			for child in results['children']:
				data = results['children'][child]
				final += [data]
		else:
			return [results]
		return final
	
	def poll(self):
		results = self.list()
		return results
		
	def check(self, hashes):
		uri = '/api/torrent/checkhashes'
		post_string = "hashes[]=" + "&hashes[]=".join(hashes)
		response = self._call(uri, post_string=post_string)
		return response
	
	def clear(self, hash):
		self.delete_transfer(hash)
		self.delete_file(hash)
	
	def delete_file(self, hash):
		uri = '/api/item/delete'
		data = {"type": "torrent", "id": hash}
		response = self._call(uri, data)
		return response
	
	def delete_transfer(self, hash):
		uri = '/api/transfer/delete'
		data = {"type": "torrent", "id": hash}
		response = self._call(uri, data)
		return response
	
	def abort_transfer(self, hash):
		return self.delete_transfer(hash)
		
	
	def clear_finished(self):
		uri = '/api/transfer/clearfinished'
		results = self._call(uri)
		return results
		
	def queue(self, url, download=False):
		if download:
			from dudehere.routines.transmogrifier import TransmogrifierAPI
			TransmogrifierAPI().queue_torrent(url)
		uri = "/api/transfer/create"
		data = {"type": "torrent", "src": url}
		response = self._call(uri, data)
		return response
		
	def get_stream(self, results):
		content = results['content']
		keys = content.keys()
		results = content[keys[0]]
		if 'items' in results:
			size = 0
			final = {}
			for child in results['children']:
				data = results['children'][child]
				if int(data['size']) > size:
					size = int(data['size'])
					final = data
			url = final['url']
		else:
			url = results['url']
		return url
	
	def upload(self, torrent):
		uri = '/api/transfer/create'
		params = {'type': 'torrent'}
		multipart_data = '--%s\n' % (self.boundry)
		multipart_data += 'Content-Disposition: form-data; name="src"; filename="dummy.torrent"\n'
		multipart_data += 'Content-Type: application/x-bittorrent\n\n'
		multipart_data += torrent
		multipart_data += '\n--%s--\n' % (self.boundry)
		response = self._call(uri, data=params, multipart_data=multipart_data)
		return response
		
	def _call(self, uri, data=None, post_string=None, multipart_data=None):
		url = self.base_url + uri + '?'
		if data is None:
			data = {"customer_id": self.username, "pin": self.password}
		else:
			data["customer_id"] = self.username
			data["pin"] = self.password
		url += urllib.urlencode(data)
		if post_string is not None:
			url += '&' + post_string
		if multipart_data is not None:
			self.headers['Content-Type'] = 'multipart/form-data; boundary=%s' % (self.boundry)
			request = urllib2.Request(url, data=multipart_data, headers=self.headers)
			f = urllib2.urlopen(request)
			results = f.read()
			return json.loads(results)
		else:
			response = requests.get(url, headers=self.headers)
			if response.status_code == requests.codes.ok:
				results = response.json()
				if results['status'] == 'success':
					return results
				else:
					raise PremiumizeError('Premiumize API Error: %s' % results['message'])
			else:
				raise PremiumizeError('Premiumize API Error: %s' % response.status_code)
