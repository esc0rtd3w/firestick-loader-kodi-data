import re

domain="https://player.vimeo.com/video/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	sources=re.findall('"video/mp4".*?"url":"(.*?)".*?"quality":"(.*?)".*?}',src)
	vids={}
	for file in sources:
		u,q=file
		vids[q]=u
	return vids