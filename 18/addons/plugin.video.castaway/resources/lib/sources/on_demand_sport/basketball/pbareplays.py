from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,demand_links,control
import re,urlparse,urllib,sys,os,urllib2,json,cookielib
from resources.lib.modules.log_utils import log


class info():
    def __init__(self):
    	self.mode = 'pbareplays'
        self.name = 'pbafullreplays.com (full replays)'
        self.icon = 'pbareplays.png'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://www.pbafullgamesreplay.com'):
		self.base = 'http://www.pbafullgamesreplay.com/'
		self.url = url

	def items(self):
		html = client.request(self.url)
		html = convert.unescape(html.decode('utf-8'))
		items= re.findall('<a class=[\"\']cvp-ctr-track[\"\'].+?href=[\"\'](.+?)[\"\'] title=[\"\'](.+?)[\"\']\s*>\s*<img src=[\"\'](.+?)[\"\']',html)
		out=[]
		for item in items:
			url = item[0]
			title=item[1].replace('-Full Game Replay-','-').replace('Full Game Replay HD Quality','-').replace('Replay HD Quality','-')
			img = item[2]
			out+=[[title.encode('utf-8'),url,img]]

		return out

	def links(self,url, img=' '):
		links = demand_links.links(url,self.base,img,info().icon)
		return links




	def resolve(self,url):
		return demand_links.resolve(url)




	def next_page(self):
		html = client.request(self.url)
		try:
			next_page=re.findall("current[\"\']>.+?</span>\s*<a.+?href=[\"\']([^\"\']+)[\"\']",html)[0]
		except:
			next_page=None
		return next_page


