'''
    AxelProxy XBMC Addon
    Copyright (C) 2013 Eldorado

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
'''

import re
import urllib2
import urllib
import sys
import traceback
import socket
import base64
import hashlib
import os
import time
import threading
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
#import multiprocessing
import axel
import axelcommon #todo: remove this and its usage from this class
from axelcommon import Singleton
import urlparse
import uuid


#Address and IP for Proxy to listen on
HOST_NAME = '127.0.0.1'
#HOST_NAME = 'localhost'
PORT_NUMBER = 45550 ##move this somewhere which could be configured by UI

http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; '
        'en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/xml,application/xml,application/xhtml+xml,'
        'text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    'Accept-Language': 'en-us,en;q=0.5',
    }
    
class MyHandler(BaseHTTPRequestHandler):



    #Handles a HEAD request
    def do_HEAD(self):
        self.send_response(200)
        rtype="video/mp4"  #default type could have gone to the server to get it.
        self.send_header("Content-Type", rtype)
        self.send_header("Accept-Ranges","bytes")
        self.end_headers()

    #Handles a GET request.
    def do_GET(self):
        print "GET request"
        # Send head and video
        self.answer_request()


    #Handle incoming requests
    def answer_request(self):
        try:

            #Pull apart request path
            request_path=self.path[1:]       
            request_path=re.sub(r"\?.*","",request_path)
            #If a request to stop is sent, shut down the proxy

            if request_path.lower()=="stop":# all special web interfaces here
                sys.exit()
                return
            if request_path.lower()=="status":
                print 'Get STatus Call!'
                self.respondStatus();
                self.wfile.close()
                return
            if request_path.lower()=="favicon.ico":
                print 'dont have no icone here, may be in future'
                self.wfile.close()
                return
            if  request_path.lower()=='stopdownload' :
                #file_stop=re.findall( '=(.*)',self.path[1:])[0]
                download_id=re.findall( '=(.*)',self.path[1:])[0]
                print 'Get stop download Call!',request_path,download_id
                self.respondStopDownload(download_id);
                self.wfile.close()
                return

            print 'request_path',request_path
            #If a range was sent in with the header
            requested_range=self.headers.getheader("Range")

            print 'REQUEST PATH: %s' % request_path
            print 'REQUEST RANGE: %s' % requested_range

            #Expecting url to be sent in base64 encoded - saves any url issues with XBMC
            #(file_url,file_name)=self.decode_B64_url(request_path)

            (download_id,file_url,file_name,download_mode ,keep_file,connections,dest_folder_path)=self.decode_url(request_path)
            print file_url


            #Send file request
            self.handle_send_request(download_id,file_url, file_name, requested_range,download_mode ,keep_file,connections,dest_folder_path)
        


        except:
            #Print out a stack trace
            traceback.print_exc()

            #Close output stream file
            self.wfile.close()
            return

        #Close output stream file
        self.wfile.close()
        return

    def respondStopDownload(self,download_id):
        #response='Stopping',filename#self.getStatus()
        response=self.stopDownloading(download_id)
        if response==True:
            response="Termination has been Queued!"
        else:
            response="Remove Failed!"
        self.sendHTML(response)

    def stopDownloading(self,download_id):
        print 'stopping',download_id
        import axel
        downloader_manager=axel.AxelDownloadManager()
        return downloader_manager.stop_downloader(download_id)


    def respondStatus(self):
        response=self.getStatus()
        self.sendHTML(response)
        
    def sendHTML(self,html):
        response=html
        #print response
        try:
            self.send_response(200)
        
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-length', len(response))
            self.end_headers()
        
            self.wfile.write(response)
            self.wfile.flush()
        except: 
            traceback.print_exc() #this is giving greif every second time

    def getStatus(self):
        import axel
        downloader_manager=axel.AxelDownloadManager()
        downloaders = downloader_manager.get_downloaders()
        try:
            if len(downloaders):
                htmlText="<html><head></head><body>"
                htmlText+="<table width=100% style=\"table-layout:fixed\">"
                htmlText+= "<TR>"
                htmlText+= "<TD>Action</TD>"
                htmlText+= "<TD>File Name </TD>"
                htmlText+= "<TD>File Size (MB) (bytes)</TD>"
                htmlText+= "<TD>Completed</TD>"
                htmlText+= "<TD>Terminated</TD>"
                htmlText+= "<TD>Chunks Size (KB)</TD>"
                htmlText+= "<TD>Total Chunks</TD>"
                htmlText+= "<TD>Total Chunks Completed</TD>"
                htmlText+= "<TD>Total Chunks Remaining</TD>"
                htmlText+= "</TR>"
                #if 1==2:
                for downloader_name in downloaders:
                    downloader=downloaders[downloader_name]
                    file_size = downloader.fileLen
                    file_name = downloader.filename
                    download_id = downloader.download_id
                    
                    
                    htmlText+= "<TR>"
                    htmlText+= "<TD><a href=\"http://127.0.0.1:" +str(PORT_NUMBER)+ "/StopDownload?download_id="+ download_id + "\">Stop</a></TD>"
                    htmlText+= "<TD>"+ file_name+"</TD>"
                    htmlText+= "<TD>"+ str(int(file_size)/1024/1024 )+"</TD>"
                    htmlText+= "<TD>"+ str(downloader.completed) +"</TD>"
                    htmlText+= "<TD>"+ str(downloader.terminated) +"</TD>"
                    htmlText+= "<TD>"+ str(downloader.chunk_size/1024) +"</TD>"
                    htmlText+= "<TD>"+ str(downloader.total_chunks) +"</TD>"
                    htmlText+= "<TD>"+ str(len(downloader.completed_work())) +"</TD>"
                    htmlText+= "<TD>"+ str(downloader.total_chunks-len(downloader.completed_work())) +"</TD>"
                    htmlText+= "</TR>"
                    htmlText+= "<TR>"
                    htmlText+= "<TD colspan=9>"
                    htmlText+=  downloader.file_link
                    htmlText+= "</TR>"
                    htmlText+= "<TR>"
                    htmlText+= "<TD colspan=9>"
                    htmlText+= "<table wdith=100% cellpadding=\"0\" cellspacing=\"0\" style=\"table-layout:fixed\"><TR>"
                    L=downloader.completed_work()
                    #print L
                    
                    for index in range(0,downloader.total_chunks):
                        cellW="{0:.2f}".format(100.00/downloader.total_chunks)
                        s_number=index*downloader.chunk_size
                        
                        if len(L):
                            if  len([b for b,s in enumerate(L) if s[1] == s_number])>0:
                                htmlText+= "<TD bgcolor=green width=" + cellW + "%>&nbsp;</TD>"
                            else:
                                htmlText+= "<TD bgcolor=red width=" + cellW + "%>&nbsp;</TD>"
                    htmlText+= "</TR></table>"
                    htmlText+= "</TD></TR>"

                htmlText+="</table>"
                htmlText+="</body></html>" 
                print htmlText
                return htmlText
            else:
                return 'Nothing in cache/downloading'
        except Exception, e:
            print 'Exception creating status: %s' % e
            return 'Error in status' #connection drop
    
    def handle_send_request(self,download_id, file_url, file_name, s_range,download_mode ,keep_file,connections,dest_folder_path):

        file_dest = axelcommon.profile_path #TODO: this should be python not xbmc proxy.
        if not dest_folder_path=='':
            file_dest=dest_folder_path
        rtype="video/mp4" #just as default
        import axel
        downloadManager = axel.AxelDownloadManager() #singleton
        existing_download=downloadManager.current_downloader(download_id)
        if existing_download==None:
            file_size,file_url,rtype=self.get_file_size(file_url)# TODO: get the url again, incase there is a redirector
        else:
            file_size,file_url,rtype= existing_download.fileLen,file_url, existing_download.rtype

        file_size=int(file_size)
        print 'file size',file_size
        (srange, erange) = self.get_range_request(s_range, file_size)
        print 'REQUESTING from %s to %s, srange=%s' % (str(srange), str(erange),s_range)
        #Set response type values
        
        etag=self.generate_ETag(file_url)

        content_size= file_size
        videoContents=""
        # Do we have to send a normal response or a range response?
        portionLen=0
        print 'download_mode',download_mode
        if str(download_mode)=='2': #if its download only then do not stream
            print 'got download request'
            downloader = downloadManager.start_downloading(download_id,file_url, file_dest, file_name, 0,download_mode ,True,connections,rtype) #either create downloader or return exiting one
            print 'download started'
            self.sendHTML('Download Started')
            return
        elif s_range and not s_range=="bytes=0-0": #we have to stream?
            print 'streaming request'
            self.send_response(206)
            crange="bytes "+str(srange)+"-" +str(int(content_size-1))+"/"+str(content_size)#recalculate crange based on srange, portionLen and content_size 
            self.send_header("Content-Range",crange)
            self.send_http_headers(file_name, rtype, content_size , etag)
            downloader = downloadManager.start_downloading(download_id,file_url, file_dest, file_name, srange,download_mode ,keep_file,connections,rtype) #either create downloader or return exiting one

            self.keep_sending_video(self.wfile,downloader,srange) #TODO create a streamer class and let it do the job #start sending video, this will never terminate, unless we are done sending
            downloader.clients-=1
                
        else:
            #Send back 200 reponse - OK
            self.send_response(200)
            self.send_header("Accept-Ranges","bytes")
            self.send_http_headers(file_name, rtype, content_size , etag)


                
    def keep_sending_video(self,file_out, downloader, start_byte): #read the chunk, send it back
        try:
            while True:
                video_data,data_len = downloader.get_video_chunk(start_byte, 10) #get a video chunk, timeout 10 seconds
                if data_len==0:
                    print 'No More video'# perhaps timed out
                    return
                else:
                    #print 'got something to send back',data_len
                    if not self.send_video_back(file_out,video_data):
                        return #client disconneted?. no more work here
                start_byte+=(data_len)

        except Exception, e:
            print 'Exception start_sending_video: %s' % e
            return #connection drop no more work here

    def send_video_back(self,file_out, videoData):
        try:
            file_out.write(videoData);
            file_out.flush();
            return True
        except Exception, e:
            print 'Exception send_video_back porting: %s' % e
            return False #connection drop



    def get_file_size(self, url): #check the redirector here and update the url if needed
        request = urllib2.Request(url, None, http_headers)
        data = urllib2.urlopen(request)
        content_length = data.info()['Content-Length']
        content_type=data.info()['Content-Type']
        return content_length,url,content_type


    #Set and reply back standard set of headers including file information
    def send_http_headers(self, file_name, content_type, content_size , etag,):
        print "Sending headers"
        try:
            self.send_header("Content-Disposition", "inline; filename=\"" + file_name.encode('iso-8859-1', 'replace')+"\"")
        except:
            pass
        self.send_header("Content-Type", content_type)
        self.send_header("Last-Modified","Wed, 21 Feb 2000 08:43:39 GMT")
        self.send_header("ETag",etag)
        self.send_header("Accept-Ranges","bytes")
        self.send_header("Cache-Control","public, must-revalidate")
        self.send_header("Cache-Control","no-cache")
        self.send_header("Pragma","no-cache")
        self.send_header("features","seekable,stridable")
        self.send_header("client-id","12345")
        self.send_header("Content-Length", str(content_size))
        self.send_header("Connection", 'close')
        self.end_headers()


    #Generate a unique hash tag
    def generate_ETag(self, url):
        md=hashlib.md5()
        md.update(url)
        return md.hexdigest()


    def get_range_request(self, hrange, file_size):
        if hrange==None:
            srange=0
            erange=None
        else:
            try:
                #Get the byte value from the request string.
                hrange=str(hrange)
                splitRange=hrange.split("=")[1].split("-")
                srange=int(splitRange[0])
                erange = splitRange[1]
                if erange=="":
                    erange=int(file_size)-1
                #Build range string
                
            except:
                # Failure to build range string? Create a 0- range.
                srange=0
                erange=int(file_size-1);
        return (srange, erange)


        
    def decode_url(self, url):
        print 'in params'
        params=urlparse.parse_qs(url)
        print 'params',params # TODO read all params
        #({'url': url, 'downloadmode': downloadmode, 'keep_file':keep_file,'connections':connections})
        received_url = params['url'][0]#
        download_id = params['download_id'][0]#

        #received_url = base64.b64decode(received_url)
        download_id = params['download_id'][0]#
        file_name=''
        dest_folder_path=''
        try:
            file_name=params['name'][0]#
        except: pass
        try:
            dest_folder_path=params['dest_folder_path'][0]#
        except: pass
        if file_name=='':
            file_name=download_id
        file_ext=''
        if not '.' in file_name:
            try:
                print file_name,received_url
                file_ext = received_url.split('/')[-1]
                file_ext=file_ext.split('?')[0]
                file_ext=file_ext.split('.')
                if len(file_ext)>0:
                    file_ext=file_ext[-1]
                else:
                    file_ext=''
            except:
                traceback.print_exc()
                file_ext=''
            if len(file_ext)==0: file_ext='mp4' #catchall
            file_name+='.'+file_ext
   
        file_name=  file_name.replace("\\","")
        file_name=  file_name.replace("/","")
        file_name=  file_name.replace(":","")
        file_name=  file_name.replace("*","")
        file_name=  file_name.replace("?","")
        file_name=  file_name.replace("\"","")
        file_name=  file_name.replace("<","")
        file_name=  file_name.replace(">","")
        file_name=  file_name.replace("|","")
        
        
                
        #file_name+='.flv' #do we need to get the fullname?#todo see if we need to make the name nuetral to file naming conventions like : etc to remove

        download_mode=int(params['downloadmode'][0])
        keep_file=False
        print 'keep',params['keep_file'][0].lower()
        if params['keep_file'][0].lower()=='true':
            keep_file=True
        print keep_file
        connections=int(params['connections'][0])
        return (download_id,received_url, file_name,download_mode ,keep_file,connections,dest_folder_path)


