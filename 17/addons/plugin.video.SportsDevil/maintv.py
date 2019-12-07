# -*- coding: UTF-8 -*-
import sys,re,os
from urlparse import parse_qsl
import urlparse
import urllib
import urllib3
import requests
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import threading
import base64
from CommonFunctions import parseDOM
import inputstreamhelper
import resolveurl
import requests
import json

packer = re.compile('(eval\(function\(p,a,c,k,e,(?:r|d).*)')
clappr = re.compile('new\s+Clappr\.Player\(\{\s*?source:\s*?["\'](.+?)["\']')
source = re.compile('sources\s*:\s*\[\s*\{\s*(?:type\s*:\s*[\'\"].+?[\'\"],|)src\s*:\s*[\'\"](.+?)[\'\"]')
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.SportsDevil')
PATH            = addon.getAddonInfo('path')
DATAPATH        = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
RESOURCES       = PATH+'/resources/'
FANART=RESOURCES+'fanart.jpg'
blad=RESOURCES+'sworld.png'
bugats=RESOURCES+'bugatsinho.png'
sys.path.append( os.path.join( RESOURCES, "lib" ) )
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ICON=RESOURCES+'sport365.png'
import jsunpack
import sport365 as sport365
import streamendous as se
args            = urlparse.parse_qs(sys.argv[2][1:])
se.unbkuk = addon.getSetting('unbkuk')
ex_link = params.get('ex_link',[''])
imig= params.get('iconImage',[''])
tit= params.get('foldername',[''])
params2 = args.get('params2', [{}])[0]
BASEURLse='http://www.streamendous.com'
base="http://livetv.sx"

livelooker_url='http://livelooker.com/events.php?lang=pl'
UA='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
UAX='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
UAiphone='Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
s = requests.Session()
def add_item(url, name, image, folder, mode, infoLabels=False,pusto=False,odtworz=True,fanart=FANART):	
	if not image:
		image=RESOURCES+'empty.png'
	if pusto:
		param={}
		param={'mode': mode, 'url': url}
		list_item = xbmcgui.ListItem(label=name)
		if not infoLabels:
			infoLabels={"title": name,'plot':name}
		list_item.setInfo(type="video", infoLabels=infoLabels)			
		list_item.setProperty("IsPlayable", 'false')
		list_item.setArt({'thumb': image, 'fanart': fanart})
		xbmcplugin.addDirectoryItem(
			handle=addon_handle,
			url=build_url(param),
			listitem=list_item,
			isFolder=False
		)	
	else:
		list_item = xbmcgui.ListItem(label=name)
		if folder:
			list_item.setProperty("IsPlayable", 'false')
		else:
			if odtworz:
				list_item.setProperty("IsPlayable", 'true')
			else:
				list_item.setProperty("IsPlayable", 'false')
		if not infoLabels:
			infoLabels={"title": name,'plot':name}
		list_item.setInfo(type="video", infoLabels=infoLabels)	
		list_item.setArt({'thumb': image, 'poster': image, 'banner': image, 'fanart': fanart})		
		xbmcplugin.addDirectoryItem(
			handle=addon_handle,
			url=build_url({'mode': mode, 'url': url,'image':image,'title':name}), 
			listitem=list_item,
			isFolder=folder
		)
	xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")

def addDir(name, ex_link=None, params2=1, mode='folder', iconImage='DefaultFolder.png', infoLabels=None, fanart=FANART, contextmenu=None):
	list_item = xbmcgui.ListItem(label=name)
	folder = False if mode == 'take_stream' else True
	if not infoLabels:
		infoLabels={"title": name,'plot':name}
	list_item.setInfo(type="video", infoLabels=infoLabels)	
	list_item.setArt({'thumb': iconImage, 'poster': iconImage, 'banner': iconImage, 'fanart': fanart})		
	xbmcplugin.addDirectoryItem(
		handle=addon_handle,
		url=build_url({'mode': mode, 'foldername': name, 'ex_link': ex_link, 'params2': params2,'iconImage':iconImage}), 
		listitem=list_item,
		isFolder=folder
	)
	xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")

def addLinkItem(name, url, mode, params2=1, iconimage='DefaultFolder.png', infoLabels=False, IsPlayable=True,
                fanart=FANART, itemcount=1, contextmenu=None):
    u = build_url({'mode': mode, 'foldername': name, 'ex_link': url, 'params2': params2})

    liz = xbmcgui.ListItem(name)

    art_keys = ['thumb', 'poster', 'banner', 'fanart', 'clearart', 'clearlogo', 'landscape', 'icon']
    art = dict(zip(art_keys, [iconimage for x in art_keys]))
    art['landscape'] = fanart if fanart else art['landscape']
    art['fanart'] = fanart if fanart else art['landscape']
    liz.setArt(art)

    if not infoLabels:
        infoLabels = {"title": name}
    liz.setInfo(type="video", infoLabels=infoLabels)
    if IsPlayable:
        liz.setProperty('IsPlayable', 'true')

    if contextmenu:
        contextMenuItems = contextmenu
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)

    ok = xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=liz, isFolder=False, totalItems=itemcount)
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask="%R, %Y, %P")
    return ok
	
	
	
	
	
def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict
    
def build_url(query):
    return base_url + '?' + urllib.urlencode(encoded_dict(query))
	
def home():	
	import rtmpcheck as rtc
	#aa=rtc.get_addon()
	ab=rtc.get_addon('inputstream.adaptive')
	ac=rtc.get_addon('inputstream.rtmp')
	setUnblockKuk()
	addDir('Sport365 LIVE', ex_link='', params2={'_service':'sport365','_act':'ListChannels'}, mode='site2', iconImage=RESOURCES+'sport365.png', fanart=FANART)
	add_item('http://livelooker.com/pl/dzisiaj.html', 'LiveLooker', RESOURCES+'looker.jpg', True, "livelooker", infoLabels=False)
	add_item('http://livetv.sx/enx/allupcoming/', 'LiveTV.sx', RESOURCES+'livetv.png', True, "livetvsx", infoLabels=False)
	add_item('https://sport.tvp.pl/transmisje', 'TVP Sport - Transmisje', RESOURCES+'tvpsport.png', True, "listTVP")	
	add_item('cricfree', 'Crickfree', RESOURCES+'crfree.png', True, 'scheduleCR')	
	add_item('http://strims.world', 'Strims World', RESOURCES+'sworld.png', True, 'scheduleSW')	
	
	add_item('http://strims.world', 'LiveSport.ws', RESOURCES+'logoc.png', True, 'livesportws')	
	
	
	#add_item('http://strims.world', 'Soccer Streams', RESOURCES+'sworld.png', True, 'scheduleSstreams')	
	add_item('', 'Live channels', RESOURCES+'chan2.png', True, "liveChannels")		
	xbmcplugin.endOfDirectory(addon_handle)

def LiveSched():
	add_item('cricfree', 'Crickfree', RESOURCES+'crfree.png', True, 'scheduleCR')	
	add_item('http://strims.world', 'Strims World', RESOURCES+'sworld.png', True, 'scheduleSW')		
	xbmcplugin.endOfDirectory(addon_handle)	
	
def LiveChannels():
	links=[]
	links.append({'href':'http://canalesportivo.xyz/',	'title':'CanaleSportivo',	'img':RESOURCES+'esportivo.png',	'mode':"canalespo"	})
	links.append({'href':'http://canalesportivo.xyz/',	'title':'Super Sportowo',	'img':RESOURCES+'logoss.png',	'mode':"supersport"	})	
	links.append({'href':'cricfree', 					'title':'Crickfree',		'img':RESOURCES+'crfree.png',		'mode':'channelsCR'	})	
	links.append({'href':'http://strims.world',			'title':'Strims World',		'img':RESOURCES+'sworld.png',		'mode':'channelsSW'	})	
	#links.append({'href':'http://strims.world',			'title':'Strims TV',		'img':RESOURCES+'StrimsTV.png',		'mode':'strimstv'	})	
	links.append({'href':'http://unblocked.is/tv',		'title':'Unblocked.is',		'img':RESOURCES+'unbl.png',			'mode':"unblocked"	})	
	for f in links:
		add_item(f.get('href'), f.get('title'), f.get('img'), True, f.get('mode'))	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def ListStrimW():
	add_item('','[COLOR gold]Streams[/COLOR]', RESOURCES+'calendar.png', True, 'scheduleSW')	
	add_item('','[COLOR gold]Channels[/COLOR]', RESOURCES+'chan2.png', True, 'channelsSW')	
	xbmcplugin.endOfDirectory(addon_handle)	

def setUnblockKuk():	
	import uuid
	hash = uuid.uuid4().hex					
	aa='1679497221'
	kuk='__ddgu=%s.%s'%(hash,aa)		
	addon.setSetting('unbkuk',kuk)
	return kuk

def ListUnblocked():
	url = params.get('url', None)
	links = se.ListUnblocked(url)	
	if links:
		for f in links:
			add_item(f.get('href'), f.get('title'), RESOURCES+'unbl.png', True, 'getUnbLinks')	
	xbmcplugin.endOfDirectory(addon_handle)		
	
