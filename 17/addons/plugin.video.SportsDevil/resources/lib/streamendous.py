# -*- coding: UTF-8 -*-
import sys
import urllib2,urllib,urllib3
import cookielib
import threading
import re
import time
import requests
from CommonFunctions import parseDOM
import urlparse
import mydecode
reload(sys)
sys.setdefaultencoding('utf8')

import cfdeco6
scraper = cfdeco6.create_scraper()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BASEURL='http://www.streamendous.com'
BASEURL2='https://cricfree.stream/'
BASEURL3='http://strims.world/'
BASEURL4='https://www.soccerstreams100.com/'
BASEURL5='https://livesport.ws/en/'
sess = requests.Session()
UA="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
UAbot='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
def getUrl(url,ref=BASEURL2):
	headers = {'User-Agent': UA,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': ref,}
	html=requests.get(url,headers=headers,verify=False,timeout=30)#.content
	if html.status_code == 503:
		html=scraper.get(url).text
	else:
		html=html.content
	if html.find('by DDoS-GUARD')>0:   
		headers = {'User-Agent': UAbot,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': ref,'Cookie':unbkuk}
		html=requests.get(url,headers=headers,verify=False,timeout=30).content		
		#or creating a cookie “_ddgu” with random characters
	return html
	
def getUrl2(url,ref=BASEURL2):
	headers = {'User-Agent': UA,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Referer': ref,}
	html=requests.get(url,headers=headers,verify=False,timeout=30)
	if html.status_code == 503:
		html=scraper.get(url)#.text
	last=html.url
	html=html.content
	return html,last
def ListUnblocked(url):
	out=[]
	html=getUrl(url)
	hrefname=re.findall('col-sm-3.+?"><a class=".+?" href=(.+?) target=_blank role=button>(.+?)<',html,re.DOTALL)
	for href,title in hrefname:
		out.append({'href':href,'title':'[B][COLOR gold]%s[/COLOR][/B]'%title}) #'[COLOR lime]► [/COLOR] [B][COLOR gold] Link 2 - %s[/COLOR][/B]'
	return out

def getScheduleCR():
	out=[]
	html=getUrl(BASEURL2)
	divs = parseDOM(html,'div',attrs = {'class':'panel_mid_body'})
	for div in divs:
		day = parseDOM(div,'h2')#[0]
		if day:
			day='kiedy|%s'%day[0]
			out.append({'href':day})
		trs = parseDOM(div,'tr')#[0]
		for tr in trs:
			online= '[COLOR lime]► [/COLOR]' if tr.find('images/live.gif')>0 else '[COLOR orangered]■ [/COLOR]'
			if '>VS</td>' in tr:
				czas,dysc,team1,team2,href=re.findall('>(\d+:\d+)</td>.+?<span title="(.+?)".+?href=.+?>(.+?)<.+?>VS<.+?a href.+?>(.+?)</a>.+?<a class="watch_btn" href="(.+?)"',tr,re.DOTALL)[0]
				mecz='%s vs %s'%(team1,team2)
				
				czas=czas.split(':')
				hrs=int(czas[0])+2
				if hrs==24:
					hrs='00'
				mins=czas[1]
				czas='%s:%s'%(str(hrs),mins)
			else:
				czas,dysc,team1,href=re.findall('>(\d+:\d+)</td>.+?<span title="(.+?)".+?href=.+?>(.+?)<.+?<a class="watch_btn" href="(.+?)"',tr,re.DOTALL)[0]
				mecz=team1
			title = '[B][COLOR khaki]%s%s : [/COLOR][/B][COLOR gold][B]%s[/B][/COLOR]'%(online,czas,mecz)
			out.append({'title':title,'href':href,'code':dysc})
	return out




	
def getChannelsCR():
	out=[]
	html=getUrl(BASEURL2)
	result = parseDOM(html,'ul',attrs = {'class':"nav-sidebar"})[0]#<div class="arrowgreen">
	channels = parseDOM(result,'li')
	for channel in channels:
		if '<ul class="nav-submenu">' in channel:
			continue
		try:
			href = parseDOM(channel,'a',ret='href')[0]
			title = parseDOM(channel,'a',ret='title')[0]
			out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+title+'[/COLOR][/B]'})
		except:
			pass
	return out	
	
def getSstreamsStreams(url):
	out=[]
	html=getUrl(url)
	try:
		result = parseDOM(html,'tbody')[0]
		if 'acestream:' in result.lower():
			result = parseDOM(html,'tbody')[1]
		items = parseDOM(result,'tr')
		for item in items:
			dane = parseDOM(item,'td')
			lang=dane[4]
			href = parseDOM(item,'a',ret='href')[1]
			tyt = parseDOM(item,'a')[1]
			tyt='%s [B][%s][/B]'%(tyt,lang)
			out.append({'href':href,'title':tyt})
	except:
		pass
	return out

	
def getF1stream(url):
	out=[]
	html=getUrl(url)
	tithref=re.findall("""<h3>([^>]+)<.+?['"](http.+?)['"]""",html,re.DOTALL)

	if not tithref:
		tithref=re.findall("""<h3>([^>]+)<.+?<source src=['"]([^'"]+)['"]""",html,re.DOTALL)
	for tyt,href in tithref:
		out.append({'href':href,'title':tyt})
	return out

	

def getSWstreams(url):
	out=[]
	html,basurl=getUrl2(url)
	
	try:
		try:
			result = parseDOM(html,'font size=3.+?')[0]
		except:
			result = parseDOM(html,'font',attrs = {'size':'3'})[0]

		if '<center><b>' in result:
			result = parseDOM(html,'font',attrs = {'size':'3'})[1]
		result=result.replace('\n','').replace('<b>','').replace('</b>','')

		try:
			result2=result.replace('\n','').replace('</a> |',' |').replace('<b>','').replace('</b>','')

			xx=re.findall('(\w+.*?: <a class.+?</a>)',result2,re.DOTALL)
			
			
			for x in xx:
				x=x.replace('br>','')
				lang=re.findall('^(\w+)',x,re.DOTALL)[0]
				hreftyt=re.findall('href="(.+?)".+?>(Source \d.+?)<',x)
				for href,tyt in hreftyt:
					tyt = tyt.replace('|','')
					href=basurl+href
					tyt='%s - [B]%s[/B]'%(lang,tyt)
					out.append({'href':href,'title':tyt})

		except:
			results=result.split('|')
			for result in results:
				href,name=re.findall('href="(.+?)".+?>(.+?)<\/a>',result)[0]
				href=url+href
				out.append({'href':href,'title':name.replace('<b>','').replace('</b>','')})		
		
	except:
		pass
	if not out:
		try:
			#	except:
			results=result.split('|')
			for result in results:
				href,name=re.findall('href="(.+?)".+?>(.+?)<\/a>',result)[0]
				href=url+href
				out.append({'href':href,'title':name.replace('<b>','').replace('</b>','')})	
		except:
			pass
	return out
	
	
def getSWstreamsx(url):
	out=[]
	html=getUrl(url)
	try:
		result = parseDOM(html,'font',attrs = {'size':'3'})[0]
		if '<center><b>' in result:
			result = parseDOM(html,'font',attrs = {'size':'3'})[1]
		t = re.sub('--.*?>', '', result)
		result= t.replace('\r\n\r\n','')	
		try:
			xx=re.findall('(\w+)\: <a(.+?)adsbygoogle',result,re.DOTALL)
			b=xx[0]
			for x in xx:
				tit='%s'%x[0]
				aa=re.findall('href="(.+?)".+?>(.+?)</a>',x[1],re.DOTALL)
				for a in aa:
					if 'vjs' in a[0]:
						continue				
					href= a[0]
					tytul= a[1].replace('<b>','').replace('</b>','')
					tyt='%s - [B]%s[/B]'%(tytul,tit)
					href=url+href
					out.append({'href':href,'title':tyt})

		except:
			results=result.split('|')
			for result in results:
				href,name=re.findall('href="(.+?)".+?>(.+?)<\/a>',result)[0]
				href=url+href
				out.append({'href':href,'title':name.replace('<b>','').replace('</b>','')})		
		
	except:
		pass
	return out
def getCRlink(url):
	out=[]
	html=getUrl(url)
	result = parseDOM(html,'div',attrs = {'class':'video_btn'})#[0]
	if result:
		hrefhost=re.findall('link="(.+?)">(.+?)<',result[0],re.DOTALL)
		for href,host in hrefhost:
			out.append({'href':href,'title':host})
	return out
	
def unescapeHtml(hh):
	hh=re.findall('(eval\(unescape.+?</script>)',hh,re.DOTALL)[0]
	vales=re.findall("""['"](.+?)['"]""",hh,re.DOTALL)#[0]
	vale=vales[0] if vales else ''
	a=urllib2.unquote(vale)  
	if 'm3u8' in a or 'src="http' in a:
		return a
	else:
		try:
			spl=re.findall("""split\(['"](.+?)['"]\)""",a,re.DOTALL)[0]
			pl=re.findall("""\+\s*['"](.+?)['"]\);""",a,re.DOTALL)[0]
			odj=re.findall('\(i\)\)(.+?)\);',a,re.DOTALL)[0]	
			funkcja='chr((int(k[i%len(k)])^ord(s[i]))'+odj+')'
			tmp=vales[2]
			tmp = tmp.split(spl)
			s = urllib2.unquote(tmp[0]);
			k = urllib2.unquote(tmp[1] + pl);
			r=''
			for i in range(0, len(s)):
				r+=eval(funkcja)
			return r
		except:
			return a
	
def resolvingCR(url,ref):
	html=getUrl(url,ref)
	iframes= parseDOM(html,'iframe',ret='src')#[0]
	dal=''
	for iframe in iframes:
		if 'unblocked.is' in iframe:
			if 'nullrefer.com' in iframe or 'href.li/' in iframe:
				iframe = urlparse.urlparse(iframe).query
			html2=getUrl(iframe,url)		
			stream=getUnblocked(html2)
			return stream
		#elif 'twitch.tv' in iframe:
		#	return iframe
		
		elif 'nullrefer.com' in iframe or 'href.li/' in iframe:
			iframe = urlparse.urlparse(iframe).query

			html=getUrl(iframe,url)	
			url=iframe
			break
		elif 'sportsbay.org' in iframe:
			if iframe.startswith('//'):

				iframe = 'https:'+iframe
			html=getUrl(iframe,url)	
			url=iframe
			dal=iframe
			break
		elif 'daddylive.live' in iframe:
			if iframe.startswith('//'):

				iframe = 'https:'+iframe
			html=getUrl(iframe,url)	
			url=iframe
			dal=iframe
			break
		elif 'strimstv.eu' in iframe:
			if iframe.startswith('//'):
				iframe = 'https:'+iframe
			html=getUrl(iframe,url)	
			url=iframe
			dal=iframe
			break
	
	if html.find("eval(unescape('")>0:
		try:
			html=unescapeHtml(html)
		except:
			pass
	vido_url=re.findall("""['"](rtmp:.+?)['"]""",html,re.DOTALL)
	if vido_url:
		vido_url = vido_url[0]
	else:
		vido_url=re.findall("""source:\s*['"](.+?)['"]""",html,re.DOTALL)

		vido_url = vido_url[0]+'|User-Agent='+UA+'&Referer='+dal if vido_url else mydecode.decode(url,html)
		if vido_url:
			if 'about:blank' in vido_url:
				vido_url=mydecode.decode(url,html)	
	return vido_url
	
def getScheduleSE():
	out=[]
	html=getUrl(BASEURL)
	result = parseDOM(html,'table',attrs = {'align':'center'})[1]
	#nt=re.findall("font-size:18px'>Thursday - Feb 14th, 2019<",result)
	tds = parseDOM(result,'tr',attrs = {'style':' height:35px; vertical-align:top;'})#[0]
	dat= parseDOM(result,'span',attrs = {'style':' font-size:18px'})#<span style='font-size:18px'>
	for td in tds:
		
		tdk = parseDOM(td,'td')[0]

		czas = parseDOM(tdk,'td',attrs = {'class':'matchtime'})[0]
		teams = parseDOM(tdk,'td')[2]
		href = parseDOM(tdk,'a',ret='href')[0]
		href = BASEURL+href if href.startswith('/') else href
		dysc=teams.split(':')[0]
		tem=teams.split(':')[1]
		tit='%s - %s'%(czas,tem)
		out.append({'href':href+'|sch','title':tit,'code':dysc})
	return out

def getChannelsSE():
	out=[]
	html=getUrl(BASEURL)
	result = parseDOM(html,'div',attrs = {'class':'arrowgreen'})[0]#<div class="arrowgreen">
	lis = parseDOM(result,'li')#[0]
	for li in lis:
		title = parseDOM(li,'img',ret='alt')#[0]
		if title:
			if 'schedule' in title[0].lower():
				continue
		title=title[0] if title else parseDOM(li,'a')[0]
		href = parseDOM(li,'a',ret='href')[0]
		href = BASEURL+href if href.startswith('/') else href
		imag = parseDOM(li,'img',ret='src')#[0]
		imag= BASEURL+'/'+imag[0] if imag else ''
		out.append({'href':href+'|chan','title':title,'image':imag})
	return out	
	
def getSElink(url):
	
	out=[]
	url2=url.split('|')[0]
	
	query=urlparse.urlparse(url2).query
	co=1
	if 'sch' in url.split('|')[1]:
		url3='%s/streams/ss/ss%s.html'%(BASEURL,query)
		html=getUrl(url3,BASEURL)
		xbmc.sleep(2000) 
		stream=mydecode.decode(url3,html)
		if stream:
			out.append({'href':stream,'title':'Link %d'%co})
		return out
	else:
		url='%s/streams/misc/%s.html'%(BASEURL,query)
	html=getUrl(url,BASEURL)
	links=re.findall('id="link\d+" class="class_.+?" href="(.+?)"',html,re.DOTALL)
	
	for link in links:
		link= BASEURL+link if link.startswith('/') else link
		query=urlparse.urlparse(link).query
		if not query:
			query=link #if not query
		out.append({'href':query,'title':'Link %d'%co})

		co+=1
	return out
def getScheduleSW():
	out=[]
	html=getUrl(BASEURL3)
	first  = parseDOM(html,'div',attrs = {'class':'tab'})[0]#<div class="tab">
	iddaydate=re.findall("event, '(.+?)'\).+?<b>(.+?)</b>.+?<b>(.+?)</b>",first,re.DOTALL)
	for id,day,date in iddaydate:

		result = parseDOM(html,'div',attrs = {'id':id})[0]
		result=result.replace('a class=""','a class=" "')
		xxx=re.findall('(\d+:\d+).*<a class="([^"]+)" href="([^"]+)">([^>]+)</a>',result)
		if xxx:
			day=('kiedy|%s %s'%(day,date)).replace('FIRDAY','FRIDAY')	
			out.append({'href':day})	
			for czas,ikona,href,tyt in  xxx:
				if '\xf0\x9f\x8e\xb1' in ikona:
					ikona='snooker'
				tyt=re.sub('<font color=.+?>', '', tyt).replace('</font>','')
				if '<a href' in tyt or '<br><br' in tyt:
					continue
				tyt = '[B][COLOR khaki]%s : [/COLOR][/B][COLOR gold][B]%s[/B][/COLOR]'%(czas,tyt)
				href2='http://strims.world'+href if href.startswith ('/') else 'http://strims.world/'+href
				out.append({'title':tyt,'href':href2,'image':ikona})								
	return out
	
def getScheduleSstreams():
	out=[]
	html=getUrl(BASEURL4)
	result  = parseDOM(html,'div',attrs = {'class':"main-inner group"})[0] 
	items = parseDOM(html,'article',attrs = {'id':"post-\d+"}) 
	for item in items:
		href = parseDOM(item,'a',ret='href')[0]
		imag = parseDOM(item,'img',ret='src')[0]
		tyt = parseDOM(item,'a')[2]
		code = parseDOM(item,'a')[1]
		tyt='[COLOR gold][B]%s[/B][/COLOR]'%tyt
		out.append({'title':tyt,'href':href,'image':imag,'code':code})	
	return out

def getChannelsSW():
	out=[]
	html=getUrl(BASEURL3+'sports-channel/')
	result = parseDOM(html,'tbody')[0]
	hrefimage=re.findall('<a href="(.+?)"><img src="(.+?)"></a>',result,re.DOTALL)
	for href,image in hrefimage:
		tyt=href.split('-stream-online')[0].replace('-',' ').upper()
		href = 'http://strims.world/sports-channel/'+href
		out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+tyt+'[/COLOR][/B]','image':image})
	return out	
	