class Server(HTTPServer):
    """HTTPServer class with timeout."""

    def get_request(self):
        """Get the request and client address from the socket."""
        # 10 second timeout
        self.socket.settimeout(5.0)
        result = None
        while result is None:
            try:
                result = self.socket.accept()
            except socket.timeout:
                pass
        # Reset timeout on the new socket
        result[0].settimeout(1000)
        return result

class ThreadedHTTPServer(ThreadingMixIn, Server):
    """Handle requests in a separate thread."""
    
    
class ProxyHelper():

    def playUrl(self,url,name='',connections=2, keep_file=False,dest_folder_path=''):
        finalUrl,download_id = self.create_proxy_url(url,connections=connections,keep_file=keep_file,name=name,dest_folder_path=dest_folder_path)
        self.play_in_XBMC(finalUrl,name,download_id,keep_file)

    def download(self,url,name='',connections=2,dest_path=''):
        finalUrl,download_id = self.create_proxy_url(url,connections=connections,downloadmode=2,keep_file=True,name=name,dest_folder_path=dest_path)
        self.call_page(finalUrl)
        return download_id
        
    def play_in_XBMC(self,url, name,download_id,keep_file):
        try:
            import axelPlayer
            import xbmcgui
            import xbmc
            stopPlaying=threading.Event()
            mplayer = axelPlayer.axelPlayer()
            mplayer.setStopEvent(stopPlaying)
            listitem = xbmcgui.ListItem(name)
            mplayer.play(url,listitem)
            while True:
                xbmc.log('Sleeping...')
                xbmc.sleep(1000)
                if stopPlaying.isSet():
                    break;
            # call the proxy to stop 
            #if not keep_file: #if file saving is not required then ask download to stop
            self.stop_download(download_id)# call it all the time, so that file could be renamed
        except:
            print 'failed in play_in_XBMC'
            traceback.print_exc()

     
    def stop_download(self,download_id):
        try:
            url=self.get_stop_url(download_id)
            self.call_page(url)
            print 'stop request sent'
        except:
            print 'failed in stop_download'
            traceback.print_exc()
            
    def call_page(self,url): #reuse this to return data
        try:
            request = urllib2.Request(url, None, http_headers)
            data = urllib2.urlopen(request)
        except:
            print 'failed in call_page'
            traceback.print_exc()
            
    def get_stop_url(self,download_id): 
        newurl="StopDownload?download_id="+str(download_id)
        pm=ProxyManager()
        link = 'http://'+self.get_hostname()+(':%s/'%self.get_port()) + newurl
        return link
        
    def create_proxy_url(self,url,downloadmode=1,keep_file=False,connections=2, name='', dest_folder_path=''): #todo: use in proxy#downloadmode=1 means stream. 2 means download only
        download_id=str(uuid.uuid4())
        newurl=urllib.urlencode({'url': url, 'downloadmode': downloadmode, 'keep_file':keep_file,'connections':connections,'download_id':download_id,'name':name,'dest_folder_path':dest_folder_path})
        pm=ProxyManager()
        print 'host name is',pm.host_name,newurl
        link = 'http://'+self.get_hostname()+(':%s/'%self.get_port()) + newurl
        return (link,download_id) #make a url that caller then call load into player
        
    def get_port(self):
        return ProxyManager().port # TODO, get some sort of settings etc 

    def get_hostname(self):
        return ProxyManager().host_name # TODO, get some sort of settings etc 
        
    def restart_server(self,port=0):
        ProxyManager().restart_proxy()
        return True # TODO, we need to restart the server, perhaps with different port? 
    
    def print_debug(self):
        #ProxyManager()
        print 'debug'#dm.downloads



