# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url, referer=referer)

        f = re.compile('var f\s*=\s*(\d+);').findall(result)[0]
        a = str(int(re.compile('var a\s*=\s*(\d+);').findall(result)[0])/int(f))
        b = str(int(re.compile('var b\s*=\s*(\d+);').findall(result)[0])/int(f))
        c = str(int(re.compile('var c\s*=\s*(\d+);').findall(result)[0])/int(f))
        d = str(int(re.compile('var d\s*=\s*(\d+);').findall(result)[0])/int(f))
        v = re.compile('var v_part =\s*\'([^\']+).*').findall(result)[0]
        rtmp  = 'rtmp://' + a + '.' + b + '.' + c + '.' + d + v

        url = rtmp + ' swfUrl=http://filo.hqstream.tv/jwp6/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=http://hqstream.tv'
        return url
    except:
        return

