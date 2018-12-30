import re

domain="https://vid.me/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	sources=re.findall('source src="(.*?)" type="video/mp4" res="(.*?)"',src)
	vids={}
	for file in sources:
		u=str(file[0])
		while True:
			if "&amp;" in u:
				u=u.replace("&amp;","&")
			else:
				break
		vids[file[1]]=u
	return vids