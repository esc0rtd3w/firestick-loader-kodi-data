from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
import re,sys
from resources.lib.modules.log_utils import log

class info():
    def __init__(self):
    	self.mode = 'laola1'
        self.name = 'laola1.tv'
        self.icon = 'laola1.png'
        self.categorized = False
        self.paginated = False
        self.multilink = False

class main():
	def __init__(self):
		self.base = 'http://www.laola1.tv/'

	def events(self):
		html = client.request('http://www.laola1.tv/en-int/live-schedule', referer=self.base)
		html = convert.unescape(html.decode('utf-8'))
		soup = webutils.bs(html)
		import datetime
		now = datetime.datetime.now()
		cl = 'list list-day day-%s-%02d-%02d'%(now.year,int(now.month),int(now.day))
		section = str(soup.find('ul',{'class':cl}))
		events = re.findall('<img.+?src=[\"\']([^\"\']+)[\"\'].+\s*.+\s*.+\s*<a.+?href=[\"\']([^\"\']+)[\"\'].+\s*<h3>([^<]+)<.+\s*<h2>([^<]+)<.+\s*.+\s*.+\s*.+\s*.+\s*.+data-streamstart=[\"\']([^\"\']+)[\"\']',section)
		events = self.__prepare_events(events)
		return events
	@staticmethod
	def convert_time(time):
		

		import datetime
		from resources.lib.modules import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('Europe/Ljubljana'))).localize(datetime.datetime.fromtimestamp(float(time)))
		timezona= control.setting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%H:%M"
		time=convertido.strftime(fmt)
		return time
	
	def __prepare_events(self,events):
		new = []
		for event in events:
			img = 'http:' + event[0]
			url = self.base + event[1]
			sport = event [2]
			title = event[3]
			time = self.convert_time(event[4])
			title = '[COLOR orange](%s)[/COLOR] (%s) [B]%s[/B]'%(time,sport.decode('ascii','ignore'),title.decode('ascii','ignore'))
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