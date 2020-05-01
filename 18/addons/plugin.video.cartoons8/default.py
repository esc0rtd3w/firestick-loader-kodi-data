import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,cloudflare,net,jsunpack,json,urlresolver
from addon import Addon

net = net.Net()
addon_id = 'plugin.video.cartoons8'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
cartoon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'cartoon.png'))
anime = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'anime.png'))
superc = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'superc.png'))
animexd = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'animexd.png'))
try:os.mkdir(datapath)
except:pass
file_var = open(xbmc.translatePath(os.path.join(datapath, 'cookie.lwp')), "a")
cookie_file = os.path.join(os.path.join(datapath,''), 'cookie.lwp')

def INDEX():
        addDir('9Cartoon','url',9,cartoon,fanart)
        addDir('Super Cartoons','url',4,superc,fanart)
        addDir('GogoAnime','url',10,anime,fanart)
        addDir('AnimeXD','url',14,animexd,fanart)

#########################################################################################   ANIMEXD START
def ANIMEXDCATEGORIES():
        addDir('Latest Episodes','http://www.animexd.me/home/latest-episodes',15,animexd,fanart)
        addDir('Latest Animes','http://www.animexd.me/home/latest-animes',15,animexd,fanart)
        addDir('Winter 2017','http://www.animexd.me/home/Winter%202017',17,animexd,fanart)
        addDir('Anime List','http://www.animexd.me/home/anime-list',16,animexd,fanart)
        addDir('Ongoing','http://www.animexd.me/home/ongoing',17,animexd,fanart)
        addDir('Genres','http://www.animexd.me/home/genres',18,animexd,fanart)
        addDir('Search','http://www.animexd.me/home/genres',19,animexd,fanart)
        
def ANIMEXDSEARCH(url):
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.animexd.me/home/search?q=' + search_entered
        link = net.http_GET(url).content
        link = cleanHex(link)
        data = json.loads(link)
        data=data['animes']
        for item in data:
                name=item['original_name']
                aurl=item['seo_name']
                url='http://www.animexd.me/watch/'+aurl
                iconimage='http://www.animexd.me/anime_images/'+aurl+'.jpg'
                addDir(name,url,20,iconimage,iconimage)
        
def ANIMEXDGENRES(url):
        link = net.http_GET(url).content
        link = cleanHex(link)
        match=re.compile('<li  ><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                addDir(name,url,17,animexd,animexd)

def ANIMEXDONGOING(url):
        link = net.http_GET(url).content.replace('\r','').replace('\n','').replace('\t','').replace('  ','')
        link = cleanHex(link)
        match=re.compile('<div class="bl-box">(.+?)<div class="bl-drop">',re.DOTALL).findall(link)
        for data in match:
                name=re.compile('class="blb-title">(.+?)</a>').findall(data)[0]
                match=re.compile('<a href="(.+?)" class="blb-image"><img src="(.+?)"').findall(data)
                for url,iconimage in match:
                        addDir(name,url,20,iconimage,iconimage)
        try: 
                np=link.split('paginator-next')[0].split('</li><li>')[-1]
                np=re.compile('<a href="(.+?)" class="').findall(np)
                for url in np:
                        if not 'faq' in url:
                                addDir('Next >>',url,17,icon,fanart)
        except:pass
        
def ANIMEXDANIMELIST(url):
        link = net.http_GET(url).content
        link = cleanHex(link)
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)[8:][:-11]
        for url,name in match:
                name=name.replace('&amp;','&')
                addDir(name,url,20,animexd,animexd)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def ANIMEXDLATESTEPISODES(url):
        link = net.http_GET(url).content.replace('\r','').replace('\n','').replace('\t','').replace('  ','')
        link = cleanHex(link)
        match=re.compile('<div class="dl-item">(.+?)</div></div>').findall(link)
        for data in match:
                match=re.compile('<div class="name"><a href="(.+?)">(.+?)</a.+?/div><div class="time">(.+?) ago').findall(data)
                for url,name,time in match:
                        time=time+' ago'
                        name = cleanHex(name.replace('&amp;','&'))
                        addDir(name,url,20,animexd,animexd)       
        try: 
                np=link.split('paginator-next')[0].split('</li><li>')[-1]
                np=re.compile('<a href="(.+?)" class="').findall(np)
                for url in np:
                        addDir('Next >>',url,15,icon,fanart)
        except:pass

