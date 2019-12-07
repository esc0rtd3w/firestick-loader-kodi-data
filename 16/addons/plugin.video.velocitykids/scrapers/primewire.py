import urllib2,urllib,re,os
import sys
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi,trakt_auth
from tm_libs import dom_parser
from libs.trans_utils import i18n
from libs import log_utils
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import urlresolver
import main_scrape
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
net = Net()
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)
ADDON = xbmcaddon.Addon(id=kodi.addon_id)

#COOKIE STUFF
tools.create_directory(tools.AOPATH, "All_Cookies/PrimeWire")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','PrimeWire/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')

base_url = kodi.get_setting('primewire_base_url')
#base_url = 'http://www.primewire.ag/'


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

def primewire(name):
    try:
            sources = []
            searchUrl = base_url+'index.php?search_keywords='
            movie_name = name[:-6]
            movie_name_short = name[:-7]
            movie_year_full = name[-6:]
            movie_year = movie_year_full.replace('(','').replace(')','')
            sname = movie_name.replace(" ","+")
            primename = sname[:-1]
            movie_match =movie_name.replace(" ","_")+movie_year
            surl = searchUrl + primename
            link = OPEN_URL(surl)
            full_match  = movie_name+movie_year_full
            match=re.compile('<a href="/(.+?)" title="Watch (.+?)">').findall(link)
            for url, name in match:
                if full_match == name:
                    link = OPEN_URL(base_url+url)
                    container_pattern = r'<table[^>]+class="movie_version[ "][^>]*>(.*?)</table>'
                    item_pattern = (
                        r'quality_(?!sponsored|unknown)([^>]*)></span>.*?'
                        r'url=([^&]+)&(?:amp;)?domain=([^&]+)&(?:amp;)?(.*?)'
                        r'"version_veiws"> ([\d]+) views</')
                    max_index = 0
                    max_views = -1
                    for container in re.finditer(container_pattern, link, re.DOTALL | re.IGNORECASE):
                        for i, source in enumerate(re.finditer(item_pattern, container.group(1), re.DOTALL)):
                            qual, url, host, parts, views = source.groups()
                            if kodi.get_setting('debug') == "true":
                                print"PrimeWire Debug:"
                                print "Quality is " + qual
                                print "URL IS " + url.decode('base-64')
                                print "HOST IS  "+host.decode('base-64')
                                print "VIEWS ARE " +views
                            if host == 'ZnJhbWVndGZv': continue  # filter out promo hosts
                            #host = tools.get_hostname(host.decode('base-64'))
                            source = {'hostname':'PrimeWire','url': url.decode('base-64'), 'host': host.decode('base-64'),'views':views,'quality':qual,'direct':False}
                            sources.append(source)
            #print "MOVIE SOURCES ARE = "+str(sources)
            sources = main_scrape.apply_urlresolver(sources)
            return sources
    except Exception as e:
        sources =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='PrimeWire',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return sources



def primewire_tv(name,movie_title):
    #print "SEARCHING TITLE IS =" +movie_title
    #print "EPISODE REAL NAME IS = "+name
    tvso = []
    seasons=re.compile('S(.+?)E(.+?) ').findall(name)
    for sea,epi in seasons:


        movie_name = movie_title[:-7]
        tv_title=movie_name.replace(' ','+')
        #print "TV REAL TITLE IS = "+tv_title
        searchUrl = 'http://www.primewire.ag/index.php?search_keywords='
        surl = searchUrl + tv_title            ###########CHANGE THIS
        #print "SEARCH URL PRIME IS + " +surl
        link = OPEN_URL(surl+'&search_section=2')
        match=re.compile('<a href="/(.+?)" title="Watch (.+?)">').findall(link)
        for url, name in match:
            if movie_title == name:
                url = url.replace('watch','tv').replace('-online-free','')
                link = OPEN_URL(base_url+url+'/season-'+sea+'-episode-'+epi)
                container_pattern = r'<table[^>]+class="movie_version[ "][^>]*>(.*?)</table>'
                item_pattern = (
                    r'quality_(?!sponsored|unknown)([^>]*)></span>.*?'
                    r'url=([^&]+)&(?:amp;)?domain=([^&]+)&(?:amp;)?(.*?)'
                    r'"version_veiws"> ([\d]+) views</')
                max_index = 0
                max_views = -1
                for container in re.finditer(container_pattern, link, re.DOTALL | re.IGNORECASE):
                    for i, source in enumerate(re.finditer(item_pattern, container.group(1), re.DOTALL)):
                        qual, url, host, parts, views = source.groups()
                        if kodi.get_setting('debug') == "true":
                            print"PrimeWire Debug:"
                            print "Quality is " + qual
                            print "URL IS " + url.decode('base-64')
                            print "HOST IS  "+host.decode('base-64')
                            print "VIEWS ARE " +views
                        if host == 'ZnJhbWVndGZv': continue  # filter out promo hosts
                        #host = tools.get_hostname(host.decode('base-64'))
                        source = {'url': url.decode('base-64'), 'host':host.decode('base-64'),'view':views,'quality':qual,'direct':False}
                        tvso.append(source)
        tvso = main_scrape.apply_urlresolver(tvso)
        return tvso
