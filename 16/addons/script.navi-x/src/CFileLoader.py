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
# CFileloader:
# This class is a generic file loader and handles downloading a file to disk.
#############################################################################

from string import *
import sys, os.path, re, random, string, os, time, datetime, traceback, urllib, urllib2, xbmc, xbmcgui, shutil, zipfile, \
    ftplib, filecmp, md5
# import hashlib
from settings import *
from libs2 import *
from CServer import *

try:
    Emulating = xbmcgui.Emulating
except:
    Emulating = False


# todo: Add support for FTP files.

class CFileLoader2:
    def __init__(self, *args, **kwargs):
        if (kwargs.has_key('window')):
            try:
                self.MainWindow = kwargs['window']
            except:
                pass
            # TestBug({'From':'CFileLoader2: __init__','MainWindow':'Was Found'})
            # if hasattr(self.MainWindow,'dt'):
            #    print {"MainWindow: ":str(self.MainWindow.dt.getLabel())}
        # else:
        #    self.MainWindow=0
        self.metadata = {}
        self.metadata["expires"] = '0'
        self.localfile = ''
        cachedFlag = False
        # if hasattr(self,'MainWindow'):
        #    if hasattr(self.MainWindow,'logo'):
        #        self.MainWindow.logo.setVisible(True)
    
    ######################################################################
    # Description: Downloads a file in case of URL and returns absolute
    #              path to the local file.
    # @todo: Fill parameters
    # Parameters : URL=source, localfile=destination
    # Return     : -
    ######################################################################
    def load(self, URL, localfile='', timeout=0, proxy="CACHING", content_type='', retries=0):
        if (URL == ''):
            self.state = -1  # failed
            return
        
        destfile = localfile
        self.data = ''
        
        if not content_type in ['image']:
            TestBug({'content_type': content_type, 'proxy': proxy, 'URL': URL, 'localfile': localfile})
        if hasattr(self, 'MainWindow'):
            if not content_type in ['image']:
                # if hasattr(self.MainWindow,'logo'):
                #    self.MainWindow.logo.setVisible(True)
                # if hasattr(self.MainWindow,'imgCProtocol'):
                #    self.MainWindow.imgCProtocol.setVisible(True)
                if hasattr(self.MainWindow, 'imgProtocol'):
                    if URL.lower().startswith('ftp://') or localfile.lower().startswith('ftp://'):
                        try:
                            self.MainWindow.imgProtocol.setImage(imageBrowse['FTP'])
                        except:
                            pass
                    else:
                        try:
                            self.MainWindow.imgProtocol.setImage(imageBrowse['Remote'])
                        except:
                            pass
                        #    self.MainWindow.imgProtocol.setVisible(True)
                        #    TestBug({'imageBrowse[Cache]':imageBrowse['Remote']})
        # TestBug("MainWindow was Found. Using: load")
        #        TestBug({'From':'loadSmartCache: near end','MainWindow':'Was Found','cachedFlag':cachedFlag,'content_type':content_type,'proxy':proxy,'URL':URL,'localfile':localfile})
        #        if cachedFlag==True:
        #            self.MainWindow.logo.setVisible(False)
        #        else:
        #            self.MainWindow.logo.setVisible(True)
        # else:
        #        TestBug({'From':'loadSmartCache: near end','MainWindow':'Not Found','cachedFlag':cachedFlag,'content_type':content_type,'proxy':proxy,'URL':URL,'localfile':localfile})
        
        
        
        if (URL[:4] == 'http') or (URL[:3] == 'ftp'):
            sum_str = ''
            if proxy != "DISABLED":
                # sum=0
                ##calculate hash of URL
                # for i in range(len(URL)):
                #    sum=sum+(ord(URL[i]) * i)
                # sum_str=str(sum)
                
                # sum_str=hashlib.md5(URL).hexdigest()
                sum_str = md5.new(URL).hexdigest()
            
            if localfile != '':
                ext_pos = localfile.rfind('.')  # find last '.' in the string
                if ext_pos != -1:
                    destfile = localfile[:ext_pos] + sum_str + localfile[ext_pos:]
                else:
                    destfile = localfile + sum_str
            else:
                destfile = tempCacheDir + sum_str
            
            if proxy == "INCACHE":
                if os.path.exists(destfile) == True:
                    self.localfile = destfile
                    self.state = 0  # success
                # todo: load file in memory if localfile=''
                else:
                    self.state = -1  # failed
            elif proxy == "NEVER":
                if (os.path.exists(destfile) == True): self.deleteMetaData(destfile)
                if URL[:3] == 'ftp':
                    self.loadFTP(URL, destfile, timeout, proxy, content_type, retries)
                else:
                    self.loadHTTP(URL, destfile, timeout, proxy, content_type, retries)
            elif (not ((proxy == "ENABLED") and (os.path.exists(destfile) == True))):
                # option CACHING or SMARTCACHE is set
                # TestBug("Reached SMARTCACHE if within load function.")
                if proxy == "SMARTCACHE":
                    TestBug("*Reached SMARTCACHE if within load function.")
                    self.loadSmartCache(URL, destfile, timeout, proxy, content_type, retries)
                    TestBug("*done SMARTCACHE if within load function.")
                else:  # option CACHING or DISABLED
                    self.deleteMetaData(destfile)
                    if URL[:3] == 'ftp':
                        self.loadFTP(URL, destfile, timeout, proxy, content_type, retries)
                    else:
                        self.loadHTTP(URL, destfile, timeout, proxy, content_type, retries)
            else:  # (proxy=="ENABLED") and (os.path.exists(destfile)==True)
                if hasattr(self, 'MainWindow'):
                    if not content_type in ['image']:
                        if hasattr(self.MainWindow, 'imgProtocol'):
                            try:
                                self.MainWindow.imgProtocol.setImage(imageBrowse['Local'])
                            except:
                                pass
                
                self.localfile = destfile
                self.state = 0  # success
                
                if localfile == '':
                    try:
                        f = open(self.localfile, 'r')
                        self.data = f.read()
                        f.close()
                    except Exception, e:
                        self.state = -1;
                        print'Error EXCEPTION ' + str(e)  # failed
                        traceback.print_exc(file=sys.stdout)
        else:  # localfile
            if URL == '' and localfile != '': URL = localfile
            if len(URL) > 2:
                iLocFile = False
                if (URL[1] == ':') or (URL[0] == '/'):  # absolute (local) path
                    self.localfile = URL
                    self.state = 0  # success
                    iLocFile = True
            if iLocFile == True:
                pass
            else:  # assuming relative (local) path
                if URL == 'downloads.plx' or URL == 'incdloads.plx' or URL == 'downlqueue.plx' or URL == 'My Playlists.plx' \
                        or URL == 'blacklist.plx' or URL == 'history.plx' or URL == 'favorites.plx':
                    self.localfile = datapaths + URL
                    self.state = 0;  # success
                elif 'addons://' in URL:
                    self.localfile = xbmc.translatePath(URL.replace('addons://', 'special://home/addons/'))
                    self.state = 0
                else:
                    self.localfile = RootDir + SEPARATOR + URL;
                    self.state = 0;  # success
            # elif 'addons://' in URL:
            #    self.localfile=xbmc.translatePath(URL.replace('addons://','special://home/addons/'))
            #    self.state=0
            # else: #assuming relative (local) path
            #    self.localfile=RootDir+SEPARATOR+URL
            #    self.state=0 #success
            
            # Trace(self.localfile)
            
            if hasattr(self, 'MainWindow'):
                if not content_type in ['image']:
                    if hasattr(self.MainWindow, 'imgProtocol'):
                        try:
                            self.MainWindow.imgProtocol.setImage(imageBrowse['Local'])
                        except:
                            pass

            if localfile == '':
                try:
                    f = open(self.localfile, 'r')
                    self.data = f.read()
                    f.close()
                except Exception as e:
                    print'Error EXCEPTION ' + str(e);self.state = -1  # failed
                    traceback.print_exc(file=sys.stdout)
    
    ######################################################################
    # Description: Reads a file using smart caching
    # Parameters : URL=source, localfile=destination
    # Return     : -
    ######################################################################           
    def loadSmartCache(self, URL, localfile='', timeout=0, proxy="CACHING", content_type='', retries=0):
        
        expires = DefaultCachedExpires  # 3600 #seconds
        cachedFlag = False
        TestBug(["Attempting SmartCache"])
        # if hasattr(self,'MainWindow'):
        #    if hasattr(self.MainWindow,'logo'):
        #        if not content_type in ['image']:
        #            self.MainWindow.logo.setVisible(False)
        #            TestBug("MainWindow was Found. Using: loadSmartCache")
        if os.path.exists(localfile) == True:
            self.readMetaData(localfile)
            
            if self.metadata["expires"] != '0':
                expires = int(self.metadata["expires"])
                # check if the file is expired
                creationtime = os.path.getmtime(localfile)
                currenttime = time.time()
                deltatime = currenttime - creationtime  # ;deltatime =int(deltatime)*1000
                # dialog=xbmcgui.Dialog(); dialog.ok("DEBUG ",'expires = ' + str(expires),'deltatime = ' + str(deltatime))
                
                if deltatime < expires:
                    self.state = 0  # success
                    try:
                        f = open(localfile, 'r')
                        self.data = f.read()
                        f.close()
                    except Exception, e:
                        print 'error ' + str(e);self.state = -1  # failed
                    TestBug(["Used SmartCache?"])
                    if hasattr(self, 'MainWindow'):
                        if not content_type in ['image']:
                            # if hasattr(self.MainWindow,'logo'):
                            #    self.MainWindow.logo.setImage(imageBrowse['Cache'])
                            #    self.MainWindow.logo.setVisible(False)
                            #    TestBug(["MainWindow was Found. Just Fetched from cache. Using: loadSmartCache"])
                            if hasattr(self.MainWindow, 'imgProtocol'):
                                try:
                                    self.MainWindow.imgProtocol.setImage(imageBrowse['Cache'])
                                except:
                                    pass
                                #    self.MainWindow.imgProtocol.setVisible(False)
                                TestBug(["MainWindow was Found. Just Fetched from cache. Using: loadSmartCache"])
                                TestBug({'imageBrowse[Cache]': imageBrowse['Cache']})
                                # if hasattr(self.MainWindow,'imgCProtocol'):
                                #    self.MainWindow.imgCProtocol.setVisible(True)
                                #    TestBug({'imageBrowse[Cache]':imageBrowse['Cache']})
                    return
                
                # rename the existing (expired file)
                os.rename(localfile, localfile + ".old")
        
        # load the file
        try:
            if URL[:3] == 'ftp':
                self.loadFTP(URL, localfile, timeout, proxy, content_type, retries)
            else:
                self.loadHTTP(URL, localfile, timeout, proxy, content_type, retries)
        except:
            print('SMARTCACHE url fail ' + URL);  # print('proxy'+proxy); #  print to log
        # this will creat a new cached file from the existing file and make it usable
        if os.path.exists(localfile + ".old") == True:
            if os.path.exists(localfile) == False:  # see that the new file was not loaded from the server
                open(localfile, 'a').close()  # create an empty file
            old_ff = open(localfile + ".old", 'r')
            if (os.path.getsize(localfile) == 0) or ((os.path.getsize(localfile) < 300) and (
                (os.path.getsize(localfile) + 200) < os.path.getsize(
                        localfile + ".old"))):  # 0: #check to see if there is any data in the file
                old_ff.close()
                try:
                    with open(localfile + ".old", 'r') as old_file:  # opens the old file with auto close
                        for line in old_file:
                            with open(localfile, 'a+') as new_file:  # open the new file with autoclose
                                new_file.write(line)  # copies the line in old_file to new_file
                                cachedFlag = True
                                if hasattr(self, 'MainWindow'):
                                    if hasattr(self.MainWindow, 'logo'):
                                        try:
                                            self.MainWindow.imgProtocol.setImage(imageBrowse['Rewrite'])
                                        except:
                                            pass
                    # xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( 'Server Error', 'You are reading cached files', 5000 ) )
                    # dialog=xbmcgui.Dialog(); dialog.ok("DEBUG ","Reading old cached page", str(URL));print"DEBUG CFL 284 Reading old cached page "+str(URL)
                    with open(localfile, 'r')as newFile:
                        self.data = newFile.read();
                        self.state = 0  # success
                except Exception, e:
                    print 'Error ' + str(e);self.state = -3  # failed
            else:
                old_ff.close()
            
            os.remove(localfile + ".old")
        elif os.path.exists(localfile) == False and os.path.exists(localfile + ".old") == False:
            self.state = -3
        
        if cachedFlag == False:
            try:
                if URL.lower().startswith(nxserver_URL.lower()):
                    for ZZZA, ZZZB in CachedPagesAndTimes:
                        if URL.lower() == ZZZB:
                            expires = (ZZZA * 60) * 60
                with open(localfile, 'r') as data:
                    for line in data:
                        if line and line[0] != '#':
                            index = line.find('=')
                            if index != -1:
                                key = line[:index]
                                value = line[index + 1:]
                                if key == 'expires':
                                    expires = ((int(
                                        value) * 60) * 60);  # dialog=xbmcgui.Dialog(); dialog.ok('CFL 238','key= '+str(key),'value='+str(value),'expires'+str(expires))
                                    break
                                elif key == 'type':
                                    break
                data.close()
                TestBug({"url": URL.lower(), 'expires': expires})
            except Exception, e:
                print'DEBUG CFL312 expiration error' + str(e); expires = DefaultCachedExpires  # 3600
        else:
            expires = DefaultCachedExpires  # 3600
        
        self.metadata["expires"] = str(expires)
        self.writeMetaData(localfile)
        if cachedFlag == False:
            try:
                with open(localfile, 'r')as f:
                    self.data = f.read();
                    self.state = 0
            except:
                self.state = -3  # failed
            
            # if hasattr(self,'MainWindow'):
            #    if hasattr(self.MainWindow,'logo'):
            #        TestBug({'From':'loadSmartCache: near end','MainWindow':'Was Found','cachedFlag':cachedFlag,'content_type':content_type,'proxy':proxy,'URL':URL,'localfile':localfile})
            #        if cachedFlag==True:
            #            self.MainWindow.logo.setVisible(False)
            #        else:
            #            self.MainWindow.logo.setVisible(True)
            # else:
            #        TestBug({'From':'loadSmartCache: near end','MainWindow':'Not Found','cachedFlag':cachedFlag,'content_type':content_type,'proxy':proxy,'URL':URL,'localfile':localfile})
            # end of function
    
    ######################################################################
    # Description: Downloads a file in case of URL and returns absolute
    #              path to the local file.
    # @todo: Fill parameters
    # Parameters : URL=source, localfile=destination
    # Return     : -
    ######################################################################           
    def loadHTTP(self, URL, localfile='', timeout=0, proxy="", content_type='', retries=0):  # proxy="CACHING"
        if timeout != 0:
            socket_setdefaulttimeout(timeout)
        self.state = -1  # failure
        counter = 0
        
        while (counter <= retries) and (self.state != 0):
            counter = counter + 1
            try:
                cookies = ''
                if URL.find(nxserver_URL) != -1:
                    cookies = 'platform=' + platform + '; version=' + Version + '.' + SubVersion
                    cookies = cookies + '; nxid=' + nxserver.user_id
                    values = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)', 'Cookie': cookies}
                else:
                    values = {'User-Agent': 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)'}
                    # print URL #print 'values =    '+str(values)
                
                ### check if a differant lists and increase their timeout values
                if timeout != 0:
                    t_timer = timeout  # allow differant values passed in
                else:
                    t_timer = url_open_timeout  # 20
                    for var in '/search/', '/user_list', '/update', '/new':
                        if var in URL and var == '/search/':
                            t_timer = int(t_timer) * 3; break  # t_timer= 60; break
                        elif var in URL:
                            t_timer = int(t_timer) * 2  # t_timer=40
                
                # if 'navixtreme'  in URL: values = {'jibberish'} ###### used to stop from connecting to navi server
                req = urllib2.Request(URL, None, values);  # TestBug('req= '+str(req))
                f = urllib2.urlopen(req, None, timeout=t_timer)  ######### where it hangs and faults if server is down
                
                headers = f.info()
                type = headers.get('Content-Type', '');  # type=headers['Content-Type']
                
                if (content_type != '') and (type.find(content_type) == -1):
                    # unexpected type
                    if timeout != 0:
                        socket_setdefaulttimeout(url_open_timeout)
                    self.state = -1  # failed
                    break  # do not try again
                
                # open the destination file
                self.data = f.read()
                file = open(localfile, "wb")
                file.write(self.data)
                file.close()
                f.close()
                
                self.localfile = localfile
                self.state = 0  # success
            
            except Exception, e:
                if hasattr(e, 'code'):
                    if (not '.png' in URL.lower()) and (not '.jpg' in URL.lower()) and (
                    not '.jpeg' in URL.lower()) and (not '.bmp' in URL.lower()) and (not '.gif' in URL.lower()) and (
                    not '.psx' in URL.lower()):
                        TestBug('The server could not fulfill the request.  URL=' + str(URL))
                        TestBug(['Error code: ', e.code])
                elif hasattr(e, 'reason'):
                    if (not '.png' in URL.lower()) and (not '.jpg' in URL.lower()) and (
                    not '.jpeg' in URL.lower()) and (not '.bmp' in URL.lower()) and (not '.gif' in URL.lower()) and (
                    not '.psx' in URL.lower()):
                        # Message("Failed to reach the server. Reason: %s"%(e.reason))
                        TestBug('failed to get URL=' + str(URL))
                        TestBug(['Reason: ', e.reason])
                else:
                    if (not '.png' in URL.lower()) and (not '.jpg' in URL.lower()) and (
                    not '.jpeg' in URL.lower()) and (not '.bmp' in URL.lower()) and (not '.gif' in URL.lower()) and (
                    not '.psx' in URL.lower()):
                        TestBug(['Error CFL failed to get URL=' + URL, str(e)])
                self.state = -1  # failed
                print 'Error CFL 406 ' + str(e), 'Errored URL= ' + str(URL)
        
        if timeout != 0:
            socket_setdefaulttimeout(url_open_timeout)
            
            # end function
    
    ######################################################################
    # Description: Downloads a file in case of URL and returns absolute
    #              path to the local file.
    # @todo: Fill parameters
    # Parameters : URL=source, localfile=destination
    # Return     : -
    ######################################################################        
    def loadFTP(self, URL, localfile='', timeout=0, proxy="CACHING", content_type='', retries=0):
        self.state = 0  # success
        
        # Parse URL according RFC 1738: ftp://user:password@host:port/path
        # There is no standard Python funcion to split these URL's.
        username = ''
        password = ''
        port = 21
        
        # check for username, password
        index = URL.find('@')
        if index != -1:
            index2 = URL.find(':', 6, index)
            if index2 != -1:
                username = URL[6:index2]
                print 'user: ' + username
                password = URL[index2 + 1:index]
                print 'password: ' + password
            URL = URL[index + 1:]
        else:
            URL = URL[6:]
        
        # check for host
        index = URL.find('/')
        if index != -1:
            host = URL[:index]
            path = URL[index:]
        else:
            host = URL
            path = ''
        
        # retrieve the port
        index = host.find(':')
        if index != -1:
            port = int(host[index + 1:])
            host = host[:index]
        
        print 'host: ' + host
        print 'port: ' + str(port)
        
        # split path and file
        index = path.rfind('/')
        if index != -1:
            file = path[index + 1:]
            path = path[:index]
        else:
            file = ''
        
        print 'path: ' + path
        print 'file: ' + file
        
        try:
            self.f = ftplib.FTP()
            self.f.connect(host, port)
        except (socket.error, socket.gaierror), e:
            print 'ERROR: cannot reach "%s"' % host
            self.state = -1  # failed to download the file
            return
        
        print '*** Connected to host "%s"' % host
        
        try:
            if username != '':
                self.f.login(username, password)
            else:
                self.f.login()
        except ftplib.error_perm:
            print 'ERROR: cannot login anonymously'
            self.f.quit()
            self.state = -1  # failed to download the file
            return
        
        print '*** Logged in as "anonymous"'
        
        try:
            self.f.cwd(path)
        except ftplib.error_perm:
            print 'ERROR: cannot CD to "%s"' % path
            self.f.quit()
            self.state = -1  # failed to download the file
            return
        
        print '*** Changed to "%s" folder' % path
        
        # retrieve the file
        self.bytes = 0
        # self.file=open(localfile,'wb')
        
        try:
            self.f.retrbinary('RETR %s' % file, open(localfile, 'wb').write)
            self.localfile = localfile
            # self.size=self.f.size(file)
            # self.size_MB=float(self.size) / (1024 * 1024)
            # self.percent2=0
            # self.f.retrbinary('RETR %s'%file,self.download_fileFTP_callback)
        except ftplib.error_perm:
            print 'ERROR: cannot read file "%s"' % file
            os.unlink(self.file)
            self.state = -1  # failed
        else:
            print '*** Downloaded "%s" to CWD' % file
        
        self.f.quit()
        
        # end function
    
    ######################################################################
    # Description: Read the meta data of the file
    # Parameters : file: the file for which to read metadata
    # Return     : -
    ######################################################################        
    def readMetaData(self, file):
        try:
            f = open(file + '.info', 'r')
            # read was only returning a single string - need array
            metafile = f.readlines()
            f.close()
            for line in metafile:
                # name,var=line.partition("=")[::2]
                
                # won't handle multiple "=", but works in XBMC4Xbox
                name, var = line.strip().split("=")
                self.metadata[name.strip()] = var
        except Exception, e:
            print'Error EXCEPTION ' + str(e)
            return
    
    ######################################################################
    # Description: Write the meta data of the file
    # Parameters : file: the file for which to write metadata
    # Return     : -
    ######################################################################
    def writeMetaData(self, file):
        self.metadata['test'] = 'stuff'
        f = open(file + '.info', 'w')
        for line in self.metadata:
            f.write(line + '=' + self.metadata[line] + '\n')
        f.close()
    
    ######################################################################
    # Description: Write the meta data of the file
    # Parameters : file: the file for which to write metadata
    # Return     : -
    ######################################################################
    def deleteMetaData(self, file):
        if os.path.exists(file + '.info') == True:
            os.remove(file + '.info')