class ProxyManager(Singleton): #todo: make it singleton, add functions to start and restart etc
    def __init__(self): 
        self.runningthread=None#current downloads that happening
        self.host_name=HOST_NAME
        self.port=PORT_NUMBER
        self.abort=False
       

    def is_running(self):
        if self.runningthread:
            return True
        else:
            return False
            
    def start_proxy(self,port=PORT_NUMBER, host_name=HOST_NAME,download_folder=''):
        #todo delete the part files from the addon data directory.
        self.host_name=host_name
        self.port=port
        st = threading.Thread(target=self.start_proxy_internal, args = (download_folder,port,host_name, ))
        st.start()
        self.runningthread=st

    def stop_proxy(self):#todo: use download_folder and other parameters
        print 'stop it' #todo
    
    def restart_proxy(self,download_folder='',port=0, host_name=''):#todo: use download_folder and other parameters
        print 'restart it it' #todo kill the thread and call start_proxy

            
    def start_proxy_internal(self,download_folder,port,host_name):#todo: use download_folder and other parameters

        socket.setdefaulttimeout(10)
        server_class = ThreadedHTTPServer

        myhandler=MyHandler
        #myhandler.protocol_version = "HTTP/1.1"
        myhandler.protocol_version = "HTTP/1.0"
        httpd = server_class((host_name, port), myhandler)
        print "AxelProxy Downloader Starting - %s:%s" % (host_name, port)
        print 'Press CTL break to stop.....'
        while(True):
            httpd.handle_request()
            if self.abort: 
                print 'breaking..........................'
                break
        httpd.server_close()
        print "AxelProxy Downloader Stopping %s:%s" % (host_name, port)
