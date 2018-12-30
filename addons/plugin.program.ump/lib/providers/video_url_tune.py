import re
import json

domain="https://embed.tune.pk/play/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+hash,"utf8",referer=referer)
	js= re.findall("TunePlayer\((.*?)\)\;\s*\<\/script",src)
	vids={}
	for file in json.loads(js[0])["details"]["player"]["sources"]:
		vids[file["bitrate"]]=file["file"]
	return vids