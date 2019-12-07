# -*- coding: utf-8 -*-

# Main Module by: Blazetamer

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,htmlcleaner
from metahandler import metahandlers

try:
        from addon.common.addon import Addon

except:
        from t0mm0.common.addon import Addon
addon_id = 'plugin.video.moviedb'

addon = Addon(addon_id, sys.argv)
try:
        from addon.common.net import Net

except:  
        from t0mm0.common.net import Net
net = Net()
        

import threading

try:
     import StorageServer
except:
     import storageserverdummy as StorageServer
import time
selfAddon = xbmcaddon.Addon(id=addon_id)
# Cache  
cache = StorageServer.StorageServer("MovieDB", 0)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
art = '' 
supportsite = 'tvaddons.ag'
#=========Download Thread Module by: Blazetamer and o9r1sh1=========================
settings = xbmcaddon.Addon(id='plugin.video.moviedb')     
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
ext = addon.queries.get('ext', '')
console = addon.queries.get('console', '')
dlfoldername = addon.queries.get('dlfoldername', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
fanart = addon.queries.get('fanart', '')
art = addon.queries.get('art', '')
sound = addon.queries.get('sound', '')




download_path = settings.getSetting('download_folder')
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

#================Threading===========================================
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link

############## Start DownloadThread Class ################
class downloadThread (threading.Thread):
    def __init__(self, name, url, thumb, console, ext):
        threading.Thread.__init__(self)
        self.thumb = thumb
        self.kill = False
        #self.kill = threading.Event()

    def kill(self):
        self.kill = True
        
    def stop(self):
        print ('killing queue ') + str(self.kill)
        self.kill = True
        print ('killing queue ') + str(self.kill)
        
    def run(self):
        queue = cache.get('queue')
        if queue:
            queue_items = sorted(eval(queue), key=lambda item: item[1])
            for item in queue_items:
                self.name = item[0]
                self.url = item[1]
                self.ext = item[3]
                self.console = item[4]
                thumb = item[2]


                #print queue_items               
                self.path = download_path + self.console
                if not os.path.exists(self.path):
                    os.makedirs(self.path)

                self.file_name = self.name + self.ext

                addon.show_small_popup(title='[COLOR gold]Downloads Started[/COLOR]', msg=self.name + ' Is Downloading', delay=int(7000), image= 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png')

                u = urllib2.urlopen(self.url)
                meta = u.info()
                print meta
                if 'Content-Length' not in meta:
                    file_size_string = 'Unknown'
                    file_size = 1  #
                else:
                    file_size_string = ''
                    file_size =  int(meta.getheaders("Content-Length")[0])
                    #print file_size
                f = open(os.path.join(self.path,self.file_name), 'ab')                    
                existSize = os.path.getsize(os.path.join(self.path,self.file_name))
                if file_size_string != 'Unknown':
                    # only download the remaining bytes using byte range
                    #for RangeEntry in 'Ranges','Range','':
                    for RangeEntry in 'Ranges','Range','':        
                        headers = u.info()
                        if RangeEntry != '':
                            #print "TRYING BYTE SIZES"    
                            try:
                                
                                # this request sets the pointer to where you want to start
                                req = urllib2.Request(self.url)
                                # reopen url with preset byte range in header
                                req.headers["Range"] = 'bytes=%s-' %existSize
                                u = urllib2.urlopen(req)
                                # Set the begining write point
                                file_size_dl = existSize
                                break
                            except Exception, e:
                                file_size_dl = 0
                                print '\t\t error byte range not supported ' + str(e)  # Expected error: HTTP Error 416: Requested Range Not Satisfiable'
                else:
                    print ('\t\t\t Remote file size is unknown')
                    file_size_dl = 0  # byte range not supported continue as usual
                    
                # Number of bytes to read at a time
                block_sz = 500 * 1024

                # Download init
                starttime = time.time()
                startSize = file_size_dl
                
                
                while (file_size_string == 'Unknown' or (existSize <= file_size and file_size >= 1)) \
                          and queue and not self.kill:
                        #print ('\t\t\t checking kill ') + str(self.kill)
                        # keep from adding empty bytes after end of file
                        if (existSize + block_sz) > file_size and file_size > 1:
                            block_sz = file_size - existSize  # only read the remainder
                        buffer = u.read(block_sz)
                        if buffer == '':  # end of file
                            break
                        # dont overwrite existing data
                        if file_size_dl >= existSize:
                                f.write(buffer)
                        file_size_dl += block_sz 
                        
                        try:  # calculate the percentage downloaded                        
                            deltatime = time.time() - starttime
                            if file_size <= 1 or file_size_string == 'Unknown' :
                                if deltatime >= 150:  # in seconds. update display every 2.5 min
                                    addon.show_small_popup(title=self.name, msg='Downloading...',delay=int(10), image=thumb)
                            else:
                                percent = file_size_dl * 100 / file_size
                                if percent in range(10,101,10):
                                    #Actual size info
                                    totalsize = file_size /1000000
                                    if totalsize < 1000:
                                        full_size = str(totalsize) +"MB"
                                    else  :
                                         totalgbsize = totalsize /float(1000)
                                         full_size =str(totalgbsize) +"GB"
                                    truesize = file_size_dl /1000000
                                    if truesize < 1000:
                                        dl_size = str(truesize) +"MB"
                                    else  :
                                         truegbsize = truesize /float(1000)
                                         dl_size =str(truegbsize) +"GB"
                                    #Actual Size Info    
                                    addon.show_small_popup(title=self.name, msg= str(percent) + '% Complete of '+ full_size,delay=int(10),image= 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png')



                                    #calculate the download speed
                                    deltasize = file_size_dl - startSize
                                    dlspeed = (deltasize / 1024) / deltatime                        

                                    starttime = time.time()
                                    startSize = file_size_dl
                                    #print ('\t\t\t Download Speed= ' + str(dlspeed) + ' kbs')
       
                        except Exception,e:
                           print('\t\t\t ERROR DISPLAY ' + str(e))
                        

                try:
                    addon.show_small_popup(title='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed', delay=int(5000), image= 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png')


                except:
                    addon.show_small_popup(title='Error', msg=self.name + ' Failed To Download File', delay=int(5000), image=thumb)
                    print 'ERROR - File Failed To Download'
                   
                f.close()

                removeFromQueue(self.name,self.url,thumb,self.ext,self.console)
                 
                addon.show_small_popup(title='[COLOR gold]Process Complete[/COLOR]', msg=self.name + ' is in your downloads folder', delay=int(5000), image= 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png')



                

#END CRZEN DL FUNCTION


class downloadThreadOLD (threading.Thread):
    def __init__(self, name, url, thumb, console, ext):
        threading.Thread.__init__(self)
        self.thumb = thumb
          
    def run(self):
     queue = cache.get('queue')
  
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               thumb = item[2]
                                
               self.path = download_path + self.console
               if not os.path.exists(self.path):
                    os.makedirs(self.path)
  
               self.file_name = self.name + self.ext
  
               addon.show_small_popup(title='[COLOR gold]Downloads Started[/COLOR]', msg=self.name + ' Is Downloading', delay=int(7000), image=thumb)
               u = urllib.urlopen(self.url)
               f = open(os.path.join(self.path,self.file_name), 'wb')
               meta = u.info()
               file_size = int(meta.getheaders("Content-Length")[0])
  
               file_size_dl = 0
               block_sz = 8192
  
               
                 
               while True:
                   buffer = u.read(block_sz)
                   if not buffer:
                       break
  
                   file_size_dl += len(buffer)
                   f.write(buffer)
                   status = int( file_size_dl * 1000. / file_size)
                   thumb = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png'
                   if status > 99 and status < 101:
                         addon.show_small_popup(title=self.name, msg='10% Complete',delay=int(10), image=thumb)

                   elif status > 199 and status < 201:
                         addon.show_small_popup(title=self.name, msg='20% Complete',delay=int(10), image=thumb)
                         
                   elif status > 299 and status < 301:
                         addon.show_small_popup(title=self.name, msg='30% Complete',delay=int(10), image=thumb)

                   elif status > 399 and status < 401:
                         addon.show_small_popup(title=self.name, msg='40% Complete',delay=int(10), image=thumb)

                   elif status > 499 and status < 501:
                         addon.show_small_popup(title=self.name, msg='50% Complete',delay=int(10), image=thumb)

                   elif status > 599 and status < 601:
                         addon.show_small_popup(title=self.name, msg='60% Complete',delay=int(10), image=thumb)      
                   
                   elif status > 699 and status < 701:
                         addon.show_small_popup(title=self.name, msg='70% Complete',delay=int(10), image=thumb)

                   elif status > 799 and status < 801:
                         addon.show_small_popup(title=self.name, msg='80% Complete',delay=int(10), image=thumb)

                   elif status > 899 and status < 901:
                         addon.show_small_popup(title=self.name, msg='90% Complete',delay=int(10), image=thumb)

                   elif status > 994 and status < 996:
                         addon.show_small_popup(title=self.name, msg='95% Complete',delay=int(10), image=thumb)       
                   
                   
               f.close()
  
               removeFromQueue(self.name,self.url,thumb,self.ext,self.console)
  
  
               try:
                    addon.show_small_popup(title='[COLOR gold]Download Complete[/COLOR]', msg=self.name + ' Completed', delay=int(5000), image=thumb)
               except:
                    addon.show_small_popup(title='Error', msg=self.name + ' Failed To Download File', delay=int(5000), image=thumb)
                    print 'ERROR - File Failed To Download'
  
                 
               addon.show_small_popup(title='[COLOR gold]Process Complete[/COLOR]', msg=self.name + ' is in your downloads folder', delay=int(5000), image=thumb) 

               


############## End DownloadThread Class ################
def addDirpop(name,url,mode,thumb,fanart,sound):
        fanart = fanart
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'fanart':fanart, 'sound':sound}        
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&sound="+urllib.quote_plus(sound)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": ''} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addQDir(name,url,mode,thumb,console):
     contextMenuItems = []

     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,'console':console, 'ext':ext}

     contextMenuItems.append(('[COLOR red]Remove From Queue[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removeFromQueue', 'name': name,'url': url,'thumb': thumb,'ext': ext,'console': console})))

     addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)
     
def addToQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     queue_items = []
     if queue:
          queue_items = eval(queue)
          if queue_items:
               if (name,url,thumb,ext,console) in queue_items:
                    addon.show_small_popup(title='[COLOR red]Item Already In Your Queue[/COLOR]', msg=name + ' Is Already In Your Download Queue', delay=int(5000), image=thumb)
                    return
     queue_items.append((name,url,thumb,ext,console))         
     cache.set('queue', str(queue_items))
     addon.show_small_popup(title='[COLOR gold]Item Added To Your Queue [/COLOR]', msg=name + ' Was Added To Your Download Queue', delay=int(5000), image=thumb)

def viewQueue():
     addDir('[COLOR blue]Start Downloads[/COLOR]','none','download',artwork +'downloadsstart.jpg','','')
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          for item in queue_items:
               addQDir(item[0],item[1],'viewQueue',item[2],item[4])

def KILLSLEEP(self):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          for item in queue_items:
               self.name = item[0]
               self.url = item[1]
               self.ext = item[3]
               self.console = item[4]
               self.thumb = item[2]

               time.sleep(3)
     removeFromQueue(self.name,self.url,self.thumb,self.ext,self.console)
     
     
          
def removeFromQueue(name,url,thumb,ext,console):
     queue = cache.get('queue')
     if queue:
          queue_items = sorted(eval(queue), key=lambda item: item[1])
          print queue_items
          try:
               queue_items.remove((name,url,thumb,'.mp4',console))
          except:
               try:
                    queue_items.remove((name,url,thumb,'.flv',console))
               except:
                    queue_items.remove((name,url,thumb,'.avi',console))
          cache.set('queue', str(queue_items))
          xbmc.executebuiltin("XBMC.Container.Refresh")


