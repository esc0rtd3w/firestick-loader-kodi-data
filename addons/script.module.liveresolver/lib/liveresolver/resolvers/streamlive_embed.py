# -*- coding: utf-8 -*-


import re,urlparse,json,requests,cookielib
from liveresolver.modules import client
from liveresolver.modules import control
from liveresolver.modules import constants,liveresolver_utils
from liveresolver.modules.log_utils import log
import urllib,sys,os


cookieFile = os.path.join(control.dataPath, 'streamliveembedcookie.lwp')

def resolve(url):
    
    try:
        jar = get_cj()
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: 
            try:
                referer = re.findall('referer=([^$&]+)',url)[0]
            except:
                referer = url

        s = requests.Session()
        s.cookies = jar
        id = re.findall('embed/(\d+)',url)[0]
        page = 'http://www.streamlive.to/embedplayer_new2.php?width=840&height=490&channel=%s&autoplay=true'%id
        
        headers = {'Host':'www.streamlive.to','Referer':referer,'Connection':'keep-alive'}
        s.headers = headers
        result = s.get(page).text
        if 'captcha' in result:
            q = re.findall('Question:([^<]+)<',result)[0]
            ans = control.get_keyboard(q)
            if ans:
                result = s.post(page,data={'captcha':ans}).text
        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        if 'http' not in token_url:
            token_url = 'http:' + token_url
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]

        file = re.compile('(?:[\"\'])?file(?:[\"\'])?\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=' + constants.flash_ver() + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page

        jar.save (cookieFile,ignore_discard=True)
        return url
    except:
        return ''

def get_cj():
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookieFile,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar


