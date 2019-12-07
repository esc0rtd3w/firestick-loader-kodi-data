#############################################################################
#
#   Copyright (C) 2013 Navi-X
#
#   This file is part of Navi-X.
#
#   Navi-X is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   Navi-X is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Navi-X.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

#############################################################################
#
# CDownloader:
# This class handles file downloads in a background task.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui, xbmcaddon
import re, os, time, datetime, traceback
import shutil
import zipfile
import threading
import ftplib
import os
import socket
import time
from settings import *
from CPlayList import *
from CDialogBrowse import *
from CURLLoader import *
from libs2 import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

######################################################################
# Description: See comments in class body
######################################################################
#class myURLOpener(urllib.FancyURLopener):
#    """Create sub-class in order to overide error 206.  This error means a
#       partial file is being sent,
#       which is ok in this case.  Do nothing with this error.
#    """
#    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
#        pass

######################################################################
# Description: File downloader including progress bar. 
######################################################################
class CDownLoader(threading.Thread):
    def __init__(self, *args, **kwargs):
        if (kwargs.has_key('window')): 
            self.MainWindow = kwargs['window']
        if (kwargs.has_key('playlist_src')): 
            self.playlist_src = kwargs['playlist_src']  
        if (kwargs.has_key('playlist_inc')): 
            self.playlist_inc = kwargs['playlist_inc']       
        if (kwargs.has_key('playlist_dst')): 
            self.playlist_dst = kwargs['playlist_dst']       

        threading.Thread.__init__(self)    

        self.setDaemon(True) #make a daemon thread   
        
        self.killed = False #not killed
        self.running = False #at startup downloader is not running
        self.shutdown = False #shutdown after all files downloaded

    def run(self):
        while self.killed == False:
            time.sleep(1.0) #delay 1 second
            #check if there are files in the download queue.
            while (self.killed == False) and (self.running == True) and (self.playlist_src.size() > 0):
                #there are files to be downloaded.
                self.download_queue()
    
    def download_start(self, shutdown = False):
        self.shutdown = shutdown
        self.running = True
    
    def download_stop(self):
        self.running = False
        
    def download_isrunning(self):
        return self.running
             
    def kill(self):
        self.killed = True
    
