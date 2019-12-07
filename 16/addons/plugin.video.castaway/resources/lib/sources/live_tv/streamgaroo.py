from __future__ import unicode_literals
from resources.lib.modules import client, webutils,control,convert,constants
from resources.lib.modules.log_utils import log
import urllib, requests
import re,sys,xbmcgui,os,cookielib,time,requests,json

cookieFile = os.path.join(control.dataPath, 'vaughnlivecookie.lwp')


class info():
    def __init__(self):
    	self.mode = 'streamgaroo'
        self.name = 'streamgaroo.com'
        self.icon = 'streamgaroo.png'
        self.paginated = False
        self.categorized = True
        self.multilink = True


class main():
	def __init__(self, url = 'http://www.streamgaroo.com/live-television'):
		self.base = 'http://www.streamgaroo.com'
		self.url = url



	def categories(self):
		out = []
		img = control.icon_path(info().icon)
		s = requests.Session()
		html = s.get('http://www.streamgaroo.com/live-television/').text
		cats = re.findall('href=[\"\']([^\"\']+)[\"\']><img.+?alt=[\"\']([^\"\']+)[\"\']>',html)
		for c in cats:
			out.append((c[0],c[1],img))
			if c[1]=='United States':
				break
		return out

	def channels(self,url):
		out = []
		s = requests.Session()
		html = s.get(url).text
		channels = re.findall('data-clk=[\"\']([^\"\']+)[\"\'].+?title=[\"\']([^\"\']+)[\"\'].+?img.+?src=[\"\']([^\"\']+)[\"\']',html)
		a = urllib.unquote(re.findall('data-a=[\"\']([^\"\']+)[\"\']',html)[0])
		s.headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Host':'www.streamgaroo.com','Referer':url,'X-Requested-With' : 'XMLHttpRequest'}
		resp = json.loads(s.post('http://www.streamgaroo.com/calls/get/more_streams', data={'p':a}).text)
		data = resp['data']
		channels += re.findall('data-clk=[\"\']([^\"\']+)[\"\'].+?title=[\"\']([^\"\']+)[\"\'].+?img.+?src=[\"\']([^\"\']+)[\"\']',data)
		newa = urllib.unquote(resp['newa'])
		while True:
			if int(resp['count'])==0:
				break
			resp = json.loads(s.post('http://www.streamgaroo.com/calls/get/more_streams', data={'p':newa}).text)
			data = resp['data']
			channels += re.findall('data-clk=[\"\']([^\"\']+)[\"\'].+?title=[\"\']([^\"\']+)[\"\'].+?img.+?src=[\"\']([^\"\']+)[\"\']',data)
			newa = urllib.unquote(resp['newa'])

		for c in channels:
			url = urllib.unquote(c[0])
			title = c[1]
			img = c[2]
			out.append((url,title,img))
		return out


	def links(self,urlx):
		s = requests.Session()
		html = s.get(urlx).text
		urls = re.findall('stream-box-sources-list-item.+?data-status=[\"\']approved[\"\'].+?data-h=[\"\']([^\"\']+)[\"\']',html)
		i = 0
		out = []
		for u in urls:
			url = urlx + '##' + u
			i += 1
			out.append((url,'Stream %s'%i))
		return out
	def resolve(self,url):
		try:
			referer,id = url.split('##')
			s = requests.Session()
			s.headers = {'Accept':'application/json, text/javascript, */*; q=0.01','Host':'www.streamgaroo.com','Referer':referer,'X-Requested-With' : 'XMLHttpRequest'}
			html = s.post('http://www.streamgaroo.com/calls/get/source',data={'h':urllib.unquote(id)}).text
			s.headers = ({'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Host':'www.streamgaroo.com','Referer':referer, 'Accept-Encoding':'gzip, deflate, lzma, sdch'})
			link = json.loads(html)['link']
			html = s.get(link).text
			
			#hls
			try:
				url = re.findall('playStream\(.+?,.((?:http|rtmp)[^\"\']+)',html)[0]
				if 'rtmp' in url:
					return url 
				else:
					return url + '|%s' %urllib.urlencode({'X-Requested-With':constants.get_shockwave(),'Referer':link,'User-agent':client.agent()})
			except:	pass

			#everything else
			import liveresolver
			return liveresolver.resolve(link,html=html)
		except:
			control.infoDialog('No stream available!')
			return ''
		

	