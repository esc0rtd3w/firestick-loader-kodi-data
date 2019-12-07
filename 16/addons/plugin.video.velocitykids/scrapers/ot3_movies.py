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
import xml.etree.ElementTree as ET
import main_scrape
addon_id = kodi.addon_id


timeout = int(kodi.get_setting('scraper_timeout'))

def __enum(**enums):
    return type('Enum', (), enums)


VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')
#COOKIE STUFF
tools.create_directory(tools.AOPATH, "All_Cookies/123Movies")
cookiepath = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'All_Cookies','123Movies/'))
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


Q_ORDER = {QUALITIES.LOW: 1, QUALITIES.MEDIUM: 2, QUALITIES.HIGH: 3, QUALITIES.HD720: 4, QUALITIES.HD1080: 5}
Q_LIST = [item[0] for item in sorted(Q_ORDER.items(), key=lambda x:x[1])]


BLOG_Q_MAP = {}
BLOG_Q_MAP[QUALITIES.LOW] = [' CAM ', ' TS ', ' R6 ', 'CAMRIP']
BLOG_Q_MAP[QUALITIES.MEDIUM] = ['-XVID', '-MP4', 'MEDIUM']
BLOG_Q_MAP[QUALITIES.HIGH] = ['HDRIP', 'DVDRIP', 'BRRIP', 'BDRIP', '480P']
BLOG_Q_MAP[QUALITIES.HD720] = ['720', 'HDTS', ' HD ']
BLOG_Q_MAP[QUALITIES.HD1080] = ['1080']

HOST_Q = {}
HOST_Q[QUALITIES.LOW] = ['youwatch', 'allmyvideos', 'played.to', 'gorillavid']
HOST_Q[QUALITIES.MEDIUM] = ['primeshare', 'exashare', 'bestreams', 'flashx', 'vidto', 'vodlocker', 'thevideo', 'vidzi', 'vidbull', 'realvid', 'nosvideo', 'daclips', 'sharerepo', 'zalaa']
HOST_Q[QUALITIES.HIGH] = ['vidspot', 'mrfile', 'divxstage', 'streamcloud', 'mooshare', 'novamov', 'mail.ru', 'vid.ag']
HOST_Q[QUALITIES.HD720] = ['thefile', 'sharesix', 'filenuke', 'vidxden', 'movshare', 'nowvideo', 'vidbux', 'streamin.to']
HOST_Q[QUALITIES.HD1080] = ['hugefiles', '180upload', 'mightyupload', 'videomega']




timeout = 30
######################

base_url = kodi.get_setting('123movies_base_url')
PLAYLIST_URL1 = 'movie/loadEmbed/%s'
PLAYLIST_URL2 = 'movie/loadepisoderss/%s/%s/3/%s'
SL_URL = '/movie/loadepisodes/%s'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD-720P': QUALITIES.HD720}
##############################

class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        log_utils.log('Stopping Redirect', log_utils.LOGDEBUG)
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
            request.add_unredirected_header('Host', '123movies.to')
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
            return 'gvideo'
        else:
            return 'Native'


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
        search_url = urlparse.urljoin(base_url, '/movie/search/')
        search_url += title
        html = _http_get(search_url, cache_limit=1)
        results = []
        for item in dom_parser.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'mli-info'})
            match_url = re.search('href="([^"]+)', item, re.DOTALL)
            match_year = re.search('class="jt-info">(\d{4})<', item)
            is_episodes = dom_parser.parse_dom(item, 'span', {'class': 'mli-eps'})

            if match_title and match_url and not is_episodes:
                match_title = match_title[0]
                match_title = re.sub('</?h2>', '', match_title)
                match_title = re.sub('\s+\d{4}$', '', match_title)
                url = urlparse.urljoin(match_url.group(1), 'watching.html')
                match_year = match_year.group(1) if match_year else ''

                if not year or not match_year or year == match_year:
                    result = {'title': match_title, 'year': match_year, 'url': _pathify_url(url)}
                    results.append(result)

        return results

def get_sources(suf_url,pre_url):
        source_url = suf_url
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(base_url, source_url)
            page_html = _http_get(url, cache_limit=.5)
            movie_id = dom_parser.parse_dom(page_html, 'div', {'id': 'media-player'}, 'movie-id')
            if movie_id:
                server_url = SL_URL % (movie_id[0])
                url = urlparse.urljoin(base_url, server_url)
                html = _http_get(url, cache_limit=.5)
                sources = {}
                for match in re.finditer('loadEpisode\(\s*(\d+)\s*,\s*(\d+)\s*\).*?class="btn-eps[^>]*>([^<]+)', html, re.DOTALL):
                    link_type, link_id, q_str = match.groups()
                    if link_type in ['12', '13', '14']:
                        url = urlparse.urljoin(base_url, PLAYLIST_URL1 % (link_id))
                        sources.update(__get_link_from_json(url, q_str))
                    else:
                        media_url = __get_ep_pl_url(link_type, page_html)
                        if media_url:
                            url = urlparse.urljoin(base_url, media_url)
                            xml = _http_get(url, cache_limit=.5)
                            sources.update(__get_links_from_xml(xml, pre_url))

            for source in sources:
                if sources[source]['direct']:
                    host = _get_direct_hostname(source)
                else:
                    host = urlparse.urlparse(source).hostname
                hoster = {'hostname':'123Movies','multi-part': False, 'host': host, 'quality': sources[source]['quality'], 'views': None, 'rating': None, 'url': source, 'direct': sources[source]['direct']}
                hosters.append(hoster)
        hosters = main_scrape.apply_urlresolver(hosters)
        return hosters



