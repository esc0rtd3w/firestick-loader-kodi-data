# -*- coding: utf-8 -*-

import re,urlparse,urllib
from liveresolver.modules import client
from liveresolver.modules.log_utils import log



def resolve(url):
    #try:
        id = re.findall('streamup.com/([^$/]+)',url)[0]
        playUrl = 'https://streamup.com/%s/embeds/video?startMuted=true'%id

        url = 'https://api.streamup.com/v1/channels/' + id
        result = client.request(url, referer=playUrl)
        slug = re.findall('.*?["\']slug["\']\s*:\s*["\']([^"\']+)["\'].*',result)[0]

        url2 = 'https://lancer.streamup.com/api/channels/%s/playlists'%slug
        result = client.request(url2, referer=playUrl)
        url = re.findall('.*(http[^"\']+\.m3u8[^"\']*).*',result)[0]
        url+='|%s' %urllib.urlencode({'Referer':playUrl,'User-agent':client.agent()})
        return url

       
    #except:
    #   return


