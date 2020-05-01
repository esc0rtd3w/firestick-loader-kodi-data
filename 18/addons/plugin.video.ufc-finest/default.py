import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil,urlresolver,resolveurl,random,liveresolver
from resources.libs.common_addon import Addon
import base64
from metahandler import metahandlers
from resources.libs import dom_parser

addon_id        = 'plugin.video.ufc-finest'
addon           = Addon(addon_id, sys.argv)
AddonTitle          = '[COLOR red]Planet[/COLOR] [COLOR white]MMA[/COLOR]'
selfAddon       = xbmcaddon.Addon(id=addon_id)
PLEXUS_PATH         = xbmc.translatePath('special://home/addons/program.plexus')
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
fanarts         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
DATA_FOLDER         = xbmc.translatePath(os.path.join('special://profile/addon_data/' , addon_id))
searchicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'search.jpg'))
newicon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'whatsnew.jpg'))
nextpage        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'next.png'))
realdebrid      = xbmc.translatePath(os.path.join('http://i.imgur.com/uSSYjMb.png'))
sd_path         = xbmc.translatePath(os.path.join('special://home/addons/', 'plugin.video.sportsdevil'))
dp                  = xbmcgui.DialogProgress()
REDDIT_FILE         = xbmc.translatePath(os.path.join(DATA_FOLDER, 'reddit.xml'))
PLEXUS_PATH         = xbmc.translatePath('special://home/addons/program.plexus')
baseurl         = 'http://supremacy.org.uk/MMA/ufcmain.xml'
ytpl            = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
ytpl2           = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
ytplpg1         = 'https://www.googleapis.com/youtube/v3/playlistItems?pageToken='
ytplpg2         = '&part=snippet&playlistId='
ytplpg3         = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
adultpass       = selfAddon.getSetting('password')
metaset         = selfAddon.getSetting('enable_meta')
messagetext     = 'http://supremacy.org.uk/MMA/startinfo.xml'
startinfo       = 'http://supremacy.org.uk/MMA/startinfo.xml'
SEARCH_LIST     = 'http://supremacy.org.uk/MMA/search.xml'
dialog          = xbmcgui.Dialog()
                                                               
