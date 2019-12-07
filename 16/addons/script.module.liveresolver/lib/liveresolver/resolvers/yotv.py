# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        page = urlparse.parse_qs(urlparse.urlparse(url).query)['live'][0]
        page = 'http://www.yotv.co/embed.php?live=%s&vw=620&vh=490' % page

        result = client.request(page, referer=referer)
        rtmp = re.compile('file\s*:\s*(?:\"|\')(.+?)(?:\"|\')').findall(result)[0]
        token = re.compile('securetoken\s*:\s*(?:\"|\')(.+?)(?:\"|\')').findall(result)[0]

        url= rtmp + ' swfUrl=http://p.jwpcdn.com/6/11/jwplayer.flash.swf live=1 token=' + token + ' timeout=14 swfVfy=1 pageUrl=' + page
        return url
    except:
        return


