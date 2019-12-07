import socket
from urllib2 import urlopen, URLError, HTTPError
import urllib2, re,os,base64,ua
import ftplib
import time 
import datetime
import random


def getIdByUrl(url):
    try :
        _regex_getM3u = re.compile("http://(.*?)/flv/(.*?)/1.flv", re.DOTALL)
        streamId = _regex_getM3u.search(url).group(2)
        return streamId
    except :
        return url


def OPEN_URL2(page, referer=None, ua=None):
    url = page                                                           
    try:                                                                 
        req = urllib2.Request(url ,None)                                                                          
        if(referer is not None):                                                                                  
            req.add_header('Referer', referer)                                                                    
                                                                                                                  
        if(ua is not None):                                                                                       
            req.add_header('User-Agent', ua)                                                                      
                                                                                                                  
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')               
        req.add_header('Accept-Language', 'nl,en-US;q=0.7,en;q=0.3')                                              
        req.add_header('Accept-Encoding', 'deflate')                                                        
        req.add_header('Connection', 'keep-alive')                                                                
        response = urllib2.urlopen(req)                                            
        data = response.read()                                                                                    
        response.close()                                                                                          
        if(ua is None) :                                                                                          
            print(data)                                                                            
        return str(data)                                                                           
    except :                                                                                       
        return ''                                                                                  
        print('We failed to open '+url)

def getPage(page, referer=None, ua=None):                                
    url = page                                                           
    try:                                                                 
        req = urllib2.Request(url ,None)                                                                          
        if(referer is not None):                                                                                  
            req.add_header('Referer', referer)                                                                    
                                                                                                                  
        if(ua is not None):                                                                                       
            req.add_header('User-Agent', ua)                                                                      
                                                                                                                  
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')               
        req.add_header('Accept-Language', 'nl,en-US;q=0.7,en;q=0.3')                                              
        req.add_header('Accept-Encoding', 'deflate')                                                        
        req.add_header('Connection', 'keep-alive')                                                                
        response = urllib2.urlopen(req)                                            
        data = response.read()                                                                                    
        response.close()                                                                                          
        if(ua is None) :                                                                                          
            print(data)                                                                            
        return str(data)                                                                           
    except :                                                                                       
        return ''                                                                                  
        print('We failed to open '+url)

def getBaseEncodedString(streamPage):
    try:
        _regex_encodedstring = re.compile("file\s*\:\s*window\.atob\(\'(.*?)\'\)" , re.DOTALL)
        baseEncoded = _regex_encodedstring.search(streamPage).group(1)
        return baseEncoded
    except:
        return ''

def getStreamUrl(baseEncoded):
    return base64.b64decode(baseEncoded)

def getUserAgent():
    return getUa()

def getUa():
    foo = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0", "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0", "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0", "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0", "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1", "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0", "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0", "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0", "Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0", "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0", "Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1", "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1", "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1", "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1", "Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:15.0) Gecko/20121011 Firefox/15.0.1"]
    return(random.choice(foo))

def getResponse(url):
    try:
        response = urllib2.urlopen(url, timeout=10)
        if response and response.getcode() == 200:
            return response
        else :
            return False
    except:
        return False

def VeetleId(streamUrl):
    veetleId = getIdByUrl(streamUrl)
    veetleUrl = 'plugin://plugin.video.veetle/?channel='+veetleId
    return veetleUrl