def getUnbLinks():
	url = params.get('url', None)
	tyt = params.get('title', None)
	add_item(url, '[COLOR lime]► [/COLOR] [B][COLOR gold] Link 1 - %s[/COLOR]'%tyt, RESOURCES+'unbl.png', False, 'linksSW2')
	add_item(url+'?player=1', '[COLOR lime]► [/COLOR] [B][COLOR gold] Link 2 - %s[/COLOR]'%tyt, RESOURCES+'unbl.png',False, 'linksSW2')	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def ListStreamendous():
	url = params.get('url', None)
	mod='CR'
	if 'streamendous' in url:
		mod='SE'
	add_item('','[COLOR gold]Schedule[/COLOR]', RESOURCES+'calendar.png', True, 'schedule%s'%mod)			
	add_item('','[COLOR gold]Channels[/COLOR]', RESOURCES+'chan2.png', True, 'channels%s'%mod)	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def getSuperSport():		
	add_item('https://supersportowo.com/stream1.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Canal+ HD[/COLOR][/B]', "https://i.imgur.com/UUCy060.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream2.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Canal+ Sport HD[/COLOR][/B]', "https://i.imgur.com/mqnZ2Io.png", False, "playsupersportowo")		
	add_item('https://supersportowo.com/stream3.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Canal+ Sport 2 HD[/COLOR][/B]', "https://i.imgur.com/UYxVd2W.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream4.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eurosport HD[/COLOR][/B]', "https://i.imgur.com/yCgj02s.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream5.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eurosport 2 HD[/COLOR][/B]', "https://i.imgur.com/3IA1QAd.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream6.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]nSport+ HD[/COLOR][/B]', "https://i.imgur.com/GDTICof.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream7.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]TVP Sport HD[/COLOR][/B]', "https://i.imgur.com/A34dfve.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream8.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eleven Sports 1 HD[/COLOR][/B]', "https://i.imgur.com/6KvZtpg.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream9.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eleven Sports 2 HD[/COLOR][/B]', "https://i.imgur.com/yt3tfHm.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream10.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eleven Sports 3 HD[/COLOR][/B]', "https://i.imgur.com/FQkKANW.png", False, "playsupersportowo")	
	add_item('https://supersportowo.com/stream11.html', '[COLOR lime]► [/COLOR] [B][COLOR gold]Polsat Sport HD[/COLOR][/B]', "https://i.imgur.com/VkY8zNV.png", False, "playsupersportowo")	

	
	
def getLiveSport():
	links = se.getLiveSport()
	if links:
		for f in links:
			if 'kiedy' in f.get('href'):
				title=(f.get('href')).split('|')[1]
				title='[B][COLOR blue]                        %s[/B][/COLOR]'%title
				add_item('', title, RESOURCES+'calendar.png', True, '', infoLabels=False, pusto=True)
			else:
				ikona=ikony(f.get('image'))
				add_item(f.get('href'), f.get('title'), ikona, False,'getLinksLiveSport', infoLabels={'plot':f.get('title'),'code':f.get('code')},odtworz=False)			

		xbmcplugin.setContent(addon_handle, 'videos')	
		xbmcplugin.endOfDirectory(addon_handle)	
		
def getLinksLiveSport():

	
	url = params.get('url', None)
	tytul = params.get('title', None)
	links = se.getLinksLiveSport(url,tytul)
	
	

    
	items = len(links)
	if links:
		t = [ x.get('title') for x in links]
		u = [ x.get('href') for x in links]
		al = "Links"	
    
		if items>1:	
			select = xbmcgui.Dialog().select(al, t)
			
			if select > -1:
				link = u[select];	
				stream_url = se.getStreamLiveSport(link)	
    
			else:
				quit()
		else:
			link = u[0];
			stream_url = se.getStreamLiveSport(link)	
		if stream_url:
			if 'youtube.com' in stream_url or 'youtu.be' in stream_url:
				stream_url = resolveurl.resolve(stream_url)
			play_item = xbmcgui.ListItem(path=stream_url,label=tytul)
			play_item.setInfo(type="Video", infoLabels={"title": tytul,'plot':tytul})
			play_item.setProperty("IsPlayable", "true")
			play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
			play_item.setMimeType('application/vnd.apple.mpegurl')
			play_item.setContentLookup(False)

			xbmc.Player().play(stream_url,play_item)
		else:
			xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]This video is not available at the moment.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
			return	
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]No links available.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)	
		return	
	return

def PlayLiveSport():
	url = params.get('url', None)
	tytul = params.get('title', None)
	stream_url = se.getStreamLiveSport(url)	

	is_helper = inputstreamhelper.Helper('hls')
	if is_helper.check_inputstream():
		play_item = xbmcgui.ListItem(path=stream_url)
		play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
		play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
		play_item.setMimeType('application/x-mpegurl')
		play_item.setContentLookup(False)
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def getScheduleSW():

	links = se.getScheduleSW()
	#add_item('http://strims.world/KSW50.php', '[B][COLOR gold]KSW[/B][/COLOR]', '', False,'streamsSW', odtworz=False)
	if links:
		for f in links:
			if 'kiedy' in f.get('href'):
				title=(f.get('href')).split('|')[1]
				title='[B][COLOR blue]                        %s[/B][/COLOR]'%title
				add_item('', title, RESOURCES+'calendar.png', True, '', infoLabels=False, pusto=True)
			else:
				ikona=ikony(f.get('image'))
				add_item(f.get('href'), f.get('title'), ikona, False,'streamsSW', odtworz=False)				

		xbmcplugin.setContent(addon_handle, 'videos')	
		xbmcplugin.endOfDirectory(addon_handle)	
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]No schedule links.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)	

def getScheduleSstreams():

	links = se.getScheduleSstreams()
	if links:
		for f in links:
			add_item(f.get('href'), f.get('title'), f.get('image'), False, 'streamsSstreams',infoLabels={'plot':f.get('title'),'code':f.get('code')})				

		xbmcplugin.setContent(addon_handle, 'videos')	
		xbmcplugin.endOfDirectory(addon_handle)	
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]No schedule links.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)	
	
		
		
		
def getScheduleCR():
	links = se.getScheduleCR()
	if links:
		for f in links:
			if 'kiedy' in f.get('href'):
				title=(f.get('href')).split('|')[1]
				title='[B][COLOR blue]                        %s[/B][/COLOR]'%title
				add_item('', title, RESOURCES+'calendar.png', True, '', infoLabels=False, pusto=True)
			else:
				imag=((f.get('code')).lower()).replace('football','soccer').replace('nba','basketball').replace('boxing','fighting').replace('wwe','fighting').replace('ncaa','basketball')
				if 'ufc' in imag:
					imag='fighting'
				if 'motors' in imag:
					imag='f1'
				add_item(f.get('href'), f.get('title'), RESOURCES+'%s.png'%imag, False, 'linksCR',infoLabels={'code':'[COLOR lightgreen][B]'+f.get('code')+'[/B][/COLOR]','plot':f.get('title')})	
		xbmcplugin.setContent(addon_handle, 'videos')	
		xbmcplugin.endOfDirectory(addon_handle)	
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]No schedule links.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)	


