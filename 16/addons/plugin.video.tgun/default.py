import xbmc, xbmcgui
import urllib, urllib2
import re, string
import os, time
import traceback
import random
from urlparse import urlparse
from addon.common.addon import Addon
from addon.common.net import Net
net = Net()


addon_id = 'plugin.video.tgun'

#Common Cache
# plugin constants
dbg = False # Set to false if you don't want debugging

#Common Cache
try:
  import StorageServer
except Exception, e:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer(addon_id)


##### XBMC  ##########
addon = Addon(addon_id, sys.argv)
datapath = addon.get_profile()


##### Paths ##########
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "cookiejar.lwp")
if os.path.exists(cookie_path) == False:
    os.makedirs(cookie_path)

##### Queries ##########
play = addon.queries.get('play', None)
mode = addon.queries['mode']
page_num = addon.queries.get('page_num', None)
url = addon.queries.get('url', None)

addon.log('----------------------TGUN Addon Params------------------------')
addon.log('--- Version: ' + str(addon.get_version()))
addon.log('--- Mode: ' + str(mode))
addon.log('--- Play: ' + str(play))
addon.log('--- URL: ' + str(url))
addon.log('--- Page: ' + str(page_num))
addon.log('---------------------------------------------------------------')

################### Global Constants #################################

main_url = 'http://www.tgun.tv/'
shows_url = main_url + 'shows/'
#showlist_url = 'http://www.tgun.tv/menus2/shows/chmenu%s.php'
showlist_url = 'http://www.tgun.tv/menus/shows/chmenu.php'
num_showpages = 4
classic_url = main_url + 'classic/'
classic_shows_url = 'http://www.tgun.tv/menus2/classic/chmenu%s.php'
livetv_url = main_url + 'usa/'
livetv_pages = 'http://www.tgun.tv/menus2/usa/chmenu%s.php'
addon_path = addon.get_path()
icon_path = addon_path + "/icons/"

######################################################################

def Notify(typeq, title, message, times, line2='', line3=''):
     #simplified way to call notifications. common notifications here.
     if title == '':
          title='TGUN Notification'
     if typeq == 'small':
          if times == '':
               times='5000'
          smallicon= icon_path + 'tgun.png'
          xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+smallicon+")")
     elif typeq == 'big':
          dialog = xbmcgui.Dialog()
          dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
     else:
          dialog = xbmcgui.Dialog()
          dialog.ok(' '+title+' ', ' '+message+' ')


def get_url(url, data=None, headers=None, use_cache=True, cache_limit=8):

    html = ''
    if use_cache:
        created = cache.get('timestamp_' + url)
        if created:
            age = time.time() - float(created)
            limit = 60 * 60 * cache_limit
            if age < limit:
                html = cache.get(url)
                if html:
                    addon.log_debug('Cache URL data found for: %s' % url)
                    return html
    
    addon.log('Retrieving: %s' % url)
    if data:
        if headers:
            html = net.http_POST(url, data, headers=headers).content
        else:
            html = net.http_POST(url, data).content
    else:
        if headers:
            html = net.http_GET(url, headers=headers).content
        else:
            html = net.http_GET(url).content

    if use_cache:            
        cache.set(url, html)
        cache.set('timestamp_' + url, str(time.time()))

    return html


def sys_exit():
    xbmc.executebuiltin("XBMC.Container.Update(addons://sources/video/plugin.video.tgun?mode=main,replace)")
    return


def sawlive(embedcode, ref_url):
    url = re.search("<script type='text/javascript'> swidth='[0-9%]+', sheight='[0-9%]+';</script><script type='text/javascript' src='(.+?)'></script>", embedcode, re.DOTALL).group(1)
    ref_data = {'Referer': ref_url}

    try:
        ## Current SawLive resolving technique - always try to fix first
        html = net.http_GET(url,ref_data).content
        get_url(url, ref_data)
        link = re.search('src="(http://sawlive.tv/embed/watch/[A-Za-z0-9_/]+)">', html).group(1)
        addon.log(link)

    except Exception, e:
        ## Use if first section does not work - last resort which returns compiled javascript
        addon.log('SawLive resolving failed, attempting jsunpack.jeek.org, msg: %s' % e)
        Notify('small','SawLive', 'Resolve Failed. Using jsunpack','')
        
        jsunpackurl = 'http://jsunpack.jeek.org'
        data = {'urlin': url}
        html = get_url(jsunpackurl, data=data)
        link = re.search('src="(http://sawlive.tv/embed/watch/[A-Za-z0-9]+[/][A-Za-z0-9_]+)"',html).group(1)
        addon.log(link)

    html = get_url(link, headers=ref_data)
    
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\', \'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\', \'(.+?)\'', html).group(1)
    appUrl = re.search('rtmp[e]*://.+?/(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' app=', appUrl,
       ' pageURL=', url,
       ' swfUrl=', swfPlayer,
       ' live=true'])
    addon.log(rtmpUrl)
    return rtmpUrl


