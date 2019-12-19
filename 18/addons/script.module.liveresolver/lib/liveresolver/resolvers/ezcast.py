# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        url = url.replace(referer,'').replace('?referer=', '')
        result = client.request(url, referer = referer)
        swf='http://www.embedezcast.com' + re.compile('SWFObject\(\"(.+?)".*?').findall(result)[0]
        vars = re.compile('id=(\d+)&s=([^&\'"]+).*?&pk=([^&\'"]+).*').findall(result)[0]
        id,channel,pk=vars[0],vars[1],vars[2]
        page2='http://www.embedezcast.com:1935/loadbalancer?' + id
        result = client.request(page2, referer=referer)
        ip = re.compile(".*redirect=([\.\d]+).*").findall(result)[0]
        rtmp='rtmp://%s/live/'%ip
        url='%s playPath=%s?id=%s&pk=%s swfVfy=1 timeout=10 conn=S:OK live=true swfUrl=%s flashver=' + constants.flash_ver() + ' pageUrl=%s'%(rtmp,channel,id,pk,swf,url)
        return url
    except:
        return

