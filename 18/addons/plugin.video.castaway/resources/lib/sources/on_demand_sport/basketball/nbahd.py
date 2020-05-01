from __future__ import unicode_literals
from resources.lib.modules import client,webutils
from resources.lib.modules.log_utils import log
from random import shuffle
import re,urlparse,urllib


class info():
    def __init__(self):
    	self.mode = 'nbahd'
        self.name = 'NBA GO (full replays)'
        self.icon = 'nbastream.png'
        self.paginated = True
        self.categorized = False
        self.multilink = True


class main():
	def __init__(self,url = 'http://nbahd.com'):
		self.base = 'http://nbahd.com'
		self.url = url

	def items(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		items=soup.findAll('div',{'class':'thumb'})
		out=[]
		for item in items:
			url=item.find('a')['href']
			title=item.find('a')['title'].encode('utf-8')
			thumb=item.find('img')['src'].encode('utf-8')

			out+=[[title,url,thumb]]

		return out

	def links(self,url, img=' '):
		html = client.request(url)
		out=[]
		urls = []
		subs = ['GVIDEO','ALTERNATIVE']
		gvideos = []
		for i in range(1,5):
			gvideos += re.findall('(http://play.wtutor.net/cgi-bin/ProtectFile.File[^\"\']+)[\"\'] target="_blank"><img src=[\"\'](http://nbahd.com/wp-content/uploads/2015/04/p(%s).png)[\"\']'%i,html)



		
		for i in range(1,5):
			gvideos += re.findall('href=[\"\'](http://wefights.com[^\"\']+)[\"\'] target="_blank"><img src=[\"\'](http://nbahd.com/wp-content/uploads/2015/04/p(%s).png)[\"\']'%i,html)

		for i in range(1,5):
			gvideos += re.findall('href=[\"\'](http://nbahd.com/[^\"\']+)[\"\'] target="_blank"><img src=[\"\'](http://nbahd.com/wp-content/uploads/2015/04/p(%s).png)[\"\']'%i,html)

		for v in gvideos:
			url = v[0]
			sub = subs[0]
			if 'nbahd' in url:
				sub = subs[1]


			title = 'Part %s %s'%(v[2],sub)
			img = v[1]
			if url not in urls:
				out.append((title,url,img))
				urls.append(url)
		return out





	def resolve(self,url):
		if 'nbahd.com' in url:
			return self.resolve_nbahd(url)
		else:
			return self.resolve_wtutor(url)


	def resolve_nbahd(self,url):
		try:
			html=client.request(url)
			urls = re.findall('iframe.+?src=[\"\']([^\"\']+)[\"\']',html)
			import urlresolver
			for url in urls:
				try:
					resolved = urlresolver.resolve(url)
				except:
					resolved = False
				if resolved:
					break
			return resolved
		except:
			return ''
	def resolve_wtutor(self,url):
		try:
			base = 'wefights.com'
			if 'wtutor' in url:
				base = 'play.wtutor.net'
			ref = url
			html=client.request(url)
			urls = re.findall('data-link=[\"\']([^\"\']+)[\"\']',html)
			url = 'http://%s/wp-admin/admin-ajax.php?action=ts-ajax&p=%s&n=1'%(base,urllib.quote(urls[0]))
			html = client.request(url,referer=ref,headers={'Host':base})
			log(html)
			try:
				video = re.findall('file\s*:\s*[\"\']([^\"\']+)[\"\']',html)[0]
			except:
				video = re.findall('src=[\"\']([^\"\']+)[\"\']',html)[0]
			if 'google' in video:
				return video
			else:
				import urlresolver
				return urlresolver.resolve(url)
		except:
			return ''


	def next_page(self):
		html = client.request(self.url)
		soup = webutils.bs(html)
		try:
			next_page=soup.find('div',{'class':'wp-pagenavi'}).find('a',{'class':'nextpostslink'})['href']
		except:
			next_page=None
		return next_page

