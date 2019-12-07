from resources.lib.modules import client,control
from resources.lib.modules.log_utils import log
import re,urllib

def resolve(url):

		html = client.request(url)
		links = re.findall('id=[\"\']([^\"\']+)[\"\']><a href=[\"\']#\d+[\"\']><div.+?>([^<]+)<',html)
		if len(links)<2:
			urls = re.findall('<iframe.+?src=[\'"](.+?)[\'"]',html)
			import urlresolver
			for url in urls:
				resolved = urlresolver.resolve(url)
				if resolved:
					return resolved
					break	
		else:
			import requests
			choices = [x[1] for x in links]
			i = control.selectDialog(choices,heading='Choose a link:')
			ref = url
			headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest','Referer':ref, 'Origin':'http://fullmatchtv.com', 'Host':'fullmatchtv.com'}
			s = requests.Session()

			

			acp_pid = re.findall("id=[\"\']acp_post[\"\'].+?value=[\"\'](\d+)[\"\']",html)[0]
			post_data = {'acp_currpage' : int(i)+1,
						'acp_pid' : acp_pid,
						'acp_shortcode' : 'acp_shortcode',
						'action' : 'pp_with_ajax' 
						}
			result = s.post('http://fullmatchtv.com/wp-admin/admin-ajax.php', data=post_data, headers=headers).content
			url = re.findall('<iframe.+?src=[\'"](.+?)[\'"]',result)[0]
			import urlresolver
			return urlresolver.resolve(url)
