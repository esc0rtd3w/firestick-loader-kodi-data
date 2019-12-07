# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64
from liveresolver.modules import client,constants

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 
        
        result = client.request(url, referer=referer)
        streamer = re.findall("'streamer',\s*'(.+?)'\);",result)[0]
        file = re.findall("'file',\s*'(.+?)'\);",result)[0]
        token = re.findall("'token',\s*'(.+?)'\);",result)[0]
        swf = 'http://tutelehd.com/player.swf'

        url = streamer + ' playpath=' + file + ' swfUrl=' + swf + ' swfVfy=1 flashver=' + constants.flash_ver() + ' live=true token=' + token + ' pageUrl=' + url
        return url
    
    except:
        return

