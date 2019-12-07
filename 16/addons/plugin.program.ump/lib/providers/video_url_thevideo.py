import re
import time
from third import unpack

domain="http://thevideo.me/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	vars=["op","usr_login","id","fname","referer","hash","inhu"]
	data={}
	for var in vars:
		data[var]=re.findall('type="hidden" name="'+var+'" value="(.*?)"',src)[0]
	vars2=["gfk","_vhash"]
	for var in vars2:
		data[var]=re.findall("name: '"+var+"', value: '(.*?)'",src)[0]
	
	#manioulate the cookies. not o sure if that is mandatory
	cooks=["aff","file_id"]
	cstr="ref_url=%2f"+hash+";"
	for cookie in ump.cj:
		if "thevideo.me" in cookie.domain:
			cstr+="%s=%s;"%(cookie.name,cookie.value)
	for cook in cooks:
		cval=re.findall("cookie\('"+cook+"', '(.*?)'",src)[0]
		cstr+="%s=%s; "%(cook,cval)
	data["imhuman"]=""
	header={"Cookie":cstr,
		"Host":"thevideo.me",
		"Origin":"http://thevideo.me",
		"Cache-Control":"max-age=0",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Upgrade-Insecure-Requests":"1"}
	#end cookie/header manipulation
	src = ump.get_page(domain+hash,"utf8",data=data,referer=domain+hash,header=header)
	
	mpri=re.findall("mpri_Key='(.*?)'",src)[0]
	msrc=ump.get_page("%s/jwv/%s"%(domain,mpri),"utf-8",referer=domain+hash)
	vt=re.findall("jwConfig\|(.*?)\|return",msrc)[0]
	mirrors={}
	for file in re.findall("label: '(.*?)', file: '(.*?)'",src):
		mirrors[file[0]]="%s?direct=false&ua=1&vt=%s"%(file[1],vt)
	return dict(mirrors)