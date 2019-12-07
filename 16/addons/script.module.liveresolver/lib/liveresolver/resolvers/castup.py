# -*- coding: utf-8 -*-


import re,urllib,urlparse,json
from liveresolver.modules import client

def resolve(url):
    try:
        pageUrl = url
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url, referer=referer)
        json_url = re.compile('\$.getJSON\("(.+?)", function\(json\){').findall(result)[0]
        token = re.compile("\('token', '(.+?)'\);").findall(result)[0]
        data = json.loads(client.request(json_url))
        file = data['streamname']
        rtmp = data['rtmp']
        swf ='http://www.castup.tv' + re.compile('.*?SWFObject\([\'"]([^\'"]+)[\'"].*').findall(result)[0]
        url = rtmp + ' playpath=' + file + ' swfUrl=' + swf + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl=' + pageUrl
        return url
    except:
        return

