import re

def run(hash,ump,referer=None):
	url = "http://yourupload.com/embed/%s" % hash
	src = ump.get_page(url, "utf-8")
	link=re.findall("file: '(.*?\.mp4)'",src)
	return {"part": {"url":link[0],"referer":url}}
