
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
addon_id = kodi.addon_id
addon = Addon(addon_id, sys.argv)

#COOKIE STUFF
tools.create_directory(tools.AOPATH, "All_Cookies/Two_Movies")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','Two_Movies/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')

base_url = kodi.get_setting('twomovies_base_url')
host_url = base_url.replace('http://','').replace('/','')

def LogNotify(title,message,times,icon):
		xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")



def OPEN_URLTM(url):

        try:
            req=urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
            req.add_header('Content-Type','application/x-www-form-urlencoded')
            req.add_header('Host',host_url)
            req.add_header('Referer','')
            req.add_header('Connection','keep-alive')
            req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            response=urllib2.urlopen(req)
            link=response.read()
            cj.save(cookie_file, ignore_discard=True)
            response.close()
            return link
        except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "true":
                kodi.notify(header='TwoMovies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)

def OPEN_URL(url):

  try:
      req=urllib2.Request(url)
      req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
      response=urllib2.urlopen(req)
      link=response.read()
      cj.save(cookie_file, ignore_discard=True)
      response.close()
      return link
  except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "true":
                kodi.notify(header='TwoMovies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)

def tmovies(name):

    try:
        sources = []
        searchUrl = base_url+'watch_movie/'
        movie_name = name[:-6]
        movie_name_short = name[:-7]
        movie_year = name[-6:]
        movie_year = movie_year.replace('(','').replace(')','')
        sname = movie_name.replace(" ","+")
        movie_match =movie_name.replace(" ","_").replace(":","").replace("-","")
        year_movie_match = movie_match+movie_year
        direct_movie_match = movie_match[:-1]
        tmurl = base_url+'watch_movie/'+direct_movie_match
        ytmurl = base_url+'watch_movie/'+year_movie_match
        link = OPEN_URLTM(tmurl)
        names = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"})
        urls = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"}, ret='href')
        for host, url in zip(names, urls):
            host = host.replace('www.','')
            #host = tools.get_hostname(host)
            source = {'url': url, 'host':host,'direct':False}
            sources.append(source)
        link = OPEN_URLTM(ytmurl)
        names = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"})
        urls = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"}, ret='href')
        for host, url in zip(names, urls):
            host = host.replace('www.','')
            #host = tools.get_hostname(host)
            source = {'url': url, 'host':host,'direct':False}
            sources.append(source)
        sources = main_scrape.apply_urlresolver(sources)
        return sources
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='TwoMovies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters


def tmovies_tv(name,movie_title):

    try:
        sources = []
        searchUrl = base_url+'watch_episode/'
        # if 'House' in movie_title:
        #     movie_title = movie_title.replace('House','DR House')
        movie_name = movie_title[:-6]
        movie_name_short = movie_title[:-7]
        movie_year = movie_title[-6:]
        movie_year = movie_year.replace('(','').replace(')','')
        movie_match =movie_name.replace(" ","_").replace(":","").replace("-","")
        year_movie_match = movie_match+movie_year
        direct_movie_match = movie_match[:-1]
        seasons=re.compile('S(.+?)E(.+?) ').findall(name)
        for sea,epi in seasons:
            tmurl = searchUrl+direct_movie_match+'/'+sea+'/'+epi+'/'
            link = OPEN_URLTM(tmurl)
            names = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"})
            urls = dom_parser.parse_dom(link, 'a',{'class':"norm vlink"}, ret='href')
            for host, url in zip(names, urls):
                host = host.replace('www.','')
                #host = tools.get_hostname(host)
                source = {'url': url, 'host':host,'direct':False}
                sources.append(source)
            sources = main_scrape.apply_urlresolver(sources)
            return sources
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='TwoMovies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters


def tmlinkpage(url,movie_title,thumb,media):

    try:
        if  "full" in url:
                link = OPEN_URL(url)
                if 'Before you start watching' in link:
                                                #print 'Confirmation Button '
                                                url = url
                                                header_dict = {}
                                                header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                                                header_dict['Connection'] = 'keep-alive'
                                                header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
                                                header_dict['Origin'] = host_url
                                                header_dict['Referer'] = url
                                                header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
                                                form_data = {'confirm':'I understand, Let me watch the movie now!'}
                                                net.set_cookies(cookiejar)
                                                conbutton = net.http_POST(url, form_data=form_data,headers=header_dict)

                link=OPEN_URL(url)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
                matchurl=re.compile('Sourcelink:<arel="nofollow"onlicktarget="_blank">(.+?)</').findall(link)
                for urls in matchurl:
                    urls = str(urls)
                    urls = urls.replace('&rel=nofollow','')
                    if media =='movies':
                        main_scrape.get_link(urls,movie_title,thumb,media)
                    else:
                        main_scrape.get_tv_link(urls,movie_title,thumb,media)
    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "true":
                kodi.notify(header='TwoMovies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)




