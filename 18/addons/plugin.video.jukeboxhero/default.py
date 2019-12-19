import os,re,requests,sys,urllib,dandy
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from addon.common.addon import Addon



addon_id='plugin.video.jukeboxhero'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/icons/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
s = requests.session()





def CAT():
	addDir('[B][COLOR white]Popular Vevo Playlists[/COLOR][/B]','https://www.youtube.com/results?q=vevo&sp=EgIQAw%253D%253D',5,art + 'pop_vev.jpg',fanart,'')
	addDir('[B][COLOR white]UK Charts Playlists[/COLOR][/B]','https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=uk+chart',5,art + 'uk_ch.jpg',fanart,'')
	addDir('[B][COLOR white]US Charts Playlists[/COLOR][/B]','https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=us+chart',5,art + 'us_ch.jpg',fanart,'')
	addDir('[B][COLOR white]1000 Most Popular Artists[/COLOR][/B]','https://www.letssingit.com/artists/popular/1',2,art + 'most_pop.jpg',fanart,'')
	addDir('[B][COLOR white]Featured Artists[/COLOR][/B]','https://www.letssingit.com/artists/featured/1',2,art + 'featured.jpg',fanart,'')
	addDir('[B][COLOR white]Billboard Popular Top 100 Artists[/COLOR][/B]','http://www.billboard.com/artists/top-100',3,art + 'bill_pop.jpg',fanart,'')
	addDir('[B][COLOR white]Billboard All time Artists[/COLOR][/B]','http://www.billboard.com/charts/greatest-billboard-200-artists',4,art + 'bill_all.jpg',fanart,'')
	addDir('[B][COLOR white]Greatest All Time Hot 100 Artists[/COLOR][/B]','http://www.billboard.com/charts/greatest-hot-100-artists',4,art + 'great_all.jpg',fanart,'')
	addDir('[B][COLOR white]Compilations[/COLOR][/B]','https://raw.githubusercontent.com/dandy0850/iStream/master/artists.xml',6,art + 'comp.jpg',fanart,'')
	addDir('[B][COLOR white]User Voted Lists[/COLOR][/B]','https://raw.githubusercontent.com/dandy0850/iStream/master/ranker_list.xml',8,art + 'uservoted.jpg',fanart,'')
	addDir('[B][COLOR white]Search for Playlists[/COLOR][/B]','url',100,art + 'search.jpg',fanart,'')

def get_xml(url):
    OPEN = OPEN_URL(url)
    Regex = re.compile('<artist>(.+?)</artist><thumbnail>(.+?)</thumbnail>').findall(OPEN)
    for name,icon in Regex:
        artist = name 
        artist = artist.replace(' ','+')
        url = 'https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=' + artist
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,icon,fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def get_rankers(url):
    OPEN = OPEN_URL(url)
    Regex = re.compile('<list>(.+?)</list><urlpage>(.+?)</urlpage>').findall(OPEN)
    for name,url in Regex:
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,7,art + 'uservoted.jpg',fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def Get_content(url):
    OPEN = OPEN_URL(url)
    Regex = re.compile('="https://i.ytimg.com/(.+?).jpg.+?<span class="formatted-video-count-label"><b>(.+?)</b>.+?data-list-id="(.+?)".+?title=.+?title="(.+?)"',re.DOTALL).findall(OPEN)
    for icon,count,url,name in Regex:
            amount = int(count)
            icon = icon+'.jpg'
            name=name.replace('amp;','').replace('&quot;','').replace('&#39;','\'').title()
            name=name +'  [B][COLOR red]('+count+')'
            if amount <250:
               addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,1,'https://i.ytimg.com/%s'%icon,fanart,'')
    np = re.compile('<a href="(.+?)".+?<span class="yt-uix-button-content">(.+?)</span>',re.DOTALL).findall(OPEN)
    for url,name in np:
            if 'Next' in name:
                url=url.replace('amp;','')
                addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]','https://www.youtube.com%s'%url,5,art + 'nextpage.jpg',fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def billboard(url):
    OPEN = OPEN_URL(url)
    Regex = re.compile('<div class="thumbnail">.+?src="(.+?)" alt="(.+?)"',re.DOTALL).findall(OPEN)
    for icon,name in Regex:
        name=name.replace('amp;','').replace('&quot;','').replace('&#39;','\'').title()
        icon=icon.replace('width_140','promo_310')
        artist = name 
        artist = artist.replace(' ','+')
        url = 'https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=' + artist
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,icon,fanart,'')
    np = re.compile('<li class="pager-current.+?href="(.+?)"',re.DOTALL).findall(OPEN)
    for url in np:
        addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]','http://www.billboard.com/%s'%url,3,art + 'nextpage.jpg',fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
 
def alltime(url):
    OPEN = OPEN_URL(url)
    Regex = re.compile('<div class="chart-row__image".+?http(.+?)".+?data-tracklabel="Artist Name">(.+?)</a>',re.DOTALL).findall(OPEN)
    for icon,name in Regex:
        icon=icon.replace(')','')
        name=name.replace('amp;','').replace('&quot;','').replace('&#039;','\'').lstrip().title()
        artist = name 
        artist = artist.replace(' ','+')
        url = 'https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=' + artist
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,'http%s'%icon,fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def ranker(url):
    headers = {'User-Agent':User_Agent}
    OPEN = requests.get(url,headers=headers,allow_redirects=False).content
    print OPEN
    Regex = re.compile('itemprop="image" data-src="(.+?)".+? alt="(.+?)"',re.DOTALL).findall(OPEN)
    for icon,name in Regex:
        icon=icon.replace('w=87&h=87','').replace('&fit=crop&crop=faces','')
        name=name.split(' is listed')[0]
        artist = name 
        artist = artist.replace(' ','+')
        url = 'https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=' + artist
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,icon,fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def LSI_index(url):
    OPEN = OPEN_URL(url)
    page=url
    Regex = re.compile('<img data-post-load="(.+?)".+?alt="(.+?)">',re.DOTALL).findall(OPEN)
    for icon,name in Regex:
        name =name.replace('amp;','').replace('&quot;','').replace('&#39;','\'').title()
        #icon = 'http:' + icon
        icon = icon.replace('thumb_','')
        artist = name 
        artist = artist.replace(' ','+')
        url = 'https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=' + artist
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,icon,fanart,'')
    curpage=int(page.split('/')[-1])
    nextp=str(curpage+1)
    page=page.replace(str(curpage),nextp)
    addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',page,2,art + 'nextpage.jpg',fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
 

    
def Search():
        keyb = xbmc.Keyboard('', 'Search for Playlists')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = 'https://www.youtube.com/results?sp=EgIQAw%253D%253D&q=' + search
                Get_content(url)

def Resolve(url):
        url = 'plugin://plugin.video.youtube/play/?playlist_id=' + url + '&order=default'
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
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



def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==1:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers, allow_redirects=False).text
	link = link.encode('ascii', 'ignore')
	return link




params=get_params()
url=None
name=None
mode=None
iconimage=None
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
	description=urllib.unquote_plus(params["description"])
except:
	pass




if mode==None or url==None or len(url)<1:
	CAT()

elif mode==1:
	Resolve(url)

elif mode==2:
	LSI_index(url)    

elif mode==3:
	billboard(url)    

elif mode==4:
	alltime(url) 
  
elif mode==6:
	get_xml(url) 
    
elif mode==7:
	ranker(url)

elif mode==8:
	get_rankers(url)
    
elif mode==100:
	Search()

elif mode==5:
	Get_content(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))