def __get_ep_pl_url( link_id, html):
        movie_id = dom_parser.parse_dom(html, 'div', {'id': 'media-player'}, 'movie-id')
        player_token = dom_parser.parse_dom(html, 'div', {'id': 'media-player'}, 'player-token')
        if movie_id and player_token:
            return PLAYLIST_URL2 % (movie_id[0], player_token[0], link_id)

def __get_link_from_json( url, q_str):
    sources = {}
    html = _http_get(url, cache_limit=.5)
    js_result = _parse_json(html, url)
    if 'embed_url' in js_result:
        quality = Q_MAP.get(q_str.upper(), QUALITIES.HIGH)
        sources[js_result['embed_url']] = {'quality': quality, 'direct': False}
    return sources

def __get_links_from_xml(xml, video):
    sources = {}
    try:
        root = ET.fromstring(xml)
        for item in root.findall('.//item'):
            title = item.find('title').text
            for source in item.findall('{http://rss.jwpcdn.com/}source'):
                stream_url = source.get('file')
                label = source.get('label')
                if _get_direct_hostname(stream_url) == 'gvideo':
                    quality = _gv_get_quality(stream_url)
                elif label:
                    quality = _height_get_quality(label)
                else:
                    quality = _blog_get_quality(video, title, '')
                sources[stream_url] = {'quality': quality, 'direct': True}
                if kodi.get_setting('debug') == "true":
                        kodi.notify(header='ERROR', msg='Adding stream: %s Quality: %s' % (stream_url, quality), duration=5000, sound=None)
    except Exception as e:
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='ERROR', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)

    return sources


def _set_cookies(base_url, cookies):
        cj = cookielib.LWPCookieJar(cookie_file)
        try: cj.load(ignore_discard=True)
        except: pass
        if kodi.get_setting('debug') == 'true':
            log_utils.log('Before Cookies: %s' % (cookies_as_str(cj)), log_utils.LOGDEBUG)
        domain = urlparse.urlsplit(base_url).hostname
        for key in cookies:
            c = cookielib.Cookie(0, key, str(cookies[key]), port=None, port_specified=False, domain=domain, domain_specified=True,domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=False, comment=None,comment_url=None, rest={})
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
                    if kodi.get_setting('debug') == "true":
                        kodi.notify(header='Cookie Fix', msg='Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint), duration=5000, sound=None)
                        log_utils.log('Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint), xbmc.LOGERROR)
                    cookie.expires = sys.maxint


def _blog_get_quality(video, q_str, host):
        """
        Use the q_str to determine the post quality; then use the host to determine host quality
        allow the host to drop the quality but not increase it
        """
        q_str.replace(video.title, '')
        q_str.replace(str(video.year), '')
        q_str = q_str.upper()

        post_quality = None
        for key in Q_LIST:
            if any(q in q_str for q in BLOG_Q_MAP[key]):
                post_quality = key

        return _get_quality(video, host, post_quality)


def _get_quality(video, host, base_quality=None):
        host = host.lower()
        # Assume movies are low quality, tv shows are high quality
        if base_quality is None:
            if video.video_type == VIDEO_TYPES.MOVIE:
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

        # log_utils.log('q_str: %s, host: %s, post q: %s, host q: %s' % (q_str, host, post_quality, host_quality), log_utils.LOGDEBUG)
        if host_quality is not None and Q_ORDER[host_quality] < Q_ORDER[quality]:
            quality = host_quality

        return quality

def _parse_json(html, url=''):
        if html:
            try:
                return json.loads(html)
            except ValueError:
                log_utils.log('Invalid JSON returned: %s: %s' % (html, url), xbmc.LOGERROR)
                return {}
        else:
            log_utils.log('Empty JSON object: %s: %s' % (html, url), xbmc.LOGERROR)
            return {}

def ot3_movies(name):
    try:
        title = name[:-7]
        movie_year = name[-6:]
        year = movie_year.replace('(','').replace(')','')
        video_type = 'movies'
        source = search(video_type,title,year)
        for e in source:
                url = e['url']
                year = e['year']
                name = e['title']
                srcurl =base_url+url
                hosters=get_sources(srcurl,url)
                hosters = main_scrape.apply_urlresolver(hosters)
                return hosters
    except Exception as e:
        hosters =[]
        log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        if kodi.get_setting('error_notify') == "true":
            kodi.notify(header='123Movies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
        return hosters
