import re
import urlparse


def run(hash,ump,referer=None):
	src=ump.get_page("http://www.novamov.com/video/"+hash,"utf-8")
	domain=re.findall('flashvars.domain="(.*?)"',src)
	file=re.findall('flashvars.file="(.*?)"',src)
	key=re.findall('flashvars.filekey="(.*?)"',src)
	url=domain[0]+"/api/player.api.php"
	data={"file":file[0],"key":key}
	src=ump.get_page(url,"utf-8",query=data)
	dic=urlparse.parse_qs(src)
	for key in dic.keys():
		if not key=="url":
			dic.pop(key)
		else:
			dic[key]=dic[key][0]
	return dic