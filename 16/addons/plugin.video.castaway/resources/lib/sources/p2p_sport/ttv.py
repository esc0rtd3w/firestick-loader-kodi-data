# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.modules import client,control
import re,sys,xbmcgui,os,json


AddonPath = control.addonPath
IconPath = AddonPath + "/resources/media/"
def icon_path(filename):
    return os.path.join(IconPath, filename)

class info():
    def __init__(self):
    	self.mode = 'ttv'
    	self.name = 'Torrent-TV.ru'
    	self.icon = icon_path('ttv.png')
    	self.paginated = False
    	self.categorized = True
    	self.multilink = False

class main():
	def __init__(self,url = 'http://super-pomoyka.us.to/trash/ttv-list/ttv.json'):
		self.base = 'acestream://'
		self.url = url
		self.dict_torrent = {}
		self.html = client.request(self.url)
		
	def categories(self):
		cats = [('Music','Музыка'),('General','Общие'),('News','Новостные'),('Educational','Познавательные'),('Entertainment','Развлекательные'),('Regional','Региональные'),
				('Men', 'Мужские'),('Adult' ,'Для взрослых'),('Kids','Детские'), ('Movies', 'Фильмы'),('Religious','Религиозные'),('.Sport','Спорт')]
		out=[]
		for cat in cats:
			url = cat[1]
			out.append((url,cat[0],info().icon))
		out.sort(key=lambda x: x[1])
		return out


	def channels(self,url):
		url = url.decode('utf-8')
		self.html = self.html.decode('utf-8')
		ms = re.compile('\"name\":\"(.+?)\",\"url\":\"(.+?)\",\"cat\":\"%s\"'%url,re.U).findall(self.html)
		events = []
		for ch in ms:
			title = ch[0].encode('utf-8')
			url = self.base + ch[1]
			events.append((url,title,info().icon))
		events.sort(key=lambda x: x[1])
		return events

	
	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)