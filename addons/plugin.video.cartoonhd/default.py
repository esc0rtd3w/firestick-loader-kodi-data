import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

import json,net


net=net.Net()

ADDON = xbmcaddon.Addon(id='plugin.video.cartoonhd')

cartoon=os.path.join(ADDON.getAddonInfo('path'),'cartoon')
headers={'xKey': 'eae09beb57d6b1823e872eded0a3a054','User-Agent':'MyApp/2.2.2 (iPhone; iOS 8.4; Scale/2.00','Host': 'wowcartoon.com:8182'}
GETLINK='http://wowcartoon.com:8182/C4C/api/C4C/GetGenreDetail'
GETKIDLINK='http://wowcartoon.com:8182/C4C/api/C4C/GetClips'
SEARCHLINK ='http://wowcartoon.com:8182/C4C/api/C4C/FindCategory'

def CATEGORIES():
    addDir('Search','http://wowcartoon.com:8182/C4C/api/C4C/FindCategory',3,'','')            
    addDir('Kids Latest','http://wowcartoon.com:8182/C4C/api/C4C/GetCategories',2,'','')
    addDir('Kids Popular','http://wowcartoon.com:8182/C4C/api/C4C/GetCategories',1,'','')
    addDir('Movies/Tv Latest','http://wowcartoon.com:8182/C4C/api/C4C/GetGenres',2,'','')
    addDir('Movies/Tv Popular','http://wowcartoon.com:8182/C4C/api/C4C/GetGenres',1,'','')

                
    setView('movies', 'default') 
       


def OPEN_URL(url,data,headers):
    import utils
    return utils.GetHTML(url,data,headers)
       
                                                                      
def GetContent(url,pagenum=''):
        if pagenum==None:
            pagenum='0'

        data = {'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
                'Hash':'f93e3156637c9fce37154e2d091bca8a',
                'Key':'AA9FSK1323X3F',
                'Pagesize':'-1',
                'SortType':'1',
                'StartIndex':str(pagenum),
                'Version':'5'}
        #print data
        html = OPEN_URL(url,data,headers)
        link = json.loads(html)
         
        data=link['Data']
        if pagenum=='0':        
            pagenum=len(data)
        else:pagenum=len(data)+80  
        #print data
        for field in data:
            name=field['Name'].encode('utf8')
            iconimage=field['ThumbnailUrl']#.encode('utf8')
            try:
                id=field['GenreId']
                addDir(name,str(id),2001,iconimage,'')
            except:
                id=field['CategoryId']
                addDir(name,str(id),2002,iconimage,'')
        if pagenum % 80 == 0:              
            addDir('[COLOR blue]>> Next Page >>[/COLOR]',url,1,'',str(pagenum))             
        setView('movies', 'movies')

        
def GetContentLatest(url,pagenum=''):
        if pagenum==None:
            pagenum='0'

        data = {'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
                'Hash':'f93e3156637c9fce37154e2d091bca8a',
                'Key':'AA9FSK1323X3F',
                'Pagesize':'-1',
                'SortType':'0',
                'StartIndex':str(pagenum),
                'Version':'5'}
        #print data
        html = OPEN_URL(url,data,headers)
        link = json.loads(html)
         
        data=link['Data']
        if pagenum=='0':        
            pagenum=len(data)
        else:pagenum=len(data)+80    
        #print data
        for field in data:
            name=field['Name'].encode('utf8')
            iconimage=field['ThumbnailUrl']#.encode('utf8')
            try:
                id=field['GenreId']
                addDir(name,str(id),2001,iconimage,'')
            except:
                id=field['CategoryId']
                addDir(name,str(id),2002,iconimage,'')
                
        if pagenum % 80 == 0:              
            addDir('[COLOR blue]>> Next Page >>[/COLOR]',url,1,'',str(pagenum))             
        setView('movies', 'movies')
    


        
def GetLink(url,pagenum=''):
        if pagenum==None:
            pagenum='0'

        data={'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
                  'Hash':'f93e3156637c9fce37154e2d091bca8a',
                  'Key':'AA9FSK1323X3F',
                  'Id':url,
                  'PageSize':'20',
                  'StartIndex':str(pagenum),
                  'Version':'5'}

       
        html = OPEN_URL(GETLINK,data,headers)
        
        link = json.loads(html)
         
        data=link['Data']
        print data
        if pagenum=='0':        
            pagenum=len(data)
        else:pagenum=len(data)+80  
        
        for field in data:
            name=field['Name'].encode('utf8')
            id=field['VideoId']
            iconimage=field['ThumbnailUrl']#.encode('utf8')
            try:addDir(name,str(id),200,iconimage,'')
            except:pass
        if pagenum % 80 == 0:    
            addDir('[COLOR blue]>> Next Page >>[/COLOR]',url,2001,'',str(pagenum))         
        setView('movies', 'default')


