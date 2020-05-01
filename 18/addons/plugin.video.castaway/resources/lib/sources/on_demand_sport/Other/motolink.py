from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control,cache,control
import re,urlparse,json,urllib,os

from resources.lib.modules.log_utils import log


class info():
    def __init__(self):
    	self.mode = 'motolink'
        self.name = 'motolinks.info'
        self.icon = 'motolink.png'
        self.paginated = False
        self.categorized = False
        self.multilink = False


class main():
	
	def __init__(self,url = control.setting('motolink_base')):
		self.base = control.setting('motolink_base')
		self.url = url
	
	def items(self):
		out = []
		html = client.request(self.base)
		items = webutils.bs(html).findAll('p',{'class':'MsoNormal'})
		words = ['thank','full','chrome','&nbsp;','page','contact','you must?']
		for i in items:
				item = i.getText()
				if len(item)>50 or any(w in item.lower() for w in words):
					continue
				if '(' in item:
					item = '[B][COLOR orange]%s[/COLOR][/B]'%item

				out.append((item,item,control.icon_path(info().icon)))		
		
		
		return out

	
	
	def resolve(self,url):
		url = self.base + '/' + url + '.htm'
		html = client.request(url,referer=self.base)
		unescape = urllib.unquote(re.findall('unescape\s*\(\s*[\"\']([^\"\']+)',html)[0])
		links = re.findall('(http://adf.ly[^\"\']+)',unescape)
		import random
		url = random.choice(links)
		if 'adf.ly' not in url:
			return
		url = cache.get(webutils.adfly,1,url)
		from resources.lib.resolvers import onedrive
		resolved = onedrive.resolve(url)
		return resolved