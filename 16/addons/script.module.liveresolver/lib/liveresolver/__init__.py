# -*- coding: utf-8 -*-
import re
from modules import client,webutils,cloudflare,decryptionUtils,cache,liveresolver_utils,convert
from modules.constants import resolver_dict
from modules.log_utils import log
from modules.liveresolver_utils import *
import urlparse,urllib,base64
from BeautifulSoup import BeautifulSoup as bs

global limit
limit=0

from modules import constants
FLASH = constants.flash_ver()

'''
    Pass any url containing video to this function.
    It will try to find the embedded video and resolve it, returning the resolved 
    and playable video link.

    cache_timeout (in hours) - how long to cache the found stream link for the given page.
    html - pass html content to resolver and it will search for embedded links from it, instead 
    of requesting the given url and searching from there.
'''
def resolve(url, cache_timeout=3, html=None, title='Video',icon='x'):
    try:
        log("Resolver called with url: " + url)
        resolved=None
        if html==None:
            resolved=resolve_it(url,title=title)
        if resolved==None:
            if html==None and cache_timeout!=0:
                #semi-cached resolving
                url=cache.get(find_link,cache_timeout,url)
            else:
                url = find_link(url,html=html)
            resolved=url
            url=resolve_it(url,title=title,icon=icon)
            if url!=None:
                resolved=url
        log("Resolved url: " + resolved)
        return resolved
    except:
        log("Failed to find link.")

        return url


'''
    Check if your video link is resolvable through the liveresolver module.
'''
def isValid(url):
    return prepare(urlparse.urlparse(url).netloc) in resolver_dict.keys()
   


'''
    Flush the liveresolver cache.
'''
def delete_cache():
    cache.clear()



'''
    Not intended for external use.
    This method is used internally for resolving the found link.
'''
def resolve_it(url, title='Video',icon='x'):
    if '.m3u8' in url or 'rtmp:' in url or '.flv' in url or '.mp4' in url or '.ts' in url or url.startswith('plugin://'):
        if '.m3u8' in url and '|' not in url:
            url += '|%s' % urllib.urlencode({'User-Agent': client.agent()})
        if '.ts' in url:
            url = 'plugin://plugin.video.f4mTester/?name=%s&iconImage=%s&streamtype=TSDOWNLOADER&url='%(urllib.quote(title),urllib.quote(icon)) + urllib.quote(url)
        return url

    if '.f4m' in url:
        from resolvers import f4m
        resolved = f4m.resolve(url)
        return resolved

    if url.startswith('acestream://') or url.startswith('sop://') or '.acelive' in url:
        from resolvers import sop_ace
        resolved = sop_ace.resolve(url, title)
        return resolved
    netloc = prepare(urlparse.urlparse(url).netloc)
    if netloc in resolver_dict.keys():
        resolver = resolver_dict[netloc]
        log("Calling resolver: " + resolver)
        exec "from resolvers import %s"%resolver
        resolved = eval(resolver+".resolve(url)")
        return resolved

    else:
       return 






