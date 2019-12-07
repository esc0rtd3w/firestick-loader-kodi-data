# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client,constants

def resolve(url):
    try:
    	try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url, referer = referer)
        file = re.findall('.*(http[^"\']+\.m3u8[^"\']*).*',result)[0]
        url = file+'|Referer='+referer+'&User-Agent=' + client.agent() + '&X-Requested-With=' + constants.get_shockwave()
        return url
    
    except:
        return

