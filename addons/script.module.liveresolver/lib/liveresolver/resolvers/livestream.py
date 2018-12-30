# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client

def resolve(url):
    try:
        result = client.request(url)
        m3u8_url = re.findall('.*?m3u8_url["]?\s*:\s*["]?((?:[^"]+?m3u8\?dw=1)[^"]+).*',result)[0]
        result = client.request(m3u8_url)
        m3u8 = re.findall('.*?(http[^"\']+\.m3u8[^"\'\n]*).*',result)[0]
        result = client.request(m3u8_url,output='cookie')
        cookie = urllib.quote(re.findall('hdntl=(.+?);',result)[0])
        url = m3u8 +'|Cookie=hdntl='+cookie+'&User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        return url
    except:
       return

