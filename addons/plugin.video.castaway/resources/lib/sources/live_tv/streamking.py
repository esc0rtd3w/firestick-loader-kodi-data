from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control
from resources.lib.modules.log_utils import log
import re,os


class info():
    def __init__(self):
    	self.mode = 'streamking'
        self.name = 'streamking.cc'
        self.icon = 'streamking.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
	def __init__(self):
		self.base = 'http://streamking.cc'

	def channels(self):
		html = client.request(self.base)
		channels = re.findall('tv-block[\"\']>\s*<a href=[\"\']([^\"\']+)[\"\']><img.+?src=[\"\']([^\"\']+)[\"\'].+?alt=[\"\']([^\"\']+)[\"\']',html)
		events = self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		urls=[]
		for channel in channels:
			url = self.base + channel[0]
			
			title = channel[2]
			img = self.base + channel[1]
			if url not in urls:
				new.append((url,title,img))
				urls.append(url)
		return new



	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)