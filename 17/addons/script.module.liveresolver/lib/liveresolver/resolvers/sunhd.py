# -*- coding: utf-8 -*-


import re,urlparse,json
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

       

        result = client.request(url, referer=referer)
        src = re.compile('.*?src=(?:\'|\")([^\'"><]+)(?:\'|\").*').findall(result)[0]
        result = client.request(src, referer=referer)
        token = re.findall('securetoken\s*:\s*(.+?)\n',result)[0]
        surl = re.findall("var sUrl\s*=\s*'(.+?)';")
        cod1 = re.findall("var cod1\s*=\s*'(.+?)';")
        url = surl+'/' +cod1
        result = client.request(url, referer=referer)
        return url
    except:
        return


