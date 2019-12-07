# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
        
        result = client.request(url, referer=referer)
        file = re.compile('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')').findall(result)[-1].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\"|\')(.+?)(?:\"|\')').findall(result)[-1]
        
        url = rtmp + ' playpath=' + file + ' swfUrl=http://www.openlive.org/player.swf live=1 timeout=15 swfVfy=1 pageUrl=' + url
        return url
    except:
        return

