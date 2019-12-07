# -*- coding: utf-8 -*-


import re,urlparse,json,urllib
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
        host = urlparse.urlparse(url).netloc
        url = 'http://www.%s/jwplayer6.php?channel=%s&vw=700&vh=480'%(host,id)
        result = client.request(url, referer=referer)
        
        json_url = re.findall('getJSON\([\"\']([^\"\']+)',result)[0]
        j = json.loads(client.request(json_url, referer=url))
        token,file,rtmp = j['token'],j['streamname'],j['rtmp']

        ur = rtmp+'/'+file+'/chunklist.m3u8'
        ur += '|%s' %urllib.urlencode({'User-agent':client.agent(),'X-Requested-With':constants.get_shockwave(),'Referer':url,'Host':urlparse.urlparse(rtmp).netloc})
        return ur
    except:
        return

