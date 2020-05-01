import json
import re


def run(hash,ump,referer=None):
	src = ump.get_page("http://myvi.ru/player/embed/html/"+hash,"utf8")
	p=re.findall("dataUrl:'(.*?)'",src)[0]
	js=json.loads(ump.get_page("http://myvi.ru"+p,"utf-8"))
	videos=js["sprutoData"]["playlist"]
	opts={}
	for video in videos:
		opts[video["videoId"]]=video["video"][0]["url"]
	return opts