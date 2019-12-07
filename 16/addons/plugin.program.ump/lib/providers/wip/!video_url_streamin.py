from cookielib import Cookie
import re
import time
import urllib
import urlparse


def run(hash,interface):
	src=interface.get_page("http://www.streamin.to/"+hash,"utf8")
	cookies=re.findall("cookie\('(.*?)', '(.*?)'",src)
	form=re.findall('\<Form method="POST"(.*?)</Form',src,re.DOTALL)
	if len(form)>0:
		inputs=re.findall('<input.*?name="(.*?)" value="(.*?)"',form[0])
		data={}
		for input in inputs:
			data[input[0]]=input[1]
	else:
		return None
	time.sleep(5)
	src=interface.get_page("http://www.streamin.to/"+hash,"utf8",data=data)
	key=re.findall('file: "(.*?)"',src)
	if len(key)>0:
		key=key[0]
	else:
		key=None
	return key