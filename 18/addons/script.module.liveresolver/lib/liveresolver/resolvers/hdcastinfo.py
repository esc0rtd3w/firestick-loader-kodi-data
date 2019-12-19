# -*- coding: utf-8 -*-

import re,urlparse,urllib
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log


def resolve(url):
    try:
        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace('&referer=%s'%referer,'')
            url = url.replace('?referer=%s'%referer,'')
        except: referer = url

        page = url
        result = client.request(url, referer=referer)
        result= result.replace('","','').replace('["','').replace('"]','').replace('.join("")',' ').replace(r'\/','/')

        vars = re.findall('var (.+?)\s*=\s*(.+?);',result)
        inners = re.findall('id=(.+?)>([^<]+)<',result)
        inners = dict(inners)

        js = re.findall('srcs*=s*(?:\'|\")(.+?player\.js(?:.+?|))(?:\'|\")',result)[0]
        js = client.request(js, referer=referer)
        token = re.findall('securetoken: ([^\n]+)',result)[0]
        token = re.findall('var\s+%s\s*=\s*(?:\'|\")(.+?)(?:\'|\")' % token, js)[-1]

        for i in range (100):
            for v in vars:
                result = result.replace('  + %s'%v[0],v[1])
        for x in inners.keys():
            result = result.replace('  + document.getElementById("%s").innerHTML'%x,inners[x])

        
        fs = re.findall('function (.+?)\(\)\s*\{\s*return\(([^\n]+)',result)
        url = re.findall('file:(.+?)\s*\}',result)[0]
        for f in fs:
                url = url.replace('%s()'%f[0],f[1])
        url = url.replace(');','').split(" + '/' + ")
        streamer, file = url[0].replace('rtmpe','rtmp').strip(), url[1]
        url=streamer + '/ playpath=' + file + ' swfUrl=http://www.hdcast.info/myplayer/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' live=1 timeout=20 token=' + token + ' pageUrl=' + page
        return url

    except:
        return

