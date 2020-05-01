import re
domain="http://vidspot.net/"
encoding="utf-8"
def run(hash,ump,referer=None):
	page=ump.get_page(domain+"embed-"+hash+".html",encoding)
	vids=re.findall('"file"\s*:\s*"(.*?)"',page)
	for vid in vids:
		if ".mp4" in vid:
			return {"video":vid}