import sys,urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,json
import urlresolver
import requests
from addon.common.addon import Addon
from metahandler import metahandlers
from resources.lib.jsbeautifier.unpackers import packer

#HD-Movie14 Add-on Created By Mucky Duck (1/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdhdmovie14'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
metaset = selfAddon.getSetting('enable_meta')
con_trailer = selfAddon.getSetting('enable_trailers')
metaget = metahandlers.MetaData()
baseurl = 'http://hdmovie14.net'




def CAT():
        addDir('[B][COLOR white]Most Views[/COLOR][/B]',baseurl+'/list/most-view',1,icon,fanart,'')
        addDir('[B][COLOR white]Top IMDB[/COLOR][/B]',baseurl+'/list/topimdb',1,icon,fanart,'')
        addDir('[B][COLOR white]Country[/COLOR][/B]',baseurl,7,icon,fanart,'')
        addDir('[B][COLOR white]Search[/COLOR][/B]','url',4,icon,fanart,'')
        addDir('[B][COLOR white]Movies[/COLOR][/B]',baseurl+'/list/movie',1,icon,fanart,'')
        addDir('[B][COLOR white]Genre[/COLOR][/B]',baseurl,5,icon,fanart,'')
        addDir('[B][COLOR white]Year[/COLOR][/B]',baseurl,6,icon,fanart,'')
        addDir('[B][COLOR white]TV[/COLOR][/B]',baseurl+'/list/series',1,icon,fanart,'')




def INDEX(url):
        link = OPEN_URL(url)
        all_videos = regex_get_all(link, '<div data-content=', '</div></div></div>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, '<h3>', '<').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#039;',"'")
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                seas = regex_from_to(a, '<p>', '<')
                if 'Season'not in seas:
                        if metaset=='true':
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,3,thumb,items)
                        else:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,3,thumb,fanart,'')
                else:
                        addDir('[B][COLOR white]%s[/COLOR] : [I][COLOR red]%s[/COLOR][/I][/B]' %(name,seas),baseurl+url,2,thumb,fanart,'') 
        try:
                np = re.compile('<a href="(.*?)".*?</a>').findall(link)[-2]
                addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',baseurl+np,1,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')




def EPIS(url):
        link = OPEN_URL(url)
        addDir('[I][B][COLOR red]Episode[/COLOR][COLOR white] 1[/COLOR][/B][/I]' ,url,3,iconimage,fanart,'')
        all_links = regex_get_all(link, 'Select Episode		</div>', '</div>')
        all_videos = regex_get_all(str(all_links), 'button', 'button')
        try:
                for a in all_videos:
                        name = regex_from_to(a, 'episode">', '<')
                        url = regex_from_to(a, '\&quot;', '\&')
                        if name > '':
                                addDir('[I][B][COLOR red]Episode[/COLOR][COLOR white] %s[/COLOR][/B][/I]' %name,baseurl+url,3,iconimage,fanart,'')
        except: pass
        try:
                all_links = regex_get_all(link, 'Select Season		</div>', '</div>')
                all_videos = regex_get_all(str(all_links), 'button', 'button')
                for a in all_videos:
                        name = regex_from_to(a, 'episode">', '<')
                        url = regex_from_to(a, '\&quot;', '\&')
                        if name > '':
                                addDir('[I][B][COLOR cyan]Season[/COLOR][COLOR white] %s[/COLOR][/B][/I]' %name,baseurl+url,2,iconimage,fanart,'')
        except: pass
        setView('tvshows', 'show-view')




def LINK(name,url,iconimage):
        if iconimage == None:
                iconimage = icon
        link = OPEN_URL(url)
        RequestURL = baseurl+re.findall(r'<ifram.*?rc="(.*?)" .*?>', str(link), re.I|re.DOTALL)[-1]
        print '#################################RequestURL='+str(RequestURL)
        headers = {'referer': url, 'user-agent': User_Agent}
        r = requests.get(RequestURL, headers=headers).text
        gvids = re.findall(r'"url":"(.*?)","res":"(.*?)","type":"video/mp4"', str(r), re.I|re.DOTALL)
        items = len(gvids)
        for url, name in gvids:
                if metaset=='true':
                        addDir2('[B][COLOR white]Google Vids %s[/COLOR][/B]' %name,url,100,iconimage,items)
                else:
                        addDir('[B][COLOR white]Google Vids %s[/COLOR][/B]' %name,url,100,iconimage,fanart,'')
                
        print '#################################r'+str(r)
        RequestALT = baseurl+re.findall(r'ajax\({url: "(.*?)"', str(r), re.I|re.DOTALL)[0]
        print '#################################RequestALT'+str(RequestALT)
        r = requests.get(RequestALT).json()
        items2 = len(r)
        for url in r:
                if 'google' in str(url):
                        try:
                                url = re.findall("'url': u'(.*?)'", str(url), re.I|re.DOTALL)[-1]
                        except:
                                url = re.findall("'url': u'(.*?)'", str(url), re.I|re.DOTALL)[0]
                url = str(url).replace('-[W]x[H]','')
                name2 = str(url).replace('http://','').replace('https://','').replace('lh3.','').replace('usercontent','').partition('.')[0]
                if metaset=='true':
                        addDir2('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,items2)
                else:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,fanart,'')




