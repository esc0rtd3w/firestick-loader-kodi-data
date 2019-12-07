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
###############################################################################

#############################################################################
#
# CServer:
# Handles all services with the Navi-Xtreme server.
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
from settings import *
from CFileLoader import *
from libs2 import *
from CDialogLogin import *
from CDialogRating import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

######################################################################
# Description: Text viewer
######################################################################
class CServer: 
    def __init__(self):
        
        #public member of CServer class.
        self.user_id = ''
        
        #read the stored user ID
        self.read_user_id()

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################            
    def login(self): ## http://www.navixtreme.com/members/
        ## http://www.navixtreme.com/members/
        ## POST /members/ action=takelogin&ajax=1&username=###[]###&password=###[]###&rndval=###[numbers]###
        ## 
        ## 
        ## 
        keyboard = xbmc.Keyboard('', 'Enter User name')
        keyboard.doModal()
        if (keyboard.isConfirmed() != True):
            return -2
        
        username = keyboard.getText()
        
        keyboard = xbmc.Keyboard('', 'Enter Password')
        keyboard.doModal()
        if (keyboard.isConfirmed() != True):
            return -2
        
        password = keyboard.getText()
        
        #login to the Navi-X server
        self.user_id=self.nxLogin(username,password)
        self.user_id=str(self.user_id).strip()
        if (self.user_id=='') or (self.user_id=="<class 'urllib2.HTTPError'>") or (self.user_id=="<type 'exceptions.ValueError'>"):
            #failed
            print {'user_id':self.user_id}
            self.user_id=''
            self.save_user_id()
            #xbmcgui.Dialog().ok("Login",'Failed',' ',' ')
            return -1
        elif len(self.user_id)==48:
            #	xbmcgui.Dialog().ok("Login",'Successful',' ',' ')
            print "Login to the NXServer was successful"
            
            #save the returned user ID
            self.save_user_id()
            #success   
            return 0
        else:
            #failed
            print {'user_id':self.user_id}
            self.user_id=''
            self.save_user_id()
            #xbmcgui.Dialog().ok("Login",'Failed',' ',' ')
            return -1
        
    ######################################################################
    # Description: Login function for Navi-Xtreme login.
    # Parameters : username: user name
    #              password: user password
    # Return     : blowfish-encrypted string identifying the user for 
    #              saving locally, or an empty string if the login failed.
    ######################################################################  
    def nxLogin(self, username, password, LoginUrl='http://www.navixtreme.com/members/'):
        ## POST /members/ action=takelogin&ajax=1&username=###[]###&password=###[]###&rndval=###[numbers]###
        LoginUrl='http://www.navixtreme.com/login/'
        #return str(getRemote(LoginUrl,{'method':'post',
        #    'postdata':urllib.urlencode({'username':username,'password':password,'action':'takelogin','ajax':'1'})
        #})['content'])
        #try: 
        print'Attempting to login'
        html=UrlDoPost(LoginUrl,{'username':username,'password':password,'action':'takelogin','ajax':'1','rndval':''})
        #except: html=''
        print 'Length: '+str(len(html)); #print html
        return html
        #return str(getRemote('http://www.navixtreme.com/login/',{
        #    'method':'post',
        #    'postdata':urllib.urlencode({'username':username,'password':password})
        #})['content'])
        
    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################                     
    def logout(self): ## http://www.navixtreme.com/members/?action=signout
        #empty the user ID
        self.user_id=''
        self.save_user_id()
        
    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################             
    def is_user_logged_in(self):
        self.user_id=str(self.user_id).strip()
        if (self.user_id != '') and (self.user_id !="<class 'urllib2.HTTPError'>") or (self.user_id=="<type 'exceptions.ValueError'>"):
            if (len(self.user_id) != 48): return False
            return True
        return False

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################            
    def rate_item(self, mediaitem):    
        #rate = CDialogRating("CRatingskin.xml", os.getcwd())
        rate = CDialogRating("CRatingskin2.xml", addon.getAddonInfo('path'))
        rate.doModal()
        if rate.state != 0:
            return -2
                
        if self.is_user_logged_in() == False:
            dialog = xbmcgui.Dialog()
            dialog.ok(" Error", "You are not logged in.")
            return -1

        #login to the Navi-X server
        result = self.nxrate_item(mediaitem, rate.rating)

    ######################################################################
    # Description: -
    # Parameters : mediaitem: CMediaItem instance to rate
    #              rating = value [0-5]
    # Return     : -
    # API Return : Success: value [0-5] representing the new average rating
    #              Failure: error message string
    ######################################################################      
    def nxrate_item(self, mediaitem, rating):  
        result=getRemote('http://www.navixtreme.com/rate/',{
            'method':'post',
            'postdata':urllib.urlencode({'url':mediaitem.URL,'rating':rating}),
            'cookie':'nxid='+nxserver.user_id
        })['content']

        dialog = xbmcgui.Dialog()                            
        p=re.compile('^\d$')
        match=p.search(result)
        if match:
            dialog.ok(" Rate", "Rating Successful.")
            mediaitem.rating=result
        else:
            dialog.ok(" Rate", result)

        return 0
    
    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ######################################################################     
    def read_user_id(self):
        try:
            f=open(RootDir + 'user_id.dat', 'r')
            self.user_id = f.read()
            f.close()
        except IOError:
            return   

    ######################################################################
    # Description: -
    # Parameters : -
    # Return     : -
    ###################################################################### 
    def save_user_id(self):
        f=open(RootDir + 'user_id.dat', 'w')
        f.write(self.user_id)    
        f.close()
        pass
 

#Create server instance here and use it as a global variable for all other components that import CServer.py.
global nxserver
nxserver = CServer() 

global re_server
re_server = re.compile('^[^:]+://(?:www\.)?([^/]+)')