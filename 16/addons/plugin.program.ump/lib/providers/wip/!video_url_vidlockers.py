import re
import time
import urlparse

from third import unpack


domain="http://www.vidlockers.ag/"
def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	vars=["op","id","rand","method_free","method_premium"]
	data={}
	for var in vars:
		data[var]=re.findall('type="hidden" name="'+var+'" value="(.*?)"',src)[0]
	time.sleep(1)
	data["down_script"]="1"
	src = ump.get_page(domain+hash,"utf8",data=data,referer=domain+hash)
	files=re.findall('file: "(.*?)"',src)
	return {"video":{"url":files[0],"referer":domain+hash}}