"""
    SALTS XBMC Addon
    Copyright (C) 2016 tknorris

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
import hashlib
import base64
import random
import re
import sys
import time
import urllib
import urlparse
import json
import os.path
import string
import kodi
import log_utils
import dom_parser2
import xbmcgui
from salts_lib import pyaes
from salts_lib import utils2
from salts_lib.constants import *  # @UnusedWildImport

logger = log_utils.Logger.get_logger(__name__)
# logger.disable()

cleanse_title = utils2.cleanse_title
to_datetime = utils2.to_datetime
normalize_title = utils2.normalize_title
CAPTCHA_BASE_URL = 'http://www.google.com/recaptcha/api'

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
        logger.log('Creating New User Agent: %s' % (user_agent), log_utils.LOGDEBUG)
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
                    logger.log('Fixing cookie expiration for %s: was: %s now: %s' % (key, cookie.expires, sys.maxint), log_utils.LOGDEBUG)
                    cookie.expires = sys.maxint
    return cookies

def force_title(video):
        trakt_str = kodi.get_setting('force_title_match')
        trakt_list = trakt_str.split('|') if trakt_str else []
        return str(video.trakt_id) in trakt_list

def blog_get_quality(video, q_str, host):
    """
    Use the q_str to determine the post quality; then use the host to determine host quality
    allow the host to drop the quality but not increase it
    """
    q_str.replace(video.title, '')
    q_str.replace(str(video.year), '')
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

    # logger.log('q_str: %s, host: %s, post q: %s, host q: %s' % (q_str, host, post_quality, host_quality), log_utils.LOGDEBUG)
    if host_quality is not None and Q_ORDER[host_quality] < Q_ORDER[quality]:
        quality = host_quality

    return quality

def width_get_quality(width):
    try: width = int(width)
    except: width = 320
    if width > 1280:
        quality = QUALITIES.HD1080
    elif width > 854:
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
    if 'itag=18' in stream_url or '=m18' in stream_url or '/m18' in stream_url:
        return QUALITIES.MEDIUM
    elif 'itag=22' in stream_url or '=m22' in stream_url or '/m22' in stream_url:
        return QUALITIES.HD720
    elif 'itag=15' in stream_url or '=m15' in stream_url or '/m15' in stream_url:
        return QUALITIES.HD720
    elif 'itag=45' in stream_url or '=m45' in stream_url or '/m45' in stream_url:
        return QUALITIES.HD720
    elif 'itag=34' in stream_url or '=m34' in stream_url or '/m34' in stream_url:
        return QUALITIES.MEDIUM
    elif 'itag=35' in stream_url or '=m35' in stream_url or '/m35' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=59' in stream_url or '=m59' in stream_url or '/m59' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=44' in stream_url or '=m44' in stream_url or '/m44' in stream_url:
        return QUALITIES.HIGH
    elif 'itag=37' in stream_url or '=m37' in stream_url or '/m37' in stream_url:
        return QUALITIES.HD1080
    elif 'itag=38' in stream_url or '=m38' in stream_url or '/m38' in stream_url:
        return QUALITIES.HD1080
    elif 'itag=46' in stream_url or '=m46' in stream_url or '/m46' in stream_url:
        return QUALITIES.HD1080
    elif 'itag=43' in stream_url or '=m43' in stream_url or '/m43' in stream_url:
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
                logger.log('Exception during sucuri js: %s' % (e), log_utils.LOGWARNING)
    
    return {}
    
def gk_decrypt(name, key, cipher_link):
    try:
        key += (24 - len(key)) * '\0'
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(key))
        plain_text = decrypter.feed(cipher_link.decode('hex'))
        plain_text += decrypter.feed()
        plain_text = plain_text.split('\0', 1)[0]
    except Exception as e:
        logger.log('Exception (%s) during %s gk decrypt: cipher_link: %s' % (e, name, cipher_link), log_utils.LOGWARNING)
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
        '(?P<title>.*?){delim}\(?(?P<airdate>\d{{4}}{delim}\d{{1,2}}{delim}\d{{1,2}})\)?.*?{delim}(?P<height>\d+)p{delim}?(?P<extra>.*)',

        # episode with sxe or airdate not height
        '(?P<title>.*?){delim}S(?P<season>\d+){delim}*E(?P<episode>\d+)(?:E\d+)*{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}(?P<season>\d+)x(?P<episode>\d+)(?:-\d+)*{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}SEASON{delim}*(?P<season>\d+){delim}*EPISODE{delim}*(?P<episode>\d+){delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}\[S(?P<season>\d+)\]{delim}*\[E(?P<episode>\d+)(?:E\d+)*\]{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}S(?P<season>\d+){delim}*EP(?P<episode>\d+)(?:E\d+)*{delim}?(?P<extra>.*)',
        '(?P<title>.*?){delim}\(?(?P<airdate>\d{{4}}{delim}\d{{1,2}}{delim}\d{{1,2}})\)?{delim}?(?P<extra>.*)',
        
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
    link = cleanse_title(urllib.unquote(link))
    file_name = link.split('/')[-1]
    for pattern in patterns:
        pattern = pattern.format(delim=DELIM)
        match = re.search(pattern, file_name, re.I)
        if match:
            match = dict((k, v) for k, v in match.groupdict().iteritems() if v is not None)
            item.update(match)
            break
    else:
        logger.log('No Regex Match: |%s|%s|' % (item, link), log_utils.LOGDEBUG)

    extra = item['extra'].upper()
    if 'X265' in extra or 'HEVC' in extra:
        item['format'] = 'x265'
    
    item['dubbed'] = True if 'DUBBED' in extra else False
    
    if 'airdate' in item and item['airdate']:
        pattern = '{delim}+'.format(delim=DELIM)
        item['airdate'] = re.sub(pattern, '-', item['airdate'])
        item['airdate'] = utils2.to_datetime(item['airdate'], "%Y-%m-%d").date()
        
    return item
    
def release_check(video, title, require_title=True):
    if isinstance(title, unicode): title = title.encode('utf-8')
    left_meta = {'title': video.title, 'height': '', 'extra': '', 'dubbed': False}
    if video.video_type == VIDEO_TYPES.MOVIE:
        left_meta.update({'year': video.year})
        right_meta = parse_movie_link(title)
    else:
        left_meta.update({'season': video.season, 'episode': video.episode, 'airdate': video.ep_airdate})
        right_meta = parse_episode_link(title)
        
    return meta_release_check(video.video_type, left_meta, right_meta, require_title)

def meta_release_check(video_type, left_meta, right_meta, require_title=True):
    norm_title = normalize_title(left_meta['title'])
    match_norm_title = normalize_title(right_meta['title'])
    title_match = not require_title or (norm_title and (match_norm_title in norm_title or norm_title in match_norm_title))
    try: year_match = not left_meta['year'] or not right_meta['year'] or left_meta['year'] == right_meta['year']
    except: year_match = True
    try: sxe_match = int(left_meta['season']) == int(right_meta['season']) and int(left_meta['episode']) == int(right_meta['episode'])
    except: sxe_match = False
    try: airdate_match = left_meta['airdate'] == right_meta['airdate']
    except: airdate_match = False
    
    matches = title_match and year_match
    if video_type == VIDEO_TYPES.EPISODE:
        matches = matches and (sxe_match or airdate_match)
        
    if not matches:
        logger.log('*%s*%s* - |%s|%s|%s|%s|' % (left_meta, right_meta, title_match, year_match, sxe_match, airdate_match), log_utils.LOGDEBUG)
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
                html = html.decode('utf-8')
                
            js_data = json.loads(html)
            if js_data is None:
                return {}
            else:
                return js_data
        except (ValueError, TypeError):
            logger.log('Invalid JSON returned: %s: %s' % (html, url), log_utils.LOGWARNING)
            return {}
    else:
        logger.log('Empty JSON object: %s: %s' % (html, url), log_utils.LOGDEBUG)
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
            
            logger.log('%s path: %s, new_py: %s, match: %s' % (__file__, py_path, bool(new_py), new_py == old_py), log_utils.LOGDEBUG)
            if old_py != new_py:
                with open(py_path, 'w') as f:
                    f.write(new_py)

def urljoin(base_url, url, scheme='http', replace_path=False):
    def join_fields(left, right, sep):
        if right:
            if left:
                return left + sep + right
            else:
                return right
        else:
            return left

    base_parts = urlparse.urlparse(base_url)
    url_parts = urlparse.urlparse(url)
    new_scheme = base_parts.scheme or url_parts.scheme or scheme
    new_netloc = url_parts.netloc or base_parts.netloc
     
    if replace_path:
        new_path = url_parts.path
    else:
        if url_parts.path:
            new_path = base_parts.path + '/' + url_parts.path
            new_path = new_path.replace('///', '/').replace('//', '/')
        else:
            new_path = base_parts.path
     
    if new_path == '/':
        new_path = ''
 
    new_params = join_fields(base_parts.params, url_parts.params, ';')
    new_query = join_fields(base_parts.query, url_parts.query, '&')
    new_fragment = url_parts.fragment or base_parts.fragment
 
    new_parts = urlparse.ParseResult(scheme=new_scheme, netloc=new_netloc, path=new_path,
                                     params=new_params, query=new_query, fragment=new_fragment)
    return urlparse.urlunparse(new_parts)

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

def extra_year(match_title_year):
    match_title_year = match_title_year.strip()
    match = re.search('(.*?)\s+\((\d{4})[^)]*\)', match_title_year, re.UNICODE)
    if match:
        match_title, match_year = match.groups()
    else:
        match = re.search('(.*?)\s+(\d{4})$', match_title_year, re.UNICODE)
        if match:
            match_title, match_year = match.groups()
        else:
            match_title = match_title_year
            match_year = ''
    return match_title, match_year

def get_token(hash_len=16):
    chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
    base = hashlib.sha512(str(int(time.time()) / 60 / 60)).digest()
    return ''.join([chars[int(ord(c) % len(chars))] for c in base[:hash_len]])

def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])

def excluded_link(stream_url):
    return re.search('\.part\.?\d+', stream_url) or '.rar' in stream_url or 'sample' in stream_url or stream_url.endswith('.nfo')

def rshift(val, n):
    return (val % 0x100000000) >> n

def int32(x):
    x = 0xffffffff & x
    if x > 0x7fffffff:
        return int(-(~(x - 1) & 0xffffffff))
    else:
        return int(x)

# if salt is provided, it should be string
# ciphertext is base64 and passphrase is string
def evp_decode(cipher_text, passphrase, salt=None):
    cipher_text = base64.b64decode(cipher_text)
    if not salt:
        salt = cipher_text[8:16]
        cipher_text = cipher_text[16:]
    data = evpKDF(passphrase, salt)
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(data['key'], data['iv']))
    plain_text = decrypter.feed(cipher_text)
    plain_text += decrypter.feed()
    return plain_text

def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    target_key_size = key_size + iv_size
    derived_bytes = ""
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)

        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)

        for _i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)

        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]

        number_of_derived_words += len(block) / 4

    return {
        "key": derived_bytes[0: key_size * 4],
        "iv": derived_bytes[key_size * 4:]
    }

def get_direct_hostname(scraper, link):
    host = urlparse.urlparse(link).hostname
    if host and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
        return 'gvideo'
    else:
        return scraper.get_name()

def parse_sources_list(scraper, html, key='sources', var=None, file_key=None):
    sources = {}
    match = re.search('''['"]?%s["']?\s*:\s*[\{\[](\s*)[\}\]]''' % (key), html, re.DOTALL)
    if not match:
        match = re.search('''['"]?%s["']?\s*:\s*\[(.*?)\}\s*,?\s*\]''' % (key), html, re.DOTALL)
        if not match:
            match = re.search('''['"]?%s["']?\s*:\s*\{(.*?)\}''' % (key), html, re.DOTALL)
            if not match and var is not None:
                match = re.search('''%s\s*=\s*[^\[]*\[\{(.*?)\}\]''' % (var), html, re.DOTALL)
                
    if match:
        fragment = match.group(1)
    elif var is not None:
        fragment = ''.join(re.findall("%s\.push\(([^)]+)" % (var), html, re.DOTALL))
    else:
        fragment = ''
    
    file_key = 'file' if file_key is None else file_key
    files = re.findall('''['"]?%s['"]?\s*:\s*['"]([^'"]+)''' % (file_key), fragment, re.DOTALL)
    labels = re.findall('''['"]?label['"]?\s*:\s*['"]([^'"]*)''', fragment, re.DOTALL)
    for stream_url, label in map(None, files, labels):
        if not stream_url: continue
        
        stream_url = stream_url.replace('\/', '/')
        stream_url = urllib.unquote(stream_url)
        if get_direct_hostname(scraper, stream_url) == 'gvideo':
            sources[stream_url] = {'quality': gv_get_quality(stream_url), 'direct': True}
        elif label is not None and re.search('\d+p?', label, re.I):
            sources[stream_url] = {'quality': height_get_quality(label), 'direct': True}
        elif label is not None:
            sources[stream_url] = {'quality': label, 'direct': True}
        else:
            sources[stream_url] = {'quality': QUALITIES.HIGH, 'direct': True}

    return sources

def get_gk_links(scraper, html, page_url, page_quality, link_url, player_url):
    def get_real_gk_url(scraper, player_url, params):
        html = scraper._http_get(player_url, params=params, headers=XHR, cache_limit=.25)
        js_data = parse_json(html, player_url)
        data = js_data.get('data', {})
        if data is not None and 'files' in data:
            return data['files']
        else:
            return data

    sources = {}
    for attrs, _content in dom_parser2.parse_dom(html, 'a', req=['data-film', 'data-name', 'data-server']):
        data = {'ipplugins': 1, 'ip_film': attrs['data-film'], 'ip_server': attrs['data-server'], 'ip_name': attrs['data-name']}
        headers = {'Referer': page_url}
        headers.update(XHR)
        html = scraper._http_get(link_url, data=data, headers=headers, cache_limit=.25)
        js_data = parse_json(html, link_url)
        params = {'u': js_data.get('s'), 'w': '100%', 'h': 420, 's': js_data.get('v'), 'n': 0}
        stream_urls = get_real_gk_url(scraper, player_url, params)
        if stream_urls is None: continue
        
        if isinstance(stream_urls, basestring):
            sources[stream_urls] = page_quality
        else:
            for item in stream_urls:
                stream_url = item['files']
                if get_direct_hostname(scraper, stream_url) == 'gvideo':
                    quality = gv_get_quality(stream_url)
                elif 'quality' in item:
                    quality = height_get_quality(item['quality'])
                else:
                    quality = page_quality
                sources[stream_url] = quality
                    
    return sources

def get_files(scraper, url, headers=None, cache_limit=.5):
    sources = []
    for row in parse_directory(scraper, scraper._http_get(url, headers=headers, cache_limit=cache_limit)):
        source_url = urljoin(url, row['link'])
        if row['directory'] and not row['link'].startswith('..'):
            sources += get_files(scraper, source_url, headers={'Referer': url}, cache_limit=cache_limit)
        else:
            row['url'] = source_url
            sources.append(row)
    return sources

def parse_directory(scraper, html):
    rows = []
    for match in re.finditer(scraper.row_pattern, html):
        row = match.groupdict()
        if row['title'].endswith('/'): row['title'] = row['title'][:-1]
        row['directory'] = True if row['link'].endswith('/') else False
        if row['size'] == '-': row['size'] = None
        rows.append(row)
    return rows

def parse_google(scraper, link):
    sources = []
    html = scraper._http_get(link, cache_limit=.25)
    match = re.search('pid=([^&]+)', link)
    if match:
        vid_id = match.group(1)
        sources = parse_gplus(vid_id, html, link)
    else:
        if 'drive.google' in link or 'docs.google' in link or 'youtube.googleapis' in link:
            sources = parse_gdocs(scraper, link)
        if 'picasaweb' in link:
            i = link.rfind('#')
            if i > -1:
                link_id = link[i + 1:]
            else:
                link_id = ''
            match = re.search('feedPreload:\s*(.*}]}})},', html, re.DOTALL)
            if match:
                js = parse_json(match.group(1), link)
                for item in js['feed']['entry']:
                    if not link_id or item['gphoto$id'] == link_id:
                        for media in item['media']['content']:
                            if media['type'].startswith('video'):
                                sources.append(media['url'].replace('%3D', '='))
            else:
                match = re.search('preload\'?:\s*(.*}})},', html, re.DOTALL)
                if match:
                    js = parse_json(match.group(1), link)
                    for media in js['feed']['media']['content']:
                        if media['type'].startswith('video'):
                            sources.append(media['url'].replace('%3D', '='))

    sources = list(set(sources))
    return sources

def parse_gplus(vid_id, html, link=''):
    def extract_video(self, item):
        vid_sources = []
        for e in item:
            if not isinstance(e, dict): continue
            for key in e:
                for item2 in e[key]:
                    if not isinstance(item2, list): continue
                    for item3 in item2:
                        if not isinstance(item3, list): continue
                        for item4 in item3:
                            if not isinstance(item4, basestring): continue
                            s = urllib.unquote(item4).replace('\\0026', '&').replace('\\003D', '=')
                            for match in re.finditer('url=([^&]+)', s):
                                vid_sources.append(match.group(1))
        return vid_sources
    
    sources = []
    match = re.search('return\s+(\[\[.*?)\s*}}', html, re.DOTALL)
    if match:
        try:
            js = parse_json(match.group(1), link)
            for top_item in js:
                if not isinstance(top_item, list): continue
                for item in top_item:
                    if not isinstance(item, list): continue
                    for item2 in item:
                        if not isinstance(item2, list): continue
                        for item3 in item2:
                            if item3 == vid_id:
                                sources = extract_video(item2)
                                
        except Exception as e:
            logger.log('Google Plus Parse failure: %s - %s' % (link, e), log_utils.LOGWARNING)
    return sources

def parse_gdocs(scraper, link):
    urls = []
    link = re.sub('/preview$', '/view', link)
    html = scraper._http_get(link, cache_limit=.5)
    for match in re.finditer('\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', html):
        key, value = match.groups()
        if key != 'fmt_stream_map': continue
        urls += parse_stream_map(scraper, value)
    
    if not urls:
        doc_id = ''
        query = parse_query(link)
        if 'docid' in query:
            doc_id = query['docid']
        elif '/view' in link:
            match = re.search("'id'\s*:\s*'([^']+)", html)
            if match: doc_id = match.group(1)
                
        if doc_id:
            info_url = 'https://drive.google.com/get_video_info'
            html = scraper._http_get(info_url, params={'docid': doc_id}, headers={'Referer': link}, cache_limit=.5)
            if 'status=ok' not in html:
                html = base64.b64decode(html)
            query = parse_query(html)
            urls += parse_stream_map(scraper, query.get('fmt_stream_map', ''))
                
    return urls

def parse_stream_map(scraper, value):
    urls = []
    for item in value.split(','):
        _source_fmt, source_url = item.split('|')
        source_url = source_url.replace('\\u003d', '=').replace('\\u0026', '&')
        source_url = urllib.unquote(source_url)
        if scraper is not None:
            source_url += '|Cookie=%s' % (scraper._get_stream_cookies())
        urls.append(source_url)
    return urls
    
def do_recaptcha(scraper, key, tries=None, max_tries=None):
    challenge_url = CAPTCHA_BASE_URL + '/challenge?k=%s' % (key)
    html = scraper._cached_http_get(challenge_url, CAPTCHA_BASE_URL, timeout=DEFAULT_TIMEOUT, cache_limit=0)
    match = re.search("challenge\s+\:\s+'([^']+)", html)
    captchaimg = 'http://www.google.com/recaptcha/api/image?c=%s' % (match.group(1))
    img = xbmcgui.ControlImage(450, 0, 400, 130, captchaimg)
    wdlg = xbmcgui.WindowDialog()
    wdlg.addControl(img)
    wdlg.show()
    header = 'Type the words in the image'
    if tries and max_tries:
        header += ' (Try: %s/%s)' % (tries, max_tries)
    solution = kodi.get_keyboard(header)
    if not solution:
        raise Exception('You must enter text in the image to access video')
    wdlg.close()
    return {'recaptcha_challenge_field': match.group(1), 'recaptcha_response_field': solution}

def to_slug(title):
    slug = title.lower()
    slug = re.sub('[^A-Za-z0-9 -]', ' ', slug)
    slug = re.sub('\s\s+', ' ', slug)
    slug = re.sub(' ', '-', slug)
    return slug

def parse_query(url):
    q = {}
    queries = urlparse.parse_qs(urlparse.urlparse(url).query)
    if not queries: queries = urlparse.parse_qs(url)
    for key, value in queries.iteritems():
        if len(value) == 1:
            q[key] = value[0]
        else:
            q[key] = value
    return q

def get_days(age):
    age = age.replace('&nbsp;', ' ')
    match = re.search('(\d+)\s*(.*)', age)
    units = {'day': 1, 'week': 7, 'month': 30, 'year': 365}
    if match:
        num, unit = match.groups()
        unit = unit.lower()
        if unit.endswith('s'): unit = unit[:-1]
        days = int(num) * units.get(unit, 0)
    else:
        days = 0
        
    return days
