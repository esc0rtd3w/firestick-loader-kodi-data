# -*- coding: utf-8 -*-

import re,urlparse
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]

        pageUrl = 'http://hdcast.me/embedplayer.php?width=640&height=480&id=%s&autoplay=true&strech=exactfit' % id

        result = client.request(pageUrl, referer=url)
        x = re.compile('/file\s*: \s*[\'|\"](.+?)[\'|\"]').findall(result)

        url = re.compile('file\s*: \s*[\'|\"](.+?)[\'|\"]').findall(result)
        url = [i for i in url if not i in x]
        url = [i for i in url if 'rtmp' in i or  'm3u8' in i][0]

        if url.startswith('rtmp'): url += ' live=1 timeout=15'

        
        return url
    except:
        return

