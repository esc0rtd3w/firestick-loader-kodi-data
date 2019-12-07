# -*- coding: utf-8 -*-


import re,urllib,urlparse,json
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 
        url = liveresolver_utils.remove_referer(url)
        result = client.request(url, referer=referer)
        json_url = re.findall('getJSON\([\"\']([^\"\']+)',result)[0]
        j = json.loads(client.request(json_url, referer=url))
        rtmp = j['rtmp']
        file = j['streamname']
        u2 = 'http://'+rtmp+'/player.php?ch='+file
        result = client.request(u2, referer=url)
        auth = re.findall('.*?(c2V[^"\'&]+)',result)[0]
        url = 'http://'+rtmp+'/live/'+file+'.m3u8?token='+auth
        url += '|%s' %urllib.urlencode({'Referer':u2,'User-agent':client.agent(),'X-Requested-With':constants.get_shockwave()})
        return url
    except:
        return

