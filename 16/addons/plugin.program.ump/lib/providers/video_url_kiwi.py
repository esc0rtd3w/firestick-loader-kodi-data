import re
import urllib2
import urlparse


def run(hash,ump,referer=None):
	src = ump.get_page("http://v.kiwi.kz/v2/"+hash,"utf8")
	fv=re.findall('flashvars="(.*?)"',src)[0]
	keys=urlparse.parse_qs(urllib2.unquote(fv))
	return {"video":keys["url"][0]}