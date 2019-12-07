# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        page = urlparse.parse_qs(urlparse.urlparse(url).query)['live'][0]
        page = 'http://www.yocast.tv/embed.php?live=%s&vw=600&vh=450' % page

        result = client.request(page, referer=referer)

        file = re.compile('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[-1].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[-1]
        url = rtmp + ' playpath='+file+' swfUrl=http://www.yocast.tv/myplayer/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' live=1 timeout=14 swfVfy=1 pageUrl=' + page
        return url
    except:
        return


