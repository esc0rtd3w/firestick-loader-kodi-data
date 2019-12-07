import re
import time
from third import unpack


domain="http://vidto.me/"
def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	vars=["op","usr_login","id","fname","referer","hash"]
	data={}
	for var in vars:
		data[var]=re.findall('type="hidden" name="'+var+'" value="(.*?)"',src)[0]
	time.sleep(6)
	data["imhuman"]="Proceed to video"
	src = ump.get_page(domain+hash,"utf8",data=data,referer=domain+hash)
	packed=re.findall("script type='text/javascript'\>(eval\(function\(.*?)\n",src)
	data= unpack.unpack(packed[0]).encode("ascii","ignore").replace("\\","")
	files=re.findall('label:"(.*?)",file:"(.*?)"',data)
	return dict(files)