def download():
     download_path = settings.getSetting('download_folder')
     if download_path == '':
          addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image='')
     else:
          #viewQueue()
          dlThread = downloadThread(name, url, thumb, console, ext)
          dlThread.start() 

                   

#=============END DLFUNCTION======================================================================================================================


     



# Global Stuff
settings = xbmcaddon.Addon(id=addon_id)



def nameCleaner(name):
        name = name.replace('&#8211;','')
        name = name.replace("&#8217;","")
        name = name.replace("&#039;s","'s")
        name = unicode(name, errors='ignore')
        name = htmlcleaner.clean(name,strip=True)
        return(name)
     


#Metadata    
grab=metahandlers.MetaData()

def GRABMETA(name,year):
        
        meta = grab.get_meta('movie',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'tmdb_id': meta['tmdb_id'],'year': meta['year']}
                
        return infoLabels
        
        

def GRABTVMETA(name,year):
        
        meta = grab.get_meta('tvshow',name,year,None,None)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'cover_url': meta['cover_url'],
        'cast': meta['cast'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id'],'year': meta['year']}
                
        return infoLabels
        

def GRABEPISODEMETA(name,imdb_id,season,episode):
        
        meta = grab.get_episode_meta('tvshow',name,imdb_id,season,episode)
        infoLabels = {'rating': meta['rating'],'duration': meta['duration'],'genre': meta['genre'],'mpaa':"rated %s"%meta['mpaa'],
        'plot': meta['plot'],'title': meta['title'],'writer': meta['writer'],'cover_url': meta['cover_url'],
        'director': meta['director'],'backdrop_url': meta['backdrop_url'],'imdb_id': meta['imdb_id']}
                
        return infoLabels
                


#Add Directory Stuff
def addDiralt(name,url,mode,thumb):
     name = nameCleaner(name)
     if thumb == '':
          thumb = artwork + 'noepisode.jpg'
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'movie'}
     addon.add_directory(params, {'title':name}, img= thumb, fanart= fanart)



     
