# -*- coding: utf-8 -*-


import re,urllib,urlparse,json,base64
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log

def resolve(url):
    #try:
        pageUrl = url
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        url = liveresolver_utils.remove_referer(url)

        result = client.request(url, referer=referer, headers= { 'Host': urlparse.urlparse(url).netloc} )
        
        file = re.findall('file=([^&]+)',result)[0]
        streamer = re.findall('streamer=([^&]+)',result)[0]
        swf = re.findall('[\"\'](.+?.swf)[\"\']',result)[0]
        url = streamer + ' playpath=' + file + ' swfUrl=' + swf + ' live=1 token=Fo5_n0w?U.rA6l3-70w47ch flashver=' + constants.flash_ver() + ' timeout=13 swfVfy=1 pageUrl=' + pageUrl
        return url
    #except:
    #    return
