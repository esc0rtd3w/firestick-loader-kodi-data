import re


def run(hash,ump,referer=None):
	if isinstance(hash,dict):
		return hash
	else:
		src = ump.get_page(hash,"utf8",referer=referer)
		videos=re.findall('"?file"?: "(.*?)",\r?\n?\s*?"?label"?: "(.*?)",\r?\n?\s*?"?type',src)
		opts={}
		for video in videos:
			opts[video[1]]=video[0]
		return opts