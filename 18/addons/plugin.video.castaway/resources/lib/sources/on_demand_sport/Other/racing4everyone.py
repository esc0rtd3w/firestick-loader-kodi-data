from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
import re,urlparse,json,urllib,os,urllib2,cookielib

from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
    	self.mode = 'racing4everyone'
        self.name = 'racing4everyone.eu'
        self.icon = 'r4e.png'
        self.paginated = False
        self.categorized = True
        self.multilink = True


class main():
	
	def __init__(self,url = 'http://racing4everyone.eu/yr2016/'):
		self.base = 'http://racing4everyone.eu/'
		self.url = url
		


	def categories(self):
		out = []

		html = client.request('http://racing4everyone.eu/yr2016/')
		cats = re.findall('color: #008000;[\"\'] href=[\"\']([^\"\']+)[\"\']>([^<]+)</a></span></li>',html)
		img = control.icon_path(info().icon)
		for c in cats:
			out.append((c[0],c[1],img))
		return out

	

	def items(self):
		out = []
		urls=[]
		img = control.icon_path(info().icon)
		html = client.request(self.url)
		if html is None:
			return []
		links = webutils.bs(html).find('div',{'id':'primary'}).findAll('a')
		for l in links:
			a = re.findall('201[56]/\d\d/',l['href'])
			if len(a)!=0:
				out.append((l.getText(),l['href'],img))
		
		return out

	def links(self,url):
		out = []
		html = client.request(url)
		links = re.findall('<option value=[\"\']([^\"\']+)[\"\']>([^<]+)<',html)
		for link in links:
			out.append((link[1],convert.unescape(link[0]),control.icon_path(info().icon)))
		return out
	
	def resolve(self,url):
		try:
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
		except:
			return ''

	