#******************For Movie Download*********************************
def addDLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype, 'mainimg':mainimg}
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)                             
       

#********************TV DOWNLOAD DIR***************************
def addTVDLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype,'mainimg':mainimg}
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dltvvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)
     

def addUFCDLDir(name,url,mode,thumb,labels,dlfoldername,favtype,mainimg):
        contextMenuItems = []
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername, 'favtype':favtype,'mainimg':mainimg}
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR gold]Download This File[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'dlsportvidpage', 'name':name, 'thumb':mainimg, 'console':console, 'dlfoldername':dlfoldername,'favtype':favtype})))
        addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb)

     
#Resolve Movie DL Links******************************************
def RESOLVEDL(name,url,thumb):  
        data=0
        try:
          data = GRABMETA(movie_name,year)
        except:
           data=0
        hmf = urlresolver.HostedMediaFile(url)
        host = ''
        if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          ext = ''
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'

          elif '.mkv' in url:
                    ext = '.mkv'          
          
          
          console = 'Downloads/Movies/'+ dlfoldername
          params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 


          xbmc.sleep(1000)

          addToQueue(name,url,thumb,ext,console)

def SPECIALDL(name,url,thumb):
        data=0
        try:
          data = GRABMETA(movie_name,year)
        except:
           data=0
        hmf = urlresolver.HostedMediaFile(url)
        host = ''
        if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          ext = ''
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'
                    
          elif '.mkv' in url:
                    ext = '.mkv'          
          
          
          console = 'Downloads/Specials/'+ dlfoldername
          params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 


          xbmc.sleep(1000)

          addToQueue(name,url,thumb,ext,console)         

#********Resolve TV DL Links*****************************************

def RESOLVETVDL(name,url,thumb):
         
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'

          elif '.mkv' in url:
                    ext = '.mkv'
                    
          if not ext == '':
          
               console = 'Downloads/TV Shows/'+ dlfoldername
               params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 
     
               xbmc.sleep(1000)
        
               addToQueue(name,url,thumb,ext,console)


#================Reslove Sport DL Links===========================
def RESOLVESPORTDL(name,url,thumb):
         
     data=0
     try:
          data = GRABMETA(movie_name,year)
     except:
           data=0
     hmf = urlresolver.HostedMediaFile(url)
     host = ''
     if hmf:
          url = urlresolver.resolve(url)
          host = hmf.get_host()
          if '.mp4' in url:
                    ext = '.mp4'
          elif '.flv' in url:
                    ext = '.flv'
          elif '.avi' in url:
                    ext = '.avi'

          elif '.mkv' in url:
                    ext = '.mkv'
                    
          if not ext == '':
          
               console = 'Downloads/Sports/'+ dlfoldername
               params = {'url':url, 'name':name, 'thumb':thumb, 'dlfoldername':dlfoldername} 
     
               xbmc.sleep(1000)
        
               addToQueue(name,url,thumb,ext,console)
               
        
     
