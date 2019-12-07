# -*- coding: utf-8 -*-


import re,urlparse,json,time,socket,random
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        id = urlparse.parse_qs(urlparse.urlparse(url).query)['game'][0]

        ts = int(time.time())

        tk = 'http://sportstream365.com/LiveFeed/GetGame?lng=ru&id='+id+'&partner=24&_='+str(ts)

        html = client.request(tk,referer='http://www.sportstream365.com/')
        file = re.findall('.*?VI[\'"]*[:,]\s*[\'"]([^\'"]+)[\'"].*',html)[0]
        rt = _resolve('rtmpe://xlive.sportstream365.com/xlive')
        rand = str(random.randint(10000000000000000,99999999999999999))
        url = rt + ' playpath=raw:' + file + ' conn=S:client conn=S:3.1.0.10 conn=S:en live=1 timeout=15 pageUrl=http://www.sportstream365.com/ swfVfy=http://sportstream365.com/swf/VideoPlayer.swf?x=0.'+rand+' flashver=' + constants.flash_ver()
        return url
    except:
        return


def _resolve(src):
    parsed_link = urlparse.urlsplit(src)
    tmp_host = parsed_link.netloc.split(':')
    
    servers = ["93.189.57.254",
                       "93.189.62.10",
                       "185.49.70.58",
                       "46.28.205.96",
                       "178.17.168.90",
                       "185.28.190.69",
                       "85.114.135.215",
                       "94.242.254.211"]
    tmp_host[0] = random.choice(servers)
    
    tmp_host = ':'.join(tmp_host)
    parsed_link = parsed_link._replace(netloc=tmp_host)
    return parsed_link.geturl()