from __future__ import unicode_literals
from resources.lib.modules import client, webutils,control
from resources.lib.modules.log_utils import log
import urllib, requests
import re,sys,xbmcgui,os,cookielib

cookieFile = os.path.join(control.dataPath, 'streamlivecookie.lwp')


class info():
    def __init__(self):
    	self.mode = 'streamlive'
        self.name = 'Streamlive.to'
        self.icon = 'streamlive.png'
        self.paginated = True
        self.categorized = True
        self.multilink= False


class main():
	def __init__(self, url = 'http://www.streamlive.to/channels/?sort=1'):
		self.base = 'http://www.streamlive.to/'
		self.url = url
		self.favourites_url = 'http://www.streamlive.to/channels_favorite'


	def categories(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items = soup.find('select', {'name':'category'}).findAll('option')
		ic = info().icon
		cats = [('#schedule','Schedule',ic)]
		for item in items:
			name = item['value']
			url = self.base + urllib.quote(name)
			if name =='': name = 'All'
			cats.append((url, name, ic))
		return cats


	@staticmethod
	def convert_time(time):
		pm  = False
		if 'pm' in time.lower():
			pm = True
		time = time.upper().replace('AM','').replace('PM','').strip()
		li = time.split(':')
		hour,minute=int(li[0]),int(li[1])
		if hour == 12 and not pm:
			hour = 0
		if pm and hour!=12:
			hour += 12


		import datetime
		from resources.lib.modules import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('America/Detroit'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
		timezona= control.setting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%H:%M"
		time=convertido.strftime(fmt)
		return time

	def channels(self, url):
		if url == '#schedule':
			self.url = url
			return self.schedule()
		elif url == '#favourites':
			self.url = self.favourites_url
			return self.favourites()
		self.url = url.replace(' ','%20')
		html = client.request(self.url,referer=self.base)
		channels = webutils.bs(html).findAll('li')
		events = self.__prepare_channels(channels)
		return events


	def sch_dict(self):
		sch = []
		html = client.request(self.base)
		events = client.parseDOM(html,'div', attrs={'id':'single-sport'})
		for event in events:
			title = re.findall('^\s*([^<]+)',event)[0]
			date = re.findall('(\([^\)]+\))',title)[0]
			urls = event.replace(title,'')
			title = title.replace(date,'')
			orig_time = re.findall('(\d\d:\d\d (?:AM|PM))',title)[0]
			time = self.convert_time(orig_time)
			time = '[COLOR orange](%s)[/COLOR]'%time
			title = title.replace(orig_time,time).replace(': ',' ')
			sch.append((title,urls))
		return sch


	def schedule(self):
		out = []
		html = client.request(self.base)
		sch = self.sch_dict()
		for s in sch:
			out.append((s[0].replace('embed','view'),s[0],control.icon_path(info().icon)))

		return out

	def sch_links(self,key):
		dicty = dict(self.sch_dict())
		urls = dicty[key]
		choices = []
		links = re.findall('href=[\"\']([^\"\']+)[\"\'].+?>([^<]+)<',urls)
		for link in links:
			choices.append(link[1])

		index = control.selectDialog(choices,heading='Choose the source')
		if index>-1:
			return links[index][0]
		return ''


	def __prepare_channels(self,channels):
		new=[]
		for channel in channels:
			try:
				url = channel.find('a')['href']
				img = 'http:' + re.findall('img.+?src="(.+?)"',str(channel.find('img')))[0]
				title = channel.find('img')['alt'].encode('utf-8')
				if 'premium' in channel.getText().lower() and control.setting('streamlive_show_premium')=='false':
					continue
				else:
					new.append((url.replace('embed','view'),title,img))
				
			except:
				pass
		return new

	def next_page(self):
		
		try: 
			html = client.request(self.url, headers={'referer':self.base})
			next = re.compile('>\s\d+\s<a href="(.+?)">').findall(html)[0]
			return next
		except:
			return None

	def resolve(self,url):
		if 'http' not in url:
			url = self.sch_links(url)
			if url=='':
				return url

		import liveresolver
		return liveresolver.resolve(url)
		