from resources.lib.modules import client,webutils,control
import sys,os,cookielib,urllib2,re,urllib,json

from resources.lib.modules.log_utils import log


class info():
    def __init__(self):
    	self.mode = 'ustvnow'
        self.name = 'ustvnow.com'
        self.icon = 'ustvnow.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False


class main():
	def __init__(self):
		self.base = 'http://mc.ustvnow.com/'
		self.premium = control.setting('ustvnow_show_premium') == 'true'

	def channels(self):
		token = self.get_token()
		result = 'http://m-api.ustvnow.com/gtv/1/live/playingnow?token=%s' % token
		channels = json.loads(client.request(result))['results']
		channels = self.__prepare_channels(channels)
		return channels

	def __prepare_channels(self,channels):
		new=[]
		free = ['whtm', 'whp', 'wlyh', 'wpmt', 'wgal', 'wpsu', 'whvl']
		for channel in channels:
			try:
				img = self.base + channel['img']
				log(img)
				code = channel['scode']
				url = 'http://www.ustvnow.com/?scode=' + code.lower()
				show = channel['title']
				name = channel['stream_code']
				title = '%s - %s'%(name,show)
				if code.lower() in free: pass
				else: 
					if not self.premium: continue

				new.append((url,title,img))

			except:
				pass
		return new



	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url, cache_timeout=0)

	def get_token(self):
		user, password = control.setting('ustvnow_email'), control.setting('ustvnow_pass')
		token = urllib.urlencode({'username': user, 'password': password})
		token = 'http://m-api.ustvnow.com/gtv/1/live/login?%s&device=gtv&redir=0' % token
		token = json.loads(client.request(token))['token']
		return token