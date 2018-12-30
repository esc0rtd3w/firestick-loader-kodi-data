import xbmc,os,re,base64,requests,urllib,json

addon_id   = 'script.cypherstream'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

def cat():
	#addDir('[COLOR white][B]Dhamka TV[/COLOR][/B]','dhamkatv',4,'https://lh3.googleusercontent.com/j-IM8JRk5bLHIA8h9F5QITT0aIetO6C-mgzCwt-gtzIjHRrHZ6-MnFb-Y4ckoieR=h900',fanart,'')
	#addDir('[COLOR white][B]eDoctor IPTV[/COLOR][/B]','edoctor',4,'https://lh3.googleusercontent.com/qydRpyUiySg1MuswXdbQE88PBfyPH8uJYhONBL3UO1Ij4yEHtftHFK3pKXHXppFUCmk=w300',fanart,'')
	#addDir('[COLOR white][B]Geo Streamz[/COLOR][/B]','geotv',4,'https://image.winudf.com/v2/image/Y29tLnNuci5lbnRfaWNvbl8wX2I0N2VlYjZi/icon.png?w=170&fakeurl=1&type=.png',fanart,'')
	#addDir('[COLOR white][B]IPTV Restream[/COLOR][/B]','iptvrestream',4,'https://1.bp.blogspot.com/-SnEmyxvBHxA/WDW4v6asHAI/AAAAAAAAUac/QBXOMnYAH2Y8MNS1qDbJxgswJpnBfcgAACLcB/s1600/14494667_992633267526877_2246028541223869412_n.jpg',fanart,'')
	#addDir('[COLOR white][B]Mega IPTV[/COLOR][/B]','megaiptv',4,'https://i.ytimg.com/vi/xiMZ231EBus/hqdefault.jpg',fanart,'')
	#addDir('[COLOR white][B]Mobdro[/COLOR][/B]','mobdro',4,'http://apk.co/images/mobdro-2014-freemium.png',fanart,'')
	addDir('[COLOR white][B]Pak India Sports[/COLOR][/B]','pakindiasport',4,'http://www.madhyamam.com/en/sites/default/files/india-pak.jpg',fanart,'')
	#addDir('[COLOR white][B]Snappy Streamz[/COLOR][/B]','snappystreams',4,'https://www.apkdld.com/wp-content/uploads/2017/06/snappy-streamz-apk-300x293.jpg',fanart,'')
	#addDir('[COLOR white][B]Swift Streamz[/COLOR][/B]','swiftstreams',4,'http://www.swiftstreamz.com/images/mbl-app.png',fanart,'')
	#addDir('[COLOR white][B]UKTV Now[/COLOR][/B]','uktvnow',4,'https://kodicommunity.com/wp-content/uploads/2016/06/uk-tv-now-addon-plugin-xbmc-kodi1-1.png',fanart,'')
	#addDir('[COLOR white][B]TV Online Plus+[/COLOR][/B]','tvonlineplus',4,'https://1.bp.blogspot.com/-I_th1gsuna8/WRsJAg3SqMI/AAAAAAAAGdk/J-YznRwYMaMB_Y9ZINmhQzyvopkAbtA1wCLcB/s200/18424147_301931813588370_8617351845985017033_n.jpg',fanart,'')	
	#addDir('[COLOR white][B]Swift Streams[/COLOR][/B]','swiftstreams',4,'https://i.ytimg.com/vi/SZ5BkBmHbFk/hqdefault.jpg',fanart,'')

	
