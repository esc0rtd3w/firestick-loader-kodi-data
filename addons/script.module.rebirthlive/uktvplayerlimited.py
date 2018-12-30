import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re  
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii,sys
import CustomPlayer,uuid
from time import time
import base64

addon_id = 'script.module.rebirthlive'
selfAddon = xbmcaddon.Addon(id=addon_id)
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.37_'+xbmc.getInfoLabel('Container.PluginName'))
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

def getUserAgent():
#    ua="Mozilla/5.0 (Linux; Android 5.1; en-US; Nexus 6 Build/LMY47Z) "+("MX Player/%s.%s.%s"%(binascii.b2a_hex(os.urandom(2))[:2],binascii.b2a_hex(os.urandom(2))[:2],binascii.b2a_hex(os.urandom(2))[:3]))
    ua="EMVideoView 2.5.6 (25600) / Android 4.4.4 / GT-I9300S1"
    import random
    
    return ua#''.join(random.sample(set(ua.split(' ')), 3))

def tryplay(url,listitem):    
    import  CustomPlayer,time

    player = CustomPlayer.MyXBMCPlayer()
    start = time.time() 
    #xbmc.Player().play( liveLink,listitem)
    player.play( url, listitem)
    xbmc.sleep(1000)
    while player.is_active:
        xbmc.sleep(200)
        if player.urlplayed:
            print 'yes played'
            return True
        xbmc.sleep(1000)
    print 'not played',url
    return False

def getmyidentity():
    try:
        profile = xbmc.translatePath(selfAddon.getAddonInfo('profile').decode('utf-8'))
        source_file = os.path.join(profile, 'keyfile.txt')
        return open(source_file,"r").read()
    except: pass
    return ""
    
def play(listitem, item):
    played=False
    print 'i n pl;ay'
 
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('Zem', 'Trying to get the ticket')
    pDialog.update(30, 'reading the page')
    import time
    try:
        try:
            print 'enc Item',item
            url=item["msg"]["channel"]["http_stream"]

            if not url.startswith('http'):
                import pyaes
                post={'type':'getticket','ticket':selfAddon.getSetting( "uktvticket"),'id':getmyidentity()}
                post = urllib.urlencode(post)
                ticketurl="aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL1VLVFYucGhwP3Q9JXM=".decode("base64")%(str(int(time.time())))
                ticket=getUrl(ticketurl,post=post)
                print ticket
                if ticket.startswith('TKT_'):
                    pDialog.update(60, 'got the ticket!!')
                    selfAddon.setSetting( "uktvticket" ,ticket);
                    if selfAddon.getSetting( "uktvticket")=="": return False #addon setting curropted?
                    post={'type':'getUrl','ticket':selfAddon.getSetting( "uktvticket"),'url':url}
                    post = urllib.urlencode(post)
                    decurl="aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL1VLVFYucGhwP3Q9JXM=".decode("base64")%str(int(time.time()))
                    url=getUrl(decurl,post=post)
                    key="Nzc1ODI5NDkxMzg1MTcwNzA2ODI0MDgyMTQwOTcyMDk=".decode("base64")
                    iv="ODg3NzExMzUzOTc5MzM1MQ==".decode("base64")
                    print 'trying to decode',url
                    decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
                    url= decryptor.decrypt(url.decode("base64")).split('\0')[0]
                    print repr(url)
                    
                else:
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('XBMC', 'Error while generating ticket\r\n'+ticket)           
                    return False
                    
            #if '|' in url:# and 1==2:
            #    url=url#.split('|')[0]+"|User-Agent=UKTVNOW_PLAYER_1.2&Referer=www.uktvnow.net"
            #elif url.startswith('http') :
            #    url=url.split('|')[0]+"|User-Agent=%s"%getUserAgent()

            #if url.startswith('rtmp'):
            #    url+=' timeout=10'
            #print 'first',url
            pDialog.close()
            played=tryplay(url,listitem)
            
        except: 
            print 'err in play'
            traceback.print_exc(file=sys.stdout)
        #if played: return True
        ##print "playing stream name: " + str(name) 
        ##xbmc.Player(  ).play( urlToPlay, listitem)    
        #url=item["msg"]["channel"]["rtmp_stream"]
        #import pyaes
        #key="ZGlmajM4OXJqZjgzZmY5MA==".decode("base64")
        #iv="Z3IwNGpoc2Y0Nzg5MCQ5Mw==".decode("base64")
        #decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
        #url= decryptor.decrypt(url.decode("hex")).split('\0')[0]
        #print repr(url)
        #url=url.replace(' ','')
        #if '|' not in url and url.startswith('http'):
        #    url=url+"|User-Agent=%s"%getUserAgent()
        #if url.startswith('rtmp'):
        #    url+=' timeout=10'
        #if not played:
        #    played=tryplay(url,listitem)
    except: pass
    return played
        
        