#    def notify(self):
#        self.event.set()
        
    ######################################################################
    # Description: Downloads a URL to local disk
    # Parameters : entry = media item
    # Return     : self.state (0=success, -1=failure, -2=cancel) 
    #              self.dir (the new selected download dir)
    #              self.localfile (the destination path+file)
    ######################################################################
    def browse(self, entry, dir=myDownloadsDir):
        self.state = 0 #success
        self.dir = ''
        self.processed=False
       
        URL=entry.URL

        if (URL[:4] != 'http') and (URL[:3] != 'ftp'):
            self.state = -1 #URL does not point to internet file.
            return

        if re.search('^http://(\w+\.)?(icefilms|mega(upload|video))\.', URL):
            size_check_skip=True
        else:
            size_check_skip=False
            
        if size_check_skip:
            print("Mega URL; skipping size check")
            size=0
            urlopener = CURLLoader()
            result = urlopener.geturl_processor(entry)
            URL=entry.URL
            loc_url=URL
            self.processed=entry.processed          
            self.loc_url=URL
            url_stripped = re.sub('\?.*$', '', loc_url) # strip GET-method args
            url_stripped = re.sub('\|.*$', '', url_stripped) # strip header info if any
            # find extension
            match = re.search('(\.\w+)$',url_stripped)
            if match is None:
                #ext = ""
                ext = getFileExtension(loc_url)
                if ext != '':
                    ext = '.' + ext
            else:
                ext = match.group(1)
        else:
            ext, size = self.read_file_info(entry)
            url_stripped = re.sub('\?.*$', '', entry.URL) # strip GET-method args
            url_stripped = re.sub('\&.*$', '', entry.URL) # strip odd GET-method args
            url_stripped = re.sub('\|.*$', '', url_stripped) # strip header info if any

        if self.state != 0:
            return
               
        # For the local file name we use the playlist item 'name' field.
        # But this string may contain invalid characters. Therefore
        # we strip these invalid characters. We also limit the file
        # name length to 42 which is the XBMC XBOX limit.

        if re.search('^Source #', entry.name):
            localfile=url_stripped[url_stripped.rindex("/")+1:]
        else:
            localfile = re.sub('[^\w\s-]', '', entry.name) # remove characters which are not a letter, digit, white-space, underscore, or dash
            localfile = re.sub('\s+', ' ', localfile) # convert all instances of multiple spaces to single spaces
            localfile = localfile[:(42-len(ext))] # limit to 42 characters.
            localfile = localfile + ext
        
        if size_check_skip:
            heading="Download File"
        else:
            size_string, raw_size = self.file_size(size,'')
            heading = "Download File: (Size = %s)" % size_string
            
        if (entry.type=='playlist') and (localfile.lower().endswith('.plx')==False):
            localfile+='.plx'
        
        #browsewnd = CDialogBrowse("CBrowseskin.xml", os.getcwd())
        curdir = addon.getAddonInfo('path')
        browsewnd = CDialogBrowse("CBrowseskin2.xml", curdir)
        browsewnd.SetFile(dir, localfile, 3, heading)
        browsewnd.doModal()

        if browsewnd.state != 0:
            self.state = -2 #cancel download
            return
        
        self.localfile = browsewnd.dir + browsewnd.filename
        self.dir = browsewnd.dir
        
        #Check if the file already exists
        if os.path.exists(self.localfile):
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Message", "The destination file already exists, continue?") == False:
                self.state = -2 #cancel download

        #end of function.        
        
    ######################################################################
    # Description: Retrieve the file extenstion and size of a URL 
    # Parameters : entry = mediaitem.
    # Return     : the file extension (ext) and file size (size)
    ######################################################################
    def read_file_info(self, entry):
        self.state = 0 #success    
        ext='' #no extension
        size = 0
        try:
            URL, headers = parse_headers(entry.URL)
        
            if URL[:3] == 'ftp':
                #FTP
                ext = getFileExtension(URL)
                if ext != '':
                    ext = '.' + ext
            else:
                #HTTP
                urlopener = CURLLoader()
                result = urlopener.urlopen(URL, entry);
                if result["code"] != 0:
                    self.state = -1; print('URL does not point to internet file.')
                    return ext, size
                loc_url = urlopener.loc_url#; print('line223 loc_url= ' +str(loc_url))
                self.processed=urlopener.processed#; print('self.processed= ' +str(self.processed))

                #Now we try to open the URL. If it does not exist an error is
                #returned.
                try:
                    #headers = { 'User-Agent' : 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)'}
                    req = urllib2.Request(loc_url, None, headers)
                    size_string,size_raw = self.file_size(0,req)
                    size = int(size_raw)
                except Exception, e: size = 0; print('ERROR line 237' +str(e))
                #loc_url=f.geturl()
                try:
                    #special handing for some URL's
                    pos = URL.find('http://www.youtube.com') #find last 'http' in the URL
                    if pos != -1:
                        ext='.mp4'
                    else:
          #todo: deprecated            
                        pos = URL.find("flyupload.com")
                        if pos != -1:
                            ext='.avi'
                        else:                             
                            #extract the file extension
                            url_stripped = re.sub('\?.*$', '', loc_url) # strip GET-method args
                            re_ext = re.compile('(\.\w+)$') # find extension
                            match = re_ext.search(url_stripped)
                            if match is None:
                                #ext = ""
                                ext = getFileExtension(loc_url)
                                if ext != '':
                                    ext = '.' + ext
                            else:
                                ext = match.group(1)
                except Exception, e: print('ERROR line 261','e =' +str(e))
            # processed youtube URL
    #the code below is failing. Do we still need it?
    #            match=re.search('youtube\.com/.*?&itag=(\d+)', loc_url)
    #            if match:
    #               fmt=int(match.group(1))
    #                if [5,6,34,35].index(fmt) >= 0:
    #                    ext='.flv'
    #                elif [43,44,45,46,100,101,46,102].index(fmt) >= 0:
    #                    ext='.webm'
    #                else:
    #                    ext='.mp4' # [18,22,37,38,83,82,85,84] - default to instead of testing for

            # safety net
            if len(ext)>6:
                ext='.avi'
        except Exception,e:
            print '\t\t\t Error CDL 278 ' + str(e)
        return ext, size
        
    ######################################################################
    # Description: Adds an item to the local playlists: queue, incomplete downloads, 
    #                     or completed downloads. while removing duplicate entries
    # Parameters : URL=source
    # Return     : -
    ######################################################################
    def add_list(self, entry,item_list):
        #if item_list == 'incdl': loc_list = RootDir + incomplete_downloads; playlist = self.playlist_inc
        #elif item_list== 'cmpdl': loc_list = RootDir + downloads_complete; playlist = self.playlist_dst
        #else: item_list ='queue'; loc_list = RootDir + downloads_queue; playlist = self.playlist_src
        
        if item_list == 'incdl': loc_list = datapaths + incomplete_downloads; playlist = self.playlist_inc
        elif item_list== 'cmpdl': loc_list = datapaths + downloads_complete; playlist = self.playlist_dst
        else: item_list ='queue'; loc_list = datapaths + downloads_queue; playlist = self.playlist_src
        self.state = 0 #success
        tmp = CMediaItem() #create new item
        tmp.type = entry.type
        tmp.name = entry.name
        tmp.thumb = entry.thumb
        tmp.URL = entry.URL
        tmp.DLloc = entry.DLloc
        tmp.player = entry.player
        tmp.processor = entry.processor
        tmp.background = entry.background
        #### remove duplicates from list then add new item
        pos = 0
        for line in open(loc_list,'r'):
            if line == '#\n' : pos+=1
            elif entry.DLloc in line: playlist.remove(pos-1)
        playlist.save(loc_list)         
        playlist.add(tmp); playlist.save(loc_list)
        
    ######################################################################
    # Description: Downloads a URL to local disk
    # Parameters : shutdown = true if auto shutdown after download.
    # Return     : -
    ######################################################################
    def download_queue(self, shutdown = False):
        self.state = 0 #success
        
        counter = 0
        
        self.MainWindow.download_logo.setVisible(1)
        self.MainWindow.dlinfotekst.setVisible(1)
        
        while (self.state != -2) and (self.playlist_src.size() > 0) and (self.killed == False) and (self.running == True):
            header = str(counter+1) + " of " + str(self.playlist_src.size()+counter)
            self.download_file(self.playlist_src.list[0], header) #download single file

            if self.state == 0:
                #Download file completed successfully
                self.playlist_src.remove(0)
                #self.playlist_src.save(RootDir + downloads_queue)
                self.playlist_src.save(datapaths + downloads_queue)
                counter += 1
            elif self.state == -1:     
                #Downlaod failed
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Error",str(self.playlist_src.list[0].name),"Download failed. Retry?") == False:
                    self.playlist_src.remove(0)
                    #self.playlist_src.save(RootDir + downloads_queue)
                    self.playlist_src.save(datapaths + downloads_queue)
                    counter += 1
                                            
            #Display the updated Queue playlist
            if (self.MainWindow.pl_focus == self.MainWindow.downloadqueue) or \
               (self.MainWindow.pl_focus == self.MainWindow.incompletelist) or \
               (self.MainWindow.pl_focus == self.MainWindow.downloadslist):
                self.MainWindow.ParsePlaylist(reload=False) #display download list
               
        if (self.shutdown == True) and (self.killed == False) and (self.running == True):
            self.MainWindow.onSaveSettings()
            self.MainWindow.delFiles(cacheDir) #clear the cache first        
            self.MainWindow.bkgndloadertask.kill()
            self.MainWindow.bkgndloadertask.join(10) #timeout after 10 seconds        
            xbmc.shutdown() #shutdown XBMC
        
        self.running = False #disable downloading
        
        self.MainWindow.dlinfotekst.setVisible(0)        
        self.MainWindow.download_logo.setVisible(0)

    ######################################################################
    # Description: Downloads a URL to local disk
    # Parameters : entry =  mediaitem to download
    #              header = header to display (1 of x)
    # Return     : -
    ######################################################################
    def download_file(self, entry, header=""):
        self.state = 0 #success
        
        URL = entry.URL
        localfile = entry.DLloc     
        
        #download of FTP file is handled in a separte function
        if URL[:3] == 'ftp':
            self.download_fileFTP(entry, header)
            return
        
        if URL[:4] != 'http':
            self.state = -1 #URL does not point to internet file.
            return

        #Continue with HTTP download
        self.MainWindow.dlinfotekst.setLabel('(' + header + ')' + " Retrieving file info...")
            
        # set custom headers if specified
        URL, headers=parse_headers(URL, entry)
        try:
            cookies = ''
            if URL.find(nxserver_URL) != -1:
                cookies='platform='+platform+'; version='+Version+'.'+SubVersion
                cookies=cookies+'; nxid='+nxserver.user_id
                headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4','Cookie':cookies}
                #headers={'User-Agent':'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)','Cookie':cookies}
        except Exception,e: 
            print('ERROR line 397 cookies ' +str(e))
            #print 'headers =    ' + str(headers)

        #Get the direct URL to the mediaitem given URL      
        urlopener = CURLLoader()
        self.processed=urlopener.processed            #### needed or will fault the next line at times
        entry.processed=self.processed
        try:
            result = urlopener.urlopen(URL, entry)
            if result["code"] != 0:
                self.state = -1 #failed to open the file
                print("urlopener.urlopen failed line 408  " + str(result))
                line2 = '%s  %s' % ('failed to open', str(entry.name))
                self.MainWindow.dlinfotekst.setLabel(line2)
                return
        except Exception,e:
            self.state = -1 #failed to open the file
            print("urlopener.urlopen failed line 414  " + str(e))
            line2 = '%s  %s' % ('failed to open', str(entry.name))
            self.MainWindow.dlinfotekst.setLabel(line2)
            return

        URL = urlopener.loc_url
        
