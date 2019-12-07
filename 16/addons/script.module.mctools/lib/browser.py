# -*- coding: utf-8 -*-
# Name:        browser.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Mini Browser
url = "http://example.com"
if Browser.open(url):
    print Browser.content

Using cloudhole
Using with GET request
url = "http://example.com"
Browser.get_cloudhole_key()
if Browser.open(url):
    print Browser.content

Using with GET request
data = {"value1": "12", "value1": "abc"}
url = "http://example.com"
if Browser.open(url, get_data=data):
    print Browser.content

Using with POST request
data = {"value1": "12", "value1": "abc"}
url = "http://example.com"
if Browser.open(url, post_data=data):
    print Browser.content
"""
import json
import re
import urllib2
from contextlib import closing
from cookielib import Cookie, LWPCookieJar
from os import path
from time import sleep, time
from urllib import quote_plus
from urllib import urlencode, unquote_plus
from urlparse import urlparse

import logger
from constants import *
from normalize import clear_string, normalize_string
from storage import Storage


class Browser:
    """
    Mini Web Browser with cookies handle
    """
    _counter = 0
    _cookies_filename = ''
    _cookies = LWPCookieJar()
    user_agent = USER_AGENT
    clearance = None
    content = None
    status = None
    headers = dict()

    def __init__(self):
        pass

    @classmethod
    def _create_cookies(cls, payload):
        return urlencode(payload)

    @classmethod
    def _read_cookies(cls, url=''):
        cls._cookies_filename = path.join(PATH_TEMP, urlparse(url).netloc + '_cookies.jar')
        if path.exists(cls._cookies_filename):
            try:
                cls._cookies.load(cls._cookies_filename)
            except Exception as e:
                logger.debug("Reading cookies error: %s" % repr(e))

        # Check for cf_clearance cookie provided by scakemyer
        # https://github.com/scakemyer/cloudhole-api
        if cls.clearance and not any(cookie.name == 'cf_clearance' for cookie in cls._cookies):
            t = str(int(time()) + 604800)
            c = Cookie(None, 'cf_clearance', cls.clearance[13:], None, False,
                       '.{uri.netloc}'.format(uri=urlparse(url)), True, True,
                       '/', True, False, t, False, None, None, None, False)
            cls._cookies.set_cookie(c)

    @classmethod
    def _save_cookies(cls):
        try:
            cls._cookies.save(cls._cookies_filename)
        except Exception as e:
            logger.debug("Saving cookies error: %s" % repr(e))

    @classmethod
    def _good_spider(cls):
        """
        Delay of 0.5 seconds to to call too many requests per second. Some pages start to block
        """
        cls._counter += 1
        if cls._counter > 1:
            sleep(0.5)  # good spider

    @classmethod
    def cookies(cls):
        """
        Cookies
        :return: LWPCookieJar format.
        """
        return cls._cookies

    @classmethod
    def open(cls, url='', language='en', post_data=None, get_data=None, use_cache=True):
        """
        Open a web page and returns its contents
        :param use_cache: if it uses the information stored in the cache
        :type use_cache: bool
        :param url: url address web page
        :type url: str
        :param language: language encoding web page
        :type language: str
        :param post_data: parameters for POST request
        :type post_data: dict
        :param get_data: parameters for GET request
        :type get_data: dict
        :return: True if the web page was opened successfully. False, otherwise.
        """
        if len(url) == 0:
            cls.status = 404
            cls.content = ''
            logger.debug('Empty url')
            return False

        # Check the cache
        cache_file = quote_plus(normalize_string(url)) + '.cache'
        if use_cache:
            cache = Storage.open(cache_file, ttl=15)
            if 'uri' in cache:
                cls.status = 200
                cls.content = cache['uri']
                cls.headers = cache['headers']
                logger.debug('Using cache for %s' % url)
                cache.close()
                logger.debug("Status: " + str(cls.status))
                logger.debug(repr(cls.content))
                return True

        # Creating request
        if post_data is None:
            post_data = {}
        if get_data is not None:
            url += '?' + urlencode(get_data)

        logger.debug(url)
        result = True
        cls.status = 200
        data = urlencode(post_data) if len(post_data) > 0 else None
        req = urllib2.Request(url, data)
        # Cookies and cloudhole info
        cls._read_cookies(url)
        logger.debug("Cookies: %s" % repr(cls._cookies))
        # open cookie jar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cls._cookies))
        # Headers
        req.add_header('User-Agent', cls.user_agent)
        req.add_header('Content-Language', language)
        req.add_header("Accept-Encoding", "gzip")
        try:
            cls._good_spider()
            # send cookies and open url
            with closing(opener.open(req)) as response:
                cls.headers = response.headers
                cls._save_cookies()
                # borrow from provider.py Steeve
                if response.headers.get("Content-Encoding", "") == "gzip":
                    import zlib
                    cls.content = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(response.read())
                else:
                    cls.content = response.read()

        except urllib2.HTTPError as e:
            result = False
            cls.status = e.code
            logger.warning("Status: " + str(cls.status))
            if e.code == 403:
                logger.warning("CloudFlared at %s" % url)

        except urllib2.URLError as e:
            result = False
            cls.status = e.reason
            logger.warning("Status: " + str(cls.status))

        except Exception as e:
            result = False
            logger.error("Error in the browser: %s" % repr(e))

        if result:
            # Save in the cache
            if use_cache:
                cache = Storage.open(cache_file, ttl=15)
                cache['uri'] = cls.content
                cache['headers'] = cls.headers
                cache.close()

            # status
            logger.debug("Status: " + str(cls.status))
            logger.debug(repr(cls.content))

        return result

    @classmethod
    def login(cls, url='', payload=None, word=''):
        """
        Login to web site
        :param url:  url address from web site
        :type url: str
        :param payload: parameters for the login request
        :type payload: dict
        :param word:  message from the web site when the login fails
        :type word: str
        :return: True if the login was successful. False, otherwise.
        """
        result = False
        if cls.open(url, post_data=payload):
            result = True
            data = cls.content
            if word in data:
                cls.status = 'Wrong Username or Password'
                result = False

        return result


def read_torrent(uri=None):
    """
    Copy a torrent file locally and returns its content
    :param uri:  Uniform Resource Identifier for the torrent un_code
    :type uri: str
    :return: Torrent file contents.
    """
    result = ''
    link = get_links(uri)
    if link.startswith('magnet'):
        link = 'http://itorrents.org/torrent/%s.torrent' % Magnet(link).info_hash

    if len(link) > 0 and Browser.open(link):
        logger.debug('opening torrent: %s' % link)
        result = Browser.content

    logger.debug('inside of the torrent: %s' % repr(result))
    return result


def get_links(uri=None):
    """
    Find the magnet information or torrent from web page
    :param uri:  Uniform Resource Identifier for the web page un_code
    :type uri: str
    :return: the torrent file URI, but not magnet.
    """

    if not uri:
        logger.debug('get link result: Nothing, empty uri')
        return ''

    url_parse = urlparse(uri)
    logger.debug('Before checking get links: %s ' % repr(url_parse))
    if MAGNETIC_SERVICE_HOST in url_parse.netloc:
        uri = unquote_plus(url_parse.query.replace('uri=', ''))
        logger.debug('Erasing 127.0.0.1: %s' % uri)

    if uri.startswith('magnet'):
        logger.debug('get link result: %s' % uri)
        return uri

    url_parse = urlparse(uri)
    base_url = '%s://%s' % (url_parse.scheme, url_parse.netloc)
    if not Browser.open(uri):
        logger.debug('get link result: Error Opening uri')
        return ''

    data = clear_string(Browser.content)
    logger.debug('Get links headers: %s' % repr(Browser.headers))
    if 'bittorrent' in Browser.headers.get('content-type', ''):
        logger.debug('get link result: Torrent=%s' % uri)
        return uri

    content = re.findall('magnet:\?[^\'"\s<>\[\]]+', data)
    if content:
        result = content[0]
        logger.debug('get link result: %s' % result)
        return result

    content = re.findall('http(.*?).torrent["\']', data)
    if content:
        result = 'http' + content[0] + '.torrent'
        result = result.replace('torcache.net', 'itorrents.org')
        logger.debug('get link result: %s' % result)
        return result

    content = re.findall('/download\?token=[A-Za-z0-9%]+', data)
    if content:
        result = base_url + content[0]
        logger.debug('get link result: %s' % result)
        return result

    content = re.findall('/telechargement/[a-z0-9-_.]+', data)  # cpasbien
    if content:
        result = base_url + content[0]
        logger.debug('get link result: %s' % result)
        return result

    content = re.findall('/torrents/download/\?id=[a-z0-9-_.]+', data)  # t411
    if content:
        result = base_url + content[0]
        logger.debug('get link result: %s' % result)
        return result

    logger.debug('get link result: No Links found')
    return ''


def get_cloudhole_key():
    """
    Get the Cloudhole Key
    https://github.com/scakemyer/cloudhole-api
    """
    cloudhole_key = None
    try:
        req = urllib2.Request("https://cloudhole.herokuapp.com/key")
        req.add_header('Content-type', 'application/json')
        with closing(urllib2.urlopen(req)) as response:
            content = response.read()

        logger.debug("CloudHole key: %s" % content)
        data = json.loads(content)
        cloudhole_key = data['key']

    except Exception as e:
        logger.debug("Getting CloudHole Key error: %s" % repr(e))

    return cloudhole_key


def get_cloudhole_clearance(cloudhole_key=None):
    """
    Define the clearance value and USER AGENT
    https://github.com/scakemyer/cloudhole-api
    :param cloudhole_key: key from cloudhole
    :type  cloudhole_key: str
    :return clearance, USER AGENT
    """
    user_agent = USER_AGENT
    clearance = None
    if cloudhole_key:
        try:
            req = urllib2.Request("https://cloudhole.herokuapp.com/clearances")
            req.add_header('Content-type', 'application/json')
            req.add_header('Authorization', cloudhole_key)
            with closing(urllib2.urlopen(req)) as response:
                content = response.read()

            logger.debug("CloudHole returned: %s" % content)
            data = json.loads(content)
            user_agent = data[0]['userAgent']
            clearance = data[0]['cookies']
            logger.debug("New UA and clearance: %s / %s" % (user_agent, clearance))

        except Exception as e:
            logger.debug("CloudHole error: %s" % repr(e))

    return clearance, user_agent


class Magnet:
    """
    Create Magnet object with its properties
    """

    def __init__(self, magnet):
        self.magnet = magnet + '&'
        # hash
        info_hash = re.search('urn:btih:(\w+)&', self.magnet, re.IGNORECASE)
        result = ''
        if info_hash is not None:
            result = info_hash.group(1)

        self.info_hash = result
        # name
        name = re.search('dn=(.*?)&', self.magnet)
        result = ''
        if name is not None:
            result = name.group(1).replace('+', ' ')

        self.name = result.title()
        # trackers
        self.trackers = re.findall('tr=(.*?)&', self.magnet)
