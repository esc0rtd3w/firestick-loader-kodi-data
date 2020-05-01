import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,cookielib
from datetime import datetime,tzinfo,timedelta
import json
import base64




def resolve(url):
		import requests
		if 'tvcatchup' in url:
			open = OPEN_URL(url)
			url  = re.compile("file: '(.+?)'").findall(open)[0]
			url  = url  + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
		elif 'tvplayer' in url:
			url  = playtvplayer(url)
		elif 'sdwnet' in url:
			
			open  = OPEN_URL(url)
		
			iframe= regex_from_to(open,"iframe src='","'")
			h     = {}
			h['referer'] = url
			link = requests.session().get(iframe, headers=h, verify=False).text
			link = link.encode('ascii', 'ignore')
			url  = regex_from_to(link,'source: "','"')
			if not url.endswith=='.ts':
				url = url+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
			else:
				url    = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=%s'%url
		elif 'mpd://' in url:
			url = mobdroresolve(url)
		elif 'ustreamix' in url:
			url = ustreamixresolve(url)
		elif 'ibrod' in url:
			url = ibrodresolve(url)
		elif 'liveonlinetv247' in url:
			url  = (url).replace('liveonlinetv247:','')
			link = 'http://www.liveonlinetv247.info/embed/%s.php?width=650&height=480'%url
			open = OPEN_URL(link)
			url  = regex_from_to(open,'source src="','"') + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
		elif 'arconaitv' in url:
			open = OPEN_URL(url)
			url  = re.compile('"src":"(.*?)"',re.DOTALL).findall(open)[0]
			url  = (url).replace('\/','/')
			url  = url + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
		elif 'snappystreams:' in url:
			url = (url).replace('snappystreams:','')
			headers = {'Authorization': 'Basic QFN3aWZ0MTQjOkBTd2lmdDE0Iw==',
				'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)',
				'Accept-Encoding': 'gzip'}
			
			try:
				open = requests.session().get('http://173.212.202.101/token304.php',headers=headers).text
			except:	
				open = requests.session().get('http://173.212.202.101/token10304.php',headers=headers).text
			if '404 Not Found' in open:
				open = requests.session().get('http://173.212.202.101/token3004.php',headers=headers).text
			link = url+open
			url  = link+'|User-Agent=Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q'
			
		elif 'iptvrestream.net'in url:
			url  = url + '|User-Agent=FC'
			
		elif 'livetvindia.co.in' in url:
			url = url+'|User-Agent=samrai945&Accept=*/*&Range=bytes=0-&Connection=close&Host=live1.livetvindia.co.in:8000&Icy-MetaData=1'
		elif 'madotv.com' in url:
			url = url+'|User-Agent=Lavf/56.15.102&Accept=*/*&Range=bytes=0-&Connection=close&Host=main.madotv.com:25461&Icy-MetaData=1'
			
		elif 'mamahd.com' in url:
			url = mamahdresolve(url)
		elif 'cricfree' in url:
			url = cricfreeresolve(url)
		else:
			url = url
		return (url).replace('<p>','')

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	

def mamahdresolve(url):
			import requests
			open = OPEN_URL(url)
			embed = regex_from_to(open,'iframe.+?src="','"')
			open = OPEN_URL(embed)
			id   = regex_from_to(open,'fid="','"')
			url  = 'http://hdcast.org/embedlive1.php?u=%s&vw=680&vh=490'%id
			
			headers = {'Referer':embed}
			
			open = requests.session().get(url,headers=headers).text
			iframe = regex_from_to(open,'iframe.+?allowtransparency.+?src=',' ')
			
			headers = {'Referer':url}
			log(iframe)
			open = requests.session().get(iframe,headers=headers).text
			m3u8 = regex_from_to(open,'file: "','"')
			log(m3u8)
			url  = m3u8+ '|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
			return url

	
