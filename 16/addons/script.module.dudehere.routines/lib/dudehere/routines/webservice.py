#!/usr/bin/python
from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn
from dudehere.routines.plugin import log

class Server(HTTPServer):
	def get_request(self):
		self.socket.settimeout(5.0)
		result = None
		while result is None:
			try:
				result = self.socket.accept()
			except socket.timeout:
				pass
		result[0].settimeout(1000)
		return result
	
	def _handle_request_noblock(self):
		"""Handle one request, without blocking.

		I assume that select.select has returned that the socket is
		readable before this function was called, so there should be
		no risk of blocking in get_request().
		"""
		try:
			request, client_address = self.get_request()
		except socket.error, e:
			if isinstance(e.args, tuple):
				print "errno is %d" % e[0]
				if e[0] == errno.EPIPE:
					log("Detected remote disconnect")
				else:
					log("Socket error: %s" % e)
			else:
				log("Socket error: %s" % e)
		if self.verify_request(request, client_address):
			try:
				self.process_request(request, client_address)
			except:
				self.handle_error(request, client_address)
				self.shutdown_request(request)

class ThreadedHTTPServer(ThreadingMixIn, Server):
	"""Handle requests in a separate thread."""
