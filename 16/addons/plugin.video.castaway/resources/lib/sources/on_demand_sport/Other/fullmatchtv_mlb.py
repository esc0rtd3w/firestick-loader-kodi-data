from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert
import re,urlparse,json,urllib

from resources.lib.modules.log_utils import log



class info():
    def __init__(self):
    	self.mode = 'fullmatchtv_mlb'
        self.name = 'fullmatchtv.com MLB'
        self.icon = 'fullmatchtv.png'
        self.paginated = True
        self.categorized = False
        self.multilink = False


class main():
	
	def __init__(self,url = 'http://fullmatchtv.com/mlb'):
		self.base = 'http://fullmatchtv.com'
		self.url = url
		self.post_url = 'http://fullmatchtv.com/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=6.6.2'
		self.postData = self.get_post()
		self.postData['td_filter_value'] =  self.url.split('##')[0]
		try:

			self.postData['td_current_page'] = self.url.split('##')[1]
		except:
			self.postData['td_current_page'] = '1'

	def get_post(self):
		content = client.request('http://fullmatchtv.com/mlb',referer=self.base)
		action = 'td_ajax_block'
		block_type = re.compile('block_type.*?"(.+?)"').findall(content)[1]
		td_atts = re.compile('atts.*?\'(.+?)\'').findall(content)[1]
		td_block_id = re.compile('id.*?"(.+?)"').findall(content)[1]
		td_column_number = re.compile('td_column_number.*?"(.+?)"').findall(content)[1]
		
		data = {
			'action':action,
			'block_type':block_type,
			'td_atts':td_atts,
			'td_block_id':td_block_id,
			'td_column_number':td_column_number,
		}
		return data

	def clean(self,text):
		def fixup(m):
			text = m.group(0)
			if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
			else: return unichr(int(text[2:-1])).encode('utf-8')
		try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
		except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))


	def items(self):
		out = []
		urls=[]
		html = client.request(self.post_url,post=urllib.urlencode(self.postData))
		j = json.loads(html)
		data = j['td_data']
		items = re.findall('href=[\"\']([^\"\']+)[\"\'].+?title=[\"\']([^\"\']+)[\"\'].+?img.+?src=[\"\']([^\"\']+)[\"\']',data)
		for item in items:
			title = self.clean(item[1])
			if item[0] not in urls:
				out.append((title,item[0],item[2]))
				urls.append(item[0])
		

		return out

	
	def resolve(self,url):
		from resources.lib.resolvers import fullmatchtv
		return fullmatchtv.resolve(url)

	def next_page(self):
		try:
			page = int(self.url.split('##')[1])
		except:
			page=1
		next = self.postData['td_filter_value'] + '##%s'%(page+1)
		return next