# HELPDIR



def addHELPDir(name,url,mode,iconimage,fanart,description,filetype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def add2HELPDir(name,url,mode,iconimage,fanart,description,filetype):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok          

     
# Standard addDir
def addDir(name,url,mode,thumb,labels,favtype):
        name = nameCleaner(name)
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'dlfoldername':dlfoldername, 'mainimg':mainimg}
        contextMenuItems = []
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        sitethumb = thumb
        sitename = name
        fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
       
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb       
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addMDCDir(name,url,mode,thumb,labels,favtype):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'dlfoldername':dlfoldername, 'mainimg':mainimg}
        contextMenuItems = []
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        sitethumb = thumb
        sitename = name
        fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
       
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb       
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

# AddDir for TV SHows to add a year forpass

def addTVDir(name,url,mode,thumb,labels,favtype,year):
        contextMenuItems = []
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        sitethumb = thumb
        sitename = name
        try:
                name = data['title']
                thumb = data['cover_url']
                fanart = data['backdrop_url']
        except:
                name = sitename
                
        if thumb == '':
                thumb = sitethumb 
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&year="+urllib.quote_plus(year)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels=labels )
        if favtype == 'movie':
                contextMenuItems.append(('[COLOR gold]Movie Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'tvshow':
                contextMenuItems.append(('[COLOR gold]TV Show  Information[/COLOR]', 'XBMC.Action(Info)'))
        elif favtype == 'episode':
                contextMenuItems.append(('[COLOR gold]Episode  Information[/COLOR]', 'XBMC.Action(Info)'))       
                
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        try:
             liz.setProperty( "Fanart_Image", labels['backdrop_url'] )
        except:
             pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#Season Directory for TV Shows

def addSDir(name,url,mode,thumb,year,types):
     name = nameCleaner(name)
     contextMenuItems = []
     meta = {}
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'show':name}
     gomode=mode
     contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
     contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))

     if settings.getSetting('metadata') == 'true':
          meta = grab.get_meta('tvshow',name)
          if meta['backdrop_url'] == '':
               fanart = fanart
          else:
               fanart = meta['backdrop_url']
     else:
          fanart = fanart
          

     if settings.getSetting('metadata') == 'true':
               if settings.getSetting('banners') == 'false':
                    if thumb == '':
                         thumb = meta['cover_url']
               else:
                    thumb = meta['banner_url']
     if thumb == '':
          thumb = artwork + 'noepisode.jpg'
     contextMenuItems.append(('[COLOR gold]Tv Show Information[/COLOR]', 'XBMC.Action(Info)'))

     
     if settings.getSetting('metadata') == 'true':
          addon.add_directory(params, meta, contextmenu_items=contextMenuItems, img=thumb, fanart=fanart)          
     else:
          addon.add_directory(params, {'title':name}, contextmenu_items=contextMenuItems, img= thumb, fanart=fanart)     



# Episode add DirFunction 
def addEPDir(name,url,thumb,mode,show,dlfoldername,mainimg,season,episode):
        #params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}
        name = nameCleaner(name)
        contextMenuItems = []
        fullname = name
        ep_meta = None
        show_id = None
        meta = None
        othumb = thumb
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        if settings.getSetting('metadata') == 'true':
          #meta = grab.get_meta('tvshow',dlfoldername,'',season,episode)
          inc = 0
          movie_name = show[:-6]
          year = show[-6:]
          print 'Meta Year is ' +year
          print 'Meta Name is ' +movie_name
          
              
          meta = GRABTVMETA(movie_name,year)
          thumb = meta['cover_url']               
          yeargrab = meta['year']
          year = str(yeargrab)       
          #meta = grab.get_meta('tvshow',name,'')
          show_id = meta['imdb_id']
          print 'IMDB ID is ' +show_id
        else:
          fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
          thumb = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png'
        s,e = GET_EPISODE_NUMBERS(name)
        if settings.getSetting('metadata') == 'true':
          try:
              
              ep_meta = GRABEPISODEMETA(show_id,season,episode,'')
              if ep_meta['cover_url'] == '':
                    thumb = mainimg
              else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = mainimg
             
        else:
          thumb = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/icon.png'
          if thumb == '':
               thumb = mainimg
     
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':season, 'episode':episode, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}        
        if settings.getSetting('metadata') == 'true':
         contextMenuItems.append(('[COLOR gold]Tv Show Information[/COLOR]', 'XBMC.Action(Info)'))
         if ep_meta==None:
               fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
               addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems, img=thumb) 
         else:
               if meta['backdrop_url'] == '':
                    fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
               else:
                    fanart = meta['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta,contextmenu_items=contextMenuItems, fanart=fanart, img=thumb)
        else:
            addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems,fanart=fanart, img=thumb)
     
