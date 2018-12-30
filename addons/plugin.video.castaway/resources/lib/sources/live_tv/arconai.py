from __future__ import unicode_literals
from resources.lib.modules import client, webutils,control,convert,constants
from resources.lib.modules.log_utils import log
import urllib, requests
import re,sys,xbmcgui,os,cookielib,time,pickle,requests

cookieFile = os.path.join(control.dataPath, 'vaughnlivecookie.lwp')


class info():
    def __init__(self):
    	self.mode = 'arconai'
        self.name = 'arconaitv.me'
        self.icon = 'arconai.png'
        self.paginated = False
        self.categorized = True
        self.multilink = False


class main():
	def __init__(self, url = 'http://af-proxy.appspot.com/arconaitv.me'):
		self.base = 'http://af-proxy.appspot.com'
		self.real = 'https://www.arconaitv.me'
		self.url = url

	def categories(self):
		img = control.icon_path(info().icon)
		cats = (('0','Shows',img),('1','Live TV',img),('2','Movies',img))
		return cats

	def channels(self,index):
		index = int(index)
		img = control.icon_path(info().icon)
		events = []
		html = client.request('http://af-proxy.appspot.com/arconaitv.me')
		lis = webutils.bs(html).findAll('ul',{'id':'mega_main_menu_ul'})[0]
		lis = lis.findNext('li')
		if index > 0:
			lis = lis.findNextSibling('li')
		if index > 1:
			lis = lis.findNextSibling('li')
		lis = lis.findAll('a')
		for li in lis:
			if li.getText()[1] != '-' :
				events.append((li['href'],li.getText(),img))
		events.sort(key=lambda x: x[1])
		return events

	

	
	def resolve(self,url):
		try:
			url = self.base + url
			html = client.request(url)
			url = 'http:/' + re.findall('src=[\"\']([^\"\']+)[\"\'].+?mpeg',html)[0]
			url += '|%s' % urllib.urlencode({'X-Requested-With':constants.get_shockwave(),'User-agent':client.agent()})
			return url
		except:
			return url
		

	