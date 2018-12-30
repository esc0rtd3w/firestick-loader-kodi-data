from __future__ import unicode_literals
from resources.lib.modules import client
import re,base64
from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
    	self.mode = 'zoptv'
        self.name = 'zoptv.com'
        self.icon = 'zoptv.png'
        self.paginated = False
        self.categorized = True
        self.multilink = False
class main():
	def __init__(self,url = 'http://www.zoptv.com/'):
		self.base = 'http://www.zoptv.com'
		self.url = url
		
       


	def categories(self):
		out = []
		urls = []
		html = client.request(self.base)
		cats = re.findall('href=[\"\'](/channels[^\"\']+)[\"\']>([^<]+)<',html)
		for cat in cats:
			url = self.base + cat[0]
			title = cat[1]
			if url not in urls and title.strip()!='':
				out.append((url,title,info().icon))
				urls.append(url)
		return out

	def channels(self,url):
		self.url = url
		html = client.request(url, referer=self.base)
		regex='zp-channel.+?href=[\"\']([^\"\']+)[\"\']>\s*<img src=[\"\']([^\"\']+)[\"\']>\s*<span>([^<]+)<'
		channels=re.compile(regex).findall(html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = self.base + channel[0]
			img = self.base + channel[1]
			title = channel[2].encode('utf-8')
			new.append((url,title,img))
		return new

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)
