from __future__ import unicode_literals
from resources.lib.modules import client
import re


class info():
    def __init__(self):
    	self.mode = 'zerocast'
        self.name = 'zerocast.tv'
        self.icon = 'zerocast.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self):
		self.base = 'http://zerocast.tv/channels/'

	def channels(self):
		html = client.request(self.base, referer=self.base)
		regex='<a href="http://www\.zerocast\.tv/channels/chan\.php\?chan=([^"]+)">\s*<img src="(.+?)".*\s*.*src="(.+?)"'
		reg=re.compile(regex)
		channels = re.findall(regex,html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:

			img = 'http://zerocast.tv/channels/' + channel[1].replace('./','')
			url = channel[2]
			title = channel[0].upper()
			new.append((url,title,img))
		return new



	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)