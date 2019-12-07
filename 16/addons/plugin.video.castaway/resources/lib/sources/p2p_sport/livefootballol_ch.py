from __future__ import unicode_literals
from resources.lib.modules import client,convert,control
from resources.lib.modules.log_utils import log
import re, urllib,sys,os

AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)



class info():
    def __init__(self):
    	self.mode = 'livefootballol_ch'
        self.name = 'livefootballol.com (channels)'
        self.icon = 'livefootballol.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self,url = 'http://www.livefootballol.com/acestream-channel-list-new.html'):
		self.base = 'http://www.livefootballol.com/'
		self.url = url

	

	def channels(self):
		html = client.request(self.url, referer=self.base)
		html = convert.unescape(html.decode('utf-8'))		
		channels=re.compile('<strong>(.+?)</strong></a></td>\s*<td>(.+?)</td>\s*<td>(.+?)</td>\s*<td>(.+?)</td>').findall(html)
		events = self.__prepare_channels(channels)

		html = client.request('http://www.livefootballol.com/sopcast-channel-list.html', referer=self.base)
		html = convert.unescape(html.decode('utf-8'))

		channels=re.compile('<strong>(.+?)</strong></a></td>\s*<td>(.+?)</td>\s*<td>(.+?)</td>\s*<td>(.+?)</td>').findall(html)
		events = self.__prepare_channels(channels, ev=events)
		events.sort(key=lambda x: x[1])
		return events

	def __prepare_channels(self,channels, ev=[]):
		new=ev
		for channel in channels:
			log(channel)
			url = channel[1]
			title = channel[0].replace('AceStream','').encode('utf-8', 'xmlcharrefreplace')
			lang=channel[2].encode('utf-8', 'xmlcharrefreplace')
			bitrate = channel[3]
			title = '%s [%s] - %s kbps'%(title.decode('utf-8'),lang,bitrate)
			new.append((url,title.encode('utf-8'),icon_path(info().icon)))
		return new

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)