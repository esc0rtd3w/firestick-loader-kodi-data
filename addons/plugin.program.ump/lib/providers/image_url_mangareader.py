import re


domain="http://www.mangareader.net"
encoding="utf-8"
timeout=60*60*24

def run(hash,ump,referer=None):
	pg=ump.get_page(hash,encoding,referer=domain)
	img=re.findall('img.*?src="(.*?)"',pg)
	return {"img":img[0]}
	