def getChannelsSW():
	add_item("http://strims.world/live/realtv.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]Real TV[/COLOR][/B]', "https://i.imgur.com/ofDzqEz.png", False, 'linksSW')	
	add_item("http://strims.world/live/sevillatv.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]Sevilla TV[/COLOR][/B]', "https://i.imgur.com/mggF1cB.png", False, 'linksSW')	
	add_item("http://strims.world/live/lfctv.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]Liverpool TV[/COLOR][/B]', "https://i.imgur.com/3UZFS9c.png", False, 'linksSW')	
	add_item("http://strims.world/live/mutv.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]MUTV[/COLOR][/B]', "https://i.imgur.com/zg16NiQ.png", False, 'linksSW')			
	add_item("http://strims.world/live/chelseatv.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]Chelsea TV[/COLOR][/B]', "https://i.imgur.com/HQFgiYi.png", False, 'linksSW')	
	add_item("http://strims.world/live/nbatv.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]NBA TV[/COLOR][/B]', "https://i.imgur.com/IooE7PF.png", False, 'linksSW')			
	add_item("http://strims.world/live/f1base.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]F1 Base[/COLOR][/B]', "https://i.imgur.com/K5scJB9.png", False, 'streamsSW')		
	add_item("http://strims.world/live/f1base.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]F1 FULL VIDEO REPLAYS [/COLOR][/B]', "https://i.imgur.com/K5scJB9.png", True, 'channF1')		


#F1 FULL VIDEO REPLAYS 
	add_item("http://strims.world/live/tennistv2.php", '[COLOR lime]► [/COLOR] [B][COLOR gold]Tennis TV[/COLOR][/B]', "https://i.imgur.com/JTWxqrd.png", False, 'streamsSW')			
	xbmcplugin.setContent(addon_handle, 'videos')	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def StrimsTv():
	add_item('http://strims.tv/tv5/cs.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Canal+ Sport[/COLOR][/B]', "https://i.imgur.com/mqnZ2Io.png", False, 'playStrimsTv')		
	add_item('http://strims.tv/tv5/cs2.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Canal+ Sport 2[/COLOR][/B]', "https://i.imgur.com/UYxVd2W.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/e1.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eleven Sports 1[/COLOR][/B]', "https://i.imgur.com/6KvZtpg.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/e2.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eleven Sports 2[/COLOR][/B]', "https://i.imgur.com/yt3tfHm.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/e3.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eleven Sports 3[/COLOR][/B]', "https://i.imgur.com/FQkKANW.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/ps.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Polsat Sport[/COLOR][/B]', "https://i.imgur.com/VkY8zNV.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/pse.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Polsat Sport EXTRA[/COLOR][/B]', "https://i.imgur.com/PBOxzIJ.png", False, 'playStrimsTv')	
	
	add_item('http://strims.tv/tv5/psp1.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Polsat Sport Premium 1[/COLOR][/B]', "https://i.imgur.com/mQXMgAD.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/psp2.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Polsat Sport Premium 2[/COLOR][/B]', "https://i.imgur.com/3m0RZFs.png", False, 'playStrimsTv')	
	
	
	add_item('http://strims.tv/tv5/es1.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eurosport[/COLOR][/B]', "https://i.imgur.com/yCgj02s.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/es2.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Eurosport 2[/COLOR][/B]', "https://i.imgur.com/3IA1QAd.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/ns.php  ', '[COLOR lime]► [/COLOR] [B][COLOR gold]nSport+[/COLOR][/B]', "https://i.imgur.com/GDTICof.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/tvps.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]TVP Sport[/COLOR][/B]', "https://i.imgur.com/A34dfve.png", False, 'playStrimsTv')	
	add_item('http://strims.tv/tv5/sp.php', '[COLOR lime]► [/COLOR] [B][COLOR gold]Super Polsat[/COLOR][/B]', "https://i.imgur.com/WMM1NnQ.png", False, 'playStrimsTv')	
	xbmcplugin.setContent(addon_handle, 'videos')	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def PlayStrimsTv():
	url = params.get('url', None)
	#url = params.get('url', None)
	
	#r = requests.get(
	#	url, 
	#	verify=False)	
	data=''
	import mydecode
	stream_url = mydecode._strimstv(url,data,url)
	if stream_url:
		play_item = xbmcgui.ListItem(path=stream_url)
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	
	
	
def getChannelsCR():
	channels = se.getChannelsCR()
	if channels:
		for f in channels:
			add_item(f.get('href'), f.get('title'), RESOURCES+'chan2.png', False, 'linksCR')		
	xbmcplugin.setContent(addon_handle, 'videos')	
	xbmcplugin.endOfDirectory(addon_handle)		

def getLinksCR():
	url = params.get('url', None)
	links=se.getCRlink(url)
	
	items = len(links)
	if links:
		t = [ x.get('title') for x in links]
		u = [ x.get('href') for x in links]
		al = "Links"	
		
		if items>1:	
	
			
			select = xbmcgui.Dialog().select(al, t)
			
			if select > -1:
				link = u[select];	
				stream_url=se.resolvingCR(link,url)
		else:
			link = u[0];
			stream_url=se.resolvingCR(link,url)
		if stream_url:
			play_item = xbmcgui.ListItem(path=stream_url)
			xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		else:
			play_item = xbmcgui.ListItem(path=stream_url)
			xbmcplugin.setResolvedUrl(addon_handle, False, listitem=play_item)
			return
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]This video is not available at the moment.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
		return


def getStreamsSstreams():	
	stream_url=''
	url = params.get('url', None)
	links=se.getSstreamsStreams(url)	
	items = len(links)
	if links:
		t = [ x.get('title') for x in links]
		u = [ x.get('href') for x in links]
		al = "Links"	

		if items>1:	
			select = xbmcgui.Dialog().select(al, t)
			
			if select > -1:
				link = u[select];	

				stream_url=se.resolvingCR(link,url)
				
			else:
				quit()
		else:
			link = u[0];
			stream_url=se.resolvingCR(link,url)
		if stream_url:
			play_item = xbmcgui.ListItem(path=stream_url)
			xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		else:
			xbmcgui.Dialog().notification('[COLOR orangered][B]Error[/B][/COLOR]', '[COLOR orangered][B]This link is NOT working[/B][/COLOR]', blad, 5000)
			play_item = xbmcgui.ListItem(path=stream_url)
			xbmcplugin.setResolvedUrl(addon_handle, False, listitem=play_item)
			return
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]This video is not available at the moment.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
		return	


def getF1channels():
	channels = se.F1channels()
	if channels:
		for f in channels:
			add_item(f.get('href'), f.get('title'), RESOURCES+'chan2.png', False, 'F1stream')		
	xbmcplugin.setContent(addon_handle, 'videos')	
	xbmcplugin.endOfDirectory(addon_handle)	

def getStreamsSW():
	stream_url=''
	url = params.get('url', None)
	tytul = params.get('title', None)
	links=se.getSWstreams(url)	
	items = len(links)
	if links:
		t = [ x.get('title') for x in links]
		u = [ x.get('href') for x in links]
		al = "Links"	

		if items>1:	
			select = xbmcgui.Dialog().select(al, t)
			
			if select > -1:
				link = u[select];	

				stream_url=se.resolvingCR(link,url)
				
			else:
				quit()
		else:
			link = u[0];
			stream_url=se.resolvingCR(link,url)
		if stream_url:
			if 'video.assia' in stream_url: 
				
				is_helper = inputstreamhelper.Helper('hls')
				if is_helper.check_inputstream():
					play_item = xbmcgui.ListItem(path=stream_url,label=tytul)
					play_item.setInfo(type="Video", infoLabels={"title": tytul,'plot':tytul})
					play_item.setProperty("IsPlayable", "true")
					play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
					play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
					
					play_item.setMimeType('application/vnd.apple.mpegurl')
					play_item.setContentLookup(False)
					xbmc.Player().play(stream_url,play_item)
			#elif 'twitch.tv' in stream_url:
			#	web_pdb.set_trace()
			#	stream_url = resolveurl.resolve(stream_url)
			#	play_item = xbmcgui.ListItem(path=stream_url,label=tytul)
			#	play_item.setInfo(type="Video", infoLabels={"title": tytul,'plot':tytul})
			#	play_item.setProperty("IsPlayable", "true")
			#	xbmc.Player().play(stream_url,play_item)
				
			elif 'us/ingest' in stream_url:
				#play_item = xbmcgui.ListItem(path=stream_url,label=tytul)
				#play_item.setInfo(type="Video", infoLabels={"title": tytul,'plot':tytul})
				#play_item.setProperty("IsPlayable", "true")
				#xbmc.Player().play(stream_url,play_item)
				play_item = xbmcgui.ListItem(path=stream_url)
			
				xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		
	
			else:	
				play_item = xbmcgui.ListItem(path=stream_url,label=tytul)
				play_item.setInfo(type="Video", infoLabels={"title": tytul,'plot':tytul})
				play_item.setProperty("IsPlayable", "true")
				xbmc.Player().play(stream_url,play_item)

				
		else:
			xbmcgui.Dialog().notification('[COLOR orangered][B]Error[/B][/COLOR]', '[COLOR orangered][B]This link is NOT working[/B][/COLOR]', blad, 5000)
			play_item = xbmcgui.ListItem(path=stream_url)
			play_item.setProperty("IsPlayable", "false")
			xbmcplugin.setResolvedUrl(addon_handle, False, listitem=play_item)
			return
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]This video is not available at the moment.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
		return			
	return
def getF1stream():
	stream_url=''
	url = params.get('url', None)

	links=se.getF1stream(url)	
	items = len(links)
	if links:
		t = [ x.get('title') for x in links]
		u = [ x.get('href') for x in links]
		al = "Links"	

		if items>1:	
			select = xbmcgui.Dialog().select(al, t)
			
			if select > -1:
				link = u[select];	

				try:
					src = resolveurl.resolve(link)
				except:
					pass
				if src:
					stream_url=src
				else:
					stream_url=link
			else:
				quit()
		else:
			link = u[0];
			try:
				src = resolveurl.resolve(link)
			except:
				pass
			if src:
				stream_url=src
			else:
				stream_url=link
		if stream_url:
			
			play_item = xbmcgui.ListItem(path=stream_url)
			
			xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		else:
			xbmcgui.Dialog().notification('[COLOR orangered][B]Error[/B][/COLOR]', '[COLOR orangered][B]This link is NOT working[/B][/COLOR]', blad, 5000)
			play_item = xbmcgui.ListItem(path=stream_url)
			xbmcplugin.setResolvedUrl(addon_handle, False, listitem=play_item)
			return
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]This video is not available at the moment.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
		return	



	
def getLinksSW():
	url = params.get('url', None)
	link,playt=se.getSWlink(url)
	if link:
		if playt:
			is_helper = inputstreamhelper.Helper('hls')
			if is_helper.check_inputstream():
				play_item = xbmcgui.ListItem(path=link)
				play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
				play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
				play_item.setMimeType('application/x-mpegurl')
				play_item.setContentLookup(False)
		else:
			play_item = xbmcgui.ListItem(path=link)
		
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	else:

		xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem(path=None))#
		return	

def getLinksSW2():
	url = params.get('url', None)
	link,playt=se.getSWlink2(url) 
	if link:
		if playt:
			is_helper = inputstreamhelper.Helper('hls')
			if is_helper.check_inputstream():
				play_item = xbmcgui.ListItem(path=link)
				play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
				play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
				play_item.setMimeType('application/x-mpegurl')
				play_item.setContentLookup(False)
		else:
			play_item = xbmcgui.ListItem(path=link)
		
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	else:

		xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem(path=None))#
		return	
		
def ListTVP():	
	import tvpsport
	url = params.get('url', None)
	links = tvpsport.getChannels(url)
	if links:
		items = len(links)

		for f in links:
			add_item(f.get('href'), f.get('title'), f.get('image'), False, 'playTVP',infoLabels={'code':f.get('code'),'plot':f.get('plot')})	


		xbmcplugin.setContent(addon_handle, 'videos')	
		xbmcplugin.endOfDirectory(addon_handle)	
	else:
		xbmcgui.Dialog().ok('[COLOR red]Problem[/COLOR]','Brak materiałów do wyświetlenia.')	
def PlayTVP():
	import tvpsport
	url = params.get('url', None)
	link,proxy = tvpsport.getChannelVideo(url)
	if link:
		is_helper = inputstreamhelper.Helper('hls')
		if is_helper.check_inputstream():
			play_item = xbmcgui.ListItem(path=link)
			play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
			play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
			play_item.setMimeType('application/x-mpegurl')
			play_item.setContentLookup(False)
		
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	else:

		xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem(path=None))#
	
def PlaySW():
	url = params.get('url', None)
	if link:
		is_helper = inputstreamhelper.Helper('hls')
		if is_helper.check_inputstream():
			play_item = xbmcgui.ListItem(path=link)
			play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
			play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
			play_item.setMimeType('application/x-mpegurl')
			play_item.setContentLookup(False)
		
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	else:

		xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem(path=None))#	
def getDysc(imag):
	if "pilka_nozna.png" in imag: 
		return RESOURCES+'soccer.png', u'Piłka nożna'
	elif "lekkoatletyka.png" in imag: 
		return RESOURCES+'athletics.png', u'Lekkoatletyka'		
	elif "koszykowka.png" in imag: 
		return RESOURCES+'basketball.png', u'Koszykówka'
	elif "siatkowka.png" in imag: 
		return RESOURCES+'volleyball.png', u'Siatkówka'
	elif "specjalne.png" in imag: 
		return RESOURCES+'looker.jpg', u'Specjalne'
	elif "pilka_reczna.png" in imag: 
		return RESOURCES+'handball.png', u'Piłka ręczna'
	elif "baseball.png" in imag: 
		return RESOURCES+'baseball.png', u'Baseball'
	elif "tenis.png" in imag: 
		return RESOURCES+'tennis.png', u'Tenis'
	elif "wyscigi_samochodowe.png" in imag: 
		return RESOURCES+'F1.png', u'Wyścigi samochodowe'
	elif "78.png" in imag: 
		return RESOURCES+'golf.png', u'Golf'
	elif "hokej.png" in imag: 
		return RESOURCES+'hockey.png', u'Hokej na lodzie'
	elif "football_amerykanski.png" in imag: 
		return RESOURCES+'football.png', u'Futbol amerykański'
	elif "zuzel.png" in imag: 
		return RESOURCES+'looker.png', u'Żużel'
	elif "kolarstwo.png" in imag: 
		return RESOURCES+'cycling.png', u'Kolarstwo'
	elif "boks.png" in imag: 
		return RESOURCES+'fighting.png', u'Sporty walki'
	elif "specjalne.png" in imag: 
		return RESOURCES+ 'specjalne.png', u'Specjalne'
	elif "snooker.png" in imag: 
		return RESOURCES+'snooker.png', u'Snooker'
	elif "motorbike.png" in imag: 
		return RESOURCES+'F1.png', u'Motorbikes'
	elif "darts.png" in imag: 
		return RESOURCES+'darts.png', u'Darts'
	elif "23.png" in imag: 
		return RESOURCES+'f1.png', u'Formuła 1'
	elif "badminton.png" in imag: 
		return RESOURCES+'badminton.png', u'Badminton'
	elif "rugby.png" in imag: 
		return RESOURCES+'rugby.png', u'Rugby'
	elif "43.png" in imag: 
		return RESOURCES+'rowing.png', u'Wioślarstwo'
	elif "88.png" in imag: 
		return RESOURCES+'skiing.png', u'Sporty zimowe'		
	elif "skoki_narciarskie.png" in imag: 
		return RESOURCES+'ski_jumping.png', u'Skoki narciarskie'			
	elif "boks.png" in imag: 
		return RESOURCES+'fighting.png', u'Wrestling'
	elif "biathlon.png" in imag: 
		return RESOURCES+'biathlon.png', u'Biathlon'
	elif "currling.png" in imag: 
		return RESOURCES+'curling.png', u'Curling'
	elif "ping_pong.png" in imag:
		return RESOURCES+'table_tennis.png', u'Tenis stołowy'
	else:
		return RESOURCES+'looker.jpg',''

def categories(html):

	cats = re.findall('<tr>\s*<[^<]*<a class="main" href="([^"]*allupcomingsports/(\d+)/)"><img[^>]*src="([^"]+)"></a></td>\s*<td align="left">[^<]*<a[^<]*<b>([^<]*)</b></a>\s*</td>\s*<td width=\d+ align="center">\s*<a [^<]*<b>\+(\d+)</b></a>\s*</td>\s*</tr>', html)
	cats = __prepare_cats(cats)
	return cats

def events(url):

	import requests
	html = requests.get(url).text
	main = parseDOM(html,'table',attrs = {'class':'main'})
	
	events = parseDOM(main,'td',attrs = { 'colspan':'2', 'height':'38'})
	events = __prepare_events(events)
	return events

def links(url,tyt):
	import requests
	html = requests.get(url).text
	links = parseDOM(html, "table", attrs = { "class": "lnktbj" })
	
	links = __prepare_links(links,tyt)
	return links	
	
def __prepare_cats(cats):
	new = []
	for cat in cats:
		url = base + cat[0]
		title = cat[3] + ' (%s)'%cat[4]
		id = get_id(cat[3])
		img = '%s.png'%id
		new.append((url,title,img))

	return new	

def __prepare_links(links,tyt):
	new = []
	for link in links:
		try:
			try:
				bitrate = parseDOM(link, "td", attrs={"class":"bitrate"}) [0]
				bitrate = ' ' + re.sub("<[^>]*>","",bitrate)
			except:
				bitrate = ' '

			try:
				lang = parseDOM(link,"img",ret="title") [0]
				lang = ' ' + re.sub("<[^>]*>","",lang)
			except:
				lang = ' '
			health = re.findall('&nbsp;(\d+)',link)#[0]
			health =health[0] if health else ''

			try:
				streamer_tmp,video,eid,lid,ci,si,jj,url = re.findall('show_webplayer\("(\w+)",\s*"(\w+)",\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*"(\w+)"\).+?href="(.+?)">',link)[0]
				
				streamer_tmp= re.findall('show_webplayer\("(\w+)",',link)[0]
			except:
				url=re.findall('href="([^"]+)"><img OnMouseOver',link,re.DOTALL)#[0]
				streamer_tmp='flash'
				if url:
					url=url[0]
				else:
					url=re.findall('href="([^"]+)">',link,re.DOTALL)[0]
					streamer_tmp='youtube'

			title = "%s (health %s%%) %s %s"%(streamer_tmp,health,lang, bitrate)
			if 'cast3d' not in title and 'acestream' not in title and 'sopcast' not in title:
				new.append((url+'|'+tyt,title.replace('ifr','flash')))
		except:
			pass
	return new
		
def get_id(id):
	id = id.lower().replace(' ','_')
	id = id.replace('ice_hockey','hockey').replace('football','soccer').replace('american_soccer','football').replace('rugby_union','rugby').replace('combat_sport','fighting').replace('rugby_league','rugby').replace('field_hockey','fieldhockey').replace('ncaa','basketball')
	id = id.replace('winter_sport','skiing').replace('water_sports','waterpolo').replace('billiard','snooker').replace('racing','f1').replace('boxing','fighting').replace('water_polo','waterpolo').replace('e-sports','esports')
	return id	

def __prepare_events(events):
	new=[]
	for ev in events:
	
	
	

		url= base+ str(parseDOM(ev, 'a', ret='href')[0])		
		event= str(parseDOM(ev, 'a')[0])		
		info = str(parseDOM(ev, "span", attrs = { "class": "evdesc" }))
		try:
			league = re.findall('\((.+?)\)',info)[0]
		except:
			league = ''

		time = re.findall('(\d+:\d+)',info)[0]
		li = time.split(':')
		hour,minute=li[0],li[1]
		hour=int(li[0])+1
		hour=('{:02}'.format(hour))
		time=hour+':'+minute
		day,month = re.findall('(\d+) (\w+) at',info)[0]
		color = u'[COLOR orangered]■ '
		if 'live.gif' in str(ev):
			color = u'[COLOR lime]► '
		title = PLchar('%s[/COLOR][B][COLOR khaki]%s  : [/COLOR][/B] [B][COLOR gold]%s[/COLOR] [B][COLOR lightgreen]%s[/COLOR][/B]'%(color,time,event,league))        
		new.append((url,title))
        return new
		
def getLivetvsx():
	import requests
	url = params.get('url', None)
	html = requests.get(
		url,
		verify=False).text
	cats=categories(html)
	for cat in cats:
		add_item(cat[0], cat[1], RESOURCES+cat[2], True, 'livetvevents')
	xbmcplugin.endOfDirectory(addon_handle)	

def getLiveEvents():
	url = params.get('url', None)
	img = params.get('image', None)
	event=events(url)
	for even in event:
		add_item(even[0],even[1], img, True, 'livelinks')	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def getLinks():
	url = params.get('url', None)
	tyt = params.get('title', None)
	link=links(url,tyt)
	for new in link:
		add_item('http:'+new[0], new[1], RESOURCES+'play.png', False, 'playlivetvsx')
	xbmcplugin.endOfDirectory(addon_handle)		

	
def getLivelooker():
	url = params.get('url', None)
	r = requests.get(
		url, 
		verify=False)	

	result = parseDOM(r.content, 'div', attrs={'id': "content"})
	links = parseDOM(result,  'div', attrs={'class':'transmisja'})
	if not links:
		r = requests.get(
			"http://livelooker.com/pl/jutro.html", 
			verify=False)	
		result = parseDOM(r.content, 'div', attrs={'id': "content"})
		links = parseDOM(result,  'div', attrs={'class':'transmisja'})		
	for link in links:	
		if 'img_front/live.gif' in link:
			live=u'[COLOR lime]► [/COLOR]'
		else:	
			live=u'[COLOR orangered]■ [/COLOR]'			
		godz=parseDOM(link,  'span', attrs={'style':'font-weight: bold'})[0]
		li = godz.split(':')
		hour,minute=li[0],li[1]
		hour=int(li[0])+1
		hour=('{:02}'.format(hour))
		godz=hour+':'+minute
		title=parseDOM(link, 'b')[0]
		title=title
		imag= parseDOM(link, 'img', ret='src')[0]
		
		if "png" in imag:
			imag,dysc=getDysc(imag)
		else:
			imag= parseDOM(link, 'img', ret='src')[1]
			imag,dysc=getDysc(imag)
		if 'biegi narciarskie' in title.lower():
			imag=RESOURCES+'skiing.png'
			dysc=u'Sporty zimowe'	
		elif u'Łyżwiarstwo szybkie' in title.lower() or 'short track' in title.lower():
			imag=RESOURCES+'speed_skating.png'
			dysc=u'Łyżwiarstwo szybkie'	
		count = 0
		kody='%s (%s)'%(title,dysc)
		linkstrans = parseDOM(link,  'a', ret='href')   
		xx=[]
		out=[]
		for linktransm in linkstrans:
			url=linktransm
			if 'tele-wizja' in url:
				count+=1
				host = urlparse.urlparse(url).netloc
				tytul= '-    Link %s (%s)'%(str(count),host)
				out.append({'title':tytul,'href':url,'mode':'playtvru'})

			elif 'supersportowo' in url:
				count+=1
				host = urlparse.urlparse(url).netloc
				tytul= '-    Link %s (%s)'%(str(count),host)	
				out.append({'title':tytul,'href':url,'mode':'playSupersportowo'})
				
			elif 'zobacz.ws' in url:
				count+=1
				host = urlparse.urlparse(url).netloc
				tytul= '-    Link %s (%s)'%(str(count),host)	
				out.append({'title':tytul,'href':url,'mode':'playZobaczws'})				
			elif 'typertv' in url:
				count+=1
				host = urlparse.urlparse(url).netloc
				tytul= '-    Link %s (%s)'%(str(count),host)
				out.append({'title':tytul,'href':url,'mode':'PlayTyperTV'})				
			elif 'ustreamix' in url:
				count+=1
				host = urlparse.urlparse(url).netloc
				tytul= '-    Link %s (%s)'%(str(count),host) 
				out.append({'title':tytul,'href':url,'mode':'playUstreamix'})	
			#elif 'ustreamyx' in url:
			#	count+=1
			#	host = urlparse.urlparse(url).netloc
			#	tytul= '-    Link %s (%s)'%(str(count),host) 
			#	out.append({'title':tytul,'href':url,'mode':'playUstreamix'})	
           #
			elif 'drhtv.com.pl' in url:
				count+=1
				host = urlparse.urlparse(url).netloc
				tytul= '-    Link %s (%s)'%(str(count),host) 
				out.append({'title':tytul,'href':url,'mode':'playDRhtv'})	

				
		add_item(urllib.quote(str(out)),live+'[B][COLOR khaki]'+godz+'[/COLOR] [/B]''[B][COLOR khaki] : [/COLOR] [/B]'+'[B][COLOR gold]'+title+'[/COLOR] [/B]', imag, False, 'dal2',infoLabels={'code':'[B][COLOR lightgreen]'+dysc+'[/COLOR][/B]','plot':godz+' : '+'[B][COLOR gold]'+title+'[/COLOR] [/B]'}) 

	xbmcplugin.setContent(addon_handle, 'videos')
	xbmcplugin.endOfDirectory(addon_handle)		

def playZobaczws(newurl):
	import cloudflare6
	scraper = cloudflare6.create_scraper()	
	html=scraper.get(url,verify=False).content
	stream=getTelerium(html,newurl)
	if stream:
		play_item = xbmcgui.ListItem(path=stream)
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)	
	else:
		xbmcgui.Dialog().notification('[COLOR orangered][B]Błąd[/B][/COLOR]', '[COLOR orangered][B]Brak działającego streama[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)
		
def ikony(imag):
	if "pi\xc5\x82ka no\xc5\xbcna" in imag.lower() or 'yFgOa2K.png' in imag: 
		return RESOURCES+'soccer.png'
	elif "soccer" in imag.lower() or 'pilkanozna' in imag.lower():
		return RESOURCES+'soccer.png'
	elif "football" in imag.lower():
		return RESOURCES+'soccer.png'
	elif "GPAn874.png" in imag: 
		return RESOURCES+'ski_jumping.png'		
	elif "6zo69E6.png" in imag or 'magazyn' in imag.lower():
		return RESOURCES+'chan2.png'	
	elif "QN5kYMV.png" in imag or 'wyscigi' in imag.lower():
		return RESOURCES+'f1.png'			

	elif "basketball" in imag.lower() or 'koszykowka' in imag.lower():
		return RESOURCES+'basketball.png'	
		
	elif "koszyk\xc3\xb3wka" in imag.lower() or 'Du3nKmW.png' in imag: 
		return RESOURCES+'basketball.png'
	elif "boxing" in imag.lower(): 
		return RESOURCES+'fighting.png'	
	elif "hockey" in imag.lower() or 'Kt3vNRI' in imag or 'hokej' in imag:
		return RESOURCES+'hockey.png'	
	elif "tenis" in imag.lower() or 'GHqJGj4.png' in imag:
		return RESOURCES+'tennis.png'		
	elif "cricket" in imag.lower(): 
		return RESOURCES+'cricket.png'		
	elif "handball" in imag.lower() or 'FUuvZQ9.png' in imag or 'pilkareczna' in imag:
		return RESOURCES+'handball.png'		
	elif "volleyball" in imag.lower() or 'KIZQeih.png' in imag or 'siatkowka' in imag: 
		return RESOURCES+'volleyball.png'		
	elif "rugby" in imag.lower(): 
		return RESOURCES+'rugby.png'		
	elif 'mixed martial' in imag.lower() or '1gUH8gM.png' in imag or 'walki' in imag: 
		return RESOURCES+'fighting.png'		
	elif 'golf' in imag.lower(): 
		return RESOURCES+'golf.png'		
	elif 'darts' in imag.lower(): 
		return RESOURCES+'darts.png'	
	elif 'snooker' in imag.lower(): 
		return RESOURCES+'snooker.png'
	elif 'motorsports' in imag.lower(): 
		return RESOURCES+'f1.png'
	elif 'baseball' in imag.lower(): 
		return RESOURCES+'baseball.png'	
	elif 'afl' in imag.lower(): 
		return RESOURCES+'rugby.png'	
	elif 'cycling' in imag.lower(): 
		return RESOURCES+'cycling.png'
	elif 'tennis' in imag.lower(): 
		return RESOURCES+'tennis.png'
		
	else:
		return RESOURCES+'play.png'

def playDRhtv(newurl):	
	import mydecode
	r = requests.get(newurl,verify=False)
	html=r.content
	src = mydecode.decode(newurl,html)
	if src:
		play_item = xbmcgui.ListItem(path=src)
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

		
def playUstreamix(newurl):
	headers = {
		'Host': 'ssl.ustreamix.com',
		'User-Agent': UA,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': newurl,
		'Upgrade-Insecure-Requests': '1',}	
	r = requests.get(newurl,verify=False)
	content=r.content
	next = re.compile("window.open\('(.*?)'").findall(content)
	nxtu='https://ssl.ustreamix.com%s'%next[0]
	r = requests.get(nxtu,headers=headers,verify=False)	
	content=r.content
	packed = packer.findall(content)[0]
	unpacked = jsunpack.unpack(packed)		
	next2=re.findall('replace\("(.+?)"',unpacked,re.DOTALL)[0]
	headers2 = {
				'User-Agent': UA,
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
				'Referer': nxtu,
				'Connection': 'keep-alive',
				'Upgrade-Insecure-Requests': '1',
				'Cache-Control': 'max-age=0',}
	
	r = requests.get(next2,headers=headers2,verify=False)	
	content=r.content
	unpacked=''
	packeds = packer.findall(content)#[0]
	for packed in packeds:
		unpacked += jsunpack.unpack(packed)
	varhost=re.compile('var host_tmg="(.*?)"').findall(unpacked)
	varfname=re.compile('var file_name="(.*?)"').findall(unpacked)
	varjdtk=re.compile('var jdtk="(.*?)"').findall(unpacked)
	stream_url = 'https://' + varhost[0] + '/' + varfname[0] + '?token=' + varjdtk[0] +'|User-Agent='+urllib.quote(UA)+'&Referer='+next2
	play_item = xbmcgui.ListItem(path=stream_url)
	xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		
def PlayAdaptive(link):	
	is_helper = inputstreamhelper.Helper('hls')
	if is_helper.check_inputstream():
		play_item = xbmcgui.ListItem(path=link)
		play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
		play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
		play_item.setMimeType('application/x-mpegurl')
		play_item.setContentLookup(False)
	
	xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)	

	
def playSupersportowo(newurl=None):
	if not newurl:
	
		newurl = params.get('url', None)
	stream_url=''
	r = requests.get(
		newurl,
		verify=False)
	if 'whostreams' in (r.content).lower():
		stream_url=	getWhostreams(r.content,newurl)
	elif 'nlive.club' in (r.content).lower():
		stream_url=	getNlive(r.content,newurl)
	if stream_url:
		play_item = xbmcgui.ListItem(path=stream_url)
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)	
	else:
		xbmcgui.Dialog().ok('[COLOR red]Problem[/COLOR] ','Brak działającego streama!!!')

def playLivetvsx():
	url = params.get('url', None)
	tyt = url.split('|')[1]
	url =url.split('|')[0]

	r = requests.get(
		url,
		verify=False)
	content=r.content
	
	streamurl=getLivetvsxStream(content,url)
	#
	if streamurl:

		play_item = xbmcgui.ListItem(path=streamurl,label=tyt)

		play_item.setInfo(type="Video", infoLabels={"title": tyt,'plot':tyt})

		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)	

	else:
		xbmcgui.Dialog().notification('[COLOR orangered][B]Error[/B][/COLOR]', '[COLOR orangered][B]This link is NOT working[/B][/COLOR]', blad, 5000)
