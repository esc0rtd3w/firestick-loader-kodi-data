import json
import re


def run(hash,ump,referer=None):
	page=ump.get_page("http://www.dailymotion.com/embed/video/"+hash,"utf8")
	js=re.findall("window.playerV5 = dmp.create\(document.getElementById\('player'\), (.*?)\);\n",page)
	opts={}
	for k,v in json.loads(js[0])["metadata"]["qualities"].iteritems():
		opts[k]=v[0]["url"]
	return opts