#       oldtimeout=socket_getdefaulttimeout()
#       socket_setdefaulttimeout(url_open_timeout)

        existSize=0 #existing size = 0 Bytes

        if os.path.exists(localfile): 
            existSize = os.path.getsize(localfile)
            #Message("Exist size: " + str(existSize))
            #If the file exists, then only download the remainder
            NoRangeEntry = headers
            for RangeEntry in 'Ranges','Range','':
                if RangeEntry != '':
                    try:            #### test for range support
                        headers[RangeEntry] = 'bytes=%s-' % existSize
                        req = urllib2.Request(URL, None, headers)
                        f = urllib2.urlopen(req)
                        break
                    except: pass         #Expected error: HTTP Error 416: Requested Range Not Satisfiable'
                else:           #### if ranges are not supported
                    try:
                        req = urllib2.Request(URL, None, NoRangeEntry)
                        f = urllib2.urlopen(req)
                    except Exception as e:
                        self.state = -1; print('ERROR URL= ' + str(URL)); print('failed to open the URL file line 444 '+ str(e))
                        line2 = '%s  %s' % ('failed to open', str(entry.name))
                        self.MainWindow.dlinfotekst.setLabel(line2); return

        else:   # if the file does not exist
            #print('URL = ' +str(URL)); print('headers = ' + str(headers))
            try:
                req = urllib2.Request(URL, None, headers)
                f = urllib2.urlopen(req)
            except Exception as e:
                self.state = -1; print ('failed to open the URL file line 454', str(e))
                line2 = '%s %s' % ('failed to download', str(entry.name))
                self.MainWindow.dlinfotekst.setLabel(line2); return
            
        try: size_string,size_raw = self.file_size(0,req)     #### gets size of remote URL file or sets size_string = Unknown and size_raw = 0
        except Exception as e:
            self.state = -1; print ('failed to open the URL file line460', str(e))
            line2 = '%s  %s' % ('failed to download', str(entry.name)) 
            self.MainWindow.dlinfotekst.setLabel(line2); return

        #If the file exists, but we already have the whole thing, don't download again
        size = size_raw  #The remaining bytes
        
        file = open(localfile,'ab+')           #### opens and/or creates the destination file
        #Message("Remaining: " + str(size))
            
        if ((size > 0) and (size != existSize)) or size == 0:
            bytes = existSize #bytes downloaded already
            size = int(size) + int(existSize) #total size
            #Message("Total: " + str(size))
            total_chunks = 0
            
            #DL-speed calculation
            starttime=time.time()
            startSize = bytes
            deltatime = 0
            deltasize = 0
            dlspeed = 0
            
            self.add_list(entry,'incdl')             #### add to incomplete downloads, removing existing duplicate entries
            try:
                self.MainWindow.dlinfotekst.setLabel('(' + header + ')' + " Downloading file...")

                #download in chunks of 100kBytes                
                while ((bytes < size) or (size == 0) or (size_string == 'Unknown')) and (self.killed == False) and (self.running == True):
                    chunk = 100 * 1024 #100kBytes chunks
                    total_chunks += chunk           #### total chunks read
                    if ((bytes + chunk) > size and size!=0) and (size_string != 'Unknown'):
                        chunk = size-bytes #remainder
                    data = f.read(chunk)
                    #### if total_chunks <= whats already downloaded dont write it for unknown file size (append issue)
                    if data !='' and (size_string == 'Unknown') and (total_chunks > os.path.getsize(localfile)): file.write(data)
                    elif data !='' and (size_string != 'Unknown'): file.write(data)           #### write statement for files of known size
                    bytes = bytes + chunk
                    
                    if size == 0 or size_string == 'Unknown' : percent = 'Unknown %'
                    else: percent = str(100 * bytes / size) + '%'
                    size_string,r_size = self.file_size(size,req)
                    done,r_size = self.file_size(bytes,'')

                    deltatime = time.time() - starttime
                    if deltatime >=5: #update every 5 seconds
                        #calculate the download speed                        
                        deltasize = bytes - startSize
                        dlspeed = (deltasize / 1024) / deltatime                        
                        starttime = time.time()
                        startSize = bytes
                                            
                    line2 = '(%s) %s of %s - %s - %dkB/s' % (header, done, size_string, percent, dlspeed)
                    self.MainWindow.dlinfotekst.setLabel(line2)
                    if (size >= 0 or size_string == 'Unknown') and data == '': break
                f.close() #close the URL
            except Exception as e:
                self.state = -1; print ('failed to download the file CDLline 517', str(e))
                line2 = '%s  %s' % ('failed to download', str(entry.name))
                self.MainWindow.dlinfotekst.setLabel(line2)

            if (self.killed == True) or (self.running == False):
                self.state = -1 #failed to download the file

        file.close() #close the destination file  
