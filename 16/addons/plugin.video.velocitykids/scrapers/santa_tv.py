import urllib2,urllib,re,os
import random
import urlparse
import sys
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi
from tm_libs import dom_parser
from libs import log_utils
import tools
from libs import cloudflare
from libs import log_utils
from tm_libs import dom_parser
import cookielib
from StringIO import StringIO
import gzip
import main_scrape
import base64
addon_id = kodi.addon_id


timeout = int(kodi.get_setting('scraper_timeout'))


tools.create_directory(tools.AOPATH, "All_Cookies/SantaSeries")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','SantaSeries/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')



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


HOST_Q = {}
HOST_Q[QUALITIES.LOW] = ['youwatch', 'allmyvideos', 'played.to', 'gorillavid']
HOST_Q[QUALITIES.MEDIUM] = ['primeshare', 'exashare', 'bestreams', 'flashx', 'vidto', 'vodlocker', 'thevideo', 'vidzi', 'vidbull',
                            'realvid', 'nosvideo', 'daclips', 'sharerepo', 'zalaa', 'filehoot', 'vshare']
HOST_Q[QUALITIES.HIGH] = ['vidspot', 'mrfile', 'divxstage', 'streamcloud', 'mooshare', 'novamov', 'mail.ru', 'vid.ag']
HOST_Q[QUALITIES.HD720] = ['thefile', 'sharesix', 'filenuke', 'vidxden', 'movshare', 'nowvideo', 'vidbux', 'streamin.to', 'allvid.ch']
HOST_Q[QUALITIES.HD1080] = ['hugefiles', '180upload', 'mightyupload', 'videomega', 'allmyvideos']
Q_ORDER = {QUALITIES.LOW: 1, QUALITIES.MEDIUM: 2, QUALITIES.HIGH: 3, QUALITIES.HD720: 4, QUALITIES.HD1080: 5}


# base_url = 'http://www.santaseries.com'


base_url = kodi.get_setting('santatv_base_url')





def format_source_label( item):
    if 'label' in item:
        return '[%s] %s (%s)' % (item['quality'], item['host'], item['label'])
    else:
        return '[%s] %s' % (item['quality'], item['host'])


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
            #request.add_unredirected_header('Host', base_url)
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
            if kodi.get_setting('debug') == "true":
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
                 print 'Response exceeded allowed size. %s => %s / %s' % (url, content_length, MAX_RESPONSE)

            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO(response.read(MAX_RESPONSE))
                f = gzip.GzipFile(fileobj=buf)
                html = f.read()
            else:
                html = response.read(MAX_RESPONSE)
        except urllib2.HTTPError as e:
            if e.code == 503 and 'cf-browser-verification' in e.read():
                print "WAS ERROR"
                html = cloudflare.solve(url, cj, _get_ua())
                if not html:
                    return ''
            else:
                print 'Error (%s) during THE scraper http get: %s' % (str(e), url)
                return ''
        except Exception as e:
            print 'Error (%s) during scraper http get: %s' % (str(e), url)
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
            print 'Creating New User Agent: %s' % (user_agent)
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
        print "returning pathify "+ url
        return url


def get_sources(video):
    source_url = urlparse.urljoin(base_url, video)
    # print url
    # source_url = _http_get(url)
    hosters = []
    if source_url and source_url != FORCE_NO_MATCH:
        page_url = urlparse.urljoin(base_url, source_url)
        html = _http_get(page_url, cache_limit=.25)
        for link in dom_parser.parse_dom(html, 'li', {'class': 'elemento'}):
            match = re.search('href="[^"]*/load-episode/#([^"]+)', link)
            #print match
            if match:
                stream_url = base64.decodestring(match.group(1))
               # print "STREAM URL BASE IS " +stream_url
                if stream_url.startswith('http'):
                    label = dom_parser.parse_dom(link, 'span', {'class': 'd'})
                    host = urlparse.urlparse(stream_url).hostname
                    quality = get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host,  'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    if label: hoster['label'] = label[0]
                    hosters.append(hoster)
    return hosters





def _get_episode_url(show_url,video, season,episode):
    episode_pattern = 'href="([^"]*-season-%s-episode-%s(?!\d)[^"]*)' % (season, episode)
    return _default_get_episode_url(show_url, video, episode_pattern)



