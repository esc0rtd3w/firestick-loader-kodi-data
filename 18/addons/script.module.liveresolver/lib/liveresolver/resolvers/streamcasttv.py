# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url, referer = referer)
        file = re.findall("var file\d+\s*=\s*(?:\'|\")(.+?)(?:\'|\")",result)[0]
        url = file +' swfUrl=http://streamcasttv.biz/jwplayer/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl=' + url
        return url
    except:
        return

