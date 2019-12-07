# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        url = liveresolver_utils.remove_referer(url)

        result = client.request(url, referer = referer)
        streamer = re.findall("'streamer',\s*'(.+?)'\);",result)[0]
        file = re.findall("'file',\s*'(.+?)'\);",result)[0]

        token = re.findall("'token',\s*'(.+?)'\);",result)[0]
        url = streamer +' playpath='+ file + ' swfUrl=http://www.castfree.me/player.swf flashver=' + constants.flash_ver() + ' token='+ token.decode('ascii','ignore') +' live=1 timeout=14 swfVfy=1 pageUrl=' + url
        return url
    except:
        return

