import re

def run(hash,ump,referer=None):
	url = "http://animebam.com/embed/%s" % hash
	src = ump.get_page(url, "utf-8")
	sources = re.findall("sources:\s\[(.+?)\]", src, re.DOTALL)[0]
	sources = re.findall("\{file:\s\"(.+?)\",\slabel:\s\"(.+?)\"\}", sources, re.DOTALL)
	videos = {}
	for video_link, video_res in sources:
		videos[video_res] = ump.get_page(video_link, None, referer=url, head=True).geturl()
	return videos
