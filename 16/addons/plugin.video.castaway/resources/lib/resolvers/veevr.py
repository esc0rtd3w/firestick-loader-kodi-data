from resources.lib.modules import client
from resources.lib.modules.log_utils import log
import re,urllib,urlparse

def resolve(url):
	#try:
		out=[]
		referer = url
		url = url.replace('embed','videos').replace('sos','videos').replace('/video.mp4','')
		html = client.request(url)
		urls = re.findall('src=[\"\']([^\"\']+)[\"\'] type=[\"\']video/mp4[\"\'] label=[\"\']([^\"\']+)',html)
		for url in urls:
			host  = urlparse.urlparse(url[0]).netloc
			ur = url[0] + '|%s' %urllib.urlencode({'Referer':referer,'User-agent':client.agent(),'Host':host}).replace('%3D','=')
			q = url[1]
			out.append((ur,q))
		return out
	#except:
#		return []
