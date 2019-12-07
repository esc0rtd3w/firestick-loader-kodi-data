import re
import time

domain="http://vshare.eu/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	vars=["op","usr_login","id","fname","referer","method_free"]
	data={}
	for var in vars:
		data[var]=re.findall('<input.*?name="'+var+'" value="(.*?)"',src)[0]
	time.sleep(1)
	src = ump.get_page(domain+hash,"utf8",data=data,referer=domain+hash)
	files=re.findall('file: "(.*?)"',src)
	return {"media":files[0]}