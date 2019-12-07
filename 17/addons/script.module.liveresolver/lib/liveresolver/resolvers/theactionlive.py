# -*- coding: utf-8 -*-


import re,urllib,urlparse
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    #try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    	except: referer = url
    	id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]

        result = client.request('http://theactionlive.com/livegamecr.js', referer=referer)
        log(result)
        url = re.findall('.*\W(\w+.php).*',result)[0]
        page='http://theactionlive.com/'+url+'?id='+id+'&width=620&height=490&stretching='
        result = client.request(page, referer=referer)
        id=re.findall(".*id=['\"]([^\"']+).*",result)[0]
        result = client.request('http://biggestplayer.me/playercr.js', referer=page)
        url = re.findall('.*\W(\w+.php).*',result)[0]
        page2='http://biggestplayer.me/'+url+'?id='+id+'&width=620&height=490'
        result = client.request(page2, referer=page)
        url=re.findall('.*(http[^"\']+\.m3u8[^"\']*).*',result)[0]
        url+='|%s' % urllib.urlencode({'Referer':page2, 'User-agent':client.agent(), 'X-Requested-With':constants.get_shockwave()})

        return url
    #except:
    #    return

