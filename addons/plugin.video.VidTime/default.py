# -*- coding: utf-8 -*-
# VinMan_JSV 2016

import os,re,sys,urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,xbmc,urlparse,cookielib,base64
from resources.lib.modules import client
from resources.lib.modules import cloudflare
from resources.lib.modules import control
from resources.lib.modules import cache
from resources.lib.modules.net import Net as net
import requests
thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
ADDON = xbmcaddon.Addon(id='plugin.video.VidTime')
path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/'))
usdata=xbmc.translatePath(os.path.join('special://userdata/addon_data/plugin.video.VidTime/'))
mediaPath = path +"resources/media/"
fanart = 'http://s22.postimg.org/84knawrzl/fanart.png'
icon = (path + 'icon.png')
SPORT = 'http://s28.postimg.org/70srmubcd/sport.png'
ROCK = 'http://s16.postimg.org/owjqyjgt1/Rock.png'
VidToon = 'http://s9.postimg.org/syfmnrfn3/Vid_Toons.png'
CONCERT = 'http://s16.postimg.org/48l3jsvkl/Rock_Concert.png'
USTV = 'http://s18.postimg.org/r80qgabnt/USTV.png'
pager = '1'
plot = None
cj = cookielib.LWPCookieJar()
cookiepath = (usdata+'cookies.lwp')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1')]

def TEST():
    return 

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
        
