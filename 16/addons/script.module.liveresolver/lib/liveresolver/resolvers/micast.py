# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,decryptionUtils

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
        url = url.replace(referer,'')
        result = client.request(url, referer=referer)
        result = decryptionUtils.doDemystify(result)
        print(result)
        rtmp = re.findall('.*["\'](rtmp[^"\']+)["\'].*',result)[0]
        
        url = rtmp + ' swfUrl=http://micast.tv/jwplayer/jwplayer.flash.swf live=true pageUrl=' + url
        return url
    except:
        return

