# -*- coding: utf-8 -*-
import urllib,re
from resources.lib.libraries import client

def resolve(url):
    try:
        test = 'http://www.streamlive.to'
        html = client.request(test)
        html=html.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
        question = re.findall('<br />(.+?)<br /><br />',html)
        words = question[0].split(': ')
        try:    
            if str(len(words))=='3':
                answer = question[0].split(': ')[2]
                data_solved = urllib.urlencode({'captcha' : answer,
                                                'submit' : 'Enter'})
            else:
                pass
        except:
            raise
    except:
        pass
    try:
        try:
            html = client.request(url,data_solved)
        except:
            html = client.request(url)
        html=html.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("\/",'/')
        playpath = re.compile('file: "(.+?)\.flv"').findall(html)[0]
        token_url = re.compile('getJSON\("(.+?)"').findall(html)[0]
        rtmp=re.compile('''streamer: "([^"]+?|.+?)",''').findall(str(html))
        app=rtmp[0].split('?xs=')
        import datetime
        time_now=datetime.datetime.now()
        import time
        epoch=time.mktime(time_now.timetuple())+(time_now.microsecond/100000.)
        epoch_str = str('%f' % epoch)
        epoch_str = epoch_str.replace('.','')
        epoch_str = epoch_str[:-3]
        token_url = token_url + '&_=' + epoch_str
        token_test = client.request(token_url)
        token = re.compile('":"(.+?)"').findall(token_test)[0]
        
        url = rtmp[0]+ ' app=edge/?xs='+app[1]+' playpath='+playpath+' swfUrl=http://www.streamlive.to/ads/streamlive.swf pageUrl='+url+' token='+token
        return url
        
    except:
        return



    
    
