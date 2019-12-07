"""
XBMCLocalProxy 0.1
Copyright 2011 Torben Gerkensmeyer

Modified for Livestreamer by your mom 2k 4 1-N

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import xbmc
import base64
import urlparse
import sys
import socket
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from livestreamer import Livestreamer


class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    """
    Serves a HEAD request
    """
    def do_HEAD(self):
        self.answer_request(0)

    """
    Serves a GET request.
    """
    def do_GET(self):
        self.answer_request(1)

    def answer_request(self, sendData):
        try:
            request_path = self.path[1:]
            if request_path == "stop":
                sys.exit()
            elif request_path == "version":
                self.send_response(200)
                self.end_headers()
                self.wfile.write("Proxy: Running\r\n")
                self.wfile.write("Version: 0.1\r\n")
            elif request_path[0:13] == "livestreamer/":
                realpath = request_path[13:]
                fURL = base64.urlsafe_b64decode(realpath)
                self.serveFile(fURL, sendData)
            else:
                self.send_response(403)
                self.end_headers()
        finally:
                return

    """
    Sends the requested file and add additional headers.
    """
    def serveFile(self, fURL, sendData):
        session = Livestreamer()
        if '|' in fURL:
                sp = fURL.split('|')
                fURL = sp[0]
                headers = dict(urlparse.parse_qsl(sp[1]))
                session.set_option("http-headers", headers)
                session.set_option("http-ssl-verify", False)
                session.set_option("hls-segment-threads", 2)
        try:
            streams = session.streams(fURL)
            self.send_response(200)
        except:
            self.send_response(403)
        finally:
            self.end_headers()

        if (sendData):
            with streams["best"].open() as stream:
                buf = 'INIT'
                while (len(buf) > 0):
                    buf = stream.read(500 * 1024)
                    self.wfile.write(buf)


class Server(HTTPServer):
    """HTTPServer class with timeout."""

    def get_request(self):
        """Get the request and client address from the socket."""
        self.socket.settimeout(5.0)
        result = None
        while result is None:
            try:
                result = self.socket.accept()
            except socket.timeout:
                pass
        result[0].settimeout(1000)
        return result


class ThreadedHTTPServer(ThreadingMixIn, Server):
    """Handle requests in a separate thread."""


HOST_NAME = '127.0.0.1'
PORT_NUMBER = 19001

if __name__ == '__main__':
    sys.stderr = sys.stdout
    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    while not xbmc.abortRequested:
        httpd.handle_request()
    httpd.server_close()
