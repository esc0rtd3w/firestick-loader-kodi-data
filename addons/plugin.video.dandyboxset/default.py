# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, dandy, xbmcaddon, base64,random
from addon.common.addon import Addon
import urlresolver
from metahandler import metahandlers
addon_id='plugin.video.dandyboxset'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PATH = 'dandyboxset'
VERSION = ADDON.getAddonInfo('version')
ART = ADDON_PATH + "/resources/icons/"
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()

alluc_user = selfAddon.getSetting('alluc_username')
alluc_pw = selfAddon.getSetting('alluc_password')
max_items = int(selfAddon.getSetting('alluc_max_results'))
max_result_string = '&count=%s' % max_items


keys = ['7912675e249526c037e21a237863aba0', '9252a8e0f8cb44564ff1a87b47477821', '73978dd7d836b3c0ec362a86ca561d41', '47106bcdd168c44d5aa440a52084e2a3', '72632925e32bf9097e387c9ef9c6fdc3', '33f5d08c3591e605e487c4da9fe0b6ea', '63831b636197620f989df4da3f3c1b5e', 'd3bb8a6b38920be2ad77478589a1b400', '7d3f84d5f7526b08d966bd3b4cca464c','9500877da965b7568ae8f45e4f1a3b33', 'e22bf4590576c6db9d1963c58f27f020', 'eaadbe1a31b1c631b034ae1504716eff']
alluc_rand=(random.choice(keys))

if alluc_user == '':
    alluc_get =  'https://www.alluc.ee/api/search/download/?apikey=%s&query=' % (alluc_rand)
else:
    alluc_get =  'http://www.alluc.ee/api/search/download/?user=%s&password=%s&query=' % (alluc_user, alluc_pw)

def Main_Menu():
    OPEN = Open_Url('https://raw.githubusercontent.com/dandy0850/iStream/master/dandyboxsetsv2/main.xml')
    Regex = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART>').findall(OPEN)
    count = 0
    for name,url,icon,fanart in Regex:
        if 'xml' in url:
            addDir(name,url,1,icon,fanart,'')
        else:
            addDir(name,url,100,icon,fanart,'')
    addDir('[B][COLOR white]All %s movies[/COLOR][/B]' % addon_name,"",300,ICON,FANART,'')
    addDir('[B][COLOR white]Search %s movies[/COLOR][/B]' % addon_name,"",400,ICON,FANART,'')

def Second_Menu(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART>').findall(OPEN)
    for name,url,icon,fanart in Regex:
            items = len(Regex)
            if metaset=='true':
                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,fanart,'')
    setView('movies', 'movie-view')

def All_Movies():
    OPEN = Open_Url('https://raw.githubusercontent.com/dandy0850/iStream/master/dandyboxsetsv2/main.xml')
    TotalRegex = []
    for u in [q for q in [s[1] for s in re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART>').findall(OPEN)] if q.endswith(".xml")]:
        TotalRegex = TotalRegex + re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART>').findall(Open_Url(u))
    for name,url,icon,fanart in sorted(TotalRegex):
        addDir(name,url,100,icon,fanart,'')

def Search(url):
    if url and url is not ("" or None): query = url
    else:
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
            query = keyb.getText()
    OPEN = Open_Url('https://raw.githubusercontent.com/dandy0850/iStream/master/dandyboxsetsv2/main.xml')
    TotalRegex = []
    for u in [q for q in [s[1] for s in re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART>').findall(OPEN)] if q.endswith(".xml")]:
        TotalRegex = TotalRegex + re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART>').findall(Open_Url(u))
    for name,url,icon,fanart in sorted(TotalRegex):
        if query.lower() in str(name).lower():
            addDir(name,url,100,icon,fanart,'')

def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addDir(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==100:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)

def addDir2(name,url,mode,iconimage,itemcount):
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        splitName=name.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
            simplename=splitName[0]
            simpleyear=splitName[2].partition(')')
        if len(simpleyear)>0:
            simpleyear=simpleyear[0]
        mg = eval(base64.b64decode('bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iMzZjMWM1OWYwNTI0YTYzZTc3MmI5MGMzNzc4ZmIwOTciKQ=='))
        meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=iconimage
        name = '[B][COLOR white]' + name + '[/COLOR][/B]'
        meta['title'] = name
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 99, 'url':meta['trailer']})))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image',FANART)
        if mode==100 or mode==101:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok

def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':

        print addon.get_setting(viewType)
        if addon.get_setting(viewType) == 'Info':
            VT = '504'
        elif addon.get_setting(viewType) == 'Info2':
            VT = '503'
        elif addon.get_setting(viewType) == 'Info3':
            VT = '515'
        elif addon.get_setting(viewType) == 'Fanart':
            VT = '508'
        elif addon.get_setting(viewType) == 'Poster Wrap':
            VT = '501'
        elif addon.get_setting(viewType) == 'Big List':
            VT = '51'
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
        elif addon.get_setting(viewType) == 'List':
            VT = '50'
        elif addon.get_setting(viewType) == 'Default Menu View':
            VT = addon.get_setting('default-view1')
        elif addon.get_setting(viewType) == 'Default TV Shows View':
            VT = addon.get_setting('default-view2')
        elif addon.get_setting(viewType) == 'Default Episodes View':
            VT = addon.get_setting('default-view3')
        elif addon.get_setting(viewType) == 'Default Movies View':
            VT = addon.get_setting('default-view4')
        elif addon.get_setting(viewType) == 'Default Docs View':
            VT = addon.get_setting('default-view5')
        elif addon.get_setting(viewType) == 'Default Cartoons View':
            VT = addon.get_setting('default-view6')
        elif addon.get_setting(viewType) == 'Default Anime View':
            VT = addon.get_setting('default-view7')

        print viewType
        print VT
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
        return

def resolve(name,url,iconimage,description):
    hoster = []
    stream_url = []
    host = ''
    movie = name.split('(')[0].replace('[B][COLOR white]','').replace(':','').replace('\'','').lower()   
    year = name.split('(')[1].replace(')','').replace('[/COLOR][/B]','')
    film = movie.replace(' ','%20').replace('&','%26') + year
    allucsearch = alluc_get + film + max_result_string
    print 'search url > ' + allucsearch
    #print 'ALLUC > ' + alluc_get
    
    OPEN = Open_Url(allucsearch)
    match = re.compile('"title":"(.+?)".+?"hostername":"(.+?)".+?"url":"(.+?)"').findall(OPEN)
    for title,label,link in match:
        if '.rar'not in title:
            if '.rar'not in link:
                link=link.replace('\/','/')
                if urlresolver.HostedMediaFile(link).valid_url():
                    title = title.replace('.','%20').replace('_','%20').replace(' ','%20')
                    print 'title > ' + title
                    movie = movie.replace(' ','%20').replace(',','')
                    print 'movie > ' + movie
                    if movie in title.lower():
                        if year in title:
                            if '1080' in title:
                                rez = '1080p'
                            elif '720' in title:
                                rez = '720p'
                            elif 'docs.google' in link:
                                rez = 'HD'
                            else: rez = 'DVD'
                            if 'easybytez' not in link:
                                if 'shared' not in link:
                                    if 'filepup' not in link: 
                                        if 'k2s.cc' not in link:  
                                            label = label + '[COLOR blue] ['+rez+']'                                            
                                            host = '[B][COLOR white]%s[/COLOR][/B]' %label
                                            hoster.append(host)
                                            stream_url.append(link)
    if len(match) >1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Select Your Link',hoster)
            if ret == -1:
                return
            elif ret > -1:
                    url = stream_url[ret]
    else:
        pass
    url = url.replace('/preview','/edit')
    if 'vidlox' in url:
        OPEN = Open_Url(url)
        url = re.compile('master.m3u8","(.+?)"',re.DOTALL).findall(OPEN)[0] 
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 
  
    else: 
        stream = urlresolver.HostedMediaFile(url).resolve()
        try:
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title':name})
            liz.setProperty("IsPlayable","true")
            liz.setPath(stream)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        except: pass 

def OPEN_UrlRez():
        xbmcaddon.Addon('script.module.urlresolver').openSettings()

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
iconimage=None
mode=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

###########################################

if mode == None: Main_Menu()
elif mode == 1 : Second_Menu(url)
elif mode == 99: PT(url)
elif mode == 100 : resolve(name,url,iconimage,description)
elif mode == 200: OPEN_UrlRez()
elif mode == 300: All_Movies()
elif mode == 400: Search(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