def ibrodresolve(url):
	import requests
	open = OPEN_URL(url)
	embed = regex_from_to(open,'iframe.+?src="','"')
	open = OPEN_URL(embed)
	iframe = regex_from_to(open,'text/javascript" src="','"')
	open = OPEN_URL(iframe)
	iframe  = regex_from_to(open,"iframe src='","'")
	open = requests.session().get(iframe,headers={'Referer':embed},verify=False).text
	link = open.encode('ascii', 'ignore')
	url  = re.compile("source.+?'(.+?)'").findall(link)[0]
	return url
	
	
	
def ustreamixresolve(url):
	import re,base64,requests
	html = OPEN_URL(url)
	ohtm = eval(re.findall('Obfuscator.*?var.*?(\[.*?\])',html,re.DOTALL)[0])
	oval = int(re.findall('replace.*?- (\d*)',html)[0])
	phtml = ''
	for oht in ohtm:
		phtml += chr(int(re.findall('\D*(\d*)',oht.decode('base64'))[0]) - oval)
		
		
	strurl = re.findall("var stream = '(.*?)'",phtml)[0]
	tokurl = re.findall('src="(.*?)"',phtml)[0]
	hdr = {}
	hdr['Referer'] = url
	tokpg = requests.get(tokurl,headers=hdr,verify=False).text
	token = re.findall('jdtk="(.*?)"',tokpg)[0]
	url   = strurl+token+'|referer=&User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&&X-Requested-With: ShockwaveFlash/25.0.0.171'
	return url
def mobdroresolve(url):
    import random,time,md5
    from base64 import b64encode
    url  = (url).replace('mpd://','')
    user_agent = 'Mozilla%2F5.0%20%28Linux%3B%20Android%205.1.1%3B%20Nexus%205%20Build%2FLMY48B%3B%20wv%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Version%2F4.0%20Chrome%2F43.0.2357.65%20Mobile%20Safari%2F537.36'
    token = "65rSw"+"UzRad"
    time_stamp = str(int(time.time()) + 14400)
    to_hash = "{0}{1}/hls/{2}".format(token,time_stamp,url)
    out_hash = b64encode(md5.new(to_hash).digest()).replace("+", "-").replace("/", "_").replace("=", "")
    servers = ['185.152.64.236','185.102.219.72','185.102.219.67','185.102.218.56','185.59.222.232']
    server  = random.choice(servers)
    
    url = "http://{0}/p2p/{1}?st={2}&e={3}".format(server,url,out_hash,time_stamp)
    return '{url}|User-Agent={user_agent}&referer={referer}'.format(url=url,user_agent=user_agent,referer='6d6f6264726f2e6d65'.decode('hex'))








def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString

def getTVPCookieJar(updatedUName=False):
    cookieJar=None
    print 'updatedUName',updatedUName
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(TVPCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar
	
def OPEN_URL(url):
	import requests
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
    
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    #ctx = ssl.create_default_context()
    #ctx.check_hostname = False
    #ctx.verify_mode = ssl.CERT_NONE

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)

    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Accept-Encoding','gzip')

    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;
    
def playtvplayer(url):
        import re,urllib,json
        cj=cookielib.LWPCookieJar()
        watchHtml=getUrl(url, cookieJar=cj)
        channelid=re.findall('data-resource="(.*?)"' ,watchHtml)[0]
        token=re.findall('data-token="(.*?)"' ,watchHtml)[0]
        #token='null'
        url  = "https://tvplayer.com/watch/context?resource=%s&gen=%s"%(channelid,token)
        contextjs=getUrl(url, cookieJar=cj)  
        contextjs=json.loads(contextjs)
        validate=contextjs["validate"]
        #cj = cookielib.LWPCookieJar()
        data = urllib.urlencode({'service':'1','platform':'firefox','validate':validate ,'id' : channelid})
        headers=[('Referer','http://tvplayer.com/watch/'),('Origin','http://tvplayer.com'),('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')]
        retjson=getUrl("http://api.tvplayer.com/api/v2/stream/live",post=data, headers=headers,cookieJar=cj);
        jsondata=json.loads(retjson)
  #      xbmc.Player().play(jsondata)
        url=re.compile('stream": "(.+?)"').findall(retjson)[0]
        return url+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&X-Requested-With=ShockwaveFlash/22.0.0.209&Referer=http://tvplayer.com/watch/'
		
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
	import re
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r