def F1channels():

	out=[]
	html=getUrl(BASEURL3+'live/4/f1fanbase.php')

	result = parseDOM(html,'h3')[0]
	hreftit=re.findall('href="([^"]+)"><.+?>([^>]+)<',result,re.DOTALL)
	for href,tyt in hreftit:
		href = 'http://strims.world'+href
		out.append({'href':href,'title':'[COLOR lime]► [/COLOR] [B][COLOR gold]'+tyt+'[/COLOR][/B]'})
	return out	
	
	
def getUnblocked(html):
	html=re.findall('<script>(.+?)document.write',html,re.DOTALL)[0]
	oile=re.findall('(\d+?)\); }',html,re.DOTALL)[0]
	dane2=re.findall('(\[.+?\])',html,re.DOTALL)[0]
	ht=eval(dane2)
	text=''
	for d in ht:
		a=int(d)-int(oile)
		text+=chr(a)
	source=re.findall('src="(.+?m3u8.+?)"',text)
	if not source:
		source =re.findall('source: "(.+?)"',text,re.DOTALL)
		source = source[0] if source else ''
	else:
		source=source[0] if source else ''
	source = 'http:'+source if source.startswith('//') else source
	return source
def getSWlink(url):
	stream=''
	playt=True
	html=getUrl(url,BASEURL3)
	if 'streamamg.com' in html:
		iframes = parseDOM(html,'iframe',ret='src')#[0]
		for iframe in iframes:
			if 'streamamg.' in iframe:
				html2=getUrl(iframe,url)	
				xx=re.findall('"partnerId":(\d+)',html2,re.DOTALL)[0]
				xx2=re.findall('"rootEntryId":"(.+?)"',html2,re.DOTALL)[0]
				m3u8='http://open.http.mp.streamamg.com/p/%s/playManifest/entryId/%s/format/applehttp'%(xx,xx2)
				return m3u8+'|User-Agent='+UA+'&Referer='+iframe,False
	elif 'unblocked.is' in html:
		iframes= parseDOM(html,'iframe',ret='src')#[0]
		for iframe in iframes:
			if 'unblocked.is' in iframe:
				if 'nullrefer.com' in iframe or 'href.li/' in iframe:
					iframe = urlparse.urlparse(iframe).query
				html2=getUrl(iframe,url)
				stream=getUnblocked(html2)
				return stream,False
	else:
		stream=re.findall('source: "(.+?)"',html,re.DOTALL)
	if stream:
		stream=stream[0]	
	else:
		stream=re.findall('source src="(.+?)"',html,re.DOTALL)[0]
		playt=False
	return stream+'|User-Agent='+UA+'&Referer='+url,playt
	
