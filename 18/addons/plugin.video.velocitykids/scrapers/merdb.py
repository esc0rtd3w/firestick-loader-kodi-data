
import urllib2,urllib,re,os
import sys
import urlresolver
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
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
tools.create_directory(tools.AOPATH, "All_Cookies/MerDb")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','MerDb/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')

base_url = kodi.get_setting('merdb_base_url')

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

def merdb(name):
    try:
        sources = []
        searchUrl = base_url+'?search='
        movie_name = name[:-6]
        movie_name_short = name[:-7]
        movie_year = name[-6:]
        movie_year = movie_year.replace('(','').replace(')','')
        sname = movie_name.replace(" ","+")
        mername = sname[:-1]
        movie_match =movie_name.replace(" ","_")+movie_year
        surl = searchUrl + mername
        link = OPEN_URL(surl)
        #dp.update(80)
        match=re.compile('<div class="main_list_box"><a href="(.+?)" title="(.+?)"><img').findall(link)
        for url, name in match:
            if movie_match in url or movie_name_short == name:
                link = OPEN_URL(base_url+url)
                vidlinks=dom_parser.parse_dom(link, 'span',{'class':"movie_version_link"})
                linknames=dom_parser.parse_dom(link, 'span',{'class':"version_host"})
                for name, vidlink in zip(linknames, vidlinks):
                    #dp.update(80)
                    match=re.compile('<a href="(.+?)"').findall(vidlink)
                    for linkurl in match:
                        if "ads.php" not in linkurl and "Sponsor" not in name and "Host" not in name:
                            url = base_url+linkurl
                            #print "URLS IS = " +url
                            host = name.replace("'","")
                            #linkname = tools.get_hostname(name)
                            source = {'hostname':'MerDB','views':None,'url': url, 'host': host, 'direct':False}
                            sources.append(source)
        #dp.close()
        sources = main_scrape.apply_urlresolver(sources)
        return sources
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='MerDb',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters


# def playmerdblink(url,movie_title,thumb):
#                  link = OPEN_URL(url)
#                  #print "URL IS  = " +url
#                  hostmatch=re.compile('src="(.+?)" style').findall(link)
#                  for urls in hostmatch:
#                    #print 'Pre HMF url is  ' +urls
#                    hmf = urlresolver.HostedMediaFile(urls)
#                   ##########################################
#                    if hmf:
#                        try:
#                                 main_scrape.playlink(movie_title,urls,thumb)
#                        except:
#                             LogNotify('Try another Link! ', 'Link has been removed or is invalid', '5000', '')
#                             #print "NO MATCH"
#                    else:
# 									LogNotify('Try another Link! ', 'Link has been removed or is invalid', '5000', '')
# 									#print "NO MATCH"
#                           #except:
#                                   #pass


