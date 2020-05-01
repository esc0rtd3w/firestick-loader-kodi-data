
import re
import os
import sys
import json
import string
import urllib
import urllib2
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import xbmcplugin

addon_id = 'plugin.video.VidTime'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
cookiesfolder=os.path.join(datapath,'Cookies')
try: os.makedirs(cookiesfolder)
except: pass

def OPENURL(url, mobile = False, q = False, verbose = True, timeout = 10, cookie = None, data = None,
            cookiejar = False, log = True, headers = [], type = '',ua = False,setCookie = [],raiseErrors = False,ignore_discard = True):
    import urllib2 
    UserAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    if ua: UserAgent = ua
    try:
        if log:
            xbmc.log("Vidtime-Openurl = " + url)
        if 'afdah.org' in url:
            url = url.replace('https','http')
            import requests
            link = requests.get(url, headers=headers, allow_redirects=False).text
            link = link.encode('ascii', 'ignore').decode('ascii')
        else:
            if cookie and not cookiejar:
                import cookielib
                cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
                cj = cookielib.LWPCookieJar()
                if os.path.exists(cookie_file):
                    try:
                        cj.load(cookie_file,ignore_discard)
                        for c in setCookie:
                            cj.set_cookie(c)
                    except: cj.save(cookie_file,True)
                else: cj.save(cookie_file,True)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            elif cookiejar:
                import cookielib
                cj = cookielib.LWPCookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            else:
                opener = urllib2.build_opener()
            if mobile:
                opener.addheaders = [('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')]
            else:
                opener.addheaders = [('User-Agent', UserAgent)]
            for header in headers:
                opener.addheaders.append(header)
            if data:
                if type == 'json': 
                    import json
                    data = json.dumps(data)
                    opener.addheaders.append(('Content-Type', 'application/json'))
                    headers = dict(headers)
                    headers.update({'Content-Type': 'application/json'})
                    req = urllib2.Request(url, data=data,headers=headers)
                    response = opener.open(req)
                else:
                    data = urllib.urlencode(data)
                    response = opener.open(url, data, timeout)
            else:
                response = opener.open(url, data, timeout)
            if cookie and not cookiejar:
                cj.save(cookie_file,ignore_discard)
            opener.close()
            link=response.read()
            response.close()
        #link = net(UserAgent).http_GET(url).content
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','x').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        if q: q.put(link)
        return link
    except Exception as e:
        if raiseErrors: raise
        if verbose:
            from urlparse import urlparse
            host = urlparse(url).hostname.replace('www.','').partition('.')[0]
            xbmc.executebuiltin("XBMC.Notification(Sorry!,"+host.title()+" Website is Down,3000," ")")
        xbmc.log('***********Website Error: '+str(e)+'**************', xbmc.LOGERROR)
        xbmc.log('***********Url: '+url+' **************', xbmc.LOGERROR)
        import traceback
        traceback.print_exc()
        try: link = e.read()
        except: link ='website down'
        if q: q.put(link)
        return link
    
def getFile(path,default = None):
    content = default
    if os.path.exists(path):
        try: content = open(path).read()
        except: pass
    return content

def resolve(url):
    try:
        import json
        xbmc.log('MashUp MailRU - Requesting GET URL: %s' % url)
        urllist=[]
        quaList=[]
        m = re.search('my.mail.ru/(.+?)/(.+?)/video/_myvideo/(\d+).html',url,re.I)
        if m:
                path=m.group(1)
                user=m.group(2)
                file_id=m.group(3)
                link='http://videoapi.my.mail.ru/videos/'+path+'/'+user+'/_myvideo/'+file_id+'.json?ver=0.2.60'
                xbmc.log('MashUp MailRU - Requesting GET URL: %s' % link)
                link=OPENURL(link,cookie="mailru")
        if link:
                cookie_file = os.path.join(os.path.join(datapath,'Cookies'), 'mailru.cookies')
                cookie = getFile(cookie_file)
                vidkey = re.findall('(video_key=[^;]+?);',cookie)
                fields = json.loads(link)
                videos = fields["videos"]
                for video in reversed(videos):
                    videourl = video['url'] + "|Cookie=" + vidkey[0]
                    urllist.append(videourl)
                    quaList.append("MAIL.RU " + video['key'])
        dialog2 = xbmcgui.Dialog()
        ret = dialog2.select('[COLOR=FF67cc33][B]Select Quality[/COLOR][/B]',quaList)
        if ret == -1:
            return False
        stream_url = urllist[ret]
        stream_url = stream_url.replace("\/",'/')
        return stream_url
    except Exception, e:
        raise ResolverError(str(e),"MailRu")
        xbmc.executebuiltin('[B][COLOR white]MailRU[/COLOR][/B]','[COLOR red]%s[/COLOR]' % e, 5000, 'error')
        print "error"
        return False



