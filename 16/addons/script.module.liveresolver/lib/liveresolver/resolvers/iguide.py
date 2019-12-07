# -*- coding: utf-8 -*-


import re,urlparse,json
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    #try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        try:
            channel = urlparse.parse_qs(urlparse.urlparse(url).query)['channel'][0]
        except:
            channel = re.compile('/embed/(\d+)&').findall(url)[0]


        page = 'http://www.iguide.to/embedplayer_new.php?width=700&height=410&channel=%s&autoplay=true' % channel
        
        log(page)
        headers = {'Host':'www.iguide.to','Connection':'keep-alive'}
        result = client.request(page, referer=referer,headers = headers)
        log(result)
        token_url =re.compile('\$.getJSON\("(.+?)", function\(json\){').findall(result)[0]
        token = json.loads(client.request(token_url, referer=referer))['token']

        file = re.compile('(?:\'|\")?file(?:\'|\")?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('(?:\'|\")?streamer(?:\'|\")?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]

        url=rtmp +  ' playpath=' + file + ' swfUrl=http://www.iguide.to/player/secure_player_iguide_token.swf flashver=' + constants.flash_ver() + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page
        return url
    #except:
    #    return


