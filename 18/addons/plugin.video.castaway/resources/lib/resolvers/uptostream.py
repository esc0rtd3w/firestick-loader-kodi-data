from resources.lib.modules import client
from resources.lib.modules.log_utils import log
import re

def resolve(url):
	try:
		out = []
		ref=url
		q = url.split('/')[-2]
		headers = {'Referer':ref}
		id = re.findall('uptostream.com/(?:iframe/)?([^/]+)',url)[0]
		url = 'https://uptostream.com/'+id
		html = client.request(url,headers = headers)
		urls = re.findall('src=[\'\"]([^\'\"]+)[\'\"] type=[\'\"]video/mp4[\'\"] data-res=[\'\"]([^\"\']+)[\'\"]',html)
		for url in urls:
			ur = 'http:' + url[0]
			res = url[1]
			out.append((ur,res))

		return out
	except:
		return []
