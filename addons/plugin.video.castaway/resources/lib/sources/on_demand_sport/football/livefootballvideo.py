from __future__ import unicode_literals
from resources.lib.modules import client,webutils,control,convert
import re,urlparse,json,sys,os

class info():
    def __init__(self):
    	self.mode = 'livefootballvideo'
        self.name = 'livefootballvideo.com (highlights)'
        self.icon = control.icon_path('livefootballvideo.png')
        self.paginated = True
        self.categorized = False
        self.multilink = False


class main():
	def __init__(self,url = 'http://livefootballvideo.com/highlights'):
		self.base = 'http://livefootballvideo.com/highlights'
		self.url = url

	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items = soup.find('div',{'class':'listhighlights'}).findAll('li')
		out = []
		for item in items:
			date = convert.unescape(item.find('div',{'class':'date_time column'}).getText())
			url = item.find('div',{'class':'play_btn column'}).find('a')['href']
			home = convert.unescape(item.find('div',{'class':'team home column'}).getText())
			away = convert.unescape(item.find('div',{'class':'team column'}).getText())
			result = convert.unescape(item.find('div',{'class':'result column'}).getText())
			league = convert.unescape(item.find('div',{'class':'leaguelogo column'}).find('a')['title'])
			title  = '%s (%s) [B]%s %s %s[/B]'%(date,league,home,result,away)
			import HTMLParser
			title = HTMLParser.HTMLParser().unescape(title).encode('utf-8')
			out.append((title,url,info().icon))

		return out

	



	def resolve(self,url):
		try:
			result = client.request(url)
			html = result
			url = 'http:' + re.findall('(\/\/config\.playwire\.com\/[^\'\"]+)',html)[0]
			result = client.request(url)

			result = json.loads(result)
			try:
				f4m=result['content']['media']['f4m']
			except:
				reg=re.compile('"src":"http://(.+?).f4m"')
				f4m=re.findall(reg,html)[0]
				f4m='http://'+pom+'.f4m'

			result = client.request(f4m)
			soup = webutils.bs(result)
			try:
				base=soup.find('baseURL').getText()+'/'
			except:
				base=soup.find('baseurl').getText()+'/'

			linklist = soup.findAll('media')
			choices,links=[],[]
			for link in linklist:
				url = base + link['url']
				bitrate = link['bitrate']
				choices.append(bitrate)
				links.append(url)
				if len(links)==1:
					return links[0]
				if len(links)>1:
					import xbmcgui
					dialog = xbmcgui.Dialog()
					index = dialog.select('Select bitrate', choices)
				if index>-1:
					return links[index]
			return


		except:
			return



	def next_page(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		try:
			next = soup.find('div',{'class':'navigation'}).find('span',{'class':'current'}).findNext('a')['href']
		except:
			next = None
		return next