def GetKIDLink(url,pagenum=''):
        if pagenum==None:
            pagenum='0'

        data={'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
                  'Hash':'f93e3156637c9fce37154e2d091bca8a',
                  'Key':'AA9FSK1323X3F',
                  'Id':url,
                  'PageSize':'20',
                  'StartIndex':pagenum,
                  'Version':'5'}

       
        html = OPEN_URL(GETKIDLINK,data,headers)
        
        link = json.loads(html)
         
        data=link['Data']
   
        if pagenum=='0':        
            pagenum=len(data)
        else:pagenum=len(data)+80  
        
        for field in data:
            name=field['Name'].encode('utf8')
            id=field['VideoId']
            iconimage=field['ThumbnailUrl']#.encode('utf8')      
            try:addDir(name,str(id),200,iconimage,'')
            except:pass
        if pagenum % 80 == 0:    
            addDir('[COLOR blue]>> Next Page >>[/COLOR]',url,2002,'',str(pagenum))         
               
        setView('movies', 'default')        

def SEARCH(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search Cartoon HD Extra')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText()
        
    data={'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
          'Hash':'f93e3156637c9fce37154e2d091bca8a',
          'Key':'AA9FSK1323X3F',
          'Pagesize':'-1',
          'Keyword':search_entered,
          'StartIndex':'0',
          'Version':'5'}

    html = OPEN_URL(SEARCHLINK,data,headers)
    #print html  
    link = json.loads(html)
     
    data=link['Data']
    print data

    for field in data:
        name=field['Name'].encode('utf8')
        iconimage=field['ThumbnailUrl']#.encode('utf8') 
        id=field['Link']
        if not id:
            id=field['Id']
            addDir(name,str(id),2001,iconimage,'')
        else:    
            addDir(name,str(id),200,iconimage,'')


    setView('movies', 'movies')
        
 

    
def Show_Dialog():
    dialog = xbmcgui.Dialog()
    dialog.ok('Cartoon HD', '',"Files Does Not Exist", "")

def anime(url):
    link=net.http_GET(url).content
    if '>File was deleted<' in link:
        return Show_Dialog()
    URL=[]
    NAME=[]

    match=re.compile('"file" : "(.+?)".+?"label" : "(.+?)"',re.DOTALL).findall(link)
    for urls , res in match:
        URL.append(urls)
        NAME.append(res.replace('o','')+'P')
    return URL[xbmcgui.Dialog().select('Please Select Resolution', NAME)]

def getmpstar(url):
    link=net.http_GET(url).content
    match=re.compile('source src="(.+?)"').findall(link)
    return match[0]

def tunemovie(url):
    link=net.http_GET(url,headers={'Host': 'tunemovie.is','User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'}).content
    #print link
    match=re.compile("source src='(.+?)'").findall(link)
    return match[0]
    
def PLAY_STREAM(name,url,iconimage):
        
    #print url

    if 'redirector.googlevideo' in url:
        url=urllib2.urlopen(url).geturl()
        
    if 'allmyvideos' in url:
        url=anime(url)
        
    if 'mp4star' in url:
        url=getmpstar(url)

    if 'tunemovie.is'in url:
        url=tunemovie(url)

    if 'blogspot' in url:
        url=url
    else:
        import urlresolver
        url=urlresolver.resolve(url)        
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
  
    
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

def addDir(name,url,mode,iconimage,pagenum):
        if not '>>' in name: name=name.title()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&pagenum="+urllib.quote_plus(pagenum)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        menu = []
        if mode ==200:
            liz.setProperty("IsPlayable","true")
            
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=2001&iconimage=None&url=%s)'% (sys.argv[0],name,url)))
            liz.addContextMenuItems(items=menu, replaceItems=False)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
        
 
        
def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
pagenum=None


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
        pagenum=urllib.unquote_plus(params["pagenum"])
except:
        pass

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        #print ""
        CATEGORIES()
       
elif mode==1:
        #print ""+url
        GetContent(url,pagenum)

elif mode==2:
        #print ""+url
        GetContentLatest(url,pagenum)
elif mode==3:
        #print ""+url
        SEARCH(url)                
        
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

elif mode==2001:

        GetLink(url,pagenum)

elif mode==2002:

        GetKIDLink(url,pagenum)         
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
