from resources.lib.modules import client,webutils,control
import sys,os

class info():
    def __init__(self):
    	self.mode = 'sportx'
        self.name = 'sports-x.net'
        self.icon = 'sportx.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False


class main():
	def __init__(self):
		self.base = 'http://www.sports-x.net/'

	def channels(self):
		html = client.request(self.base)
		matches = webutils.bs(html).findAll('div',{'class':'match'})
		match_infos = webutils.bs(html).findAll('div',{'class':'match_info'})
		events = self.__prepare_schedule(matches,match_infos)

		html = client.request('http://www.sports-x.net/index.phplivetv', referer=self.base)
		channels = webutils.bs(html).find('article',{'class':'main'}).findAll('a')
		events += self.__prepare_channels(channels)
		return events

	def __prepare_channels(self,channels):
		new=[]
		urls=[]
		for channel in channels:
			url = channel['href']
			title = channel.getText()
			if url not in urls:
				urls.append(url)
				new.append((url,title,control.icon_path(info().icon)))
		#new.pop(-1)
		return new

	def __prepare_schedule(self,matches,match_infos):
		new = []
		urls=[]
		for i in range(len(matches)):
			match = matches[i]
			time = match.find('div',{'style':'float:left;padding-top:1px;'}).getText()
			time = self.convert_time(time)
			title = match.find('div',{'style':'float:left;padding-top:1px;padding-left:10px;'}).getText()
			infs = match_infos[i].findAll('div',{'style':'margin-top: -2px;'})
			urls = match_infos[i].findAll('a')
			for i in range(len(infs)):
				inf = infs[i].getText()
				url = self.base + urls[i]['href']
				titl = '[COLOR orange](%s)[/COLOR] %s - %s'%(time,title,inf)
				if url not in urls:
					new.append((url,titl.encode('utf-8'),control.icon_path(info().icon)))
					urls.append(url)
		return new

	@staticmethod
	def convert_time(time):
		li = time.split(':')
		hour,minute=li[0],li[1]

		import datetime
		from resources.lib.modules import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
		timezona= control.setting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%H:%M"
		time=convertido.strftime(fmt)
		return time

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)