import sys,urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
from addon.common.addon import Addon
from metahandler import metahandlers
import urlresolver
import requests

#SHOW-BOX Add-on Created By Mucky Duck (5/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdshow-box'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()
baseurl = 'http://show-box.co'




def CAT():
        addDir('[B][COLOR white]Trending Netflix Original Series[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR white]Recently Added Episodes[/COLOR][/B]',baseurl+'/?filtre=date&cat=0',2,icon,fanart,'')
        addDir('[B][COLOR white]Trending TV Shows[/COLOR][/B]',baseurl+'/trending-tv-shows',1,icon,fanart,'')
        addDir('[B][COLOR white]All Shows[/COLOR][/B]',baseurl+'/categories',1,icon,fanart,'')
        addDir('[B][COLOR white]Search[/COLOR][/B]','url',4,icon,fanart,'')
        
        




def INDEX(url):
        link = OPEN_URL(url)
        try:
                pagen = re.compile('<div class="pagination"><ul><li><span>(.*?)</span>').findall(link)[0]
                addLink('[I][B][COLOR red]%s[/COLOR][/B][/I]' %pagen,'url','',icon,fanart)
        except: pass
        all_videos = regex_get_all(link, '<li class="border-radius-5 box-shadow">', '</li>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'href=.*? title="', '"')
                name = name.replace('&nbsp;','')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'lazy-src="', '"')
                if thumb == '':
                        thumb = regex_from_to(a, 'src="', '"')
                if metaset=='true':
                        addDir2('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,2,thumb,items,'',name)
                else:
                        addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,2,thumb,fanart,'')
        try:
                pages=re.compile('<li><a href=\'(.*?)\' class="inactive">(.*?)</a>').findall(link)
                for url, name in pages: 
                        addDir('[I][B][COLOR red]Page %s >>>[/COLOR][/B][/I]' %name,url,1,icon,fanart,'')
        except: pass
        setView('movies', 'tv-view')




def EPIS(url,show_title):
        link = OPEN_URL(url)
        try:
                pagen = re.compile('<div class="pagination"><ul><li><span>(.*?)</span>').findall(link)[0]
                addLink('[I][B][COLOR red]%s[/COLOR][/B][/I]' %pagen,'url','',icon,fanart)
        except:pass
        all_videos = regex_get_all(link, '<li class="border-radius-5 box-shadow">', '</li>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'href=.*? title="', '"')
                name = name.replace('&nbsp;','')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'lazy-src="', '"')
                if thumb == '':
                        thumb = regex_from_to(a, 'src="', '"')
                if show_title == None:
                        show_title = name
                if metaset=='true':
                        addDir2('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,3,thumb,items,'',show_title)
                else:
                        addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,3,thumb,fanart,'')
        try:
                pages=re.compile('<li><a href=\'(.*?)\' class="inactive">(.*?)</a>').findall(link)
                for url, name in pages: 
                        addDir('[I][B][COLOR red]Page %s >>>[/COLOR][/B][/I]' %name,url,2,icon,fanart,'')
        except: pass
        setView('movies', 'tv-view')




def NETF(url):
        link = OPEN_URL(url)
        print '###########################link='+str(link)
        all_links = regex_get_all(link, '<span>Trending Netflix Original Series</span>', '</ul>')
        all_videos = regex_get_all(str(all_links), '<li class="border-radius-5 box-shadow">', '</li>')
        items = len(all_videos)
        print '############################str(all_links)='+str(all_links)
        print '############################str(all_videos)='+str(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'href=.*? title="', '"')
                name = name.replace('&nbsp;','')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii').replace("\\'", "'")
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'lazy-src="', '"')
                if thumb == '':
                        thumb = regex_from_to(a, 'src="', '"')
                if metaset=='true':
                        addDir2('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,2,thumb,items,'',name)
                else:
                        addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,2,thumb,fanart,'')
        try:
                pages=re.compile('<li><a href=\'(.*?)\' class="inactive">(.*?)</a>').findall(link)
                for url, name in pages: 
                        addDir('[I][B][COLOR red]Page %s >>>[/COLOR][/B][/I]' %name,url,1,icon,fanart,'')
        except: pass
        setView('movies', 'tv-view')




def RESOLVE(name,url,iconimage):
        link = OPEN_URL(url)
        match = re.compile('data-lazy-src="(.*?)"').findall(link)[0]
        url = urlresolver.resolve(match)
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={"Title":name, "Plot":description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def SEARCH():
        keyb = xbmc.Keyboard('', 'Search TV Shows')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/?s='+search
                link = OPEN_URL(url)
                try:
                        pagen = re.compile('<div class="pagination"><ul><li><span>(.*?)</span>').findall(link)[0]
                        addLink('[I][B][COLOR red]%s[/COLOR][/B][/I]' %pagen,'url','',icon,fanart)
                except:pass
                all_videos = regex_get_all(link, '<li class="border-radius-5 box-shadow">', '</li>')
                items = len(all_videos)
                for a in all_videos:
                        name = regex_from_to(a, 'href=.*? title="', '"')
                        name = name.replace('&nbsp;','')
                        name = addon.unescape(name)
                        name = name.encode('ascii', 'ignore').decode('ascii')
                        url = regex_from_to(a, 'href="', '"')
                        thumb = regex_from_to(a, 'lazy-src="', '"')
                        if thumb == '':
                                thumb = regex_from_to(a, 'src="', '"')
                        show_title = name[:-7]
                        if metaset=='true':
                                addDir2('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,3,thumb,items,'',show_title)
                        else:
                                addDir('[I][B][COLOR white]%s[/COLOR][/B][/I]' %name,url,3,thumb,fanart,'')
                try:
                        pages=re.compile('<li><a href=\'(.*?)\' class="inactive">(.*?)</a>').findall(link)
                        for url, name in pages: 
                                addDir('[I][B][COLOR red]Page %s >>>[/COLOR][/B][/I]' %name,url,2,icon,fanart,'')
                except: pass
                setView('movies', 'tv-view') 




def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r




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




def addDir(name,url,mode,iconimage,fanart,description):
        name = name.replace('()','')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok




def addDir2(name,url,mode,iconimage,itemcount,description,show_title):
        print '######################################show_title='+str(show_title)
        show_title = show_title.replace('[I][B][COLOR white]','').replace('[/COLOR][/B][/I]','')
        splitName=show_title.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
        if len(simpleyear)>0:
                simpleyear=simpleyear[0]
        meta = metaget.get_meta('tvshow',simplename,simpleyear)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        meta['title'] = name
        contextMenuItems = []
        contextMenuItems.append(('Show Info', 'XBMC.Action(Info)'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&show_title="+urllib.quote_plus(show_title)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else:
                liz.setProperty('fanart_image', art+'m4u.jpg')
        if mode==3:
                liz.setProperty("IsPlayable","true")
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok



def addLink(name,url,mode,iconimage,fanart,description=''):
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def OPEN_URL(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = requests.get(url, headers=headers).text
    link = link.encode('ascii', 'ignore').decode('ascii')
    return link






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
        elif addon.get_setting(viewType) == 'Default View':
            VT = addon.get_setting('default-view')
        

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




params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
show_title=None



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
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:
        show_title=urllib.unquote_plus(params["show_title"])
except:
        pass




if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        INDEX(url)

elif mode==2:
        EPIS(url,show_title)

elif mode==3:
        RESOLVE(name,url,iconimage)

elif mode==4:
        SEARCH()

elif mode==5:
        NETF(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
