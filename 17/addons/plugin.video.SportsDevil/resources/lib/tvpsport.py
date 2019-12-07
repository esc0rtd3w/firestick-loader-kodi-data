# -*- coding: utf-8 -*-
import urllib2,urllib
import cookielib
import threading
import re
import time
import json
import xbmc
from datetime import datetime
BASEURL='http://sport.tvp.pl'
proxy={}
TIMEOUT = 10
BRAMKA='http://www.bramka.proxy.net.pl/index.php?q='
BRAMKA3='https://darmowe-proxy.pl'
COOKIEFILE = ''

def getPhotoLink(uid):
    retVal=''
    h1=uid[0]
    h2=uid[1]
    h3=uid[2]
    ext=uid[-4:]
    hash=uid[:-4]
    width='640'
    heigth='360'
    retVal += "http://s.tvp.pl/images/";
    retVal += h1;
    retVal += "/";
    retVal += h2;
    retVal += "/";
    retVal += h3;
    retVal += "/";
    retVal += "uid_" + hash + "_width_" + width + "_height_" + heigth + "_gs_0" + ext;
    return retVal
	
#/self.image = 'http://s.tvp.pl/images/c/4/6/uid_c46b86c16a54c00b2de2b4789d9142851484890841049_width_640_height_360_gs_0.jpg';	
	
	
 #       self.getPhotoLink = function(filename, heigth, width ){
 #
 #           if (filename.length < 34) return "";
 #           if (!filename.indexOf(".")) return "";
 #           if (heigth < 0 || width < 0) return "";
 #
 #           var retVal = "";
 #           try {
 #               retVal += "http://s.tvp.pl/images/";
 #
 #
 #               var hash = getFileName(filename);
 #               var extension = getFileExtension(filename);
 #
 #               var h1, h2, h3;
 #               h1 = filename[0];
 #               h2 = filename[1];
 #               h3 = filename[2];
 #
 #               retVal += h1;
 #               retVal += "/";
 #               retVal += h2;
 #               retVal += "/";
 #               retVal += h3;
 #               retVal += "/";
 #
 #               retVal += "uid_" + hash + "_width_" + width + "_height_" + heigth + "_gs_0" + extension;
 #
 #           } catch (Exception) { return ""; }




UA='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
cs=''
def getUrl(url,proxy={},timeout=TIMEOUT,cookies=True):
	global cs
	cookie=[]
	if proxy:
		urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler(proxy)))
	elif cookies:
		cookie = cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
	try:
		response = urllib2.urlopen(req,timeout=timeout)
		linkSRC = response.read()
		response.close()
	except:
		linkSRC=''
	cs = ''.join(['%s=%s;'%(c.name, c.value) for c in cookie])
	return linkSRC
def suma(czas):
    y, m, d = czas.split('-')
    return int(y)*365 + int(m)*30 + int(d)	
def sekundy(czas):
    g, m = czas.split(':')
    return int(g) * 3600 + int(m) * 60
	
def getChannels(url='http://sport.tvp.pl/transmisje'):
	teraz=datetime.now().strftime("%Y-%m-%d %H:%M").split(' ')#[0]
	godzteraz=sekundy(teraz[1])
	dzissum=suma(teraz[0])
	now2=teraz[0].split('-')
	mies=now2[1]
	dzien=now2[2]
	jutro=('{:02}'.format(int(dzien)+1))
	pojutrze=('{:02}'.format(int(dzien)+2))
	out=[]
	content=getUrl('http://www.api.v3.tvp.pl/shared/listing_blackburst.php?dump=json&nocount=1&type=video&parent_id=40537342&copy=false&direct=false&order=release_date_long,-1&count=-1')
	html=json.loads(content)
	items = html.get('items', [])
	for item in items:
		try:
			imag= item.get('image',[])[0].get("file_name",'')
			img= getPhotoLink(imag)
		except:
			img=''
		tyt= item.get('title','')
		dat=item.get("release_date_dt",'')
		datkon=item.get("broadcast_end_date_dt",'')
		datkonsum=suma(datkon)
		datsum=suma(dat)

		if suma(dat)<suma(teraz[0]):
			continue		
		godz= item.get("release_date_hour",'')  
		godzkon= item.get("broadcast_end_date_hour",'')  		
		if suma(datkon)==suma(teraz[0]) and sekundy(godzkon)<sekundy(teraz[1]):
			continue
		id= item.get('video_id','') 
		trwa= item.get('playable','') 
		mies2=dat.split('-')[1]
		day2=dat.split('-')[2]
		kiedy=dat
		if mies==mies2 and dzien==day2:
			kiedy='dzisiaj'
		elif mies==mies2 and day2==jutro:
			kiedy='jutro'		
		elif mies==mies2 and day2==pojutrze:
			kiedy='pojutrze'	
		plot='[B][COLOR blue]%s[/COLOR] o [COLOR gold]%s[/COLOR][CR]%s[/B]'%(kiedy,godz,tyt)
		code = '[B][COLOR lightgreen]%s[/COLOR][/B]'%(kiedy)		
		t=u'[COLOR orangered]■[/COLOR][B] [COLOR khaki]%s : [/COLOR][COLOR gold]%s[/COLOR][/B]'%(godz,tyt)	
		if trwa:
			t=u'[COLOR lime]►[/COLOR][B] [COLOR khaki]%s : [/COLOR][COLOR gold]%s[/COLOR][/B]'%(godz,tyt)	
		out.append({'title':t,'href':id,'image':img,'code':code,'plot':plot})
	return out
