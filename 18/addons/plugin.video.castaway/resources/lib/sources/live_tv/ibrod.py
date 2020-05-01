from __future__ import unicode_literals
from resources.lib.modules import client, webutils, convert, control
from BeautifulSoup import BeautifulSoup as bs
import re,sys,xbmcgui,os



class info():
    def __init__(self):
    	self.mode = 'ibrod'
        self.name = 'iBrod.tv'
        self.icon = 'ibrod.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False
class main():
	def __init__(self):
		self.base = 'http://www.ibrod.tv'

	def channels(self):
		soup = webutils.get_soup(self.base)
		headers = soup.findAll('a',{'class':'menuitem submenuheader'})
		headers.pop(0)
		items = soup.findAll('div',{'class':'submenu'})
		items.pop(0)
		events = self.__prepare_channels(headers,items)

		return events

	def __prepare_channels(self,headers,items):
		new=[]
		i = 0
		for header in headers:
			if header.getText()=='LIVE EVENTS':
				new = self.__get_schedule(new)
				i+=1
				continue
			new.append(('x','[COLOR yellow]%s[/COLOR]'%header.getText(),control.icon_path(info().icon)))
			channels = items[i].findAll('li')
			for channel in channels:
				url = self.base + '/' + channel.find('a')['href']
				title = channel.getText()
				new.append((url,title,control.icon_path(info().icon)))
			i+=1
		return new

	def __get_schedule(self,list):
		new = []
		new.append(('x','[COLOR yellow]LIVE EVENTS[/COLOR]',control.icon_path(info().icon)))
		html = client.request('http://www.ibrodtv.net/load.php')
		html = convert.unescape(html.decode('cp1252'))
		items = re.findall('class=[\"\']t[\"\']>(.+?)</span></div>\s*<div class=[\"\']name[\"\']>(.+?)</div>\s*<a href=[\"\'](.+?)[\"\']>',html)
		for item in items:
			title = item[1]
			url = item[2]
			time = self.convert_time(item[0])
			title = '[COLOR orange](%s)[/COLOR] [B]%s[/B]'%(time,title)
			new.append((url,title.encode('utf-8', 'xmlcharrefreplace'),control.icon_path(info().icon)))
		list = new+list
		return list

	@staticmethod
	def convert_time(time):
		li = time.split(':')
		hour,minute=li[0],li[1]

		import datetime
		from resources.lib.modules import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('Europe/Minsk'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
		timezona= control.setting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%H:%M"
		time=convertido.strftime(fmt)
		return time

	def resolve(self,url):
		import liveresolver
		return liveresolver.resolve(url)