def get(url):
	if url == 'sourceetv':
		sourcetv()
	elif url == 'swiftstreams':
		swiftstreams()
	elif 'swiftstreamz.com' in url:
		swiftstreamschans(url)
	elif url == 'snappystreams':
		snappystreams()
	elif 'SnappyStreamz' in url:
		snappystreamschans(url)
	elif url == 'mobdro':
		mobdro()
	elif url == 'livetv':
		livetv()
	elif url == 'geotv':
		geotv()
	elif '173.212.206.199' in url:
		geotvchans(url)
	elif 'pakindiasport' in url:
		pakindiasport()
	elif url == 'edoctor':
		edoctor()
	elif url == 'mobiletv':
		mobiletv()
	elif 'mobiletv:' in url:
		mobiletvchans(url)
	elif url == 'tvonlineplus':
		tvonlineplus()
	elif 'tvonlineplus:' in url:
		tvonlinepluschans(url)
	elif url == 'dhamkatv':
		dhamkatv()
	elif url == 'cricket':
		cricket()
	elif url == 'iptvrestream':
		iptvrestream()
	elif url ==  'uktvnow':
		uktvnow()
	elif 'UKTVNOW:' in url:
		uktvnowChannels(url)
	elif url == 'megaiptv':
		megaiptv()
	
username   ='-1'


def megaiptv():
	r = requests.get('http://pejaguide.com/IPTVv3/World/kategoria.php?kategoria=kategorit&udb=1234&pdb=12345',headers={'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G928F Build/NRD90M)'}).text
	all = regex_get_all(r,'<kategoria>','</kategoria>')
	for a in all:
		name = regex_from_to(a,'<emri>','</emri>')
		url  = regex_from_to(a,'<linku>','</linku>')
		icon = regex_from_to(a,'<fotografia>','</fotografia>')
		if not 'VOD' in name:addDir(name,urllib.quote_plus(url.replace('&amp;','&')),3,icon,fanart,'')
def uktvnow():
	addDir('All Channels','UKTVNOW:0',4,icon,fanart,'')
	addDir('Entertainment','UKTVNOW:1',4,icon,fanart,'')
	addDir('Movies','UKTVNOW:2',4,icon,fanart,'')
	addDir('Sports','UKTVNOW:5',4,icon,fanart,'')
	addDir('Music','UKTVNOW:3',4,icon,fanart,'')
	addDir('News','UKTVNOW:4',4,icon,fanart,'')
	addDir('Documentary','UKTVNOW:6',4,icon,fanart,'')
	addDir('Kids Corner','UKTVNOW:7',4,icon,fanart,'')
	addDir('Food','UKTVNOW:8',4,icon,fanart,'')
	
def uktvnowgetChannels():
	
	token=getToken('http://uktvnow.net/uktvnow8/index.php?case=get_all_channels',username)
	print "ASDASDAADS"
	headers={'User-Agent':'USER-AGENT-UKTVNOW-APP-V2','app-token':token}
	#headers={}
	postdata={'username':username}
	print requests.post('http://uktvnow.net/uktvnow8/index.php?case=get_all_channels',data=postdata,headers=headers, verify=False).content
	channels = requests.post('http://uktvnow.net/uktvnow8/index.php?case=get_all_channels',data=postdata,headers=headers, verify=False).content
	print channels
	channels = channels.replace('\/','/')
	print channels
	match=re.compile('"pk_id":"(.+?)","channel_name":"(.+?)","img":"(.+?)","http_stream":"(.+?)","rtmp_stream":"(.+?)","cat_id":"(.+?)"').findall(channels)
	return match
	
def getToken(url, username):
	s = base64.b64decode("dWt0dm5vdy10b2tlbi0tX3xfLSVzLXVrdHZub3dfdG9rZW5fZ2VuZXJhdGlvbi0lcy1ffF8tMTIzNDU2X3VrdHZub3dfNjU0MzIx")%(url,username)
	import hashlib
	return hashlib.md5(s).hexdigest()


def uktvnowChannels(url):

	url   = url.replace('UKTVNOW:','')
	match = uktvnowgetChannels()
	for channelid,name,iconimage,stream1,stream2,cat in match:
		thumb='https://app.uktvnow.net/'+iconimage+'|User-Agent=Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G935F Build/MMB29K)'
		if url=='0':addDir(name,'UKTVNOW',9999,thumb,fanart,channelid)
		if cat==url:addDir(name,'UKTVNOW',9999,thumb,fanart,channelid)
		
		
