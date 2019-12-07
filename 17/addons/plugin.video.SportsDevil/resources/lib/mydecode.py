# -*- coding: utf-8 -*-
import sys
import re
import urllib2,urllib
import base64
import urlparse
import jsunpack
import cookielib
import requests
import gzip
from StringIO import StringIO
sess=requests.Session()

UACHR = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
UA='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
packer = re.compile('(eval\(function\(p,a,c,k,e,(?:r|d).*)')
clappr = re.compile('new\s+Clappr\.Player\(\{\s*?source:\s*?["\'](.+?)["\']')
source = re.compile('sources\s*:\s*\[\s*\{\s*(?:type\s*:\s*[\'\"].+?[\'\"],|)src\s*:\s*[\'\"](.+?)[\'\"]')

def getUrl(url,data=None,header={},cookies=None):
    if not header:
        header = {'User-Agent':UA}
    req = urllib2.Request(url,data,headers=header)
    try:
        response = urllib2.urlopen(req, timeout=10)
        link = response.read()
        response.close()
    except:
        link=''
    return link

def get_url_(url,cj,header={},cookies=None):
    headers = {'User-Agent':UA}
    headers.update(header)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    req = urllib2.Request(url,data=None,headers=header)
    response = urllib2.urlopen(req, timeout=15)
    link = response.read()
    response.close()
    return link
def decodeSecur(data):
    srcs = []
    if 'iframe-secure' in data:
        ifrSec = re.compile('src="(//iframe-secure.*?)"',re.DOTALL|re.IGNORECASE).findall(data)
        id = ifrSec[0].split('/')[-1] if ifrSec else ''
        url = 'http://iframe-secured.com/embed/iframe.php?u='+id
        header= {'User-Agent':UA,'Referer':'http://iframe-secured.com/embed/'+id}
        contentDec = getUrl(url,header=header)
        match = re.compile('(eval\\(function\\(p,a,c,k,e,d\\).*?)\n').findall(contentDec)
        if match:
            contentVideo = jsunpack.unpack(match[0]).decode('string_escape')
            srcs=re.findall('window.location.replace\\([\'"](.*?)[\'"]',contentVideo)
    return srcs
def debug(deb):
    pass
def decode(url,data):

	srcs=re.compile('src=["\']\\s*((?:http|).*?)["\']',re.DOTALL+re.IGNORECASE).findall(data)
	m3ux=re.findall("""source: atob\(["\'](.+?)["\']""",data,re.DOTALL)
	if m3ux:
		vidurl=base64.b64decode(m3ux[0])
		return vidurl+'|User-Agent'+urllib.quote(UA)+'&Referer='+url
	
	try:

		for query in srcs:	

			query = query.replace('\n','').replace('\r','')
			if 'livecounter' in query or 'pagead2.google' in query or 'imgur.com' in query or 'platform.twitter' in query or 'googletagmanager.com' in query:
				continue
			if 'ripple.is' in query:

				return _rippleis(query,data,url)
			if '/embed/' in query and 'exprestream.com' in url:

				return _exprestreamcom(query,data,url)
				
			if './../ss' in query and 'dubs.to' in url:

				return _dubsto(query,data,url)
				
			elif 'telerium' in query:
				debug('@telerium')

				return _telerium(query,data,url)
			elif 'soccerlive.xyz' in query:
				return _soccerlivexyz(query,data,url)
			
			elif 'livesport4u.pw' in query:
				return _livesport4upw(query,data,url)
			
			
			
			elif 'arembed.com' in query:
				return _arembedcom(query,data,url)
			
			#$"http://sportlive.site
			elif 'sportlive.site' in query:
				return _sportlivesite(query,data,url)
				
			elif 'streamcdn.to' in query:
				return _streamcdnto(query,data,url)	
				
				
				
			elif 'flowframes.online' in query:
				return _flowframesonline(query,data,url)

			elif 'strims.tv' in query:
			
				return _strimstv(query,data,url)	


		
			elif 'sportsbay.org' in query:
				return _sportsbayorg(query,data,url)
		
			#elif 'crackstreams.com' in query:
			#	return _crackstreamscom(query,data,url)
		
		
			elif 'tvsport.ws' in query:
				return _tvsportws(query,data,url)
			
			elif 'whd365.pro' in query:
				return _whd365pro(query,data,url)	

				
			elif 'olimp-app.ru' in query:
				return _olimpappru(query,data,url)	
			elif 'sport7.biz' in query:
				return _sport7biz(query,data,url)	
				
			#yoursports.stream
			elif 'youtube.com' in query or 'youtu.be' in query:
				return query
				
			elif 'yoursports.stream' in query:
				return _yoursportsstream(query,data,url)
			
			
			elif 'yrsprts.xyz' in query:
				return _yrsprts(query,data,url)

			
			elif 'h247bay.js' in query:
				return _h247bay(query,data,url)
			
			
			
			elif 'soccerlive.uk' in query:
				return _soccerliveuk(query,data,url)		
				
				
			elif 'wstream.to' in query:
				return _wstreamto(query,data,url)
		
				

			elif 'hazmolive.stream' in query:
				return _hazmostream(query,data,url)
			elif 'hazmo.stream' in query:
				return _hazmostream2(query,data,url)
	
			elif 'soccershow.xyz' in query:
				return _hdstreamsclub2(query,data,url)
		
			elif 'hdstreams.club/page' in query:
				return _hdstreamsclub2(query,data,url)
	
			elif 'streamcdn.co' in query:
				return _streamcdnco(query,data,url)
				
			elif 'studiojunction.live' in query:
				return _studiojunctionlive(query,data,url)
		
			elif 'dailyhealthandcare.com' in query:
				return _dailyhealthandcare(query,data,url)
		
		
			elif '7streams.pro' in query:
				return _7streamspro(query,data,url)
		
		
			elif 'strimstv.eu' in query:
				return _strimstveu(query,data,url)
				
			elif 'bnk.sportz.is' in query:
				return _bnksportzis(query,data,url)
				
			elif 'sdfgdf.xyz' in query:

				return _sdfgdfxyz(query,data,url)			
				
			elif 'bfst.to' in query:

				return _bfstto(query,data,url)					
			elif 'vsdea.me' in query:

				return _vsdeame(query,data,url)

				
			elif 'twojetv.ws' in query:
				debug('@@aliez')
				return _twojetv(query,data,url)	
				
			elif 'bankai.stream' in query:
				debug('@@aliez')
				return _bankaistream(query,data,url)					
			elif 'aliez.me' in query:
				debug('@@aliez')
				return _aliezme(query,data,url)				
			elif '1me.club' in url:
				return _1meclub(data,url)	
			
			elif 'pcast.pw/static/embed' in query:
				return _pcastpw(query,data,url)	
			
			elif 'sports-stream.net/ch/sps.php' in query:
				return _sportsstreamnet(query,data,url)	
				
			elif 'sportzonline.pw' in query:
				return _sportzonlinepw(query,data,url)	

			elif 'sportzonline' in query:
				return _sportzonlinepw(query,data,url)	

				
			elif 'tumarcador.xyz' in query:
				return _tumarcadorxyz(query,data,url)	

				
			elif 'realcam.pw/embed' in query:
				return _realcampw(query,data,url)				
							
			elif 'livesport4u.com' in query:
				return _livesport4ucom(query,data,url)
				
			elif 'nowlive.pro' in query:
				return _nowlivepro(query,data,url)					
				
			elif 'streamup.me/livetv/' in query:
				return _streamupme(query,data,url)				
				
			elif 'hdstreams.club/page' in url:
				return _hdstreamsclub(data,url)
							
			elif 'bonstreams.net/footstream/hd.php' in url:
				return _bonstreams(data,url)
				
			elif 'whostreams' in query:
				return _whostreams(query,data,url)
		
			elif 'ucasterplayer.com/static/scripts/hucaster' in query:
				return _ucasterplayer(query,data,url)	
			
			
			elif 'webtv.ws' in query:
				return _webtv(query,data,url)
			elif 'www.wlive.tv/embed' in query:
				return _wlivetv(query,data,url)
				
			elif 'assia.tv' in query:
				return _assiatv(query,data,url)				

				
			elif 'sawlive.tv' in url:
				return _sawlivetv2(query,data,url)				
							
			elif 'hdcast.me/' in query:
				return _hdcastme(query,data,url)	

			elif 'fstream.me' in query:
				return _fstreamme(query,data,url)
			

			elif 'embed.pot-iptv' in query:
				debug('@embed.pot-iptv')
				return _embedpot_iptv(query,data,url)
			elif 'vvcast' in query:
				debug('@vvcast')
				return _vvcast(query,data,url)
			elif 'tvp.pl/sess/tvplayer.php' in query:
				debug('@tvp.pl tvplayer')
				return _tvpPlayer(query,data,url)
			elif 'byetv' in query:
				debug('@byetv')
				return _byetv(query,data,url)
			elif 'veecast' in query:
				debug('@veecast')
				return _veecast(query,data,url)
			elif 'srkcast' in query:
				debug('@_srkcast')
				return _srkcast(query,data,url)
			elif 'sharecast' in query:
				debug('@_sharecast')
				return _sharecast(query,data,url)
			elif 'lima-city.de' in query:
				debug('@_lima-city.de')
				return _limacity(query,data,url)
			elif 'ustream.tv' in query:
				debug('@_ustream.tv')
				return _ustream(query,data,url)
			elif 'ustreamix.com' in query or 'ustreamyx' in query:
				debug('@_ustreamix.com')
				return _ustreamix(query,data,url)
			elif 'dailymotion.com' in query:
				debug('@dailymotion.com')
				return _dailymotion(query,data,url)
			elif 'www.jazztv.co' in query:
				debug('@jazztv.co')
				return _jazztv(query,data,url)
			elif 'urhd.tv' in query:
				debug('@urhd.tv')
				return _urhdtv(query,data,url)
			elif 'tv.jardello.com' in query:
				debug('@tv.jardello.com')
				return _jardello(query,data,url)
			elif 'cricfree.sc' in query:
				debug('@cricfree.sc')
				return _cricfree(query,data,url)
			elif 'static.nowlive.club' in query:
				debug('@static.nowlive.club')
				return _staticnowliveclub(query,data,url)
			elif 'abcast.net' in query:
				debug('@abcast.net')
				return _abcastnet(query,data,url)
			elif 'freelive365.com' in query:
				debug('@freelive365.com')
				return _freelive365(query,data,url)
			elif 'cast4u.tv' in query:
				debug('@cast4u.tv')
				return _cast4utv(query,data,url)
			elif 'osgchmura.tk' in query:
				debug('@osgchmura')
				return _osgchmura(query,data,url)
			elif 'static.u-pro.fr' in query:
				debug('@static.u-pro.fr')
				return _staticu_profr(query,data,url)
			elif 'widestream.io' in query:
				debug('@@widestream.io')
				return _widestream(query,data,url)
			elif 'static.nowlive.xyz' in query:
				debug('@@static.nowlive')
				return _staticnowlive(query,data,url)
			elif 'delta-live.pro' in query:
				debug('@@delta-live.pro')
				return _deltalivepro(query,data,url)
			elif 'openlive.org' in query:
				debug('@@openlive.org')
				return _openliveorg(query,data,url)
			elif 'sawlive.tv' in query:
				debug('@@sawlive.tv' )
				return _sawlivetv(query,data,url)
			elif 'pxstream.tv' in query:
				debug('@@pxstream')
				return _pxstream(query,data,url)
			elif 'myfreshinfo' in query:
				debug('@@myfreshinfo')
				return _myfreshinfo(query,data,url)
			elif 'cinema-tv.xyz' in query:
				debug('@@cinema-tv.xyz')
				return _cinematvxyz(query,data,url)
			elif 'flowplayer' in query:
				debug('@@flowplayer')
				return _flowplayer(query,data,url)
			elif 'shidurlive' in query:
				debug('@@shidurlive')
				return _shidurlive(query,data,url)
			elif 'freedocast' in query:
				debug('@@freedocast')
				return _freedocast(query,data,url)
			elif 'tvope' in query:
				debug('@@tvope')
				return _tvope(query,data,url)
			elif 'dotstream.tv' in query:
				debug('@@dotstream')
				return _dotstream(query,data,url)
			elif 'bro.adca.st' in query:
				debug('@@bro.adca.st')
				return _broadcast(query,data,url)
			elif 'jwpsrv.com' in query:
				debug('@@jwpsrv')
				return _jwpsrv(query,data)
			elif 'jwpcdn.com' in query:
				debug('@@jwpcdn')
				return _jwpcdn(query,data,url)		

			elif 'ustream' in query:
				debug('@@ustream')
				return _ustream(query,data)
			elif 'castto.me' in query:
				debug('@@castto')
				return _casttome(query,url,data)
			elif 'privatestream' in query:
				debug('@@privatestream')
				return _privatestream(query,data)
				
			#elif 'bfst.to' in url:
			#	query=url
			#	return _bfstto(query,data,url)	
				
			else:
				if 'http' in query and 'm3u' in query:
					return 'http'+query.split('http')[-1]
	except:
		pass
	if 'player.cloud.wowza.com' in data:
		return _playercloudwowza(data,url)
	elif 'youtube' in url:
		return _youtube(url)	
	return None
	
	
