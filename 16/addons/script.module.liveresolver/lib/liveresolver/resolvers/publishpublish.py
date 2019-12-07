# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        result = client.request(url,referer=referer)
        url = re.compile('(?:\'|\")?file(?:\'|\")?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        url+='|%s'%urllib.urlencode({'referer':referer,'user-agent':client.agent()})
        return url
    except:
        return