def getSWlink2(url):
	stream=''
	playt=True
	html=getUrl(url,BASEURL3)
	stream=getUnblocked(html)
	return stream,False

	
def getLiveSport():
	out =[]
		#try:
	html=getUrl(BASEURL5,BASEURL5)
	
	result = parseDOM(html,'ul',attrs = {'class':"drop-list"})
	#<ul class="drop-list">
	acts = parseDOM(result,'li',attrs = {'class':"active"})
	for act in acts:
		
		
		#kiedy = parseDOM(act,'div',attrs = {'class':"opener"})#<div class="opener">
		#print kiedy
		
		kiedy = re.findall('"text">(.+?)<\/span><\/a>',act)[0] #>12 September, Today</span></a>
		day='kiedy|%s'%kiedy
		out.append({'href':day})	
		
		act=act.replace("\'",'"')
		links = parseDOM(act,'li')#[0]
		for link in links:
		#	print link
			href = parseDOM(link,'a',ret='href')[0]
			href = 'https://livesport.ws'+href if href.startswith('/') else href
			try:
				team1 = re.findall('right;">(.+?)<\/div>',link)[0]
				team2 = re.findall('left;">(.+?)<\/div>',link)[0]
				mecz='%s vs %s'%(team1,team2)
			except:
				mecz=re.findall('center;.+?>(.+?)<',link)[0]
			dysc = re.findall('"competition">(.+?)</',link)#[0]
			dysc =dysc[0] if dysc else ''
			ikon = parseDOM(link,'img',ret='src')[0]
			datas = parseDOM(link,'span',attrs = {'class':"date"})[0] #<span class="date">
			liv = parseDOM(datas,'i')[0]
			
			online= '[COLOR lime]► [/COLOR]' if 'live' in liv.lower() else '[COLOR orangered]■ [/COLOR]'
			id = parseDOM(link,'i',ret='id')#[0]
			if id:
				postid=re.findall('(\d+)',href)[0]
				eventid=id[0]
				href+='|event_id=%s|post_id=%s|'%(eventid,postid)
			#if 'live' in liv.lower():
			#	online = 
			czas = parseDOM(datas,'i',ret='data-datetime')[0]#attrs = {'class':"date"})
			st=re.findall('(\d+:\d+)',czas)[0]
			czas1 = str(int(st.split(':')[0])-1)
			czas = re.sub('\d+:', czas1+':', czas)
			title = '[B][COLOR khaki]%s%s : [/COLOR][/B][COLOR gold][B]%s[/B][/COLOR]'%(online,czas,mecz)
			out.append({'title':title,'href':href,'image':ikon,'code':dysc})
	#except:
	#	pass
	return out

