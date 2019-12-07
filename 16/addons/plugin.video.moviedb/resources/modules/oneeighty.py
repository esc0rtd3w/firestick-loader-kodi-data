import urllib,urllib2,re,cookielib,string,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from addon.common.addon import Addon
import datetime
import time
import os

from resources.modules import live
addon_id = 'plugin.video.moviedb'
ADDON=xbmcaddon.Addon(id='plugin.video.moviedb')
settings = xbmcaddon.Addon(id=addon_id)
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")
def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link


def ONEEIGHTYMAIN():

        link=OPEN_URL('http://www.181.fm/channellistmini.php')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match = re.compile('700"><br>(.+?)</font></td>(.+?)</table>').findall(link)
        for name,url in match:
            name=name.replace('/','&')
            thumb=name.replace(' ','%20')
            addDir(name,url,'oneeightylist','','','')
    

def ONEEIGHTYLIST(mname,murl):
        image=mname.replace(' ','%20')
        thumb=''
        match = re.compile('<a STYLE="text-decoration:none" href="(.+?)" class="left_link">(.+?)</a></font></td>').findall(murl)
        for url,name in match:
            addDir(name,url,'oneeightylink',thumb,'','')


def ONEEIGHTYLINK(name,url):
        link=OPEN_URL(url)
        source = re.compile('<REF HREF="(.+?)"/>').findall(link)
        for stream_url in source:
                match = re.compile('relay').findall(stream_url)
                print match
                if len(match)>0:
                        stream=stream_url
                else:
                        stream=stream_url
        live.LIVERESOLVE(name,stream,'')                

def addDir(name,url,mode,thumb,desc,favtype):
        
        params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'desc':desc}
        fanart = thumb
        if thumb == artwork + 'icon.png':
                fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/images/fanart2.jpg'
        elif thumb == '-':
                fanart = 'http://cliqaddon.com/support/commoncore/tvaddons/moviedb/images/fanart2.jpg'        
        if desc == '':
                desc = 'Description not available at this level'
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        liz.setInfo( type="Audio", infoLabels={ "title": name,} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        