def shidurlive(embedcode, ref_url):
    url = re.search("<script type='text/javascript'> swidth='100%', sheight='100%';</script><script type='text/javascript' src='(.+?)'></script>", embedcode, re.DOTALL).group(1)
    ref_data = {'Referer': ref_url}

    try:
        html = get_url(url, headers=ref_data)
        url = re.search('src="(.+?)">', html).group(1)
    except Exception, e:
        addon.log_error('Cannot resolver shidurlive link')
        return None

    html = get_url(url, headers=ref_data)
    
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\', \'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\', \'(.+?)\'', html).group(1)
    appUrl = re.search('rtmp[e]*://.+?/(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' app=', appUrl,
       ' pageURL=', url,
       ' swfUrl=', swfPlayer,
       ' live=true'])
    addon.log(rtmpUrl)
    return rtmpUrl


def mediaplayer(embedcode):
    url = re.search('<embed type="application/x-mplayer2" .+? src="(.+?)"></embed>', embedcode).group(1)
    addon.log('Retrieving: %s' % url)
    html = net.http_GET(url).content
    
    matches = re.findall('<Ref href = "(.+?)"/>', html)
    url = matches[1]
    
    html = get_url(url)
    
    return re.search('Ref1=(.+?.asf)', html).group(1)


def streamlive(embedcode):
    
    #channel = re.search('<script type="text/javascript" src="http://www.streamlive.to/embed/(.+?)&width=.+?"></script>', embedcode)
    channel = par
    addon.log(channel)
    headers = {
            'Referer': 'http://www.streamlive.to/',
            'Host': 'www.streamlive.to',
            'Origin': 'www.streamlive.to'
        }
    
    if channel:
        #url = 'http://www.streamlive.to/embedplayer.php?channel=%s' % channel.group(1)
        url = 'http://www.streamlive.to/embedplayer.php?channel=%s' % channel
        html = get_url(url, headers=headers)
        
        token_url=re.compile('''.*getJSON\("([^'"]+)".*''').findall(html)[0]
        if not token_url.startswith('http'):
            token_url = 'http:' + token_url
            
        token_html = get_url(token_url, headers=headers)
        token=re.compile('{"token":"(.+?)"}').findall(token_html)[0]
        
        filename = re.search('file: "([^&]+).flv"', html).group(1)
        rtmp = re.search('streamer: "(.+?)",', html).group(1)
        rtmp = rtmp.replace("\\", "")
        app = re.search('rtmp://[\.\w:]*/([^\s]+)', rtmp).group(1)
    else:
        filename = re.search('streamer=rtmp://live.streamlive.to/edge&file=(.+?)&autostart=true&controlbar=bottom"', embedcode).group(1)
        url = 'http://www.streamlive.to/embedplayer.php'

    swf = 'http://player.streamlive.to/streamlive-plugin.swf'
    return rtmp + ' playPath=' + filename + ' swfUrl=' + swf + ' swfVfy=true live=true token=' + token + ' app=' + app + ' pageUrl=' + url


def embedrtmp(embedcode, url):
    rtmp = re.search('<param name="flashvars" value="&streamer=(.+?)&file', embedcode).group(1)
    app = re.search('rtmp://[\.\w:]*/([^\s]+)', rtmp).group(1)
    swf = re.search('type="application/x-shockwave-flash" data="(.+?)"', embedcode).group(1)
    channel = par
    return rtmp + ' app=' + app + ' playpath=' + channel + ' swfUrl=http://www.tgun.tv' + swf + ' pageUrl=' + url + ' live=true'


