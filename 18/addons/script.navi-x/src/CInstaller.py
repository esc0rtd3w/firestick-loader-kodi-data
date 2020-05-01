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
# CInstaller:
# Intaller for scripts and plugins.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import zipfile
from settings import *
from CFileLoader import *
from CURLLoader import *

from libs2 import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

######################################################################
# Description: Handles installation of scripts and plugins
######################################################################
class CInstaller(xbmcgui.Window):

    ######################################################################
    # Description: Handles Installation of a scripts ZIP file.
    # Parameters : URL = URL of the file
    #              mediaitem=CMediaItem object to load
    # Return     : -
    ######################################################################
    def InstallScript(self, URL='', mediaitem=CMediaItem()):
        if URL != '':
            self.URL = URL
        else:
            self.URL = mediaitem.URL
        
        urlopener = CURLLoader()
        result = urlopener.urlopen(self.URL, mediaitem)
        if result["code"] == 0:
            self.URL = urlopener.loc_url
        
        SetInfoText("Downloading... ", setlock=True)
        
        #download the file.
        loader = CFileLoader2()
        loader.load(self.URL, tempCacheDir + 'script.zip')
        if loader.state != 0:
            return -2
        filename = loader.localfile

        SetInfoText("Installing... ", setlock=True)

        result = self.unzip_file_into_dir(filename, scriptDir)   
        
        return result
                
    ######################################################################
    # Description: Handles Installation of a plugin ZIP file.
    # Parameters : URL = URL of the file
    #              mediaitem=CMediaItem object to load
    # Return     : -
    ######################################################################
    def InstallPlugin(self,URL='',mediaitem=CMediaItem()):            
        if URL != '':
            self.URL=URL
        else:
            self.URL=mediaitem.URL
        
        urlopener=CURLLoader()
        result=urlopener.urlopen(self.URL,mediaitem)
        if result["code"] == 0:
            self.URL=urlopener.loc_url
        
        
        #retrieve the type of plugin
        index=mediaitem.type.find(":")
        if index != -1:
            subdir=mediaitem.type[index+1:]+'\\'
        else:
            subdir=''
        
        SetInfoText("Downloading... ",setlock=True)
        
        #download the file.
        loader=CFileLoader2()
        loader.load(self.URL,tempCacheDir+'plugin.zip',content_type='zip')
        if loader.state != 0:
            if loader.state == -2:
                dialog=xbmcgui.Dialog()
                dialog.ok(" Installer","Failed. Not a ZIP file.","Use the standard Download feature.")
            return -2
        filename=loader.localfile
        
        SetInfoText("Installing... ", setlock=True)
        
        result=self.unzip_file_into_dir(filename,pluginDir+subdir)
        
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()"); 
        
        return result
        
    ######################################################################
    # Description: Handles Installation of a skin ZIP file.
    # Parameters : URL = URL of the file
    #              mediaitem=CMediaItem object to load
    # Return     : -
    ######################################################################
    def InstallSkin(self, URL='', mediaitem=CMediaItem()):
        if URL != '':
            self.URL = URL
        else:
            self.URL = mediaitem.URL
        
        urlopener = CURLLoader()
        result = urlopener.urlopen(self.URL, mediaitem)
        if result["code"] == 0:
            self.URL = urlopener.loc_url
        
        SetInfoText("Downloading... ", setlock=True)
        
        #download the file.
        loader = CFileLoader2()
        loader.load(self.URL, tempCacheDir + 'skin.zip')
        if loader.state != 0:
            return -2
        filename = loader.localfile

        SetInfoText("Installing... ", setlock=True)

        result = self.unzip_file_into_dir(filename, skinDir)   

        return result

    ######################################################################
    # Description: Handles Installation of a scripts ZIP file.
    # Parameters : URL = URL of the file
    #              mediaitem=CMediaItem object to load
    # Return     : -
    ######################################################################
    def InstallNaviX(self, URL='', mediaitem=CMediaItem()):
        if URL != '':
            self.URL = URL
        else:
            self.URL = mediaitem.URL
        
        urlopener = CURLLoader()
        result = urlopener.urlopen(self.URL, mediaitem)
        if result["code"] == 0:
            self.URL = urlopener.loc_url
        
        SetInfoText("Downloading... ", setlock=True)
        
        #download the file.
        loader = CFileLoader2()
        loader.load(self.URL, tempCacheDir + 'script.zip')
        if loader.state != 0:
            return -2
        filename = loader.localfile

        SetInfoText("Installing... ", setlock=True)

        #determine the install dir based on the current Navi-X directory (root)
        if RootDir[0] == '/':
            pos =   RootDir.rfind("/",0,-1)
        else:
            pos =   RootDir.rfind("\\",0,-1)
            
        if pos != -1:
            InstallDir = RootDir[0:pos+1]

            print "Installing Navi-X in: " + InstallDir

            result = self.unzip_file_into_dir(filename, InstallDir)
            
            if result == 0: #remove pyo files (needed for XBMC Dharma)
                self.delPYOFiles(RootDir+'src')
            
        else:
            result = -1
        
        return result


    ######################################################################
    # Description: Unzip a file into a dir
    # Parameters : file = the zip file
    #              dir = destination directory
    # Return     : -
    ######################################################################                    
    def unzip_file_into_dir(self,file,dir):
        chk_confirmation=False
        dir=xbmc.translatePath(dir)
        print {'folder':dir,'file':file}
        if os.path.exists(dir)==False:
            try:
                os.makedirs(dir) #create the directory
            except IOError:
                return -1 #failure
            
        zfobj = zipfile.ZipFile(file)

        for name in zfobj.namelist():
            index = name.rfind('/')
            if index != -1:
                #entry contains path
                if os.path.exists(dir+name[:index+1]):
                    #directory exists
                    if chk_confirmation == False:
                        dialog = xbmcgui.Dialog()
                        if dialog.yesno("Installer", "Directory already exists, continue?") == False:
                            return -1
                else:
                    #directory does not exist. Create it.
                    try:
                        #create the directory structure
                        os.makedirs(os.path.join(dir, name[:index+1]))
                    except IOError:
                        return -1 #failure
                    
            if not name.endswith('/'):
                #entry contains a filename
                try:
                    outfile = open(os.path.join(dir, name), 'wb')
                    outfile.write(zfobj.read(name))
                    outfile.close()
                except IOError:
                    pass #There was a problem. Continue...
                 
            chk_confirmation = True
        return 0 #succesful

    ######################################################################
    # Description: Deletes all pyo files in a given folder and sub-folders.
    #              Note that the sub-folders itself are not deleted.
    # Parameters : folder=path to local folder
    # Return     : -
    ######################################################################
    def delPYOFiles(self, folder):
        try:        
            for root, dirs, files in os.walk(folder , topdown=False):
                for name in files:
                    filename = os.path.join(root, name)
                    if filename[-4:] == ".pyo":
                        os.remove(filename)
        except IOError:
            return
            
            
            