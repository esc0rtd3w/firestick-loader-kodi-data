# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client


def resolve(url):
    #try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        result = client.request(url,referer=referer)
        print(result)
        return url
    #except:
     #   return


