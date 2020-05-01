from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control,convert
import re,urlparse,os,sys,json,cookielib,urllib2,urllib,requests
from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
    	self.mode = 'livetv_nba'
        self.name = 'livetv.sx archive'
        self.icon = control.icon_path('nbastream.png')
        self.paginated = False
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = control.setting('livetv_base') + '/en/videotourney/3/'):
		self.base = control.setting('livetv_base')
		self.url = url

	def items(self):
		result = client.request(self.url)
		result = result.decode('iso-8859-1').encode('utf-8')
		items= client.parseDOM(result, "table", attrs = { "height": "27" })
		items = self.__prepare_items(items,result)
		return items

	def __prepare_items(self,items,result):
		out=[]
		for video in items:
				title = re.compile('<b>(.+?)</b>').findall(video)
				try:
					title = [i for i in title if '&ndash;' in i or '-' in i][-1]
				except:
					title = title[-1]
				title = title.split('<b>')[-1]
				title = title.replace('&ndash;', '-')
				title = convert.unescape(webutils.remove_tags(title))
				title = title.encode('utf-8')
				url = self.base + re.compile('<a.+?href="(.+?)"').findall(video)[0]
				out+=[(title,url,info().icon)]
			
			
		return out

	def links(self,url):
		out=[]
		html = client.request(url)
		soup = webutils.bs(html)
		table = soup.find('table',{'align':'center', 'width':'96%', 'cellpadding':'1','cellspacing':'1'})
		links = table.findAll('td',{'width':'33%'})
		for link in links:
			url = self.base + link.find('a')['href']
			title = link.findAll('a')[1].find('b').getText()
			img = link.find('img')['src']
			if 'highlight' not in title.lower():
				out.append((title,url,img))


		return out

	def resolve(self,url):
		ref=url
		html = client.request(url)
		soup = webutils.bs(html)
		try:
			url = soup.find('iframe',{'width':'600'})['src']
		except:
			try:
				url = 'http:' + re.findall('(\/\/config\.playwire\.com\/[^\'\"]+)',html)[0]
			except:
				try:
					url = soup.find('iframe',{'width':'626'})['src']
				except:
					return

		if 'nba' in url:
			url = url.split("playlist=")[-1]
			url = 'http://video.nba.com/videocenter/servlets/playlist?ids=%s&format=json' % url
			result = client.request(url)
			url = re.compile('"publishPoint":"(.+?)"').findall(result)[0]
			return url
		elif 'rutube' in url:
			url = re.findall('embed/(\d+)',url)[0]
			url = 'http://rutube.ru/api/play/options/'+url+'?format=json'
			result = client.request(url)
			jsx = json.loads(result)
			link = jsx['video_balancer']['m3u8']
			return link
		elif 'youtube' in url:
			import liveresolver
			return liveresolver.resolve(url)
		elif 'playwire' in url:
			try:
				result = client.request(url)
				html = result
				result = json.loads(result)
				try:
					f4m=result['content']['media']['f4m']
				except:
					reg=re.compile('"src":"http://(.+?).f4m"')
					f4m=re.findall(reg,html)[0]
					f4m='http://'+pom+'.f4m'

				result = client.request(f4m)
				soup = webutils.bs(result)
				try:
					base=soup.find('baseURL').getText()+'/'
				except:
					base=soup.find('baseurl').getText()+'/'

				linklist = soup.findAll('media')
				choices,links=[],[]
				for link in linklist:
					url = base + link['url']
					bitrate = link['bitrate']
					choices.append(bitrate)
					links.append(url)
					if len(links)==1:
						return links[0]
					if len(links)>1:
						import xbmcgui
						dialog = xbmcgui.Dialog()
						index = dialog.select('Select bitrate', choices)
					if index>-1:
						return links[index]
				return
			except:
				return

		elif 'mail.ru' in url:
			link=url

			link = link.replace('https://videoapi.my.mail.ru/videos/embed/mail/','http://videoapi.my.mail.ru/videos/mail/')
			link = link.replace('http://videoapi.my.mail.ru/videos/embed/mail/','http://videoapi.my.mail.ru/videos/mail/')
			link = link.replace('html','json')
			s = requests.Session()
			f = s.get(link).text

			js = json.loads(f)
			token = s.cookies.get_dict()['video_key']
			url = js['videos'][-1]['url'] + '|%s'%(urllib.urlencode({'Cookie':'video_key=%s'%token, 'User-Agent':client.agent(), 'Referer':ref} ))
			return url
		else:
			import urlresolver
			url = urlresolver.resolve(url)
			return url