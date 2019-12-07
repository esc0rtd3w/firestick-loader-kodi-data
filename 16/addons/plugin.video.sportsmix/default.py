import xbmc,xbmcaddon,xbmcgui,xbmcplugin,os,sys,urlparse,re,time,urllib,urllib2,json,random,net,logging
import pyxbmct.addonwindow as pyxbmct

net = net.Net()
addon_id = 'plugin.video.sportsmix'
selfAddon = xbmcaddon.Addon(id=addon_id)
skintheme=selfAddon.getSetting('skin')
artpath='/resources/'+skintheme
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
button_quit= xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'power.png'))
button_quit_focus= xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'power_focus.png'))
button_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'button_focus1.png'))
button_no_focus = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'button_no_focus1.png'))
bg = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + artpath, 'main-bg2.png'))
window  = pyxbmct.AddonDialogWindow('')
window.setGeometry(1240, 650, 100, 50)
background=pyxbmct.Image(bg)
window.placeControl(background, -5, 0, 125, 51)

def START():
        if 'Red' in button_quit:text='0xffffffff'
	elif 'Mono' in button_quit:text='0xffffffff'
	else:text='0xFF000000'
	global List
	global Icon
	#create butttons
	List = pyxbmct.List(buttonFocusTexture=button_focus,buttonTexture=button_no_focus,_space=11,_itemTextYOffset=-7,textColor=text)
	Icon=pyxbmct.Image(icon, aspectRatio=2)
	Icon.setImage(icon)
	Quit = pyxbmct.Button(' ',noFocusTexture=button_quit,focusTexture=button_quit_focus)
	#place buttons
	window.placeControl(List, 10, 1, 110, 30)
	window.placeControl(Icon, 30, 32, 60, 18)
	window.placeControl(Quit, 110, 48, 10, 3)
	#capture mouse moves or up down arrows
	window.connectEventList(
	[pyxbmct.ACTION_MOVE_DOWN,
	pyxbmct.ACTION_MOVE_UP,
		pyxbmct.ACTION_MOUSE_MOVE],
	LIST_UPDATE)
	#navigation
	List.controlRight(Quit)
	#button actions
	window.connect(List, PlayStream)
	window.connect(Quit, window.close)
	GETCHANNELS()

def GETCHANNELS():
	global chname
	global chicon
	global chstream
	global headers
	chname=[]
	chicon=[]
	chstream=[]
        headers={'user-agent':'Mozilla/5.0 (Linux; Android 6.0.1; en-GB; SM-G935F Build/MMB29K.G935FXXU1APGG) MXPlayer/1.8.3',
			 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			 'Accept-Encoding' : 'gzip',
        		 'Connection':'Keep-Alive'}
        api = net.http_GET('http://zona-live-tv.com/zonaapp/api.php?api_key',headers).content
        key = re.compile('"key":"(.+?)",').findall(api)[0].replace('\\','')
        url='http://zona-live-tv.com/zonaapp/api.php?cat_id=14&key='+key
        page = net.http_GET(url,headers).content
        match=re.compile('"channel_title":"(.+?)","channel_url":"(.+?)","channel_thumbnail":"(.+?)"').findall(page)
        match.sort()
        for name,url,thumb in match:
                if not 'u0'in name:
                        if 'zona' in url:
                                                thumb='http://zona-live-tv.com/zonaapp/images/thumbs/'+thumb+'|User-Agent=Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G920F Build/LMY47X)'
                                                chname.append(name)
                                                chicon.append(thumb)
                                                chstream.append(url)
                                                List.addItem(name)
      	window.setFocus(List)


def LIST_UPDATE():
	global playurl
	global iconimage
	global name
	if window.getFocus() == List:
		pos=List.getSelectedPosition()
		iconimage=chicon[pos]
		name=chname[pos]
		Icon.setImage(iconimage)
		playurl=chstream[pos]
#####################################################################################
def PlayStream():
        page = net.http_GET(playurl).content
        page=page+'|user-agent=Mozilla/5.0 (Linux; Android 6.0.1; en-GB; SM-G935F Build/MMB29K.G935FXXU1APGG) MXPlayer/1.8.3'
        window.close()
        liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage)
        xbmc.Player ().play(page, liz, False)
	
def addLink(name,url,mode,iconimage,fanart,description=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		return ok

START()
window.doModal()
del window
xbmcplugin.endOfDirectory(int(sys.argv[1]))