def choose():
    try:
        onetime = OPEN_URL(english('Vm0weE1GWXhWWGhWV0doV1lteEtWMWx0ZUVJsV28aN10V1ZteFZVbTFHVjFac2NIbFdNakZIWVdzeFdHVkdiR0ZXVm5Cb1dXdGFZV1JHVm5OWGJGcE9ZV3hhZVZkV1dtRlRiVkYzVGxaa2FWSnRVbkJXYTFaaFRXeGtWMXBFVWxWTlZXdzBWMnRvUjFZeVNrZFhiRkpXWWtkb1JGWkdXbXRYVjA1R1drZHdUbFl4U2tsV2JHTXhWakZhU0ZOc2FHeFNiRXBXVm01d1YyUldVbGhsUjNScVlrWndlVlJzVlRGV01WcEhWMnR3VjFaRmJ6Qlpha3BHWlZaYWMxWnRiRlJTVm5Cb1YxZDBZVmxXYkZkalJtaHNVbTFTVkZSWGRHRlRSbHBJVFZSU1YwMUVSbGRaTUZwM1ZqSktXV0ZHVG1GU1JWcEVWbGQ0UTFaVk1VVk5SREE5L1ZtMHdkMlF5VVhsVldHeFdWMGQ0VjFZd1pEUlhSbXhWVTIwNVYwMVdiRE5YYTJNMVZqSktSMkpFVGxoaE1VcFVWbXBCZUZZeVNrVlViR2hvVFdzd2VGWnRjRXRUTVU1SVZtdFdVbUpWV2xSV2FrcHZaVlphZEUxVVVsUk5hekUxVmtkMFYxVnRTa2RYYkdoYVlrWldNMXBWV21Ga1IwNUdVMjE0VTJKV1NrcFdiVEV3VmpGV2RGTnJiRkpoZW14V1ZtdFdTMVJHVlhoWGJYUlhUVmhDUmxaWGVIZFdNREZGVWxSQ1YwMXVVblpXYWtwSFl6Rk9kVlZ0YUZObGJYaFhWbTB4TkZsVk1IaFhiazVZWWxoU1dGUldXbmROUmxaMFpVWk9WV0pWV1RKVmJGSkRWakF4ZFZWdVdsZGhhM0JJVm1wR1QyUldWbk5YYld4b1RVaENXVll4WkRSaU1WVjNUVWhvVjFkSGFGbFpiR2hUVjBaU1YxcEVRazlpUjNoWFZqSjRUMVpYU2tkalJscFhZbGhvZWxacVJtRk9iRVpaWVVaa1UxSllRa2xXVjNCSFZESlNWMVp1VGxoaVYzaFVWRmN4YjFkR1duUk5WRUpYVFd4R05WWlhOVTloYkVwMFZXeHNXbUpIYUZSV01GcFRWakZ3UlZGck9XbFNNMmhZVm1wS05GUXhXbGhUYTJScVVteHdXRmxzYUZOTk1WcHhVMnQwVkZKc1dscFhhMXByWVVkRmVHTkhhRmhpUm5Cb1ZrUktUMk15VGtaYVIyaFRUVzVvVlZaR1kzaGlNV1J6VjFob1lWSkdTbkJVVmxwWFRURlNWbUZIT1ZoU2JWSkpXVlZhYzFkdFNraGhSbEpYVFVad1ZGWnFSbXRrUmtwMFpVWmthVkpzYTNoV2ExcGhWVEZWZUZkdVNrNVhSWEJ4VlcweGIxWXhVbGhPVms1T1RWWndlRlV5ZERCV01WcHlZMFp3V0dFeGNISlpWV1JHWlVkT1IySkdhR2hOVm5CdlZtdFNTMVF5VFhsVWExcGhVakpvVkZSWE1XOWxiR1JZWlVjNWFVMVhVbnBXTVdodldWWktSMU51UWxWV2JIQllWRlJHVTFadFJraFBWbWhUVFVoQ05WWkhlR0ZqTVdSMFUydGtXR0pYYUdGVVZscDNaV3hyZVdWSVpGTk5Wa3A1Vkd4YVQyRlhSWGRqUld4WFlsaENURlJyV2xKbFJtUnpZVVpTYUUxc1NuaFdWM1JYV1ZaWmVGZHVSbFZoTURWWlZXMTRkMlZHVm5Sa1NHUnBVakJ3VjFZeWRITlhiRnBYWTBoS1dsWlhVa2RhVldSUFUwVTVWMXBHWkZOV1dFSjJWbTEwVTFNeFVYbFZhMlJWWW10d2FGVnRlRXRqUmxweFZHMDVhMkpHY0VoV2JUQTFWV3N4V0ZWc2FGZE5WMmgyVjFaYVMxSnNUblJTYkdSb1lURndTVlpIZEdGWGJWWklVbXRvVUZadFVuQldiR2hEVTJ4YWMxcEVVbXBOVjFJd1ZUSjBhMWRIU2xoaFJtaFZWbFp3TTFwWGVISmxWMVpKV2taT1RsWnJiM2RYYkZaaFlUSkdWMU5ZY0ZwTk1taFlWRmMxYjFkR1duRlNiRXBzVW0xU1dsZHJWVEZYUmtwWlVXeHNXRlp0VWpaVVZscHpWakZXYzFkc2FHbGlWa3BaVmxjeE5HUXlWa2RXYmxKT1ZsZFNXRlJWVWtkbFZsSnpWbTA1VjAxVmJ6SlZiWFJ2VmpGYVJsZHJlRmRoYTNCUVZXMTRZV014Y0VoaVJrNU9WbFpaZWxadGVHRlZNVWw0WWtaa1dHSnJjRTlXYlhoM1YwWnNXV05HWkZkU2JGcDVWbTEwWVZReFZsVk5SR3M5'))
        
        cache.TEST2(str(onetime))
    except:
        pass
    
    try:
        fanarts = [i for i in re.findall('<pre>(.+?)</pre>',str(onetime))]
        with open(path+str(re.findall('VinManJSV_(.+?)_VinManJSV',str(onetime))[0]),'r') as menus:backdrops = re.findall('"(.+?)"', menus.readlines()[3])[0]
        for item in fanarts:
            if item == backdrops:
                start = item
            else:
                pass      
    except:
        pass
    try:
        if start:
            onetime = OPEN_URL(english('Vm0xMFYxVXhVWGhWYmxKV1ltczFjVlJsV24aN1ZzWkRSVk1XeHpZVVpPV2xac2JETlhhMVV4Vkd4YWMxSnFVbGRXTTFGM1dWVmFTMVpYU2tkWGJGcE9ZV3RGZUZkWGRHRlRiVlpIVkc1R1YySkdXbFJWYkZwM1RXeGFjbHBFVWxaTlZYQjZWakkxVDJGV1NuUlZiRkphVmtVMVJGVnJXbUZTYkd3MlVtMXNUbUpGY0VwV1ZFb3dWakZXUjFwRmFHeFNNRnBZVkZWa1UxUXhVbk5YYm1SVFlsVmFSMXBGVlRGV01rcHlVMnhTVjFaV2NGTmFSRVpEVld4Q1ZVMUVNRDA9L1ZtMHdkMlF5VVhsVldHeFhZVEpvVjFZd1pHOVdiRmwzV2tSU1YwMVdiRE5YYTJNMVZqSktTR1ZFUW1GU1YyaHlWbTE0UzJNeVRrVlJiRlpYWWxVd2VGWnRjRUpsUm1SSVZtdFdVbUpJUWs5VVZFSkxVMVprVjFwRVVscFdNREUwVjJ0b1YyRnNTblJoUnpsVlZteGFNMVpzV210V01WcDBVbXhTVG1GNlJUQldNblJ2VmpKR1YxTnVVbFppYTBwWFdXeG9VMDB4VlhoWGJYUlhUVmQwTmxsVldsTlViRnBWVm14c1YxWjZRWGhXUkVwSFVqRk9kVlZzV21sU01taFhWbTEwVjJReVVuTmpSbVJZWWxoU1dGUldaREJPYkd4V1YyeE9WV0pHY0ZaV2JYUjNWakpLU0ZWWVpGZGhhMXBoV2xaYVQyTnNjRWRoUjJ4VFRXMW9XbFl4WkRSaU1WVjNUVWhvV0ZkSGFGbFpiR2hUVjBaU1YxZHRSbXhXYkZZMVZGWlNVMVpyTVhKalJtaFdUVzVTTTFacVNrdFdWa3BaV2taa2FHRXhjRmxYYTFaaFZESk9jMk5GWkdoU01taHpXV3hvYjFkc1dYaGFSRkpwVFZaV00xUlZhRzlYUjBweVRsWnNXbUpHV21oWk1WcHpZMnh3UjFSck5WTmlhMHBJVm1wS05GUXhXbGhUYTJScVVrVmFWMVpxVGtOWFJscHhVbXR3YkdKVldrbFpWVnByWVVkRmVHTkhPVmRXUlVwb1ZrUktUMlJHVG5KYVJsSnBWak5vZGxaR1ZtOVJNV1JYVjFob1lWSkZTbUZXYWtaSFRrWlplR0ZIT1ZkaVZYQkpWbGQ0YzFkdFNrZFhiV2hYVFVad2Vsa3llSGRTTVZKMFpVWmthVkl6WTNoV01uaFhWakZSZUZkWVpFNVhSWEJZV1Zkek1WbFdVbFpYYm1SWFVteHdlRlZ0TVVkV01ERnlUbFZvVjFKNlJraFdWRVpMVmpKT1JsWnNaR2xTTVVWM1ZsWlNSMWxXV25KTlZscFhZWHBXVkZWclZrWk9VVDA5'))
            NEWWINDOW(onetime)
    except:
        NEWWINDOW(onetime)
    xbmcplugin.endOfDirectory(thisPlugin)
    
