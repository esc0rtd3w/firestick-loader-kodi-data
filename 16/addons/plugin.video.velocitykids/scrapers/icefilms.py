
import urllib2,urllib,re,os
import random
import urlparse
import sys
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi
from libs import log_utils
import tools
import string
from libs import cloudflare
from libs import log_utils
import cookielib
from StringIO import StringIO
import gzip
import main_scrape
import HTMLParser
addon_id = kodi.addon_id


timeout = int(kodi.get_setting('scraper_timeout'))

def __enum(**enums):
    return type('Enum', (), enums)


VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')
#COOKIE STUFF



tools.create_directory(tools.AOPATH, "All_Cookies/IceFilms")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','IceFilms/'))
cookiejar = os.path.join(cookiepath,'cookies.lwp')
cj = cookielib.LWPCookieJar()
cookie_file = os.path.join(cookiepath,'cookies.lwp')




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







QUALITY_MAP = {'HD 720P': QUALITIES.HD720, 'HD 720P+': QUALITIES.HD720, 'DVDRIP / STANDARD DEF': QUALITIES.HIGH, 'DVD SCREENER': QUALITIES.HIGH}
base_url = kodi.get_setting('icefilms_base_url')
#base_url = 'http://www.icefilms.info'
LIST_URL = base_url + '/membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img='
AJAX_URL = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php?id=%s&s=%s&iqs=&url=&m=%s&cap= &sec=%s&t=%s'


class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        #print 'Stopping Redirect'
        return response

    https_response = http_response


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
            request.add_header('Accept', '*/*')
            request.add_unredirected_header('Host', request.get_host())
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


#def _http_get(url):
def get_url(url):
    request=urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
    response=urllib2.urlopen(request)
    link=response.read()
    cj.save(cookie_file, ignore_discard=True)
    response.close()
    return link



def get_name(cls):
    return 'IceFilms'

def resolve_link(link):
    url, query = link.split('?', 1)
    data = urlparse.parse_qs(query, True)
    url = urlparse.urljoin(base_url, url)
    url += '?s=%s&t=%s&app_id=VELOCITY' % (data['id'][0], data['t'][0])
    list_url = LIST_URL % (data['t'][0])
    headers = {'Referer': list_url}
    html = _http_get(url, data=data, headers=headers, cache_limit=.25)
    match = re.search('url=(.*)', html)
    if match:
        url = urllib.unquote_plus(match.group(1))
        return url


def get_sources(suf_url):
    source_url = suf_url
    #source_url = get_url(video)
    sources = []
    if source_url and source_url != FORCE_NO_MATCH:
        try:
            url = urlparse.urljoin(base_url, source_url)
            html = _http_get(url, cache_limit=.5)

            pattern = '<iframe id="videoframe" src="([^"]+)'
            match = re.search(pattern, html)
            frame_url = match.group(1)
            url = urlparse.urljoin(base_url, frame_url)
            html = _http_get(url, cache_limit=.1)

            match = re.search('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?', html)
            secret = ''.join(match.groups(''))

            match = re.search('"&t=([^"]+)', html)
            t = match.group(1)

            match = re.search('(?:\s+|,)s\s*=(\d+)', html)
            s_start = int(match.group(1))

            match = re.search('(?:\s+|,)m\s*=(\d+)', html)
            m_start = int(match.group(1))

            pattern = '<div class=ripdiv>(.*?)</div>'
            for container in re.finditer(pattern, html):
                fragment = container.group(0)
                match = re.match('<div class=ripdiv><b>(.*?)</b>', fragment)
                if match:
                    quality = QUALITY_MAP.get(match.group(1).upper(), QUALITIES.HIGH)
                else:
                    quality = None

                pattern = 'onclick=\'go\((\d+)\)\'>([^<]+)(<span.*?)</a>'
                for match in re.finditer(pattern, fragment):
                    link_id, label, host_fragment = match.groups()
                    source = {'hostname':'IceFilms','multi-part': False, 'quality': quality, 'label': label, 'rating': None, 'views': None, 'direct': False}
                    source['host'] = re.sub('(<[^>]+>|</span>)', '', host_fragment)
                    s = s_start + random.randint(3, 1000)
                    m = m_start + random.randint(21, 1000)
                    url = AJAX_URL % (link_id, s, m, secret, t)
                    # bobs_dogs = url
                    # source['url'] = resolve_link(bobs_dogs)
                    urls = resolve_link(url)
                    source['url'] = urls
                    sources.append(source)
        except Exception as e:
            log_utils.log('Failure (%s) during icefilms get sources: |%s|' % (str(e), suf_url), log_utils.LOGWARNING)

    return sources



def search(video_type, title, year):
    if video_type == 'movies':
        url = urlparse.urljoin(base_url, '/movies/a-z/')
    else:
        url = urlparse.urljoin(base_url, '/tv/a-z/')

    if title.upper().startswith('THE '):
        first_letter = title[4:5]
    elif title.upper().startswith('A '):
        first_letter = title[2:3]
    elif title[:1] in string.digits:
        first_letter = '1'
    else:
        first_letter = title[:1]
    url = url + first_letter.upper()
    #print "THE ICE URL IS : "+url
    html = _http_get(url, cache_limit=.25)
    h = HTMLParser.HTMLParser()
    html = unicode(html, 'windows-1252')
    html = h.unescape(html)
    norm_title = _normalize_title(title)
    pattern = 'class=star.*?href=([^>]+)>(.*?)(?:\s*\((\d+)\))?</a>'
    results = []
    for match in re.finditer(pattern, html, re.DOTALL):
        url, match_title, match_year = match.groups('')
        if norm_title in _normalize_title(match_title) and (not year or not match_year or year == match_year):
            result = {'url': url, 'title': match_title, 'year': match_year}
            results.append(result)
    return results

