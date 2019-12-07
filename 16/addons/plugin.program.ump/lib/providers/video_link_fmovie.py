import re
import json
import urlparse

encoding="utf-8"
domain="http://fmovie.co"
encoding="utf-8"
def run(ump):
	i=ump.info
	if not ump.subscribe("movie"): return
	match=False
	names=ump.getnames(3)
	for name in names:
		if match:break
		ump.add_log("Fmovie.co is searching %s"%names[0])
		page=ump.get_page(domain+"/results",encoding,query={"q":name})
		for result in re.findall('<h3><a title=".*?" href="(.*?)">(.*?)</a></h3>\s*</div>\s*<div class="video_quality">\s*<b>Year</b>\:\s([0-9]{4})\s',page):
			link,mname,myear=result
			if ump.is_same(name,mname) and ump.is_same(myear,str(i["year"])):
				match=True
				break
				
	if not match:
		ump.add_log("Fmovie.co can't match %s"%names[0])
		return
	else:
		ump.add_log("Fmovie.co matched %s"%names[0])
	
	video=urlparse.parse_qs(urlparse.urlparse(domain+link).query).get("v",[None])[0]
	parts=[]
	if video:
		for k,v in json.loads(ump.get_page(domain+"/video_info/iframe",None,data={"v":video},referer=domain+link)).iteritems():
			vidurl=urlparse.parse_qs(urlparse.urlparse(v).query).get("url",[None])[0]
			if vidurl:
				parts.append({"url_provider_name":"google","url_provider_hash":{k:vidurl}})
	if len(parts):
		ump.add_mirror(parts,i["title"])