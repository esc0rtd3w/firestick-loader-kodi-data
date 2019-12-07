# -*- coding: utf-8 -*-


import re,urlparse,urllib
from liveresolver.modules import client,decryptionUtils,constants,jsunpack
from liveresolver.modules.log_utils import log


def resolve(url):
    #try:

        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        headers = { 'Referer': referer,
                                 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                 'Content-Type' :'application/x-www-form-urlencoded',
                                 'Connection' : 'keep-alive',
                                 'Host' : 'www.zoomtv.me',
                                 'Origin' : urlparse.urlparse(referer).netloc,
                                 'User-Agent' : client.agent()
                                 }
        fid = urlparse.parse_qs(urlparse.urlparse(url).query)['v'][0]
        pid = urlparse.parse_qs(urlparse.urlparse(url).query)['pid'][0]
        url = 'http://www.zoomtv.me/embed.php?v=%s&vw=650&vh=450'%fid
        pageUrl = url
        
        
        #get desktop stream
        #headers.update({ 'User-Agent' : 'Apple-iPhone/701.341' })
        post_data = urllib.urlencode({'uagent':'Apple-iPhone/701.341', 'pid':pid})
        result = req(url,post_data,headers)
        log(result)
        
        rtmp = re.findall('.*[^\w](\w+)\s*=.{0,20}(rtmp[^\']*).*(?:streamer.{0,20}\1).*',result)[0]
        
    
        #for HQ links(no rtmp)
        if rtmp is None:
            return streamer + '|%s' % urllib.urlencode({'user-agent':client.agent(),'Referer':referer})

        url = rtmp + ' playpath=' + file + ' swfUrl=http://static.zoomtv.me/player/jwplayer.6.7.4.swf flashver=' +constants.flash_ver() + ' conn=S:' + file + ' conn=S:'+ts+' conn=S:'+sg+' conn=S:'+auth+' live=1 timeout=15 token=H69d331eccdf347b swfVfy=1 pageUrl=' + pageUrl

        return url
    #except:
    #    return
#http://184.75.223.114:1935/zmtvliveme/UoJGbMgQme/playlist.m3u8?file=UoJGbMgQme&ts=1460893820&sg=2d5fe25dd51f705df999017031e952b5&auth=V&gt;JWhui^@2ESdu0?}&gt;AN
def req(url,post_data,headers):
    result = client.request(url, post=post_data,headers = headers)
    #result = decryptionUtils.doDemystify(result)
    #var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
    #vars = dict(var)
    #result = re.sub('var.+?=.+?;','',result)
    #for v in vars.keys():
    #    result = result.replace(v,vars[v])
    return result