def getProxyList():
	content=getUrl('http://www.idcloak.com/proxylist/free-proxy-list-poland.html')
	speed = re.compile('<div style="width:\\d+%" title="(\\d+)%"></div>').findall(content)
	trs = re.compile('<td>(http[s]*)</td><td>(\\d+)</td><td>(.*?)</td>',re.DOTALL).findall(content)
	proxies=[{x[0]: '%s:%s'%(x[2],x[1])} for x in trs]
	return proxies
def getTVPstream(url):
	if url=='':
		return vid_link
	if url.startswith('http://sport.tvp.pl'):
		content = getUrl(url)
	else:
		content = getUrl(BASEURL+url)
	src = re.compile('data-src="(.*?)"', re.DOTALL).findall(content)
	if src:
		vid_link=BASEURL+src[0]
	return vid_link
def getChannelVideo(ex_link):
	
	if ex_link:
		url = 'https://sport.tvp.pl/sess/tvplayer.php?object_id=%s&force_original_for_tracking=1&nextprev=1&autoplay=true&copy_id=%s'%(ex_link,ex_link) if ex_link else ''
		stream_url = decodeUrl(url)
		proxy=False
		if not stream_url or 'material_niedostepny' in stream_url :
			stream_url = decodeUrl(url,use='pgate5')			
			if not stream_url or 'material_niedostepny' in stream_url :
				stream_url = decodeUrl(url,use='pgate3')						
			if not stream_url or 'material_niedostepny' in stream_url :
				stream_url = decodeUrl(url,use='proxy')				
			proxy=True
	else:
		stream_url=''
		proxy=False
	return stream_url,proxy
	
def getUrlProxy2(url):	
	import requests
	global COOKIEFILE
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': 'https://darmowe-proxy.pl/',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'TE': 'Trailers',
	}
	req=requests.get(BRAMKA3,headers=headers)
	cookies=req.cookies
	data = {'u': url,'encodeURL': 'on','encodePage': 'on','allowCookies': 'on'}
	data = urllib.urlencode(data)
	vurl = BRAMKA3+'/includes/process.php?action=update'
	link=requests.post(vurl,data=data,headers=headers,cookies=cookies).content
	return link		
	
def getUrlProxy5(url):	
	import requests
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': 'https://www.sslsecureproxy.com/',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
	}
	html=requests.get('https://www.sslsecureproxy.com/',headers=headers).content
	selip=re.findall('"(.+?)">Poland',html)[0]
	data = {
	'u': url,
	'u_default': 'https://www.google.com/',
	'urlsub': '',
	'server_name': 'pl',
	'selip': selip,
	'customip': '',
	'allowCookies': 'on',
	'autoPermalink': 'on'
	}

	response = requests.post('https://www.sslsecureproxy.com/query', headers=headers, data=data).content
	return response
	
def decodeUrl(url='http://sport.tvp.pl/sess/tvplayer.php?copy_id=35828270&object_id=35828270&autoplay=true',use=''):
	vid_link=''
	if not url: return vid_link
	if use=='pgage':
		data = getUrl(BRAMKA+urllib.quote_plus(url)+'&hl=2a5')
		vid_link = getM3u8src(data)

	elif use=='pgate5':
		data = getUrlProxy5(url)
		vid_link = getM3u8src(data)
	
	elif use=='pgate3':	
		data=getUrlProxy2(url)
		vid_link = getM3u8src(data)
		
	elif use=='proxy':
		
		proxies = getProxyList()
		listOUT = list()
		prList = [[] for x in proxies]
		for i,proxy in enumerate(proxies):
			thread = threading.Thread(name='Thread%d'%i, target = chckPrList, args=[url,proxy,prList,i])
			listOUT.append(thread)
			thread.start()
		while any([i.isAlive() for i in listOUT]) and len(vid_link)==0:
			for l in prList:
				l = prList[3]
				if isinstance(l,list):
					vid_link = l
					break
			time.sleep(0.1)
		del listOUT[:]
	else:
		data = getUrl(url)
		vid_link = getM3u8src(data)
	return vid_link
	
def getM3u8src(data):
	vid_link=''
	vid_link = re.compile('1:{src[:\\s]+[\'"](.+?)[\'"]', re.DOTALL).findall(data)
	if not vid_link:
		vid_link = re.compile("0:{src:'(.+?)'", re.DOTALL).findall(data)
	vid_link = vid_link[0] if vid_link else ''
	return vid_link
	
def chckPrList(ex_link ,proxy, prList, index):
	data = getUrl(ex_link,proxy,timeout=10)
	linkSRC = m3u8Quality(getM3u8src(data))
	prList[index]= linkSRC if not 'material_niedostepny' in linkSRC else ''
	
def m3u8Quality(url):
	out=url
	if url and url.endswith('.m3u8'):
		srcm3u8 = re.search('/(\\w+)\\.m3u8',url)
		srcm3u8 = srcm3u8.group(1) if srcm3u8 else 'manifest'
		content = getUrl(url)
		matches=re.compile('RESOLUTION=(.*?)\r\n(QualityLevels\\(.*\\)/manifest\\(format=m3u8-aapl\\))').findall(content)
		if matches:
			out=[{'title':'auto','url':url}]
			for title, part in matches:
				one={'title':title,'url':url.replace(srcm3u8,part)}
				out.append(one)
	return out
