import json
import re
import urlparse

def run(hash,ump,referer=None):
	u=urlparse.urlparse(hash)
	vids={}
	src = ump.get_page(hash,"utf8",referer=referer)
	return None
	if  u.path.split("/")[1].isdigit():
		if not u.fragment.isdigit():
			return None
		else:
			pid=u.fragment
		js=json.loads(re.findall("feedPreload\:(.*?\})\}\,\n",src,re.DOTALL)[0])
		for entry in js["feed"]["entry"]:
			if entry["gphoto$id"]==pid:
				for m in entry["media"]["content"]:
					if "flash" in m["type"] or "video" in m["type"]:
						vids["%d:%d"%(m["height"],m["width"])]=m["url"]
			
	else:
		sources=re.findall('"url":"(.*?)","height":(.*?),"width":(.*?),"type":"(.*?)"',src)
		for file in sources:
			u,w,h,t=file
			if "flash" in t or "video" in t:
				vids["%s:%s"%(h,w)]=u
	return vids