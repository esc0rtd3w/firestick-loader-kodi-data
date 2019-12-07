# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['file'][0]
        result = client.request(url, referer=referer)
        streamer = re.compile("&streamer=(.+?)&").findall(result)[-1]
        file = re.compile("file=(.+?)&").findall(result)[-1].replace('.flv','')
        url=streamer + ' playPath='+ file  + ' swfUrl=http://abcast.net/juva.swf live=1 timeout=15 swfVfy=1 pageUrl=' + url
        return url
    except:
        return

