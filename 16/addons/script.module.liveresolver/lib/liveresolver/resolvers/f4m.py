# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        url = url.replace(referer,'').replace('?referer=','')
        from f4mproxy.F4mProxy import f4mProxyHelper
        helper=f4mProxyHelper()
        url_to_play,stopEvent = helper.start_proxy(url, 'play')
        return url_to_play
    except:
        return

