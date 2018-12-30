# -*- coding: utf-8 -*-
################################################################################
# |                                                                            #
# |     ______________________________________________________________         #
# |     :~8a.`~888a:::::::::::::::88......88:::::::::::::::;a8~".a88::|        #
# |     ::::~8a.`~888a::::::::::::88......88::::::::::::;a8~".a888~:::|        #
# |     :::::::~8a.`~888a:::::::::88......88:::::::::;a8~".a888~::::::|        #
# |     ::::::::::~8a.`~888a::::::88......88::::::;a8~".a888~:::::::::|        #
# |     :::::::::::::~8a.`~888a:::88......88:::;a8~".a888~::::::::::::|        #
# |     ::::::::::::  :~8a.`~888a:88 .....88;a8~".a888~:::::::::::::::|        #
# |     :::::::::::::::::::~8a.`~888......88~".a888~::::::::::::::::::|        #
# |     8888888888888888888888888888......8888888888888888888888888888|        #
# |     ..............................................................|        #
# |     ..............................................................|        #
# |     8888888888888888888888888888......8888888888888888888888888888|        #
# |     ::::::::::::::::::a888~".a88......888a."~8;:::::::::::::::::::|        #
# |     :::::::::::::::a888~".a8~:88......88~888a."~8;::::::::::::::::|        #
# |     ::::::::::::a888~".a8~::::88......88:::~888a."~8;:::::::::::::|        # 
# |     :::::::::a888~".a8~:::::::88......88::::::~888a."~8;::::::::::|        #
# |     ::::::a888~".a8~::::::::::88......88:::::::::~888a."~8;:::::::|        #
# |     :::a888~".a8~:::::::::::::88......88::::::::::::~888a."~8;::::|        #
# |     a888~".a8~::::::::::::::::88......88:::::::::::::::~888a."~8;:|        #
# |                                                                            #
# |    Rebirth Addon                                                           #
# |    Copyright (C) 2017 Cypher                                               #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################

import base64
import urlparse
import urllib
import hashlib
import re

from resources.lib.modules import client
from resources.lib.modules import trakt
from resources.lib.modules import pyaes


def is_anime(content, type, type_id):
    try:
        r = trakt.getGenre(content, type, type_id)
        return 'anime' in r or 'animation' in r
    except:
        return False


def get_release_quality(release_name):
    if release_name is None: return
    try: release_name = release_name.encode('utf-8')
    except: pass

    try:
        release_name = release_name.upper()

        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', release_name)
        fmt = re.split('\.|\(|\)|\[|\]|\s|-', fmt)
        fmt = [i.lower() for i in fmt]

        if '1080p' in fmt: quality = '1080p'
        elif '720p' in fmt: quality = 'HD'
        else: quality = 'SD'
        if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

        info = []
        if '3d' in fmt or '.3D.' in release_name: info.append('3D')
        if any(i in ['hevc', 'h265', 'x265'] for i in fmt): info.append('HEVC')

        return quality, info
    except:
        return 'SD', []

def label_to_quality(label):
    try:
        try: label = int(re.search('(\d+)', label).group(1))
        except: label = 0

        if label >= 2160:
            return '4K'
        elif label >= 1440:
            return '1440p'
        elif label >= 1080:
            return '1080p'
        elif 720 <= label < 1080:
            return 'HD'
        elif label < 720:
            return 'SD'
    except:
        return 'SD'


def strip_domain(url):
    try:
        if url.lower().startswith('http') or url.startswith('/'):
            url = re.findall('(?://.+?|)(/.+)', url)[0]
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url
    except:
        return


def is_host_valid(url, domains):
    try:
        host = __top_domain(url)
        hosts = [domain.lower() for domain in domains if host and host in domain.lower()]
        if hosts and '.' not in host:
            host = hosts[0]
        if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            host = 'gvideo'
        return any(hosts), host
    except:
        return False, ''


def __top_domain(url):
    elements = urlparse.urlparse(url)
    domain = elements.netloc or elements.path
    domain = domain.split('@')[-1].split(':')[0]
    regex = "(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
    res = re.search(regex, domain)
    if res: domain = res.group(1)
    domain = domain.lower()
    return domain


def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, str):
            filter = [filter]

        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except:
        return []


def append_headers(headers):
        return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])


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