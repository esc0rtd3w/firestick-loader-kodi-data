import urllib,urllib2,re,os,sys
#import xbmc,xbmcaddon,xbmcgui,xbmcplugin

def TVShows(url):
    stringlist=''
    fixdate=''
    link=open_url(url)
    shows=re.compile("<li class='listEpisode'(.+?)</li>",re.DOTALL).findall(link)
    for show in shows:
        name=re.compile("</span>(.+?)</a>").findall(show)[0]
        date=re.compile("\>(.+?) \: <a target").findall(show)[0].replace(' ','/')
        day=date.split('/')[0]
        month=date.split('/')[1]
        year=date.split('/')[2]
        if len(day)==1:
            day='0'+day
        date='[COLOR gold]'+day+'/'+month+'/'+year+'[/COLOR]'
        name=date+' - '+name
        url=re.compile('href="(.+?)">').findall(show)[0]
        string='<start>'+name+'<sep>'+url+'<end>'
        stringlist=stringlist+string
    return stringlist

def Stream(url):
    link=open_url(url)
    host_links=re.compile('<a target="_blank" rel="nofollow" href="(.+?)">Play</a>').findall(link)
    print host_links
    return host_links

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

