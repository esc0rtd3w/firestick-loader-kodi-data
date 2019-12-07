import urllib2,urllib,re,os
import random
import urlparse
import sys
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi
from tm_libs import dom_parser
from libs.trans_utils import i18n
from libs import log_utils
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import tools
import string
from libs import cloudflare
from tm_libs import dom_parser
import cookielib
import json
from StringIO import StringIO
import gzip
import main_scrape


net = Net()
addon_id = kodi.addon_id
addon = Addon(addon_id, sys.argv)

#COOKIE STUFF
tools.create_directory(tools.AOPATH, "All_Cookies/NineMovies")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','NineMovies/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')



timeout = int(kodi.get_setting('scraper_timeout'))

def __enum(**enums):
    return type('Enum', (), enums)


MAX_RESPONSE = 1024 * 1024 * 2
FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')

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

base_url = kodi.get_setting('9movies_base_url')
hash_url = '/ajax/film/episode?hash_id=%s&f=&p=%s'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD 720P': QUALITIES.HD720}




class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        if kodi.get_setting('debug') == "true":
            log_utils.log('Stopping Redirect', log_utils.LOGDEBUG)
        return response

    https_response = http_response

# abstractstaticmethod = abc.abstractmethod
# class abstractclassmethod(classmethod):
#
#     __isabstractmethod__ = True
#
#     def __init__(self, callable):
#         callable.__isabstractmethod__ = True
#         super(abstractclassmethod, self).__init__(callable)


def _http_get(url, cookies=None, data=None, multipart_data=None, headers=None, allow_redirect=True, cache_limit=8):
        return get_cooked_url(url, base_url, timeout, cookies=cookies, data=data, multipart_data=multipart_data,
                                     headers=headers, allow_redirect=allow_redirect, cache_limit=cache_limit)

def get_cooked_url(url, base_url, timeout, cookies=None, data=None, multipart_data=None, headers=None, allow_redirect=True, cache_limit=8):
        if cookies is None: cookies = {}
        if timeout == 0: timeout = None
        if headers is None: headers = {}
        referer = headers['Referer'] if 'Referer' in headers else url
        if kodi.get_setting('debug') == "true":
            log_utils.log('Getting Url: %s cookie=|%s| data=|%s| extra headers=|%s|' % (url, cookies, data, headers))
        if data is not None:
            if isinstance(data, basestring):
                data = data
            else:
                data = urllib.urlencode(data, True)

        if multipart_data is not None:
            headers['Content-Type'] = 'multipart/form-data; boundary=X-X-X'
            data = multipart_data

        try:
            cj = _set_cookies(base_url, cookies)
            request = urllib2.Request(url, data=data)
            request.add_header('User-Agent', _get_ua())
            request.add_unredirected_header('Host', '9movies.to')
            request.add_unredirected_header('Referer', referer)
            for key in headers: request.add_header(key, headers[key])
            cj.add_cookie_header(request)
            if not allow_redirect:
                opener = urllib2.build_opener(NoRedirection)
                urllib2.install_opener(opener)
            else:
                opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
                urllib2.install_opener(opener)
                opener2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                urllib2.install_opener(opener2)

            response = urllib2.urlopen(request, timeout=timeout)
            cj.extract_cookies(response, request)
            if kodi.get_setting('cookie_debug') == 'true':
                print 'Response Cookies: %s - %s' % (url, cookies_as_str(cj))
            __fix_bad_cookies()
            cj.save(ignore_discard=True)
            if not allow_redirect and (response.getcode() in [301, 302, 303, 307] or response.info().getheader('Refresh')):
                if response.info().getheader('Refresh') is not None:
                    refresh = response.info().getheader('Refresh')
                    return refresh.split(';')[-1].split('url=')[-1]
                else:
                    return response.info().getheader('Location')

            content_length = response.info().getheader('Content-Length', 0)
            if int(content_length) > MAX_RESPONSE:
                log_utils.log('Response exceeded allowed size. %s => %s / %s' % (url, content_length, MAX_RESPONSE), log_utils.LOGWARNING)

            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read(MAX_RESPONSE))
                f = gzip.GzipFile(fileobj=buf)
                html = f.read()
            else:
                html = response.read(MAX_RESPONSE)
        except urllib2.HTTPError as e:
            if e.code == 503 and 'cf-browser-verification' in e.read():
                #print "WAS ERROR"
                html = cloudflare.solve(url, cj, _get_ua())
                if not html:
                    return ''
            else:
                log_utils.log('Error (%s) during THE scraper http get: %s' % (str(e), url), log_utils.LOGWARNING)
                return ''
        except Exception as e:
            log_utils.log('Error (%s) during scraper http get: %s' % (str(e), url), log_utils.LOGWARNING)
            return ''

        return html