###############################################################################
	
def cricket():
	import urllib
	open = requests.get('http://aps.dynns.com/apps/output.php/playlist?type=xml&deviceSn=ipl2017&token=MTU2OTc1NjczM0AybmQyQDE1MDA0NTk4MDQ=',headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)','Authorization':'Basic YWRtaW46QWxsYWgxQA==','Accept':'gzip'}).text
	all  = regex_get_all(open,'<items>','</items>')
	for a in all:
		cat  = regex_from_to(a,'<programCategory>','</programCategory>')
		name = regex_from_to(a,'<programTitle>','</programTitle>')
		url  = regex_from_to(a,'<programURL>','</programURL>')
		icon = regex_from_to(a,'<programImage>','</programImage>')
		addDir('[COLOR ghostwhite]%s[/COLOR] - %s'%(cat,name),urllib.quote_plus(url+'?wmsAuthSign=c2VydmVyX3RpbWU9Ny8xOS8yMDE3IDk6NDc6MDYgQU0maGFzaF92YWx1ZT1VNk9yVFRrWmdwMjRxN0UzRllxRjRnPT0mdmFsaWRtaW51dGVzPTI'),9999,icon,fanart,'')	
		
		
def dhamkatv():
	
	open = requests.get('http://aps.dynns.com/apps/output.php/playlist?type=xml&deviceSn=dhamkatv&token=MTU2OTc1NTQzMEAybmQyQDE1MDA0NTg1MDE=',headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)','Authorization':'Basic YWRtaW46QWxsYWgxQA==','Accept':'gzip'}).text
	all  = regex_get_all(open,'<items>','</items>')
	for a in all:
		cat  = regex_from_to(a,'<programCategory>','</programCategory>')
		name = regex_from_to(a,'<programTitle>','</programTitle>')
		url  = regex_from_to(a,'<programURL>','</programURL>')
		icon = regex_from_to(a,'<programImage>','</programImage>')
		addDir('[COLOR ghostwhite]%s[/COLOR] - %s'%(cat,name),'DHMAKATV:'+url,10,icon,fanart,'')	

		
def iptvrestream():
	open = requests.get('http://pastebin.com/raw/wZxQt9Lh',verify=False).text
	
	m3u  = requests.get(open,headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)'}).text
	
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(m3u)
	for name,url in regex:
		url  = url.encode('ascii', 'ignore')
		name = name.encode('ascii', 'ignore')
		addDir(name.strip(),url.strip(),10,icon,fanart,'')


	
def tvonlineplus():
	open = requests.get('http://proxykingpro.com/tvonlineplus/api.php',headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)'}).text
	json = json.loads(open)
	js   = json['LIVETV']
	for a in js:
		name = a['category_name']
		id   = a['cid']
		icon = a['category_image']
		addDir(name,'tvonlineplus:'+id,4,'http://proxykingpro.com/tvonlineplus/images/'+icon,fanart,'')
		
def tvonlinepluschans(url):
	id  = (url).replace('tvonlineplus:','')
	
	url = 'http://proxykingpro.com/tvonlineplus/api.php?cat_id=%s'%id
	
	open = requests.get(url,headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)'}).text
	json = json.loads(open)
	js   = json['LIVETV']
	for a in js:
		name = a['channel_title']
		url  = a['channel_url']
		url  = url.encode('ascii', 'ignore')
		icon = a['channel_thumbnail']

		addDir(name.encode('ascii', 'ignore'),urllib.quote_plus(url+'|User-Agent=Lavf/56.15.102'),9999,'http://proxykingpro.com/tvonlineplus/images/'+icon.encode('ascii', 'ignore'),fanart,'')
	
	
