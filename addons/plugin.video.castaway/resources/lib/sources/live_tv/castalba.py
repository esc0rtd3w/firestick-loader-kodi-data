from __future__ import unicode_literals
from resources.lib.modules import client
import re


class info():
    def __init__(self):
    	self.mode = 'castalba'
        self.name = 'Castalba.tv'
        self.icon = 'castalba.jpg'
        self.paginated = True
        self.categorized = True
        self.multilink = False
class main():
	def __init__(self,url = 'http://castalba.tv/channels'):
		self.base = 'http://castalba.tv/channels'
		self.url = url

	def categories(self):
		cats = ['Animals', 'Entertainment', 'Gaming', 'Lifecasting', 'Music', 'News', 'Sports', 'Webcams', 'Other']
		out = [('http://castalba.tv/channels','All',info().icon)]
		for cat in cats:
			ch = cat.lower()
			url = 'http://castalba.tv/channels/c=%s'%(ch)
			out.append((url,cat,info().icon))
		return out

	def channels(self,url):
		self.url = url
		html = client.request(url, referer=self.base)
		regex='<img src="(.+?)" alt=""/>\s*<span class="time">Live</span>\s*</a>\s*<a href="(.+?)" class="addtoplaylist"><img src=".+?" alt=""/></a>\s*</div>\s*<div class="clear"></div>\s*<h4><a class=".+?" href=".+?">(.+?)</a>'
		channels=re.compile(regex).findall(html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = channel[1].replace('../','http://castalba.tv/')
			img = channel[0].replace('../','http://castalba.tv/')
			title = channel[2]
			new.append((url,title,img))
		return new

	def next_page(self):
		try:
			page = int(re.compile('p=(\d+)').findall(self.url)[0])
			page = self.url.replace('p=%s'%page, 'p=%s'%(page+1))
		except:
			page = self.url + '/p=2'
		
		try:
			html = client.request(page, referer=self.base)
			if html:
				return page
			return
		except:
			return

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)
