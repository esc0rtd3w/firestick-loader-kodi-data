# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client,liveresolver_utils,constants
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
        url = liveresolver_utils.remove_referer(url)

        result = client.request(url, referer=referer, mobile=True)
        r2 = client.request('http://cdn.mipspublisher.com:1935/loadbalancer')
        ipad = re.findall('redirect=([^$]+)',r2)[0]
        m3u8 = 'http://' + ipad + re.findall('[\"\'](:.+?m3u8[^\"\']+)',result)[0]
        m3u8 += '|%s' % urllib.urlencode({'Referer':referer,'User-agent':client.agent(),'X-Requested-With':constants.get_shockwave()})
        return m3u8 
        
    except:
        return

