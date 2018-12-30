from __future__ import unicode_literals
from resources.lib.modules import client,control
import re,sys

class info():
    def __init__(self):
    	self.mode = 'atdhe'
        self.name = 'Atdhenet.tv'
        self.icon = 'atdhe.jpg'
        self.categorized = False
        self.paginated = False
        self.multilink = False

class main():
	def __init__(self):
		self.base = 'http://goatd.net/'

	def events(self):
		html = client.request(self.base, referer=self.base)
		items1 = re.findall('colspan="(3)"><b><a href="(.+?)" title=".+?" target="_blank">(.+?)</a>', html)
		items = self.__prepare_events1(items1)
		regex='<td width=".+?" height=".+?"><img src=".*/(.+?).(?:gif|png|jpg)" width=".+?" height=".+?" /></td>\s*<td width=".+?"\s*align="left">\s*<b><a href="(.+?)" title=".+?" target="_blank">(.+?)</a></b><font style=".+?">\s*</font></td>\s*<td align="right"><b>(.+?)</b></td><td align="left"><b>.+?</b></td>'
		reg=re.compile(regex)
		events = re.findall(regex,html)
		events = self.__prepare_events(events,items)
		return events

	@staticmethod
	def convert_time(time):
		li = time.split(':')
		hour,minute=li[0],li[1]

		import datetime
		from resources.lib.modules import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
		timezona=control.setting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%H:%M"
		time=convertido.strftime(fmt)
		return time
	
	def __prepare_events(self,events,items):
		new = items
		for event in events:
			sport = event[0].title().replace('2Wges85','Champions League').replace('2Exu91G','College Basketball').replace('Hockey3','Hockey').replace('2W7Msf5','Pool').replace('A478Uu','Rugby').replace('2Zeezvn','College Football').replace('Orj96F','FOX').replace('120Grqw','CBS')
			sport = sport.replace('359Jrq0','Volleyball').replace('Tennis3','Tennis').replace('Dxmwp2','Europa League').replace('Baseball2','Baseball').replace('Rr8O07','AFL')
			url = self.base + event[1]
			title = event[2]
			time = self.convert_time(event[3])
			title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport,title)
			new.append((url,title))
		return new

	def __prepare_events1(self,events):
		new = []
		for event in events:
			url = self.base + event[1]
			title = event[2]
			title = '[B]%s[/B]'%(title)
			new.append((url,title))
		return new

	def resolve(self,url):

		import liveresolver
		return liveresolver.resolve(url,cache_timeout=0)