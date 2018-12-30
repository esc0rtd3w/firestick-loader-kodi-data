import urllib2,re,os,xbmc,xbmcplugin,xbmcaddon,xbmcgui,urlparse,urllib,sys,base64,process

addon_handle = int(sys.argv[1])
Decode = base64.decodestring
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum /')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
CAT = '.php'
Dialog = xbmcgui.Dialog()
BASE = base64.decodestring('aHR0cDovL2JhY2syYmFzaWNzYnVpbGQuY28udWsvdGVzdC8=')


def Kodible_Main_Menu():
    process.Menu('Audio Books','https://www.youtube.com/user/audiobooksfree/playlists',10000,ICON,FANART,'','')
    process.Menu('Kids Audio Books','',606,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


   
def Kids_Menu():
    process.Menu('A-Z','',607,ICON,FANART,'','')
    process.Menu('All','',603,ICON,FANART,'','')
    process.Menu('Search','',614,ICON,FANART,'','')

def Kids_AZ():
    HTML = process.OPEN_URL(Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9tcDNfZG93bmxvYWRzLmh0bQ=='))
    match = re.compile('<td width=".+?" align="center">.+?<a href="(.*?)">.+?<img border="0" src="images/Squeeze%20(.*?).gif" width="74" height=".*?"></a></td>',re.DOTALL).findall(HTML)
    for url,img in match:
        if '-x' in img:
            pass
        else:
            process.Menu(img,(Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay8=')) + (url).replace('colour_it','books_audio/audio_books_a'),608,(Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9pbWFnZXMvU3F1ZWV6ZSUyMA==')) + img + '.gif',FANART,'','')

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	

			
def Kids_AZ_Audio(url):   
    HTML = process.OPEN_URL(url)
    match = re.compile('<td width=".*?" height=".*?"><b>.*?<a href="(.*?)">(.*?)</a></b></td>',re.DOTALL).findall(HTML)
    for url,name in match:
        if '</a>' in name:
            pass
        elif '(' in name:
            process.Menu((name).replace('&nbsp;','').replace('  ','').replace('.mp3','').replace('	','').replace('\n',' '),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9ib29rc19hdWRpby8=') + url,605,ICON,FANART,'','')
        else:
            process.Play((name).replace('&nbsp;','').replace('  ','').replace('.mp3','').replace('	','').replace('\n',' '),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9ib29rc19hdWRpby8=') + url,604,ICON,FANART,'','')

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);		
	
def Search_Kids():
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM) # what you type in
    Search_Title = Search_Name.lower()
    HTML = process.OPEN_URL(Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9jb21wbGV0ZV9saXN0Lmh0bQ=='))
    match = re.compile('<td width=".+?">.*?<b>.+?<a href="(.*?)">(.*?)</a></b></td>',re.DOTALL).findall(HTML)
    for url,name in match:
        if Search_Name in name.lower():			
            if '</a>' in name:
                pass
            elif '(' in name:
                process.Menu((name).replace('&nbsp;','').replace('  ','').replace('+','').replace('.mp3','').replace('\n',' '),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay8=') + url,605,ICON,FANART,'','')
            else:
                process.Play((name).replace('\n',' ').replace('&nbsp;','').replace('  ','').replace('+','').replace('.mp3',''),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay8=') + url,604,ICON,FANART,'','')
	
	
def Kids_Audio():   
    HTML = process.OPEN_URL(Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9jb21wbGV0ZV9saXN0Lmh0bQ=='))
    match = re.compile('<td width=".+?">.*?<b>.+?<a href="(.*?)">(.*?)</a></b></td>',re.DOTALL).findall(HTML)
    for url,name in match:
        if '</a>' in name:
            pass
        elif '(' in name:
            process.Menu((name).replace('&nbsp;','').replace('  ','').replace('+','').replace('.mp3','').replace('	','').replace('\n',' '),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay8=') + url,605,ICON,FANART,'','')
        else:
            process.Play((name).replace('&nbsp;','').replace('  ','').replace('+','').replace('.mp3','').replace('	','').replace('\n',' '),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay8=') + url,604,ICON,FANART,'','')

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
			

def Kids_Play(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<a href="(.+?)">Download</a></b></td>').findall(HTML)
    for url in match:
        url2 = (Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9ib29rc19hdWRpby8=')) + url
        process.Resolve(url2)

def Kids_Play_Multi(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<td width="247">(.*?)</td>.*?<a href="(.+?)">',re.DOTALL).findall(HTML)
    for name,url in match:
        if '<p align' in name:
            pass
        elif '&nbsp;' in name:
            pass
        else:
            process.Play((name).replace('&nbsp;','').replace('	',''),Decode('aHR0cDovL3d3dy5raWRzYXVkaW9ib29rcy5jby51ay9ib29rc19hdWRpby8=') + url,602,ICON,FANART,'','')

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
        
