# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['channel'][0]
        token_url = 'http://www.letgo.tv/securetoken.php?id=%s'%id
        result = client.request(token_url, referer = referer)
        rtmp = re.findall('.*rtmp":"([^"]+)"',result)[0]
        file = re.findall('"streamname":"([^"]+)"',result)[0]
        token = re.findall('"token":"([^"]+).*',result)[0]
        url = rtmp + ' playpath='+file+' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf live=1 flashver=' + constants.flash_ver() + ' timeout=10 token=' + token + ' swfVfy=1 pageUrl=' + referer
        

        return url
    except:
        return

