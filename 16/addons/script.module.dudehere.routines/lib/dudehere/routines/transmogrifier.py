import os
import re
import sys
import urllib
import urllib2
import xbmc
import xbmcgui
import xbmcaddon
import hashlib
import base64
import socket
from dudehere.routines import *
from dudehere.routines import plugin
from urllib2 import URLError, HTTPError
WINDOW_PREFIX = 'transmogrifier'
try: 
	import simplejson as json
except ImportError: 
	import json

def set_property(k, v):
	k = "%s.%s" % (WINDOW_PREFIX, k)
	xbmcgui.Window(10000).setProperty(k, str(v))
	
def get_property(k):
	k = "%s.%s" % (WINDOW_PREFIX, k)
	p = xbmcgui.Window(10000).getProperty(k)
	if p == 'false': return False
	if p == 'true': return True
	return p

def clear_property(k):
	k = "%s.%s" % (WINDOW_PREFIX, k)
	xbmcgui.Window(10000).clearProperty(k)
	
class TransmogrifierAPI:
	def __init__(self):
		self.use_remote_host = xbmcaddon.Addon(id='service.transmogrifier').getSetting('connect_remote') == 'true'
		if self.use_remote_host:
			self.host = xbmcaddon.Addon(id='service.transmogrifier').getSetting('remote_host')
			self.pin = xbmcaddon.Addon(id='service.transmogrifier').getSetting('remote_auth_pin')
			self.token = xbmcaddon.Addon(id='service.transmogrifier').getSetting('remote_auth_token')
			self.port = xbmcaddon.Addon(id='service.transmogrifier').getSetting('remote_control_port')
		else:
			self.host = 'localhost'
			self.pin = xbmcaddon.Addon(id='service.transmogrifier').getSetting('auth_pin')
			self.token = xbmcaddon.Addon(id='service.transmogrifier').getSetting('auth_token')
			self.port = xbmcaddon.Addon(id='service.transmogrifier').getSetting('control_port')
		self.save_directory = xbmcaddon.Addon(id='service.transmogrifier').getSetting('save_directory')
		self._authorize()
		
	def get_progress(self):
		return self._call('progress')
	
	def notify(self, message):
		image = os.path.join(xbmc.translatePath( xbmcaddon.Addon(id='service.transmogrifier').getAddonInfo('path') ), 'icon.png')
		cmd = "XBMC.Notification(TransmogrifierAPI, %s, 1500, %s)" % (message, image)
		xbmc.executebuiltin(cmd)
	
	def _authorize(self):
		if self.token == '':
			response = self._call("authorize")
			if response is False:
				return False
			self.token = response['token']
			if xbmcaddon.Addon(id='service.transmogrifier').getSetting('connect_remote') == 'true':
				xbmcaddon.Addon(id='service.transmogrifier').setSetting('remote_auth_token', self.token)
			else:
				xbmcaddon.Addon(id='service.transmogrifier').setSetting('auth_token', self.token)
		else:
			response = self._call("validate_token")
			if 'success' not in response.keys():
				if xbmcaddon.Addon(id='service.transmogrifier').getSetting('connect_remote') == 'true':
					xbmcaddon.Addon(id='service.transmogrifier').setSetting('remote_auth_token', '')
				else:
					xbmcaddon.Addon(id='service.transmogrifier').setSetting('auth_token', '')
	
	def get_hash(self, video_type, title, season=None, episode=None, year=None):
		if video_type == 'tvshow':
			filename = "%s.S%sE%s" % (title, str(season).zfill(2), str(episode).zfill(2))
		else:
			filename = "%s (%s)" %(title,year)
		return hashlib.md5(video_type+filename).hexdigest()
	
	def get_cached_file(self, title, season=None, episode=None, year=None):
		if season is not None:
			hash = self.get_hash('tvshow', title, season, episode)
			response = self._call('get_path', {"hash": hash})	
			plugin.log(response)
			if 'path' in response and response['path']:
				return {"url": "http://%s:%s/cached/%s" % (self.host, self.port, hash), "path": response['path'], "size": response['size']}
			return False
		else:
			hash = self.get_hash('movie', title, year)
			response = self._call('get_path', {"hash": hash})
			if 'path' in response and response['path']:
				return {"url": "http://%s:%s/cached/%s" % (self.host, self.port, hash), "path": response['path'], "size": response['size']}
			return False
	
	def get_cached_url(self, title=None, season=None, episode=None, year=None, filename=None):
		url = False
		if season is not None:
			hash = self.get_hash('tvshow', title, season, episode)
		elif filename is not None:
			hash = hashlib.md5(filename).hexdigest()
		else:
			hash = self.get_hash('movie', title, year)	
		response = self._call('get_path', {"hash": hash})
		if 'path' in response and response['path'] != '':
			url = "http://%s:%s/cached/%s" % (self.host, self.port, hash)
		return url
	
	def get_streaming_url(self, url, host=None, test_url=False):
		if not url.lower().startswith(("http://", "https://")): return url
		
		try:
			response = self._call('status')
			if response['status'] != 200: 
				print 'TransmogrifierAPI Error: Proxy Host down, restart service?'
				return url
		except:
			print 'TransmogrifierAPI Error: Proxy Host down, restart service?'
			return url
		if host is not None:
			response = self._call('blacklist', {"host": host})
			if response['status'] == 406:
				print 'TransmogrifierAPI Notice: Host [ %s ] is blacklist' % host
				return url
		if test_url:
			test = self.test_url(url, host)
			if not test: return url
		file_id = hashlib.md5(url).hexdigest()
		set_property('streaming', "true")
		set_property('file_id', file_id)
		clear_property('abort_id')
		hash_url = base64.b64encode(url)
		query = {"hash_url": hash_url, "file_id": file_id}
		stream_url = "http://%s:%s/stream/?"  % (self.host, self.port) + urllib.urlencode(query)
		#stream_url = "http://%s:%s/stream/%s/%s" % (self.host, self.port, hash_url, file_id)
		return stream_url
	
	def test_url(self, url, host=None):
		response = self._call('test_url', {"url": url})
		if response is None: return False
		return response['status'] == 200 if 'status' in response else False
	
	def start_buffering(self, url):
		url = url + '?start_buffering=true'
		request = urllib2.Request(url)
		f.read()
		f.close()
	
	def clean_queue(self):
		ok = plugin.dialog_confirm("Clean Queue", "Remove complete and failed?")
		if ok: self._call("clear_queue")
		return ok
	
	def enqueue(self, videos):
		if type(videos) is dict: videos = [videos]
		data = {"videos": videos}
		result = self._call('enqueue', data)
		try:
			if result['status'] == 200:
				self.notify('Successful Enqueue')
			else:
				self.notify('Enqueue Failed, review log for details')
		except:
			self.notify('Enqueue Failed, review log for details')
		return result
	
	def abort(self, file_id):
		return self._call('abort', {"file_id": file_id})
	
	def restart(self, ids):
		if type(ids) is int: ids = [ids]
		data = {"videos": []}
		for id in ids:
			data['videos'].append({"id": id})
		return self._call('restart', data)
	
	def delete(self, ids):
		if type(ids) is int: ids = [ids]
		data = {"videos": []}
		for id in ids:
			data['videos'].append({"id": id})
		return self._call('delete', data)
	
	def queue_torrent(self, url):
		hash = re.search('/torrent/([A-Z0-9]+)\.torrent', url).group(1)
		data = {"hashes": [{"hash": hash}]}
		return self._call('queue_torrent', data)
	
	def change_priority(self, id, priority):
		data = {"videos": [{"id": id, "priority": priority}]}
		return self._call('change_priority', data)
		
	def get_videos(self, media):
		if media == 'tv':
			path = vfs.join(self.save_directory, "TV Shows")
		else:
			path = vfs.join(self.save_directory, "Movies")
		videos = vfs.ls(path, pattern="(avi|mp4|mkv|mov|flv)$")[1]
		return path, videos
	
	def add_file(self, file_hash, path, video_type):
		return self._call("add_file", {"hash_id": file_hash, "path": path, "video_type": video_type})
		
	def get_queue(self):
		return self._call('queue')
	
	def get_poll(self):
		return self._call('poll')
	
	def get_progress(self):
		return self._call('progress')
	
	def _build_url(self):
		url = "http://%s:%s/api.json" % (self.host, self.port)
		return url
	
	def raise_error(self, code, title, message):
		image = vfs.join(ROOT_PATH, 'icon.png')
		plugin.error_message(title, message, image=image)
	
	def _build_request(self, method):
		if method=='authorize':
			request = {"method": method, "pin": self.pin}
		else:
			request = {"method": method, "token": self.token}
		return request
	
	def _call(self, method, data=None):
		
		url = self._build_url()
		request = self._build_request(method)
		if data:
			for key in data.keys():
				request[key] = data[key]
		json_data = json.dumps(request)
		headers = {'Content-Type': 'application/json'}
		try:
			request = urllib2.Request(url, data=json_data, headers=headers)
			f = urllib2.urlopen(request)
			response = f.read()
			return json.loads(response)
		except HTTPError as e:
			plugin.log("TransmogrifierAPI Error: %s" % e, LOG_LEVEL.VERBOSE)
			
		except URLError as e:
			plugin.log("TransmogrifierAPI Error: %s" % e, LOG_LEVEL.VERBOSE)
			self.raise_error(e, "TransmogrifierAPI Error", e)
			return False
		except socket.timeout as e:
			plugin.log("TransmogrifierAPI Error: %s" % e, LOG_LEVEL.VERBOSE)
			self.raise_error(e, "TransmogrifierAPI Error", e)
			return False