def find_link(url, html=''):
    log('Finding in : %s'%url)
    try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
    except: referer = 'http://' + urlparse.urlparse(url).netloc
    url = manual_url_fix(url)
    host  = urlparse.urlparse(url).netloc
    headers = {'Referer':referer, 'Host':host, 'User-Agent' : client.agent(), 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language' : 'en-US,en;q=0.5'}
    
    if html=='' or html is None:

        html = client.request(url, headers=headers)
        ws = ['livetvcdn','shadow','blog']
        if any(w in url for w in ws) and 'goto/' not in url :
            
            import requests
            s = requests.Session()
            s.headers = headers
            r = s.get(url)
            html = r.text

    
    ref=url
    fs=list(globals().copy())
    for f in fs:
        if 'finder' in f:
            resolved = eval (f+"(html,ref)")
            if resolved:
                log('Resolved with %s: %s'%(f,resolved))
                return resolved
                break
    return


#embeded iframes
def finder1(html,url):
    html = html.replace('/adplus/adplus.html?id=','')
    try:html = urllib.unquote(html)
    except:pass
    global limit
    limit+=1
    ref=url
    try:
        urls = re.findall('<i?frame\s*.+?src=(?:\'|\")(.+?)(?:\'|\")',html,flags=re.IGNORECASE)
        urly = client.parseDOM(html, "iframe", ret="src")
        urlc = re.findall('top.location.href\s*=\s*[\'\"](.+?axe-tv[^\'\"]+)[\'\"]',html)
        for url in urlc:
            if 'sky-sports-1' not in url and 'fox1ushd' not in url:
                urls.append(url)
        urls += urly
        try:
            urls.append(re.findall("playStream\('iframe', '(.+?)'\)",html)[0])
        except: pass

        urls += re.findall('<a.+?href=[\'\"](/live-.+?stream.+?)[\'\"]',html)
        urls += re.findall('(http://www.hdmyt.info/(?:channel|player).php\?file=[^"\']+)["\']',html)
        
        from random import shuffle
        for url in urls:
            url = url.replace('https','http')
            if 'c4.zedo' in url or 'ProtectFile.File' in url or 'adServe' in url or 'facebook' in url or 'banner' in url:
                continue

            elif "micast" in url or 'turbocast' in url:
                return finder47(html,ref)
                
            elif 'lshstream' in url:
                return finder2(url,url)    

            rr = resolve_it(url)
            if rr:
                return rr
            uri = manual_fix(url,ref)
            if limit>=25:
                log("Exiting - iframe visit limit reached")
                return
            resolved = find_link(uri) 
            if resolved:
                break
        headers = {'User-Agent': client.agent(), 'Referer': ref}
        if '.m3u8' in resolved and '|' not in resolved:
            headers.update({'X-Requested-With':constants.get_shockwave(), 'Host':urlparse.urlparse(resolved).netloc, 'Connection':'keep-alive'})
            resolved += '|%s' % urllib.urlencode(headers)
        return resolved
    except:
        return



#lsh stream
def finder2(html,url):
    try:
        reg = re.compile('(http://(?:www.)?lshstream.com[^\"\']+)')
        url = re.findall(reg,html)[0]
        return url
    except:
        try:
            reg = re.compile('fid=[\"\'](.+?)[\"\'].+?lshstream.+?.com/embed.js')
            fid = re.findall(reg,html)[0]
            url = 'http://www.lshstreams.com/embed.php?u=%s&vw=720&vh=420&live.realstreamunited.com=%s'%(fid,url)
            return url
        except:
            return

#castalba
def finder3(html,url):
    try:
        reg=re.compile('id=[\"\']([^\"\']+)[\"\'];.+?castalba.tv/.+?.js')
        id=re.findall(reg,html)[0]
        url = 'http://castalba.tv/embed.php?cid=%s&wh=600&ht=380&referer=%s'%(id,url)
        return url
    except:
      return

#jw_config
def finder4(html,url):
    ref = url
    try:
        links = re.compile('file\s*:\s*[\"\']([^\"\']+)[\"\']').findall(html)
        for link in links:
            if '.png' in link or link == '.flv':
                continue
            if '.f4m' in link:
                link = link+'?referer=%s'%url
            if '.m3u8' in link and '|' not in link:
                link += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': ref, 'X-Requested-With':constants.get_shockwave(), 'Host':urlparse.urlparse(link).netloc, 'Connection':'keep-alive','Accept':'*/*'})
            
            return link
    except:
        return 


#vlc_config
def finder5(html,url):
    try:
        soup=bs(html)
        try:
            link=soup.find('embed',{'id':'vlc'})
            link=link['target']

        except:
            link=soup.find('embed',{'name':'vlc'})
            link=link['target']  
        return link          
    except:
        return 

#sawlive
def finder6(html,url):
    try:
        uri = re.compile("[\"']([^\"\']*sawlive.tv\/embed\/[^\"'\/]+)\"").findall(html)[0] 
        page = re.compile('//.+?/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(uri)[0]
        host  = urlparse.urlparse(uri).netloc
        uri = 'http://sawlive.tv/embed/%s?referer=%s&host=%s' % (page,url,host)
        return uri
    except:
        try:
            uri = re.compile("src=(?:\'|\")(http:\/\/(?:www\.)?sawlive.tv\/embed\/.+?)(?:\'|\")").findall(html)[0] 
            page = re.compile('//.+?/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(uri)[0]
            host  = urlparse.urlparse(uri).netloc
            uri = 'http://sawlive.tv/embed/%s?referer=%s&host=%s' % (page,url,host)
            return uri
        except: 
            return

#yocast
def finder7(html,url):
    try:
        reg=re.compile('<script>fid\s*=\s*(?:\'|\")(.+?)(?:\'|\");.+?src=(?:\'|\")http://www.yocast.tv/.+?.js(?:\'|\")')
        id = re.findall(reg,html)[0]
        url='http://www.yocast.tv/embed.php?live=%s&vw=600&vh=450'%id
        return url
    except:
        return



#miplayer
def finder8(html,url):
    try:
        reg = re.compile("(http://(?:www\.)?miplayer.net/embed[^'\"]+)")
        url = re.findall(reg,html)[0]
        return url
    except:
        return

#castamp
def finder9(html,url):
    try:
        reg = re.compile("(http://(?:www.)?castamp.com/embed.php\?c=[^\"&]+)")
        url = re.findall(reg,html)[0]
        return url
    except:
        return

#04 stream
def finder10(html,url):
    try:
        reg = re.compile('04stream.com/\w+\.js\?stream=([^ "\'&]+)')
        url = re.findall(reg,html)[0]
        url = 'http://www.04stream.com/weed.js?stream=%s&width=600&height=460&str=is&link=1&cat=3'%url
        return url
    except:
        return

#leton
def finder11(html,url):
    try:
        html = urllib.unquote(html)
        reg = re.compile('leton.tv/player.php\?streampage=([^&]+)&')
        url = re.findall(reg,html)[0]
        url = 'http://leton.tv/player.php?streampage=%s&width=600&height=450'%url
        return url
    except:
        return

#yotv.co
def finder12(html,url):
    try:
        ref=url
        reg = re.compile("<script type='text/javascript'>\s*fid=(?:\'|\")(.+?)(?:\'|\");\s*v_width=.+?;\s*v_height=.+?;</script><script type='text/javascript' src='http://www.yotv.co/player.js'></script>")
        url = re.findall(reg,html)[0]
        url = 'http://www.yotv.co/embed.php?live=%s&vw=620&vh=490&referer=%s'%(url,ref)
        return url
    except:
        return

#hdcast
def finder13(html,url):
    try:
        url = re.compile('src="(http://(?:www\.)?hdcast.me/embed[^\'"]+)').findall(html)[0]
        return url 
    except:
        pass

#zerocast
def finder14(html,url):
    try:
        ref=url
        url = re.compile('zerocast\.(?:tv|in)/(?:channel|embed)?\.php\?a=(\d+)').findall(html)[0]
        url = 'http://zerocast.tv/channel.php?a=%s&width=640&height=480&autostart=true'%url
        return url 
    except:
        pass

#castup
def finder15(html,url):
    try:
        ref = url
        reg = '<script type="text/javascript">\s*fid=(?:\'|\")(.+?)(?:\'|\");.+?src="http://www.castup.tv/js/.+?.js">'
        url = re.findall(reg,html)[0]
        url = 'http://www.castup.tv/embed_2.php?channel=%s&vw=650&vh=410&referer=%s'%(url,ref)
        return url
    except:
        return

#mybeststream
def finder16(html,url):
    try:
        ref=url
        try:
            id = re.findall('id=(?:\'|\")(\d+)(?:\'|\");width=.*?pt987.googlecode.com',html)[0]
        except:
            id = re.findall('id=[\"\']([^\"\']+)[\"\'];.+?mybeststream.xyz',html)[0]
        url = 'http://mybeststream.xyz/gen_s.php?id=%s&width=640&height=385&referer=%s'%(id,ref)
        return url
    except:
        pass

#sunhd
def finder17(html,url):
    try:
        ref=url
        url = re.findall('src="(http://www.sunhd.info/channel.+?.php\?file=.+?)"',html)[0]
        return url+'&referer=%s'%ref
    except:
        pass

#youtube
def finder18(html,url):
    try:
        url = re.findall('src="?(https?://(?:www.|)youtube(?:-nocookie)?.com.+?[^\'\"]+)',html)[0]
        return url.replace('amp;','').replace('-nocookie','')
    except:
        return

#livestream
def finder19(html,url):
    try:
        url = re.findall('(http://(?:new\.)?livestream.com[^"]+)',html)[0]
        if 'player' in url:
            return url
    except:
        return

#privatestream
def finder20(html,url):
    try:
        try:
            id = re.findall('privatestream.tv/player\?streamname=([^&]+)&', html)[0]
        except:
            id = re.findall('privatestream.tv/((?!player)[^\.&\?\=]+)',html)[0]

        if id != 'js/jquery-1':
            url = 'http://privatestream.tv/player?streamname=%s&width=640&height=490'%id
            return url
        else:
            return
    except:
        return

#airq.tv
def finder21(html,url):
    try:
        id = re.findall('(?:SRC|src)="http://airq.tv/(\w+)',html)[0]
        url = 'http://airq.tv/%s/'%id
        return url
    except:
        return

#aliez
def finder22(html,url):
    try:
        ref = url
        try:
            id = re.findall('emb.aliez[\w\.]+?/player/live.php\?id=([^&"]+)',html)[0]
            return 'http://emb.aliez.me/player/live.php?id=%s&w=728&h=480&referer=%s'%(id,ref)
        except:
            try:
                id = re.findall('(?:94.242.255.35|195.154.44.194|aliez\.\w+)/player/(?:live|embed).php\?id=(\d+)',html)[0]
            except:
                id = re.findall('http://aliez.(?:me|tv)/live/(.+?)(?:/|"|\')',html)[0]
            return 'http://emb.aliez.me/player/live.php?id=%s&w=728&h=480&referer=%s'%(id,ref)
        return
    except:
        return

#p3g
def finder23(html,url):
    try:
        id = re.findall("channel='(.+?)',\s*g='.+?';</script><script type='text/javascript' src='http://p3g.tv/resources/scripts/p3g.js'",html)[0]
        url = 'http://www.p3g.tv/embedplayer/%s/2/600/420'%id
        return url
    except:
        return


#dinozap (not implemented)
def finder24(html,url):
    try:
        url = re.findall('(http://(?:www\.)?dinozap.info/redirect/channel.php\?id=[^"\']+)',html)[0]
        return url
    except:
        return

#liveflashplayer
def finder25(html,url):
    try:
        id = re.findall("channel='(.+?)', g='.+?';</script><script type='text/javascript' src='http://www.liveflashplayer.net/resources/scripts/liveFlashEmbed.js'>",html)[0]
        url = 'http://www.liveflashplayer.net/membedplayer/%s/1/620/430'%id
        return url
    except:
        return

#laola1
def finder26(html,url):
    try:
        url = re.findall('(http://www.laola1.tv[^"]+)', html)[0]
        return url
    except:
        pass

#ehftv
def finder27(html,url):
    try:
        url = re.findall('src=(?:\'|\")(http:\/\/(?:www\.)?ehftv.com(?:/|//)player\.php[^\'\"]+)',html)[0]
        return url
    except:
        return

#zoomtv
def finder28(html,url):
    try:
        ref=url
        try:
            fid = re.findall('fid="(.+?)".+?zome.zoomtv.me/.+?.js',html)[0]
        except:
            f = re.findall('fid=([^;]+)',html)[0]
            fid = re.findall('%s\s*=\s*[\"\']([^\"\']+)'%f,html)[0]
        pid = re.findall('pid\s*=\s*(.+?);',html)[0]
        url = 'http://www.zoomtv.me/embed.php?v=' + fid + '&vw=660&vh=450&referer=%s&pid=%s'%(ref,pid)
        return url
    except:
        return

#streamlive
def finder29(html,url):
    try:
        ref = url
        url = re.findall('src="(http://(?:www.)?streamlive.to/embed/[^"]+)"',html)[0]
        url = url + '&referer=%s'%ref
        return url
    except:
        return

#roja redirect links
def finder30(html,url):
    try:
        html = client.request(url, referer=urlparse.urlparse(url).netloc)
        url = re.findall('href="(.+?)">click here...',html)[0]
        resolved = find_link(url+'&referer=http://rojedirecta.me')
        return resolved
    except:
        return

#iguide
def finder31(html,url):
    try:
        ref=url
        url = re.findall('(http://(?:www.)?iguide.to/embed/[^"\']+)"',html)[0]
        return url+'&referer='+ref
    except:
        return

#letgo
def finder32(html,url):
    try:
        id = re.findall('fid="(.+?)"; v_width=.+?; v_height=.+?;</script><script type="text/javascript" src="http://www.letgo.tv/js/embed.js"',html)[0]
        url = 'http://www.letgo.tv/embed.php?channel=%s&vw=630&vh=450'%id
        return url
    except:
        return

#streamup
def finder33(html,url):
    ref = url
    try:
        id = re.findall("streamup.com/rooms/([^/\'\"?&\s]+)",html)[0]
        url = 'http://streamup.com/%s'%id
        return url
    except:
        try:
            id = re.findall('streamup.com/([^/\'\"?&\s]+)/embed',html)[0]
            url = 'http://streamup.com/%s'%(id)
            return url
        except:
            return

#p2pcast
def finder34(html,url):
    try:
        ref = url
        try:
            id = re.findall('http://p2pcast.tv/(?:p2pembed|stream).php\?id=([^&]+)',html)[0]
        except:
            id = re.findall("id=[\"\'](.+?)[\"\'];.+?src=[\"\']http://js.p2pcast.+?.js",html)[0]
        url = 'http://p2pcast.tv/stream.php?id=%s&referer=%s'%(id,ref)
        return url
    except:
        return

def finder35(html,url):
    try:

        try:
            id = re.findall('cast3d.tv/embed.php\?(?:u|channel)=([^&]+)&',html)[0]
        except:
            id = re.findall('fid\s*=\s*(?:\'|\")(.+?)(?:\'|\");.*\s*.+?src=(?:\'|\")http://www.cast3d.tv/js/.+?.js',html)[0]
        url = 'http://www.cast3d.tv/embed.php?channel=%s&vw=600&vh=400'%id
        return url
    except:
        return

#xvtr
def finder36(html,url):
    try:
        ref = url
        id = re.findall("fid=\"(.+?)\".+?</script><script type='text/javascript' src='http://www.xvtr.pw/embed.js'></script>",html)[0]
        url = 'http://www.xvtr.pw/channel/%s.htm?referer=%s'%(id,ref)
        return url
    except:
        return

#acestream
def finder37(html,url):
    try:
        try:
            ace = re.findall('this.load(?:Player|Torrent)\((?:\'|\")(.+?)(?:\'|\")',html)[0]
        except:
            ace = re.findall('"http://torrentstream.net/p/(.+?)"',html)[0]
        url = 'plugin://program.plexus/?mode=1&url=%s&name=Video'%(ace)
        return url
    except:
        return

#sopcast
def finder38(html,url):
    try:

        sop = re.findall("(sop://[^\"\']+)['\"]",html)[0]
        url = 'plugin://program.plexus/?mode=2&url=%s&name=Video'%(sop)
        return url
    except:
        return

#turbocast
def finder39(html,url):
    try:
        url = re.findall('(http://www.turbocast.tv[^\'\"]+)',html)[0]
        return url
    except:
        try:
            url = re.findall('(.+?turbocast.tv.+?)',url)[0]
            return url
        except:
            return

#directstream
def finder40(html,url):
    try:
        ref=url
        fid = re.findall('fid=(?:\'|\")(.+?)(?:\'|\").+?</script><script type="text/javascript" src="http://direct-stream.org/embedStream.js"',html)[0]
        url = 'http://direct-stream.org/e.php?id=%s&vw=740&vh=490&referer=%s'%(fid,ref)
        return url
    except:
        return

#pxstream
def finder42(html,url):
    try:
        ref=url

        id = re.findall("file=(?:\'|\")(.+?)(?:\'|\");.+?src='http://pxstream.tv/.+?.js",html)[0]
        url = 'http://pxstream.tv/embedrouter.php?file=%s&width=730&height=430&jwplayer=flash&referer=%s'%(id,ref)
        return url
    except:
        return

#publishpublish
def finder43(html,url):
    try:
        ref=url
        id = re.findall('fid="(.+?)";.+?</script><script type="text/javascript" src="http://www.pushpublish.tv/js/embed.js"',html)[0]
        loc = (urlparse.urlparse(url).netloc).replace('www.','')
        url  ='http://www.pushpublish.tv/player.php?channel=%s&vw=650&vh=400&domain=%s&referer=%s'%(id,loc,ref)
        return url
    except:
        return
#ucaster
def finder44(html,url):
    try:
        ref=url
        id = re.findall('channel=[\'"]([^\'"]+)[\'"].*?ucaster.(?:eu|com)', html)[0]
        url = 'http://www.embeducaster.com/membedplayer/%s/1/595/500?referer=%s'%(id,ref)
        return url
    except:
        return

#rocktv
def finder45(html,url):
    try:
        ref=url
        id = re.findall("fid=[\'\"]([^\'\"]+)[\'\"];.+?src=[\'\"]http://www.rocktv.co/player.+?.js",html)[0]
        url = 'http://rocktv.co/embed.php?live=%s&vw=620&vh=490&referer=%s'%(id,ref)
        return url
    except:
        return

#ezcast
def finder46(html,url):
    try:
        ref=url
        id = re.findall("channel=(?:\'|\")(.+?)(?:\'|\").+?src=(?:\'|\")http://www.ezcast.tv/static/scripts/ezcast.js(?:\'|\")>",html)[0]
        url = 'http://www.embedezcast.com/embedplayer/%s/1/790/420?referer=%s'%(id,ref)
        return url
    except:
        return

#micast
def finder47(html,url):
    try:
        ref=url
        try:
            id = re.findall('micast.tv/.*?\.php\?ch=([^"\']+)',html)[0]
        except:
            try:
                id = re.findall('turbocast.tv/.*?\.php\?ch=([^"]+)',html)[0] 
            except:
                id  = re.findall('(?:ca|ch)=(?:\'|\")(.+?)(?:\'|\").+?micast.tv/embed.js(?:\'|\")',html)[0]

        url = 'http://micast.tv/iframe.php?ch=%s&referer=%s'%(id,ref)
        return url
    except:
        return


#openlive
def finder48(html,url):
    try:
        ref=url
        id = re.findall("file=(?:\'|\")(.+?)(?:\'|\").+?src=(?:\'|\")http://openlive.org/live.js(?:\'|\")>",html)[0]
        url = 'http://openlive.org/embed.php?file=%s&width=640&height=380&referer=%s'%(id,ref)
        return url
    except:
        return

#helper
def finder49(html,url):
    try:
        ch = re.findall('fid=(?:\'|\")(.+?)(?:\'|\");.+?src=(?:\'|\")http://www.webspor.pw/HD/TV/info/channel.js(?:\'|\")>',html)[0]
        url = 'http://worldsport.me/%s'%ch
        return find_link(url)
    except:
        return

#sostart
def finder50(html,url):
    try:
        ref=url
        id = re.findall("id=(?:\'|\")(.+?)(?:\'|\");.+?src=(?:\'|\")http://.+?sostart.([^/]+)/.+?.js(?:\'|\")>",html)[0]
        url = 'http://sostart.%s/stream.php?id=%s&width=630&height=450&referer=%s'%(id[1],id[0],ref)
        return url
    except:
        return


#lsh
def finder52(html,url):
    try:
        ref=url
        id = re.findall('fid=(?:\'|\")(.+?)(?:\'|\");.+?src=(?:\'|\")http://cdn.lshstream.com/embed.js(?:\'|\")>')
        url = 'http://cdn.lshstream.com/embed.php?u=%s&referer=' + ref
        return url
    except:
        return

#hqstream
def finder53(html,url):
    try:

        ref=url
        id = re.findall('http://hqstream.tv/.+?\?streampage=([^&/ ]+)',html)[0]
        url = 'http://hqstream.tv/player.php?streampage=%s&height=480&width=700&referer=%s'%(id,ref)
        return url
    except:
        return

#jw rtmp
def finder54(html,url):
    try:
        rtmp = re.findall('jwplayer.+?file.?\s*:\s*[\"\']((?:rtmp|http)?://[^\"\']+)[\"\']',html)[0]
        return rtmp
    except:
        return

#tutele
def finder55(html,url):
    try:
        ref = url
        id = re.findall("channel=(?:\'|\")(.+?)(?:\'|\").+?src='http://tutelehd.com/embedPlayer.js'>",html)[0]
        url = 'http://tutelehd.com/embed/embed.php?channel=%s&referer=%s'%(id,ref)
        return url
    except:
        return


#janjua
def finder56(html,url):
    try:
        ref = url
        id = re.findall("channel=(?:\'|\")(.+?)(?:\'|\").+?src=(?:\'|\")http://www.janjua.tv/resources/scripts/janjua.js(?:\'|\")>",html)[0]
        url = 'http://www.janjua.tv/embedplayer/%s/1/500/400?referer=%s'%(id,ref)
        return url
    except:
        return

#abcast
def finder57(html,url):
    try:
        ref = url
        id = re.findall("file=(?:\'|\")(.+?)(?:\'|\").+?src=(?:\'|\")http://abcast.net/simple.js(?:\'|\")",html)[0]
        url = 'http://abcast.net/embed.php?file=%s&referer=%s'%(id,ref)
        return url
    except:
        return

#castfree
def finder58(html,url):
    try:
        ref = url
        id = re.findall('castfree.me/channel.php\?a=(\d+)',html)[0]
        url = 'http://www.castfree.me/embed.php?a=%s&id=&width=640&height=460&autostart=true&referer=%s'%(id,ref)
        return url
    except:
        return

#dinozap 
def finder59(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](http://(?:www.)?player(?:hd|app)\d+.pw/channel(?:fr)?.php\?file=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return

#dinozap
def finder60(html,url):
    try:
        ref = url
        id = re.findall('(?:www\.)?sitenow.me/channel.php\?file=([^"\']+)',html)[0]
        return url + 'http://www.sitenow.me/channel.php?file=%s&width=670&height=470&autostart=true&referer=s'%(id,ref)
    except:
        return

#streamcasttv
def finder61(html,url):
    try:
        id = re.findall("file=(?:\'|\")(.+?)(?:\'|\");.+?src=(?:\'|\")http://streamcasttv.biz/.+?.js",html)[0]
        url ='http://streamcasttv.biz/embed.php?file=%s&referer=%s'%(id,url)
        return url
    except:
        return


#rtmp
def finder63(html,url):
    try:
        swf = re.findall('src=(?:\'|\")(.+?.swf)',html)[0]
        file, rtmp = re.findall('flashvars=(?:\'|\")file=(.+?)&.+?streamer=(.+?)&',html)[0]
        url = rtmp + ' playpath=' + file +' swfUrl=' + swf + ' flashver=WIN\\2019,0,0,226 live=true timeout=15 swfVfy=true pageUrl=' + url
        return url
    except:
        return

def finder64(html,url):
    try:
        url = re.findall('(http://vaughnlive.tv/embed/video/[^/\'"?&\s]+)',html)[0]
        return url

    except:
        return

def finder65(html,url):
    try:
        referer = url
        url = re.findall('src=(?:\'|\")(.+?)(?:\'|\").+?type="video/mp4"',html)[0]
        if len(url)<10:
            raise
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': referer})

        return url
    except:
        return

#hdcast.org
def finder66(html,url):
    try:
        ref = url
        id,id2 = re.findall('fid="(.+?)";.+?src="http://hdcast.org/(.+?).js">',html)[0]
        url = 'http://www.hdcast.org/%s.php?u=%s&vw=854&vh=480&domain=%s&referer=%s'%(id2,id,urlparse.urlparse(ref).netloc,ref)
        return url
    except:
        return

#serbiaplus
def finder67(html,url):
    try:
        if 'serbiaplus' not in url:
            return
        id = re.findall('fid="(.+?)";.+?src="/live.js"',html)[0]
        url = 'http://serbiaplus.com/' + id
        resolved = find_link(url) 
        return resolved
    except:
        pass

#streamking
def finder68(html,url):
    try:
        ref = url
        url = re.findall('(http://streamking.cc/[^"\']+)(?:\'|\")',html)[0]
        return url+'&referer=%s'%ref
    except:
        return

#beba
def finder69(html,url):
    try:
        url = re.findall('http://beba.ucoz.com/playerlive.html\?id=(.+?)$',url)[0]
        return find_link(url)
    except:
        return

#stream-sports
def finder70(html,url):
    try:
        ref = url
        url = re.findall('http://www.stream\-sports.eu/uploads/video.html\?id=(.+?)$',url)[0]
        return url+'&referer=%s'%ref
    except:
        return

#ustream
def finder71(html,url):
    try:
        ref=url
        url=re.findall('(https?://(?:www.)?ustream.tv/embed/.+?[^\'\"]+)',html)[0]
        url+='&referer='+ref
        return url
    except:
        return

#config finder
def finder72(html,ref):
    try:
        url = re.findall('src\s*:\s*\'(.+?(?:.m3u8)?)\'',html)[0]
        if 'images/' in url:
            return
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': ref})
        return url
    except:
        pass


#config finder
def finder73(html,url):
    try:
        ref = url
        url = re.findall('Player\(\{\n\s*source\:\s*[\'\"](.+?)[\'\"]\,',html)[0]
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': ref})
        if 'ace/manifest' in url:
            url = finder102(html,url)
        return url
    except:
        return


#cast4u
def finder74(html,url):
    try:
        ref = url

        id = re.findall('id=[\'\"](.+?)[\'\"].+?src=[\'\"]http://www.cast4u.tv/.+?.js',html)[0]
        url = 'http://www.cast4u.tv/embed.php?live=%s&vw=620&vh=490&referer=%s'%(id,ref)
        return url
    except:
        return
        
#m3u8 config finder
def finder75(html,url):
    try:
        ref = url
        url = re.findall('file: window.atob\(\'(.+?)\'\),', html)[0]
        file = base64.b64decode(url)
        file += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': ref, 'X-Requested-With':constants.get_shockwave(), 'Host':urlparse.urlparse(file).netloc, 'Connection':'keep-alive','Accept':'*/*'})
        return file
    except:
        return

#direct stream 2nd finder
def finder76(html,url):
    ref = url
    try:
        id = re.findall('fid=[\"\'](.+?)[\"\'];.+?data-rocketsrc="http://direct-stream.org/.+?.js',html)[0]
        url ="http://direct-stream.org/e.php?id=%s&vw=700&vh=400&referer=%s"%(id,ref)
        return url
    except:
        return

#zona priority
def finder77(html,url):
    try:
        html = urllib.unquote(html)
        url = finder4(html,url)
        if client.request(url) != None:
            return url
        return
    except:
        return

#weplayer
def finder78(html,url):
    try:
        id = re.findall("id=['\"](.+?)['\"];.+?src=['\"]http://weplayer.([^/]+)/.+?.js([^\s]+)",html)[0]
        url = 'http://weplayer.%s/stream.php?id=%s&width=640&height=480&referer=%s'%(id[1],id[0],url)
        if '-->' in id[2]:
            return
        return find_link(url)
    except:
        return

def finder79(html,url):
    try:
        ref = url
        url = re.findall("playStream\('hls', '(.+?)'",html)[0] 
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': ref, 'X-Requested-With':constants.get_shockwave(), 'Host':urlparse.urlparse(url).netloc, 'Connection':'keep-alive','Accept':'*/*'})
        return url
    except:
        return

#tvope
def finder80(html,ref):
    try:
        id = re.findall('c="(.+?)";.+?</script>\s*<script.+?src="http://i.tvope.com/js/.+?.js',html)[0]
        url = 'http://tvope.com/emb/player.php?c=%s&w=700&h=480&referer=%s&d=www.popofthestreams.xyz'%(id,ref)
        return url
    except:
        return

#dinozap 
def finder81(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](https?://(?:www\.)?dinozap.info/redirect/channel.php\?id=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return

#dinozap 
def finder82(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](https?://(?:www\.)?tv.verdirectotv.org/channel.php\?file=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return

#dinozap 
def finder83(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](https?://(?:www\.)?dinostream.pw/channel.php\?file=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return

#dinozap 
def finder84(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](https?://(?:www\.)?(?:serverhd.eu|cast3d.me)/channel\w*\.php\?file=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return

#dinozap 
def finder85(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](https?://(?:www\.)?sstream.pw/channel.php\?file=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return
#dinozap 
def finder86(html,url):
    try:
        ref = url
        url = re.findall('[\"\'](https?://(?:www\.)?ponlatv.com/channel.php\?file=[^"\']+)',html)[0]
        return url + '&referer=' + ref
    except:
        return

#acestream
def finder90(html,ref):
    try:
        url  = re.findall('(acestream://[^"\']+)["\']',html)[0]   
        return url
    except:
        return

#sopcast
def finder91(html,ref):
    try:
        url  = re.findall('(sop://[^"\']+)["\']',html)[0]
        return url
    except:
        return

#shadownet
def finder92(html,ref):
    try:
        url = re.findall('src=[\"\']([^\"\']+)[\"\'].+?mpeg',html)[0]
        if 'rtmp' in url:
            url+=' swfUrl=http://www.shadow-net.biz/javascript/videojs/flashls/video-js.swf flashver=%s live=true timeout=18 swfVfy=1 pageUrl=http://www.shadow-net.biz/'%FLASH
        elif 'm3u8' in url:

            url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': ref, 'X-Requested-With':constants.get_shockwave(), 'Host':urlparse.urlparse(url).netloc, 'Connection':'keep-alive','Accept':'*/*', 'Origin':'http://shadow.go.ro'})
        return url
    except:
        return

#filmon
def finder93(html,ref):
    try:
        id = re.findall('filmon.(?:com|tv)/tv/channel/export\?channel_id=(\d+)',html)[0]
        url =  'http://www.filmon.com/channel/' + id
        return url
    except:
        return

#castto
def finder94(html,ref):
    try:
        id = re.findall('fid=["\'](.+?)["\'];.+?src=["\'](http://static.castto.me/js/.+?.js)', html)[0]
        url = id[1]+'?id=%s&referer=%s'%(id[0],ref)
        return url
    except:
        return

#redirect
def finder95(html,url):
    try:
        url = re.findall('<meta http-equiv="refresh".+?; url=(.+?)"',html)[0]
        return find_link(url)
    except:
        return

#acelive
def finder96(html,url):
    try:
        url = re.findall('[\"\'](.+?.acelive.+?)[\"\']',html)[0]
        return url
    except:
        return


#castasap
def finder97(html,url):
    try:
        ref = url
        import requests
        html = requests.get(url).text
        chars = re.findall('&#(\d+)',html)
        for c in chars:
            html = html.replace('&#%s'%c, chr(int(c)))
        html = html.replace(';','')
        url = re.findall('src=[\"\'](http://www.(?:castasap|castflash|flashlive|fastflash).pw/embed.+?)[\"\']',html)[0]

        url = add_args(url,{'referer':ref})
        return url
    except:
        return

#deltatv
def finder98(html,ref):
    try:
        x,y = re.findall('id=[\'\"](.+?)[\'\"].+?src=[\'\"]http://deltatv.([^/]+)/.+?.js',html)[0]
        url = 'http://deltatv.%s/stream.php?id=%s&width=640&height=480&referer=%s'%(y,x,ref)
        return url
    except:
        return

#hdcast.info
def finder99(html,ref):
    try:
        id,rr = re.findall('fid=[\'\"](.+?)[\'\"].+?src=[\'\"]http://(?:www.)?hdcast.info/([^\.]+).js',html)[0]
        url = 'http://www.hdcast.info/%s.php?live=%s&vw=620&vh=490&referer=%s'%(rr,id,ref)
        return url
    except:
        return

#deltatv
def finder100(html,ref):
    try:
        url = re.findall('(http://deltatv.(?:pw|xyz)?/stream.php\?.+?[^"\']+)',html)[0]
        url = url + '&referer=' + ref
        return url
    except:
        return

#mybest
def finder103(html,ref):
    try:
        url = re.findall('(http://mybeststream.xyz.+?[^"\']+)',html)[0]
        url = url + '&referer=' + ref
        return url
    except:
        return


#blowfish decrypt
def finder100(html,ref):
    try:
        if 'Blowfish' not in html:
            return
            
        key = re.findall('new Blowfish\([\"\'](.+?)[\"\']\)',html)[0]
        if len(key)>56:
            key=key[:56]
        crypted = re.findall('.decrypt\([\"\'](.+?)[\"\']\)',html)[0].decode("hex")
        from modules import blowfish
        cipher = blowfish.Blowfish(key)

        decrypted = cipher.decrypt(crypted)
        return find_link(ref,html=decrypted)
    except:
        return

#theactionlive
def finder101(html,ref):
    try:
        id = re.findall('id=[\"\'](.+?)[\"\'];.+?src=[\"\']http://theactionlive.com.+?.js',html)[0]
        url = 'http://theactionlive.com?id=%s&referer=%s'%(id,ref)
        return url
    except:
        return

#acestream
def finder102(html,ref):
    try:
        url = 'acestream://' + re.findall('ace/manifest.m3u8\?id\=([^\'\"]+)[\'\"]',url)[0]
        return url
    except:
        return


#kolstg
def finder105(html,ref):
    try:
        id = re.findall('fid=["\'](.+?)["\'];.+?src=["\']http://(?:www.)?kolstg.pw/.+?.js', html)[0]
        url = 'http://www.hornos.moy.su/channel/'+ id+'.htm?referer=' + ref
        return url
    except:
        return

#mips
def finder106(html,ref):
    try:
        try:
            ch,e = re.findall('channel=[\'\"](.+?)[\'\"]\s*,\s*e=[\'\"](.+?)[\'\"].+?src=[\'\"]http://(?:www.)?mipsplayer.com/.+?.js',html)[0]
        except:
            e,ch = re.findall('[,\s]e=[\'\"](.+?)[\'\"]\s*,\s*channel=[\'\"](.+?)[\'\"].+?src=[\'\"]http://(?:www.)?mipsplayer.com/.+?.js',html)[0]
        url = 'http://www.mipsplayer.com/membedplayer/'+ch+'/'+e+'/675/400?referer=' + ref
        return url
    except:
        return

#m3u8
def finder107(html,ref):
    try:
        m3u8 = re.findall('playlist_url:\s*[\"\']([^\"\']+)',html)[0]
        host = re.findall('cdn_host:\s*[\"\']([^\"\']+)',html)[0]
        url = 'http://' + host + m3u8
        url+='|%s' % urllib.urlencode({'Referer':ref, 'User-agent':client.agent()})
        return url
    except:
        return

#streamsus
def finder108(html,ref):
    try:
        url = re.findall('Watch Live\s*<a href=[\"\'](.+?)[\"\']>Here',html)[0]
        return find_link(url)
    except:
        return

#f4m
def finder109(html,ref):
    try:
        f4m = re.findall('name=[\"\']flashvars[\"\'].+?value=[\"\']src=([^&]+)&',html)[0]
        url = urllib.unquote(f4m)
        return url
    except:
        return
        return


#zona4vip
def finder110(html,ref):
    try:
        if 'zona4vip' not in ref:
            return
        fid = re.findall('fid=[\"\'](.+?)[\"\'].+?src=[\"\']/live.js',html)[0]
        url = 'http://www.zona4vip.com/'+ fid

        return find_link(url)
    except:
        return

#veetle livetvcdn
def finder111(html,ref):
    try:
        id = re.findall('veetle&c=([^&]+)',ref)[0]
        url = 'http://veetle.com/v/' + id
        return url
    except:
        return

#vlc new
def finder112(html,ref):
    try:
        url = re.findall('version=[\"\']VideoLAN.VLCPlugin.2[\"\'].+?target=[\"\']([^\"\']+)',html)[0]
        return url
    except:
        return

#lsh stream embed
def finder113(html,ref):
    try:
        fid = re.findall('fid=[\"\'](.+?)[\"\'].+?src=[\"\'].+?lshstream.com/embed.js',html)[0]
        loc = urlparse.urlparse(ref).netloc
        url = 'http://www.lshstream.com/embed.php?u=%s&vw=640&vh=360&domain=%s'%(fid,loc)
        return find_link(url)
    except:
        return
#castamp
def finder114(html,ref):
    try:
        fid = re.findall('channel=[\"\'](.+?)[\"\'].+?src=[\"\'].+?castamp.com/embed.js',html)[0]
        url = 'http://castamp.com/embed.php?c=%s&vwidth=640&vheight=380&referer=%s'%(fid,ref)
        return url
    except:
        return

#bro.adca.st
def finder115(html,ref):
    
    try:
        id = re.findall('id=[\"\'](.+?)[\"\'].+?src=[\"\'].+?bro.adca.st/.+?.js',html)[0]
        url = 'http://bro.adca.st/stream.php?id='+id+'&width=640&height=460&referer=' + ref + '&stretching=uniform'
        return url
    except:
        try:
            url = re.findall('(http://bro.adca.st/stream.php[^\"\']+)',html)[0]
            url = url + '&referer=' + ref
            return url
        except:
            return

#akamai rtmpe
def finder116(html,ref):
    if 'akamai' in ref:
        html = decryptionUtils.doDemystify(html)
        swf,streamer,file,token = re.findall('flashplayer:[\"\']([^\"\']+)[\"\'],streamer:[\"\']([^\"\']+)[\"\'],file:[\"\']([^\"\']+)[\"\'],token:[\"\']([^\"\']+)[\"\']',html)[0]
        swf = 'http://akamaistreaming.com/' + swf
        url = '%s playpath=%s token=%s swfUrl=%s pageUrl=%s flashver=%s'%(streamer,file,token,swf,ref,constants.flash_ver())
        return url

#zunox stream
def finder117(html,ref):
    if 'zunox' in ref:
        url = 'http://zunox.hk/players/' + re.findall('(proxy.php\?id=[^\"\']+)',html)[0]
        h2 = client.request(url)
        import json
        j = json.loads(h2)
        host  = urlparse.urlparse(j['url']).netloc.split(':')[0].replace(':80','')
        url = j['url'].replace(':80','') +'.flv' + '|%s' % urllib.urlencode({'User-agent':client.agent(),'X-Requested-With':constants.get_shockwave(),'Referer':ref, 'Host':host, 'Connection':'keep-alive','Accept-Encodeing':'gzip, deflate, lzma, sdch'})
        return url

#sportstream365
def finder118(html,ref):
    try:
        try:
            id = re.findall('"sportstream365.com.+?game=(\d+)',html)[0]
        except:
            id = re.findall('"sportstream365.com.+?game=(\d+)',ref)[0]
        return 'http://sportstream365.com/?game=%s&referer=%s'%(id,ref)
    except:
        return

#cndhls
def finder119(html,ref):
    try:
        id = re.findall('id=[\"\'](.+?)[\"\'].+?src=[\"\'].+?cndhls.+?.js',html)[0]
        d = (urlparse.urlparse(ref).netloc).replace('www.','')
        url = 'http://www.cndhlsstream.pw/embed.php?channel='+id+'&vw=640&vh=385&domain=' + d + '&referer=' + ref
        return url
    except:
        return

#superplayer
def finder120(html,ref):
    try:
        id = re.findall("id=['\"](.+?)['\"];.+?src=['\"].+?superplayer.+?.js",html)[0]
        url = 'http://nowlive.xyz/embed.php?id=%s&width=640&height=480&referer=%s'%(id,ref)
        if '-->' in id[2]:
            return
        return find_link(url)
    except:
        return

#scity
def finder121(html,url):
    try:
        ref=url
        id = re.findall("id=(?:\'|\")(.+?)(?:\'|\");.+?src.+?scity.tv.+?.js",html)[0]
        url = 'http://scity.tv/stream.php?id=%s&width=630&height=450&referer=%s'%(id,ref)
        return url
    except:
        return


def finder123(html,ref):
    try:
        url = re.findall('mpegurl.+?src=[\"\']([^\"\']+)[\"\']',html)[0]
        return url + '|%s' % urllib.urlencode({'Referer':ref,'X-Requested-With':constants.get_shockwave(),'User-agent':client.agent()})
    except:
        return
#streamify
def finder124(html,url):
    try:
        ref=url
        id = re.findall("channel=[\"\']([^\"\']+)[\"\'].+?src.+?streamifyplayer.com.+?.js",html)[0]
        url = 'http://www.streamifyplayer.com/embedplayer/%s/1/620/430?referer=%s'%(id,ref)
        return url
    except:
        return

#youtube live
def finder125(html,url):
    try:
        if 'youtube-live' in html:
            url = re.findall("(https?://(?:www.)?youtube.com/[^\"\']+)",html)[0]
            return url
    except:
        return

#streamp2p
def finder126(html,url):
    try:
        url = re.findall('(http://(?:www.)?streamp2p.com[^\"\']+)[\"\']',html)[0]
        return url
    except:
        return

def finder127(html,url):
    try:
        
        try:
            html = urllib.unquote(html)
        except:
            pass
        url = re.findall('src=(http.+?m3.+?[^&]+)&',html)[0]
        if 'amis' in url:
            url = url.strip() +'|User-Agent=Mozilla/5.0'

        return url.strip()
    except:
        return

#akamaistreaming
def finder128(html,ref):
    try:
        id = re.findall("id=['\"](.+?)['\"].+?src=['\"].+?akamaistreaming.+?.js",html)[0]
        url = 'http://akamaistreaming.com/zn.php?id=%s&width=640&height=385&referer=%s'%(id,ref)
        return url
    except:
        return

def finder129(html,ref):
    try:
        id = re.findall("id=['\"](.+?)['\"].+?src=['\"].+?akamaistreaming.+?.js",html)[0]
        url = 'http://akamaistreaming.com/zn.php?id=%s&width=640&height=385&referer=%s'%(id,ref)
        return url
    except:
        return