def castto(embedcode, url):
    data = {'Referer': url}
    
    parms = re.search('<script type="text/javascript"> fid="(.+?)"; v_width=.+; .+ src=".+castto.+"></script>', embedcode)
    
    link = 'http://static.castto.me/embed.php?channel=%s' % parms.group(1)
    html = get_url(link, headers=data)
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    playPath = re.search('\'file\',\'(.+?)\'', html).group(1)
    streamer = re.search('\'streamer\',\'(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' pageURL=', 'http://static.castto.me',
       ' swfUrl=', swfPlayer,
       ' live=true',
       ' token=#ed%h0#w@1'])
    addon.log(rtmpUrl)
    return rtmpUrl


def owncast(embedcode, url):
    data = {'Referer': url}
    
    parms = re.search('<script type="text/javascript"> fid="(.+?)"; v_width=(.+?); v_height=(.+?);</script><script type="text/javascript" src="(.+?)"></script>', embedcode)
    
    link = 'http://www.owncast.me/embed.php?channel=%s&vw=%s&vh=%s&domain=www.tgun.tv' % (parms.group(1), parms.group(2), parms.group(3))
    #html = net.http_GET(link, data).content
    referrer = url
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = urllib2.Request(link)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Referer', referrer)
    response = urllib2.urlopen(req)
    html = response.read()
    swfPlayer = re.search('SWFObject\(\'(.+?)\'', html).group(1)
    rtmpjson = re.search('getJSON\("(.+?)",', html).group(1)
    
    data = {'referer': link}
    rtmplink = net.http_GET(rtmpjson, data).content
    streamer = re.search('"rtmp":"(.+?)"', rtmplink).group(1)
    playPath = re.search('"streamname":"(.+?)"', rtmplink).group(1)
    
    
    if not re.search('http://www.owncast.me', swfPlayer):
        swfPlayer = 'http://www.owncast.me' + swfPlayer
    #playPath = re.search('\'file\',\'(.+?)\'', html).group(1)
    #streamer = re.search('\'streamer\',\'(.+?)\'', html).group(1)
    rtmpUrl = ''.join([streamer,
       ' playpath=', playPath,
       ' pageURL=', link,
       ' swfUrl=', swfPlayer,
       ' live=true'])
    addon.log(rtmpUrl)
    return rtmpUrl


def vaughnlive(embedcode, url):
    headers = {
            'Referer': url, 'Host' : 'vaughnlive.tv'
        }
    
    try:
        vaughn_url = re.search('embed=embed\+\'<iframe src=\"(.+?)\'\+channel\+\'\"', embedcode).group(1) + par
        html = get_url(vaughn_url, headers=headers)

        html = get_url(vaughn_url, headers=headers)
        domain = urlparse(vaughn_url).netloc
              
        #serverlist = re.compile('(\d+\.\d+\.\d+\.\d+\:443)').findall(html)
        #stream_hash=re.search('vsVars.*= "0n0(.*?)"',html).group(1)
        swf_path = re.search('swfobject.embedSWF\("(.+?)",', html).group(1)

        live_tag = 'live'
        if   'instagib.' in domain: live_tag='instagib'
        elif 'vapers.'   in domain: live_tag='vapers'
        elif 'breakers.' in domain: live_tag='breakers'
        
        mvn_url = 'http://mvn.vaughnsoft.net/video/edge/%s_%s' % (domain, par)
        mvn_html = get_url(mvn_url, use_cache=False)
        stream_hash = re.search('mvnkey-(.+)', mvn_html).group(1)
        server = re.search('(.+?);', mvn_html).group(1)
        
        #rtmpUrl = "rtmp://%s/live?%s Playpath=%s_%s swfUrl=http://%s%s live=true pageUrl=http://%s/embed/video/%s?viewers=true&watermark=left&autoplay=true" % (random.choice(serverlist), stream_hash, live_tag, par, domain, swf_path, domain, par)
        rtmpUrl = "rtmp://%s/live App=live?%s Playpath=%s_%s  swfUrl=http://%s%s live=true pageUrl=http://%s/embed/video/%s?viewers=true&watermark=left&autoplay=true" % (server, stream_hash, live_tag, par, domain, swf_path, domain, par)        
        
        addon.log(rtmpUrl)
        return rtmpUrl

    except Exception, e:
        addon.log_error('Failed to resolve Vaughn Live: %s' % e)
        return None

