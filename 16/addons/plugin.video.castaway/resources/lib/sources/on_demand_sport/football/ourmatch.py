from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,urlparse,json,sys,os, json,urllib
import requests

class info():
    def __init__(self):
    	self.mode = 'ourmatch'
        self.name = 'ourmatch.net'
        self.icon = control.icon_path('ourmatch.png')
        self.paginated = True
        self.categorized = True
        self.multilink = True


class main():
	def __init__(self,url = 'http://ourmatch.net/'):
		self.base = 'http://ourmatch.net/'
		self.url = url
		

	def categories(self):
		urls = []
		img = control.icon_path(info().icon)
		out = [('http://ourmatch.net','Latest matches',img)]
		html = client.request(self.base)
		cats = re.findall('<li class=[\"\']hover-tg[\"\']><a href=[\"\'](.+?)[\"\']>(.+?)</a></li>',html)
		for c in cats:
			url = c[0]
			title = c[1]
			title = re.sub(' <span class="icon country.+?></span> ','',title)
			if url not in urls:
				out.append((url,title,img))
				urls.append(url)
		return out


	def items(self):
		out = []
		result = client.request(self.url)
		
		items = re.findall('title=[\"\']([^\"\']+)[\"\'].+?href=[\"\']([^\"\']+)[\"\']>\s*<span class="overlay"></span>\s*<img.+?src=[\"\']([^\"\']+)[\"\']',result)
		for item in items:
			title = item[0]
			url = item[1]
			img = item[2]
			out.append((title,url,img))
		

		return out

	
	def links(self, url):
		out=[]
		html = client.request(url)
		img = re.findall('"og:image" content=[\"\']([^\"\']+)[\"\']',html)[0]
		links = re.findall("src=[\"\']([^\"\']+)[\"\'].+?lang:[\"\']([^\"\']+)[\"\'].+?type[\"\']:[\"\']([^\"\']+)[\"\'].+?quality:[\"\']([^:\"\']+)[\"\'].+?source:[\"\']([^:\"\']+)[\"\']",html)
		for link in links:
			url = link[0]
			url = re.sub('data-config=.+?//config','//config',url)
			if url.startswith('//'):
				url = 'http:' + url
			title = '%s (%s, %s) - %s'%(link[2],link[1],link[3],link[4])
			out.append((title,url,img))

		return out

	def resolve(self,url):
		if '.mp4' in url:
			return url
		elif 'playwire' in url:
			from resources.lib.resolvers import playwire
			return playwire.resolve(url)
		else:
			import urlresolver
			return urlresolver.resolve(url)

	def next_page(self):
		html = client.request(self.url)
		try:
			next = re.findall('rel="next" href=[\"\']([^\"\']+)[\"\']',html)[0]
		except:
			next = None
		return next

