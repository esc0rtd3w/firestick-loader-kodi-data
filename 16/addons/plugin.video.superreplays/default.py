import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os



PLUGIN = 'plugin.video.superreplays'
ADDON = xbmcaddon.Addon(id=PLUGIN)

addonfolder = ADDON.getAddonInfo('path')
maxVideoQuality = ADDON.getSetting("maxVideoQuality")
qual = ["480p", "720p", "1080p"]
maxVideoQuality = qual[int(maxVideoQuality)]

base_url = 'http://livetv.ru/en/videotourney/'




def CATEGORIES():
    addDir('Football',"url",1,'')
    addDir('Basketball',"url",1,'')
    addDir('American Football',"url",1,'')
    addDir('Ice Hockey',"url",1,'')

    
def Listcat(name):
    a=open(os.path.join(addonfolder,'resources',name)).read()
    match=re.compile('id=<(.+?)> name=<(.+?)>').findall(a)    
    for id,name in match:   
        iconimage='http://cdnx.livetv.sx/img/tables/%s.gif' %id
        addDir(name,id,2,iconimage)
    
    

def ListTeams(url):
    print base_url+url
    link = OPEN_URL(base_url+url)
    link = link.split('<td bgcolor="#f7f7f7">')[1]
    match = re.compile('<b>(.+?)</b>').findall (link)

    for name in match:
        if not ':' in name:
            if not 'x' in name:
                if not 'Live' in name:
                    if not '&ndash;' in name:
                        name='[COLOR blue]%s[/COLOR]'%name
                    addDir(name.replace('&ndash;','-'),url,5,"")
        
        
        
def ListVideoType(name,url):
    name=name.replace('-','&ndash;')
    url = OPEN_URL(base_url+url)
    link=url.split('<b>%s</b>'% name)[1]
    link=link.split('<table width="100%" height=27 cellpadding=4 cellspacing=0>')[0]
    link=link.split('href="/en')
    for p in link:
        match = re.compile('/(.+?)">(Highlights|First Half|Second Half|Long Highlights|Full match record*)<').findall(p)
        print match
        for url,name in match:
            addDir(name.title(),'http://livetv.sx/en/'+url,6,"")
    
                
def getStreamUrl(id):
    content = OPEN_URL("http://www.dailymotion.com/embed/video/"+id)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,Not Found (DailyMotion)!,5000)')
        return ""
    else:
        matchFullHD = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(content)
        matchHD = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(content)
        matchHQ = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(content)
        matchSD = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(content)
        matchLD = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(content)
        url = ""
        if matchFullHD and maxVideoQuality == "1080p":
            url = urllib.unquote_plus(matchFullHD[0]).replace("\\", "")
        elif matchHD and (maxVideoQuality == "720p" or maxVideoQuality == "1080p"):
            url = urllib.unquote_plus(matchHD[0]).replace("\\", "")
        elif matchHQ:
            url = urllib.unquote_plus(matchHQ[0]).replace("\\", "")
        elif matchSD:
            url = urllib.unquote_plus(matchSD[0]).replace("\\", "")
        elif matchLD:
            url = urllib.unquote_plus(matchLD[0]).replace("\\", "")
        return url
        
def GrabNHL(id):
    link = OPEN_URL('http://video.nhl.com/videocenter/servlets/playlist?ids=%s&format=json'%str(id))
    r = '"publishPoint":"(.+?)\?'
    match = re.compile(r,re.DOTALL).findall(link)
    return match[0]
        
def GrabRu(id):
    link = OPEN_URL('http://rutube.ru/api/play/trackinfo/%s/?format=xml'%str(id))
    r = '<m3u8>(.+?)</m3u8>'
    match = re.compile(r,re.DOTALL).findall(link)
    return match[0]
    