def mobiletv():
	addDir('HQ Links','mobiletv:http://sportstv.club/playlist/mobiletv.m3u',4,icon,fanart,'')
	addDir('Entertainment/Movies Links','mobiletv:'+urllib.quote_plus('http://sportstv.club/playlist/Movies&Entertainment.m3u'),4,icon,fanart,'')
	addDir('Indian Links','mobiletv:http://sportstv.club/playlist/indian.m3u',4,icon,fanart,'')
	addDir('2G Links','mobiletv:http://sportstv.club/playlist/2g.m3u',4,icon,fanart,'')
	addDir('IPL','mobiletv:http://sportstv.club/playlist/iPl2017.m3u',4,icon,fanart,'')
	
	
	
		
def mobiletvchans(url):
	headers = {'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)',
		'Accept-Encoding':'gzip'}
	
	url     = (url).replace('mobiletv:','')
	open    = requests.get(url,headers=headers).text
	regex   = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		addDir(name,url,10,icon,fanart,'')

def edoctor():
	open = OPEN_URL('https://raw.githubusercontent.com/hadjistyllis/myapp/master/TV%20category.m3u')
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		if not 'youtube' in name:
			addDir(name,url,10,icon,fanart,'')

def pakindiasport():
    import urllib,urllib2,base64,json
    req = urllib2.Request( base64.b64decode('aHR0cDovL3NtYXJ0ZXJsb2dpeC5jb20vTmV3QXBwcy9QYWtJbmRpYVNwb3J0c0hEL1YxLTAvbWFpbkNvbnRlbnQucGhw') )      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwSW5kaWElMjBTcG9ydHMlMjBIRC8xLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWtGM1lURXdjenAwZHpGdWEyd3pRbUZ1UVc1Qk5qZzM=")) 
    response = urllib2.urlopen(req)
    link=response.read()
    from resources.modules import rc
    cryptor=rc.RNCryptor()
    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("YkFuZ3I0bDF0dGwzNTY3"))
    
    decrypted_data=json.loads(decrypted_data)
    dataUrl=decrypted_data[0]["dataUrl"]

    req = urllib2.Request( dataUrl)      
    req.add_header(base64.b64decode("VXNlci1BZ2VudA=="),base64.b64decode("UGFrJTIwSW5kaWElMjBTcG9ydHMlMjBIRC8xLjAgQ0ZOZXR3b3JrLzc1OC4wLjIgRGFyd2luLzE1LjAuMA==")) 
    req.add_header(base64.b64decode("QXV0aG9yaXphdGlvbg=="),base64.b64decode("QmFzaWMgYWtGM1lURXdjenAwZHpGdWEyd3pRbUZ1UVc1Qk5qZzM=")) 
    response = urllib2.urlopen(req)
    link=response.read()

    d=base64.b64decode(link)    
    decrypted_data = cryptor.decrypt(d, base64.b64decode("YkFuZ3I0bDF0dGwzNTY3"))
    
    jsondata=json.loads(decrypted_data)
    for a in jsondata:#Cricket#
	
                name=a["channelName"]
                
                url =a["channelLink"]+'|User-Agent=AppleCoreMedia/1.0.0.13A452 (iPhone; U; CPU OS 9_0_2 like Mac OS X; en_gb)' 
				
                icon=a["categoryLogo"]
                addDir(name,urllib.quote_plus(url),9999,urllib.quote_plus(icon),fanart,'')
		
def geotv():
	open = requests.get('http://173.212.206.199:25461/enigma2.php?username=geop&password=pocket&type=get_live_categories',headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)'}).text
	all_cats = regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		if not 'UK/USA/CAN' in name:
			if not 'MALAY/THAI' in name:
				if not 'NEPALI' in name:
					addDir(name,urllib.quote_plus(url1),4,'https://image.winudf.com/v2/image/Y29tLnNuci5lbnRfaWNvbl8wX2I0N2VlYjZi/icon.png?w=170&fakeurl=1&type=.png',fanart,'')
		
