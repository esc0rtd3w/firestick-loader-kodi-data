from __future__ import unicode_literals
from resources.lib.modules import client,webutils, control
import re,urlparse, os, xbmcvfs, urllib, urllib2

torrent_path = os.path.join(control.dataPath, 'myTorrent.torrent')

class info():
    def __init__(self):
    	self.mode = 'torrent_afl'
        self.name = 'AFL/Gaellic football torrents (full replays)'
        self.icon = 'torrent.png'
        self.paginated = True
        self.categorized = False
        self.multilink = False


class main():
	def __init__(self,url = 'http://www.sport-video.org.ua/afl.html'):
		self.base = 'http://www.sport-video.org.ua/'
		self.url = url

	def items(self):
		html = client.request(self.url)
		out=[]
		items = reversed(re.findall("javascript\:popupwnd\([\"\']([^\"\']+)[\"\'],.+?target=[\"\']_self[\"\'] title=[\"\']([^\"\']+)[\"\']><img src=[\"\']([^\"\']+)[\"\'].+?style3.>([^<]+)",  html, flags=re.DOTALL))
		for i in items:
				title = i[3]
				url = i[0].replace('./',self.base + '/').replace('0.html','.html')
				img = self.base + i[2]
				out+=[[title,url,img]]

		return out

	
	def resolve(self,url):
		html = client.request(url)
		url = urllib.quote(re.findall('a href=[\"\'](.+?.torrent)[\"\']',html)[0])
		url = self.base + url[1:]
		from resources.lib.resolvers import torrent
		return torrent.resolve(url)




	def next_page(self):
		try:
			page = re.findall('afl(\d+).html',self.url)[0]
			next_page = self.url.replace('afl%s.html'%(page),'afl%s.html'%(int(page)+1))
		except:
			next_page = self.url.replace('afl.html','afl1.html')
		return next_page