def NEWWINDOW(onetime):
    
    stuff = re.compile('<window>(.+?)</window><base>(.+?)</base><thumbnail>(.+?)</thumbnail>').findall(str(onetime))
    for name, base, thumb in stuff:
        try:
            test = english(base)
            if str(test) != "None":
                base = str(test)
            else:
                pass
        except:
            pass
        
        if not ('http') in base and not base == " ":
            url = build_url({'mode': str(base), 'icon': thumb})
        else:
            url =build_url({'mode': 'XML', 'name':name, 'base': str(base)})        
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=thumb)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                   listitem=li, isFolder=True)
    return
def english(final):
    try:
        x = "MlVPdKNBjIuHvGtF1ocXdEasWZaSeFbNyRtHmJ"
        y =":/."
        fget = x[-1]+x[-11].lower()+x[2]
        rget = x[-12]+x[6]+x[16] 
        this = fget+'.+?'+rget
        getter = re.findall(this,final)[0]
        stage = int(final.index(getter))/5
        work = base64.b64decode(str(final.replace(getter,''))).split('/')
        Solve = True
        S = 1
        while Solve is True:        
            if S<= stage*2:first = base64.b64decode(work[1])
            if S<= stage:sec = base64.b64decode(work[0])
            S = S + 1
            if not S<= stage*2 and not S<= stage: Solve = False
            work =[sec,first]
        answ = work[1]+work[0]
        if answ.startswith (x[-5].lower()+x[-10]):
            begin = (x[-3].lower()+(x[-4]*2)+x[3].lower()+y[0:2]+y[1]+x[7].lower())
            ender = (x[-10]+x[-5].lower())
            killit = (x[-5].lower()+x[-10]+x[-4]+x[-12].lower()+x[-5].lower()+x[4]+x[-11].lower()+x[-3].lower())
            mid = y[2]+x[1]+x[-6]
            url = answ.replace(killit,begin).replace(ender,mid)
        elif answ.startswith ('rtmp') or answ.startswith ('rtsp') or answ.startswith ('plugin'):url = answ
        elif answ.startswith (x[-3].lower()+(x[-4]*2)):url = answ
        elif answ.startswith (x[13].lower()+(x[17]*2)+x[4]):
            killit = (x[13].lower()+(x[17]*2)+x[4])
            begin = (x[-3].lower()+(x[-4]*2)+x[3].lower()+x[-15]+y[0:2]+y[1])
            url = answ.replace(killit,begin)
        else:
            pass
        url = url.replace('/{3,}','//').replace('  ',' ').encode('utf-8')
        return url
        
    except:
        return None

    