def ANIMEXDPLAYLINK(name,url,iconimage):
        referer=url
        link = net.http_GET(url).content.replace('\r','').replace('\n','').replace('\t','').replace('  ','')
        link = cleanHex(link)
        try:
                if 'file:'in link:
                        try:url=re.compile("file: '(.+?)'").findall(link)[0]
                        except:url=re.compile('file: "(.+?)"').findall(link)[0]
                        print url
                        ok=True
                        liz=xbmcgui.ListItem(cleanHex(name), iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
                        xbmc.Player ().play(url)#+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0', liz, False)
                        quit()
        except:pass
        if 'safeupload' in link:
                url=re.compile('src="(.+?)" width=').findall(link)
                link = net.http_GET(url).content
                link = cleanHex(link)
        elif 'epCheck' in link:
                match=re.compile('<div class="epCheck ">(.+?)</li>',re.DOTALL).findall(link)
                match=list(reversed(match))
                if 'checkk' in str(match):
                        for data in match:
                                if 'checkk' in data:
                                        match=re.compile('<a href="(.+?)">(.+?)</a>').findall(data)
                                        for url,name in match:
                                                name = cleanHex(name.replace('&amp;','&'))
                                                addDir(name,url,20,iconimage,fanart)
                else:
                         for data in match:
                                match=re.compile('<a href="(.+?)">(.+?)</a>').findall(data)
                                for url,name in match:
                                        name = cleanHex(name.replace('&amp;','&'))
                                        addDir(name,url,20,iconimage,fanart)
       
#########################################################################################   ANIMEXD END

#########################################################################################   SUPERCARTOONS START
def SCCATEGORIES():
        addDir('Super Cartoons - Characters','http://www.supercartoons.net/characters/1',3,superc,fanart)
        addDir('Super Cartoons - Studio','http://www.supercartoons.net/studios/1',3,superc,fanart)
        
def GETSUPER(url):
        referer=url
        domain='http://www.supercartoons.net'
        link = net.http_GET(url).content.replace('\n','')
        if not 'file:' in link:
                match=re.compile('<article class="cartoon col-md-3">(.+?)</article>',re.DOTALL).findall(link)
                for data in match:
                        name=re.compile('<h3 class="caption">(.+?)</h3>').findall(data)[0].replace('&amp;', '&').replace('&#039;', "'").split('<br>')[0]
                        url=domain+re.compile('<a href="(.+?)">').findall(data)[0]
                        iconimage=domain+re.compile('src="(.+?)"').findall(data)[0]
                        if not '20th Century' in name:
                                        if not 'Filmation' in name:
                                                if not 'Paramount' in name:
                                                        if not 'Universal' in name:
                                                                if not 'Columbia' in name:
                                                                        addDir(name,url,3,iconimage,iconimage)
                try:
                        np=domain+re.compile('<link rel="next" href="(.+?)">').findall(link)[0]
                        nextpage=np.split('/')[-1]
                        addDir('Next >> Page',np,3,icon,fanart)
                except:pass
        else:GETSUPERLINK(referer)

def GETSUPERLINK(referer):
        link = net.http_GET(url).content
        access = net.http_GET('http://www.supercartoons.net/ad-preroll.html')
        playurl=re.compile("file: '(.+?)'").findall(link)[0]
        playurl=playurl+'&pu='+playurl+'|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36&Referer='+referer
        PLAYLINK(name,playurl,iconimage)
        quit()
#########################################################################################   SUPERCARTOONS END
        
#########################################################################################   CARTOONS8 START
def CCATEGORIES():
        addDir('9Cartoon - Latest Update','http://9cartoon.me/CartoonList/LatestUpdate',12,cartoon,fanart)
        addDir('9Cartoon - New & Hot','http://9cartoon.me/CartoonList/NewAndHot?page=1',1,cartoon,fanart)
	addDir('9Cartoon - New Added','http://9cartoon.me/CartoonList/New?page=1',1,cartoon,fanart)
	addDir('9Cartoon - Popular','http://9cartoon.me/CartoonList/MostViewed?page=1',1,cartoon,fanart)
	addDir('9Cartoon - A - Z','http://9cartoon.me/CartoonList',5,cartoon,fanart)
	addDir('9Cartoon - Genres','http://9cartoon.me',6,cartoon,fanart)
        addDir('9Cartoon - Search','http://9cartoon.me/Search?s=',8,cartoon,fanart)

def ACATEGORIES():
        addDir('GogoAnime - Latest Update','http://chiaanime.co/AnimeList/LatestUpdate',12,anime,fanart)
        addDir('GogoAnime - New & Hot','http://chiaanime.co/AnimeList/NewAndHot?page=1',1,anime,fanart)
	addDir('GogoAnime - New Added','http://chiaanime.co/AnimeList/New?page=1',1,anime,fanart)
	addDir('GogoAnime - Popular','http://chiaanime.co/AnimeList/MostViewed?page=1',1,anime,fanart)
	addDir('GogoAnime - A - Z','http://chiaanime.co/AnimeList',5,anime,fanart)
	addDir('GogoAnime - Genres','http://chiaanime.co/',6,anime,fanart)
        addDir('GogoAnime - Search','http://chiaanime.co/Search?s=',8,anime,fanart)

def LATESTUPDATE(url):
        link = open_url(url)
        link = link.replace("'",'"')
        match=re.compile('<li title="<div class="thumnail_tool">(.+?)</li>',re.DOTALL).findall(link)
        for data in match:
                ep=''
                url=re.compile('<a href="(.+?)" title').findall(data)[0]
                name=re.compile('title="(.+?)">').findall(data)[0]
                try:ep=re.compile('#FF4429">(.+?)</span>').findall(data)[0]
                except:pass        
                iconimage=re.compile('<img src="(.+?)"').findall(data)[0]
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                addLink(name+ep,url,100,iconimage,iconimage)

def GETMOVIES(url,name):
        link = open_url(url)
        link = link.replace("'",'"').replace('\n','').replace('\t','').replace('  ','')
        items=re.compile('<li title=(.+?)</li>',re.DOTALL).findall(link)
        for item in items:
                iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
                murl=re.compile('bigChar" href="(.+?)">').findall(item)[0]
                name=re.compile('bigChar" href=".+?">(.+?)</a>').findall(item)[0]
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                name = cleanHex(name)
                addDir(name,murl,2,iconimage,iconimage)
        try:
                pagenum = url.split('?page=')
                curpage = int(pagenum[1])
                nextpage = curpage + 1
                nextpageurl = pagenum[0]+'?page='+str(nextpage)
                addDir('Next >> Page '+str(nextpage),nextpageurl,1,icon,fanart)
        except: pass

def GETEPISODES(url,name,iconimage):
        link = open_url(url)
        link = link.replace('\n','').replace('  ','').replace('\t','').replace('\r','')
        match=re.compile('<ul id="episode_related">(.+?)</ul></div>').findall(link)[0]      
        match=re.compile('<a href="(.+?)">(.+?)</a>').findall(match)
        match=list(reversed(match))
        for url, name2 in match:
                if len(match)==1:
                        url=GETPLAYLINK(name,url,iconimage)
                        PLAYLINK(name,url,iconimage)
                else:
                        name = cleanHex(name)
                        addLink(name2,url,100,iconimage,iconimage)
def SEARCH(url):
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = url + search_entered + '&page=1'
        GETGENREMOVIES(url)

def GETGENRES(url,iconimage):
        list=[]
        link = open_url(url)
        match=re.compile('<a href="(.+?)"').findall(link)
        for url in match:
                if 'Genre' in url:
                        if url not in list:
                                list.append(url)                 
        for url in list:
                name=url.split('/')[-1].title()
                url=url+'?page=1'
                addDir(name,url,7,iconimage,iconimage)
                        
def GETGENREMOVIES(url):
	url2=url
        link = open_url(url)        
        match=re.compile('<img src="(.+?)">.+?<a href="(.+?)" title="(.+?)">',re.DOTALL).findall(link)[3:]
        if len(match)==0:
                items=re.compile('<div class="last_episodes_items">(.+?)<div class="left sub">',re.DOTALL).findall(link)
                for data in items:
                        url=re.compile('<a href="(.+?)" title').findall(data)[0]
                        name=re.compile('title="(.+?)">').findall(data)[0]
                        iconimage=re.compile("url\('(.+?)'").findall(data)[0]
                        iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                        addDir(name,url,2,iconimage,iconimage)     
        else:
                for iconimage, url, name  in match:
                        iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                        addDir(name,url,2,iconimage,iconimage)
	try:
                pagenum = url2.split('?page=')[1]
                genre = url2.split('?page=')[0]
                curpage = int(pagenum)
                nextpage = curpage + 1
                nextpageurl = genre+'?page='+str(nextpage)
                addDir('Next >> Page '+str(nextpage),nextpageurl,7,icon,icon)
        except: pass

def GETFULL(url,name):
        if '9cartoon.me' in url:base='http://9cartoon.me/CartoonList'
        else: base='http://chiaanime.co/AnimeList'
        link = open_url(url)
        match=re.compile('<li class="first-char"><a  href="(.+?)">(.+?)</a></li>').findall(link)
        if len(match)==0:
                link = link.replace('\n','').replace('  ','').replace('\t','').replace('\r','')
                match=re.compile('<li class="first-char"><a href="(.+?)" class="">(.+?)</a></li>').findall(link)
        for url, name in match:
                if not 'http' in url:
                        url=base +url
                url=url+'&page=1'
                addDir(name,url,11,iconimage,iconimage)
              
def AZ(url,name):
        link = open_url(url)
        link = link.replace("'",'"')
        match=re.compile('<li title="<div class=".+?"><img src="(.+?)".+?href="(.+?)">(.+?)</a',re.DOTALL).findall(link)
        for iconimage, murl, name in match:
                iconimage=iconimage+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                name = cleanHex(name)
                addDir(name,murl,2,iconimage,iconimage)
        try:
                pagenum = url.split('&page=')
                curpage = int(pagenum[1])
                nextpage = curpage + 1
                nextpageurl = pagenum[0]+'&page='+str(nextpage)
                addDir('Next >> Page '+str(nextpage),nextpageurl,11,iconimage,iconimage)
        except: pass
    
def GETPLAYLINK(name,url,iconimage):
        link = open_url(url)
        referer=url
        holderpage = re.compile('<iframe src="(.+?)" scrolling').findall(link)
        for hlink in holderpage:
                if 'http://player' in hlink:
                        link = open_url(hlink)
        if 'googlevideo.com' in link:#GOOGLE
                urls=re.compile('Right Click and Save Link as(.+?)pausePlayer',re.DOTALL).findall(link)[0]
                url=re.compile('<a href="(.+?)"').findall(link)[-1]
                print 'xxxxxxx' + url
                PLAYLINK(name,url,iconimage)
                quit()
        elif '/rd.php' in link:#OWN HOST
                url=re.compile('<source src="(.+?)" type="video/mp4"').findall(link)[0]+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Cookie=%s"%getCookiesString()
                PLAYLINK(name,url,iconimage)
                quit()
        elif 'openload.co/embed' in link:#OPENLOAD
                url=re.compile('<iframe src="(.+?)" scrolling').findall(link)[0]
                url=urlresolver.resolve(url)
                PLAYLINK(name,url,iconimage)
        else:#VKPASS
                url=re.compile('<center><iframe src="(.+?)" scrolling').findall(link)[0]
                url = urllib.unquote(url)
                headers = {'Content-Type':'application/x-www-form-urlencoded','Referer': referer}
                link=cleanHex(net.http_GET(url,headers).content)
                js=re.compile('</div></div></div></div><script>(.+?)</script><script>eval').findall(link)[0]
                jsdone=jsunpack.unpack(js)
                url=re.compile('<source src="(.+?)" type="video/mp4"').findall(jsdone)[0]
                url=url+"|User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0&Referer=%s&Cookie=%s"%(url,getCookiesString())
                PLAYLINK(name,url,iconimage)
                quit()                
###########################################################################################################################   CARTOONS8 END

def getCookiesString():
    cookieString=""
    import cookielib
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookie_file,ignore_discard=True)
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: 
        import sys,traceback
        traceback.print_exc(file=sys.stdout)
    return cookieString