def getLinksLiveSport(url,tytul):
	out=[]

	ref=url.split('|')[0]
	evpo = re.findall('(\d+)\|post_id=(\d+)\|',url)[0]

	event_id=evpo[0]
	post_id=evpo[1]
	cookies = {
		'dle_time_zone_offset': '7200',
	}

	headers = {
		'User-Agent': UA,
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'X-Requested-With': 'XMLHttpRequest',

		'Referer': ref,

	}
	
	dane = (
		('from', 'event'),
		('event_id', event_id),
		('tab_id', 'undefined'),
		('post_id', post_id),
		('lang', 'en'),
	)

	response = sess.get('https://livesport.ws/engine/modules/sports/sport_refresh.php', headers=headers, params=dane, cookies=cookies,verify=False,timeout=30).json()
	try:
		broadcast=response['broadcast']
		flashes = parseDOM(broadcast,'li',attrs = {'class':"flashtable",'id':'.+?'})#[0]
		if flashes:
			flashes  = parseDOM(flashes[0],'tbody')
		links = parseDOM(flashes,'tr')
		co=1
		for link in links:
			code = parseDOM(link,'img',ret='title')#[0]
			code = code[0] if code else ''
			href = parseDOM(link,'a',ret='href')
			href = href[0] if href else ''
			
			tyt = 'Link %s - [COLOR violet]%s[/COLOR]'%(co,code)

			if href:
				out.append({'title':tyt,'href':href,'image':'','code':code})	
				co+=1
			else:
				continue
	except:
		pass
	return out
	
	
	
	
