import re

def run(hash,ump,referer=None):
	src = ump.get_page("http://auengine.com/embed.php?file=%s" % hash, "utf-8")
	return {"url": re.findall("var video_link = '(.*?)'",src)[0]}
