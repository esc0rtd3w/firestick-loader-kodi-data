# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url, referer = referer)
        json_url = re.findall('.*?getJSON\([\'"]([^\'"]+)[\'"].*?',result)[0]
        result = client.request(json_url, referer = url)
        rtmp = re.findall('.*?rtmp":"([^"]+)"',result)[0]
        file = re.findall('"streamname":"([^"]+)',result)[0]
        url = rtmp + ' playpath=' + file + ' swfhash=2f17c059e0fb060411ac97d1da663ce996b5538b85a55affb7e42a3062abfba7 swfsize=224436 token=#@8x12pX@!x@# live=1 timeout=14 swfVfy=1 pageUrl=' + referer
        return url
    except:
       return