def zerocast(embedcode, url):
    headers = {
            'Referer': url, 'Host' : 'zerocast.in'
        }
    
    try:
        zero_url = re.search('src="(.+?)"></script>', embedcode)
        final_url = url
        if zero_url and re.search('zerocast', zero_url.group(1)):
            html = get_url(zero_url.group(1), headers=headers)
            final_url = re.search('var url = \'(.+?)\';', html).group(1)
            
        html = get_url(final_url, headers=headers)
        
        token_url = re.search('getJSON\("(.+?)",', html).group(1)
        token_html = get_url(token_url, headers=headers)
        token=re.compile('{"token":"(.+?)"}').findall(token_html)[0]
        
        #rtmp = re.search('file: "(.+?)",', html).group(1)
        #playPath = re.search('file\', \'(.+?)\'\);', html).group(1)
        
        file = re.search('file: \' (.+?)\',', html).group(1)
        playPath = re.search('rtmp://[\.\w:]*/.+/([^\s]+)', file).group(1)
        
        rtmpUrl = ''.join(['rtmpe://207.244.74.135:1935/goLive',
        ' playpath=', playPath,
        ' pageURL=', final_url,
        ' swfUrl=', 'http://cdn.zerocast.tv/player/jwplayer.flash.swf',
        ' token=', token,
        ' live=true'])
        
        addon.log(rtmpUrl)
        return rtmpUrl
        
    except Exception, e:
        addon.log_error('Failed to resolve Zerocast: %s' % e)
        raise


def livegome(embedcode, url):
    headers = {
            'Referer': url, 'Host' : 'www.livego.me'
        }
    
    try:
         
        html = get_url(url, headers=headers)
        
        token_url = re.search('getJSON\("(.+?)",', html).group(1)
        token_html = get_url(token_url, headers=headers)
        token=re.compile('{"token":"(.+?)"}').findall(token_html)[0]
        
        rtmp = re.search('file: \'(.+?)\',', html).group(1)
        playPath = re.search('rtmp://[\.\w:]*/.+/([^\s]+)', rtmp).group(1)
        
        rtmpUrl = ''.join([rtmp,
        ' playpath=', playPath,
        ' pageURL=', url,
        ' swfUrl=', 'http://p.jwpcdn.com/6/8/jwplayer.flash.swf',
        ' token=', token,
        ' live=true'])
        
        addon.log(rtmpUrl)
        return rtmpUrl
        
    except Exception, e:
        addon.log_error('Failed to resolve Livego.me: %s' % e)
        return None
        
def playerindex(embedcode):
    link = re.search('iframe src="(.+?)"', embedcode).group(1)
    link = urllib2.unquote(urllib2.unquote(link))
    addon.log('Retrieving: %s' % link)
    html = get_url('http://www.tgun.tv/shows/' + link)
    return html


def get_embed(html):
    #embedtext = "(<object type=\"application/x-shockwave-flash\"|<!--[0-9]* start embed [0-9]*-->|<!-- BEGIN PLAYER CODE.+?-->|<!-- Begin PLAYER CODE.+?-->|<!--[ ]*START PLAYER CODE [&ac=270 kayakcon11]*-->|)(.+?)<!-- END PLAYER CODE [A-Za-z0-9]*-->"
    embedtext = "</div>(.+?)<!-- start Ad Code 2 -->"
    #embedcode = re.search(embedtext, html, re.DOTALL).group(2)
    embedcode = re.search(embedtext, html, re.DOTALL).group(1)
    #Remove any commented out sources to we don't try to use them
    embedcode = re.sub('(?s)<!--.*?-->', '', embedcode).strip()
    return embedcode


def determine_stream(embedcode, url):
    if re.search('/playerindex[0-9]*.php', html) or re.search('http://www.tgun.tv/embeds2/index[0-9]*.html\?', html):
        addon.log_debug('TGUN Stream')
        stream_url = tgun_stream(embedcode)
    elif re.search('vaughnlive.tv', embedcode):
        addon.log_debug('vaughnlive.tv')
        stream_url = vaughnlive(embedcode, url)
    elif re.search('zerocast.tv', embedcode):
        addon.log_debug('zerocast.tv')
        stream_url = zerocast(embedcode, url)
    elif re.search('livego.me', embedcode):
        addon.log_debug('livego.me')
        stream_url = livegome(embedcode, url)        
    elif re.search('castto', embedcode):
        addon.log_debug('casto')
        stream_url = castto(embedcode, url)
    elif re.search('owncast', embedcode):
        addon.log_debug('owncast')
        stream_url = owncast(embedcode, url)
    elif re.search('sawlive', embedcode):
        addon.log_debug('sawlive')
        stream_url = sawlive(embedcode, url)
    elif re.search('shidurlive', embedcode):
        addon.log_debug('shidurlive')
        stream_url = shidurlive(embedcode, url)       
    elif re.search('streamlive.to', embedcode):
        addon.log_debug('streamlive')
        stream_url = streamlive(embedcode)
    elif re.search('MediaPlayer', embedcode):
        stream_url = mediaplayer(embedcode)
    elif re.search('rtmp', embedcode):
        stream_url = embedrtmp(embedcode, url)
    elif re.search('Ref1=(.+?asf)', embedcode):
        stream_url = re.search('Ref1=(.+?asf)', embedcode).group(1)
    else:
        stream_url = None
    return stream_url

    
