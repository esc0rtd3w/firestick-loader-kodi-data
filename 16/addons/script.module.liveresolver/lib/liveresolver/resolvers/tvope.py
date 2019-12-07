# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client
from liveresolver.modules.log_utils import log 

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 
        
        result = client.request(url, referer=referer)
        swf = 'http://releases.flowplayer.org/flowplayer.rtmp/flowplayer.rtmp-3.2.3.swf'
        rtmp = 'rtmp://play5.tvope.com/tvope'
        file = re.findall('clip:\s*\{\s*url:\s*[\'\"](.+?)[\'\"]',result)[0]

        url = "%s playpath=%s swfUrl=%s live=1 pageUrl=%s"%(rtmp,file,swf,url)
        return url
    
    except:
        return

