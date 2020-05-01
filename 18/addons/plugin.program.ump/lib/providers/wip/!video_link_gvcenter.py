import base64
import hashlib
import json
import random
import re
import sys
import time

from third import pyaes


domain="http://www.gearscenter.com"
encoding="utf-8"

ANDROID_LEVELS = {'22': '5.1', '21': '5.0', '19': '4.4.4', '18': '4.3.0', '17': '4.2.0', '16': '4.1.0', '15': '4.0.4', '14': '4.0.2', '13': '3.2.0'}
COUNTRIES = ['US', 'GB', 'CA', 'DK', 'MX', 'ES', 'JP', 'CN', 'DE', 'GR']
DKEY = base64.b64decode('M2FiYWFkMjE2NDYzYjc0MQ==')
FKEY = base64.b64decode('MmIyYTNkNTNkYzdiZjQyNw==')
ua="Apache-HttpClient/UNAVAILABLE (java 1.4)"
build = random.choice(ANDROID_LEVELS.keys())
device_id = hashlib.md5(str(random.randint(0, sys.maxint))).hexdigest()
country = random.choice(COUNTRIES)

#algo borrowed from SALTS
def querify(query={}):
	extra=query.copy()		
	now = str(int(time.time()))
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

def get_json(*args,**kwargs):
	if "query" in kwargs.keys():
		kwargs["query"]=querify(kwargs["query"])
	try:
		js=json.loads(ump.get_page(*args,**kwargs))
	except ValueError:
		ump.add_log('Invalid JSON returned for: %s' % (args[0]))
		return None
	else:
		if 'data' in js:
			return json.loads(decrypt(js["data"],DKEY))

def decrypt(text,cipher):
	decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(cipher))
	plain_text = decrypter.feed(base64.b64decode(text))
	plain_text += decrypter.feed()
	return plain_text

def get_episode_json( sea, epi, js_data):
	new_data = {'listvideos': []}
	for episode in js_data['listvideos']:
		if ' S%02dE%02d ' % (int(sea), int(epi)) in episode['film_name']:
			new_data['listvideos'].append(episode)
	return new_data

def get_sources(catalog_id,is_serie,sea=None,epi=None):
	sources=[]
	query={"option":"content","id":catalog_id}
	js=get_json("%s/gold-server/gapiandroid205/"%domain,encoding,query=query,header={"User-Agent":ua})
	if is_serie:
		js = get_episode_json(sea,epi,js)
	for film in js['listvideos']:
		query={"option":"filmcontent","id":film['film_id'],"cataid":0}
		film_js=get_json("%s/gold-server/gapiandroid205/"%domain,encoding,query=query,header={"User-Agent":ua})
		for film in film_js['videos']:
			film_link = decrypt(film['film_link'],FKEY)
			for match in re.finditer('(http.*?(?:#(\d+)#)?)(?=http|$)', film_link):
				link, height = match.groups()
				parts=[{"url_provider_name":"google", "url_provider_hash":json.dumps({"html5":True,"url":link})}]
				ump.add_mirror(parts,ump.info["title"])

def run(ump):
	globals()['ump'] = ump
	i=ump.info

	is_serie="tvshowtitle" in i.keys() and not i["tvshowtitle"].replace(" ","") == ""

	if is_serie:
		orgname=i["tvshowtitle"]
		altnames=i["tvshowalias"].split("|")
	else:
		orgname=i["title"]
		altnames=i["originaltitle"].split("|")
	
	for k in range(len(altnames)):
		if altnames[k]=="":
			altnames.pop(k)
	
	names=[orgname]
	names.extend(altnames)
	
	found=False
	for name in names:
		if found:
			break
		ump.add_log("gvcenter is searching %s"%name)
		q={"option":"search","q":name,"page":1,"total":0,"block":0}
		js=get_json("%s/gold-server/gapiandroid205/"%domain,encoding,query=q,header={"User-Agent":ua})
		for item in js['categories']:
			match = re.search('(.*?)\s+\((\d{4}).?\d{0,4}\s*\)', item['catalog_name'])
			if match:
				match_title, match_year = match.groups()
			else:
				match_title = item['catalog_name']
				match_year = ''
			
			sameyear=("year" in i and not i["year"]=="" and int(i["year"])==int(match_year)) or is_serie
			
			if ump.is_same(match_title,name) and int(is_serie)==int(item["type_film"]) and sameyear:
				found=True
				ump.add_log("gvcenter has matched %s"%name)
				query={"video_type":item["type_film"],"catalog_id":item['catalog_id']}
				break
	
	if not found:
		ump.add_log("gvcenter can't match %s"%name)
		return None
	
	if is_serie:
		get_sources(query["catalog_id"],is_serie,i["season"],i["episode"])
	else:
		get_sources(query["catalog_id"],is_serie,i["season"],i["episode"])