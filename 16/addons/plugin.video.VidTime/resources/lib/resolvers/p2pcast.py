# -*- coding: utf-8 -*-

import re,sys,urllib,urlparse,base64,urllib2
from resources.lib.modules import client


def TEST():
    return

def resolve(url):
    
    try:
        result = client.request(url)
        js = re.compile('src\s*=\s*[\'|\"](.+?player.+?\.js)[\'|\"]').findall(result)[-1]
        js = client.request(js)
  
        try:
            token = re.findall('[\'|\"](.+?\.php)[\'|\"]',js)[-1]
            token = urlparse.urljoin('http://p2pcast.tv', token)
            token = client.request(token, referer=url, headers={'User-Agent': client.agent(), 'X-Requested-With': 'XMLHttpRequest'})
            token = re.compile('[\'|\"]token[\'|\"]\s*:\s*[\'|\"](.+?)[\'|\"]').findall(token)[0]
        except:
            token = ''

        try:
            swf = re.compile('flashplayer\s*:\s*[\'|\"](.+?)[\'|\"]').findall(js)[-1]
        except:
            swf = 'http://cdn.p2pcast.tv/jwplayer.flash.swf'


        url = re.compile('url\s*=\s*[\'|\"](.+?)[\'|\"]').findall(result)[0]
        url = base64.b64decode(url) + token
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': swf})

        return url
   
    except:
        return
    
