from __future__ import unicode_literals
from resources.lib.modules import client,webutils,convert,control
from resources.lib.modules.log_utils import log
import re,urlparse,json,sys,os, json,urllib
import requests



class info():
    def __init__(self):
    	self.mode = 'fullmatchesandshows'
        self.name = 'fullmatchesandshows.com'
        self.icon = control.icon_path('fms.png')
        self.paginated = True
        self.categorized = True
        self.multilink = True


class main():
	def __init__(self,url = 'http://www.fullmatchesandshows.com'):
		self.base = 'http://www.fullmatchesandshows.com'
		self.url = url
		self.post_url = 'http://www.fullmatchesandshows.com/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=7.0'
		self.postData = self.get_post(client.request(self.base))
		self.postData['td_filter_value'] =  self.url.split('##')[0]
		try:

			self.postData['td_current_page'] = self.url.split('##')[1]
		except:
			self.postData['td_current_page'] = '1'

	def categories(self):
		cats=[]
		html = client.request(self.base)
		td_block_id = re.findall('<script>var (block_td_uid.+?)[\s=]',html)[0]
		html_cut = html#re.findall('td-subcat-list.*?>(.+?)</u',html)[0]
		items = re.findall('data-td_filter_value=[\"\'](\d+)[\"\'][^<]+>([^<]+)<',html_cut)
		for item in items:
			cats.append((item[0],item[1],control.icon_path(info().icon)))
		return cats



	def get_post(self,content):
		action = 'td_ajax_block'
		block_type = re.compile('block_type.*?"(.+?)"').findall(content)[0]
		td_atts = re.compile('atts.*?\'(.+?)\'').findall(content)[0]
		td_block_id = re.compile('block_td_uid.+?id.*?"(.+?)";').findall(content)[0]
		td_column_number = re.compile('block_td_uid.+?td_column_number.*?"(.+?)";').findall(content)[0]
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
		html = client.request(self.post_url,post=urllib.urlencode(self.postData))
		j = json.loads(html)
		data = j['td_data']
		items = re.findall('href=[\"\']([^\"\']+)[\"\'].+?title=[\"\']([^\"\']+)[\"\'].+?img.+?src=[\"\']([^\"\']+)[\"\']',data)
		for item in items:
			title = self.clean(item[1])
			out.append((title,item[0],item[2]))
		

		return out

	
	def links(self, url):
		out=[]
		html = client.request(url)
		try:
			img = re.findall('class="wpb_wrapper">\s*<a href=[\"\']([^\"\']+)[\"\']',html)[0]
		except:
			img = control.icon_path(info().icon)

		links = re.findall('id=[\"\']([^\"\']+)[\"\']><a href=[\"\']#\d+[\"\']><div.+?>([^<]+)<',html)

		if len(links)<2:
			links = re.findall('href=[\"\']([^\"\']+)[\"\']><div class="acp_title">([^<]+)<',html)

			if len(links)<2:
				try:
					urlx = 'http:' + re.findall('(\/\/config\.playwire\.com\/[^\'\"]+)',html)[0]
				except:
					urlx = re.findall('iframe.+?src=[\"\'](.+?youtu[^\"\']+)',html)[0]
				title = self.clean(re.findall('og:title.+?content=[\"\']([^\"\']+)[\"\']',html)[0]) 
				
				out.append((title,urlx,img))
				return out
			else:
				for link in links:
					title = link[1]
					urlx = link[0]
					out.append((title,urlx,img))
				return out

		for link in links:
			urlx = url + '?id=' + link[0]
			title = self.clean(link[1].upper())
			try:
				img = re.findall('class="wpb_wrapper">\s*<a href=[\"\']([^\"\']+)[\"\']',html)[0]
			except:
				img = control.icon_path(info().icon)
			out.append((title,urlx,img))
		return out

	def resolve(self,url):
		if 'youtu' in url:
			import urlresolver
			return urlresolver.resolve(url)
		if 'fullmatches' in url:
			html = client.request(url)
			try:
				urlx = 'http:' + re.findall('(\/\/config\.playwire\.com\/[^\'\"]+)',html)[0]
			except:
				urlx = re.findall('iframe.+?src=[\"\'](.+?youtu[^\"\']+)',html)[0]
			return self.resolve(urlx)
		if 'playwire' not in url and 'http' not in url:
			ref = url
			headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest','Referer':ref, 'Origin':self.base, 'Host':'fullmatchesandshows.com'}
			s = requests.Session()

			video_d = re.findall('id=(.+?(\d+))',url)[0]
			video_id = video_d[1]
			url = url.replace('?id=%s'%video_d[0],'')
			html = client.request(url)

			acp_pid = re.findall("id=[\"\']acp_post[\"\'].+?value=[\"\'](\d+)[\"\']",html)[0]
			post_data = {'acp_currpage' : video_id,
						'acp_pid' : acp_pid,
						'acp_shortcode' : 'acp_shortcode',
						'action' : 'pp_with_ajax' 
						}
			result = s.post(self.post_url, data=post_data, headers=headers).content
			url = 'http:' + re.findall('(\/\/config\.playwire\.com\/[^\'\"]+)',result)[0]

		

		result = client.request(url)
		result = json.loads(result)
		try:
			f4m=result['content']['media']['f4m']
		except:
			reg=re.compile('"src":"(http://.+?.f4m)"')
			f4m=re.findall(reg,html)[0]
			

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

		
	def next_page(self):
		try:
			page = int(self.url.split('##')[1])
		except:
			page=1
		next = self.postData['td_filter_value'] + '##%s'%(page+1)
		return next

