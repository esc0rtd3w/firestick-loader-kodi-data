from __future__ import unicode_literals
from resources.lib.modules import client
import re, urllib


class info():
    def __init__(self):
    	self.mode = 'serbiaplus'
        self.name = 'serbiaplus.club'
        self.icon = 'serbiaplus.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self,url = 'http://www.singi.club/menu2.html'):
		self.base = 'http://www.singi.club/'
		self.url = url

	

	def channels(self):
		html = client.request(self.url, referer=self.base)
		channels=re.compile('<a href="(.+?)" target="_blank"><img src="(images/(.+?).(?:jpg|gif|png))".+?></a></div>').findall(html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			url = self.base + channel[0]
			img = self.base + urllib.quote(channel[1])
			title = channel[2].replace('ACE','')
			new.append((url,title,img))
		return new

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)