def getLivetvsxStream(content,url):
	src=''
	
	iframes = parseDOM(content, 'iframe', ret='src')#[0]	
	
	for iframe in iframes:
		
		if'live.php' in iframe:
			iframe=iframe.replace('\r ','')
			nxturl=iframe
			nxturl = 'https:'+nxturl if nxturl.startswith('//') else nxturl		
			headers = {
			'User-Agent': UA,
			'Accept': '*/*',
			'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
			'Referer': url,
			'Connection': 'keep-alive',}			
			result = requests.get(nxturl,headers=headers,verify=False).content
			result=result.replace("\'",'"')

			try:
				src=re.findall("source: '(.+?)'",result,re.DOTALL)[0]	
			except:
				src=re.findall('\.init\("([^"]+)"',result,re.DOTALL)[0]	
			#
			src=src+'|User-Agent='+urllib.quote(UA)+'&Referer='+nxturl			
			break
		elif 'youtube.com' in iframe:
			src = resolveurl.resolve(iframe)
			break
		elif 'livestream.com/accounts' in iframe:
			headers = {
			'User-Agent': UA,
			'Accept': '*/*',
			'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
			'Referer': url,
			'Connection': 'keep-alive',}	
			nxturl=iframe
			nxturl = 'https:'+nxturl if nxturl.startswith('//') else nxturl	
			result = requests.get(nxturl,headers=headers,verify=False).content
			result=result.replace("\'",'"')
			src = re.findall('m3u8_url":"([^"]+)"',result,re.DOTALL)[0]
			src=src+'|User-Agent='+urllib.quote(UA)+'&Referer='+nxturl	
			break
		elif 'streameast.live' in iframe:
			headers = {
			'User-Agent': UA,
			'Accept': '*/*',
			'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
			'Referer': url,
			'Connection': 'keep-alive',}	
			nxturl=iframe
			nxturl = 'https:'+nxturl if nxturl.startswith('//') else nxturl	
			result = requests.get(nxturl,headers=headers,verify=False).content
			result=result.replace("\'",'"')
			try:
				src=re.findall("""source:\s*['"](.+?)['"]""",result,re.DOTALL)[0]	
			except:
				src=re.findall('\.init\("([^"]+)"',result,re.DOTALL)[0]	
			#
			src=src+'|User-Agent='+urllib.quote(UA)+'&Referer='+nxturl			
			break
		else:

			import mydecode
			src = mydecode.decode(url,content)
			break


	return src