def OPEN_URL(url,headers=False):
    req = urllib2.Request(url)
    if headers:            
        req.add_header('User-Agent',headers['User-Agent'])
        req.add_header('Referer', headers['Referer'])
        req.add_header('Accept', headers['Accept'])
    else:
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    onetime=response.read()
    response.close()
    onetime = onetime.replace('\n','').replace('\r','')  
    return onetime

def addDirItem(title,icon,fanart,url):
    listitem =xbmcgui.ListItem (title,'','',thumbnailImage=icon)
    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                listitem=listitem)
def endDir():
    xbmcplugin.endOfDirectory(thisPlugin)
    
def TIMESHIFT():
    from datetime import datetime
    sitetime = int(datetime.utcnow().time().hour)+2
    localt = int(datetime.now().time().hour)
    diff = sitetime - localt
    return diff

if mode is None:
    choose()

elif mode[0] == "XML":
    name = args['name'][0]
    if ('Hockey') in name:
        line99 = "If you continue, VidTime will modify your system." 
        line100 = "It redirects nhl.com to a system that allows playable streams."
        line101 = "This is necessary to make hockey work. Click No if you do not want this modification made."        
        i = xbmcgui.Dialog().yesno(addonname, line99, line100, line101)
        if i == 1:
            try:
                xbmc.executebuiltin('RunScript(special://home/addons/plugin.video.VidTime/HOSTS.py)')
            except:
                pass
        else:
            pass   
    base = args['base'][0]
    onetime = OPEN_URL(base)
    try:
        fanart = re.findall('<fanart>(.+?)</fanart>',str(onetime))[0]
    except:
        pass
    if ('<window>') in str(onetime):NEWWINDOW(onetime)
    stuff = re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(str(onetime))
    
    for title, url, icon in stuff:
        if not ('http') in url and not ('plugin') in url and not ('rtmp') in url and not ('rstp') in url and not ('base64') in url and len(url) > 2:
            url = english(url)
        if ('base64') in url:
            url = base64.b64decode(url[8:-1])
        if ('sdw-net') in url or ('shadow-net') in url:
            url = build_url({'mode': 'shadow', 'name':title, 'icon':icon, 'url':url})    
        if ('youtube') in url and not 'plugin' in url:
            url = build_url({'mode': 'YouTube', 'name':title, 'icon':icon, 'url':url})
        if ('sawlive') in url:
            url = build_url({'mode': 'sawlive', 'name':title, 'icon':icon, 'url':url})
        if ('p2pcast') in url:
            url = build_url({'mode': 'P2P', 'name':title, 'icon':icon, 'url':url})
        if ('t-tv.org') in url:
            url = build_url({'mode': 'acestream', 'name':title, 'icon':icon, 'url':url})
        if ('liveonlinetv') in url:
            url = build_url({'mode': 'ONTV', 'name':title, 'icon':icon, 'url':url})
        if ('mail.ru') in url:
            url = build_url({'mode': 'MAILRU', 'name':title, 'icon':icon, 'url':url})
        if ('vaughnlive.tv') in url:
            url = build_url({'mode': 'VAUGHNLIVE', 'name':title, 'icon':icon, 'url':url})
        if ('thechive.com') in url:
            url = build_url({'mode': 'THECHIVE', 'name':title, 'icon':icon, 'url':url})
        if ('arconaitv.me') in url:
            url = build_url({'mode': 'ARCON', 'name':title, 'icon':icon, 'url':url})
        if ('redbull.com') in url:
            url = build_url({'mode': 'REDBULL', 'name':title, 'icon':icon, 'url':url})
        if ('nfl-watch.com') in url:
            url = build_url({'mode': 'NFLWATCH', 'name':title, 'icon':icon, 'url':url})
        if ('sublink') in url:
            links = re.findall('<sublink>(.+?)</sublink>',str(url))
            for item in links:
                url = item
                addDirItem(title,icon,fanart,url)        
        else:
            try:
                url = urlresolver.HostedMediaFile(url).resolve()
                addDirItem(title,icon,fanart,url)
            except:
                pass
        addDirItem(title,icon,fanart,url)    
    endDir()
    
