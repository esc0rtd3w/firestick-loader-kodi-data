"""
    SALTS XBMC Addon
    Copyright (C) 2016 tknorris
    Altered by : Blazetamer for "V"

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import base64
import datetime
import random
import re
import sys
import time
import urllib
import urlparse
import json
import os.path
from libs import kodi
from libs import log_utils
import htmlentitydefs
from libs.constants import *




def __enum(**enums):
    return type('Enum', (), enums)

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
MAX_RESPONSE = 1024 * 1024 * 2


VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')


HOST_Q = {}
HOST_Q[QUALITIES.LOW] = ['youwatch', 'allmyvideos', 'played.to', 'gorillavid']
HOST_Q[QUALITIES.MEDIUM] = ['primeshare', 'exashare', 'bestreams', 'flashx', 'vidto', 'vodlocker', 'vidzi', 'vidbull', 'realvid', 'nosvideo',
                            'daclips', 'sharerepo', 'zalaa', 'filehoot', 'vshare.io']
HOST_Q[QUALITIES.HIGH] = ['vidspot', 'mrfile', 'divxstage', 'streamcloud', 'mooshare', 'novamov', 'mail.ru', 'vid.ag', 'thevideo']
HOST_Q[QUALITIES.HD720] = ['thefile', 'sharesix', 'filenuke', 'vidxden', 'movshare', 'nowvideo', 'vidbux', 'streamin.to', 'allvid.ch', 'weshare']
HOST_Q[QUALITIES.HD1080] = ['hugefiles', '180upload', 'mightyupload', 'videomega', 'allmyvideos']

Q_ORDER = {QUALITIES.LOW: 1, QUALITIES.MEDIUM: 2, QUALITIES.HIGH: 3, QUALITIES.HD720: 4, QUALITIES.HD1080: 5}



def disable_sub_check(settings):
    for i in reversed(xrange(len(settings))):
        if 'sub_check' in settings[i]:
            settings[i] = settings[i].replace('default="true"', 'default="false"')
    return settings

def get_ua():
    try: last_gen = int(kodi.get_setting('last_ua_create'))
    except: last_gen = 0
    if not kodi.get_setting('current_ua') or last_gen < (time.time() - (7 * 24 * 60 * 60)):
        index = random.randrange(len(RAND_UAS))
        versions = {'win_ver': random.choice(WIN_VERS), 'feature': random.choice(FEATURES), 'br_ver': random.choice(BR_VERS[index])}
        user_agent = RAND_UAS[index].format(**versions)
        log_utils.log('Creating New User Agent: %s' % (user_agent), log_utils.LOGDEBUG)
        kodi.set_setting('current_ua', user_agent)
        kodi.set_setting('last_ua_create', str(int(time.time())))
    else:
        user_agent = kodi.get_setting('current_ua')
    return user_agent

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
                
# TODO: Test with CJ
def fix_bad_cookies(cookies):
    for domain in cookies:
        for path in cookies[domain]:
            for key in cookies[domain][path]:
                cookie = cookies[domain][path][key]
                if cookie.expires > sys.maxint:
                    log_utils.log('Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint), log_utils.LOGDEBUG)
                    cookie.expires = sys.maxint
    return cookies

def force_title(video):
        trakt_str = kodi.get_setting('force_title_match')
        trakt_list = trakt_str.split('|') if trakt_str else []
        return str(video.trakt_id) in trakt_list

def normalize_title(title):
    if title is None: title = ''
    title = cleanse_title(title)
    new_title = title.upper()
    new_title = re.sub('[^A-Za-z0-9]', '', new_title)
    if isinstance(new_title, unicode):
        new_title = new_title.encode('utf-8')
    # log_utils.log('In title: |%s| Out title: |%s|' % (title,new_title), log_utils.LOGDEBUG)
    return new_title

def blog_get_quality(video, q_str, host):
    """
    Use the q_str to determine the post quality; then use the host to determine host quality
    allow the host to drop the quality but not increase it
    """
    # q_str.replace(video.title, '')
    # q_str.replace(str(video.year), '')
    q_str = q_str.upper()

    post_quality = None
    for key in [item[0] for item in sorted(Q_ORDER.items(), key=lambda x:x[1])]:
        if any(q in q_str for q in BLOG_Q_MAP[key]):
            post_quality = key

    return get_quality(video, host, post_quality)

def get_quality(video, host, base_quality=None):
    if host is None: host = ''
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

def width_get_quality(width):
    try: width = int(width)
    except: width = 320
    if width > 1280:
        quality = QUALITIES.HD1080
    elif width > 800:
        quality = QUALITIES.HD720
    elif width > 640:
        quality = QUALITIES.HIGH
    elif width > 320:
        quality = QUALITIES.MEDIUM
    else:
        quality = QUALITIES.LOW
    return quality

def height_get_quality(height):
    if str(height)[-1] in ['p', 'P']:
        height = str(height)[:-1]
        
    try: height = int(height)
    except: height = 200
    if height >= 800:
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

def gv_get_quality(stream_url):
    stream_url = urllib.unquote(stream_url)
    if 'itag=18' in stream_url or '=m18' in stream_url:
        return QUALITIES.MEDIUM
    elif 'itag=22' in stream_url or '=m22' in stream_url:
        return QUALITIES.HD720
    elif 'itag=15' in stream_url or '=m15' in stream_url:
        return QUALITIES.HD720
    elif 'itag=34' in stream_url or '=m34' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=35' in stream_url or '=m35' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=37' in stream_url or '=m37' in stream_url:
        return QUALITIES.HD1080
    elif 'itag=43' in stream_url or '=m43' in stream_url:
        return QUALITIES.MEDIUM
    else:
        return QUALITIES.HIGH

def get_sucuri_cookie(html):
    if 'sucuri_cloudproxy_js' in html:
        match = re.search("S\s*=\s*'([^']+)", html)
        if match:
            s = base64.b64decode(match.group(1))
            s = s.replace(' ', '')
            s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
            s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
            s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
            s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
            s = re.sub(';location.reload\(\);', '', s)
            s = re.sub(r'\n', '', s)
            s = re.sub(r'document\.cookie', 'cookie', s)
            try:
                cookie = ''
                exec(s)
                match = re.match('([^=]+)=(.*)', cookie)
                if match:
                    return {match.group(1): match.group(2)}
            except Exception as e:
                log_utils.log('Exception during sucuri js: %s' % (e), log_utils.LOGWARNING)
    
    return {}
    
def gk_decrypt(name, key, cipher_link):
    try:
        key += (24 - len(key)) * '\0'
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
        plain_text = decrypter.feed(cipher_link.decode('hex'))
        plain_text += decrypter.feed()
        plain_text = plain_text.split('\0', 1)[0]
    except Exception as e:
        log_utils.log('Exception (%s) during %s gk decrypt: cipher_link: %s' % (e, name, cipher_link), log_utils.LOGWARNING)
        plain_text = ''

    return plain_text

def parse_episode_link(link):
    episode = {'title': '', 'season': '-1', 'episode': '-1', 'airdate': '', 'height': '480', 'extra': '', 'dubbed': False}
    ep_patterns = [
        # episode with sxe or airdate and height
        '(?P<title>.*?){delim}S(?P<season>\d+){delim}*E(?P<episode>\d+)(?:E\d+)*.*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}(?P<season>\d+)x(?P<episode>\d+)(?:-\d+)*.*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}SEASON{delim}*(?P<season>\d+){delim}*EPISODE{delim}*(?P<episode>\d+).*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}\[S(?P<season>\d+)\]{delim}*\[E(?P<episode>\d+)(?:E\d+)*\].*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}S(?P<season>\d+){delim}*EP(?P<episode>\d+)(?:EP\d+)*.*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}(?P<airdate>\d{{4}}{delim}\d{{1,2}}{delim}\d{{1,2}}).*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',

        # episode with sxe or airdate not height
        '(?P<title>.*?){delim}S(?P<season>\d+){delim}*E(?P<episode>\d+)(?:E\d+)*{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}(?P<season>\d+)x(?P<episode>\d+)(?:-\d+)*{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}SEASON{delim}*(?P<season>\d+){delim}*EPISODE{delim}*(?P<episode>\d+){delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}\[S(?P<season>\d+)\]{delim}*\[E(?P<episode>\d+)(?:E\d+)*\]{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}S(?P<season>\d+){delim}*EP(?P<episode>\d+)(?:E\d+)*{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}(?P<airdate>\d{{4}}{delim}\d{{1,2}}{delim}\d{{1,2}}){delim}?(?P<extra>.*)',
        
        '(?P<title>.*?){delim}(?P<height>\d{{3,}})p{delim}?(?P<extra>.*)',  # episode with height only
        '(?P<title>.*)'  # title only
    ]
 
    return parse_link(link, episode, ep_patterns)

def parse_movie_link(link):
    movie = {'title': '', 'year': '', 'height': '480', 'extra': '', 'dubbed': False}
    movie_patterns = [
        '(?P<title>.*?){delim}(?P<year>\d{{4}}){delim}.*?(?P<height>\d+)p{delim}(?P<extra>.*)',  # title, year, and quality present
        '(?P<title>.*?){delim}(?P<year>\d{{4}}){delim}(?P<extra>.*)',  # title and year only
        '(?P<title>.*?){delim}(?P<height>\d+)p{delim}(?P<extra>.*)',  # title and quality only
        '(?P<title>.*)(?P<extra>\.[A-Z\d]{{3}}$)',  # title with extension
        '(?P<title>.*)'  # title only
    ]
    return parse_link(link, movie, movie_patterns)

def parse_link(link, item, patterns):
    delim = '[._ -]'
    link = urllib.unquote(link)
    file_name = link.split('/')[-1]
    for pattern in patterns:
        pattern = pattern.format(delim=delim)
        match = re.search(pattern, file_name, re.I)
        if match:
            match = dict((k, v) for k, v in match.groupdict().iteritems() if v is not None)
            item.update(match)
            break
    else:
        log_utils.log('No Regex Match: |%s|%s|' % (item, link), log_utils.LOGDEBUG)

    extra = item['extra'].upper()
    if 'X265' in extra or 'HEVC' in extra:
        item['format'] = 'x265'
    
    item['dubbed'] = True if 'DUBBED' in extra else False
    
    if 'airdate' in item and item['airdate']:
        pattern = '{delim}+'.format(delim=delim)
        item['airdate'] = re.sub(pattern, '-', item['airdate'])
        item['airdate'] = utils2.to_datetime(item['airdate'], "%Y-%m-%d").date()
        
    return item
    
def release_check(video, title, require_title=True):
    if video.video_type == VIDEO_TYPES.MOVIE:
        meta = parse_movie_link(title)
    else:
        meta = parse_episode_link(title)
    
    norm_title = normalize_title(video.title)
    match_norm_title = normalize_title(meta['title'])
    title_match = not require_title or (norm_title and (match_norm_title in norm_title or norm_title in match_norm_title))
    try: year_match = not video.year or not meta['year'] or video.year == meta['year']
    except: year_match = True
    try: sxe_match = int(video.season) == int(meta['season']) and int(video.episode) == int(meta['episode'])
    except: sxe_match = False
    try: airdate_match = video.ep_airdate == meta['airdate']
    except: airdate_match = False
    
    matches = title_match and year_match
    if video.video_type == VIDEO_TYPES.EPISODE:
        matches = matches and (sxe_match or airdate_match)
        
    if not matches:
        log_utils.log('*%s*%s*%s* - |%s|%s|%s| - |%s|%s|%s| - |%s|%s|' % (video, title, meta, norm_title, match_norm_title, title_match,
                                                                          video.year, meta.get('year'), year_match, sxe_match, airdate_match), log_utils.LOGDEBUG)
    return matches

def pathify_url(url):
    url = url.replace('\/', '/')
    pieces = urlparse.urlparse(url)
    if pieces.scheme:
        strip = pieces.scheme + ':'
    else:
        strip = ''
    strip += '//' + pieces.netloc
    url = url.replace(strip, '')
    if url.startswith('..'): url = url[2:]
    if not url.startswith('/'): url = '/' + url
    url = url.replace('/./', '/')
    url = url.replace('&amp;', '&')
    url = url.replace('//', '/')
    return url

def parse_json(html, url=''):
    if html:
        try:
            if not isinstance(html, unicode):
                if html.startswith('\xef\xbb\xbf'):
                    html = html[3:]
                elif html.startswith('\xfe\xff'):
                    html = html[2:]
                
            js_data = json.loads(html)
            if js_data is None:
                return {}
            else:
                return js_data
        except ValueError:
            log_utils.log('Invalid JSON returned: %s: %s' % (html, url), log_utils.LOGWARNING)
            return {}
    else:
        log_utils.log('Empty JSON object: %s: %s' % (html, url), log_utils.LOGDEBUG)
        return {}

def format_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def to_bytes(num, unit):
    unit = unit.upper()
    if unit.endswith('B'): unit = unit[:-1]
    units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    try: mult = pow(1024, units.index(unit))
    except: mult = sys.maxint
    return int(float(num) * mult)
    
def update_scraper(file_name, scraper_url, scraper_key):
    py_path = os.path.join(kodi.get_path(), 'scrapers', file_name)
    exists = os.path.exists(py_path)
    if not exists or (time.time() - os.path.getmtime(py_path)) > (8 * 60 * 60):
        new_py = utils2.get_and_decrypt(scraper_url, scraper_key)
        if new_py:
            if exists:
                with open(py_path, 'r') as f:
                    old_py = f.read()
            else:
                old_py = ''
            
            log_utils.log('%s path: %s, new_py: %s, match: %s' % (__file__, py_path, bool(new_py), new_py == old_py), log_utils.LOGDEBUG)
            if old_py != new_py:
                with open(py_path, 'w') as f:
                    f.write(new_py)

def urljoin(base_url, url):
    if not base_url.endswith('/'):
        base_url += '/'
    if url.startswith('/'):
        url = url[1:]
    return urlparse.urljoin(base_url, url)

def parse_params(params):
    result = {}
    params = params[1:-1]
    for element in params.split(','):
        key, value = element.split(':')
        key = re.sub('''['"]''', '', key.strip())
        value = re.sub('''['"]''', '', value.strip())
        result[key] = value
    return result

# if no default url has been set, then pick one and set it. If one has been set, use it
def set_default_url(Scraper):
    default_url = kodi.get_setting('%s-default_url' % (Scraper.get_name()))
    if not default_url:
        default_url = random.choice(Scraper.OPTIONS)
        kodi.set_setting('%s-default_url' % (Scraper.get_name()), default_url)
    Scraper.base_url = default_url
    return default_url


def cleanse_title(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])

            except KeyError:
                pass

        # replace nbsp with a space
        text = text.replace(u'\xa0', u' ')
        return text

    if isinstance(text, str):
        try:
            text = text.decode('utf-8')
        except:
            pass

    return re.sub("&#?\w+;", fixup, text.strip())

def to_datetime(dt_str, date_format):
    # strptime mysteriously fails sometimes with TypeError; this is a hacky workaround
    # note, they aren't 100% equal as time.strptime loses fractional seconds but they are close enough
    try: dt = datetime.datetime.strptime(dt_str, date_format)
    except (TypeError, ImportError): dt = datetime.datetime(*(time.strptime(dt_str, date_format)[0:6]))
    except Exception as e:
        log_utils.log('Failed dt conversion: (%s) - |%s|%s|' % (e, dt_str, date_format))
        dt = datetime.datetime.fromtimestamp(0)
    return dt

def extra_year(match_title_year):
    match = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
    if match:
        match_title, match_year = match.groups()
    else:
        match = re.search('(.*?)\s+(\d{4})$', match_title_year)
        if match:
            match_title, match_year = match.groups()
        else:
            match_title = match_title_year
            match_year = ''
    return match_title, match_year

def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])