def decode(content2,strona):
	if 'telerium' in content2:
		stream_url=getTelerium(content2,strona[0])
		return stream_url
	elif 'wiz1.net' in content2:
		stream_url=getWiz1net(content2,strona)
		return stream_url		
	return None

def getTelerium(content2,strona):
	try:
		id=re.compile("""'>id=\'(.*?)'; width=""").findall(content2)
		embedd= "http://telerium.tv/embed/" + id[0] + ".html"
	except:		
		url = parseDOM(content2, 'iframe', ret='src')
		embedd=url[0]
	#str = _telerium(query,data,url)
	import mydecode
	str=mydecode._telerium(embedd,data,strona)
	return str
def rev(a_string):
    return a_string[::-1]	

	
def resolve(embedd,stronka):
	resp = s.get(embedd, headers={'User-Agent':UA, 'Referer':stronka},verify=False,allow_redirects=False)#.content
	data=resp.content
	try:
		packed = packer.findall(data)[0]
	except:
		return ''
	unpacked = jsunpack.unpack(packed)	
	src = re.compile('source:([^,]*)').findall(unpacked)	
	patern3	='var '+src[0]+'=atob\((.+?)\)'
	
	src6=re.compile(patern3).findall(unpacked)	
	patern6=src6[0]+'="(.*?)"'		
	src7=re.compile(patern6).findall(unpacked)	 #poprawny poczatek adresu
	d=src7[0]
	d1=base64.b64decode(d)	
	#varNames = re.compile('ajax\(\{url:atob\((.+?)\)\+atob\((.+?)\),dataType\:')#\$\.ajax\(\s*\{\s*url\s*:\s*atob\(\w+\((.+?)\)\)\s*\+\s*atob\(\w+\((.+?)\)\)\s*,dataType\s*:\s*[\'\"]json[\'\"]')
	varNames = re.compile('url:\s*atob\((.+?)\)\s*\+\s*atob\((.+?)\).\s*dataType')#\$\.ajax\(\s*\{\s*url\s*:\s*atob\(\w+\((.+?)\)\)\s*\+\s*atob\(\w+\((.+?)\)\)\s*,dataType\s*:\s*[\'\"]json[\'\"]')
	vars = varNames.findall(unpacked)[0]
	part1Reversed = re.compile('{0}\s*=\s*[\'\"](.+?)[\'\"];'.format(vars[0])).findall(unpacked)[0]
	part2Reversed = re.compile('{0}\s*=\s*[\'\"](.+?)[\'\"];'.format(vars[1])).findall(unpacked)[0]	
	part1 = base64.b64decode(part1Reversed)
	part2 = base64.b64decode(part2Reversed) 	
	realtoken = getRealToken('https://telerium.tv'+part1+part2, embedd)
	stream = 'https:{0}{1}|Referer={2}&User-Agent={3}&Origin=https://telerium.tv&Connection=keep-alive&Accept=*/*'
	stream = stream.format(d1, realtoken, urllib.quote(embedd, safe=''), UA) 
	return stream	

    
