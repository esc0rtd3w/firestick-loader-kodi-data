from __future__ import unicode_literals
from resources.lib.modules import client, webutils,control
from resources.lib.modules.log_utils import log
import urllib, requests
import re,sys,xbmcgui,os,cookielib,time,pickle,requests

cookieFile = os.path.join(control.dataPath, 'vaughnlivecookie.lwp')


class info():
    def __init__(self):
    	self.mode = 'vaughnlive'
        self.name = 'vaughnlive.tv'
        self.icon = 'vaughnlive.jpg'
        self.paginated = False
        self.categorized = True
        self.multilink = False


class main():
	def __init__(self, url = 'http://vaughnlive.tv'):
		self.base = 'http://vaughnlive.tv'
		self.url = url


	def categories(self):
		img = control.icon_path(info().icon)
		categories = [('following','Following',img), ('all','All',img),('people','People',img),('nature','Nature',img),('creative','Creative',img),('music_cafe','Music Cafe',img),
					('news_tech','News & Tech',img),('lifestyles','Lifestyles',img),('misc','Misc',img),('espanol','Espanol',img),('vapers','Vapers',img),('breakers','Breakers',img),
					('gamers','Gamers',img)]
		return categories



	def channels(self, url):
		self.url = 'http://vaughnlive.tv/browse/%s&a=mvn&b=%s'%(url,time.time())
		if url == 'following':
			if control.setting('vaughn_user')!='' and control.setting('vaughn_password')!='':
				return self.get_followed()
			else:
				return []
		html = client.request(self.url,referer=self.base)
		channels = re.findall('href=[\"\']([^\"\']+)[\"\'] target=[\"\']_top[\"\']><img src=[\"\']([^\"\']+)[\"\']',html)
		events = self.__prepare_channels(channels)
		return events

	def get_followed(self):
		s = self.get_session()
		html = s.get('http://vaughnlive.tv/browse/following&a=following').text
		channels = re.findall('href=[\"\']([^\"\']+)[\"\'] target=[\"\']_top[\"\']><img src=[\"\']([^\"\']+)[\"\']',html)
		events = self.__prepare_channels(channels)
		return events

	def get_session(self):
		session = requests.Session()
		session.headers = {'X-Requested-With':'XMLHttpRequest', 'Referer':self.base, 'User-agent':client.agent()}
		cookies = self.load_cookies()
		if not cookies:
			log('Getting new cookies...')
			self.login(session)
			with open(cookieFile, 'wb') as f:
				pickle.dump(session.cookies, f)

			cookies = session.cookies

		session.cookies = cookies
		test = session.get(self.base).text
		if control.setting('vaughn_user') in test:
			log('Logged in !')
			return session
		else:
			log('Getting new cookies...')
			self.login(session)
			with open(cookieFile, 'wb') as f:
				pickle.dump(session.cookies, f)
			return session


	def login(self,s):

		post_data = {'u':control.setting('vaughn_user'),'p':control.setting('vaughn_password')}
		login = s.post('http://vaughnlive.tv/signin?a=process', data=post_data)


	def load_cookies(self):
		try:
			with open(cookieFile,'rb') as f:
				cookies = pickle.load(f)
				return cookies
		except:
			return False

	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			try:
				url = channel[0]
				if 'http' not in url:
					url = self.base + channel[0]
				img = 'http:' + channel[1]
				title = channel[0].split('/')[-1]
				new.append((url.replace('embed','view'),title,img))
				
			except:
				pass
		return new

	
	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)
		

	