def getStreamLiveSport(url):


	headers = {
		'Host': 'stream.livesport.ws',
		'User-Agent': UA,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		'DNT': '1',
		'Upgrade-Insecure-Requests': '1',
	}

	html = sess.get(url, headers=headers,verify=False,timeout=30).text
	
	iframe = parseDOM(html,'iframe',ret='src')[0]
	if 'vamosplay' in iframe:
		headers = {
			'User-Agent': UA,
			'Accept': '*/*',
			'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
			'Connection': 'keep-alive',
			'Referer': iframe,
		}
		
		html = sess.get('http://vamosplay.tech/js/config-stream.js', headers=headers,verify=False,timeout=30).text
		html=html.replace("\'",'"')
		servers = re.findall('var servers\s*=\s*"([^"]+)"',html)
		
		headers = {
			'User-Agent': UA,
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
			'Origin': 'http://vamosplay.tech',
			'Connection': 'keep-alive',
			'Referer': iframe,
	
		}
		
		response = sess.get(servers[0], headers=headers,verify=False,timeout=30).json()
		stream_adr=response['data']['url']
		rodzaj = re.findall('(\/\w+)',iframe)[-1]
		source = 'http://' + stream_adr + '/channels' + rodzaj + '/stream.m3u8'

	else:

		source=mydecode.decode(url,html)

	return source
	
	

	