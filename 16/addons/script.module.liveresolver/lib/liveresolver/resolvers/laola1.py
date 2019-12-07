# -*- coding: utf-8 -*-


import re,urlparse,random,string
from liveresolver.modules import client,control
from liveresolver.modules.log_utils import log
def resolve(url):
    try:
        
        if 'player' not in url:
            result = client.request(url)
            rr = 'http://www.laola1.tv' + re.findall('(\/titanplayer.php\?videoid=[^\"\']+)',result)[0]
        else:
            rr = url
        result = client.request(rr)   
        streamid = re.compile('streamid: "(.+?)"', re.DOTALL).findall(result)[0]
        partnerid = re.compile('partnerid: "(.+?)"', re.DOTALL).findall(result)[0]
        portalid = re.compile('portalid: "(.+?)"', re.DOTALL).findall(result)[0]
        sprache = re.compile('sprache: "(.+?)"', re.DOTALL).findall(result)[0]
        auth = re.compile('auth = "(.+?)"', re.DOTALL).findall(result)[0]
        timestamp = ''.join(re.compile('<!--.*?([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}).*?-->', re.DOTALL).findall(result)[0])

        hdvideourl = 'http://www.laola1.tv/server/hd_video.php?play='+streamid+'&partner='+partnerid+'&portal='+portalid+'&v5ident=&lang='+sprache
        result = client.request(hdvideourl)
        url2 = re.findall('<url>([^<]+)</url>',result)[0]
        url2 = url2.replace('amp;','')
        url2 = url2 +'&timestamp='+timestamp+'&auth='+auth
        result = client.request(url2, referer = hdvideourl)
        
        url = re.findall('url\s*=\s*[\"\']([^\'\"]+)',result)[0]
        auth = re.findall('auth\s*=\s*[\"\']([^\'\"]+)',result)[0]
        status = re.findall('status\s*=\s*[\"\']([^\'\"]+)',result)[0]
        if status == '-1':
            comment = re.findall('comment\s*=\s*[\"\']([^\'\"]+)',result)[0]
            control.infoDialog(comment, heading='laola1.tv')
            return

        chars=string.ascii_uppercase
        rand =  ''.join(random.choice(chars) for x in range(12))
        url = url.replace('/z/','/i/')
        url = urlparse.urljoin(url, 'master.m3u8?hdnea=' + auth + '&g=' + rand + '&hdcore=3.8.0')
        return url
    except:
        return