elif mode[0] =="YouTube":
    url = args['url'][0]
    name = args['name'][0]
    thumbnailImage = args['icon'][0]
    try:
        try:
            url = 'plugin://plugin.video.youtube/play/?video_id=' + str(url.split('v=')[1])
        except:
            url = xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+ url.split('v=')[1]+')')
            pass
    except:
        pass
    listitem =xbmcgui.ListItem(name, '','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url, listitem)

elif mode[0] =="shadow":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import shadownet
    setter = shadownet.resolve(url)
    listitem = xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(str(setter),listitem)

elif mode[0] =="USTVNOW":
    from resources.lib.indexers import ustvnow
    ustvnow.CHList(fanart)

elif mode[0] =="CHPLAY":
    url = args['url'][0]
    from resources.lib.indexers import ustvnow
    ustvnow.CHPlay(url)

elif mode[0] == "REDBULL":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    link=OPEN_URL(url)
    vid_id= re.findall("data-video-id='([^']+)'",link)
    if vid_id:
        vid_id= vid_id[0]
        account= re.findall("data-account='([^']+)'",link)[0]
        url2='https://edge.api.brightcove.com/playback/v1/accounts/'+account+'/videos/'+vid_id
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36','Referer':url,'Accept':'application/json;pk=BCpkADawqM04GwfHVvRSv5kMqi1EoG_1z5mEyoDfMLer8s8rVN7jmoshU1T2q6oix3bMPtZBvpZeXjx6nPXxU5YsbnPRo9ghJKq7sIdVzHdxwMXJJUFgwsZXZBZPv0yle1JS341r7VHAEFL_'}
        link=OPEN_URL(url2,headers=headers)
        import json
        data=json.loads(link)
        data=data["id"]
        stream='http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId='+data
        listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(stream,listitem)
    else:
        xbmc.executebuiltin("XBMC.Notification(Link Down!, ,3000,"+icon+")")
    

elif mode[0] == "NFLWATCH":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    result = client.request(url, referer=url)
    link = re.findall('<iframe src="([^"]+)"',result)[0]
    link = 'http://www.nfl-watch.com'+link
    result = client.request(link, referer=link)
    link = re.findall('<iframe src="([^"]+)"',result)[0]
    result = client.request(link, referer=link)
    try: stream = re.findall('"([^"]+m3u8)"',result)[0]
    except:stream = re.findall('file: "([^"]+)"',result)[0]
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)
    
