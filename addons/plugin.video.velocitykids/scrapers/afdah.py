
import urllib2,urllib,re,os
import random
import urlparse
import sys
import urlresolver
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi
from tm_libs import dom_parser
from libs import log_utils
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import tools
import string
import main_scrape
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib
net = Net()
addon_id = kodi.addon_id
addon = Addon(addon_id, sys.argv)

#COOKIE STUFF
tools.create_directory(tools.AOPATH, "All_Cookies/Afdah")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','Afdah/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')


def __enum(**enums):
    return type('Enum', (), enums)

FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')

def LogNotify(title,message,times,icon):
		xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")



XHR = {'X-Requested-With': 'XMLHttpRequest'}
USER_AGENT = "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
BR_VERS = [
    ['%s.0' % i for i in xrange(18, 43)],
    ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
     '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
     '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
    ['11.0']]

WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
            'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
            'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']


#base_url = 'http://afdah.tv/'
base_url = kodi.get_setting('afdah_base_url')

def OPEN_URL (url,cookies=None, data=None, multipart_data=None, headers=None, allow_redirect=True, cache_limit=8):
    # form_data = {'login':'somename', 'password':'somepassword','remember_me':'on','submit_login':'Login', 'submit_login':''}
    # print form_data
    # print data

    #Get UPDATED COOKIE AND STORE
    #Create an opener to open pages using the http protocol and to process cookies.
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    request = urllib2.Request(base_url)
    #print 'Request method before data:', request.get_method()

    request.add_data(urllib.urlencode(data))
    #print 'Request method after data :', request.get_method()


    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
    request.add_header('Content-Type','application/x-www-form-urlencoded')
    request.add_header('Host','afdah.tv')
    request.add_header('Referer',url)
    request.add_header('Connection','keep-alive')
    request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')


    urllib2.urlopen(request).read()
    response = urllib2.urlopen(request)
    cj.save(cookie_file, ignore_discard=True)
    response.close()



    #LOAD UPDATED COOKIE AND GET NEW URL
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    request = urllib2.Request(url)
    request.add_data(urllib.urlencode(data))

    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
    request.add_header('Content-Type','application/x-www-form-urlencoded')
    request.add_header('Host','afdah.tv')
    request.add_header('Referer','')
    request.add_header('Connection','keep-alive')
    request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    link = urllib2.urlopen(request).read()
    #print ' RETURNING COOKED DATA' + link

    return link

def OPEN_URL_REG(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
  response=urllib2.urlopen(req)
  link=response.read()
  cj.save(cookie_file, ignore_discard=True)
  response.close()
  return link


def afdah(name):
    try:
        title = name[:-7]
        movie_year = name[-6:]
        year = movie_year.replace('(','').replace(')','')
        video_type = 'movies'
        search_url = urlparse.urljoin(base_url, '/wp-content/themes/afdah/ajax-search.php')
        data = {'search': title, 'type': 'title'}
        html = OPEN_URL(search_url, data=data, cache_limit=1)
        pattern = '<li>.*?href="([^"]+)">([^<]+)\s+\((\d{4})\)'
        results = []
        for match in re.finditer(pattern, html, re.DOTALL | re.I):
            url, title, match_year = match.groups('')
            if not year or not match_year or year == match_year:
                result = {'url': _pathify_url(url), 'title': title, 'year': year}
                results.append(result)
        for e in results:

            url = e['url']
            year = e['year']
            name = e['title']
            # print year
            # print name
            # print url
            # srcurl = base_url+url
            # link = OPEN_URL_REG(srcurl)
            hosters=get_sources(url)
            # print hosters
            return hosters
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='Afdah',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters

def _get_ua():
    index = random.randrange(len(RAND_UAS))
    user_agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
    #print 'Creating New User Agent: %s' % (user_agent)
    return user_agent





def _pathify_url(url):
    url = url.replace('\/', '/')
    pieces = urlparse.urlparse(url)
    if pieces.scheme:
        strip = pieces.scheme + ':'
    else:
        strip = ''
    strip += '//' + pieces.netloc
    url = url.replace(strip, '')
    if not url.startswith('/'): url = '/' + url
    url = url.replace('/./', '/')
    return url

def _get_links(html):
        hosters = []
        for match in re.finditer('file\s*:\s*"([^"]+).*?label\s*:\s*"([^"]+)', html):
            url, resolution = match.groups()
            url += '|User-Agent=%s&Cookie=%s' % (_get_ua(), __get_stream_cookies())
            hoster = {'url': url, 'host': 'FANCY HOST'}
            hosters.append(hoster)
        return hosters


def __get_stream_cookies():
        #print "STREAM COOKIES"
        cj = OPEN_URL(base_url, {})
        cookies = []
        for cookie in cj:
            cookies.append('%s=%s' % (cookie.name, cookie.value))
        return urllib.quote(';'.join(cookies))

def _caesar(plaintext, shift):
        lower = string.ascii_lowercase
        lower_trans = lower[shift:] + lower[:shift]
        alphabet = lower + lower.upper()
        shifted = lower_trans + lower_trans.upper()
        return plaintext.translate(string.maketrans(alphabet, shifted))

def _get_direct_hostname(link):
        host = urlparse.urlparse(link).hostname
        if host and any([h for h in ['google', 'picasa'] if h in host]):
            return 'gvideo'
        else:
            return get_name()


def get_name(cls):
        """
        Must return a string that is a name that will be used through out the UI and DB to refer to urls from this source
        Should be descriptive enough to be recognized but short enough to be presented in the UI
        """
        raise NotImplementedError


def get_sources(source_url):

        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(base_url, source_url)
            #html = _http_get(url, cache_limit=.5)
            html = OPEN_URL_REG(url)
            #print "HTML IS NOW = "+html

            match = re.search('This movie is of poor quality', html, re.I)
            if match:
                quality = QUALITIES.LOW
            else:
                quality = QUALITIES.HIGH
            #print "QUALITY IS = "+quality

            for match in re.finditer('href="([^"]+/embed\d*/[^"]+)', html):
                url = match.group(1)
                embed_html = OPEN_URL_REG(url)
                r = re.search('{\s*write\("([^"]+)', embed_html)
                if r:
                    plaintext = _caesar(r.group(1), 13).decode('base-64')
                    if 'http' not in plaintext:
                        plaintext = _caesar(r.group(1).decode('base-64'), 13).decode('base-64')
                else:
                    plaintext = embed_html
                #print "PLAINTEXT IS = "+plaintext
                hosters += _get_links(plaintext)

            pattern = 'href="([^"]+)".*play_video.gif'
            for match in re.finditer(pattern, html, re.I):
                url = match.group(1)
                host = urlparse.urlparse(url).hostname
                host = host.replace('www.','')
                host = host.replace('http://','')
                hoster = {'hostname':'AFDAH','multi-part': False, 'url': url, 'host': host, 'quality': quality, 'rating': None, 'views': None, 'direct': False}
                #hoster = {'url': url, 'host': host,'view':None,'quality':quality,'direct':False}
                hosters.append(hoster)
        hosters = main_scrape.apply_urlresolver(hosters)
        return hosters







