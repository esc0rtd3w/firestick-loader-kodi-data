from cookielib import Cookie
import re
import time
import urllib
import urlparse


def run(hash,interface):
	src=interface.get_page("http://www.thefile.me/"+hash,"utf-8")
	form=re.findall('\<form method="POST"(.*?)</form',src,re.DOTALL)
	if len(form)>0:
		inputs=re.findall('<input.*?name="(.*?)".*?value="(.*?)"',form[0])
		data={}
		for input in inputs:
			data[input[0]]=input[1]
	else:
		return None
	time.sleep(1)
	src=interface.get_page("http://www.thefile.me/"+hash,"utf8",data=data)
	key=re.findall('file: "(.*?)"',src)
	if len(key)>0:
		key=key[0]
	else:
		key=None
	return key