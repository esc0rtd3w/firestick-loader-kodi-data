from resources.lib.modules import webutils,client
from resources.lib.modules.log_utils import log
import re,urllib,urlparse,requests,json

def resolve(url):
	try:
		try: 
			referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
		except:
			referer = page

		s = requests.Session()
		url = webutils.remove_referer(url)

		html = client.request(url,referer=referer)
		rand = re.findall('name=[\"\']rand[\"\'] value=[\"\']([^\"\']+)',html)[0]
		id = re.findall('name=[\"\']id[\"\'] value=[\"\']([^\"\']+)',html)[0]
		post_data = {'op':'download2','id':id,'rand':rand,'referer':referer,'down_script':'1','method_free':'','method_premium':''}
		tor = client.request(url,redirect=False,output ='geturl',post=urllib.urlencode(post_data),headers = {'Referer':referer,'Content-type':'application/x-www-form-urlencoded','Host':'userscloud.com'})
		tor = re.sub(':\d+/','/',tor)
		sm = tor.split('/')[-1]
		tor = tor.replace(sm,urllib.quote(sm))
		from resources.lib.resolvers import torrent
		out = torrent.resolve(tor.replace('https','http'))
		return out
	except:
		return ''