def geotvchans(url):
	open = requests.get(url,headers={'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)'}).text
	all_cats = regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		log(a)
		name = regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		name = re.sub('\[.*?min ','-',name)
		thumb= regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = regex_from_to(a,'<description>','</description>')
		addDir(name,urllib.quote_plus(url1),10,thumb,fanart,base64.b64decode(desc))
		
def livetv():
	import re
	open = OPEN_URL('http://163.172.89.151:25461/get.php?username=iptvrestream.net&password=wC5Qtu9Zbl&type=m3u&output=ts')
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		addDir(name,url,10,icon,fanart,'')
		
		
def mobdro():
        import re
        file = xbmc.translatePath('special://home/addons/script.cypherstream/resources/')
        if os.path.exists(file):
            file = open(os.path.join(file, 'mobdrochans.txt'))
            data = file.read()
            file.close()
			
            all   = re.compile('\n([^:]+):(mpd://[^\n]+)').findall(data)
            for name,url in all:
				addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,'http://geekpeaksoftware.com/wp-content/uploads/2016/10/mobdro.png',fanart,'')
				

		
def swiftstreams():
	import json,requests
	url = 'http://swiftstreamz.com/SwiftStreamz/api.php'
	
	headers = {'Authorization': 'Basic QFN3aWZ0MTEjOkBTd2lmdDExIw',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get(url,headers=headers).text
	js   = json.loads(open)
	js   = js['LIVETV']
	for a in js:
		name = a['category_name']
		id   = a['cid']
		icon = a['category_image']
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'http://swiftstreamz.com/SwiftStreamz/api.php?cat_id='+id,4,'http://swiftstreamz.com/SwiftStream/images/thumbs' + icon,fanart,'')
		
		
def swiftstreamschans(url):
	import json,requests

	headers = {'Authorization': 'Basic QFN3aWZ0MTEjOkBTd2lmdDExIw',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get(url,headers=headers).text
	js   = json.loads(open)
	js   = js['LIVETV']
	for a in js:
		name = a['channel_title']
		url  = a['channel_url']
		icon = a['channel_thumbnail']
		desc = a['channel_desc']
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'swift:'+url,10,'http://swiftstreamz.com/SwiftStream/images/thumbs/' + icon,fanart,desc)
		
		
def snappystreams():
	import json,requests
	url = 'http://swiftstreamz.com/SnappyStreamz/api.php'
	
	headers = {'Authorization': 'Basic QFN3aWZ0MTEjOkBTd2lmdDExIw==',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get(url,headers=headers).text
	js   = json.loads(open)
	js   = js['LIVETV']
	for a in js:
		name = a['category_name']
		id   = a['cid']
		icon = a['category_image']
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'http://swiftstreamz.com/SnappyStreamz/api.php?cat_id='+id,4,'http://swiftstreamz.com/SwiftStream/images/thumbs' + icon,fanart,'')
		
		
def snappystreamschans(url):
	import json,requests

	headers = {'Authorization': 'Basic QFN3aWZ0MTEjOkBTd2lmdDExIw',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get(url,headers=headers).text
	js   = json.loads(open)
	js   = js['LIVETV']
	for a in js:
		name = a['channel_title']
		url  = a['channel_url']
		icon = a['channel_thumbnail']
		desc = a['channel_desc']
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'swift:'+url,10,'http://swiftstreamz.com/SwiftStream/images/thumbs/' + icon,fanart,desc)
		
######################################################################################################
		
		
		
def regex_from_to(text, from_string, to_string, excluding=True):
	import re,string
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	import re,string
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r



def OPEN_URL(url):
	
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
logfile    = xbmc.translatePath(os.path.join('special://home/addons/script.cypherstream', 'log.txt'))

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	

		
		
def addDir(name,url,mode,iconimage,fanart,description):
	import xbmcgui,xbmcplugin,urllib,sys
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==102 or mode==9999 or mode==99999 or mode==10:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory