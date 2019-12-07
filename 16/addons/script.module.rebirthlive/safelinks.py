import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re

import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
import CustomPlayer,uuid, os,sys
import checkbad
from time import time
import base64

    
try:
    from lxmlERRRORRRR import etree
    print("running with lxml.etree")
except ImportError:
    try:
        import xml.etree.ElementTree as etree
        print("running with ElementTree on Python 2.5+")
    except ImportError:
        try:
        # normal cElementTree install
            import cElementTree as etree
            print("running with cElementTree")
        except ImportError:
            try:
            # normal ElementTree install
                import elementtree.ElementTree as etree
                print("running with ElementTree")
            except ImportError:
                print("Failed to import ElementTree from any known place")
          
try:
    import json
except:
    import simplejson as json
    
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'script.module.rebirthlive'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;

def Colored(text = '', colorid = '', isBold = False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid
        
    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'	
    
def getSafeChannels(url):
    import time 
    tt=int(time.time())
    url=url.decode("base64")
    
    cname,curl=url.split(',')
    headers=[('Referer',base64.b64decode("aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20vb25saW5ldHYuaHRtbA==")),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),('X-Requested-With','XMLHttpRequest')]               
    jsondata=getUrl(base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20vcGhwL2dldFByb2dGb3JMYW5ndWFnZS5waHA/dmFyTmFtZT1hbGxDaGFubmVsc0FsbENhdHMmbm9BZGQ9ZmFsc2UmYnJvd3Nlckxhbmc9JXMmZGlzcGxheUxhbmc9ZW4mdXNlckNvdW50cnk9VW5pdGVkJSUyMEtpbmdkb20mc3JjPWFsbCZkdHA9JXM=')%(curl,tt),headers=headers)
    #print jsondata
    jsondata=re.findall('=(\[.*\])',jsondata)[0]
    
    #print jsondata
    jsondata=json.loads(jsondata)
    ret=[]
    for cc in jsondata:
        try:
            cc=json.loads(cc)
            mm=11
            col='ZM'
            #print 'xxxxxxxxxxx'
            ##print cc
            if 'name' in cc:
                #print 'in name'
                cname,logo,cid=cc["name"].encode("utf-8"),cc["logo"],cc["cId"]
            else:
                mm=0
                col='red'
                if 'seperatorText' in cc:
                    cname,logo,cid=cc["seperatorText"],'',''
                else:
                    continue
            if not logo.startswith('http'):
                logo= base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20v')+logo
            ret.append((Colored(cname.capitalize(),col) ,base64.b64encode('safe:'+cid) ,mm ,logo))
        except: 
            traceback.print_exc(file=sys.stdout)
    return ret
def f4mcallback(param, type, error, Cookie_Jar, url, headers):
  if type==1:
    newlink,ws=createSafeLink(param)  
    #newurl=getUrl(param,Cookie_Jar)
    #oldservername=url.split('/')[2]
    #newserver=newurl.split('/')
    #newserver[2]=oldservername
    #newurl='/'.join(newserver)
    return newlink,Cookie_Jar
  else:
    return '',None
    
  return 
  
  
def getSafeLink(url, recursive=False, usecode=None, progress=None, name=""):
    newlink,ws=createSafeLink(url,progress=progress)
    #referer=''
    #callbackfunction=os.path.realpath(__file__)
    #callbackparam=url
    #newlink=urllib.quote_plus (newlink + '|Referer=' + referer+'&User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36') +'&callbackpath='+urllib.quote_plus(callbackfunction)+'&callbackparam='+urllib.quote_plus(callbackparam)
    #newlink='plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&url='+newlink+'&name='+name
    return newlink+'|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',ws
    
    
def createSafeLink(url, recursive=False, usecode=None, progress=None):
    import websocket
    ws = websocket.WebSocket()
    #wsfirst = websocket.WebSocket()
    import datetime
    try:
        useragent=''
        sess=getUrl('http://shani.offshorepastebin.com/safesession.php?t='+datetime.datetime.today().strftime('%Y-%m-%d'))
        ss=re.findall(base64.b64decode('PT5ccyooLio/KTsuKj9jdXN0b21lclwuc2FmZXJzdXJmXC5jb20='),sess)[0]
        print ss
        headers = [('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'),
           ('Accept', 'text/html, */*; q=0.01'),
           ('Accept-Language', 'en-US,en;q=0.5'),
           ('X-Requested-With', 'XMLHttpRequest'),
           ('Accept-Encoding', 'gzip, deflate'),    
           ('Cookie', ss),               
           ('Referer', base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20vb25saW5ldHYuaHRtbA=='))]
        import time
        od= base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20v')
        mainhtml=getUrl(od,headers=headers)
        
        js=urllib.unquote(re.findall("StartScriptSpeedTest\(unescape\('(.*?)'",mainhtml)[0])
        speedhtml= urllib.unquote(re.findall("phpUrl = unescape\('(.*?)'",mainhtml)[0])
        
        servername,portnum=re.findall("\n\s*?\{.*?url\s*?\:\s*?['\"]([^'\"]+?)['\"].*?port\s*?\:\s*?([0-9]+)\s*?\}",mainhtml.split('man.AddServers')[1].split(']);')[0])[0]
        print servername,portnum
        portnum=portnum.strip()
        if not js.startswith('http'):
            js=od+js
        #header=[base64.b64decode("T3JpZ2luOiBodHRwOi8vY3VzdG9tZXIuc2FmZXJzdXJmLmNvbQ=="),"User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"]
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'Origin': base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20='),
      'Accept-Encoding': 'gzip, deflate',              
      'Sec-WebSocket-Version': '13',
      'Sec-WebSocket-Extensions': 'permessage-deflate'}
        #wsfirst.connect(base64.b64decode("d3M6Ly81Mi40OC44Ni4xMzU6MTMzOC90Yi9tM3U4L21hc3Rlci9zaXRlaWQvY3VzdG9tZXIub25saW5ldHYudjM="),header=header)
        #wsfirst.recv() 
        #ws.connect(base64.b64decode("d3M6Ly8lczolcy90Yi9tM3U4L21hc3Rlci9zaXRlaWQvY3VzdG9tZXIub25saW5ldHYudjM=")%(servername,portnum),header=header)
        ws.connect(base64.b64decode("d3M6Ly8lczolcy90Yi9tM3U4L21hc3Rlci9zaXRlaWQvY3VzdG9tZXIub25saW5ldHYudjM=")%(servername,portnum),header=header)
        result = ws.recv() 
        print 'result',result
        #headers = [('Referer', base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20=')),('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),('Origin',base64.b64decode('WC1SZXF1ZXN0ZWQtV2l0aDogWE1MSHR0cFJlcXVlc3Q=')),('Cookie','jwplayer.captionLabel=Off'),
        #    ('Accept-Encoding','gzip, deflate, sdch'),('Accept-Language','en-US,en;q=0.8')]

        import time
        print 'js',js
        st= time.time()
        getUrl(js+'?dt='+ str(int(time.time()*1000)),headers=headers)
        totaltime=time.time()- st
        print totaltime
        testsize,kbps, kbRes, res =safeFinishedTest(totaltime)
        bpsurl=base64.b64decode("JXM/ZHRwPQ==")%speedhtml+ str(int(time.time()*1000))
        bpsdata=getUrl( bpsurl,headers=headers)
        bpsres, bpstime,user=re.findall("'bpsResultDiv'>(.*?)<.*?bpsTimeResultDiv'>(.*?)<.*?user'>(.*?)<",bpsdata)[0]
        lastval=selfAddon.getSetting( "safeplaylastcode" ) 
        if lastval=="": lastval=bpsres
        selfAddon.setSetting( "safeplaylastcode",bpsres)
        #bpsres,bpstime="", ""#lastval
        #if usecode: bpsres=usecode
        
        jsdata='[{"key":"type","value":"info"},{"key":"info","value":"speedtest"},{"key":"country","value":"France"},{"key":"language","value":"en"},{"key":"speedTestSize","value": "%s"},{"key":"kbPs","value":"%s"},{"key":"speedResKb","value":"%s"},{"key":"bpsResult","value":"%s"},{"key":"speedResTime","value":"%s"},{"key":"websocketSupport","value":"true"},{"key":"speedTestInTime","value":"true"},{"key":"bpsTimeResult","value":"%s"},{"key":"flash","value":"true"},{"key":"touchScreen","value":"false"},{"key":"rotationSupport","value":"false"},{"key":"pixelRatio","value":"1"},{"key":"width","value":"1366"},{"key":"height","value":"768"},{"key":"user","value":"%s"},{"key":"mobilePercent","value":"33"}]'%( testsize,str(kbps),kbRes , bpsres, res, bpstime,user)
        ws.send(jsdata)
        
        #result = ws.recv()   
        #xbmc.sleep(2000)
#        jsdata='[{"key":"type","value":"channelrequest"},{"key":"dbid","value":"%s"},{"key":"tbid","value":""},{"key":"format","value":"masterm3u8"},{"key":"proxify","value":"true"},{"key":"bitrate","value":"1368000"},{"key":"maxbitrate","value":"3305000"}]'%url
        jsdata='[{"key":"type","value":"channelrequest"},{"key":"dbid","value":"%s"},{"key":"tbid","value":""},{"key":"format","value":"masterm3u8"},{"key":"proxify","value":"true"},{"key":"bitrate","value":"1368000"},{"key":"maxbitrate","value":"3305000"}]'%url
        ws.send(jsdata)
        result = ws.recv()
        #result = ws.recv()
        print repr(result)

        headers = [('Referer', base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20vb25saW5ldHYuaHRtbA==')),('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'),('Origin',base64.b64decode('aHR0cDovL2N1c3RvbWVyLnNhZmVyc3VyZi5jb20='))]
        urlnew=re.findall('[\'"](http.*?)[\'"]',result)[0]
        result=getUrl(urlnew,headers=headers)
    except: 
        traceback.print_exc(file=sys.stdout)

    #try:
    #    print ws.close()
    #    #wsfirst.close()
    #except: 
    #    traceback.print_exc(file=sys.stdout)
    urlToPlay=re.findall('(http.*?)\s',result)[-1]
    try:
        result2=getUrl(urlToPlay,headers=headers)
        return urlnew, ws
    except:
        traceback.print_exc(file=sys.stdout)
    
    
    
def safeFinishedTest(dur):
    import math
    res = "";
    kbMulti = 1
    if (dur > 5): #// 43 kb/s
        res = "GPRS"; 
    elif (dur > 2):# // 47 kb/s | onlinedemo : ~2.3s
        res = "2G"; 
        kbMulti = 2.6;
    elif (dur > 1.3):# // 89 kb/s | onlinedemo : ~1.3s
        res = "2G"; 
        kbMulti = 2.8;
    elif (dur > 0.7):# // 153 kb/s | onlinedemo : ~0.8s
        res = "3G"; 
        kbMulti = 3;
    elif (dur > 0.4):# // 358 kb/s | onlinedemo : ~0.45s
        res = "3G";
        kbMulti = 3;
    elif (dur > 0.3):# // 358 kb/s | onlinedemo : ~0.35s
        res = "DSL";
        kbMulti = 3.3;
    else:
        res = "4G"; 
        kbMulti = 4;
    kbps = (210 / dur) * 1.024 * kbMulti
    kbps = round(kbps * 100) / 100
    kbRes = "";
    if (kbps > 1500.0):
        kbRes = "4G";
    elif (kbps > 600.0):
        kbRes = "DSL";
    elif (kbps > 300.0):
        kbRes = "3G";
    elif (kbps > 100.0):
        kbRes = "2G";
    else:
        kbRes = "GPRS";
    
                
    return "210",kbps, kbRes, res
     
