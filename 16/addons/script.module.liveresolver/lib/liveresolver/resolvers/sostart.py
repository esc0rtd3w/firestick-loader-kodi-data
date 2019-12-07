# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
    
        result = client.request(url, referer=referer)
        rtmp = re.findall('.*?[\'"]?file[\'"]?[:,]\s*[\'"]([^\'"]+)[\'"].*',result)[0]
        url = rtmp+' swfUrl=http://sostart.org/jw/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' token=SECURET0KEN#yw%.?()@W! live=1 timeout=14 swfVfy=1 pageUrl='+url
        return url
    except:
        return