def addEPNOCLEANDir(name,url,thumb,mode,show,dlfoldername,mainimg,season,episode):
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb,  'dlfoldername':dlfoldername, 'mainimg':mainimg}
        contextMenuItems = []
        fullname = name
        ep_meta = None
        show_id = None
        meta = None
        othumb = thumb
        gomode=mode
        contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
        if settings.getSetting('metadata') == 'true':
          #meta = grab.get_meta('tvshow',dlfoldername,'',season,episode)
          inc = 0
          #movie_name = show[:-6]
          movie_name = show
          #year = show[-6:]
          year = ''
          print 'Meta Year is ' +year
          print 'Meta Name is ' +movie_name
          
              
          meta = GRABTVMETA(movie_name,year)
          thumb = meta['cover_url']               
          yeargrab = meta['year']
          year = str(yeargrab)       
          #meta = grab.get_meta('tvshow',name,'')
          show_id = meta['imdb_id']
          print 'IMDB ID is ' +show_id
        else:
          fanart = fanart
        s,e = GET_EPISODE_NUMBERS(name)
        if settings.getSetting('metadata') == 'true':
          try:
              
              ep_meta = GRABEPISODEMETA(show_id,season,episode,'')
              if ep_meta['cover_url'] == '':
                    thumb = mainimg
              else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = mainimg
             
        else:
          thumb = othumb
          if thumb == '':
               thumb = mainimg
     
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':season, 'episode':episode, 'show':show, 'types':'episode','dlfoldername':dlfoldername, 'mainimg':mainimg}        
        if settings.getSetting('metadata') == 'true':
         contextMenuItems.append(('[COLOR gold]Tv Show Information[/COLOR]', 'XBMC.Action(Info)'))
         if ep_meta==None:
               fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
               addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems, img=thumb, fanart=fanart) 
         else:
               if meta['backdrop_url'] == '':
                    fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg'
               else:
                    fanart = meta['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta,contextmenu_items=contextMenuItems, fanart=fanart, img=thumb)
        else:
            addon.add_directory(params, {'title':name},contextmenu_items=contextMenuItems,fanart=fanart, img=thumb)
     



#Host directory function for  Host Dir , hthumb =  host thumb and should be grabbed using the 'GETHOSTTHUMB(host)' function before 
def addHDir(name,url,mode,thumb,hthumb):
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'season':season, 'episode':episode, 'show':show}
     addon.add_directory(params, {'title':name}, img=hthumb, fanart=fanart)




#Resolve Functions
     
def RESOLVE(name,url,iconimage):
         url = urlresolver.HostedMediaFile(url=url).resolve()
         ok=True
         liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
         ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=str(url),listitem=liz)
         xbmc.sleep(1000)
         xbmc.Player ().play(str(url), liz, False)

         AUTO_VIEW('')

#Resolve 2

    

def RESOLVE2(name,url,thumb):
         
     #data=0
     #try:
     #data = GRABMETA(movie_name,year)
     #except:
     data=0
     #hmf = urlresolver.HostedMediaFile(url)
     #host = ''
     #if hmf:
     url = urlresolver.resolve(url)
          #host = hmf.get_host() 
             
     params = {'url':url, 'name':name, 'thumb':thumb}
     if data == 0:
          addon.add_video_item(params, {'title':name}, img=thumb)
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

     else:
          addon.add_video_item(params, {'title':name}, img=data['cover_url'])
          liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=data['cover_url'])
          liz.setInfo('video',infoLabels=data)

     xbmc.sleep(1000)
        
     xbmc.Player ().play(url, liz, False)

     