def GrabVidea(id):
    link = OPEN_URL('http://videa.hu/flvplayer_get_video_xml.php?v=%s&m=0'%str(id))
    name=[]
    url=[]
    r = 'version quality="(.+?)" video_url="(.+?)"'
    match = re.compile(r,re.DOTALL).findall(link)
    for quality,stream in match:
        name.append(quality.title())
        url.append(stream)
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]

def GrabVK(url):
    link = OPEN_URL(url.replace('amp;',''))
    name=[]
    url=[]
    r      ='"url(.+?)":"(.+?)"'
    match = re.compile(r,re.DOTALL).findall(link)
    for quality,stream in match:
        name.append(quality+'p')
        url.append(stream.replace('\/','/'))
    return url[xbmcgui.Dialog().select('Please Select Resolution', name)]
                

def HIGHLIGHTS_LINKS(name,url):
    link = OPEN_URL(url)
    if "www.youtube.com/embed/" in link :
        r = 'youtube.com/embed/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        yt= match[0]
        iconimage = 'http://i.ytimg.com/vi/%s/0.jpg' % yt.replace('?rel=0','')
        url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % yt.replace('?rel=0','')
        addDir( name+' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , iconimage  )
    if "dailymotion.com" in link :
        r = 'src="http://www.dailymotion.com/embed/video/(.+?)\?.+?"></iframe>'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir ( name+' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , GETTHUMB(url), '' )
    if "http://videa" in link :
        r = 'http://videa.+?v=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]VIDEA[/COLOR]',url,200,'')
            
    if "rutube.ru" in link :
        r = 'rutube.ru/video/embed/(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]RUTUBE[/COLOR]',url,200,'' )
            
    if "playwire" in link :
        r = 'cdn.playwire.com.+?config=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]PLAYWIRE[/COLOR]',url,200,'' )
    if "vk.com" in link :
        r = '<iframe src="(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]VK.COM[/COLOR]',url,200,'' )
    if '"file"' in link :
        r = '"file","(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]DIRECT[/COLOR]',url,200,'' )
    if 'nhl.com' in link :
        r = 'videocenter/embed\?playlist=(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match :
            addDir (name+' - [COLOR red]NHL[/COLOR]',url,200,'' )
    if 'googlevideo.com' in link :
        r = 'src="(https://.+googlevideo.com.+?)"'
        match = re.compile(r).findall(link)
        for url in match :

            addDir (name+' - [COLOR red]GOOGLE VIDEO[/COLOR]',url,200,'' )            
            
    
def PLAY_STREAM(name,url,iconimage):
        if 'DIRECT' in name:
            link = str(url)
        if 'YOUTUBE' in name:
            link = str(url)
        elif 'VIDEA' in name:
            link = GrabVidea(url)
        elif 'VK.COM' in name:
            link = GrabVK(url)
        elif 'NHL' in name:
            link = GrabNHL(url)
            
            
        elif 'RUTUBE' in name:
            try:
                html = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml'% url.replace('_ru','')
                link = OPEN_URL(html)
                r = '<m3u8>(.+?)</m3u8>'
                match = re.compile(r,re.DOTALL).findall(link)
                if match:
                    link=match[0]
                else:
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                    return
            except:
                dialog = xbmcgui.Dialog()
                dialog.ok("Football Replays", '','Sorry Video Is Private', '')
                return
        elif 'PLAYWIRE' in name:
            link = OPEN_URL(url)
            r = '"src":"(.+?)"'
            match = re.compile(r,re.DOTALL).findall(link)
            if match:
                link=match[0]
        elif 'DAILYMOTION' in name:
            link = getStreamUrl(url)
        else:
            link=url
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(link)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            



def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if mode == 200:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok



          
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

print "URL: "+str(url)



if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

elif mode==1:
    Listcat(name)

elif mode==2:
    ListTeams(url)

    
    
elif mode==5:
    ListVideoType(name,url)
    
elif mode==6:
    HIGHLIGHTS_LINKS(name,url)
    
    
elif mode==200:
    PLAY_STREAM(name,url,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
