# -*- coding: utf-8 -*-


import re,urlparse,json
from liveresolver.modules import client
import urllib

def resolve(url):
    
    try:
        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace(referer,'').replace('?referer=','').replace('&referer=','')
        except: referer = url


        result = client.request(url,referer=referer)
        url = re.findall('(http://.+?\.m3u8)',result)[0]
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': referer})
        return url
    except:
        return


