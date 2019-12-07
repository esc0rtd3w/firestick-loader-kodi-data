# -*- coding: utf-8 -*-


import re,urlparse,random
from liveresolver.modules import client
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 

        result = client.request(url, referer=referer)
        server_list = re.findall(r'(\[\s*[\"\'].+?\\x.+?[^\]]+\])',result)[0]
        server_list = server_list.replace(r'\\x',r'\\u00')
        server_list = eval(u'%s'%server_list)
        server = random.choice(server_list)
        file = re.findall('file:\s*.*?[\"\']([^\"\']+).,',result)[0]

        return 'rtmp://' + server + file + ' swfUrl=http://streamp2p.com/jarani.player.swf live=1'
    except:
        return

