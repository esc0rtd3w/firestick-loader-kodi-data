"""
XBMCLocalProxy 0.1
Copyright 2011 Torben Gerkensmeyer

Modified for Livestreamer by your mom 2k15

Modified for StreamLink by your dad 2k18

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

import xbmc, xbmcgui
import base64
import urlparse,urllib
import sys, traceback, os, errno
import thread, threading
import socket
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import struct
import streamlink
from streamlink.exceptions import StreamError, PluginError, NoPluginError
from urlparse import urljoin


##aes stuff - custom crypto implementation
_android_ssl = False
_oscrypto = False
_dec = False
_crypto = 'None'

try:
    from Cryptodome.Cipher import AES
    _dec = True
    _crypto = 'CryptoDome'
except ImportError:
    try:
        import androidsslPy
        enc = androidsslPy._load_crypto_libcrypto()
        _android_ssl = True
        _dec = True
        _crypto = 'androidsslPy'
    except:
        try:
            from oscrypto.symmetric import aes_cbc_no_padding_decrypt
            class AES(object):
                def __init__(self,key,iv):
                    self.key=key
                    self.iv=iv
                def decrypt(self, data):
                    return aes_cbc_no_padding_decrypt(self.key, data, self.iv)
            _oscrypto = True
            _dec = True
            _crypto = 'OSCrypto' 
        except:
            try:
                from Crypto.Cipher import AES
                _dec = True
            except ImportError:
                _dec = False


def num_to_iv(n):
    return struct.pack(">8xq", n)

## override SL decryptor functions
def create_decryptor(self, key, sequence):
    if key.method != "AES-128":
        raise StreamError("Unable to decrypt cipher {0}", key.method)

    if not key.uri:
        raise StreamError("Missing URI to decryption key")

    if self.key_uri != key.uri:
        zoom_key = self.reader.stream.session.options.get("zoom-key")
        zuom_key = self.reader.stream.session.options.get("zuom-key")
        livecam_key = self.reader.stream.session.options.get("livecam-key")
        saw_key = self.reader.stream.session.options.get("saw-key")
        your_key = self.reader.stream.session.options.get("your-key")
        mama_key = self.reader.stream.session.options.get("mama-key")
        custom_uri = self.reader.stream.session.options.get("custom-uri")

        if zoom_key:
            uri = 'http://www.zoomtv.me/k.php?q='+base64.urlsafe_b64encode(zoom_key+base64.urlsafe_b64encode(key.uri))
        elif zuom_key:
            uri = 'http://www.zuom.xyz/k.php?q='+base64.urlsafe_b64encode(zuom_key+base64.urlsafe_b64encode(key.uri))
        elif livecam_key:           
            h = urlparse.urlparse(urllib.unquote(livecam_key)).netloc
            q = urlparse.urlparse(urllib.unquote(livecam_key)).query            
            uri = 'http://%s/kaes?q='%h+base64.urlsafe_b64encode(q+base64.b64encode(key.uri))
        elif saw_key:
            if 'foxsportsgo' in key.uri:
                _tmp = key.uri.split('/')
                uri = urljoin(saw_key,'/m/fream?p='+_tmp[-4]+'&k='+_tmp[-1])
            elif 'nlsk.neulion' in key.uri:
                _tmp = key.uri.split('?')
                uri = urljoin(saw_key,'/m/stream?'+_tmp[-1])
            elif 'nlsk' in key.uri:
                _tmp = key.uri.split('?')
                uri = 'http://bile.level303.club/m/stream?'+_tmp[-1]
            elif 'nhl.com' in key.uri:
                _tmp = key.uri.split('/')
                uri = urljoin(saw_key,'/m/streams?ci='+_tmp[-3]+'&k='+_tmp[-1])
            else:
                uri = key.uri
        elif mama_key:
           if 'nlsk' in key.uri:
                _tmp = key.uri.split('&url=')
                uri = 'http://mamahd.in/nba?url=' + _tmp[-1]
        elif your_key:
            if 'mlb.com' in key.uri:
                _tmp = key.uri.split('?')
                uri = urljoin(your_key,'/mlb/get_key/'+_tmp[-1])
            elif 'espn3/auth' in key.uri:
                _tmp = key.uri.split('?')
                uri = urljoin(your_key,'/ncaa/get_key/'+_tmp[-1])
            elif 'nhl.com' in key.uri:
                _tmp = key.uri.split('nhl.com/')
                uri = urljoin(your_key,'/nhl/get_key/'+_tmp[-1])
            else:
                uri = key.uri
        elif custom_uri:
            uri = custom_uri

        else:
            uri = key.uri

        #xbmc.log('[StreamLink_Proxy] using key uri %s'%str(uri))

        res = self.session.http.get(uri, exception=StreamError,
                                    retries=self.retries,
                                    **self.reader.request_params)

        self.key_data = res.content
        self.key_uri = key.uri

    iv = key.iv or num_to_iv(sequence)

    # Pad IV if needed
    iv = b"\x00" * (16 - len(iv)) + iv

    if _android_ssl:
        return enc(self.key_data, iv)
    elif _oscrypto:
        return AES(self.key_data, iv)
    else:
        return AES.new(self.key_data, AES.MODE_CBC, iv)


def process_sequences(self, playlist, sequences):    
    first_sequence, last_sequence = sequences[0], sequences[-1]
    #log.debug("process_sequences: %s"%len(sequences))

    if first_sequence.segment.key and first_sequence.segment.key.method != "NONE":
        xbmc.log('[StreamLink_Proxy] Segments in this playlist are encrypted.')

    self.playlist_changed = ([s.num for s in self.playlist_sequences] !=
                                [s.num for s in sequences])
    self.playlist_reload_time = (playlist.target_duration or
                                    last_sequence.segment.duration)
    self.playlist_sequences = sequences

    if not self.playlist_changed:
        self.playlist_reload_time = max(self.playlist_reload_time / 2, 1)

    if playlist.is_endlist:
        self.playlist_end = last_sequence.num

    if self.playlist_sequence < 0:
        if self.playlist_end is None and not self.hls_live_restart:
            edge_index = -(min(len(sequences), max(int(self.live_edge), 1)))
            edge_sequence = sequences[edge_index]
            self.playlist_sequence = edge_sequence.num
        else:
            self.playlist_sequence = first_sequence.num



class MyHandler(BaseHTTPRequestHandler):
    handlerStop = threading.Event()
    handlerStop.clear()

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
            request_path =  self.path[1:]
            parsed_path = urlparse.urlparse(self.path)
            path =  parsed_path.path[1:]
            try:
                params = dict(urlparse.parse_qsl(parsed_path.query))
            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write('URL malformed or stream not found!')
                return
            
            if request_path == "version":
                self.send_response(200)
                self.end_headers()
                self.wfile.write("StreamLink Proxy: Running\r\n")
                self.wfile.write("Version: 0.2\r\n")

            elif path == "streamlink/":
                fURL = params.get('url')
                fURL = urllib.unquote(fURL)
                q = params.get('q', None)
                if not q:
                    q = 'best' 
                #print 'fURL, q ', fURL,q      
                self.serveFile(fURL, q, sendData)        

            else:
                self.send_response(404)
                self.end_headers()
        finally:
                return

    """
    Sends the requested file and add additional headers.
    """
    def serveFile(self, fURL, quality, sendData):
        ## get SL plugins dir
        #
        try:
            streamlink_plugins = os.path.join('script.module.streamlink.plugins', 'plugins')
            path_streamlink_service = os.path.join('script.module.slproxy', 'lib', 'dsp')
            kodi_folder = os.path.dirname(os.path.realpath(__file__))
            custom_plugins = kodi_folder.replace(path_streamlink_service, streamlink_plugins)
        except:
            pass

        session = streamlink.session.Streamlink()
        #session.set_loglevel("debug")
        session.set_logoutput(sys.stdout)

        try:
            session.load_plugins(custom_plugins)
        except:
            pass
        
        if _dec:
            streamlink.stream.hls.HLSStreamWriter.create_decryptor = create_decryptor
            streamlink.stream.hls.HLSStreamWorker.process_sequences = process_sequences            

        if '|' in fURL:
            sp = fURL.split('|')
            fURL = sp[0]            
            headers = dict(urlparse.parse_qsl(sp[1]))
            session.set_option("http-ssl-verify", False)
            session.set_option("hls-segment-threads", 1)
            session.set_option("hls-segment-timeout", 10)

            try:
                if 'zoomtv' in headers['Referer']:
                    session.set_option("zoom-key", headers['Referer'].split('?')[1])                    
                elif 'zuom' in headers['Referer']:
                    session.set_option("zuom-key", headers['Referer'].split('?')[1])
                elif 'livecamtv' in headers['Referer'] or 'realtimetv' in headers['Referer'] or 'seelive' in headers['Referer']: 
                    session.set_option("livecam-key", headers['Referer'])
                    headers.pop('Referer')               
                elif 'sawlive' in headers['Referer']:
                    session.set_option("saw-key", headers['Referer'])
                elif 'yoursportsinhd' in headers['Referer']:
                    session.set_option("your-key", headers['Referer'])
                elif 'mamahd' in headers['Referer']:
                    session.set_option("mama-key", headers['Referer'].split('&')[1])
                elif 'CustomKeyUri' in headers:
                    session.set_option("custom-uri", headers['CustomKeyUri'])
                    headers.pop('CustomKeyUri')

            except:
                pass
            
            session.set_option("http-headers", headers)
            #xbmc.log('[StreamLink_Proxy] http-headers added: %s'%str(session.get_option("http-headers"))) 
            

        try:
            #xbmc.log('[StreamLink_Proxy] %s'%fURL) 
            streams = session.streams(fURL)             
            self.send_response(200)

        except NoPluginError:
            xbmc.log('[StreamLink_Proxy] no plugin found to handle this stream.')
            self.send_response(404)
            pass
            
        except Exception as err:
            traceback.print_exc(file=sys.stdout)
            xbmc.log('[StreamLink_Proxy] an error occured: %s'%str(err.message))
            self.send_response(500)
            
        finally:
            self.end_headers()

        if not streams:
            xbmc.log('[StreamLink_Proxy] no playable streams found on this URL: %s'%fURL)
            self.send_response(404)
            self.end_headers()
            return
         

        if (sendData):
               
            if not streams.get(quality, None):
                quality = 'best'                
                
            try:
                with streams[quality].open() as stream:
                    #xbmc.log('[StreamLink_Proxy] Playing stream %s with quality \'%s\''%(streams[quality],quality))
                    cache = 100 * 1024
                    self.send_response(200)
                    self.send_header('Content-type', 'video/unknown')
                    buf = 'INIT'
                    while buf and (len(buf) > 0 and not self.handlerStop.isSet()):
                        buf = stream.read(cache)
                        self.wfile.write(buf)

            except socket.error as e:
                if isinstance(e.args, tuple):
                    if e.errno == errno.EPIPE:
                        # remote peer disconnected
                        xbmc.log('[StreamLink_Proxy] detected remote disconnect!')
                    else:
                        xbmc.log('[StreamLink_Proxy] %s'%str(e))
                else:
                    xbmc.log('[StreamLink_Proxy] %s'%str(e))
            
            except Exception as err:
                traceback.print_exc(file=sys.stdout)
                xbmc.log('[StreamLink_Proxy] could not open stream: {0}'.format(err))

            finally:
                self.wfile.close()
                try: stream.close()
                except: pass
                stream = None            



class Server(HTTPServer):    
    timeout = 5
    """HTTPServer class with timeout.""" 

        

class ThreadedHTTPServer(ThreadingMixIn, Server):
    """Handle requests in a separate thread."""


class SLProxy():
    HOST_NAME = '127.1.2.3'
    PORT_NUMBER = 45678
    ready = threading.Event()

    def start(self, stopEvent):
        self.ready.clear()
        sys.stderr = sys.stdout
        server_class = ThreadedHTTPServer
        server_class.allow_reuse_address = True
        MyHandler.handlerStop = stopEvent
        httpd = server_class((self.HOST_NAME, self.PORT_NUMBER), MyHandler)
        xbmc.log("[StreamLink_Proxy] Service started - %s:%s." % (self.HOST_NAME, self.PORT_NUMBER))
        self.ready.set()

        while(True and not stopEvent.isSet()): #and not xbmc.abortRequested
            httpd.handle_request()
        
        httpd.server_close()
        self.ready.clear()
        xbmc.log('[StreamLink_Proxy] Service stopped.')
    
    def stop(self):
        pass

    def status(self):
        pass


class SLProxy_Helper():

    def startProxy(self):
        pass

    def playSLink(self, url, listitem):
        #print 'SLurl ',url
        stopPlaying=threading.Event()
        stopPlaying.clear()
        progress = xbmcgui.DialogProgress()
        sl_Proxy = SLProxy()
        url_to_play = 'http://%s:%s/streamlink/?url=%s'%(sl_Proxy.HOST_NAME, sl_Proxy.PORT_NUMBER, url)
        runningthread=thread.start_new_thread(sl_Proxy.start, (stopPlaying,))
        proxyReady = sl_Proxy.ready

        progress.create('Starting StreamLink Proxy')
        progress.update(0, 'Loading StreamLink Proxy','','')
        p = 10
        while True and p<100:
            if proxyReady.isSet():
                progress.update(90)
                break
            progress.update(p)
            xbmc.sleep(500)
            p+=10
        
        mplayer = MyPlayer()    
        mplayer.stopPlaying = stopPlaying
        progress.update(100)
        progress.close()
        mplayer.play(url_to_play, listitem)

        played=False
        while True:
            if stopPlaying.isSet():
                break
            if xbmc.Player().isPlaying():
                played=True
            xbmc.log('Sleeping...')
            xbmc.sleep(200)
            
        return played



class MyPlayer (xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def play(self, url, listitem):
        #print 'Now im playing... %s' % url
        self.stopPlaying.clear()
        xbmc.Player( ).play(url, listitem)
        
    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        #print "seting event in onPlayBackEnded " 
        self.stopPlaying.set()
        #print "stop Event is SET" 

    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        #print "seting event in onPlayBackStopped " 
        self.stopPlaying.set()
        #print "stop Event is SET" 




