from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control
import re,urlparse,json,xbmcgui, xbmc, sys
from resources.lib.modules.log_utils import log


class info():
    def __init__(self):
    	self.mode = 'nflVK'
        self.name = 'NFL on VK  (full replays)'
        self.icon = 'nfl.jpg'
        self.paginated = True
        self.categorized = True
        self.multilink = False
        self.debug = xbmc.LOGDEBUG



class main():
	def __init__(self,url = 'http://vk.com/videos-93577664?section=playlists'):
		self.base = 'http://vk.com/'
		self.url = url
		self.clientID = '5178769'

	def categories(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		tag = soup.find('div',{'class':'video_playlists_content clear_fix'})
		cats = tag.findAll('div')
		cats = self.__prepare_cats(cats)
		return cats



	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items = soup.find('div',{'id':'video_rows'}).findAll('div')
		out = []
		for item in items:
			try:
				url = self.base + item.find('a')['href']
				title = item.find('div',{'class':'video_row_info_name'}).getText().strip().replace('NFL 2015-2016 /','').encode('utf-8')
				img = re.findall("background-image: url\('(.+?)'\);",str(item))[0]
				item = (title,url,img)
				if item not in out:
					out.append(item)
			except:
				pass

		return out


	def resolve(self,url):
		import urlresolver
		return urlresolver.resolve(url)




	def next_page(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		try:
			next = soup.find('span',{'class':'page-numbers current'}).findNext('a')['href']
			log("{} | Next page: {}".format(info().mode, next), info().debug)
		except:
			log("{} | Next page not found".format(info().mode), info().debug)
			next = None
		return next


	def __prepare_cats(self,cats):
		new=[]
		for cat in cats:
			try:
				url = self.base + cat.find('a')['href']
				title = cat.getText().replace('updated',' (updated').replace('ago','ago)').encode('utf-8')
				title = title.split('Week')
				title = 'Week ' + title[1] + ' - %s'%title[0]
				img = info().icon
				item = (url,title,img)
				if item not in new:
					new.append(item)
			except:
				pass

		return new