#AutoView
def AUTO_VIEW(content):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
                if settings.getSetting('auto-view') == 'true':
                        
                        if content == 'movies':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view') )
                        if content == 'tvshows':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('tvshows-view') )

                        if content == 'episode':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('episode-view') )
                        if content == 'season':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('season-view') )
                        if content == 'list':
                                xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('list-view') )
                                
                else:
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

        


     

#Returns the host thumbnail so that you can pass it as and argument 
def GETHOSTTHUMB(host):
     if host.endswith('.com'):
          host = host[:-4]
     if host.endswith('.org'):
          host = host[:-4]
     if host.endswith('.eu'):
          host = host[:-3]
     if host.endswith('.ch'):
          host = host[:-3]
     if host.endswith('.in'):
          host = host[:-3]
     if host.endswith('.es'):
          host = host[:-3]
     if host.endswith('.tv'):
          host = host[:-3]
     if host.endswith('.net'):
          host = host[:-4]
     if host.endswith('.me'):
          host = host[:-3]
     if host.endswith('.ws'):
          host = host[:-3]
     if host.endswith('.sx'):
          host = host[:-3]
     if host.startswith('www.'):
             host = host[4:]
     
     if settings.getSetting('theme') == '0':
             host = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/hosts/' + host +'.png'
     else:
             host = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/hosts/' + host +'.jpg'
     return(host)

#========================Returns Hostname For Directory ======================
def GETHOSTNAME(host):
     if host.endswith('.com'):
          host = host[:-4]
     if host.endswith('.org'):
          host = host[:-4]
     if host.endswith('.eu'):
          host = host[:-3]
     if host.endswith('.ch'):
          host = host[:-3]
     if host.endswith('.in'):
          host = host[:-3]
     if host.endswith('.es'):
          host = host[:-3]
     if host.endswith('.tv'):
          host = host[:-3]
     if host.endswith('.net'):
          host = host[:-4]
     if host.endswith('.me'):
          host = host[:-3]
     if host.endswith('.ws'):
          host = host[:-3]
     if host.endswith('.sx'):
          host = host[:-3]
     if host.startswith('www.'):
             host = host[4:]
     hostname=' '+host+'' 
     
     return(hostname)

#Episode directory function to be used when adding a Episode, all metadata scrapes and context menu items are handled within_________
def addEDir(name,url,mode,thumb,show):
     ep_meta = None
     show_id = None
     meta = None
     othumb = thumb
     gomode=mode
     contextMenuItems.append(('[COLOR red]Add to CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'addsttofavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
     contextMenuItems.append(('[COLOR red]Remove From CLIQ Favorites[/COLOR]', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 'removestfromfavs', 'name': name,'url': url,'thumb': thumb,'gomode': gomode})))
     if settings.getSetting('metadata') == 'true':
          data = GRABTVMETA('tvshow',show)
          

     else:
          fanart = fanart
     
     s,e = GET_EPISODE_NUMBERS(name)

     if settings.getSetting('metadata') == 'true':
          try:
               ep_meta = GRABTVMETA(show,show_id,int(s),int(e))
               if ep_meta['cover_url'] == '':
                    thumb = artwork + 'noepisode.jpg'
               else:
                    thumb = str(ep_meta['cover_url'])
          except:
               ep_meta=None
               thumb = artwork + 'noepisode.jpg'
             
     else:
          thumb = othumb
          if thumb == '':
               thumb = artwork + 'noepisode.jpg'
     params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode'}        
     if settings.getSetting('metadata') == 'true':

          if ep_meta==None:
               fanart = fanart
               addon.add_directory(params, {'title':name}, img=thumb, fanart=fanart) 
          else:
               if data['backdrop_url'] == '':
                    fanart = fanart
               else:
                    fanart = data['backdrop_url']
               ep_meta['title'] = name
               addon.add_directory(params, ep_meta, fanart=fanart, img=thumb)
     else:
          addon.add_directory(params, {'title':name},fanart=fanart, img=thumb) 


#Called within the addEDir function, returns needed season and episode numbers needed for metadata scraping___________________________