def decode_text(s, split_val, added_val, minus_val):
    r = ""
    tmp = s.split(split_val)
    s = urllib.unquote(tmp[0])
    k = urllib.unquote(tmp[1] + added_val)

    i = 0
    for letter in s:
        r = r + chr(int(int(k[i % len(k)]) ^ ord(s[i])) + int(minus_val))
        i = i + 1

    return r


def tgun_stream(html):
 
    try:
        url = re.search('<iframe src="(.+?)\'\+channel\+\'"', html)
        url = url.group(1) + par
        html = get_url(url, headers=headers)
        
        function = urllib.unquote(re.search('eval\(unescape\(\'(.+?)\'\)\);', html).group(1))
        addon.log_debug('TGUN Function: %s' % function)
        split_val = re.search('split\("(.+?)"\);', function)
        added_val = re.search('unescape\(.+ \+ "(.+?)"', function)
        minus_val = re.search('charCodeAt\(i\)\)[\+|-]([\+|-]*[0-9])\);', function)
        
        encoded = re.search("eval\(unescape\(.+?\) \+ '(.+?)'", html).group(1)
        html = decode_text(encoded, split_val.group(1), added_val.group(1), minus_val.group(1))
        addon.log_debug('TGUN Decoded HTML: %s' % html)
        
        swfPlayer = 'http://www.tgun.tv/menus/players/jwplayer/jwplayer.flash.swf'
        streamer = re.search("file: '(.+?)'", html)
        playPath = par
        stream_url = ''.join([streamer.group(1) + par,
                       ' playpath=', playPath,
                       ' pageURL=', url,
                       ' swfUrl=', swfPlayer,
                       ' live=true']) 

        return stream_url
    except:
        raise Exception('Failed to resolve TGUN owned stream')

        
if play:

    try:
    
        #Check for channel name at the end of url
        global par
        par = urlparse(url).query
        
        #Sometimes they pass in the url we want in a url query parm, check first
        r = re.search("((HTTP|http)://.+)", par)
        if r:
            url = r.group(1)

        headers = {
                'Referer': url, 'Host' : 'www.tgun.tv'
            }        

        html = get_url(url, headers=headers)

        #Check for channels that have multiple stream sources
        stream_sources = re.compile('<a style="color: #000000; text-decoration: none;padding:10px; background: #38ACEC" href="#" onClick="Chat=window.open\(\'(.+?)\',\'player\',\'\'\); return false;"><b>(.+?)</b></a>').findall(html)
        
        #Prompt user to select channel stream #
        if stream_sources:
            names = []
            links = []
            for link, name in stream_sources:
                names.append(name)
                links.append(link)
            
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose a video source', names)
            if index >= 0:
                url = links[index]
                par = urlparse(url).query
                if par.startswith('http://'):
                    url = par
                html = get_url(url)

        #Remove any commented out sources to we don't try to use them
        embedcode = re.sub('(?s)<!--.*?-->', '', html).strip()
        #html = re.sub('(?s)<!--.*?-->', '', html).strip()

        if re.search('http://tgun.tv/embed/', embedcode):
            link = re.search('src="(.+?)"', embedcode).group(1)
            embedcode = get_url(link)
            embedcode = re.sub('(?s)<!--.*?-->', '', embedcode).strip()

        stream_url = determine_stream(embedcode, url)
        
        if not stream_url:
            raise Exception('Channel is using an unknown stream type')
            stream_url = None

        #Play the stream
        if stream_url and stream_url <> "Offline":
            addon.resolve_url(stream_url)            
            
    except Exception, e:
        traceback.print_exc()
        Notify('small','TGUN', str(e),'')    

        
