from resources.lib.modules import control,client
from resources.lib.modules.log_utils import log
import xbmc,os,re,urllib,base64

def resolve(url):
	initial = url
	libPath = os.path.join(control.addonPath, 'resources/lib/modules')
	serverPath = os.path.join(libPath, 'livestreamerXBMCLocalProxy.py')
	try:
		import requests
		requests.get('http://127.0.0.1:19000/version')
		proxyIsRunning = True
	except:
		proxyIsRunning = False
		if not proxyIsRunning:
			xbmc.executebuiltin('RunScript(' + serverPath + ')')


	url = re.findall('[\"\']([^\"\']+)',url)[0]
	try:
		headers = re.findall('-http-headers=([^\s]+)',url)[0]
	except:
		headers = urllib.urlencode({'User-agent':client.agent()})

	url += '|' + headers

	try:
		cookies = re.findall('-http-cookie=([^\s]+)',initial)[0]
		url += '|' + cookies
	except:
		pass

	url = base64.b64encode(url)

	url = 'http://127.0.0.1:19000/livestreamer/' + url + '|' + cookies

	return url

   	
