# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client

def resolve(url):
    try:
        result = client.request(url, mobile=True)
        pom = re.findall('.*?url:\s[\'"](\/\/streamaccess\.unas\.tv[^\'"]+\" \+ label \+ \"[^\'"]+).*?', result)[0].replace('" + label + "','ehftv')
        result = client.request('http:' +pom, referer='http://ehftv.com/assets/swf/videoplayer_6.0.2388.swf?r=20150422', mobile=True)
        auth,url = re.findall('.*?auth="([^\'"]+)"\s*url="([^\'"]+)".*?',result)[0]
        url = url + '?hdnea='+ auth 
        return url
    except:
        return