def PLAYLINK(name,url,iconimage):  
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)
        #liz.setPath(url)
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

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

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        #liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def open_url(url):
        try:
                net.set_cookies(cookie_file)
                link = net.http_GET(url).content
                link = cleanHex(link)
                return link
        except:
                import cloudflare
                cloudflare.createCookie(url,cookie_file,'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0')
                net.set_cookies(cookie_file)
                link = net.http_GET(url).content
                link = cleanHex(link)
                return link
	
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
    

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

if mode==None or url==None or len(url)<1: INDEX()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETEPISODES(url,name,iconimage)
elif mode==3: GETSUPER(url)
elif mode==4: SCCATEGORIES()
elif mode==5: GETFULL(url,name)
elif mode==6: GETGENRES(url,iconimage)
elif mode==7: GETGENREMOVIES(url)
elif mode==8: SEARCH(url)
elif mode==9: CCATEGORIES()
elif mode==10: ACATEGORIES()
elif mode==11: AZ(url,name)
elif mode==12: LATESTUPDATE(url)
elif mode==13: GETSUPERLINK(name,url,iconimage)
elif mode==14: ANIMEXDCATEGORIES()
elif mode==15: ANIMEXDLATESTEPISODES(url)
elif mode==16: ANIMEXDANIMELIST(url)
elif mode==17: ANIMEXDONGOING(url)
elif mode==18: ANIMEXDGENRES(url)
elif mode==19: ANIMEXDSEARCH(url)
elif mode==20: ANIMEXDPLAYLINK(name,url,iconimage)

elif mode==100: GETPLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

