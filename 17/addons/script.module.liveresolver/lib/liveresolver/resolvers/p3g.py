# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client,constants


def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        result = client.request(url, referer=referer)
        swf = 'http://www.p3g.tv/resources/scripts/eplayer.swf'
        info = re.findall('id=(\d+)&s=([^&\'"]+).*?&pk=([^&\'"]+).*',result)[0]
        id,channel,pk = info
        rtmp_url = 'http://www.p3g.tv:1935/loadbalancer?' + id
        result = client.request(rtmp_url, referer=swf)
        rtmp = re.findall('.*redirect=([\.\d]+).*',result)[0]
        rtmp = 'rtmp://%s/live/'%rtmp
        url = rtmp + ' playPath=' + channel + '?id=' + id + '&pk='+pk+' swfVfy=1 timeout=15 conn=S:OK live=true swfUrl='+swf + ' flashver=' + constants.flash_ver() + ' pageUrl=' + url
        return url
    except:
        return


