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

def testenabled():
    return not getmyidentity()==""

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

def getVideoPage(url,mode):
    import time
    post={'mode':str(mode),'data':url,'id':getmyidentity()}
    post = urllib.urlencode(post)
    ticketurl="aHR0cDovL3NoYW5pLm9mZnNob3JlcGFzdGViaW4uY29tL3Rlc3RyZXNvdXJjZXMvdGVzdHBhZ2VuZXcucGhwP3Q9JXM=".decode("base64")%(str(int(time.time())))
    return getUrl(ticketurl,post=post)
    
    
def getChannels(url,mode):
    url=url.decode("base64")
    ret=[]
    try:
        import json
        jsondata=json.loads(getVideoPage(url,mode))
        for channel in jsondata["data"]:
            cname=channel["cname"]
            type=channel["type"]
            if type=="folder":
                curl=channel["curl"]
            else:
                curl='testpage:'+channel["curl"]+"|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)"
            cimage=channel["cimage"]+"|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)"
            ret.append((cname ,'manual', curl ,cimage,type))  
        if len(ret)>0:
            ret=sorted(ret,key=lambda s: s[0].lower() )                        
    except:
        traceback.print_exc(file=sys.stdout)
    return ret

    
def play(name,url, mode):
    played=False
    url=url
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    played=tryplay(url,listitem)    