elif mode[0] == "MAILRU":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import mailru
    stream = mailru.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "THECHIVE":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    link=OPEN_URL(url)
    match=re.search('''<meta name="twitter:player" content="https://cdnapi.kaltura.com/p/(.+?)/sp/(.+?)/embedIframeJs/uiconf_id/.+?/partner_id/.+?iframeembed=true&amp;playerId=kaltura_player_.+?&amp;entry_id=(.+?)" />''',link)
    if match:
        p=match.group(1)
        sp=match.group(2)
        entryId=match.group(3)
        stream = 'http://cdnapi.kaltura.com/p/'+p+'/sp/'+sp+'/playManifest/entryId/'+entryId+'/format/applehttp/protocol/http/a.m3u8'
    else:
        match=re.findall('''src="https://www.youtube.com/embed/(.+?)"''',link)[0]
        try:
            stream = 'plugin://plugin.video.youtube/play/?video_id=' + str(match.split('?feature')[0])
        except:
            stream = xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+ match.split('?feature')[1]+')')
            pass
    xbmc.log('HDH '+str(match))
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "VAUGHNLIVE":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import vaughnlive
    stream = vaughnlive.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "ARCON":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    post = {'submit':'Continue','f_url':url,'dataSource':'free_seo_tools'}
    headers = {'Referer': 'https://northcutt.com/tools/free-seo-tools/source-code-viewer/'}
    result = net().http_POST('https://northcutt.com/tools/free-seo-tools/source-code-viewer/', post, headers=headers).content
    try:stream=re.findall('hostname=www.arconaitv.me&url=(.+?)&callback',result)[0]
    except:stream=re.findall('<source src="([^"]+)" type="',result)[0]
    stream += '|X-Requested-With=ShockwaveFlash%2F21.0.0.242&User-agent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+WOW64%3B+Trident%2F7.0%3B+rv%3A11.0%29+like+Gecko'
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "P2P":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import p2pcast
    stream = p2pcast.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "sawlive":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import sawlive
    stream = sawlive.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "VT SPORTS":
    fanart = 'http://s18.postimg.org/yehmbqqy1/d0i0w_desktop_2418840_1920x1080.jpg'
    icon = args['icon'][0]
    url = 'http://www.wiz1.net'
    a = requests.get(url+'/schedule/')
    ans = a.text
    page = re.findall('iframe src="(.+?)"',ans)[0]
    game_page = requests.get(url+page)
    a =game_page.text
    b = a.split('<hr>')
    sports = re.compile('<a href="(.+?)" target="(.+?)">(.+?)</a>').findall(b[0])

    for url, blank, name in sports:
        name = name
        url =  url.replace('wiz1.net/','www.wiz1.net/watch')
        url = build_url({'mode': 'wiz1', 'name':name, 'icon':icon, 'url':url})
        addDirItem(name,icon,fanart,url)
        
    burl = 'http://www.ibrod.tv/index.html'
    req = cloudflare.request(burl)
    heading = client.parseDOM(req, 'a', attrs={'title':'Watch UK TV Online'})[0]
    slist = req.split(str(heading))[1].split('a class')[0]
    title = re.findall('title="(.+?)"',str(slist))
    turl = re.findall('href="(.+?)"',str(slist))
    joint = zip(title,turl)
    for title,turl in joint:
        title = title.replace('Watch ','').replace('Online','').upper()
        turl = 'http://www.ibrod.tv/'+str(turl)
        url = build_url({'mode': 'UKSPORT', 'name':title, 'icon':icon, 'url':turl})
        addDirItem(title,icon,fanart,url)
        
    channels = re.compile('(\d+?:\d+? )<font color=".+?"><b>(.+?)</b></font>(.+?)<a href="(.+?)" target=".+?">(.+?)<').findall(a)   
    for time, sport, detail, url, chan in channels:
        times = time.split(':')
        if times[0][0]=='0':
            if 0 <= int(times[0][1]) <= 9:
                stimes = int(times[0][1])
                time = str(int(stimes)- TIMESHIFT())+':'+str(times[1])
        else:
            time = str(int(times[0])- TIMESHIFT())+':'+str(times[1])
        newday = int(times[0]) - TIMESHIFT()
        if int(newday) >= 24:time = str(int(newday)-24)+":"+str(times[1])
        if ('-') in str(time):time = str(int(str(time).split(':')[0])+24)+':'+str(times[1])
        name = str(time) +' '+sport+'-'+detail[1:]
        url = url.replace('wiz','www.wiz').replace('annel','')+'?referer'+str(url)
        url = build_url({'mode': 'wiz1', 'name':name, 'icon':icon, 'url':url})
        addDirItem(name,icon,fanart,url)                            
    endDir()   

elif mode[0] =="wiz1":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    site_url = cloudflare.request(url)                      
    url = re.findall('src="(.+?sawlive.+?)"',str(site_url))[0]
    from resources.lib.resolvers import sawlive
    stream = sawlive.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)
    
elif mode[0] =="UKSPORT":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    req = cloudflare.request(str(url))
    murl = re.findall('iframe .+? src="(.+?)"',str(req))[0]
    req = cloudflare.request(str(murl))
    url = re.findall('src="(http://mipl.+?)"',str(req))[0]
    url =url.encode('utf-8')
    from resources.lib.resolvers import miplayer
    url = miplayer.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(str(url),listitem)

