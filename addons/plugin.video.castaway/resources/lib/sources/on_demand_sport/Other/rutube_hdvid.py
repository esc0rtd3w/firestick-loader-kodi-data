from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert
import re,urlparse,json
from resources.lib.modules.log_utils import log



class info():
    def __init__(self):
    	self.mode = 'rutube_hdvid'
        self.name = 'Rutube HD-vid'
        self.icon = 'rutube.png'
        self.paginated = True
        self.categorized = False
        self.multilink = False


class main():
	
	def __init__(self,url = 'http://rutube.ru/api/video/person/834887/?page=1&format=json'):
		self.base = 'http://fullmatchtv.com'
		self.url = url

	def items(self):
		out=[]
		result = client.request(self.url)
		jsx = json.loads(result)['results']
		for el in jsx:
			title = el['title']
			url = el['id']
			img = el['thumbnail_url']
			item = (title.encode('utf-8'),url,img)
			out.append(item)

		return out

	def resolve(self,url):
		url = 'http://rutube.ru/api/play/options/'+url+'?format=json'
		result = client.request(url)
		jsx = json.loads(result)
		link = jsx['video_balancer']['m3u8']
		return link

	def next_page(self):
		try:
			page = re.findall('page=(\d+)',self.url)[0]
			next_page = self.url.replace('page=%s'%(page),'page=%s'%(int(page)+1))
		except:
			return None
		return next_page