def _streamcdnto(query,data,url):
	video_url=''

	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	packed = packer.findall(contentVideo)[0]
	unpacked = jsunpack.unpack(packed)

	try:
		video_url = clappr.findall(unpacked)[0]
	except:
		video_url = source.findall(unpacked)[0]
	if video_url:
		video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)	
		
	return video_url
	
	
def _pcastpw(query,data,url):

	id = re.findall('>id="([^"]+)"; width="',data)[0]
	url = 'http://pcast.pw/embed/%s.php?width=700&height=480&stretching=uniform'%id
	headers = {'User-Agent': UA,'Referer': url}	

	contentVideo=getUrl(url,header=headers)	

	html=contentVideo.replace("\'",'"')
	vido_url=decode(url,html)
	return vido_url 

def _sportlivesite(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')

	vido_url=decode(query,html)
	return vido_url 
	
	
def _livesport4upw(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')

	vido_url=decode(query,html)
	return vido_url 
def _strimstv(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')

	try:
		video_url = clappr.findall(html)[0]
	except:
		video_url = source.findall(html)[0]
	
	return video_url

def _sport7biz(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')
	vid_url = re.findall("""videoLink\s*=\s['"](.+?)['"]""",html)[0]
	vid_url= 'https:'+vid_url if vid_url.startswith('//') else vid_url
	vid_url+= '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)	
	return vid_url
def _olimpappru(query,data,url)	:

	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=requests.get(query,headers=headers,verify=False).text#getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')
	src = re.findall('"file": "(.+?)"',html)[0]
	src = src.replace('\\/','/')
	vid_url= 'https:'+src if src.startswith('//') else src
	vid_url+= '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)	

	return vid_url
#def _crackstreamscom(query,data,url):
#	web_pdb.set_trace()
def _sportsbayorg(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')

	vido_url=decode(query,html)
	return vido_url 
	
def _flowframesonline(query,data,url):
	
	dod = re.findall('(\d+)',query)[-1]
	headers = {'User-Agent': UA,'Referer': url}	
	nturl='http://185.255.96.166:3007/api/channels/'+dod
	response = sess.get(nturl, headers=headers,verify=False,timeout=30).json()
	
	vid_url2=response['data']['sourceUrl']
	
	contentVideo=getUrl(vid_url2,header=headers)	

	
	html=contentVideo.replace("\'",'"')

	try:
		vido_url = clappr.findall(html)[0]
		vid_url+= '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=vid_url2)	
	except:
		vido_url = source.findall(html)[0]
		vid_url+= '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=vid_url2)	
	
	if not vido_url:
		vido_url=decode(vid_url,html)
	return vido_url 

	
def _whd365pro(query,data,url):
	vido_url=''
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')
	
	data_channel=re.findall("""data-channel=['"](.+?)['"]""",html)
	data_channel = data_channel[0] if data_channel else ''
	
	headers = {
		'User-Agent': UA,
		'Accept': '*/*',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Origin': 'https://whd365.pro',
		'Connection': 'keep-alive',
		'Referer': query,
		'TE': 'Trailers',
	}

	host = requests.get('https://api.livesports24.online/gethost', headers=headers).text
	if data_channel and host:
		vido_url= "https://" + host + "/" + data_channel  + ".m3u8"
	return vido_url
	
	
	
	
def _tvsportws(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')
	vido_url = re.findall("""videoLink\s*=\s*['"](.+?)['"]""",html)#[0]
	vido_url = vido_url[0] if vido_url else ''

	return vido_url
	
def _yoursportsstream(query,data,url):
	
	headers = {'User-Agent': UA,'Referer': url}	
	query = 'https:'+query if query.startswith('//') else query
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')

	vido_url=decode(query,html)
	return vido_url 
	
	
def _yrsprts(query,data,url):
	
	query = 'https:'+query if query.startswith('//') else query
	headers = {'User-Agent': UA,'Referer': url}	
	video_url=''
	html=getUrl(query,header=headers)
	html = html.replace("\'",'"')	
	
	try:
		pattern = re.findall('{source:([^:]+)}',html)[0]
		regex = 'var %s\s*=\s*atob\("(.+?)"'%pattern
		b64src = re.findall(regex,html)[0]
		vid = base64.b64decode(b64src)
		
		if not vid.startswith("http"):
			video_url='https://yrsprts.xyz'+vid
		
	except:
		dane = (re.findall('var\s+.+?=\[(\d+.+?)\]',html)[0]).split(',')
		co = re.findall('fromCharCode\(parseInt\(value\).(\d+)\)',html)[0]
		htmlx=''
		for x in dane:
			htmlx+=chr(int(x)-int(co))
		try:
			video_url = re.findall('{source:([^:]+)}',htmlx)[0]
		except:
			video_url = re.findall('source:\s*"([^"]+)"',htmlx)[0]
		if video_url.startswith('//'):
			video_url='http:'+video_url
		try:
			co1,co2 =re.findall('rewrittenUrl\=rewrittenUrl.replace\("(.+?)","(.+?)"\);if',html)[0]
			video_url=video_url.replace(co1,co2)
		except:
			pass
	video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)	
	return video_url
	
	
	
def _wstreamto(query,data,url):
	query = 'https:'+query if query.startswith('//') else query
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')
	packed = packer.findall(contentVideo)[0]
	unpacked = jsunpack.unpack(packed)
	
	try:
		video_url = clappr.findall(unpacked)[0]
	except:
		video_url = source.findall(unpacked)[0]
	video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)		
	return video_url

	#vido_url=decode(query,contentVideo)
	#return vido_url 
	
def _arembedcom(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	

	html=contentVideo.replace("\'",'"')

	vido_url=decode(query,contentVideo)
	return vido_url 

def _h247bay(query,data,url):
	
	data=data.replace("\'",'"')
	
	channel,g = re.findall('channel="([^"]+)",\s*g="([^"]+)"',data)[0] #channel="([^"]+)",\s*g="([^"]+)"
	ifrurl='https://www.247bay.tv/hembedplayer/'+channel+'/'+g+'/700/400'
	
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(ifrurl,header=headers)	
	html=contentVideo.replace("\'",'"')

	adres = re.findall('hlsUrl = "([^"]+)".+?"([^"]+)"',html)[0]
	eaurl = re.findall('url: "([^"]+)" \+ (\d+),',html)[0]
	eaadres = eaurl[0]+eaurl[1]
	headers = {'User-Agent': UA,'Referer': ifrurl}	
	contentVideo=getUrl(eaadres,header=headers)	
	html=contentVideo.replace("\'",'"')

	ea = html.split('=')[1]
	vidurl= '%s%s%s'%(adres[0],ea,adres[1])
	return vidurl + '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=ifrurl)	
	
	
def _soccerlivexyz(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')
	video_url=re.findall('source: "([^"]+)"',html,re.DOTALL)[0]
	video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)		
	return video_url
	
def _soccerliveuk(query,data,url)	:
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')
	vido_url=decode(query,contentVideo)
	return vido_url

	
	
	
def  _hdstreamsclub2(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')
	video_url=base64.b64decode(re.findall("""source:\s+window.atob\(["\'](.+?)["\']""",html)[0])
	video_url+= '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)	
	return video_url


def _hazmostream(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')
	vido_url=decode(query,contentVideo)
	return vido_url

def _hazmostream2(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')

	try:
		video_url = clappr.findall(html)[0]
	except:
		video_url = source.findall(html)[0]
	video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)		
	return video_url
	
def _streamcdnco(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')
	packed = packer.findall(contentVideo)[0]
	unpacked = jsunpack.unpack(packed)

	try:
		video_url = clappr.findall(unpacked)[0]
	except:
		video_url = source.findall(unpacked)[0]
	video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)		
	return video_url
	
def _7streamspro(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	html=contentVideo.replace("\'",'"')

	vidurl=re.findall('var videoLink = "(.+?)"',html,re.DOTALL)[0]
	return vidurl
	
	
	
	
def _strimstveu(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	
	html=contentVideo.replace("\'",'"')

	vidurl=re.findall('sources:.+?src: "(.+?)"',html,re.DOTALL)[0]
	return vidurl
	
	
def _studiojunctionlive(query,data,url):
	query = 'https:'+query if query.startswith('//') else query
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	vido_url=decode(query,contentVideo)	
	return vido_url	
	
def _dailyhealthandcare(query,data,url):

	query = 'https:'+query if query.startswith('//') else query
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)	
	vido_url=decode(query,contentVideo)	
	return vido_url	
	
def _bnksportzis(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)		
	m3ux=re.findall("""source: ["\'](.+?)["\']""",contentVideo,re.DOTALL)[0]
	if not '/' in m3ux:
		
		m3ux='http://bnk.sportz.is/'+m3ux
	return m3ux+'|User-Agent='+UA+'&Referer='+url
	
def _hdstreamsclub(data,url):
	video_url=''

	video_url=base64.b64decode(re.findall("""source:\s+window.atob\(["\'](.+?)["\'].*mimeType""",data)[0])
	video_url+= '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=url)	
	return video_url
	
	
def _sdfgdfxyz(query,data,url):
	urlk=re.findall("""hanturl\s*=\s*["\'](.+?)["\']""",data)[0]

	return urlk+'|User-Agent='+UA+'&Referer='+url
	
def _dubsto(query,data,url):
	urlk='http://www.dubs.to'+re.findall('\.\.(.+?)$',query)[0]

	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(urlk,header=headers)
	video_url=_hdstreamsclub(contentVideo,urlk)
	return video_url
def _exprestreamcom(query,data,url):
	
	urlk='https://exprestream.com'+query
	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(urlk,header=headers)	
	src=re.findall('iframe src="(.+?)"',contentVideo)[0]
	headers = {'User-Agent': UA,'Referer': src}	
	urlk='https://exprestream.com'+src
	contentVideo=getUrl(urlk,header=headers)	

	m3ux=re.findall("""source: ["\'](.+?)["\']""",contentVideo,re.DOTALL)
	return m3ux[0]+'|User-Agent='+UA+'&Referer='+urlk

def _vsdeame(query,data,url):

	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)			
	atob=re.findall("""atob\(['"](.+?)['"]""",contentVideo)#[0]
	if atob:
		unpacked=base64.b64decode(atob[0])
	else:
		return ''
	return unpacked+'|User-Agent='+UA+'&Referer='+query
def _bfstto(query,data,url):

	headers = {'User-Agent': UA,'Referer': url}	
	contentVideo=getUrl(query,header=headers)			
	vido_url=decode(query,contentVideo)	
	return vido_url		
	
def _rippleis(query,data,url):

	cookies2 = {
		'challenge': 'BitMitigate.com',
	}
	
	headers2 = {
		'Host': 'ripple.is',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Upgrade-Insecure-Requests': '1',
		'Cache-Control': 'max-age=0',
	}

	contentVideo=sess.get(query,headers=headers2,cookies=cookies2).text

	nxturl = re.findall('src="([^"]+live.+?)" width',contentVideo)[0]
	
	contentVideo=sess.get(nxturl).text
	html=contentVideo.replace("\'",'"')
	vidurl=re.findall('source:\s+"(.+?.m3u8)"',html,re.DOTALL)[0]	
	vidurl = vidurl+'|User-Agent'+urllib.quote(UA)+'&Referer='+nxturl #if vidurl else ''	
	return vidurl		
	
def _twojetv(query,data,url):
	import uuid
	hash = uuid.uuid4().hex					
	aa='1679497221'
	kuk='__ddgu=%s.%s'%(hash,aa)


	headers = {'User-Agent': UA,'Referer': url,'Cookie':kuk}	
	query=query.replace('&amp;','&')

	contentVideo=getUrl(query,header=headers)	
	contentVideo=contentVideo.replace("\'",'"')

	try:
		vidurl=re.findall('source:\s+"(.+?.m3u8)"',contentVideo,re.DOTALL)[0]	
	except:
		vidurl=re.findall('source src="(.+?.m3u8)"',contentVideo,re.DOTALL)[0]	
	
	vidurl = 'http:'+vidurl if vidurl.startswith('//') else vidurl
	vidurl = vidurl+'|User-Agent'+urllib.quote(UA)+'&Referer='+query if vidurl else ''	
	return vidurl		
	
def _1meclub(data,url):
	src=re.findall('iframe src="(.+?)"',data)[0]
	headers = {'User-Agent': UA,'Referer': url}
	
	contentVideo=getUrl(src,header=headers)	
	vido_url=decode(src,contentVideo)

	return vido_url	
def _sportzonlinepw(query,data,url):
	
	headers = {'User-Agent': UA,'Referer': url}
	html=getUrl(query,header=headers)
	vido_url = decode(query,html)
	return vido_url	

def _sportsstreamnet(query,data,url):
	headers = {'User-Agent': UA,'Referer': url}
	contentVideo=getUrl(query,header=headers)
	vido_url = decode(url,contentVideo)
	return vido_url
	
def _realcampw(query,data,url):
	
	feed=re.compile('zmid = "(.+?)", pid = (.+?); edm = "(.+?)"').findall(data)
	headers = {'User-Agent': UA,'Referer': url,'Content-Type': 'application/x-www-form-urlencoded','Connection': 'keep-alive','Upgrade-Insecure-Requests': '1',}
	url_main='https://%s/sdembed?v=%s'%(feed[0][2],feed[0][0])
	
	params='pid=%s'%feed[0][1]
	contentVideo=getUrl(url_main,header=headers,data=params)
	return
	
def _fstreamme(query,data,url):
	video_url=''	
	data=data.replace("\'",'"')
	feed = re.compile('width=(.*?), height=(.*?), channel="(.*?)", g="(.*?)";').findall(data)
	if feed:		
		header = {'User-Agent':UA,'Referer': url}
		url_main='https://www.playerfs.com//hembedplayer/%s/%s/%s/%s'%(feed[0][2],feed[0][3],feed[0][0],feed[0][1])				
		contentVideo = getUrl(url_main,header=header)	
		main_url=re.findall("""['"]src['"].+?['"](.+?)['"].+?['"](.+?)['"]""",contentVideo)[0]
		id=re.findall('url:.+?".+?lquest.+?".+?(\d+).+?&',contentVideo)[0]		
		idurl="https://www.lquest123b.top/loadbalancer?%s"%str(id) + "&"
		header = {'User-Agent':UA,'Referer': url_main}
		contentVideo = getUrl(idurl,header=header)
		ea = contentVideo.split('=')[1]
		video_url=main_url[0]+ea+main_url[1]
		return video_url	

def _livesport4ucom(query,data,url):
	video_url=''
	header = {'User-Agent':UA,'Referer': url}	
	content = getUrl(query,header=header)
	feed = re.compile('id=["\'](.*?)["\']; width=["\'](.*?)["\']; height=["\'](.*?)["\'];').findall(content)
	if feed:
		url_main='http://hdcast.pw/stream_jw2.php?id=%s&width=%s&height=%s&stretching=uniform'%(feed[0][0],feed[0][1],feed[0][2])		
		header = {'User-Agent':UA,'Referer': url}			
		contentVideo = getUrl(url_main,header=header)		
		video_url=re.findall('curl.+?"(.+?)"',contentVideo)[0] #
		video_url=base64.b64decode(re.findall('curl.+?"(.+?)"',contentVideo)[0])
		video_url=video_url+'|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=url_main)	
	return video_url	

def _nowlivepro	(query,data,url):
	video_url=''
	header = {'User-Agent':UA,'Referer': url}		
	content = getUrl(query,header=header)	
	unescs=re.findall('unescape\("(.+?)"',content)
	for unesc in unescs:
		link = urllib.unquote(unesc)
		video_url=re.findall('"application/x-mpegurl", src: "(.+?)"',link)
		if video_url:
			video_url = 'http:'+video_url[0] if video_url[0].startswith('//') else video_url[0]	
			break	
	return video_url	
		
def _streamupme	(query,data,url):
	video_url=''
	content = getUrl(query,header=header)

	data=data.replace("\'",'"')
	feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
	if feed:
		url_main='http://www.webtv.ws/embed.php?live=%s&vw=%s&vh=%s'%(feed[0][0],feed[0][1],feed[0][2])		
		header = {'User-Agent':UA,'Referer': url}			
		contentVideo = getUrl(url_main,header=header)		
		video_url=re.findall('source\s+src="(.+?)"\s+type',contentVideo)[0] #
		video_url=video_url+'|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=url_main)	
		return video_url	
def _webtv(query,data,url):
	video_url=''
	data=data.replace("\'",'"')
	feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
	if feed:
		url_main='http://www.webtv.ws/embed.php?live=%s&vw=%s&vh=%s'%(feed[0][0],feed[0][1],feed[0][2])		
		header = {'User-Agent':UA,'Referer': url}			
		contentVideo = getUrl(url_main,header=header)		
		video_url=re.findall('source\s+src="(.+?)"\s+type',contentVideo)[0] #
		video_url=video_url+'|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=url_main)	
		return video_url	

def _youtube(url):
	video_url=re.findall("(.+?)\?",url)[0]	
	vid=urlparse.urlparse(video_url).path.split('/')[-1]
	video_url = 'plugin://plugin.video.youtube/play/?video_id=' + vid	
	return video_url
	


def _bonstreams(data,url):
	video_url=''	
	data=data.replace("\'",'"')
	id=re.findall(""">id="(.+?)"; width=""",data)[0]
	vidurl='https://telerium.tv/embed/%s.html'%id
	header = {'User-Agent':UA,'Referer': url}	
	
	contentVideo = getUrl(vidurl,header=header)	
	video_url=_telerium(contentVideo,contentVideo,vidurl)	
	return video_url	


	

def _hdcastme(query,data,url):
	
	video_url=''	
	feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
	if feed:
		url_main='https://www.hdcast.me/embed.php?player=desktop&live=%s&vw=%s&vh=%s'%(feed[0][0],feed[0][1],feed[0][2])		
		header = {'User-Agent':UA,'Referer': url}	
		contentVideo = getUrl(url_main,header=header)	
		video_url=re.findall("""source:\s+["\'](.+?)['"].*mimeType""",contentVideo)[0]
		video_url='https:'+video_url+'|verifypeer=false&User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=url)
		return video_url

	
def _ucasterplayer(query,data,url):
	video_url=''	
	feed = re.compile('width=(.*?), height=(.*?), channel=["\'](.*?)["\'], g=["\'](.*?)["\'];').findall(data)
	if feed:		
		header = {'User-Agent':UA,'Referer': url}
		url_main='https://www.ucasterplayer.com/hembedplayer/%s/%s/%s/%s'%(feed[0][2],feed[0][3],feed[0][0],feed[0][1])				
		contentVideo = getUrl(url_main,header=header)	
		main_url=re.findall("""['"]src['"].+?['"](.+?)['"].+?['"](.+?)['"]""",contentVideo)[0]
		id=re.findall('url:.+?".+?lquest.+?".+?(\d+).+?&',contentVideo)[0]		
		idurl="https://www.lquest123b.top/loadbalancer?%s"%str(id) + "&"
		header = {'User-Agent':UA,'Referer': url_main}
		contentVideo = getUrl(idurl,header=header)
		ea = contentVideo.split('=')[1]
		video_url=main_url[0]+ea+main_url[1]
		return video_url
		
def _whostreams(query,data,url):
	if '\r' in url:
		url=url.replace('\r','')	
	
	ref_url = 'http:'+query if query.startswith('//') else query
	header = {'User-Agent':UA,'Referer': url}	
	contentVideo = getUrl(ref_url,header=header)
	packed = packer.findall(contentVideo)[0]
	unpacked = jsunpack.unpack(packed)
	try:
		video_url = clappr.findall(unpacked)[0]
	except:
		video_url = source.findall(unpacked)[0]
	video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=ref_url)		
	return video_url
	
def rev(a_string):
    return a_string[::-1]

def getRequestAdv (url, headers, isReplace=True):
    UTF8 = 'utf-8'
    request = urllib2.Request(url.encode(UTF8), None, headers)

    try:
        response = urllib2.urlopen(request)
        
        if response.info().getheader('Content-Encoding') == 'gzip':
            print ("Content Encoding == gzip")

            buf = StringIO( response.read() )
            f = gzip.GzipFile(fileobj=buf)
            link1 = f.read()
        else:
            link1=response.read()
    except:
        link1 = ""
        
    if (isReplace):
        link1 = str(link1).replace('\n','')

    return(link1)	
def getRequest (url, referUrl, userAgent, xRequestedWith=""):
    UTF8 = 'utf-8'
    headers = {'User-Agent':userAgent, 'Referer':referUrl, 'X-Requested-With': xRequestedWith, 'Accept':"text/html", 'Accept-Encoding':'gzip,deflate,sdch', 'Accept-Language':'en-US,en;q=0.8'} 
    request = urllib2.Request(url.encode(UTF8), None, headers)

    try:
        response = urllib2.urlopen(request)
        
        if response.info().getheader('Content-Encoding') == 'gzip':
            print ("Content Encoding == gzip")

            buf = StringIO( response.read() )
            f = gzip.GzipFile(fileobj=buf)
            link1 = f.read()
        else:
            link1=response.read()
    except:
        link1 = ""
    
    link1 = str(link1).replace('\n','')
    return(link1)	
	
def _telerium(query,data,url):
	
	data = requests.get(query, headers={'User-Agent':UACHR, 'Referer':url},verify=False).content

	packer2 = re.compile('(eval\(function\(p,a,c,k,e,(?:r|d).*)')
	
	if query:
		try:
			packed = packer2.findall(data)[0]
		except:
			return ''
	
	unpacked = jsunpack.unpack(packed)	
	ab=unpacked
	pliki = (re.findall('doThePIayer\((.+?)\)',unpacked)[0]).split(',') 
	patern3	='var '+pliki[1]+'=window.atob\((.+?)\)'
	src6=re.compile(patern3).findall(unpacked)	
	patern6=src6[0]+'="(.*?)"'	
	
	src7=re.compile(patern6).findall(unpacked)	 #poprawny poczatek adresu
	d=src7[0]
	d1=base64.b64decode(d)	
	varNames = re.compile('url:window.atob\((.*?)\)\.slice\((\d+)\)\+window.atob\((.*?)\)')
	vars = varNames.findall(unpacked)[0]
	
	part1Reversed = re.compile('{0}\s*=\s*[\'\"](.+?)[\'\"];'.format(vars[0])).findall(unpacked)[0]
	part2Reversed = re.compile('{0}\s*=\s*[\'\"](.+?)[\'\"];'.format(vars[2])).findall(unpacked)[0]	
	part1 = (base64.b64decode(part1Reversed))[int(vars[1]):]
	part2 = base64.b64decode(part2Reversed) 	
	obliczenia = re.findall('navigator.cookieEnabled\)\{(.+?);\$\.ajax',unpacked)[0]
	sppech = re.findall('var speechless=(.+?)([-+])(.+?)$',obliczenia)[0]
	reg1 = 'var '+sppech[0]+'=(.+?)([-+])(.+?);'
	reg2 = 'var '+sppech[2]+'=(.+?)([-+])(.+?);'
	ob1 =re.compile(reg1).findall(obliczenia)
	ob2 =re.compile(reg2).findall(obliczenia)
	ob11 = re.compile('var '+ob1[0][0]+'=(.+?);').findall(obliczenia)
	ob12 = re.compile('var '+ob1[0][2]+'=(.+?);').findall(obliczenia)
	
	ob21 = re.compile('var '+ob2[0][0]+'=(.+?);').findall(obliczenia)
	ob22 = re.compile('var '+ob2[0][2]+'=(.+?);').findall(obliczenia)
	
	
	obliczob1 = eval('%s%s%s'%(ob11[0],ob1[0][1],ob12[0]))
	obliczob2 = eval('%s%s%s'%(ob21[0],ob2[0][1],ob22[0]))
	spech = eval('%s%s%s'%(obliczob1,sppech[1],obliczob2))
	
	
	realtoken = getRealToken('https://telerium.tv'+part1+part2, query,spech)

	path = 'https:'+d1+realtoken
	
	path+='|User-Agent='+UACHR+'&Referer='+urllib.quote(query, safe='')+'&Sec-Fetch-Mode=cors&Origin=https://telerium.tv'

	return path	
	
def getRealToken(link, referer,spech):
	cookies = {
		'ChorreameLaJa': '100',
		'setVolumeSize': '100',
		'NoldoTres': '100',
	}
	
	headers = {
		'Host': 'telerium.tv',
		'User-Agent': UACHR,
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': referer,
	}
	h = {
		'User-Agent': UACHR,
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'Referer': referer,
		'X-Requested-With': 'XMLHttpRequest',
		'Connection': 'keep-alive',}	

	realResp = requests.get(link, headers=headers,cookies=cookies,verify=False).content#[1:-1]

	realResp=re.findall('"(.+?)"',realResp)[spech]	

	return realResp[::-1]	


def _assiatv(query,data,url):
	video_url=''
	header = {'User-Agent':UA,'Referer': url}
	content = getUrl(query,header=header)	
	content=content.replace("\'",'"')
	video_url=re.findall('file:"([^"]+)"',content)#[0]
	#
	if video_url:
		video_url=video_url[0]+'|User-Agent='+UA+'&Referer='+query	
	else:
		try:
			
			content=content.replace("\'",'"')
			video_url=re.findall('<source src="([^"]+)" type="application',content)[0]
			video_url=video_url+'|User-Agent='+UA+'&Referer='+query	
		except:
			try:
				video_url = clappr.findall(content)[0]
			except:
				video_url = source.findall(content)[0]
			if video_url:
				video_url += '|User-Agent={ua}&Referer={ref}'.format(ua=UA, ref=query)	
	return video_url

def _wlivetv(query,data,url):
	video_url=''
	feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
	if feed:
		
		header = {'User-Agent':UA,'Referer': url}
		if data.find('wlive.tv/embedra.js')>0:
			url_main='http://www.wlive.tv/embedra.php?player=desktop&live=%s&vw=660&vh=420'%feed[0][0]			
		else:
			url_main='http://www.wlive.tv/embedhd.php?player=desktop&live=%s&vw=660&vh=420'%feed[0][0]
		contentVideo = getUrl(url_main,header=header)
		pi = re.findall('return\\((.*?)\\);',contentVideo)
		pi=pi[0]
		if pi:		
			join = re.findall('(\\[.*?\\]).join',pi)
			el_id = re.findall('(\\w+).join',pi)
			aa = re.findall('document.getElementById\\("(.*?)"',pi)
			if join:
				join = ''.join(eval(join[0])).replace('\\','')
			if el_id:
				tmp = re.findall('var %s\\s*=\\s*(\\[.*?\\])'%el_id[0],contentVideo)
				el_id = ''.join(eval(tmp[0])) if tmp else ''
			if aa:
				aa = re.findall('%s\\s*>(.*?)<'%aa[0],contentVideo)
				aa = aa[0] if aa else ''
				video_url = join + el_id + aa +'|User-Agent='+UA+'&Referer='+url
		return video_url
def _tumarcadorxyz(query,data,url):
	import requests
	str_url=''
	header = {'User-Agent':UA,'Referer': url}	
	content = requests.get(query,headers=header,verify=False).content
	str_url=re.findall("""file:\s+['"](.+?)['"]""",content,re.DOTALL)
	if str_url:
		str_url=str_url[0]
	return str_url	
def _embedpot_iptv(query,data,url):
    video_url=''
    feed = re.compile('cid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
    if feed:
        url_main='http://embed.pot-iptv.pl/playerr/%s?vw=600&vh=450'%feed[0][0]
        header = {'User-Agent':UA,
                'Referer': url}
        contentVideo = getUrl(url_main,header=header)
        src = re.findall('{ src\\s*:\\s*[\'"](http.*?)[\'"]',contentVideo)
        if src:
            header['Referer']=url_main
            req = urllib2.Request(src[0],data=None,headers=header)
            try:
                response = urllib2.urlopen(req, timeout=10)
                link = response.geturl()
                response.close()
            except:
                link=''
            if link:
                video_url = link+'|User-Agent='+UA+'&Referer='+url_main
    return video_url
def _vvcast(query,data,url):
    video_url=''
    feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
    if feed:
        url_main='http://www.vvcast.tv/embedhd.php?live=%s&vw=%s&vh=%s'%feed[0]
        header = {'User-Agent':UA,
                'Referer': url}
        contentVideo = getUrl(url_main,header=header)
        szuk = re.findall('return\\((.*?)\\);',contentVideo)
        if szuk:
            szuk = szuk[0]
            join = re.findall('(\\[.*?\\]).join',szuk)
            el_id = re.findall('(\\w+).join',szuk)
            aa = re.findall('document.getElementById\\("(.*?)"',szuk)
            if join:
                join = ''.join(eval(join[0])).replace('\\','')
            if el_id:
                tmp = re.findall('var %s\\s*=\\s*(\\[.*?\\])'%el_id[0],contentVideo)
                el_id = ''.join(eval(tmp[0])) if tmp else ''
            if aa:
                aa = re.findall('%s\\s*>(.*?)<'%aa[0],contentVideo)
                aa = aa[0] if aa else ''
            if join and el_id and aa:
                video_url = join + el_id + aa +'|User-Agent='+UA+'&Referer='+url_main
    return video_url
def _playercloudwowza(data,url):
    video_url=''
    href=re.findall('video_id=(http.+m3u[8])',data)
    if href:
        video_url=href[0]+'|Referer=%s&User-Agent=%s'%(url,UA)+'X-Requested-With=ShockwaveFlash/28.0.0.126'
    return video_url
def _tvpPlayer(query,data,url):
    data=getUrl(query)
    src_vid = re.compile('0:{src:["\'](.*?)[\'"]', re.DOTALL).findall(data)
    if src_vid: video_url = src_vid[0]
    else: video_url=''
    return video_url
def _byetv(query,data,url):
    contentbye= getUrl(query)
    ref_url = re.findall('url\\s*=\\s*["\'](http.+?)["\']',contentbye)
    if ref_url:
        contentVideo= getUrl(ref_url[0])
        try:
            hlsUrl=re.findall('var hlsURL\\s*=\\s*(.*?);',contentVideo)
            name=re.findall('var\\s+name\\s*=\\s*["\'](.+?)["\']\\s*;',contentVideo)[0]
            ipserver=re.findall('var\\s+edgeserverip\\s*=\\s*["\'](.+?)["\']\\s*;',contentVideo)[0]
            appname=re.findall('var\\s+appName\\s*=\\s*["\'](.+?)["\']\\s*;',contentVideo)[0]
            width=re.findall('var\\s+width\\s*=\\s*["\'](.+?)["\']\\s*;',contentVideo)[0]
            height=re.findall('var\\s+height\\s*=\\s*["\'](.+?)["\']\\s*;',contentVideo)[0]
            video_url = eval(hlsUrl[0]) +'|User-Agent='+UA+'&Referer='+ref_url[0]
        except:
            video_url=''
    return video_url
def _veecast(query,data,url):
    video_url=''
    header = {'User-Agent':UA,
            'Referer': url}
    contentVideo = getUrl(query,header=header)
    if contentVideo:
        f1   = re.compile('source\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
        f2   = re.compile('file\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
        src_vid   = re.compile('<source src=["\'](.*?)[\'"]').findall(contentVideo)
        if   f1:  video_url = f1[0]
        elif f2:  video_url = f2[0]
        elif src_vid:  video_url = src_vid[0]
        if video_url:
            video_url += '|User-Agent='+UA+'&Referer='+url
    return video_url
def _srkcast(query,data,url):
    video_url=''
    feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
    if feed:
        url_main='http://www.srkcast.com/embed.php?sid=default&live=%s&vw=%s&vh=%s'%feed[0]
        header = {'User-Agent':UA,
                'Referer': url}
        contentVideo = getUrl(url_main,header=header)
        if contentVideo:
            f1   = re.compile('source\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
            f2   = re.compile('file\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
            src_vid   = re.compile('<source src=["\'](.*?)[\'"]').findall(contentVideo)
            if   f1:  video_url = f1[0]
            elif f2:  video_url = f2[0]
            elif src_vid:  video_url = src_vid[0]
            if video_url:
                video_url += '|User-Agent='+UA+'&Referer='+url_main
    return video_url
def _sharecast(query,data,url):
    video_url=''
    header={'Referer':url,'User-Agent':UA}
    contentVideo = getUrl(query,header=header)
    if contentVideo:
        f1   = re.compile('source\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
        f2   = re.compile('file\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
        src_vid   = re.compile('<source src=["\'](.*?)[\'"]').findall(contentVideo)
        if   f1:  video_url = f1[0]
        elif f2:  video_url = f2[0]
        elif src_vid:  video_url = src_vid[0]
        if video_url:
            video_url += '|User-Agent='+UA+'&Referer='+query
    return video_url
def _limacity(query,data,url):
    video_url=''
    contentVideo = getUrl(query)
    if contentVideo:
        file   = re.compile('source\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
        if file:
            video_url = file[-1]
        file   = re.compile('file\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
        if file:
            video_url = file[-1]
        file   = re.compile('<source src=["\'](.*?)[\'"]').findall(contentVideo)
        if file:
            video_url = file[-1]
        if video_url:
            hlsNumb=re.findall('hls(\\d+)',video_url)
            if hlsNumb:
               video_url = video_url.replace('masterlist.m3u8','%sp/list.m3u8'%hlsNumb[0])
            else:
               video_url = video_url.replace('masterlist.m3u8','720p/list.m3u8')
            video_url += '|User-Agent='+UA+'&Referer='+query
    return video_url
def _ustream(query,data,url):
    video_url=''
    return video_url
def _ustreamix(query,data,url):
    video_url=''
    if 'cr.php' in query:
        content = getUrl(query)
        href = re.compile('<a href="(.*?)" target="_blank">').findall(content)
        if href:
            stream_url='stream='+href[0].split('id=')[-1]
    else:
        if 'id=' in url:
            stream_url='stream='+url.split('id=')[-1]
        else:
            stream_url='stream='+query.split('id=')[-1]
    content = getUrl(query,header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0 Iceweasel/44.0', 'Accept': '*/*'})
    firstIp = re.findall("x_first_ip.+?'(.*?)'", content)
    if not firstIp:
        query = 'https://ustreamix.com/'+stream_url.replace('=','.php?id=')
        content = getUrl(query,header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0 Iceweasel/44.0', 'Accept': '*/*'})
        firstIp = re.findall("x_first_ip.+?'(.*?)'", content)
    firstIp = firstIp[0]
    ustreamyxBase = ['http://ustreamyx.com/']
    varjdtk=''
    hosttmg=''
    for item in ustreamyxBase:
        url_main_str = item + 'stats.php?p=' + firstIp
        source = getUrl(url_main_str, header = {'Referer': query, 'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0 Iceweasel/44.0', 'Accept': '*/*'})
        varjdtk = re.findall('var jdtk="(.*?)"', source)
        hosttmg = re.findall('host_tmg="(.*?)"', source)
        if varjdtk: varjdtk=varjdtk[0]
        if hosttmg: hosttmg =hosttmg[0]
    if varjdtk:
        stream_host = hosttmg if hosttmg else item
        video_url= 'http://%s/tmg.m3u8?stream=%s&token=%s'%(stream_host,stream_url.replace('.php?id',''), varjdtk) +'|User-Agent=Mozilla/5.0 (X11; Linux i686; rv:44.0) Gecko/20100101 Firefox/44.0 Iceweasel/44.0&Referer='+url
    return video_url
def _dailymotion(query,data,url):
    video_id=query.split('?')[0].split('/')[-1]
    content = getUrl('http://www.dailymotion.com/embed/video/%s' % video_id)
    srcs=re.compile('"(auto)":\\[{"type":"(.*?)","url":"(.*?)"}\\]',re.DOTALL).findall(content)
    for quality,type,url in srcs:
        url = url.replace('\\','')
        contentDM = getUrl(url + '&redirect=0')
        extm3u='I0VYVE0zVQ=='.decode('base64')
        if not contentDM:
            contentDM = getUrl(url + '&redirect=0')
        if extm3u in contentDM:
            names=re.compile('NAME="(.*?)"\n(.*?)\n').findall(contentDM)
            for label,url in names:
                video_url=url
        else:
            if contentDM and not contentDM.startswith('http:'):
                contentDM = re.findall('(http://.*?)$', contentDM)[0]
            live_url = contentDM.split('live.isml')[0]+'live.isml/'
            contentDM2 = getUrl(url)
            if extm3u in contentDM2:
                names=re.compile('RESOLUTION=(.*?)\n(.*?)\n').findall(contentDM2)
                for label,added in names:
                    video_url=live_url+added
    return video_url
def _jazztv(query,data,url):
    video_url=''
    feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
    if feed:
        url_main='http://www.jazztv.co/embedo.php?live=%s&vw=%s&vh=%s'%feed[0]
        header = {'User-Agent':UA,
                'Referer': url,
                'Host':'www.jazztv.co',
                }
        contentVideo = getUrl(url_main,header=header)
        file   = re.compile('file[: ]*(.*?)}',re.DOTALL).findall(contentVideo)
        for f in file:
            video_url = f.strip().split('"')[1]
            if video_url.startswith('rtmp'):
                video_url += ' swfVfy=1 live=1 timeout=13  swfUrl=http://ssl.p.jwpcdn.com/player/v/7.9.3/jwplayer.flash.swf pageUrl='+url_main
                break
    return video_url
def _urhdtv(query,data,url):
    video_url=''
    data = getUrl(query)
    file = re.compile('file:\\s*[\'"](.*?)[\'"]').findall(data)
    if file:
        video_url = file[0]
    return video_url
def _jardello(query,data,url):
    video_url=''
    data = getUrl(query)
    file = re.compile('file:\\s*[\'"](.*?)[\'"]').findall(data)
    if file:
        video_url = file[0]
    return video_url
def _cricfree(query,data,url):
    data = getUrl(query)
    video_url=''
    feed = re.compile('id=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(data)
    if feed:
        url_main='http://soccerschedule.online/livegamecrnope.php?id=%s&width=%s&height=%s&stretching='%feed[0]
        header = {'User-Agent':UA,
                 'Referer': query,}
        contentDec = getUrl(url_main,header=header)
        idcric=re.compile('id=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(contentDec)
        if idcric:
            url_cric='http://playlive.pw/streamt.php?id=%s&width=%s&height=%s'%idcric[0]
            header = {'User-Agent':UA,'Referer': url_main,}
            contentCric = getUrl(url_cric,header=header)
            file = re.compile('source:\\s*[\'"](.*?)[\'"]').findall(contentCric)
            if file:
                video_url = file[0]
    return video_url
def _staticnowliveclub(query,data,url):
    video_url=''
    feed = re.compile('id=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(data)
    if feed:
        url_main='http://nowlive.club/stream.php?id=%s&width=%s&height=%s&stretching=uniform&p=1'%feed[0]
        header = {'User-Agent':UA,
                 'Referer': url,}
        contentVideo = getUrl(url_main,header=header)
        stream = re.compile('curl = "(.*?)"').findall(contentVideo)
        h = '|Cookie=%s' % urllib.quote('PHPSESSID=1')
        header={'User-Agent':UA,'Referer': url_main,'Host':'nowlive.club',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':'c_ref_3504694=%s'%urllib.quote_plus(url)}
        url_swf='http://nowlive.club/jwplayer.flash.swf'
        contentSTCL = getUrl('http://nowlive.club/getToken.php',header=header)
        token = re.compile('"token":"(.*?)"').findall(contentSTCL)
        if token and stream:
            video_url = base64.b64decode(stream[0]) + token[0] +'|Referer=%s&User-Agent=%s&X-Requested-With=ShockwaveFlash/23.0.0.185'%(url_swf,UA)
    return video_url
def _abcastnet(query,data,url):
    video_url =''
    feed = re.compile('file=["\'](.*?)["\']; width=(.*?); height=(.*?);').findall(data)
    if feed:
        url_main='http://abcast.net/embed.php?file=%s&width=640&height=430'%feed[0][0]
        contentDec = getUrl(url_main)
        param_val = re.compile('<param value="(.*?)"\\s*name="flashvars">').findall(contentDec)
        link = re.compile('player.src\\((.*?)\\)',re.DOTALL).findall(contentDec)
        if param_val:
            url_swf='http://abcast.net/ob.swf'
            streamer=re.compile('streamer=(.*?)&').findall(param_val[0])
            file=re.compile('file=(.*?)&').findall(param_val[0])
            if streamer and file:
                video_url =streamer[0]+ ' playpath='+file[0].split('.')[0] +' swfUrl='+url_swf + ' swfVfy=1 live=1 timeout=13 pageUrl='+url_main
                video_url =streamer[0].replace('redirect','live') + ' playpath='+file[0].split('.')[0] +' swfUrl='+url_swf + ' pageUrl='+url_main
        elif link:
            url_abcast=re.compile('["\'](http.*?)["\']').findall(link[0])
            video_url = url_abcast[0] if url_abcast else ''
        else:
            source = re.compile('(?:src|source)(?:\\:|=)\\s*[\'"](http.+m3u.*?)[\'"]').findall(contentDec)
            if source:
                video_url = source[0]
    else:
        contentDec = getUrl(query)
        source = re.compile('(?:src|source)(?:\\:|=)\\s*[\'"](http.+m3u.*?)[\'"]').findall(contentDec)
        if source:
            video_url = source[0]
    return video_url
def _freelive365(query,data,url):
    video_url =''
    contentVideo = getUrl(query)
    hlsUrl=re.search('var hlsURL\\s*=\\s*(.*?);',contentVideo)
    if hlsUrl:
       hlsUrl = hlsUrl.group(1)
    else:
        url_main=re.compile('url\\s*=\\s*["\'](http://freelive365.com/.*?)["\']').findall(contentVideo)
        if url_main:
            contentVideo = getUrl(url_main[0])
            hlsUrl=re.search('var hlsURL\\s*=\\s*(.*?);',contentVideo)
            hlsUrl = hlsUrl.group(1) if hlsUrl else ''
    if hlsUrl:
        xxx=re.compile('\\+(\\w+)\\+').findall(hlsUrl)
        l111l1lll1l11l111_tv_={}
        for w in xxx:
            vars=re.compile('var %s\\s*=\\s*(.*?);'%w).search(contentVideo)
            if vars: hlsUrl = hlsUrl.replace('%s'%w,vars.group(1))
        try:
            video_url =eval(hlsUrl)
        except:pass
    return video_url
def _cast4utv(query,data,url):
    video_url =''
    feed = re.compile('fid=["\'](.*?)["\']; v_width=(.*?); v_height=(.*?);').findall(data)
    if feed:
        url_main='http://www.cast4u.tv/embed.php?v=%s&vw=%s&vh=%s'%feed[0]
        header = {'User-Agent':UA,
                'Referer': url,
                'Host':'www.cast4u.tv',
                }
        contentVideo = getUrl(url_main,header=header)
        file   = re.compile('file[: ]*(.*?)}').findall(contentVideo)
        token = re.compile('securetoken: (\\w+)').findall(contentVideo)
        file = file[0].strip() if file else ''
        if file and token:
            xxx = re.compile('(\\w+)\\(\\)').findall(file)
            f = xxx[0]
            fd = re.compile('function\\s+%s\\(\\)\\s*{(.*?)}'%f,re.DOTALL).findall(contentVideo)
            if fd:
                stream = re.compile('(\\[[^\\]]*\\])').findall(fd[0])
                stream = ''.join(eval(stream[0]))
                join = re.compile(' (\\w+).join\\(""\\)').findall(fd[0])
                if join:
                    dd = re.compile('%s = (\\[[^\\]]*\\])'%join[0]).findall(contentVideo)
                    join = ''.join(eval(dd[0]))
                el_id = re.compile('getElementById\\("(.*?)"\\)').findall(fd[0])
                if el_id:
                    id_get = re.compile('id=%s>(.*?)<'%el_id[0]).findall(contentVideo)
                    el_id =id_get[0]
            fd = re.compile('function\\s+%s\\(\\)\\s*{(.*?)}'%xxx[1],re.DOTALL).findall(contentVideo)
            if fd:
                aa = re.compile('(\\[[^\\]]*\\])').findall(fd[0])
                aa = ''.join(eval(aa[0]))
            url_cast4u = stream+join+el_id+'/'+aa
            token='JVhCMDAobktIQCMu'
            video_url = url_cast4u.replace('\\','') +' swfUrl=http://cast4u.tv/jwplayer/jwplayer.flash.swf token='+token.decode('base64')+' live=1 timeout=15 pageUrl=' + query
    return video_url
def _osgchmura(query,data,url):
    video_url=''
    header = {'User-Agent':UA,
             'Referer': url,}
    contentVideo = getUrl(query,header=header)
    source = re.compile('src=["\'](http.*?)["\']').findall(contentVideo)
    for src in source:
        if src.endswith('m3u8'):
            video_url = src
            break
    return video_url
def _staticu_profr(query,data,url):
    video_url=''
    source = re.compile('src=["\'](http.*?)["\']').findall(data)
    if source:
        source = re.compile('source=(rtmp.*?[^&]*)').findall(source[0])
        if source:
            video_url = source[0]
    return video_url
def _widestream(query,data,url):
    video_url=''
    header = {'User-Agent':UA,
             'Referer': url,}
    contentVideo = getUrl(query,header=header)
    file = re.compile('file\\s*:\\s*["\'](.*?)["\']').search(contentVideo)
    if file:
        video_url=file.group(1)
    return video_url
def _staticnowlive(query,data,url):
    video_url=''
    feed = re.compile('id=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(data)
    if feed:
        url_main='http://nowlive.pw/stream.php?id=%s&width=%s&height=%s&stretching=uniform&p=1'%feed[0]
        header = {'User-Agent':UA,
                 'Referer': url,}
        contentVideo = getUrl(url_main,header=header)
        stream = re.compile('curl = "(.*?)"').findall(contentVideo)
        h = '|Cookie=%s' % urllib.quote('PHPSESSID=1')
        header={'User-Agent':UA,'Referer': url_main,'Host':'nowlive.pw',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':'c_ref_3504694=%s'%urllib.quote_plus(url)}
        url_swf='http://nowlive.pw/jwplayer.flash.swf'
        contentSTCL = getUrl('http://nowlive.pw/getToken.php',header=header)
        token = re.compile('"token":"(.*?)"').findall(contentSTCL)
        if token and stream:
            video_url = base64.b64decode(stream[0]) + token[0] +'|Referer=%s&User-Agent=%s&X-Requested-With=ShockwaveFlash/23.0.0.185'%(url_swf,UA)
    return video_url
def _deltalivepro(query,data,url):
    video_url=''
    file = re.compile("url: '(.*?)'").search(data)
    netCon = re.compile("netConnectionUrl: '(.*?)'").search(data)
    url_swf = re.search('"player", "(.*?.swf)"',data)
    if file and netCon and url_swf:
        video_url = netCon.group(1) + ' playpath='+file.group(1).strip() +' swfUrl='+url_swf.group(1) + ' swfVfy=1 live=1 timeout=13  pageUrl='+url
    return video_url
def _openliveorg(query,data,url):
    video_url=''
    feed = re.compile('file=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(data)
    if feed:
        url_main='http://openlive.org/embed.php?file=%s&width=%s&height=%s'%feed[0]
        header = {'User-Agent':UA,
                    'Referer': url,}
        contentVideo = getUrl(url_main,header=header)
        url_swf = ['http://p.jwpcdn.com/6/12/jwplayer.flash.swf']
        stream = re.compile("'streamer'[:, ]+'(.*?)'").findall(contentVideo)
        file   = re.compile("'file'[:, ]+'(.*?)'").findall(contentVideo)
        if url_swf and stream and file:
            urlbase_openlive=urlparse.urlparse(stream[0])
            request = urllib2.Request('http://'+urlbase_openlive.netloc+urlbase_openlive.path, None, header)
            data =  urllib2.urlopen(request)
            aa,port=data.fp._sock.fp._sock.getpeername()
            netCon = 'rtmp://94.176.148.234/live?'+urlbase_openlive.query
            video_url = netCon +' playpath='+file[0] + ' swfUrl='+url_swf[0] + ' swfVfy=1 live=1  timeout=10 pageUrl='+url_main
    return video_url
#def _sawlivetv(query,data,url):
#	video_url=''
#	source = getUrl(query)
#	unpacked = ''
#	packed = source.split('\n')
#	for i in packed:
#		try:
#			if 'unescape' in i:
#				a=i
#			if 'rtmp://' in i:
#				rtm=i
#			unpacked += jsunpack.unpack(i)
#		except:
#			pass
#	try:
#		contentVideo = jsunpack.unpack(source.decode('string_escape'))
#	except:
#		contentVideo =''
#	src=re.compile('src=["\'](http:.*?)["\']').findall(contentVideo)
#	if src:
#		header = {'Referer':  src[0], 'User-Agent': UA}
#		contentVideo = getUrl(src[0].replace('/view/','/watch/'),header=header)
#		url_swf = re.compile("SWFObject\\('(.*?)'").findall(contentVideo)
#		match = re.compile('(eval\\(function\\(p,a,c,k,e,d\\).*?)\n').findall(contentVideo)
#		if match:
#			contentVideo = jsunpack.unpack(match[0].decode('string_escape'))
#			dec_saw = lambda x: x.group(0).replace('%','').decode('hex')
#			contentVideo = re.sub('%.{2}',dec_saw,contentVideo)
#			code = contentVideo.replace("so.addVariable('file',",'file=')
#			code = code.replace("so.addVariable('streamer',",'streamer=')
#			code = code.replace('));',');')
#			code = code.replace('unescape','')
#			context = js2py.EvalJs()
#			context.execute(code)
#			streamer= getattr(context,'streamer')
#			file= getattr(context,'file')
#			if url_swf and streamer and file:
#				video_url = streamer +' playpath='+file + ' swfUrl='+url_swf[0] + ' swfVfy=1 live=1 timeout=13   pageUrl='+src[0]
#	return video_url
#
#def _sawlivetv2(query,data,url):
#    video_url=''
#    source = getUrl(url)
#    try:
#        contentVideo = jsunpack.unpack(source.decode('string_escape'))
#    except:
#        contentVideo =''
#    src=re.compile('src=["\'](http:.*?)["\']').findall(contentVideo)
#    if src:
#        header = {'Referer':  src[0], 'User-Agent': UA}
#        contentVideo = getUrl(src[0].replace('/view/','/watch/'),header=header)
#        url_swf = re.compile("SWFObject\\('(.*?)'").findall(contentVideo)
#        match = re.compile('(eval\\(function\\(p,a,c,k,e,d\\).*?)\n').findall(contentVideo)
#        if match:
#            contentVideo = jsunpack.unpack(match[0].decode('string_escape'))
#            dec_saw = lambda x: x.group(0).replace('%','').decode('hex')
#            contentVideo = re.sub('%.{2}',dec_saw,contentVideo)
#            code = contentVideo.replace("so.addVariable('file',",'file=')
#            code = code.replace("so.addVariable('streamer',",'streamer=')
#            code = code.replace('));',');')
#            code = code.replace('unescape','')
#            context = js2py.EvalJs()
#            context.execute(code)
#            streamer= getattr(context,'streamer')
#            file= getattr(context,'file')
#            if url_swf and streamer and file:
#                video_url = streamer +' playpath='+file + ' swfUrl='+url_swf[0] + ' swfVfy=1 live=1 timeout=13   pageUrl='+src[0]
#    return video_url

class reqaa(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
def _pxstream(query,data,url='http://tele-wizja.com/tvp-1/'):
    video_url=''
    header = {'User-Agent':UA,
                'Referer': url,
                'Host':'pxstream.tv',
                'Upgrade-Insecure-Requests':1}
    cj = cookielib.LWPCookieJar()
    contentVideo = get_url_(query,cj,header=header)
    decaa=';'.join(['%s=%s'%(c.name,c.value) for c in cj])
    source = re.compile('(?:src|source)(?:\\:|=)\\s*[\'"](http.*?m3u.)[\'"]').findall(contentVideo)
    if not source:
        source = re.compile('(?:src|source|file)(?:\\:|=)\\s*[\'"](http.+stream.+?m3u.*)[\'"]').findall(contentVideo)
    if source:
        header={'Origin':'http://pxstream.tv',
                'Pragma':'no-cache',
                'Referer':query,
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Cache-Control':'no-cache',
                }
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(reqaa, urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = header.items()
        response = opener.open(source[0])
        locat = response.headers.get('Location','')
        response.close()
        if locat:
            video_url = locat+'|Referer='+query+'&User-Agent='+UA
    return video_url
#def _myfreshinfo(query,data,url):
#    video_url=''
#    contentDec=getUrl(query)
#    unesc = re.compile('unescape\\(["\'](.*?)["\']\\)').findall(contentDec)
#    unesc2 = unesc[0].replace('%','').decode('hex')
#    funct = re.compile('function (.*?)\\(').findall(unesc2)[0]
#    funct2 = unesc[1].replace('%','').decode('hex')
#    jscript = re.compile('<SCRIPT LANGUAGE="JavaScript">%s\\("(.*?)"\\);</SCRIPT>'%funct,re.DOTALL).findall(contentDec)
#    if jscript:
#        code = jscript[0]
#        code =''+code.strip('\\n')+''
#        try:
#            fun = unesc2.replace('document.write(tttmmm)','return tttmmm')
#            ctx = execjs.compile(fun)
#            contentVideo = ctx.call(funct, code)
#        except:
#            context = js2py.EvalJs()
#            context.execute(fun)
#            contentVideo = getattr(context,funct)(code)
#    return video_url
def _flowplayer(query,data,url):
    video_url=''
    netCon = re.compile("'(rtmp://.*?)'").findall(data)
    url_swf = re.compile("src:'(http://.*?swf)'").findall(data)
    if netCon and url_swf:
        video_url = netCon[0] + ' swfUrl='+url_swf[0] + ' swfVfy=1 live=1 timeout=13  pageUrl='+url
    return video_url
def _cinematvxyz(query,data,url):
    video_url=''
    file = re.compile("url: '(.*?)'").findall(data)
    netCon = re.compile("'(rtmp://.*?)'").findall(data)
    url_swf = re.search('"player", "(.*?.swf)"',data)
    if file and netCon and url_swf:
        video_url = netCon[0] + ' playpath='+file[0].strip() +' swfUrl='+url_swf.group(1) + ' swfVfy=1 live=1 timeout=13  pageUrl='+url
    return video_url
def _shidurlive(query,data,url):
    video_url='TODO'
    return video_url
def _freedocast(query,data,url):
    video_url=''
    link = re.compile('"streamer=(.*?)"').findall(data)
    if link:
        contentDec=link[0].split('&amp;')
        video_url = contentDec[0] +' playpath='+contentDec[1].split('=')[-1] +' swfUrl='+query+ ' swfVfy=1 live=1 timeout=13  pageUrl='+url
    return video_url
def _tvope(query,data,url):
    video_url=''
    feed = re.compile('c="(.*?)"; w=(.*?); h=(.*?);').findall(data)
    query = 'http://tvope.com/emb/player.php?c=%s&w=%s&h=%s&jw&d='%feed[0]
    query +=query+urlparse.urlparse(url).hostname
    header = {'User-Agent':UA,
                'Referer': url,
                'Host':'tvope.com'}
    contentVideo = getUrl(query,header=header)
    url_swf = re.compile("SWFObject\\('(.*?)'").findall(contentVideo)
    stream = re.compile("'streamer','(.*?)'\\);").findall(contentVideo)
    file   = re.compile("'file','(.*?)'\\);").findall(contentVideo)
    if url_swf and stream and file:
        video_url = stream[0] +' playpath='+file[0] + ' swfUrl='+url_swf[0] + ' swfVfy=1 live=1 timeout=13  pageUrl='+query
    return video_url
def _dotstream(query,data,urlref):
    video_url=''
    query = query.replace('/pl?','/player.php?')
    query = 'http:'+query if query.startswith('//') else query
    header = {'User-Agent':UA,
            'Referer': urlref}
    contentVideo = getUrl(query,header=header)
    if contentVideo:
        url_swf = re.compile('swfPath: "(.*?)"').findall(contentVideo)
        url_swf = url_swf[-1] if url_swf else 'http://dotstream.tv/jwp/jwplayer.flash.swf'
        if url_swf.startswith('//'):
            url_swf = 'http:'+url_swf
        vpartm = re.search("v_part_m = '(.*?)';",contentVideo)
        addrpart = re.search("addr_part = '(.*?)';",contentVideo)
        if re.search('a = ([0-9]+)',contentVideo):
            a=int(re.search('a = ([0-9]+)',contentVideo).group(1))
            b=int(re.search('b = ([0-9]+)',contentVideo).group(1))
            c=int(re.search('c = ([0-9]+)',contentVideo).group(1))
            d=int(re.search('d = ([0-9]+)',contentVideo).group(1))
            f=int(re.search('f = ([0-9]+)',contentVideo).group(1))
            v_part = re.search("v_part = '(.*?)';",contentVideo).group(1)
            if a and b and c and d :
                link = 'rtmp://%d.%d.%d.%d/'%(a/f,b/f,c/f,d/f)
            else:
                link = 'rtmp://'+ re.search("addr_part = '(.*?)';",contentVideo).group(1)+'/'
            link = link + v_part.split('/')[1]+'/'+' playpath='+v_part.split('/')[-1]
            video_url = link + ' swfUrl='+url_swf + ' swfVfy=1 live=1 timeout=13 pageUrl='+query
    return video_url
def get_Cookies(url,params=None,header={}):
    try:
        req = urllib2.Request(url,params,headers=header)
        sock=urllib2.urlopen(req)
        cookies=sock.info()['Set-Cookie']
        sock.close()
    except:
        cookies=''
    return cookies
def l11l1l1ll1l11l111_tv_(url,params=None,header={}):
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener( urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    if not header: header = {'User-Agent':UA}
    req = urllib2.Request(url,params,headers=header)
    try:
        response = urllib2.urlopen(req,timeout=5)
        response.close()
    except:
        pass
    cookies=''.join(['%s=%s;'%(c.name, c.value) for c in cj])
    return cookies
def get_cookie_value(cookies='',value='sesssid'):
    idx1=cookies.find(value+'=')
    if idx1==-1:
        return ''
    else:
        idx2=cookies.find(';',idx1+1)
    return cookies[idx1:idx2]
	
def _bankaistream(query,data,url):	
	header = {'User-Agent':UA,
			'Referer': url}
	contentVideo = getUrl(query,header=header)	
	vido_url=re.findall("""source:\s*['"](.+?)['"]""",contentVideo,re.DOTALL)	
	vido_url = vido_url[0] if vido_url else ''
	return vido_url
def _broadcast(query,data,url):
    video_url=''
    if 'st/stream.php' in query:
        url_main = query
    else:
        feed = re.compile('id=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(data)
        if feed: url_main='http://bro.adca.st/stream.php?id=%s&p=1&c=0&stretching=uniform&old=0'%feed[0][0]
        else: url_main=''
    if url_main:
        header = {'User-Agent':UA,
                'Referer': url}
        contentVideo = getUrl(url_main,header=header)
        host ='bro.adca.st'
        url_bro='http://bro.adca.st/aloha.php'
        header = {'User-Agent':UA,
                'Referer': url_main,
                'Host':host,
                'X-Requested-With':'XMLHttpRequest'}
        contentBro = getUrl(url_bro,header=header)
        token = re.findall('"rumba":"(.*?)"',contentBro)
        main_url_bro = re.findall('\\w+\\s*=\\s*"(.+?token=)"',contentVideo)
        if main_url_bro and token:
            video_url = main_url_bro[0] + token[0] +'|User-Agent='+urllib.quote(UA)+'&Referer='+url_main
    return video_url
def _111lll1lll11l111_tv_(query,data,url):
    video_url=''
    feed = re.compile('id=[\'"](.*?)[\'"]; width=[\'"](.*?)[\'"]; height=[\'"](.*?)[\'"];').findall(data)
    if feed:
        url_main='http://bro.adca.st/stream.php?id=%s&cache=4&width=%s&height=%s&stretching=uniform&p=1&c=0'%feed[0]
        host ='bro.adca.st'
        header = {'User-Agent':UA,
                'Referer': url,
                'Host':host,
                 }
        cookies=''
        contentVideo = getUrl(url_main,header=header)
        main_url_bro = re.search('curl = "(.*?)"',contentVideo)
        header = {'User-Agent':UA,
                'Referer': url_main,
                'Host':host,
                'X-Requested-With':'XMLHttpRequest'}
        url_bro='http://'+host+'/getToken.php'
        contentBro = getUrl(url_bro,header=header)
        token = re.search('"token":"(.*?)"',contentBro)
        if main_url_bro and token:
            cookies= get_Cookies(url_main,header=header)
            h = '|Cookie=%s' % get_cookie_value(cookies,'PHPSESSID')
            l1111ll11ll11l111_tv_='http://cdn.allofme.site/jw/jwplayer.flash.swf'
            link = base64.b64decode(main_url_bro.group(1))
            video_url = link + token.group(1) + h+'&User-Agent='+UA+'&Referer='+l1111ll11ll11l111_tv_
    return video_url
def _jwpcdn(query,data,url):
    video_url=''
    file   = re.compile('[\']*file[\']*[:, ]*[\'"](.*?)[\'"]').findall(data)
    if file:
        file = file[0]
        if file.endswith('m3u8'):
            video_url = file
        else:
            url_swf='http://p.jwpcdn.com/6/12/jwplayer.flash.swf'
            video_url = file + ' swfUrl='+url_swf + ' live=1 timeout=13  pageUrl='+url
    return video_url
def _jwpsrv(query,data):
    video_url=''
    file   = re.compile('[\']*file[\']*[:, ]*[\'"](.*?)[\'"]').findall(data)
    if file:
        file = file[0]
        if file.endswith('m3u8'):
            video_url = file
        else:
            url_swf='http://p.jwpcdn.com/6/12/jwplayer.flash.swf'
            video_url = file + ' swfUrl='+url_swf + ' live=1 timeout=13  pageUrl='+query
    return video_url
def _aliezme(query,data,url):
	video_url=''
	header = {'User-Agent':UA,'Referer': url}
	contentVideo=getUrl(query,header=header)
	video_url   = re.compile("""['"]*(http[^'^"]+?\.m3u8[^'^"]*?)['"]""").findall(contentVideo)
	video_url=video_url[0] +'|User-Agent='+UA+'&Referer='+url  # '|User-Agent='+UA+'&Referer='+next_url[0] #' live=true swfVfy=1 swfUrl=http://i.aliez.me/swf/playernew.swf flashver=WIN\2024,0,0,221 pageUrl=' +next_url[0]
	return video_url
def _ustream(query,data):
    video_url=''
    cid = re.search('cid=(.*?)"',data)
    HLS_PLAYLIST_URL = 'http://iphone-streaming.ustream.tv/uhls/%s/streams/live/iphone/playlist.m3u8'
    if cid:
        cid=cid.group(1)
        data = getUrl(HLS_PLAYLIST_URL%cid)
        if data:
            links = re.compile('\n(http.*?)\n').findall(data)
            if links:
                video_url = links[0]
    return video_url
def _privatestream(query,data):
    video_url=''
    query = 'http:'+query if query.startswith('//') else query
    if 'js?' in query:
        tmp = getUrl(query)
        src2 = re.compile('src=["\'](.*?)["\']',re.IGNORECASE).findall(tmp)
        if src2:
            src2 = src2[0]
            query = 'http:'+src2 if src2.startswith('//') else src2
    contentVideo = getUrl(query)
    url_main=[]
    if url_main:
        url_swf = re.compile('swfPath: "(http.*?)"').findall(contentVideo)
        url_swf = url_swf[-1] if url_swf else 'http://privatestream.tv/clappr/RTMP.swf?inline=1'
        url_swf='http://privatestream.tv/clappr/RTMP.swf'
        a=int(re.search('a = ([0-9]+)',contentVideo).group(1))
        b=int(re.search('b = ([0-9]+)',contentVideo).group(1))
        c=int(re.search('c = ([0-9]+)',contentVideo).group(1))
        d=int(re.search('d = ([0-9]+)',contentVideo).group(1))
        f=int(re.search('f = ([0-9]+)',contentVideo).group(1))
        v_part = re.search("v_part = '(.*?)';",contentVideo).group(1)
        link = 'rtmp://%d.%d.%d.%d/'%(a/f,b/f,c/f,d/f) + v_part.split('/')[1]+'/'+' playpath='+v_part.split('/')[-1]
        video_url = link + ' swfUrl='+url_swf + ' live=1 timeout=13 pageUrl='+query
    elif contentVideo:
        vpartm = re.search("v_part_m = '(.*?)';",contentVideo)
        addrpart = re.search("addr_part = '(.*?)';",contentVideo)
        url_swf='http://privatestream.tv/clappr/RTMP.swf'
        if re.search('a = ([0-9]+)',contentVideo):
            a=int(re.search('a = ([0-9]+)',contentVideo).group(1))
            b=int(re.search('b = ([0-9]+)',contentVideo).group(1))
            c=int(re.search('c = ([0-9]+)',contentVideo).group(1))
            d=int(re.search('d = ([0-9]+)',contentVideo).group(1))
            f=int(re.search('f = ([0-9]+)',contentVideo).group(1))
            v_part = re.search("v_part = '(.*?)';",contentVideo).group(1)
            if a and b and c and d :
                link = 'rtmp://%d.%d.%d.%d/'%(a/f,b/f,c/f,d/f)
            else:
                link = 'rtmp://'+ re.search("addr_part = '(.*?)';",contentVideo).group(1)+'/'
            link = link + v_part.split('/')[1]+'/'+' playpath='+v_part.split('/')[-1]
            video_url = link + ' swfUrl='+url_swf + ' swfVfy=1 live=1 timeout=13 pageUrl='+query
    return video_url
def _casttome(query,url,data):
    video_url =''
    feed = re.compile('fid="(.*?)"; v_width=(.*?); v_height=(.*?);').findall(data)
    if feed:
        url_main='http://static.castto.me/embedlivesrclappr.php?channel=%s&vw=%s&vh=%s'%feed[0]
    else:
        url_main=query
    header = {'User-Agent':UA,
            'Referer': url,
            'Host':'static.castto.me',
            }
    contentVideo = getUrl(url_main,header=header)
    file   = re.compile('file\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
    if file:
        video_url = file[-1]
    file   = re.compile('source\\s*:\\s*["\'](.*?)[\'"]').findall(contentVideo)
    if file:
        video_url = file[-1]
    file   = re.compile('<source src=["\'](.*?)[\'"]').findall(contentVideo)
    if file:
        video_url = file[-1]
    if video_url:
        video_url += '|User-Agent='+urllib.quote(UA)+'&Referer='+url_main+'&Cookie='+urllib.quote('userid=264414038;')
    return video_url
