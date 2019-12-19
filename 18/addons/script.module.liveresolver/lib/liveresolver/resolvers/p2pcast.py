# -*- coding: utf-8 -*-



import re,urllib,urlparse,base64,json,socket
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log 

def resolve(url):
    try:
        page = url
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer = url
        if 'streamcdn' not in url:
            page = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
            page = 'http://p2pcast.tech/stream.php?id=%s&osr=2&live=0&p2p=0&stretching=uniform' % page

        result = client.request(page, referer=referer)
        if 'streamcdn' not in url:
            token = client.request('http://p2pcast.tech/getTok.php', referer=page, headers={'User-Agent': client.agent(), 'X-Requested-With': 'XMLHttpRequest'})
        try: token = json.loads(token)['token']
        except: token = ''
        url = re.compile('murl\s*=\s*[\'|\"](.+?)[\'|\"]').findall(result)[0] 
        url = base64.b64decode(url) + token
        url += '|Referer='+page+'&User-Agent=%s&X-Requested-With=%s&Host=%s'%(client.agent(),constants.get_shockwave(),urlparse.urlparse(url).netloc)

        return url
    except:
        return


