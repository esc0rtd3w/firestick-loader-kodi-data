# -*- coding: utf-8 -*-


import re,urlparse,json,requests
import client
from log_utils import log
import urllib

def resolve(html,referer):
    
    try:
        
        result = html
        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]
        file = re.compile('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=WIN\\2020,0,0,286 live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+referer

        return url
    except:
        return