#        socket_setdefaulttimeout(oldtimeout)
  
        #add the downloaded file to the download list
        if self.state == 0:
            self.add_list(entry,'cmpdl')
            #### remove from Incomplete Downloads
            #pos = 0; incdl = RootDir + incomplete_downloads
            pos = 0; incdl = datapaths + incomplete_downloads
            for line in open(incdl,'r'):
                if line == '#\n' : pos+=1
                elif entry.DLloc in line: self.playlist_inc.remove(pos-1)
            self.playlist_inc.save(incdl)

        #end of function

    ######################################################################
    # Description: Downloads a FTP URL to local disk
    # Parameters : entry =  mediaitem to download
    #              shutdown = true is shutdown after download
    #              header = header to display (1 of x)
    # Return     : -
    ######################################################################            
    def download_fileFTP(self, entry, header=""):
        self.state = 0 #success

        URL = entry.URL
        localfile = entry.DLloc

        self.header = header
        self.MainWindow.dlinfotekst.setLabel('(' + header + ')')
#@todo: move URLparse to another function.
########################
        #Parse URL according RFC 1738: ftp://user:password@host:port/path 
        #There is no standard Python funcion to split these URL's.
        username=''
        password=''        
        port=21
        
        #check for username, password
        index = URL.find('@')
        if index != -1:
            index2 = URL.find(':',6,index)
            if index2 != -1:
                username = URL[6:index2]
                print ('user: ' + username)
                password = URL[index2+1:index]
                print ('password: ' + password)           
            URL = URL[index+1:]
        else:
            URL = URL[6:]
        
        #check for host
        index = URL.find('/')
        if index != -1:
            host = URL[:index]
            path = URL[index:]
        else:
            host = URL
            path = ''
            
        #retrieve the port
        index = host.find(':')
        if index != -1:
            port = int(host[index+1:])
            host = host[:index]
            
        print ('host: ' + host)    
        print ('port: ' + str(port))
            
        #split path and file
        index = path.rfind('/')
        if index != -1:
            file = path[index+1:]
            path = path[:index]
        else:
            file = ''        
        
        print ('path: ' + path)
        print ('file: ' + file)
