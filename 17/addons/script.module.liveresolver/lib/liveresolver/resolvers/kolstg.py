# -*- coding: utf-8 -*-


import re,urllib,urlparse
from liveresolver.modules import client,liveresolver_utils
from liveresolver.modules.log_utils import log
def resolve(url):
    #try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    	except: referer = url

    	url = liveresolver_utils.remove_referer(url)
        result = client.request(url, referer=referer)
        log(result)
        
        return url
    #except:
     #   return