def get_url(url):
    request=urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
    response=urllib2.urlopen(request)
    link=response.read()
    cj.save(cookie_file, ignore_discard=True)
    response.close()
    return link


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


def _caesar(plaintext, shift):
        lower = string.ascii_lowercase
        lower_trans = lower[shift:] + lower[:shift]
        alphabet = lower + lower.upper()
        shifted = lower_trans + lower_trans.upper()
        return plaintext.translate(string.maketrans(alphabet, shifted))


def _get_direct_hostname(link):
        host = urlparse.urlparse(link).hostname
        if host and any([h for h in ['google', 'picasa'] if h in host]):
            return 'GVideo'
        else:
            return 'Host Native'


def _height_get_quality(height):
        if str(height)[-1] in ['p', 'P']:
            height = str(height)[:-1]

        try: height = int(height)
        except: height = 200
        if height > 800:
            quality = QUALITIES.HD1080
        elif height > 480:
            quality = QUALITIES.HD720
        elif height >= 400:
            quality = QUALITIES.HIGH
        elif height > 200:
            quality = QUALITIES.MEDIUM
        else:
            quality = QUALITIES.LOW
        return quality


def _gv_get_quality(stream_url):
        stream_url = urllib.unquote(stream_url)
        if 'itag=18' in stream_url or '=m18' in stream_url:
            return QUALITIES.MEDIUM
        elif 'itag=22' in stream_url or '=m22' in stream_url:
            return QUALITIES.HD720
        elif 'itag=34' in stream_url or '=m34' in stream_url:
            return QUALITIES.HIGH
        elif 'itag=35' in stream_url or '=m35' in stream_url:
            return QUALITIES.HIGH
        elif 'itag=37' in stream_url or '=m37' in stream_url:
            return QUALITIES.HD1080
        else:
            return QUALITIES.HIGH


def search(video_type, title, year):
    search_url = urlparse.urljoin(base_url, '/search?keyword=%s' % (urllib.quote_plus(title)))
    html = get_url(search_url)
    results = []
    match_year = ''
    fragment = dom_parser.parse_dom(html, 'ul', {'class': 'movie-list'})
    if fragment:
        for item in dom_parser.parse_dom(fragment[0], 'li'):
            if dom_parser.parse_dom(item, 'div', {'class': '[^"]*episode[^"]*'}): continue
            match = re.search('href="([^"]+).*?title="([^"]+)', item)
            if match:
                match_url, match_title = match.groups()
                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': '', 'url': _pathify_url(match_url)}
                    results.append(result)

    return results


