from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control
from resources.lib.modules.log_utils import log
import re


class info():
    def __init__(self):
    	self.mode = 'streamhd'
        self.name = 'streamhd.eu'
        self.icon = 'streamhd.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False

class main():
	def __init__(self):
		self.base = 'http://www.streamhd.eu'

	def channels(self):
		html = client.request('http://www.streamhd.eu/tv/')
		channels = re.findall('<a href=[\"\'](/[^\"\']+)[\"\']>	<img.+?alt=[\"\'](.+?)\s*Live Stream[\"\'].+?src=[\"\']data:image/png;base64',html)
		out = self.__prepare_channels(channels)
		html = client.request(self.base)
		html = client.request(self.base)
		soup = webutils.bs(html)
		rows = soup.find('table',{'class':'table table-hover table-condensed table-striped'}).find('tbody').findAll('tr')
		for row in rows:
			tds = row.findAll('td')
			time = self.convert_time(tds[0].getText().replace('GMT','').strip())
			sport = tds[1].getText().strip()
			sub = tds[3].getText().strip()
			match = tds[4].getText().strip()
			url = self.base + tds[4].findAll('a')[0]['href']
			if sport!=sub:
				sport += '-%s'%sub

			title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,match)
			out.append((url,title,control.icon_path(info().icon)))
		
		return out

	@staticmethod
	def convert_time(time):
		li = time.split(':')
		hour,minute=li[0],li[1]

		import datetime
		from resources.lib.modules import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('Europe/London'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
		timezona = control.setting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%H:%M"
		time=convertido.strftime(fmt)
		return time

	def __prepare_channels(self,channels):
		new=[]
		urls=[]
		img = control.icon_path(info().icon)
		for channel in channels:
			url = self.base + channel[0]
			title = channel[1]
			if url not in urls:
				new.append((url,title,img))
				urls.append(url)
		return new


	def __prepare_events(self,events):
		new = []
		img = ''
		for e in events:
			url = self.base + e[3]
			time = self.convert_time(e[0])
			sport = e[1]
			if e[2].strip() != e[1].strip():
				sport += ' - %s'%e[2]

			match = e[4]

			title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,match)
			new.append((url,title,img))

		return new


	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)