def GetMenu():
    popup()
    xbmc.executebuiltin('Container.SetViewMode(500)')
    url = baseurl
    addDir('[B][COLOR red]I[/COLOR][/B][B][COLOR white]nformation[/COLOR][/B]',url,10,newicon,fanarts)
    addDir('[B][COLOR red]S[/COLOR][/B][B][COLOR white]earch[/COLOR][/B]',url,5,searchicon,fanarts)        
    addItem('[B][COLOR white]'+'Real Debrid Login'+'[/COLOR]''[/B]','url',16,realdebrid,fanarts)
    link=open_url(baseurl)
    match= re.compile('<item>(.+?)</item>').findall(link)
    for item in match:
        try:
            if '<channel>' in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    url=re.compile('<channel>(.+?)</channel>').findall(item)[0]
                    addDir(name,url,6,iconimage,fanart)
            elif '<playlist>' in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    url=re.compile('<playlist>(.+?)</playlist>').findall(item)[0]
                    addDir(name,url,43,iconimage,fanart)
            elif '<mma_openload>' in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    url=re.compile('<mma_openload>(.+?)</mma_openload>').findall(item)[0]
                    addDir(name,url,13,iconimage,fanart)
            elif "<reddit>" in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    url=re.compile('<reddit>(.+?)</reddit>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    addDir(name,'url',320,iconimage,fanart,'')           
            elif "<reddit_link>" in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    url=re.compile('<reddit_link>(.+?)</reddit_link>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    addDir(name,url,319,iconimage,fanart,'')
            elif "<redditevents>" in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    url=re.compile('<redditevents>(.+?)</redditevents>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    addDir(name,url,317,iconimage,fanart,'')
            elif "<reddit_suggested>" in item:
                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    url=re.compile('<reddit_suggested>(.+?)</reddit_suggested>').findall(item)[0]
                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                    addDir(name,url,322,iconimage,fanart,'')                     
            if '<sportsdevil>' in item:
                    links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)
                    if len(links)==1:
                         name=re.compile('<title>(.+?)</title>').findall(item)[0]
                         iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                         url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                         referer=re.compile('<referer>(.+?)</referer>').findall(item)[0]
                         check = referer
                         suffix = "/"
                         if not check.endswith(suffix):
                             refer = check + "/"
                         else:
                             refer = check
                         link = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                         url = link + '%26referer=' +refer
                         addItem(name,url,4,iconimage,fanart)   
                    elif len(links)>1:
                         name=re.compile('<title>(.+?)</title>').findall(item)[0]
                         iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                         fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                         addItem(name,url2,8,iconimage,fanart)       
            elif '<folder>'in item:
                            data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                            for name,url,iconimage,fanart in data:
                                    addDir(name,url,1,iconimage,fanart)
            else:
                            links=re.compile('<link>(.+?)</link>').findall(item)
                            if len(links)==1:
                                    data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                    lcount=len(match)
                                    for name,url,iconimage,fanart in data:
                                            if 'youtube.com/playlist' in url:
                                                    addDir(name,url,2,iconimage,fanart)
                                            else:
                                                    addLink(name,url,2,iconimage,fanart)
                            elif len(links)>1:
                                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                    fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                                    addLink(name,url2,3,iconimage,fanart)
        except:pass
        view(link)


		
        
        
    #view(link)
def CLEANUP(text):

    text = str(text)
    text = text.replace('\\r','')
    text = text.replace('\\n','')
    text = text.replace('\\t','')
    text = text.replace('\\','')
    text = text.replace('<br />','\n')
    text = text.replace('<hr />','')
    text = text.replace('&#039;',"'")
    text = text.replace('&#39;',"'")
    text = text.replace('&quot;','"')
    text = text.replace('&rsquo;',"'")
    text = text.replace('&amp;',"&")
    text = text.replace('&#8211;',"&")
    text = text.replace('&#8217;',"'")
    text = text.replace('&#038;',"&")
    text = text.replace('&#8211;',"-")
    text = text.lstrip(' ')
    text = text.lstrip('	')

    return text

def popup():
        message=open_url2(startinfo)
        if len(message)>1:
                path = xbmcaddon.Addon().getAddonInfo('path')
                comparefile = os.path.join(os.path.join(path,''), 'compare.txt')
                r = open(comparefile)
                compfile = r.read()       
                if compfile == message:pass
                else:
                        showText('[B][COLOR white]IMPORTANT[/COLOR] [COLOR red]NEWS[/COLOR] [COLOR white]AND[/COLOR] [COLOR red]INFO[/COLOR][/B]', message)
                        text_file = open(comparefile, "w")
                        text_file.write(message)
                        text_file.close()

def resolver_settings():
    resolveurl.display_settings()
                        
def GetContent(name,url,iconimage,fanart):
        url2=url
        link=open_url(url)

        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
            try:
                if '<channel>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<channel>(.+?)</channel>').findall(item)[0]
                        addDir(name,url,6,iconimage,fanart)
                if '<image>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<image>(.+?)</image>').findall(item)[0]
                        addDir(name,iconimage,9,iconimage,fanart)
                elif '<playlist>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<playlist>(.+?)</playlist>').findall(item)[0]
                        addDir(name,url,43,iconimage,fanart)
                elif "<reddit>" in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        url=re.compile('<reddit>(.+?)</reddit>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        addDir(name,'url',320,iconimage,fanart,'')
                elif "<reddit_link>" in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        url=re.compile('<reddit_link>(.+?)</reddit_link>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        addDir(name,url,319,iconimage,fanart,'')
                elif "<redditevents>" in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        url=re.compile('<redditevents>(.+?)</redditevents>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        addDir(name,url,317,iconimage,fanart,'')
                elif "<reddit_suggested>" in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        url=re.compile('<reddit_suggested>(.+?)</reddit_suggested>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        addDir(name,url,322,iconimage,fanart,'')
                        
                elif '<dx-tv>' in item:
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        url=re.compile('<dx-tv>(.+?)</dx-tv>').findall(item)[0]
                        addDir(name,url,13,iconimage,fanart)
                elif ('<sportsdevil>' in item) and ('<link>' in item):
                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                        addItem(name,url2,8,iconimage,fanart)
                if '<sportsdevil>' in item:
                        links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)
                        if len(links)==1:
                             name=re.compile('<title>(.+?)</title>').findall(item)[0]
                             iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                             url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                             referer=re.compile('<referer>(.+?)</referer>').findall(item)[0]
                             check = referer
                             suffix = "/"
                             if not check.endswith(suffix):
                                 refer = check + "/"
                             else:
                                 refer = check
                             link = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                             url = link + '%26referer=' +refer
                             addItem(name,url,4,iconimage,fanart)   
                        elif len(links)>1:
                             name=re.compile('<title>(.+?)</title>').findall(item)[0]
                             iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                             fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                             addItem(name,url2,8,iconimage,fanart)
    
                elif '<folder>'in item:
                                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                for name,url,iconimage,fanart in data:
                                        addDir(name,url,1,iconimage,fanart)
                else:
                                links=re.compile('<link>(.+?)</link>').findall(item)
                                if len(links)==1:
                                        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                        lcount=len(match)
                                        for name,url,iconimage,fanart in data:
                                                if 'youtube.com/playlist' in url:
                                                        addDir(name,url,2,iconimage,fanart)
                                                else:
                                                        addLink(name,url,2,iconimage,fanart)
                                elif len(links)>1:
                                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                                        addLink(name,url2,3,iconimage,fanart)
            except:pass
            view(link)

def YOUTUBE_CHANNEL(url):

	CHANNEL = RUNNER + url
	link = open_url(CHANNEL)
	patron = "<video>(.*?)</video>"
	videos = re.findall(patron,link,re.DOTALL)

	items = []
	for video in videos:
		item = {}
		item["name"] = find_single_match(video,"<name>([^<]+)</name>")
		item["url"] = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9") + find_single_match(video,"<id>([^<]+)</id>")
		item["author"] = find_single_match(video,"<author>([^<]+)</author>")
		item["iconimage"] = find_single_match(video,"<iconimage>([^<]+)</iconimage>")
		item["date"] = find_single_match(video,"<date>([^<]+)</date>")
		
		addLink('[COLOR white]' + item["name"] + ' - on ' + item["date"] + '[/COLOR]',item["url"],7,item["iconimage"],fanart)

                
	
def CLEANUP(text):

    text = str(text)
    text = text.replace('\\r','')
    text = text.replace('\\n','')
    text = text.replace('\\t','')
    text = text.replace('\\','')
    text = text.replace('<br />','\n')
    text = text.replace('<hr />','')
    text = text.replace('&#039;',"'")
    text = text.replace('&#39;',"'")
    text = text.replace('&quot;','"')
    text = text.replace('&rsquo;',"'")
    text = text.replace('&amp;',"&")
    text = text.replace('&#8211;',"&")
    text = text.replace('&#8217;',"'")
    text = text.replace('&#038;',"&")
    text = text.replace('&nbsp;'," ")
    text = text.lstrip(' ')
    text = text.lstrip('    ')

def NEW():
        message=open_url2(messagetext)
        if len(message)>1:
                path = xbmcaddon.Addon().getAddonInfo('path')
                showText('[B][COLOR white]Whats[/COLOR] [COLOR red]New[/COLOR][/B]', message)
                quit()

def DXTV_CATS(url):

    u = open_url(url)
    match = re.compile('<article class=".+?">.+?<a href="(.+?)" title="(.+?)" rel="nofollow" id="featured-thumbnail">.+?<img.+?src="(.+?)".+?</article>',re.DOTALL).findall(u)
    for url2,name,image in match:
        name = name.replace('Watch','').replace('Download','').replace('online','').replace('/','').encode('utf-8').lstrip()
        url2 = url2.encode('utf-8')
        iconimage = image.encode('utf-8')
        addLink(name,url2,15,iconimage,fanart)
    np = re.compile("<div class=\"pagination pagination-numeric\">.+?<li class='current'><span class='currenttext'>.+?</span></li><li><a rel='nofollow' href='(.+?)' class='inactive'>.+?</a>").findall(u)
    for nextpage in np:	
        addDir('Next Page -->',nextpage,13,icon,fanart)

def DXTV_LINKS(name,url):

    xbmc.executebuiltin("ActivateWindow(busydialog)")

    r = open_url(url)
    r = re.compile('<ifram.+?src="(.+?)"').findall(r)# + re.compile('<span style="color: #008000;"><strong>(.+?)</strong>',re.DOTALL).findall(r)
    
    if len(r) == 0: quit()
    elif len(r) >= 1:
        streamurl=[]
        streamname=[]
        a = 0
        for b in r:
            b = b.lstrip()
            if resolveurl.HostedMediaFile(b).valid_url():
                a += 1
                streamurl.append(b)
                streamname.append('Link %s' % str(a))
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        if len(streamurl) == 1: PLAYLINK(name,streamurl[0],icon)
        else:
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,streamname)
            if select < 0:
                quit()
            else:
                PLAYLINK(name,streamurl[select],icon)

def CALANDER():

    items = json.loads(open_url('http://calendar.ufc.com/unitedkingdom/EventsList?eventIds=&externalEventIds='))

    if items: 
        for entry in items['DataBag']:
                if "Name" in entry:
                    name = entry['Name'].encode('utf-8')
                else:
                    name = "No Name Found"
                if "StartDateTime" in entry:
                    time = entry['StartDateTime'].encode('utf-8')
                else:
                    time = "No Name Found"

                a,b = time.split('T')
                f = a.split('-')
                a = ''
                for i in reversed(f):
                    a = a + i + '-'    
                a = a.rstrip('-')
                f = b.split(':')
                b = ''
                for i in f[:-1]:
                    b = b + i + ':'    
                b = b.rstrip(':')                               
                time = ('%s GMT - %s' % (b,a))
                name = name.replace('\xf0\x9f\x91\x8a  ','')
                display =  ('[B][COLOR white]%s[/COLOR] | [COLOR red]%s[/COLOR][/B]' % (name,time)) 
                addLink(display,'url',999,cal_icon,fanarts)
                

def REDDIT_MAIN():

    xbmc.executebuiltin("ActivateWindow(busydialog)")

    addDir('Click for Recommended Reddits','url',322,icon,fanarts)
    addLink('Add A Reddit/Subreddit','url',321,icon,fanarts)
    addLink('-----------------------------------','url',999,icon,fanarts)
    addLink('User Added Reddits','url',999,iconimage,fanart)

    if os.path.exists(REDDIT_FILE):
        f = open(REDDIT_FILE,mode='r'); msg = f.read(); f.close()
        msg = msg.replace('\n','')
        if '<item>' in msg:
            match = re.compile('<item>(.+?)</item>').findall(msg)
            for item in match:
                name=re.compile('<name>(.+?)</name>').findall(item)[0]
                url=re.compile('<url>(.+?)</url>').findall(item)[0]
                cm=[]
                cm.append(('Remove from list','XBMC.RunPlugin(%s?mode=323&name=%s&url=%s)'% (sys.argv[0],name,url)))
                addDir('[COLOR white]' + name.encode('utf-8') + '[/COLOR]',url.encode('utf-8'),319,iconimage,fanart,'',cm)
        else: addLink('No user added Reddits detected.','url',999,iconimage,fanart)
    xbmc.executebuiltin("Dialog.Close(busydialog)")

def REDDIT_ADD():

    xbmc.executebuiltin("ActivateWindow(busydialog)")
    if not os.path.isfile(REDDIT_FILE):
        f = open(REDDIT_FILE,'w'); f.write('#START OF FILE#'); f.close()

    string =''
    keyboard = xbmc.Keyboard(string, 'Enter Reddit URL/Name')
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText()
        if len(string)>1:
            if not 'http' in string.lower(): string = 'https://www.reddit.com/r/' + string
            r = open_url_m3u(string)
            if '<p id="noresults" class="error">' in r:
                dialog.ok(AddonTitle, 'An invalid URL has been entered.')
                xbmc.executebuiltin("Dialog.Close(busydialog)")
                quit()
            url = string
        else: 
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            quit()
    else: 
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        quit()
    
    try:
        name = re.compile('<h1 class="hover redditname">.+?>(.+?)<\/a>').findall(r)[0]
        a=open(REDDIT_FILE).read()
        b=a.replace('#START OF FILE#', '#START OF FILE#\n<item>\n<name>'+str(name)+'</name>\n<url>'+str(url)+'</url>\n</item>\n')
        f= open(REDDIT_FILE, mode='w')
        f.write(str(b))
        f.close()
    except:
        dialog.ok(AddonTitle, 'Sorry, we were unable to add this Reddit.')
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        quit()
    dialog.ok(AddonTitle, name + ' has been added!')
    xbmc.executebuiltin("Dialog.Close(busydialog)")
    xbmc.executebuiltin("Container.Refresh")

def REDDIT_SUGGESTED():

    r = open_url('http://supremacy.org.uk/MMA/suggested.xml')
    
    r = re.compile('<link>(.+?)</link>').findall(r)

    for u in r:

        r = open_url_m3u(u)
            
        try:
            name = re.compile('<h1 class="hover redditname">.+?>(.+?)<\/a>').findall(r)[0]
            addDir(name.encode('utf-8'),u,319,icon,fanarts)
        except: pass
        
def REDDIT_GET(url):

    r = open_url_m3u(url)
    
    if not 'comments' in url:
    
        namelist = []; urllist = []; scorelist = []; commentlist = []; combinedlist = []
        try:
            sitename = re.compile('<h1 class="hover redditname">.+?>(.+?)<\/a>').findall(r)[0]
            addLink('[COLORwhite][B]Welcome to the ' + sitename.title() + ' Reddit![/B][/COLOR]','url',999,icon,fanart)
        except: pass
        
        r = dom_parser.parse_dom(r, 'div', {'class': re.compile('\sthing\sid')})

        if r:
            for i in r:
                title = re.compile('<a class="title may-blank.+?rel=".+?>(.+?)<').findall(i.content)[0]
                url = re.compile('href="([^"]+)').findall(i.content)
                url = [u for u in url if ('comments' in u) and ('reddit' in u)]
                try: score = re.compile('<div class="score unvoted" title=".+?">([0-9]+)</div>').findall(i.content)[0]
                except: score = '0'
                try: comments = re.compile('data-event-action="comments".+?>([0-9]+)\scomments<\/a>').findall(i.content)[0]
                except: comments = '0'

                if 'comments' in url[0]:
                    url = url[0]
                    if not 'reddit.com' in url: url = 'https://www.reddit.com' + url
                    namelist.append(title.encode('utf-8'))
                    urllist.append(url.encode('utf-8'))
                    scorelist.append(score.encode('utf-8'))
                    commentlist.append(comments.encode('utf-8'))
                    combinedlist = list(zip(scorelist,namelist,urllist,commentlist))

            #tup = sorted(combinedlist, key=lambda x: int(x[0]),reverse=True)
            for score,title,url,comments in combinedlist:
                title = title.replace('&amp;','&')
                addDir('[COLORwhite][B]' + score + '[/B][/COLOR] - [COLOR white]' + title + '[/COLOR] - ' + comments + ' Comments',url,319,icon,fanarts)
        else: addLink('No Sub Reddits Found','url',999,icon,fanart)

    else:
        
        checks = ['acestream','href']
        black = ['ads']
        s = 1

        r = dom_parser.parse_dom(r, 'div', {'class': re.compile('md')})
        ace = re.compile('([0-9a-z]+)').findall(str(r))
        e = [i for i in ace if len(i) == 40]
        u = [i[1] for i in r[1:] if ('<p>' in i[1]) and any(f for f in checks if f in i[1]) and not any(f for f in black if f in i[1])]
        r = re.findall('acestream:\/\/([0-9 a-z]+)[\s|<]', str(u)) + re.findall('<a href=\"http(.+?)\"', str(u))
        a = []
        a.extend(e)
        a.extend(r)

        combined  = []

        if a:
            countlist = []
            namelist  = []
            urllist   = []
            for i in a:
                if not i.endswith(('.jpg','.jpeg','.png','.gif')):
                    i = i.encode('utf-8')
                    if '://' in i: i = 'http' + i
                    if not 'reddit' in i:
                        if not 'http' in i:
                            if os.path.exists(PLEXUS_PATH): 
                                name = '[COLORwhite][B]Link ' + str(s) + '[/B][/COLOR] - Acestream: ' + i
                                namelist.append(name)
                                if not i in urllist: urllist.append('acestream://'+i)
                                countlist.append('0')
                                combined = list(zip(countlist,namelist,urllist))
                                s += 1
                        else: 
                            name = '[COLORwhite][B]Link ' + str(s) + '[/B][/COLOR] - ' + i
                            namelist.append(name)
                            if not i in urllist: urllist.append(i)
                            countlist.append('1')
                            combined = list(zip(countlist,namelist,urllist))
                            s += 1
            if s == 1: addLink('No Links Found','url',999,icon,fanart)
        else: addLink('No Links Found','url',999,icon,fanart)

        if combined:
            ace_got  = 0
            http_got = 0
            tup = sorted(combined, key=lambda x: int(x[0]))
            for count,name,url in tup:
                if count == '0': 
                    if ace_got == 0:
                        addLink('[COLOR white][B]| Acestream Links | [I]Most Recent At Bottom[/I] |[/B][/COLOR]','url',999,icon,fanart)
                        ace_got = 1
                    addLink(name.encode('utf-8'),url,318,icon,fanart)
                else:
                    if http_got == 0:

                        addLink('[COLOR white][B]| Web Links | [I]Most Recent At Bottom[/I] |[/B][/COLOR]','url',999,icon,fanart)
                        
                        http_got = 1
                    addLink(name.encode('utf-8'),url,318,icon,fanart)
        
def REDDIT_REMOVE(name,url):

    try:
        name = name.replace('[COLORwhite]','').replace('[/COLOR]','')
        a=open(REDDIT_FILE).read()
        b=a.replace('<item>\n<name>'+str(name)+'</name>\n<url>'+str(url)+'</url>\n</item>','')
        f=open(REDDIT_FILE, mode='w')
        f.write(str(b))
        xbmc.executebuiltin("Container.Refresh")
    except:
        dialog.ok(AddonTitle,'There was an error removing the entry from the list.')
        quit()
        
def EVENT_REDDIT():

    r = open_url('https://pastebin.com/raw/6w0TPFBx')
    r = re.compile('<link>(.+?)</link>').findall(r)
    
    checks = ['acestream','href']
    black = ['ads']
    s = 1
    for u in r:
        r = open_url(u)
        checks = ['acestream','href']
        black = ['ads']
        s = 1

        r = dom_parser.parse_dom(r, 'div', {'class': re.compile('md')})
        ace = re.compile('([0-9a-z]+)').findall(str(r))
        e = [i for i in ace if len(i) == 40]
        u = [i[1] for i in r[1:] if ('<p>' in i[1]) and any(f for f in checks if f in i[1]) and not any(f for f in black if f in i[1])]
        r = re.findall('acestream:\/\/([0-9 a-z]+)[\s|<]', str(u)) + re.findall('<a href=\"http(.+?)\"', str(u))
        a = []
        a.extend(e)
        a.extend(r)

        combined  = []

        if a:
            countlist = []
            namelist  = []
            urllist   = []
            for i in a:
                if not i.endswith(('.jpg','.jpeg','.png','.gif')):
                    i = i.encode('utf-8')
                    if '://' in i: i = 'http' + i
                    if not 'reddit' in i:
                        if not 'http' in i:
                            if os.path.exists(PLEXUS_PATH): 
                                name = '[COLORwhite][B]Link ' + str(s) + '[/B][/COLOR] - Acestream: ' + i
                                namelist.append(name)
                                urllist.append('acestream://'+i)
                                countlist.append('0')
                                combined = list(zip(countlist,namelist,urllist))
                                s += 1
                        else: 
                            name = '[COLORwhite][B]Link ' + str(s) + '[/B][/COLOR] - ' + i
                            namelist.append(name)
                            urllist.append(i)
                            countlist.append('1')
                            combined = list(zip(countlist,namelist,urllist))
                            s += 1
            if s == 1: addLink('No Links Found','url',999,icon,fanart)
        else: addLink('No Links Found','url',999,icon,fanart)

        if combined:
            ace_got  = 0
            http_got = 0
            tup = sorted(combined, key=lambda x: int(x[0]),reverse=False)
            for count,name,url in tup:
                if count == '0': 
                    if ace_got == 0:

                        addLink('[COLORwhite][B]| Acestream Links | [I]Most Recent At Bottom[/I] |[/B][/COLOR]','url',999,icon,fanart)
                        
                        ace_got = 1
                    addLink(name.encode('utf-8'),url,318,icon,fanart)
                else:
                    if http_got == 0:
                        
                        addLink('[COLORwhite][B]| Web Links | [I]Most Recent At Bottom[/I] |[/B][/COLOR]','url',999,icon,fanart)
                        
                        http_got = 1
                    addLink(name.encode('utf-8'),url,318,icon,fanart)

def REDDIT_PLAYER(name,url,iconimage):

    dp.create(AddonTitle,"[COLORred]Opening link...[/COLOR]",'[COLOR white]Please wait...[/COLOR]','')   
    dp.update(0)
    import resolveurl
    import liveresolver
    if 'acestream' in url: url = "plugin://program.plexus/?url="+url+"&mode=1&name=acestream+"+name
    elif '.m3u8' in url:
        url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&amp;name='+name+'&amp;url='+url+'&amp;iconImage='+iconimage  
    elif '.ts'in url:
        url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+name+'&amp;url='+url+'&amp;iconImage='+iconimage  
    elif resolveurl.HostedMediaFile(url).valid_url(): 
        url = resolveurl.HostedMediaFile(url).resolve()
        liz = xbmcgui.ListItem(name,iconImage=iconimage, thumbnailImage=iconimage)
        liz.setPath(url)
        dp.close()
        xbmc.Player ().play(url, liz, False)
    elif liveresolver.isValid(url)==True:
        url=liveresolver.resolve(url)
        liz = xbmcgui.ListItem(name,iconImage=iconimage, thumbnailImage=iconimage)
        liz.setPath(url)
        dp.close()
        xbmc.Player ().play(url, liz, False)
    else:
        url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26title='+str(name)+'%26url=' + url + '%26referer=none'    
    liz = xbmcgui.ListItem(name,iconImage=iconimage, thumbnailImage=iconimage)
    liz.setPath(url)
    dp.close()
    xbmc.Player ().play(url, liz, False)

def open_url_m3u(url):

    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        response = urllib2.urlopen(req, timeout = 10)
        link=response.read()
        response.close()
        return link
    except Exception as e:
        if ('tls' in str(e).lower()) or ('ssl' in str(e).lower()):
            kodi.notify(msg='Error connecting to the URL due to a TLS/SSL issue.', duration=5000, sound=True)
            quit()
        else:
            kodi.notify(msg='URL Error. Please try again.', duration=5000, sound=True)
            quit()

def SEARCH():
	keyb = xbmc.Keyboard('', '[B][COLOR white]Search[/COLOR] [COLOR red]Planet[/COLOR] [COLOR white]MMA[/COLOR][/B]')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchterm=keyb.getText()
		searchterm=searchterm.upper()
	else:quit()
	link=open_url(SEARCH_LIST)
	slist=re.compile('<link>(.+?)</link>').findall(link)
	for url in slist:
                url2=url
                link=open_url(url)
                entries= re.compile('<item>(.+?)</item>').findall(link)
                for item in entries:
                        match=re.compile('<title>(.+?)</title>').findall(item)
                        for title in match:
                                title=title.upper()
                                if searchterm in title:
                                    try:
                                        if '<sportsdevil>' in item:
                                                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]            
                                                url=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(item)[0]
                                                referer=re.compile('<referer>(.+?)</referer>').findall(item)[0]
                                                link = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
                                                url = link + '%26referer=' +referer
                                                if 'tp' in url:
                                                        addLink(name,url,4,iconimage,fanarts)       
                                        elif '<folder>'in item:
                                                        data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                                        for name,url,iconimage,fanart in data:
                                                                if 'tp' in url:
                                                                        addDir(name,url,1,iconimage,fanarts)
                                        else:
                                                        links=re.compile('<link>(.+?)</link>').findall(item)
                                                        if len(links)==1:
                                                                data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                                                lcount=len(match)
                                                                for name,url,iconimage,fanart in data:
                                                                        if 'youtube.com/playlist' in url:
                                                                                addDir(name,url,2,iconimage,fanarts)
                                                                        else:
                                                                                if 'tp' in url: 
                                                                                        addLink(name,url,2,iconimage,fanarts)
                                                        elif len(links)>1:
                                                                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                                                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                                                addLink(name,url2,3,iconimage,fanarts)
                                    except:pass       
                        
		
def GETMULTI(name,url,iconimage):
    
	dp.create(AddonTitle,"[COLORred]Opening Link...[/COLOR]",'[COLORwhite][/COLOR]','')           
	dp.update(0)
    
	streamurl=[]
	streamname=[]
	streamicon=[]
	link=open_url(url)
	urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
	iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
	links=re.compile('<link>(.+?)</link>').findall(urls)
	i=1
	for sturl in links:
                sturl2=sturl
                if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                else:
                        streamurl.append( sturl )
                        streamname.append( 'Link '+str(i) )
                i=i+1
	name='[COLOR red]'+name+'[/COLOR]'
	dialog = xbmcgui.Dialog()
	select = dialog.select(name,streamname)
	if select < 0:
		quit()
	else:
		url = streamurl[select]
		print url
		if resolveurl.HostedMediaFile(url).valid_url(): stream_url = resolveurl.HostedMediaFile(url).resolve()
                elif liveresolver.isValid(url)==True: stream_url=liveresolver.resolve(url)
                else: stream_url=url
                liz = xbmcgui.ListItem(name,iconImage='DefaultVideo.png', thumbnailImage=iconimage)
                liz.setPath(stream_url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                
def GETMULTI_SD(name,url,iconimage):

    sdbase = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='
    streamurl=[]
    streamname=[]
    streamicon=[]
    streamnumber=[]
    link=open_url(url)
    urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
    links=re.compile('<sportsdevil>(.+?)</sportsdevil>').findall(urls)
    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
    i=1

    for sturl in links:
                sturl2=sturl
                if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                        streamnumber.append('Stream ' + str(i))
                else:
                        streamurl.append( sturl )
                        streamname.append( 'Link '+str(i) )

                i=i+1
    name='[COLOR red]'+name+'[/COLOR]'
    dialog = xbmcgui.Dialog()
    select = dialog.select(name,streamname)
    if select < 0:
        quit()
    else:
        check = streamname[select]
        suffix = "/"
        if not check.endswith(suffix):
              refer = check + "/"
        else:
              refer = check
        url = sdbase + streamurl[select] + "%26referer=" + refer
        print url

        xbmc.Player().play(url)

def PLAYSD(name,url,iconimage):
    
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)
        
def PLAYLINK(name,url,iconimage):
	
    dp.create(AddonTitle,"[COLORred]Opening Link...[/COLOR]",'[COLORwhite][/COLOR]','')   
    dp.update(0)
    
    if 'youtube.com/playlist' in url:
        searchterm = url.split('list=')[1]
        ytapi = ytpl + searchterm + ytpl2
        req = urllib2.Request(ytapi)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = link.replace('\r','').replace('\n','').replace('  ','')     
        match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
        try:
            np=re.compile('"nextPageToken": "(.+?)"').findall(link)[0]
            ytapi = ytplpg1 + np + ytplpg2 + searchterm + ytplpg3
            addDir('Next Page >>',ytapi,2,nextpage,fanart)
        except:pass
        for name,ytid in match:
            url = 'https://www.youtube.com/watch?v='+ytid
            iconimage = 'https://i.ytimg.com/vi/'+ytid+'/hqdefault.jpg'
            if not 'Private video' in name:
                if not 'Deleted video' in name:
                    addLink(name,url,2,iconimage,fanart)

    if 'https://www.googleapis.com/youtube/v3' in url:
            searchterm = re.compile('playlistId=(.+?)&maxResults').findall(url)[0]
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            link = link.replace('\r','').replace('\n','').replace('  ','')     
            match=re.compile('"title": "(.+?)".+?"videoId": "(.+?)"',re.DOTALL).findall(link)
            try:
                    np=re.compile('"nextPageToken": "(.+?)"').findall(link)[0]
                    ytapi = ytplpg1 + np + ytplpg2 + searchterm + ytplpg3
                    addDir('Next Page >>',ytapi,2,nextpage,fanart)
            except:pass


   
            for name,ytid in match:
                    url = 'https://www.youtube.com/watch?v='+ytid
                    iconimage = 'https://i.ytimg.com/vi/'+ytid+'/hqdefault.jpg'
                    if not 'Private video' in name:
                            if not 'Deleted video' in name:
                                    addLink(name,url,2,iconimage,fanart)

    
    if resolveurl.HostedMediaFile(url).valid_url(): stream_url = resolveurl.HostedMediaFile(url).resolve()
    elif liveresolver.isValid(url)==True: stream_url=liveresolver.resolve(url)
    else: stream_url=url
    liz = xbmcgui.ListItem(name,iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setPath(stream_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    if 'http' not in url:
        if '.ts'in url:
            url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name='+name+'&amp;url='+url
        elif 'acestream' in url:
            url = "plugin://program.plexus/?url=" + url + "&mode=1&name=acestream+"
            xbmc.Player ().play(url)
        elif resolveurl.HostedMediaFile(url).valid_url():
            url = resolveurl.HostedMediaFile(url).resolve()           
        elif liveresolver.isValid(url)==True:
                url=liveresolver.resolve(url)
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        xbmc.Player ().play(url, liz, False)
        quit()
                            
def PLAYVIDEO(url):

	xbmc.Player().play(url)

def open_url(url):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'klopp')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n','').replace('\r','').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>').replace('<utube>','<link>https://www.youtube.com/watch?v=').replace('</utube>','</link>')#.replace('></','>x</')
        print link
        return link
    except:quit()

def open_url2(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'klopp')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        print link
        return link
 
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


def addLinkMeta(name,url,mode,iconimage,itemcount,isFolder=False):
        splitName=name.partition('(')
	simplename=""
	simpleyear=""
	if len(splitName)>0:
                simplename=splitName[0]
		simpleyear=splitName[2].partition(')')
	if len(simpleyear)>0:
		simpleyear=simpleyear[0]
	mg = metahandlers.MetaData()
	meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
	liz.setInfo( type="Video", infoLabels= meta )
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
	else: liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
	return ok
	
def addDir(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
    liz.setProperty('fanart_image', fanart)
    if 'plugin://' in url:u=url
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name, url, mode, iconimage, fanart, description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setProperty("IsPlayable","true")
    if 'plugin://' in url:u=url
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
    
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)
    
def YOUTUBE_PLAYLIST(url):

    link = open_url(url)
    match = re.compile('yt-lockup-playlist yt-lockup-grid"(.+?)<div class="yt-lockup-meta">').findall(link)
    for links in match:
        url = re.compile ('<a href="(.+?)"').findall(links)[0]
        icon = re.compile ('data-thumb="(.+?)"').findall(links)[0].replace('&amp;', '&')
        title = re.compile ('<div class="yt-lockup-content">.+?title="(.+?)"').findall(links)[0]
        title = CLEANUP(title)
        if not 'http' in url:
            url1 = 'https://www.youtube.com/' + url
            addDir("[COLOR skyblue][B]" + title + "[/B][/COLOR]",url1,43,icon,fanart)
    SET_VIEW()

def YOUTUBE_PLAYLIST_PLAY(url):

    link = open_url(url)
    match = re.compile('<li class="yt-uix-scroller-scroll-unit(.+?)<span class="vertical-align">').findall(link)
    for links in match:
        title = re.compile ('video-title="(.+?)"',re.DOTALL).findall(links)[0]
        title = CLEANUP(title)
        icon = re.compile ('url="(.+?)"',re.DOTALL).findall(links)[0].replace('&amp;', '&')
        fanart = re.compile ('url="(.+?)"',re.DOTALL).findall(links)[0].replace('&amp;', '&')
        url = re.compile ('<a href="(.+?)"').findall(links)[0]
        if not 'http' in url:
            if not 'Deleted video' in title:
                url1 = 'https://www.youtube.com' + url
                addLink("[COLORyellow][B]" + title + "[/B][/COLOR]",url1,2,icon,fanart)
                
# def YOUTUBE_CHANNEL(url):

    # link = open_url(url)
    # match = re.compile ('<div class="yt-lockup-content">(.+?)<div class="yt-lockup-meta">').findall(link)
    # for links in match:
        # title = re.compile ('title="(.+?)"').findall(links)[0]
        # title = CLEANUP(title)
        # title = strip_non_ascii(title)
        # url1 = re.compile ('href="(.+?)"').findall(links)[0]
        # url = 'https://www.youtube.com' + url1
        # icon = 'http://i.imgur.com/P5HLzGl.png'
        # addDir(title,url,72,icon,fanart)
        
# def YOUTUBE_CHANNEL_PART2(url):

    # link = open_url(url)
    # match = re.compile('<tr class="pl-video yt-uix-tile "(.+?)<span class="vertical-align">').findall(link)
    # for links in match:
        # title = re.compile ('title="(.+?)">').findall(links)[0]
        # title = CLEANUP(title)
        # title = strip_non_ascii(title)
        # url1 = re.compile ('<a href="(.+?)"').findall(links)[0]
        # url = 'https://www.youtube.com' + url1
        # icon = re.compile ('data-thumb="(.+?)"').findall(links)[0].replace('&amp;', '&')
        # addLink(title,url,2,icon,fanart)
        
def TEAMNEWS():

    url = 'http://www.worldfootball.net/teams/liverpool-fc/'
    link = open_url(url).replace('\n', '').replace('\r','').replace('\t','')
    match = re.compile('<div class="wfb-news-medium">(.+?)<script type="text/javascript">').findall(link)[0]
    grab = re.compile ('<img src="(.+?)".+?<a href="(.+?)" title="(.+?)"').findall(match)
    for icon,url,title in grab:
        if not 'http' in url:
            url = 'http://www.worldfootball.net' + url
            addLink("[COLORyellow][B]" + title + "[/B][/COLOR]",url,19,icon,fanarts)

def READNEWS(url):

    link = open_url(url)
    match = re.compile('<div class="wfb-news-content">(.+?)</div>').findall(link)[0].replace('<p>', '').replace('</p>', '').replace('"', '')
    heading = AddonTitle
    showText(heading,match)
    
def showText(heading, text):

    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            quit()
            return
        except: pass

def addItem(name,url,mode,iconimage,fanart, description=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def SHOW_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def find_single_match(text,pattern):

    result = ""
    try:    
        single = re.findall(pattern,text, flags=re.DOTALL)
        result = single[0]
    except:
        result = ""

    return result

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass

def view(link):
        try:
                match= re.compile('<layouttype>(.+?)</layouttype>').findall(link)[0]
                if layout=='thumbnail': xbmc.executebuiltin('Container.SetViewMode(500)')              
                else:xbmc.executebuiltin('Container.SetViewMode(50)')  
        except:pass

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
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
if mode==None or url==None or len(url)<1: GetMenu()
elif mode==1:GetContent(name,url,iconimage,fanart)
elif mode==2:PLAYLINK(name,url,iconimage)
elif mode==3:GETMULTI(name,url,iconimage)
elif mode==4:PLAYSD(name,url,iconimage)
elif mode==5:SEARCH()
elif mode==6:YOUTUBE_CHANNEL(url)
elif mode==7:PLAYVIDEO(url)
elif mode==8:GETMULTI_SD(name,url,iconimage)
elif mode==9:SHOW_PICTURE(url)
elif mode==10:NEW()

elif mode==12:GET_REGEX(name,url,iconimage)
elif mode==13:DXTV_CATS(url)
elif mode==15:DXTV_LINKS(name,url)

elif mode==16:resolver_settings()
elif mode==17:CALANDER()
elif mode==42:YOUTUBE_PLAYLIST(url)
elif mode==43:YOUTUBE_PLAYLIST_PLAY(url)
elif mode==71:YOUTUBE_CHANNEL(url)
elif mode==72:YOUTUBE_CHANNEL_PART2(url)
elif mode==317:EVENT_REDDIT()
elif mode==318:REDDIT_PLAYER(name,url,iconimage)
elif mode==319:REDDIT_GET(url)
elif mode==320:REDDIT_MAIN()
elif mode==321:REDDIT_ADD()
elif mode==322:REDDIT_SUGGESTED()
elif mode==323:REDDIT_REMOVE(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
