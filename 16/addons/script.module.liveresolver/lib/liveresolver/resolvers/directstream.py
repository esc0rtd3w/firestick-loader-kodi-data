# -*- coding: utf-8 -*-


import re,urllib,urlparse
from liveresolver.modules import client,constants

def resolve(url):
    try:
    	try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
     	except:
            referer=url
        result = client.request(url, referer = referer)
        
        pageUrl = re.findall('.*?iframe\s*src=["\']([^"\']+)["\'].*',result)[0]
        result = client.request(pageUrl, referer = referer)
        rtmp = re.findall('.*file\w+\s*[:=]\s*"([^\'",]+).*',result)[0].replace(' ','')
        url = rtmp + ' swfUrl=http://direct-stream.biz/jwplayer/jwplayer.flash.swf flashver=' + constants.flash:ver() + ' live=1 timeout=14 swfVfy=1 pageUrl=' + pageUrl
        return url
    
    except:
        return

