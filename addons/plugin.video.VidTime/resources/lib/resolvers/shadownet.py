# -*- coding: utf-8 -*-

import re,urlparse,urllib
from resources.lib.modules import client
from resources.lib.modules import cloudflare

def TEST():
    return

def resolve(url):
    try: 
        result = client.request(url)
        try:
            iframe = client.parseDOM(result, 'div', attrs = {'class': 'player.+?'})
            iframe = client.parseDOM(iframe, 'iframe', ret='src')[-1]
            result = client.request(iframe, referer=url)
            source = re.findall("src \: '(.+?)',",result)[0]
            result = client.request(source, referer=iframe)
            url = re.compile('(http.+?)\n').findall(result)[-1]
            url = url.encode('utf-8')
            return url
        except:
            url = re.findall('source src="(.+?)"',result)[0]
            url = url.encode('utf-8')
            return url
    except:
        return None