#def LINK(url):
        #link = OPEN_URL(url)
        #print url
        #RequestURL = baseurl+re.findall(r'<ifram.*?rc="(.*?)".*?>', str(link), re.I|re.DOTALL)[-1]
        #headers = {'host': 'hdmovie14.net', 'referer': url, 'user-agent': User_Agent}
        #r = requests.get(RequestURL, headers=headers)
        #r = requests.get(RequestURL, headers=headers, cookies=r.cookies)
        #try:
                #url = re.compile('"url":"(.*?)"').findall(str(r.text))[-1]
        #except:
                #url = re.compile('"url":"(.*?)"').findall(str(r.text))[0]
        #liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        #liz.setInfo(type='Video', infoLabels={'Title':description})
        #liz.setProperty("IsPlayable","true")
        #liz.setPath(str(url))
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def SEARCH():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = baseurl+'/arama?q='+search
                INDEX(url)




def GENRE(url):
        link = OPEN_URL(url)
        match=re.compile('<a title="(.*?)" href="(.*?)">').findall(link) 
        for name,url in match:
                if '/category/' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,1,icon,fanart,'')




def COUNTRY(url):
        link = OPEN_URL(url)
        match=re.compile('<a title="(.*?)" href="(.*?)">').findall(link) 
        for name,url in match:
                if '/country/' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,1,icon,fanart,'')




def YEAR(url):
        link = OPEN_URL(url)
        match=re.compile('<a title="(.*?)" href="(.*?)">').findall(link) 
        for name,url in match:
                if '/year/' in url:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,baseurl+url,1,icon,fanart,'')




def RESOLVE(name,url):
        url = url.replace('html\:','')
        if 'thevideos.tv' in url:
                url = thevideos(url)
        #elif 'vidlocker.xyz' in url:
                #url = vidlocker(url)
        elif 'google' in url:
                url = url
        else:
                url = urlresolver.resolve(url)
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)



def thevideos(url):
        link = requests.get(url).text
        #script = re.findall("<script type='text/javascript'>(.*?)</script>", str(link), re.I|re.DOTALL)[0]
        #unpack = packer.unpack(script)
        try:
                url = re.findall('file:"(.*?)",label:".*?0p"', str(link), re.I|re.DOTALL)[-1]
        except:
                url = re.findall('file:"(.*?)",label:".*?0p"', str(link), re.I|re.DOTALL)[0]
        return url




def vidlocker(url):
        headers = {}
        headers['User-Agent'] = User_Agent
        link = requests.get(url, headers=headers, allow_redirects=False)
        try:
            link = re.findall(r'sources: \[\{file:"(.*?)"', str(link.text), re.I|re.DOTALL)[-1]
        except:
            link = re.findall(r'sources: \[\Boot{file:"(.*?)"', str(link.text), re.I|re.DOTALL)[0]
        return link




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




def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
        return




def addDir2(name,url,mode,iconimage,itemcount):
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        meta = metaget.get_meta('movie',name)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=icon
        name = '[B][COLOR white]' + name + '[/COLOR][/B]'
        meta['title'] = name
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 8, 'url':meta['trailer']})))
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
        if mode==100:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok




def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        #ok=True
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
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
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
site=None




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




if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        INDEX(url)

elif mode==2:
        EPIS(url)

elif mode==3:
        LINK(name,url,iconimage)

elif mode==4:
        SEARCH()

elif mode==5:
        GENRE(url)

elif mode==6:
        YEAR(url)

elif mode==7:
        COUNTRY(url)

elif mode == 8:
        PT(url)

elif mode == 100:
        RESOLVE(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
