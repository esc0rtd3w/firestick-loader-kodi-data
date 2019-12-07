# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        result = client.request(url, referer=referer)
        info = re.findall('id=(\d+)&',result)[0]
        id=info
        m3u8 = re.findall('source.setAttribute\("src", "http://"\s*\+.+?\+\s*"(.+?)"\);',result)[0]
        domain_url = 'http://www.liveflashplayer.net:1935/loadbalancer?' + id
        result = client.request(domain_url, referer=url)

        domain = re.findall('.*redirect=([\.\d]+).*',result)[0]
        url = 'http://%s%s'%(domain,m3u8) 
        return url
    except:
       return