def get_sources(suf_url):
    source_url = suf_url
    hosters = []
    sources = {}
    if source_url and source_url != FORCE_NO_MATCH:
        url = urlparse.urljoin(base_url, source_url)
        #print "URL IS = "+url
        html = get_url(url)
        for server_list in dom_parser.parse_dom(html, 'ul', {'class': 'episodes'}):
            for hash_id in dom_parser.parse_dom(server_list, 'a', ret='data-id'):
                now = time.localtime()
                url = urlparse.urljoin(base_url, hash_url)  #/ajax/film/episode?hash_id=%s&f=&p=%s
                url = url % (hash_id, now.tm_hour + now.tm_min)
                #print "CRAZY URL IS = "+url
                html =_http_get(url, headers=XHR, cache_limit=.5)
                #print "HTML IS = "+html
                if html:
                    try:
                        #print "I DID JSON"
                        js_result = json.loads(html)
                        #print js_result
                    except ValueError:
                        print 'Invalid JSON returned: %s: %s' % (html)
                        log_utils.log('Invalid JSON returned: %s' % (html), log_utils.LOGWARNING)
                    else:
                        if 'videoUrlHash' in js_result and 'grabber' in js_result:
                           # print "ITS IN THERE"
                            query = {'flash': 1, 'json': 1, 's': now.tm_min, 'link': js_result['videoUrlHash'], '_': int(time.time())}
                            query['link'] = query['link'].replace('\/', '/')
                            grab_url = js_result['grabber'].replace('\/', '/')
                            grab_url += '?' + urllib.urlencode(query)
                            html =get_url(grab_url)
                            #print "NEW HTML IS = "+html
                            if html:
                                try:
                                    js_result = json.loads(html)
                                except ValueError:
                                    print 'Invalid JSON returned: %s: %s' % (html)
                                else:
                                    for result in js_result:
                                        if 'label' in result:
                                            quality = _height_get_quality(result['label'])
                                        else:
                                            quality = _gv_get_quality(result['file'])
                                        sources[result['file']] = quality

        for source in sources:
            hoster = {'hostname':'9Movies','multi-part': False, 'host': _get_direct_hostname(source),  'quality': sources[source], 'view': None, 'rating': None, 'url': source, 'direct': True}
            hosters.append(hoster)
    hosters = main_scrape.apply_urlresolver(hosters)
    return hosters


def ninemovies(name):
    try:
        title = name[:-7]
        movie_year = name[-6:]
        year = movie_year.replace('(','').replace(')','')
        video_type = 'movies'
        source = search(video_type,title,year)
        #print source
        for e in source:
                # print e
                url = e['url']
                year = e['year']
                name = e['title']
                # print "SUF URL IS = "+url
                srcurl =base_url+url
                hosters=get_sources(srcurl)
                hosters = main_scrape.apply_urlresolver(hosters)
                return hosters
    except Exception as e:
        hosters=[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='Nine Movies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters


def _set_cookies(base_url, cookies):
        cj = cookielib.LWPCookieJar(cookie_file)
        try: cj.load(ignore_discard=True)
        except: pass
        if kodi.get_setting('debug') == 'true':
            log_utils.log('Before Cookies: %s' % (cookies_as_str(cj)), log_utils.LOGDEBUG)
        domain = urlparse.urlsplit(base_url).hostname
        for key in cookies:
            c = cookielib.Cookie(0, key, str(cookies[key]), port=None, port_specified=False, domain=domain, domain_specified=True,
                                 domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None,
                                 comment_url=None, rest={})
            cj.set_cookie(c)
        cj.save(ignore_discard=True)
        if kodi.get_setting('debug') == 'true':
            log_utils.log('After Cookies: %s' % (cookies_as_str(cj)), log_utils.LOGDEBUG)
        return cj


def cookies_as_str(cj):
    s = ''
    c = cj._cookies
    for domain in c:
        s += '{%s: ' % (domain)
        for path in c[domain]:
            s += '{%s: ' % (path)
            for cookie in c[domain][path]:
                s += '{%s=%s}' % (cookie, c[domain][path][cookie].value)
            s += '}'
        s += '} '
    return s


def __fix_bad_cookies():
    c = cj._cookies
    for domain in c:
        for path in c[domain]:
            for key in c[domain][path]:
                cookie = c[domain][path][key]
                if cookie.expires > sys.maxint:
                    log_utils.log('Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint))
                    cookie.expires = sys.maxint