########################        
        try:
            self.f = ftplib.FTP()
            self.f.connect(host,port)
        except (socket.error, socket.gaierror) as e:
            print ('ERROR: cannot reach "%s"' % host)
            self.state = -1 #failed to download the file
            return

        print ('*** Connected to host "%s"' % host)

        try:
            if username != '':
                self.f.login(username, password)
            else:
                self.f.login()
        except ftplib.error_perm:
            print ('ERROR: cannot login anonymously')
            self.f.quit()
            self.state = -1 #failed to download the file
            return

        print ('*** Logged in as "anonymous"')

        try:
            self.f.cwd(path)
        except ftplib.error_perm:
            print ('ERROR: cannot CD to "%s"' % path)
            self.f.quit()
            self.state = -1 #failed to download the file
            return

        print ('*** Changed to "%s" folder' % path)

        #retrieve the file
        self.bytes = 0
        self.file = open(entry.DLloc, 'wb')

        try:
            #f.retrbinary('RETR %s' % file, open(entry.DLloc, 'wb').write)
            self.size = self.f.size(file)
            self.size_MB = float(self.size) / (1024 * 1024)
            self.percent2 = 0
            self.f.retrbinary('RETR %s' % file, self.download_fileFTP_callback)
        except ftplib.error_perm:
            print ('ERROR: cannot read file "%s"' % file)
            os.unlink(self.file)
        else:
            print ('*** Downloaded "%s" to CWD' % file)
        
        self.f.quit()
       
        self.file.close()
       
        if self.state == 0:
            self.add_list(entry,'cmpdl')            #### add to completed downloads
    
        #end of function

    ######################################################################
    # Description: Downloads a FTP URL to local disk (callback)
    # Parameters : entry =  mediaitem to download
    #              shutdown = true is shutdown after download
    #              header = header to display (1 of x)
    # Return     : -
    ######################################################################       
    def download_fileFTP_callback(self, string):
                
        self.file.write(string)
        
        self.bytes = self.bytes + len(string)
        percent = 100 * self.bytes / self.size
        
        if percent != self.percent2:
            self.percent2 = percent
        
            done = float(self.bytes) / (1024 * 1024)
        
            line2 = '(%s) %.1f MB - %d ' % (self.header, self.size_MB, percent) + '%'
                
            self.MainWindow.dlinfotekst.setLabel(line2)      
        
        if (self.killed == True) or (self.running == False):
            self.state = -2 #failed to download the file
            self.f.abort()
        
        #end of function
        
    ######################################################################
    # Description: Download Speed test
    # Parameters : entry =  mediaitem to test download speed
    # Return     : 0 on success, -1 on failure
    ######################################################################       
    def DownLoadSpeedTest(self, entry):
        #Get the direct URL to the mediaitem given URL      
        urlopener = CURLLoader()
        result = urlopener.urlopen(entry.URL, entry)
        if result["code"] != 0:
            return -1       

        URL = urlopener.loc_url

        if URL[:3] == 'ftp':
            dialog = xbmcgui.Dialog()
            dialog.ok("Message", "FTP download speed test not supported.")
            return 0

        dialog = xbmcgui.DialogProgress()
        dialog.create("Download Speed Test", entry.name)        
        dialog.update(0, entry.name)
    
        #try:
        bytes= 0
        chunk = 100 * 1024
        
        #rembember the user agent set the processor
        index = URL.find('|User-Agent=')
        if index != -1:
            useragent = URL[index+12:]
            URL = URL[:index]
        else:
            useragent = 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)'
        
        #headers = { 'User-Agent' : 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)'}
        headers = { 'User-Agent' : useragent}
        req = urllib2.Request(URL, None, headers)
        f = urllib2.urlopen(req)
        
        size_rb,size_raw = self.file_size(0,req)             ####
        #size_raw = f.headers['Content-Length']          ####
        size = int(size_raw)     
        
        file = open(tempCacheDir + "dltest", "wb")
        starttime = time.time()
        deltatime = 0
        updatetime = 0
    
        while deltatime < 10: #10 seconds
            if(dialog.iscanceled()):
                break
        
            if (bytes >= size): # got the complete file
                break;
        
            file.write(f.read(chunk))
            bytes = bytes + chunk
        
            deltatime = time.time() - starttime
            if (deltatime - updatetime) >= 1.0:
                dialog.update(int(deltatime*10), entry.name)            ####
                #dialog.update(deltatime*10, str(deltatime-updatetime))
                updatetime = deltatime

        f.close()
        file.close()                
        os.remove(tempCacheDir + "dltest")
                
        #except IOError:
            #pass
  
        dialog.close()        
        
        if deltatime < 3:
            return -1 # failed because we need at least 3 seconds to have an accurate measurement
        
        if (deltatime < 10) and (bytes < size):
            return 0 #abort
        
        #calculate the download speed
        dlspeed = (bytes / 1024) / deltatime
        
        dialog = xbmcgui.Dialog()
        dialog.ok("Message", "Download speed: %d kBytes/s." % dlspeed)
        
        return 0

    #########################################################################
    # Call Description ex: string_size, raw_size = self.file_size(size,req)
    # Parameters : size = number
    #              requ format example = [urllib2.Request(URL, None, headers)]
    # Returns: ts_size as a rounded string ex:(1.1 KB) or Unknown 
    #          fl_size as a number ex:(1132)
    #########################################################################
    def file_size(self,r_size=0,requ=''):
        ts_size = 'Unknown'; fl_size = 0
        if (r_size == 0 or r_size == 'Unknown') and requ == '': return ts_size, fl_size 
        try:
            if r_size == 0 and requ != '':
                fr = urllib2.urlopen(requ)
                #print(fr.headers)
                if 'Content-Length' not in fr.headers: return ts_size, fl_size
                fl_size = fr.headers['Content-Length']; fr.close()
                r_size = (fl_size)
            size_bt = float(r_size)
            if fl_size  >= 0 and r_size != 0:
                if (size_bt / 10**3 ) < 1  : ts_size = str(size_bt) +' Bs'
                elif (size_bt / 10**6)  < 1 : ts_size = str(round(size_bt / 10**3,1)) +' KB'
                elif (size_bt / 10**9)  < 1 : ts_size = str(round(size_bt / 10**6,1)) +' MB'
                elif (size_bt / 10**12)  < 1: ts_size = str(round(size_bt / 10**9,1)) +' GB'
                else: ts_size = str(round(size_bt /10**12,1)) +' TB'
        except Exception, e: print('ERROR line783 CDownLoader.fl_size function: '+'e = ' + str(e))
        return  ts_size, fl_size
        #end of function                      
