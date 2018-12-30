from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control
import re,urlparse,json,sys,os
from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
    	self.mode = 'livefootballvideo_fm'
        self.name = 'livefootballvideo.com (full matches)'
        self.icon = control.icon_path('livefootballvideo.png')
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://livefootballvideo.com/fullmatch'):
		self.base = 'http://livefootballvideo.com/fullmatch'
		self.url = url

	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items = soup.find('div',{'id':'archive'}).findAll('li')
		out = []
		for item in items:
			try:
				title = item.find('div',{'class':'cover'}).find('a')['title']
				url = item.find('div',{'class':'cover'}).find('a')['href']
				img = item.find('div',{'class':'cover'}).find('img')['src']
				out.append((title,url,img))
			except:
				pass

		return out

	

	def links(self,url):
		out=[]
		html = client.request(url)
		urls = re.findall('(\/\/config\.playwire\.com\/[^\'\"]+)',html)
		for link in urls:
			url = 'http:' + link
			hm = client.request(url)
			title = re.findall('"title"\s*:\s*"(.+?)"',hm)[0]
			img = re.findall('"poster"\s*:\s*"(.+?)"',hm)[0]
			out.append((title,url,img))
		return out

	def resolve(self,url):
		try:
			
			result = client.request(url)

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



	def next_page(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		try:
			next = soup.find('div',{'class':'navigation'}).find('span',{'class':'current'}).findNext('a')['href']
		except:
			next = None
		return next