def tvchannels(turl = url, tpage = page_num):
    #turl = turl % tpage
    html = get_url(turl)

    #Remove any commented out sources to we don't try to use them
    html = re.sub('(?s)<!--.*?-->', '', html).strip()
    
    match = re.compile('<a Title="(.+?)" href="#" onClick="Chat=window.open\(\'(.+?)\',\'vid_z\',\'\'\); return false;"><img src="(.+?)" border="1" width=[0-9]+ height=[0-9]+ /></a>').findall(html)
    if not match:
        match = re.compile('<a Title=".*" href="(.+?)" target="img_m"><img border="0" src="(.+?)" style="filter:alpha[ \(opacity=50\)]*; -moz-opacity:0.5" onMouseover="lightup\(this, 100\)" onMouseout="lightup\(this, 30\)" width="110" height="80"></a>(.+?)</td>').findall(html)
    for name, link, thumb in match:
        if not re.search('http://', thumb):
            thumb = main_url + thumb
        if re.search('http://www.tgun.tv/menus/players/dlock/playerindex[0-9]*.php', link):
            name = name + '[COLOR blue]*[/COLOR]'
        addon.add_video_item({'mode': 'channel', 'url': link}, {'title': name}, img=thumb)

    
def mainmenu():
    #tvchannels(showlist_url, 1)
    #whatismyip = "http://icanhazip.com/"
    #addon.log(urllib2.urlopen(whatismyip).readlines()[0])
    addon.add_directory({'mode': 'tvchannels', 'url': showlist_url, 'page_num': 1}, {'title': 'Live TV Shows & Movies'}, img=icon_path + 'newtv.png')
    addon.add_directory({'mode': 'classics', 'url': classic_shows_url % 1, 'page_num': 1}, {'title': 'Classic TV Shows'}, img=icon_path + 'retrotv.png')
    addon.add_directory({'mode': 'livetv', 'url': livetv_pages % 1, 'page_num': 1}, {'title': 'Live TV Channels'}, img=icon_path + 'livetv.png')


if mode == 'main':
    mainmenu()


elif mode == 'mainexit':
    sys_exit()
    mainmenu()


elif mode == 'tvchannels':
    tvchannels()


elif mode == 'classics':
    html = get_url(url)

    page = int(page_num)    
    if page > 1:
        addon.add_directory({'mode': 'mainexit'}, {'title': '[COLOR red]Back to Main Menu[/COLOR]'}, img=icon_path + 'back_arrow.png')

    if page < 4:
        page = page +  1
        addon.add_directory({'mode': 'classics', 'url': classic_shows_url % page, 'page_num': page}, {'title': '[COLOR blue]Next Page[/COLOR]'}, img=icon_path + 'next_arrow.png')

    match = re.compile('<a Title="" href="(.+?)" target="img_m"><img border="0" src="(.+?)" style="filter:alpha\(opacity=50\); -moz-opacity:0.5" onMouseover="lightup\(this, 100\)" onMouseout="lightup\(this, 30\)" width="110" height="80"></a>(.+?)</td>').findall(html)
    for link, thumb, name in match:
        if not re.search('http://', thumb):
            thumb = main_url + thumb
        addon.add_video_item({'mode': 'channel', 'url': link}, {'title': name}, img=thumb)


elif mode == 'livetv':
    html = get_url(url)

    page = int(page_num)    
    if page > 1:
        addon.add_directory({'mode': 'mainexit'}, {'title': '[COLOR red]Back to Main Menu[/COLOR]'}, img=icon_path + 'back_arrow.png')

    if page < 4:
        page = page +  1
        addon.add_directory({'mode': 'livetv', 'url': livetv_pages % page, 'page_num': page}, {'title': '[COLOR blue]Next Page[/COLOR]'}, img=icon_path + 'next_arrow.png')

    match = re.compile('<td width="100%" .+? href="(.+?)" target="img_m"><img border="0" src="(.+?)" style=.+?></a>(.+?)</td>').findall(html)
    for link, thumb, name in match:
        if not re.search('http://', thumb):
            thumb = main_url + thumb
        addon.add_video_item({'mode': 'channel', 'url': link}, {'title': name}, img=thumb)

    
elif mode == 'exit':
    sys_exit()


if not play:
    addon.end_of_directory()