# -*- coding: utf8 -*-
import threading
import time
import StringIO
import re
import struct
import cherrypy
from cherrypy import wsgiserver
from cherrypy.process import servers
from datetime import datetime
import random
import sys
import platform
import logging
import os
from utils import log_msg
import xbmc


class HTTPProxyError(Exception):
    pass


class Track:
    __is_playing = None
    __allowed_ips = None
    __allow_ranges = None

    def __init__(self, allowed_ips, allow_ranges=True):
        self.__allowed_ips = allowed_ips
        self.__is_playing = False
        self.__allow_ranges = allow_ranges

    def _get_wave_header(self, duration):
        '''generate a wave header for our silence stream'''
        file = StringIO.StringIO()

        # always add 2 seconds of additional duration to solve crossfade issues
        duration += 2
        numsamples = 44100 * duration
        channels = 2
        samplerate = 44100
        bitspersample = 16

        # Generate format chunk
        format_chunk_spec = "<4sLHHLLHH"
        format_chunk = struct.pack(
            format_chunk_spec,
            "fmt ",  # Chunk id
            16,  # Size of this chunk (excluding chunk id and this field)
            1,  # Audio format, 1 for PCM
            channels,  # Number of channels
            samplerate,  # Samplerate, 44100, 48000, etc.
            samplerate * channels * (bitspersample / 8),  # Byterate
            channels * (bitspersample / 8),  # Blockalign
            bitspersample,  # 16 bits for two byte samples, etc.
        )
        # Generate data chunk
        data_chunk_spec = "<4sL"
        datasize = numsamples * channels * (bitspersample / 8)
        data_chunk = struct.pack(
            data_chunk_spec,
            "data",  # Chunk id
            int(datasize),  # Chunk size (excluding chunk id and this field)
        )
        sum_items = [
            #"WAVE" string following size field
            4,
            #"fmt " + chunk size field + chunk size
            struct.calcsize(format_chunk_spec),
            # Size of data chunk spec + data size
            struct.calcsize(data_chunk_spec) + datasize
        ]
        # Generate main header
        all_cunks_size = int(sum(sum_items))
        main_header_spec = "<4sL4s"
        main_header = struct.pack(
            main_header_spec,
            "RIFF",
            all_cunks_size,
            "WAVE"
        )
        # Write all the contents in
        file.write(main_header)
        file.write(format_chunk)
        file.write(data_chunk)

        return file.getvalue(), all_cunks_size + 8

    def send_audio_stream(self, filesize, wave_header=None, max_buffer_size=8196):

        # Initialize some loop vars
        output_buffer = StringIO.StringIO()
        bytes_written = 0
        has_frames = True

        # Write wave header
        if wave_header is not None:
            output_buffer.write(wave_header)
            bytes_written = output_buffer.tell()
            yield wave_header
            output_buffer.truncate(0)
            
        # this is where we would/could normally stream packets from an audio input
        # In this case we stream only silence until the end is reached
        while bytes_written < filesize:

            # The buffer size fits into the file size
            if bytes_written + max_buffer_size < filesize:
                yield '\0' * max_buffer_size
                bytes_written += max_buffer_size

            # Does not fit, just generate the remaining bytes
            else:
                yield '\0' * (filesize - bytes_written)
                bytes_written = filesize

    def _check_request(self):
        method = cherrypy.request.method.upper()
        headers = cherrypy.request.headers

        # Fail for other methods than get or head
        if method not in ("GET", "HEAD"):
            raise cherrypy.HTTPError(405)

        # Error if the requester is not allowed
        if headers['Remote-Addr'] not in self.__allowed_ips:
            raise cherrypy.HTTPError(403)

        return method

    @cherrypy.expose
    def default(self, track_id, **kwargs):
        # Check sanity of the request
        self._check_request()

        # get duration from track id
        is_radio = False
        try:
            duration = int(track_id)
        except:
            is_radio = True
            duration = 3600

        # Calculate file size, and obtain the header
        file_header, filesize = self._get_wave_header(duration)

        # headers
        if is_radio:
            cherrypy.response.headers['Content-Type'] = 'audio/x-wav'
            cherrypy.response.headers['Connection'] = 'close'
            #cherrypy.response.headers['Transfer-Encoding'] = 'chunked'
        elif cherrypy.request.headers.get('Range', '') == "bytes=0-":
            cherrypy.response.status = '206 Partial Content'
            cherrypy.response.headers['Content-Type'] = 'audio/x-wav'
            cherrypy.response.headers['Accept-Ranges'] = 'bytes'
            cherrypy.response.headers['Content-Length'] = filesize
            cherrypy.response.headers['Content-Range'] = "bytes 0-%s/%s" % (filesize, filesize)
        elif cherrypy.request.headers.get('Range'):
            # partial request
            cherrypy.response.status = '206 Partial Content'
            cherrypy.response.headers['Content-Type'] = 'audio/x-wav'
            range = cherrypy.request.headers["Range"].split("bytes=")[1].split("-")
            range_l = int(range[0])
            try:
                range_r = int(range[1])
            except:
                range_r = filesize
            chunk = range_r - range_l
            cherrypy.response.headers['Accept-Ranges'] = 'bytes'
            cherrypy.response.headers['Content-Length'] = chunk
            cherrypy.response.headers['Content-Range'] = "bytes %s-%s/%s" % (range_l, range_r, filesize)
            filesize = chunk
        else:
            cherrypy.response.status = '200 OK'
            cherrypy.response.headers['Content-Type'] = 'audio/x-wav'
            cherrypy.response.headers['Content-Length'] = filesize

        # If method was GET, write the file content
        if cherrypy.request.method.upper() == 'GET':
            return self.send_audio_stream(filesize, file_header)

    default._cp_config = {'response.stream': True}


class Root:
    track = None

    def __init__(self, allowed_ips, allow_ranges=True):
        self.track = Track(
            allowed_ips, allow_ranges
        )

    def cleanup(self):
        self.__session = None
        self.track = None


class ProxyRunner(threading.Thread):
    __server = None
    __base_token = None
    __allowed_ips = None
    __cb_stream_ended = None
    __root = None

    def _find_free_port(self, host, port_list):
        '''find a free tcp port we can use for our webserver'''
        for port in port_list:
            try:
                servers.check_port(host, port, .1)
                return port
            except:
                pass
        list_str = ','.join([str(item) for item in port_list])
        raise HTTPProxyError("Cannot find a free port. Tried: %s" % list_str)

    def __init__(self, host='localhost', try_ports=range(51100, 51150), allowed_ips=['127.0.0.1'], allow_ranges=True):
        port = self._find_free_port(host, try_ports)
        self.__allowed_ips = allowed_ips
        self.__root = Root(
            self.__allowed_ips, allow_ranges
        )
        app = cherrypy.tree.mount(self.__root, '/')
        log = cherrypy.log
        log.access_file = ''
        log.error_file = ''
        log.screen = True

        self.__server = wsgiserver.CherryPyWSGIServer((host, port), app)
        threading.Thread.__init__(self)

    def run(self):
        self.__server.start()

    def get_port(self):
        return self.__server.bind_addr[1]

    def get_host(self):
        return self.__server.bind_addr[0]

    def ready_wait(self):
        while not self.__server.ready:
            time.sleep(.1)

    def stop(self):
        self.__server.stop()
        self.join(1)
        self.__root.cleanup()
