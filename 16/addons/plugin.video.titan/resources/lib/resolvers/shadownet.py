# -*- coding: utf-8 -*-


import re,urlparse,urllib
from resources.lib.libraries import client



def resolve(url):
    try:
        
        result = client.request(url)
        print result
        iframe = client.parseDOM(result, 'div', attrs = {'class': 'player.+?'})
        iframe = client.parseDOM(iframe, 'iframe', ret='src')[-1]
        result = client.request(iframe, referer=url)
        source = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[-1]
        result = client.request(source, referer=iframe)
        url = re.compile('(http.+?)\n').findall(result)[-1]
        #url = urllib.unquote_plus(url)
        print url

        return url
    except:
        return

