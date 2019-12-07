#
#      Copyright (C) 2014 Blazetamer
#      
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
#

"""
The following variables MUST be set in your default.py
"""
###########Author Info Variable##########

provider_name = None


###########Below is the add-on variables########

addon_id_name =None
addon_xml_loca = None
addon_name =None
addon_zip_loca =None


##########Below is the repo variables###########

repo_name = None
repo_xml_loca =None
repo_zip_loca =None
repo_entry_version =None





import urllib2,re,xbmcplugin,xbmc,xbmcaddon,os,sys,time,shutil
import xbmcgui
import urllib
import zipfile

def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")       

#====================Start update procedures=======================

def STARTUP():
        myversion=CheckVersion()
        if myversion == True:
                        print 'Version is TRUE'
        
        if myversion ==False:
                        print 'Version is FALSE'
        return


#Start Repo Check =======        
def CheckVersion():

     try:     
         repover=xbmc.translatePath(os.path.join('special://home/addons/'+repo_name,'addon.xml'))
         source= open( repover, mode = 'r' )
         link = source . read( )
         source . close ( )
         match=re.compile('" version="(.+?)" provider-name="'+provider_name+'"').findall(link)
         for repovernum in match:
                  print 'Original Repo is ' + repovernum
         try:
             link=OPEN_URL(repo_xml_loca)
         except:
             link='nill'

         link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
         match=re.compile('" version="(.+?)" provider-name="'+provider_name+'"').findall(link)
         if len(match)>0:
             for new_repovernum in match:
                
                if repovernum < str(match[0]):
                     dialog = xbmcgui.Dialog()
                     confirm=xbmcgui.Dialog().yesno("[B]"+provider_name+"'s Repo - Update Available![/B]", "                      "+provider_name+"'s  Repo is outdated." ,'                    The current available version is '+str(match[0]),'                         Would you like to update now?',"Cancel","Update")
                     
                     if confirm:
                             UPDATEREPO(repo_name,new_repovernum)
     except Exception:
        print 'Attempt to find addon.xml failed, Installing Add-ons Repo'
    
        UPDATEREPO(repo_name,repo_entry_version)                          
                             
#END REPO CHECK=======
#Start Add-on Check============
     try:
         print "HERE WE GO ADDON"
         curver=xbmc.translatePath(os.path.join('special://home/addons/'+addon_id_name,'addon.xml'))    
         source= open( curver, mode = 'r' )
         link = source . read( )
         source . close ( )
         match=re.compile('" version="(.+?)".+? provider-name="'+provider_name+'"').findall(link)
         for vernum in match:
                 print 'Original Version is ' + vernum
         try:
             link=OPEN_URL(addon_xml_loca)
         except:
             link='nill'

         link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
         match=re.compile('" version="(.+?)".+? provider-name="'+provider_name+'"').findall(link)
         if len(match)>0:
             for new_vernum in match:    
                if vernum < str(match[0]):
                     dialog = xbmcgui.Dialog()
                     confirm=xbmcgui.Dialog().yesno('[B]'+addon_name+'  Update Available![/B]', "                              Your version is outdated." ,'                    The current available version is '+str(match[0]),'                         Would you like to update now?',"Cancel","Update")
                     if confirm:
                             UPDATEFILES(addon_id_name,new_vernum)
                     return False
             else:
                     return True
         
         else:
             return False
     except Exception:
        print 'Attempt to find addon.xml failed, Please install Add-on from repo'
        return True



def UPDATEFILES(addon_id_name,new_vernum):

        url= addon_zip_loca+'/'+addon_id_name+'-'+new_vernum+'.zip'
        path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
        addonpath=xbmc.translatePath(os.path.join('special://','home/addons'))
        name= addon_id_name+'.update.zip'
        lib=os.path.join(path,name)
        try: os.remove(lib)
        except: pass
        download(url, lib, '')
        xall(lib,addonpath,'')
        LogNotify('Update Complete', 'Resetting Menus', '5000', '')
        return

def UPDATEREPO(repo_name,new_repovernum=''):
        repourl=repo_zip_loca+'/'+repo_name+'-'+new_repovernum+'.zip'
        print "FIRST REPO URL IS "+repourl
        url=repo_zip_loca+'/'+repo_name+'-'+new_repovernum+'.zip'
        print "REPO URL IS "+url
        path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
        addonpath=xbmc.translatePath(os.path.join('special://','home/addons'))
        name= repo_name+'.update.zip'
        lib=os.path.join(path,name)
        try: os.remove(lib)
        except: pass
        download(url, lib, '')
        xall(lib,addonpath,'')
        LogNotify('Repo Update Complete', 'Thanks for Updating', '5000', '')
        return    
        





#==============Downloader Function=================
def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Status...","Checking Installation",' ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Canceled")
        dp.close()

#===================Extract Function======================
def xall(_in, _out, dp=None):
    if dp:
        return allWithProgress(_in, _out, dp)

    return allNoProgress(_in, _out)
        

def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
        return False

    return True


def allWithProgress(_in, _out, dp):

    zin = zipfile.ZipFile(_in,  'r')

    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update))
            zin.extract(item, _out)
    except Exception, e:
        print str(e)
        return False

    return True
        
        


