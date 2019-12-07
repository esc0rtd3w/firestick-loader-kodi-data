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

def getUserAgent():
#    ua="Mozilla/5.0 (Linux; Android 5.1; en-US; Nexus 6 Build/LMY47Z) "+("MX Player/%s.%s.%s"%(binascii.b2a_hex(os.urandom(2))[:2],binascii.b2a_hex(os.urandom(2))[:2],binascii.b2a_hex(os.urandom(2))[:3]))
    ua="EMVideoView 2.5.6 (25600) / Android 4.4.4 / GT-I9300"
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
    
def play(listitem, item):
    played=False
    print 'i n pl;ay'
    try:
        try:
            print 'enc Item',item
            url=item["msg"]["channel"]["http_stream"]
            print 'encurl',url
            if not url.startswith('http'):
                import pyaes

                key="ZGlmajM4OXJqZjgzZmY5MA==".decode("base64")
                iv="Z3IwNGpoc2Y0Nzg5MCQ5Mw==".decode("base64")
                print 'trying to decode'
                decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
                url= decryptor.decrypt(url.decode("hex")).split('\0')[0]
                print repr(url)
            if '|' in url:# and 1==2:
                url=url#.split('|')[0]+"|User-Agent=UKTVNOW_PLAYER_1.2&Referer=www.uktvnow.net"
            elif url.startswith('http') :
                url=url.split('|')[0]+"|User-Agent=%s"%getUserAgent()

            if url.startswith('rtmp'):
                url+=' timeout=10'
            print 'first',url
            played=tryplay(url,listitem)
            
        except: 
            print 'err in play'
            traceback.print_exc(file=sys.stdout)
        if played: return True
        #print "playing stream name: " + str(name) 
        #xbmc.Player(  ).play( urlToPlay, listitem)    
        url=item["msg"]["channel"]["rtmp_stream"]
        import pyaes
        key="ZGlmajM4OXJqZjgzZmY5MA==".decode("base64")
        iv="Z3IwNGpoc2Y0Nzg5MCQ5Mw==".decode("base64")
        decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv)
        url= decryptor.decrypt(url.decode("hex")).split('\0')[0]
        print repr(url)
        url=url.replace(' ','')
        if '|' not in url and url.startswith('http'):
            url=url+"|User-Agent=%s"%getUserAgent()
        if url.startswith('rtmp'):
            url+=' timeout=10'
        if not played:
            played=tryplay(url,listitem)
    except: pass
    return played
        
        
