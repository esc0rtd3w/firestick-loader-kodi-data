import json
import sys
import cgi
import re
import socket
import os
from os import curdir, sep
from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.dispatcher import FunctionDispatcher
from dudehere.routines.scrapers import ScraperPool
from dudehere.routines import fanart
from dudehere.routines.trakt import DB as TraktDB
from dudehere.routines.trakt import TraktAPI
fanart.DB=TraktDB
fanart.trakt = TraktAPI()

HOST_ADDRESS = socket.gethostname()
LOG_FILE = vfs.join(DATA_PATH, 'access.log')
plugin.log("Setting DHCR API Access log to: %s" % LOG_FILE)

from httplib2 import Response
class RequestHandler(BaseHTTPRequestHandler):
	kodi_disconnect = False
	log_file = vfs.open(LOG_FILE, 'w')
	
	def process_cgi(self):
		parts = urlparse(self.path)
		path = parts.path
		query = parts.query
		data = cgi.parse_qs(query, keep_blank_values=True)
		arguments = path.split('/')
		return arguments, data, path

	def finish(self,*args,**kw):
		try:
			if not self.wfile.closed:
				self.wfile.flush()
				self.wfile.close()
		except socket.error:
			pass
		self.rfile.close()
	
	def handle(self):
		"""Handles a request ignoring dropped connections."""
		try:
			return BaseHTTPRequestHandler.handle(self)
		except (socket.error, socket.timeout) as e:
			self.connection_dropped(e)

	def connection_dropped(self, error, environ=None):
		self.kodi_disconnect = True
		plugin.log("Kodi disconnected")

	def log_message(self, format, *args):
		self.log_file.write("%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format % args))
	
	def _send_response(self, content, code=200, mime="application/json", headers=None):
		self.send_response(code)
		self.send_header('Content-type',	mime)
		if headers is not None:
			for header_type, header in headers:
				self.send_header(header_type, header)
		self.end_headers()
		if mime == 'application/json':
			content = json.dumps(content)
		self.wfile.write(content)
		self.wfile.flush()

	def generate_respose_headers(self, file_name=None):
		self._response_headers = {}
		now = datetime.datetime.utcnow()
		self._response_headers['Date'] = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
		self._response_headers['Server'] = 'Transmogrifier'
		self._response_headers['Last-Modified'] = "Wed, 21 Feb 2000 08:43:39 GMT"
		self._response_headers['ETag'] = get_property("streaming.file_id")
		self._response_headers['Accept-Ranges'] = 'bytes'
		self._response_headers['Content-Length'] = '0'
		self._response_headers['Range'] = '0-'
		self._response_headers['Content-Type'] = "application/octet-stream"	
		if file_name is not None:
			self._response_headers['Content-Disposition'] = "attachment; filename=\"%s\";" % file_name
	
	def set_range_header(self, start_byte, total_bytes):
		if start_byte == 0:
			self._response_headers['Content-Length'] = total_bytes
			self._response_headers['Range'] = '0-'
		else:
			last_byte = total_bytes - 1
			self._response_headers['Range'] = "%s-%s" % (start_byte, last_byte)
			self._response_headers['Content-Range'] = "%s-%s/%s" % (start_byte, last_byte, total_bytes)
			self._response_headers['Content-Length'] = str(total_bytes - start_byte)
		
	def send_all_headers(self):
		self.send_response(206)
		for header in self._response_headers:
			self.send_header(header, str(self._response_headers[header]))
		self.end_headers()
		
		

	def do_HEAD(self):
		arguments, data, path = self.process_cgi()
	
	def send_error(self, code, message):	
		self.do_Response({'status': code, 'message': message})
		
	def do_GET(self):
		arguments, data, path = self.process_cgi()
		dispatcher = FunctionDispatcher()
		
		def send_error():
			self.send_error(500,'Internal Server Error')
		
		def send_redirect(url):
			if url:
				self.send_response(302)
				self.send_header('Location', url)
				self.end_headers()
				self.wfile.flush()
			else:
				self.send_error(404,'File not found')
			return False	

		dispatcher.error = send_error

		@dispatcher.register('default')
		def default():
			self.send_error(400,'Bad Request')
		
		@dispatcher.register('/api/search')
		def search():
			results = []
			media = data['media'][0] if 'media' in data else ''
			title = data['title'][0] if 'title' in data else ''
			year = data['year'][0] if 'year' in data else ''
			season = data['season'][0] if 'season' in data else ''
			episode = data['episode'][0] if 'episode' in data else ''
			imdb_id = data['imdb_id'][0] if 'imdb_id' in data else ''

			Scraper = ScraperPool(load='all', cache_results=False, skip_states=True)
			Scraper.threadpool_size = 30
			if media == 'show':
				if not title or not season or not episode:
					self.send_error(400,'Bad Request')
					return
				sources, raw_urls, raw_results = Scraper.search_tvshows(title, season, episode, year, imdb_id, return_sources=True)
			elif media == 'movie':
				if not title or not year:
					self.send_error(400,'Bad Request')
					return
				sources, raw_urls, raw_results = Scraper.search_movies(title, year, imdb_id, return_sources=True)
			else:
				self.send_error(400,'Bad Request')
				return
			
			for result in raw_results:
				try:
					r = {
						"service": result.service,
						"host": result.hostname,
						"file": result.text,
						"url": result.url,
						"bitrate": result.bitrate,
						"filesize": result.size,
						"extension": result.extension,
						"quality":	result.quality,
						"x265": result.x265
						}
					results.append(r)
				except:
					pass	
			self.do_Response({'status': 200, 'message': 'success', 'results': results})
		
		@dispatcher.register('/api/images/movie')
		def movie_images():
			image = data['image'][0] if 'image' in data else ''
			trakt_id = data['trakt_id'][0] if 'trakt_id' in data else None
			art = fanart.get_movie_art(trakt_id)
			try:
				url = art[image]
			except:
				url = False
			send_redirect(url)
		
		@dispatcher.register('/api/images/show')
		def show_images():
			image = data['image'][0] if 'image' in data else ''
			trakt_id = data['trakt_id'][0] if 'trakt_id' in data else None
			art = fanart.get_show_art(trakt_id)
			try:
				url = art[image]
			except:
				url = False
			send_redirect(url)
	
		@dispatcher.register('/api/images/episode')
		def episode_images():
			trakt_id = data['trakt_id'][0] if 'trakt_id' in data else None
			url = fanart.get_episode_art(trakt_id)
			send_redirect(url)
			
		@dispatcher.register('/api/images/season')
		def season_images():
			tvdb_id = data['tvdb_id'][0] if 'tvdb_id' in data else None
			season = int(data['season'][0]) if 'season' in data else ''
			url = fanart.get_season_poster(tvdb_id, season)
			send_redirect(url)
			
		@dispatcher.register('/api/images/person')
		def person_image():
			tmdb_id = data['tmdb_id'][0] if 'tmdb_id' in data else None
			url = fanart.get_person_art(tmdb_id)
			send_redirect(url)	
			
		dispatcher.run(path)
		
	def do_POST(self):
		arguments, data, path = self.process_cgi()
		dispatcher = FunctionDispatcher()
		def send_error():
			self.send_error(500,'Internal Server Error')
		dispatcher.error = send_error	
		
			
	def do_Response(self, content={'status': 200, 'message': 'success'}, content_type='application/json', response=200):
		self.send_response(response)
		self.send_header('Content-type',	content_type)
		self.end_headers()
		if content_type == 'application/json':
			content['host'] = HOST_ADDRESS
			content = json.dumps(content)
		self.wfile.write(content)
		self.wfile.flush()
		self.wfile.close()