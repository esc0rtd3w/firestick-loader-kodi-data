# -*- coding: utf-8 -*-


import re,urlparse,base64
from liveresolver.modules import client,constants

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url
            
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
        url = 'http://miplayer.net/embedplayer.php?width=640&height=480&id=%s'%id
        result = client.request(url, referer=referer)
        curl = re.compile("curl\s*=\s*\"(.+?)\"").findall(result)[0]
        curl = base64.b64decode(curl)
        
        url = curl + ' swfUrl=http://otronivel.me/jw7/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' timeout=15 live=true swfVfy=1 pageUrl=http://miplayer.net/embedplayer.php?width=640&height=480&id=%s&autoplay=true&strech=exactfit'%id
        return url
    except:
      return

