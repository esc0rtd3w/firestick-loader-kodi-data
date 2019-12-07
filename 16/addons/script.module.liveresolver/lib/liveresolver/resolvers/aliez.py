# -*- coding: utf-8 -*-


import re,urllib,urlparse
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
    	

        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    	except: referer = url
        url = liveresolver_utils.remove_referer(url)
        page = url
        result = client.request(url, referer=referer)
        try:
            url = urllib.unquote(re.findall('.*file["]*\s*:\s*["\']([^"\']+)',result)[0])
        except:
            id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
            url = 'http://aliez.tv/redir/c.php?i=' + id
            url2 = client.request(url,output='geturl')
            page = url2
            result = client.request(url2,referer='http://aliez.tv')
            url = urllib.unquote(re.findall('.*file["]*\s*:\s*["\']([^"\']+)',result)[0])

        url += ' live=true swfVfy=1 swfUrl=http://i.aliez.me/swf/playernew.swf flashver=%s pageUrl='%constants.flash_ver() + page
        return url
    except:
        return