def GET_EPISODE_NUMBERS(ep_name):
     s = None
     e = None
     ep_name = re.sub('×','X',ep_name)

     S00E00 = re.findall('[Ss]\d\d[Ee]\d\d',ep_name)
     SXE = re.findall('\d[Xx]\d',ep_name)
     SXEE = re.findall('\d[Xx]\d\d',ep_name)
     SXEEE = re.findall('\d[Xx]\d\d\d',ep_name)

     SSXE = re.findall('\d\d[Xx]\d',ep_name)
     SSXEE = re.findall('\d\d[Xx]\d\d',ep_name)
     SSXEEE = re.findall('\d\d[Xx]\d\d\d',ep_name)
     
     if S00E00:
          print 'Naming Style Is S00E00'
          S00E00 = str(S00E00)
          S00E00.strip('[Ss][Ee]')
          S00E00 = S00E00.replace("u","")
          e = S00E00[-4:]
          e = e[:-2]
          s = S00E00[:5]
          s = s[-2:]
          
     if SXE:
          print 'Naming Style Is SXE'
          SXE = str(SXE)
          SXE = SXE.replace("u","")
          print 'Numer String is ' + SXE
          s = SXE[2]
          e = SXE[4]

     if SXEE:
          print 'Naming Style Is SXEE'
          SXEE = str(SXEE)
          SXEE = SXEE.replace("u","")
          print 'Numer String is ' + SXEE
          s = SXEE[2]
          e = SXEE[4] + SXEE[5]

     if SXEEE:
          print 'Naming Style Is SXEEE'
          SXEEE = str(SXEEE)
          SXEEE = SXEEE.replace("u","")
          print 'Numer String is ' + SXEEEE
          s = SXEEE[2]
          e = SXEEE[4] + SXEEE[5] + SXEEE[6]

     if SSXE:
          print 'Naming Style Is SSXE'
          SSXE = str(SSXE)
          SSXE = SSXE.replace("u","")
          print 'Numer String is ' + SSXE
          s = SSXE[2] + SSXE[3]
          e = SSXE[5]

     if SSXEE:
          print 'Naming Style Is SSXEE'
          SSXEE = str(SSXEE)
          SSXEE = SSXEE.replace("u","")
          print 'Numer String is ' + SSXEE
          s = SSXEE[2] + SSXEE[3]
          e = SSXEE[5] + SSXEE[6]

     if SSXEEE:
          print 'Naming Style Is SSXEEE'
          SSXEEE = str(SSXEEE)
          SSXEEE = SSXEEE.replace("u","")
          print 'Numer String is ' + SSXEEE
          s = SSXEEE[2] + SSXEE[3]
          e = SSXEEE[5] + SSXEEE[6] + SSXEEE[7]

     return s,e



def doRegex(murl):
    #rname=rname.replace('><','').replace('>','').replace('<','')
    import urllib2
    url=re.compile('([^<]+)<regex>',re.DOTALL).findall(murl)[0]
    doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
    for k in doRegexs:
        if k in murl:
            regex=re.compile('<name>'+k+'</name><expres>(.+?)</expres><page>(.+?)</page><referer>(.+?)</referer></regex>',re.DOTALL).search(murl)
            referer=regex.group(3)
            if referer=='':
                referer=regex.group(2)
            req = urllib2.Request(regex.group(2))
            req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
            req.add_header('Referer',referer)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\/','/')
            r=re.compile(regex.group(1),re.DOTALL).findall(link)[0]
            url = url.replace("$doregex[" + k + "]", r)
   
    return url

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def downloadFile(url,dest,silent = False,cookie = None):
    try:
        import urllib2
        file_name = url.split('/')[-1]
        print "Downloading: %s" % (file_name)
        if cookie:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
        u = opener.open(url)
        f = open(dest, 'wb')
        meta = u.info()
        if meta.getheaders("Content-Length"):
            file_size = int(meta.getheaders("Content-Length")[0])
        else: file_size = 'Unknown'
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer: break
            file_size_dl += len(buffer)
            f.write(buffer)
        print "Downloaded: %s %s Bytes" % (file_name, file_size)
        f.close()
        return True
    except Exception, e:
        print 'Error downloading file ' + url.split('/')[-1]
       
        if not silent:
            dialog = xbmcgui.Dialog()
            dialog.ok("Phoenix Streams", "Report the error below at " + supportsite, str(e), "We will try our best to help you")
        return False

                              



