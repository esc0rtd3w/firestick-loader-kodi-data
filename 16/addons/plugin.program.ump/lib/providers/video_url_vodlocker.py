import re
import time


def run(hash,ump,referer=None):
	src=ump.get_page("http://www.vodlocker.com/"+hash,"utf8")
	form=re.findall('\<Form method="POST"(.*?)</Form',src,re.DOTALL)
	inputs=re.findall('<input.*?name="(.*?)" value="(.*?)"',form[0])
	data={}
	for input in inputs:
		data[input[0]]=input[1]
	time.sleep(1)
	src=ump.get_page("http://www.vodlocker.com/"+hash,"utf8",data=data)
	key=re.findall('file: "(.*?)"',src)
	return {"url1":key[0]}