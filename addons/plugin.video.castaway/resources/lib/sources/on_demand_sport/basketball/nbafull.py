from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,demand_links,control
import re,urlparse,urllib,sys,os,urllib2,json,cookielib
from resources.lib.modules.log_utils import log


class info():
    def __init__(self):
    	self.mode = 'nbafull'
        self.name = 'nbafull.com (full replays)'
        self.icon = 'nbafull.png'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://nbafull.com'):
		self.base = 'http://nbafull.com'
		self.url = url

	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items=soup.findAll('div',{'class':'thumb'})
		out=[]
		for item in items:
			url = item.find('a')['href']
			title=item.find('a')['title'].encode('utf-8')
			title = re.sub('<[^>]*>','',title)
			out+=[[title,url,control.icon_path(info().icon)]]

		return out

	def links(self,url, img=' '):
		links = demand_links.links(url,self.base,img,info().icon)
		return links




	def resolve(self,url):
		return demand_links.resolve(url)




	def next_page(self):

		html = client.request(self.url)
		try:
			next_page=re.findall('<a.+?rel="next".+?href="(.+?)"',html)[0]
			if 'nbafull.com' not in next_page:
				next_page = self.base + next_page
		except:
			next_page=None
		return next_page


