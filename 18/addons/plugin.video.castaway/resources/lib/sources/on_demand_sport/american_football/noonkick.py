from __future__ import unicode_literals
from resources.lib.modules import client,webutils
import re,urlparse,json



class info():
    def __init__(self):
    	self.mode = 'noonkick'
        self.name = 'noonkick.com (CFL)'
        self.icon = 'noonkick.png'
        self.paginated = True
        self.categorized = False
        self.multilink = False


class main():
	def __init__(self,url = 'http://noonkick.com/browse/'):
		self.base = 'http://noonkick.com'
		self.url = url

	def items(self):
		html = client.request(self.url)
		items = re.findall('<a class="clip-link" data-id=".+?" title="(.+?)" href="(.+?)">\s*<span class="clip">\s*<img src="(.+?)"',html)
		out = []
		for item in items:
			url = item[1]
			title = item[0]
			img = 'http:'+item[2]
			out.append((title,url,img))

		return out

	def resolve(self,url):
		html = client.request(url)
		url = re.findall('(?:\'|\")(https?://(?:www.|)youtube(?:-nocookie)?.com.+?[^\'\"]+)',html)[0]
		url = url.replace('amp;','').replace('-nocookie','')
		import liveresolver
		return liveresolver.resolve(url)




	def next_page(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		soup = soup.find('div',{'class':'wp-pagenavi'})
		try:
			next = soup.find('span',{'class':'current'}).findNext('a')['href']
		except:
			next = None
		return next


