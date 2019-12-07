# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64,json
from liveresolver.modules import client,constants,liveresolver_utils,decryptionUtils
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 


        url = liveresolver_utils.remove_referer(url)

        result = client.request(url,referer=referer)
        result = decryptionUtils.doDemystify(result)
        rtmp = re.findall('.*file:"([^"]+)"',result)[0]
        token = re.findall('token:"([^"]+)"',result)[0]
        url = rtmp +' swfUrl=http://akamaistreaming.com/YjFlMTI0MT/jwplayer.flash.swf token='+token+' flashver=' + constants.flash_ver() + ' live=1 timeout=15 pageUrl=' + url
        return url 
    except:
        return

