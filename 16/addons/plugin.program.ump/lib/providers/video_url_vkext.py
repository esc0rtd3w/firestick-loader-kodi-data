import re


def run(url,ump,referer=None):
	src = ump.get_page(url,"utf8")
	videos=re.findall('"(url.*?)":"(.*?)"',src)
	opts={}
	for video in videos:
		if video[0].startswith("url"):
			opts[video[0][3:]+"p"]=video[1].replace("\\","")
	return opts