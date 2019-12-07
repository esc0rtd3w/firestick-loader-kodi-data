# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client,constants

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
        
        page = client.request(url)
        page = re.findall('.*?src=([^"\' ]+).*',page)[0]
        page = page + id + '&vw=650&vh=500'

        result = client.request(page,referer=referer)
        url = re.findall('.*(http[^"\']+\.m3u8[^"\']*).*',result)[0]
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': page,'X-Requested-With':constants.get_shockwave()})
        
        return url
    except:
        return

