import json
import random

def run(hash,ump,referer=None):
	u="https://api.pcloud.com/getvideolinks?auth=%s&fileid=%s"%(referer,hash)
	movies={}
	for variant in json.loads(ump.get_page(u,"utf-8"))["variants"]:
		movies[variant["height"]]={"url":"https://"+random.choice(variant["hosts"])+variant["path"],"referer":u}
	return movies