elif mode[0]=="ACETV":
    murl = 'http://t-tv.org'
    req = client.request(murl)
    chunk = client.parseDOM(str(req), 'div', attrs={'id':'channels'})
    chunk = re.findall('<a href=(.+?)</a>',str(chunk))
    for item in chunk:
        urls = re.findall('"(/\?channel.+?)".+?data-favid="(.+?)"', str(item))
        try:
            icon = re.findall('src="(.+?)"',str(item))[0]
            icon = str(murl)+str(icon)+'?raw=true'
        except:
            icon = 'https://cdn3.iconfinder.com/data/icons/abstract-1/512/no_image-512.png'
        url = str(murl)+str(urls[0][0])
        name = str(urls[0][1]).replace('-',' ').upper()
        url = build_url({'mode': 'acestream', 'name':name, 'icon':icon, 'url':url})
        addDirItem(name,icon,fanart,url)
    endDir()
    
elif mode[0]=="acestream":
    url = args['url'][0]
    name = args['name'][0].upper()
    thumbnailImage = args['icon'][0]
    req = client.request(url)
    url = re.findall("var id = '(acestream://.+?)'",str(req))[0]
    url = str(url)+'&name='+str(name).replace(' ','+').encode('utf-8')
    url = xbmc.executebuiltin('PlayMedia(plugin://program.plexus/?mode=1&url='+str(url)+')')

elif mode[0]=="ONTV":
    url = args['url'][0]
    url = url.split('info/')[1]
    name = args['name'][0].upper()
    thumbnailImage = args['icon'][0]
    headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
    site_url = urllib2.Request('http://liveonlinetv247.info/embed/'+str(url),headers=headers)
    b = urllib2.urlopen(site_url)
    a =b.read()
    b.close()
    stream = re.findall('application/x-mpegurl" src="(.+?)"',a)[0]
    stream = str(stream)+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
    listitem =xbmcgui.ListItem (name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(str(stream),listitem)
    
elif mode[0] =="NMR":
    no_end = True
    
    try:
        pc = int(args['c'][0])
    except:
        pc = 1
    c = pc
    #while c in range(pc,pc+4): 
    url = 'http://vumoo.at/videos/category/new-releases/?page='+str(c)
    try:
        site = cloudflare.request(url)
    except:
        no_end = False
        
    REQ = client.parseDOM(site, 'section', attrs={'class':'row-fluid'})
    movie = client.parseDOM(REQ, 'a', ret='href')
    names = client.parseDOM(REQ, 'a', ret='alt')
    icons = client.parseDOM(REQ, 'img', ret='src')
    urls =[]
    for i in movie: 
        if i.startswith('/'):
            urls.append(i)
        else:
            pass   
    list = zip(names,urls,icons)
    c = c + 1
    for name,url,icon in list:
        name = '[B]'+name+'[/B]'
        name = name.upper().encode('utf-8')
        
        url = build_url({'mode': 'vumoo', 'name':name, 'icon':icon, 'url':url})
        addDirItem(name,icon,fanart,url)
    if no_end:
        url = build_url({'mode': 'NMR', 'c': str(c)})
        li = xbmcgui.ListItem('[B][I]NEXT[/I][/B]',iconImage=icon) 
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                    listitem=li, isFolder=True)   
    endDir()
        
elif mode[0] =="vumoo":
    url = args['url'][0]
    name = args['name'][0]
    thumbnailImage = args['icon'][0]
    page = cloudflare.request('http://vumoo.at'+str(url))
    [url for url in client.parseDOM(page, 'iframe', ret='src') if ('openload') in url]
    import urlresolver
    url = urlresolver.HostedMediaFile(url).resolve() 
    url = url.encode('utf-8')
    listitem =xbmcgui.ListItem (name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url,listitem)
    
