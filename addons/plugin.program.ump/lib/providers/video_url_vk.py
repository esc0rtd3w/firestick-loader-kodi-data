import json


def run(url,ump,referer=None):
	src = ump.get_page(url,"utf-8")
	js=json.loads(src)
	videos=js["response"]
	opts={}
	for video in videos.keys():
		if video.startswith("url"):
			opts[video[3:]+"p"]=videos[video]
	return opts