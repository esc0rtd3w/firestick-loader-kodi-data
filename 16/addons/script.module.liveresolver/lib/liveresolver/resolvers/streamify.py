# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
        
        url = liveresolver_utils.remove_referer(url)
        pageUrl=url

        result = client.request(url, referer=referer)

        id,channel,pk = re.findall('id=(\d+)&s=([^&\'"]+).+?&pk=([^&\'"]+).*',result)[0]
        r2 = client.request('http://www.streamifypublisher.com:1935/loadbalancer?%s'%channel,pageUrl)
        ip = r2.split('=')[1]

        url = 'rtmp://%s/live'%ip
        url = url + ' playPath=' + channel + '?id=' + id + '&pk='+pk+' swfVfy=1 timeout=15 live=true conn=S:OK swfUrl=http://www.streamifyplayer.com/resources/scripts/eplayer.swf flashver=' + constants.flash_ver() + ' pageUrl=' + pageUrl

        return url
    
    except:
        return

