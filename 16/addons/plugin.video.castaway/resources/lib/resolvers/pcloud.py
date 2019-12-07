from resources.lib.modules import client
from resources.lib.modules.log_utils import log
import re

def resolve(url):
	try:
		
		html = client.request(url,mobile=True)
		log(html)
		url = re.findall('downloadlink[\"\']\s*:\s*[\"\']([^\"\']+)[\"\']',html)[0]
		return url.replace(r'\/','/')
	except:
		return
