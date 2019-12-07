# -*- coding: utf-8 -*-


import re,urllib,urlparse,json
from liveresolver.modules import client, xppod
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try:
            referer  = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            
        except: referer = url
        pageUrl=url
        host  = urlparse.urlparse(url).netloc
        
        result = client.request(url, referer=referer, headers={'host':host})
        s = re.findall('name=["\']s["\'] value=["\'](.+?)["\']',result)[0]
        f = re.findall('name=["\']f["\'] value=["\'](.+?)["\']',result)[0]
        s2 = json.loads(xppod.decode_sh(s))
        key = s2['stkey']
        
        file = xppod.decode_sh(re.sub(key,'',f))
        url = file + '|%s'% (urllib.urlencode({'Referer': "http://h5.adshell.net/flash", 'User-agent':client.agent()}))
        return url
    except:
        return

