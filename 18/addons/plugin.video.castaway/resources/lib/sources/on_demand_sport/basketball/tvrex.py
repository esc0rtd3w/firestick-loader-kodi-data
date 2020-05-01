from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,demand_links
import re,urlparse,sys,urllib,urllib2,cookielib,json,os
from resources.lib.modules.log_utils import log




class info():
    def __init__(self):
    	self.mode = 'tvrex'
        self.name = 'tvrex.net (full replays)'
        self.icon = 'tvrex.jpg'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://tvrex.net/'):
		self.base = 'http://tvrex.net/'
		self.url = url

	def items(self):
		html = client.request(self.url)
		items = re.findall('<div class="post-img">\s*<a href="(.+?)">\s*<img.+?data-hidpi="(.+?)" alt="(.+?)"',html)
		out=[]
		for item in items:
			url = item[0]
			title=item[2]
			thumb=item[1]

			out+=[[title,url,thumb]]
		out.pop(0)
		return out

	def links(self,url, img=' '):
		links = demand_links.links(url,self.base,img,info().icon)
		return links




	def resolve(self,url):
		return demand_links.resolve(url)




	def next_page(self):
		html = client.request(self.url)
		try:
			next_page=re.findall("class='current'>.+?</span><a href=\'(.+?)\'",html)[0]
		except:
			next_page=None
		return next_page


