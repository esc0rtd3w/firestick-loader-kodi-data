import StringIO
import base64
import hashlib
import json
import random
import re
import sys
import time
import zipfile

from third import pyaes


encoding="utf-8"
domain = 'http://mobapps.cc'
#JSON_FILES = {VIDEO_TYPES.MOVIE: 'movies_lite.json', VIDEO_TYPES.TVSHOW: 'tv_lite.json'}
#LINKS = ['/api/serials/get_movie_data/?id=%s', VIDEO_TYPES.TVSHOW: '/api/serials/es/?id=%s', VIDEO_TYPES.EPISODE: '/api/serials/e/?h=%s&u=%01d&y=%01d'}
ua = 'android-async-http/1.4.1 (http://loopj.com/android-async-http)'

#algo borrowed from SALTS
def querify(query={}):
	extra=query.copy()		
	now = str(int(time.time()))
	build = random.choice(ANDROID_LEVELS.keys())
	device_id = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
	country = random.choice(COUNTRIES)
	extra["os"]="android"
	extra["version"]="2.0"
	extra["versioncode"]="205"
	extra["param_1"]="F2EF57A9374977FD431ECAED984BA7A2"
	extra["deviceid"]=device_id
	extra["param_3"]="7326c76a03066b39e2a0b1dc235c351c"
	extra["param_4"]=country
	extra["param_5"]=country.lower()
	extra["token"]=hashlib.md5(now).hexdigest()
	extra["time"]=now
	extra["devicename"]="Google-Nexus-%s-%s"%(build, ANDROID_LEVELS[build])
	return extra


def get_json(is_serie):
	zip_data=ump.get_page(domain+'/data/data_en.zip',None)
	if zip_data:
		zip_file = zipfile.ZipFile(StringIO.StringIO(zip_data))
		jsfile=['movies_lite.json','tv_lite.json'][int(is_serie)]
		data = zip_file.read(jsfile)
		zip_file.close()
		return json.loads(data)
	else:
		return []

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not i["code"][:2]=="tt":
		return None

	is_serie,names=ump.get_vidnames()
	found=False

	ump.add_log("vkbox is searching %s"%names[0])	
	json_data = get_json(is_serie)
	for item in json_data:
		match_id = item.get('imdb_id', '')
		if i["code"]==match_id:
			ump.add_log("vkbox matched %s with exact imdbid %s"%(names[0],i["code"]))
			found=item["id"]
			break

	if not found:
		ump.add_log("vkbox can't match %s"%names[0])
		return None
	elif is_serie:
		mname="[%s S%dxE%d %s" % (i["tvshowtitle"],i["season"],i["episode"],i["title"])
		magic_num = int(found) + int(i["season"]) + int(i["episode"])
		url='/api/serials/e/?h=%s&u=%01d&y=%01d'%(found,int(i["season"]),int(i["episode"]))
	else:
		mname=i["title"]
		magic_num = int(found) + 537
		url="/api/serials/get_movie_data/?id=%s"%found
		
	sources=ump.get_page(domain+url,encoding,header={'User-Agent': ua})
	if sources:
		try:
			json_data = json.loads(sources)
		except ValueError:
			ump.add_log('vkbox: No JSON returned: %s' %url)
		else:
			try: langs = json_data['langs']
			except: langs = json_data
			for lang in langs:
				prefix="[D:%s] "%lang["lang"]
				stream_url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(lang['apple']) + magic_num), str(int(lang['google']) + magic_num), lang['microsoft'])
				c={"cookie":"remixlang=3; remixdt=0; remixrefkey=7c0a782690bc369fd7; remixtst=3ce1f985; remixsid=2393b2428d35087530d582eeb2ce691d99674cdb3dbab25841d16; remixsslsid=1; remixexp=1; remixflash=18.0.0; remixscreen_depth=24"}
				data={"video":str(int(lang['apple']) + magic_num)+"_"+str(int(lang['google']) + magic_num),"module":"search","act":"show","al":"1","autoplay":0}
				print ump.get_page("https://vk.com/al_video.php","utf-8",data=data,header=c).encode("ascii","ignore")
				print type(stream_url)
				parts=[{"url_provider_name":"vkext", "url_provider_hash":stream_url}]
				ump.add_mirror(parts,prefix+mname)
#				break
#			else:
#				log_utils.log('No english language found from vkbox: %s' % (langs), xbmc.LOGWARNING)
	else:
		ump.add_log('vkbox: No data returned from %s' % (url))



	
#	if is_serie:
#		get_sources(query["catalog_id"],is_serie,i["season"],i["episode"])
#	else:
#		get_sources(query["catalog_id"],is_serie,i["season"],i["episode"])