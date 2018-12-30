import util, urllib2, re, urllib, base64, difflib, time, json, base64, HTMLParser
import xbmcaddon,xbmcplugin,xbmcgui

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
       
ADDON_ID='plugin.video.woodrocket'

sysarg=str(sys.argv[1]) 

# This function implements a horrible hack related to python 2.4's terrible unicode handling.
def makeAscii(data):
    #log(repr(data), 5)
    #if sys.hexversion >= 0x02050000:
    #        return data

    try:
        return data.encode('ascii', "ignore")
    except:
        #log("Hit except on : " + repr(data))
        s = u""
        for i in data:
            try:
                i.encode("ascii", "ignore")
            except:
                #log("Can't convert character", 4)
                continue
            else:
                s += i

        #log(repr(s), 5)
        return s

def replaceHTMLCodes(txt):
    #log(repr(txt), 5)

    # Fix missing ; in &#<number>;
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))

    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&amp;", "&")
    #log(repr(txt), 5)
    return txt

# This function handles stupid utf handling in python.
def makeUTF8(data):
    #log(repr(data), 5)
    return data
    try:
        return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
    except:
        #log("Hit except on : " + repr(data))
        s = u""
        for i in data:
            try:
                i.decode("utf8", "xmlcharrefreplace") 
            except:
                #log("Can't convert character", 4)
                continue
            else:
                s += i
        #log(repr(s), 5)
        return s

def getCategories(params) :
    param={'categories':1}
    content=util.getURL(params['url'], hdr)
    if content!=False:
        contents=util.extract(content, '<ul class="small-block-grid-4 videos-cats">', '</ul>')
        films=util.extractAll(contents, '<li>', '</li>')
        for film in films:
            
            title=util.extract(film, '<div class="media-panel-title category-title">', '</div>')
            
            param['title']=util.extract(title, '">', '</a>')
            param['plot']=util.extract(film, '<div class="media-panel-info">', '</div>')
            param['url']=util.extract(title, '<a href="', '"')
            param['poster']=util.extract(film, '<img src="', '" />')
            param['fanart']=param['poster']
            
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&mode=2&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": param['plot']} )
                liz.setProperty("Fanart_Image", param['fanart'])
                liz.setProperty("Landscape_Image", param['fanart'])
                liz.setProperty("Poster_Image", param['poster'])
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        next=util.extract(content, '<div class="pagination">', '</div>')
        if next!=None:
            next=util.extract(next, '<li class="active">', '</a>')
            if next!=None:
                url=util.extract(next, '<a href="', '"')
                util.addDir("Next >", url, 2, "","")
        xbmcplugin.endOfDirectory(int(sysarg))
        
def getSeries(params) :
    param={'series':1}
    content=util.getURL(params['url'], hdr)
    if content!=False:
        contents=util.extract(content, '<ul class="small-block-grid-4 series">', '</ul>')
        films=util.extractAll(contents, '<li>', '</li>')
        for film in films:
            
            title=util.extract(film, '<div class="media-panel-title series-title">', '</div>')
            
            param['title']=util.extract(title, '">', '</a>')
            param['plot']=util.extract(film, '<div class="media-panel-info">', '</div>')
            param['url']=util.extract(title, '<a href="', '"')
            param['poster']=util.extract(film, '<img src="', '" />')
            param['fanart']=param['poster']
            
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&mode=2&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": param['plot']} )
                liz.setProperty("Fanart_Image", param['fanart'])
                liz.setProperty("Landscape_Image", param['fanart'])
                liz.setProperty("Poster_Image", param['poster'])
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        next=util.extract(content, '<div class="pagination">', '</div>')
        if next!=None:
            next=util.extract(next, '<li class="active">', '</a>')
            if next!=None:
                url=util.extract(next, '<a href="', '"')
                util.addDir("Next >", url, 2, "","")
        xbmcplugin.endOfDirectory(int(sysarg))
        
def getVids(params) :
    param={'play':1}
    
    content=util.getURL(params['url'], hdr)
    if content!=False:
        contents=util.extract(content, '<ul class="small-block-grid-4 videos">', '</ul>')
        films=util.extractAll(contents, '<li>', '</li>')
        for film in films:
            param['title']=util.extract(film, 'class="video-title" title="', '"')
            param['url']=util.extract(film, '<a href="', '" class="video-image"')
            param['poster']=util.extract(film, '<img src="', '" />')
            param['fanart']=param['poster']
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&play="+str(4)+"&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": ""} )
                liz.setProperty("Fanart_Image", param['fanart'])
                liz.setProperty("Landscape_Image", param['fanart'])
                liz.setProperty("Poster_Image", param['poster'])
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        next=util.extract(content, '<div class="pagination">', '</div>')
        if next!=None:
            next=util.extract(next, '<li class="active">', '</a>')
            if next!=None:
                url=util.extract(next, '<a href="', '"')
                util.addDir("Next >", url, 2, "","")
        xbmcplugin.endOfDirectory(int(sysarg))

def buildMainMenu():
    util.addDir("Newest","http://woodrocket.com/newest-porn", 2, "","")
    util.addDir("Whats Hot", "http://woodrocket.com/whats-hot", 2, "", "")
    util.addDir("Web Series","http://woodrocket.com/series", 5, "","")
    util.addDir("Exclusives","http://woodrocket.com/exclusive", 2, "","")
    util.addDir("Categories","http://woodrocket.com/categories", 6, "","")
    util.addDir("Stars","http://woodrocket.com/stars", 3, "","")
    util.addDir("Search","Search", 4, "","")
    xbmcplugin.endOfDirectory(int(sysarg))

def getStars(params):
    content=util.getURL(params['url'], hdr)
    if content!=False:
        alphabet=util.extractAll(content, "<ul class='small-block-grid-5 stars'>", '</ul>')
        for letter in alphabet:
            stars=util.extractAll(letter, '<li>', '</li>')
            for star in stars:
                name=util.extract(star, '">', '</a>')
                url=util.extract(star, 'href="', '"')
                util.addDir(name, url, 2, "","")
    xbmcplugin.endOfDirectory(int(sysarg))
    
def search():
    term=util.searchBox()
    params={'search':1}
    params['url']="http://woodrocket.com/search-videos/"+term
    getVids(params)
    
def fileInfo():
    return ((((((('&'+base64.b64decode(base64.b64decode('Ykc5bmFXND0=')))+'=')+base64.b64decode(base64.b64decode('WmpjMU1HSXlOalV4TTJZMk5EQXpOQT09')))+'&')+base64.b64decode(base64.b64decode('YTJWNQ==')))+'=')+base64.b64decode(base64.b64decode('YjJGQkxVMWlXbTg9')))
    
def playVideo(params):
    content=util.getURL(params['url'], hdr)
    if content!=False:
        vidID=util.extract(content, 'file: "http://videos.woodrocket.com/vid/', '.mp4", label: "480p"')
        source=util.extract(content, 'sources: [', '],')
        if 'label: "720p HD"' in source:
            util.playMedia(params['name'], params['poster'], "http://videos.woodrocket.com/vid/"+vidID+".hd.mp4", "Video")
        else:
            util.playMedia(params['name'], params['poster'], "http://videos.woodrocket.com/vid/"+vidID+".mp4", "Video")

parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None

if mode==2:
    getVids(parameters)
elif mode==3:
    getStars(parameters)
elif mode==4:
    # search code goes here!!
    search()
elif mode==5:
    getSeries(parameters)
elif mode==6:
    getCategories(parameters)
elif 'series' in parameters:
    getVids(paramters)
elif 'play' in parameters:
    playVideo(parameters)
else :
    buildMainMenu()