def _default_get_episode_url(show_url, video, episode_pattern, title_pattern='', airdate_pattern='', data=None, headers=None):
        #print "Before Default Episode"
        ##log_utils.log('Default Episode Url: |%s|%s|%s|%s|' % (base_url, show_url, str(video).decode('utf-8', 'replace'), data), log_utils.LOGDEBUG)
        if 'http://' not in  show_url:
             url = urlparse.urljoin(base_url, show_url)
        else:
            url = base_url+show_url
        #print "After Default Episode"
        #print url
        html = get_url(url)
        #print html
        if html:
            # force_title = _force_title(video)
            #
            # if not force_title:
                match = re.search(episode_pattern, html, re.DOTALL)
                if match:
                   # print "BEFORE PATHIFY"
                    return _pathify_url(match.group(1))
                else:
                    log_utils.log('Skipping  as Episode not found: %s' % (url), log_utils.LOGDEBUG)
                    #print "ODD SET DETECTED"
                    # norm_title = _normalize_title(video.ep_title)
                    # for match in re.finditer(title_pattern, html, re.DOTALL | re.I):
                    #     episode = match.groupdict()
                    #     if norm_title == _normalize_title(episode['title']):
                    #         return _pathify_url(episode['url'])



def search( video_type,title, year):
    results = []
    search_url = urlparse.urljoin(base_url, '/?s=')
    search_url += urllib.quote_plus(title)
    #print "search url is " +search_url
    html = get_url(search_url)
    #print "HTML IS " +html
    for item in dom_parser.parse_dom(html, 'div', {'class': 'item'}):
        match_url = dom_parser.parse_dom(item, 'a', ret='href')
        match_title = dom_parser.parse_dom(item, 'span', {'class': 'tt'})
        match_year = dom_parser.parse_dom(item, 'span', {'class': 'year'})
        if match_url and match_title:
            match_url = match_url[0]
            match_title = match_title[0]
            if match_year:
                match_year = match_year[0]
            else:
                match_year = ''

            if not year or not match_year or year == match_year:
                result = {'url': _pathify_url(match_url), 'title': match_title, 'year': match_year}
                results.append(result)
    #print results
    return results


def make_vid_params(video_type, title, year, season, episode, ep_title, ep_airdate):
    return '|%s|%s|%s|%s|%s|%s|%s|' % (video_type, title, year, season, episode, ep_title, ep_airdate)



def santa_tv(name,movie_title):
    try:
        title = movie_title[:-7]
        movie_year = movie_title[-6:]
        year = movie_year.replace('(','').replace(')','')
        video_type = 'shows'
        show_url = search(video_type,title,year)
        for e in show_url:
                url = e['url']
                newseas=re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
                for sea,epi,epi_title in newseas:
                    video = make_vid_params('Episode',title,year,sea,epi,epi_title,'')
                    ep_url = _get_episode_url(url, video,sea,epi)
                    print "HERE IS END" +ep_url
                    hosters=get_sources(ep_url)
                    hosters = main_scrape.apply_urlresolver(hosters)
                    return hosters

    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='SantaSeries',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters

def _set_cookies(base_url, cookies):
        cj = cookielib.LWPCookieJar(cookie_file)
        try: cj.load(ignore_discard=True)
        except: pass
        if kodi.get_setting('debug') == "true":
             print 'Before Cookies: %s' % (cookies_as_str(cj))
        domain = urlparse.urlsplit(base_url).hostname
        for key in cookies:
            c = cookielib.Cookie(0, key, str(cookies[key]), port=None, port_specified=False, domain=domain, domain_specified=True,
                                 domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None,
                                 comment_url=None, rest={})
            cj.set_cookie(c)
        cj.save(ignore_discard=True)
        if kodi.get_setting('debug') == "true":
             print 'After Cookies: %s' % (cookies_as_str(cj))
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
                    print 'Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint)
                    cookie.expires = sys.maxint


def get_quality(video, host, base_quality=None):
    host = host.lower()
    # Assume movies are low quality, tv shows are high quality
    if base_quality is None:
        if video.video_type == "movies":
            quality = QUALITIES.LOW
        else:
            quality = QUALITIES.HIGH
    else:
        quality = base_quality

    host_quality = None
    if host:
        for key in HOST_Q:
            if any(hostname in host for hostname in HOST_Q[key]):
                host_quality = key
                break

    #log_utils.log('q_str: %s, host: %s, post q: %s, host q: %s' % (q_str, host, post_quality, host_quality), log_utils.LOGDEBUG)
    if host_quality is not None and Q_ORDER[host_quality] < Q_ORDER[quality]:
        quality = host_quality

    return quality


