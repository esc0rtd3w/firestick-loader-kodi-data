import urllib2,urllib,re,os
import sys
import urlresolver
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
#import urlresolver
from libs import kodi
from tm_libs import dom_parser
from libs.trans_utils import i18n
from libs import log_utils
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import main_scrape
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
net = Net()
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)

#COOKIE STUFF
tools.create_directory(tools.AOPATH, "All_Cookies/Zmovies")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','Zmovies/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')

base_url = kodi.get_setting('zmovies_base_url')

def LogNotify(title,message,times,icon):
		xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
  response=urllib2.urlopen(req)
  link=response.read()
  cj.save(cookie_file, ignore_discard=True)
  response.close()
  return link

def zmovies(name):
    try:
        sources = []
        movie_name = name[:-6]
        movie_name_short = name[:-7]
        movie_year = name[-6:]
        movie_year = movie_year.replace('(','').replace(')','')
        sname = movie_name.replace(" ","+")
        movie_match =movie_name.replace(" ","-").replace(":","")
        year_movie_match = movie_match+movie_year
        direct_movie_match = movie_match[:-1]
        tmurl = base_url+'movies/view/'+direct_movie_match
        ytmurl = base_url+'movies/view/'+year_movie_match
        #dp.update(25)
        #For links that are direct
        link = OPEN_URL(tmurl)
        match=re.compile('target="_blank"   href="(.+?)"> <b> Watch Full </b></a> </td>').findall(link)
        for url in match:
            hmf = urlresolver.HostedMediaFile(url)
            if hmf:

            #linkname= hmf.get_host()
                linkname = tools.get_hostname(url)
                host = linkname
                #source = {'hostname':'IceFilms','multi-part': False, 'quality': quality, 'label': label, 'rating': None, 'views': None, 'direct': False}
                source = {'hostname':'ZMovies','views':None, 'quality': None, 'rating': None,'url': url, 'host': host, 'direct':False}
                sources.append(source)
        #Fro Links that need year added
        link = OPEN_URL(ytmurl)
        #dp.update(80)
        match=re.compile('target="_blank"   href="(.+?)"> <b> Watch Full </b></a> </td>').findall(link)
        for url in match:
            linkname = tools.get_hostname(url)
            host = linkname
            source = {'hostname':'ZMovies','views':None, 'quality': None, 'rating': None,'url': url, 'host': host, 'direct':False}
            sources.append(source)
        #dp.close()
        sources = main_scrape.apply_urlresolver(sources)
        print sources
        return sources
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='Zee Moviess',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters



# def playzmovieslink(url,name,thumb):
#                    hmf = urlresolver.HostedMediaFile(url)
#                   ##########################################
#                    #print 'URLS is ' +url
#                    if hmf:
#                        try:
#                                 main_scrape.playlink(name,url,thumb)
#                        except:
#                             LogNotify('Try another Link! ', 'Link has been removed or is invalid', '5000', '')
#                             #print "NO MATCH"
#                    else:
# 									LogNotify('Try another Link! ', 'Link has been removed or is invalid', '5000', '')
# 									#print "NO MATCH"
#                           #except:
#                                   #pass