elif mode[0] =="USTV RIGHT NOW":
    fanart = 'https://images3.alphacoders.com/799/79955.jpg'
    drop = urllib2.urlopen(english('Vm10V1UxUXhVblJWYmxKVFlUSJsV20aN1m9WbGxzYUVOVlJsVjNWbTFHVGxac1NqQlpNRnBoVkdzeFdWRnNiRmhYU0VKRVdWUkdTbVZYVWtWWGJGWlRVbFJXV1Zkc1kzaFZNVTVYV2toV1YySlZXbGxWYWtFd1pVWmtjMVp0Y0d4U01ERTBWVlpvZDFaSFNsaGhTRXBoVmpOQ1IxcEVSbkpsVlRWWFdrZHNVbFpFUVRVPS9WbTB3ZDJReVZraFZXR2hWVjBkNFYxWXdaRzlXYkd4MFpFaGtWbEpzY0RCVVZtTTFWakF4V0dWRVFscE5NMEpJV1ZkNFlXTXhaSFZqUm1ob1RWVndWVmRXVm1GVE1rMTRXa2hXYVZKdFVuQlZiWFIzVTFaa1Yxa3phRlJOVlRWWVZXMDFUMkZHU25SVmJHaFZWa1Z3ZGxwV1dtdFdNV3Q2WVVaU1RsWlVWa3BXYkdRd1ZqRlplVk5yWkZoaVIyaFlXV3hvVTAweFdYaFhiWFJYVFZaYWVWVXlNVFJWTWtwWFUydHdWMkpVUlhkV2FrWlhaRVpPY2xwR2FHaGxiWGhaVjFkNGIxVXdNSGhYYms1WVlsVmFjVmxyWkZOTlJuQkdWMnhPVldKR2NERlZWM0JYVmpGSmVtRkhhRmRoYTFwb1ZUQmFUMk50U2tkVGJXeG9UVWhDV1ZZeFpEQlpWMUY0VjFob1ZtSkhVbGxaYkZaaFYwWnNjbHBHVG14V2JHdzFXbFZXVDFZd01YSldhazVhVFVad1ZGWnFSbUZXTWs1SFZHMUdVMUpXY0VWV2JHUTBVVEZhVmsxVlZrNVNSRUU1'))
    channels= drop.readlines()
    drop.close()
    site = urllib2.urlopen('http://m.ustvnow.com/iphone/1/live/playingnow')
    playing = site.readlines()
    site.close()
    now_playing = re.findall('class="nowplaying" valign="top">(.+?)<',str(playing))
    new_format = zip(channels,now_playing)
    for c,i in new_format:
        part = c.split(' : ')
        title = part[0]
        title = '[COLOR white]'+str(title)+'[/COLOR]  '+str(i).replace('\\','').replace('amp;','').upper()
        url = part[1]
        icon = part[2][:-2]
        addDirItem('[B]'+title+'[/B]',str(icon),fanart,url)
    endDir()
    
elif mode[0] =="VIDTOONS":
    from resources.lib.indexers import vidtoons
    vidtoons.VidToon()
    
elif mode[0] =="VCartoonCraze":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCartoonCraze(image,fanart)
    
elif mode[0] =="VAnime":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAnime(image,fanart)

elif mode[0] =="VAalpha": 
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAalpha(image,fanart)

elif mode[0]=="VCalpha":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCalpha(image,fanart)

elif mode[0]=="VAgenres":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAgenres(image,fanart)
    
elif mode[0]=="VCgenres":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VCgenres(image,fanart)

elif mode[0]=="VCcat":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCcat(url, image, fanart)
    
elif mode[0]=="VAcat":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VAcat(url, image, fanart)

elif mode[0]=="VCpart":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCpart(url, image, fanart)
    
elif mode[0]=="VApart":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VApart(url, image, fanart)

elif mode[0]=="VCsearch":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCsearch(image, fanart)
    
elif mode[0]=="VAsearch":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VAsearch(image, fanart)

elif mode[0]=="VAstream":
    url = args['url'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAstream(url)
    
elif mode[0]=="VCstream":
    url = args['url'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VCstream(url)

elif mode[0]=='TV SHOWS - WEEKLY UPDATE':
    from resources.lib.indexers import Dizilab
    Dizilab.CCTV(fanart)

elif mode[0]=='CCfind':
    url = args['url'][0]
    from resources.lib.indexers import Dizilab
    Dizilab.CCfind(url)
    
elif mode[0]=='NEWMOVE':
    try:
        url = args['url'][0]
    except:
        url = 'http://m4ufree.info/'
    from resources.lib.indexers import Movies
    Movies.NEWMOVE(url,fanart)
    
elif mode[0]=='NMP':
    url = args['url'][0]
    from resources.lib.indexers import Movies
    Movies.NMP(url)
    
elif mode[0]=='MOVIECAT':
    image = icon
    from resources.lib.indexers import Movies
    Movies.MOVIECAT(image,fanart)

elif mode[0]=='GENRE':
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import Movies
    Movies.GENRE(url,image,fanart)
    
elif mode[0]=="CLEAR":
    xbmc.executebuiltin('XBMC.Container.Update(path,replace)')
    
elif mode[0]=="SEARCH":
    url = args['url'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import Movies
    Movies.SEARCH(url,fanart)