def getRealToken(link, referer):

	h = {
		'User-Agent': UA,
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': referer,
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',}	

	realResp = s.get(link, headers=h,verify=False).content#[1:-1]
	realResp=re.findall('"(.+?)"',realResp)[0]	
	return realResp[::-1]	
		
def getm3u8(content2,strona):
	m3u8playlist = re.compile('["\'](http.*?\\.m3u[8])["\']').findall(content2)
	if m3u8playlist:
		str = m3u8playlist[0]+'|User-Agent='+UA+'&Referer='+strona
	return str
	
def getDecodeSaw(content):
	mainsaw='http://www.sawlive.tv/embed/stream/'

	var = re.compile("""var\s+\w+\s+=\s*['"](.*?)['"]""").findall(content) #[0][1]
	#print var

	vars=var[0].split(';')
	var1=vars[0]
	var2=vars[1]
	dec= mainsaw+var2+'/'+var1
	return dec
	
def getWiz1net(content2,strona):

	nexturls = parseDOM(content2, 'iframe',ret='src')
	for nexturl in nexturls:
		if 'wiz1.net' in nexturl:
			break
		else:
			continue
	headers = {
    'User-Agent': UAX,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Referer': strona,
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

	content = requests.get(nexturl,headers=headers,verify=False).content	
	
	nexturl2 = re.compile('"text/javascript"\s+src="(.*?)"').findall(content)[0]
	headers = {
    'User-Agent': UAX,
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Referer': nexturl,
    'Connection': 'keep-alive',}
	
	content = requests.get(nexturl2,headers=headers,verify=False).content
	decSawUrl=getDecodeSaw(content)
	str=	_sawlivetv2(decSawUrl,nexturl)
	return str
	
def _sawlivetv2(url,ref):

	video_url=''
	headers = {
	'User-Agent': UAX,
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
	'Referer': ref,
	'Connection': 'keep-alive',}
	try:
		result = requests.get(url,headers=headers,verify=False).text
		replac = requests.get('http://sawlive.tv/ey.js',headers=headers,verify=False).text
		replac=re.findall('"(.+?)";',replac)
		if replac:
			zmiana=replac[0]
		else:
			zmiana='v6uevdvd'
	except:
		zmiana='v6uevdvd'
	packer = re.compile('(eval\(function\(p,a,c,k,e,(?:r|d).*)')
	unpacked = ''
	packed= packer.findall(result)
	
	for i in packed: 
		print i
		try: unpacked += jsunpack.unpack(i)
		except: pass
	result += unpacked
	
	result = urllib.unquote_plus(result).decode('string_escape')#.replace("\'",'"')
	gribs=re.findall('gribs="(.+?)"',result)#[-1]
	if not gribs:
		xbmcgui.Dialog().ok('[COLOR red]Problem[/COLOR]','Stream offline')	
		return
	else:
		gribs=gribs[-1]
	
	liczby=re.findall('=([^=]+)\sunescape\(qaz\)',result)[0]
	li=re.findall('var '+liczby+'\= (.+?)\s+(.+?)\s+(.+?);',result)[0]
	kod=0
	for lk in li:
		try:
			sut=re.findall('var '+lk+'\=(\d+);',result)[0]
			kod+=int(sut)
		except:
			continue

	has=re.findall("\(qaz\)\s+'(.+?)';",result)[-1].replace(zmiana,'M')
	rss=re.findall('rsss\s+=\s+"(.+?)"',result,re.DOTALL)[-1]
	usa=urllib.quote(UAX)
	dal=str(kod)+'?'+has+rss 
	swfUrl='http://static3.sawlive.tv/player.swf'
	url2='%s playpath=%s swfUrl=%s pageUrl=%s live=1 swfVfy=1'%(gribs,dal,swfUrl,url)
	return url2	

def getAliezme(content2,strona):
	next_url = re.compile('src="(http://emb.aliez.me.*?)"').findall(content2)
	headers = {

		'User-Agent': UA,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		}
	r = requests.get(
		next_url[0],
		headers=headers,
		verify=False)

	cur=r.content
	str   = re.compile("""['"]*(http[^'^"]+?\.m3u8[^'^"]*?)['"]""").findall(r.content)
	str=str[0] +'|User-Agent='+UA+'&Referer='+next_url[0]  # '|User-Agent='+UA+'&Referer='+next_url[0] #' live=true swfVfy=1 swfUrl=http://i.aliez.me/swf/playernew.swf flashver=WIN\2024,0,0,221 pageUrl=' +next_url[0]
	if str:
		return str		
	else: return None
	
def getPxstream(content2,strona):	
	next_url = re.compile('src="(.*?)"').findall(content2)
	for url in next_url:
		if 'pxstream.tv' in url:
			pxurl=url
		else:
			continue
	header = {'User-Agent':UA,
		'Referer': strona,
		'Host':'pxstream.tv'}		
	r = requests.get(
		pxurl,
		headers=header,
		verify=False)
	a=r.content
	m3u8playlist = re.compile("""file:.['"](.*?)['"]""").findall(r.content)	
	if m3u8playlist:
		str = m3u8playlist[0]+'|User-Agent='+UA+'&Referer='+pxurl+'&X-Requested-With=ShockwaveFlash/24.0.0.186'	
		return str	
	else: return None



def NLheaders(ref):
	hea = {
		'Host': 'edge.nlive.club',
		'User-Agent': UAX,
		'Accept': '*/*',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': ref,
		'Origin': 'https://nlive.club',
	}
	
	hed = ['%s=%s' % (name, value) for (name, value) in hea.items()]
	return '&'.join(hed)	
def getNlive(html, ref):
	embedd= parseDOM(html, 'iframe', ret='src')[0]
	header = {'User-Agent':UAX,'Referer': ref, }	
	r = requests.get(embedd, headers=header,	verify=False)#.text
	header2 = {
		'User-Agent': UAX,
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': embedd,
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',}	
	str=re.findall('curl = "(.+?)"',r.text,re.DOTALL)
	if str:
		token= requests.get('https://nlive.club/getToken.php', headers=header2,	cookies=r.cookies,verify=False).text
		token=re.findall('"token":"(.+?)"',token)#[0]	
	stream_url=''
	if token and str:
		hea=NLheaders(embedd)
		stream_url='%s%s|%s'%(str[0],token[0],hea)
	return stream_url
	
def getWhostreams(content2,strona):
	embedd= parseDOM(content2, 'iframe', ret='src')[0]
	header = {'User-Agent':UAiphone,'Referer': strona, }		
	page = requests.get(embedd, headers=header,	verify=False).text
	packed = packer.findall(page)[0]
	unpacked = jsunpack.unpack(packed)
	try:
		str = clappr.findall(unpacked)[0]
	except:
		str = source.findall(unpacked)[0]
	str += '|User-Agent={ua}&Referer={ref}'.format(ua=UAiphone, ref=embedd)
	return str

	
def getChanx():	
	getSuperSport()
	xbmcplugin.setContent(addon_handle, 'videos')		
	xbmcplugin.endOfDirectory(addon_handle)	
	
	
def getChan():	
	try:
			
		url = params.get('url', None)
		headersok = {
		'User-Agent': UA,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'TE': 'Trailers',}	
		html=requests.get(url,headers=headersok,verify=False,timeout=10).text
		html=html.replace("\'",'"')	
		links=parseDOM(html,'div', attrs={'class': "channelContainer"})
		
		for link in links:
			title = parseDOM(link, 'h4')[0].strip()
			href = parseDOM(link, 'iframe', ret='src')[0]	
			href  = href .replace('beisport3.php','beinsport3.php')
			html= requests.get(href,headers=headersok,verify=False).text
			try:
				href = parseDOM(html, 'iframe', ret='src')[0]	
			except:
				pass
			imag = parseDOM(link, 'img', ret='src')[0]	
			add_item(href, u'[COLOR lime]► [/COLOR][B][COLOR gold]'+title+'[/B][/COLOR]', imag, False, 'playchan')
		xbmcplugin.setContent(addon_handle, 'videos')		
		xbmcplugin.endOfDirectory(addon_handle)		
	except:
		pass

	
def PlayChan():
	url = params.get('url', None)
	url = url.replace('beisport3.php','beinsport3.php')
	headersok = {
	'User-Agent': UA,
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
	'Connection': 'keep-alive',
	'Upgrade-Insecure-Requests': '1',
	'TE': 'Trailers',}	
	html=requests.get(url,headers=headersok,verify=False).text
	html=html.replace("\'",'"')	
	src=re.findall('source:*"(.+?)"',html,re.DOTALL)#[0]
	src2=re.findall('<source(.+?)</video>',html,re.DOTALL)#[0]
	src3 = re.findall('(path to the HLS m3u8)',html,re.DOTALL)#[0]
	src4 = re.findall("""window.atob\(['"]([^"]+)['"]""",html,re.DOTALL)
	if src:
		stream=src[0]+'|User-Agent='+UA+'&Referer='+url	
		xbmcplugin.setResolvedUrl(addon_handle, True, xbmcgui.ListItem(path=stream))	
	elif src2:
		src = re.findall("""src=['"](.+?)['"]""",src2[0])
		if src:
			stream=src[0]+'|User-Agent='+UA+'&Referer='+url	
			if stream.startswith("/live/"):
				stream = 'https://www.vipsportslive.eu'+stream
			xbmcplugin.setResolvedUrl(addon_handle, True, xbmcgui.ListItem(path=stream))
	elif src3:
		dan = re.findall("sources: (\[.+?\])",html,re.DOTALL)[0]
		src = re.findall("""src:\s*['"]([^'"]+)['"]""",dan)
		if src:
			stream=src[0]+'|User-Agent='+UA+'&Referer='+url	
			xbmcplugin.setResolvedUrl(addon_handle, True, xbmcgui.ListItem(path=stream))
	elif src4:
		src = base64.b64decode(src4[0])#
		if 'manifest.mpd' in src:
			play_item = xbmcgui.ListItem(path=src)
			play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
			play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
			play_item.setMimeType('video/mp4')
			play_item.setContentLookup(False)
			xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		else:
			stream=src+'|User-Agent='+UA+'&Referer='+url
			xbmcplugin.setResolvedUrl(addon_handle, True, xbmcgui.ListItem(path=stream))
	else:
		xbmcplugin.setResolvedUrl(addon_handle, False,  xbmcgui.ListItem(path=''))		
def PlayTyperTV(url):
	headers = {'User-Agent': UA,}	
	html = requests.get(url,headers=headers,verify=False).content
	iframe = parseDOM(html, 'iframe', ret='src')[0]
	headers = {
    'User-Agent': UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Referer': url,
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',}
	html = requests.get(iframe,headers=headers,verify=False).content
	src=decode(html,iframe)
	if not src:
		import mydecode
		src = mydecode.decode(url,html)
	if src:
		play_item = xbmcgui.ListItem(path=src)
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def PLchar(char):
    if type(char) is not str:
        char=char.encode('utf-8')
    char = char.replace('\xc4\x85','ą').replace('\xc4\x84','Ą')
    char = char.replace('\xc4\x87','ć').replace('\xc4\x86','Ć')
    char = char.replace('\xc4\x99','ę').replace('\xc4\x98','Ę')
    char = char.replace('\xc5\x82','ł').replace('\xc5\x81','Ł')
    char = char.replace('\xc5\x84','ń').replace('\xc5\x83','Ń')
    char = char.replace('\xc3\xb3','ó').replace('\xc3\x93','Ó')
    char = char.replace('\xc5\x9b','ś').replace('\xc5\x9a','Ś')
    char = char.replace('\xc5\xba','ź').replace('\xc5\xb9','Ź')
    char = char.replace('\xc5\xbc','ż').replace('\xc5\xbb','Ż')
    char = char.replace('&ndash;','-') #.replace('\xc4\x84','Ą')	
    return char	
	


def play_stream(params2):
	import rtmpcheck as rtc
	aa=rtc.disable_addon()
	params2 = eval(params2)
	service = params2.get('_service')
	act = params2.get('_act')
	mod = __import__(service)
	if act == 'ListChannels':
		items = mod.getChannels(ex_link)
		img_service = '%s.png' % (RESOURCES + service)
		for one in items:
			ikona=ikony(one.get('image'))
			params2.update({'title': one.get('title', '')})
			addDir(one.get('title', ''), one['url'], params2=params2, mode='get_streams_play', infoLabels=one,iconImage=ikona, fanart=FANART)

def get_streams_play(params2,img,tit):
	params2 = eval(params2)
	orig_title = params2.get('title')
	import sport365 as mod
	frames = mod.getStreams(ex_link)
	if frames:
		for frame in frames:
			params2.update({"title": orig_title})
			#addLinkItem(frame.get('title', ''), json.dumps(frame), mode='take_stream',
			#			params2=params2, iconimage=img, fanart=FANART, infoLabels={'plot':tit},IsPlayable=True)
	
			addDir(frame.get('title', ''), json.dumps(frame), params2=params2,mode='take_stream', iconImage=img, fanart=FANART, infoLabels={'plot':tit})
		xbmcplugin.endOfDirectory(addon_handle)	
	else:
		xbmcgui.Dialog().notification('[COLOR red][B]Error[/B][/COLOR]', '[COLOR red][B]This video is not available at the moment.[/B][/COLOR]', xbmcgui.NOTIFICATION_INFO, 5000)


def take_stream(params2):
	params2 = eval(params2)
	orig_title = params2.get('title')
	import sport365 as mod
	busy()
	stream_url, url, header, title = mod.getChannelVideo(json.loads(ex_link))
	if stream_url:
		
		liz = xbmcgui.ListItem(label=orig_title)
		iconimage = xbmc.getInfoImage("ListItem.Thumb")
		liz.setArt({"fanart": FANART, "icon": iconimage})
		liz.setInfo(type="Video", infoLabels={"title": orig_title})
		liz.setProperty("IsPlayable", "true")
		if addon.getSetting('sport365') == 'Inputstream':
			stream_url, hdrs = stream_url.split('|')
			stream_url = stream_url.replace('/i', '/index.m3u8')
			liz.setPath(stream_url)
			if float(xbmc.getInfoLabel('System.BuildVersion')[0:4]) >= 17.5:
				liz.setMimeType('application/vnd.apple.mpegurl')
				liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
				liz.setProperty('inputstream.adaptive.stream_headers', str(header))
			else:
				liz.setProperty('inputstreamaddon', None)
				liz.setContentLookup(True)
	
			idle()

			try:
				import threading
				thread = threading.Thread(name='sport356Thread', target=sport356Thread2, args=[url, header])
				thread.start()
				xbmc.Player().play(stream_url, liz)
			except BaseException:

				pass
				
				
		elif addon.getSetting('sport365') == 'Streamlink':
		#else:
			stream_url, hdrs = stream_url.split('|')
			import streamlink.session
			session = streamlink.session.Streamlink()
			session.set_option('hls-live-edge', 15) 
			#session.set_option('hls-playlist-reload-attempts',15)
			#session.set_option('hls-live-restart',1)
			#stream_url, hdrs = stream_url.split('|')
			#stream_url = 'hls://' + stream_url
			stream_url = 'hls://' + stream_url.replace('/i', '/index.m3u8')
			
			hdrs += '&Origin=http://h5.adshell.net'
			session.set_option("http-headers", hdrs)
	
			streams = session.streams(stream_url)
			stream_url = streams['best'].to_url() + '|' + hdrs
	
			liz.setPath(stream_url)
			idle()
			import threading
			thread = threading.Thread(name='sport356Thread', target=sport356Thread2, args=[url, header])
			thread.start()
			xbmc.Player().play(stream_url, liz)
	
		else:
	    
			stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HLSRETRY&url={0}&name={1}'.format(
				urllib.quote_plus(stream_url), urllib.quote_plus(orig_title))
			liz.setPath(stream_url)
			idle()
			try:
				xbmc.executebuiltin('RunPlugin(' + stream_url + ')')
			except BaseException:
				pass
	
	else:
		xbmcgui.Dialog().ok("Sorry for that", 'plz contact Dev')

def sport356Thread2(url, header):
    import re, sport365 as s

    player = xbmc.Player()
    xbmc.sleep(2000) #3minutes
    player.pause()

    while player.isPlaying():
        ##########################
       #print 'sport356Thread: KODI IS PLAYING, sleeping 4s'
        a, c = s.getUrlc(url, header=header, usecookies=True)
        banner = re.compile('url:["\'](.*?)[\'"]').findall(a)[0]
        xbmc.log(banner)
        xbmc.sleep(2000)
        s.getUrlc(banner)
        xbmc.sleep(2000)
   # print 'sport356Thread: KODI STOPED, OUTSIDE WHILE LOOP ... EXITING'


		
def idle():

    if float(xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')[:4]) > 17.6:
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    else:
        xbmc.executebuiltin('Dialog.Close(busydialog)')


def busy():

    if float(xbmcaddon.Addon('xbmc.addon').getAddonInfo('version')[:4]) > 17.6:
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    else:
        xbmc.executebuiltin('ActivateWindow(busydialog)')



	

def Dalej2()	:
	url = params.get('url', None)
	
	streams = eval(urllib.unquote(url))
	t = [ x.get('title') for x in streams]
	u = [ x.get('href') for x in streams]
	m = [ x.get('mode') for x in streams]
	al = "Źródła"
	
	select = xbmcgui.Dialog().select(al, t)
	
	if select > -1:
		link = u[select];
		mod = m[select];
		graj='%s("%s")'%(mod,link)
		eval(graj)

		
		

if __name__ == '__main__':
	mode = params.get('mode', None)
	if not mode:
		home()
	elif mode == 'canalespo':
		getChan()	
	elif mode == 'supersport':
		getChanx()	
		
	elif mode == 'strimstv':
		StrimsTv()	
		
	elif mode == 'listTVP':
		ListTVP()
		
	elif mode == 'sport365':
		getSport365()	
	elif mode == 'playchan':
		PlayChan()		   
	elif mode == 'playtyper' :
		PlayTyperTV()	   
	elif mode == 'livelooker':
		getLivelooker()		
	elif mode == 'playlivetvsx':
		playLivetvsx()		
	elif mode == 'livetvsx':
		getLivetvsx()
	elif mode == 'livelinks':
		getLinks()
	elif mode == 'livetvevents':
		getLiveEvents()		
	elif mode == 'playsupersportowo':
		playSupersportowo()
	elif mode == 'playsport':
		playSport()	
	elif mode == 'playsport2':
		playSport2()			
	elif mode == 'playustreamix':
		playUstreamix()	
	elif mode == 'playTVP':
		PlayTVP	()		
	
	
	elif mode == 'streamendous':
		ListStreamendous()
	elif mode == 'unblocked':
		ListUnblocked()
	elif mode == 'getUnbLinks':
		getUnbLinks	()		
	
		
		
	elif mode == 'strimw':
		ListStrimW()		
	elif mode == 'dal2':
		Dalej2()	
		
	elif mode == 'channelsSW':
		getChannelsSW()			
	elif mode == 'channelsSE':
		getChannelsSE()	
	elif mode == 'scheduleSE':
		getScheduleSE()		
	elif mode == 'linksSE':
		getLinksSE()			
	elif mode == 'playSE':
		PlaySE()			
	elif mode == 'channelsCR':
		getChannelsCR()	
	elif mode == 'scheduleCR':
		getScheduleCR()		
	elif mode == 'linksCR':
		getLinksCR()	

		

		
	elif mode == 'scheduleSW':
		getScheduleSW()	
	elif mode == 'scheduleSstreams':
		getScheduleSstreams()	
	
	
	elif mode=='livesportws':
		getLiveSport()


		
	elif mode == 'linksSW':
		getLinksSW()
	elif mode == 'linksSW2':
		getLinksSW2()		
		
	elif mode == 'liveChannels':
		LiveChannels()	
	elif mode == 'liveSched':
		LiveSched()	

	elif mode == 'playStrimsTv'	:
		PlayStrimsTv()
#getF1channels	
	elif mode == 'channF1':
		getF1channels	()		
		
	elif mode == 'streamsSW':
		getStreamsSW()	
	
	elif mode == 'F1stream':
		getF1stream()	
	
	
	
	elif mode == 'streamsSstreams':
		getStreamsSstreams()	
	
	
	elif mode == 'playCR':
		PlayCR()

	elif mode == 'site2':
		xbmcgui.Dialog().notification('[COLOR red][B]Sports365[/B][/COLOR]', '[COLOR red][B] by BUGATSINHO[/B][/COLOR]', bugats, 7000)
		play_stream(params2)
		xbmcplugin.endOfDirectory(addon_handle)
	elif mode == 'folder':
		pass
	
	elif mode == 'take_stream':
		take_stream(params2)
		#xbmcplugin.endOfDirectory(addon_handle)
		#xbmcplugin.endOfDirectory(addon_handle)
	elif mode == 'get_streams_play':
		get_streams_play(params2,imig,tit)
	elif mode == 'getLinksLiveSport':
		getLinksLiveSport()
	elif mode == 'playLiveSport':
		PlayLiveSport()

	
	
else:
	pass
