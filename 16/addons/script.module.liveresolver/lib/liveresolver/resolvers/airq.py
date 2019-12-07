# -*- coding: utf-8 -*-


import re
from liveresolver.modules import client,xppod

def resolve(url):
    try:
        result = client.request(url, referer=url)
        jsUrl = 'http://airq.tv' + re.findall('.*src=["\']([^"\']+).*',result)[0]
        result = client.request(url, referer=jsUrl)
        file = re.findall('.*file=([^"]+).*',result)[0]
        file = xppod.decode(file)
        url = file+'|Referer='+url+'&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        return url
    except:
        return

