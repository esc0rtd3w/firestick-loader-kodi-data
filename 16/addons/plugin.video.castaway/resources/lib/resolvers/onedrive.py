from resources.lib.modules import client
from resources.lib.modules.log_utils import log
import re,urllib,urlparse,base64

def resolve(url):
	try:
		encoded = 'u!' + base64.b64encode(b'%s'%url).rstrip('=').replace('/','_').replace('+','-')
		url = 'http://api.onedrive.com/v1.0/shares/' + encoded + '/root'
		result = client.request(url)
		video = re.findall('downloadUrl[\"\']\s*:[\"\']([^\"\']+)[\"\']',result)[0].replace('https','http')
		log(video)
		return video + '|%s' % urllib.urlencode({'User-Agent':client.agent()})
	except:
		return ''