# def _get_episode_url( show_url, video):
#     episode_pattern = 'href=(/ip\.php[^>]+)>%sx0?%s\s+' % (video.season, video.episode)
#     title_pattern = 'class=star>\s*<a href=(?P<url>[^>]+)>(?:\d+x\d+\s+)+(?P<title>[^<]+)'
#     return super(IceFilms_Scraper)._default_get_episode_url(show_url, video, episode_pattern, title_pattern)




def _normalize_title(title):
        new_title = title.upper()
        new_title = re.sub('[^A-Za-z0-9]', '', new_title)
        log_utils.log('In title: |%s| Out title: |%s|' % (title,new_title), log_utils.LOGDEBUG)
        return new_title

def _set_cookies(base_url, cookies):
        cj = cookielib.LWPCookieJar(cookie_file)
        try: cj.load(ignore_discard=True)
        except: pass
        # if  printall == 'true':
        #      print 'Before Cookies: %s' % (cookies_as_str(cj))
        domain = urlparse.urlsplit(base_url).hostname
        for key in cookies:
            c = cookielib.Cookie(0, key, str(cookies[key]), port=None, port_specified=False, domain=domain, domain_specified=True,domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None,comment_url=None, rest={})
            cj.set_cookie(c)
        cj.save(ignore_discard=True)
        # if  printall == 'true':
        #      print 'After Cookies: %s' % (cookies_as_str(cj))
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


def _get_ua():
            index = random.randrange(len(RAND_UAS))
            user_agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
            if kodi.get_setting('debug') == "true":
                log_utils.log('Creating New User Agent: %s' % (user_agent))
            return user_agent


def ice_films(name):
    try:
        title = name[:-7]
        movie_year = name[-6:]
        year = movie_year.replace('(','').replace(')','')
        video_type = 'movies'
        source = search(video_type,title,year)
       # print source
        for e in source:
                url = e['url']
                year = e['year']
                name = e['title']
                srcurl =base_url+url
                hosters=get_sources(url)
                hosters = main_scrape.apply_urlresolver(hosters)
                return hosters
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='Ice Films',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters





def _get_episode_url(show_url, video,season,episode):
        #print "Before EPISODE PATTERN "+show_url
        episode_pattern = 'href=(/ip\.php[^>]+)>%sx0?%s\s+' % (season, episode)
        title_pattern = 'class=star>\s*<a href=(?P<url>[^>]+)>(?:\d+x\d+\s+)+(?P<title>[^<]+)'
        #print "After EPISODE PATTERN"
        return _default_get_episode_url(show_url, video, episode_pattern, title_pattern)


def _default_get_episode_url(show_url, video, episode_pattern, title_pattern='', airdate_pattern='', data=None, headers=None):
        #print "Before Default Episode"
        log_utils.log('Default Episode Url: |%s|%s|%s|%s|' % (base_url, show_url, str(video).decode('utf-8', 'replace'), data), log_utils.LOGDEBUG)
        # if 'http://' not in  show_url:
        #     url = urlparse.urljoin(base_url, show_url)
        # else:
        url = base_url+show_url
        #print "After Default Episode"
        #print url
        html = _http_get(url, data=data, headers=headers, cache_limit=2)
        if html:
            # force_title = _force_title(video)
            #
            # if not force_title:
                match = re.search(episode_pattern, html, re.DOTALL)
                if match:
                    #print "BEFORE PATHIFY"
                    return _pathify_url(match.group(1))
                else:
                    log_utils.log('Skipping  as Episode not found: %s' % (url), log_utils.LOGDEBUG)
                    #print "ODD SET DETECTED"
                    # norm_title = _normalize_title(video.ep_title)
                    # for match in re.finditer(title_pattern, html, re.DOTALL | re.I):
                    #     episode = match.groupdict()
                    #     if norm_title == _normalize_title(episode['title']):
                    #         return _pathify_url(episode['url'])

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
        #print "PATHIFIED URL IS : "+url
        return url

def make_vid_params(video_type, title, year, season, episode, ep_title, ep_airdate):
    return '|%s|%s|%s|%s|%s|%s|%s|' % (video_type, title, year, season, episode, ep_title, ep_airdate)


def ice_films_tv(name,movie_title):
    try:
        title = movie_title[:-7]
        movie_year = movie_title[-6:]
        year = movie_year.replace('(','').replace(')','')
        video_type = 'shows'
        # print title
        # print year

        show_url = search(video_type,title,year)
        for e in show_url:
                url = e['url']
                #TV MAIN URL RETURNED HERE
                newseas=re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
                for sea,epi,epi_title in newseas:
                    # print sea,epi
                    # print url
                    video = make_vid_params('Episode',title,year,sea,epi,epi_title,'')
                    #print video
                    ep_url = _get_episode_url(url, video,sea,epi)
                    #print "HERE IS END" +ep_url
                    hosters=get_sources(ep_url)

                    hosters = main_scrape.apply_urlresolver(hosters)
                    return hosters

    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='Ice Films',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters
