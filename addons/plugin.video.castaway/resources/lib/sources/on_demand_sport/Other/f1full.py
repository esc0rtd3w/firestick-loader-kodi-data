from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
import re,urlparse,json,urllib,os

from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
    	self.mode = 'f1full'
        self.name = 'f1fullraces.com'
        self.icon = 'f1fr.png'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	
	def __init__(self,url = 'http://fullmatchtv.com/mlb'):
		self.base = 'http://fullmatchtv.com'
		self.url = url
		


	

	def items(self):
		out = []
		urls=[]
		html = client.request('http://f1fullraces.com/category/full-race/2016/')
		items = re.findall('<div class=[\"\']content-list-thumb[\"\']>\s*<a.+?href=[\"\']([^\"\']+)[\"\'].+?title=[\"\']([^\"\']+)[\"\']>\s*<img.+?src=[\"\']([^\"\']+)[\"\']',html)
		for item in items:
				out.append((convert.unescape(item[1]).encode('utf-8'),item[0],item[2]))		

		return out

	def links(self,url):
		out = []
		html = client.request(url)
		links = re.findall('(?:<.+?>)+([A-Z][^:<]+).+?\s*(?:.+?)?<iframe.+?src=[\"\']([^\"\']+)[\"\']',html)
		i = 1
		for link in links:
			out.append((convert.unescape(link[0]).encode('utf-8'),link[1],control.icon_path(info().icon)))
			i += 1
		return out
	
	def resolve(self,url):
		if 'google' in url:
			ch = []
			from resources.lib.modules import directstream
			res = directstream.google(url)
			for x in res:
				ch += [x['quality'].replace('HD','720p').replace('SD','480p')]

			index = control.dialog.select('Select quality:',ch)
			if index >-1:
				return res[index]['url']
		elif 'my.pcloud' in url:
			from resources.lib.resolvers import pcloud
			return pcloud.resolve(url)
		else:
			import urlresolver
			return urlresolver.resolve(url)

	def next_page(self):
		html = client.request(self.url)
		try:
			page = re.findall('<span class=[\"\']page-numbers current[\"\']>\d+</span>\s*<a class=[\"\']page-numbers[\"\'] href=[\"\']([^\"\']+)[\"\']',html)[0]
		except:
			page = False
		return page