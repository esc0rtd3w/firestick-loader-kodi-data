import random
import string
import md5
import re
import time
import json
import urllib
import urlparse

_domain="cartoonhd.website"
domain="http://%s"%_domain
search="evokjaqbb8"
slk="0A6ru35yyi5yn4THYpJqy0X82tE95btV"
encoding="utf-8"

def iframe(src):
	ret=None
	for sep in ['"',"'"]:
		res=re.findall("<iframe*.?src="+sep+"(.*?)"+sep,src,re.IGNORECASE)
		if len(res):
			ret=res[0]
			break
	return ret

def caesar(plaintext, shift):
	lower = string.ascii_lowercase
	lower_trans = lower[shift:] + lower[:shift]
	alphabet = lower + lower.upper()
	shifted = lower_trans + lower_trans.upper()
	return unicode(str(plaintext).translate(string.maketrans(alphabet, shifted)).encode(encoding))

def nopad(text):
	for i in range(4):
		if text[-1]=="=":text=text[:-1]
	return text

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	
	is_serie=ump.info["mediatype"] == ump.defs.MT_EPISODE
	if not (ump.subscribe("movie") or ump.subscribe("tvshow")): return

	token=re.findall("var\s*tok\s*=\s*'(.*?)'",ump.get_page(domain,encoding))[0] 
	found=False   
	names=ump.getnames(3)
	for name in names:
		if found:break
		ump.add_log("cartoonhd is searching %s"%names[0])
		set="".join([random.choice(string.ascii_letters) for k in range(25)])
		d={
			"q":name,
			"limit":100,
			"timestamp":int(time.time() * 1000),
			"verifiedCheck":token,
			"set":set,
			"rt":caesar(token+set,13),
			"sl":md5.new(slk.encode("base-64")[:-1]+search).hexdigest()
			}
		for result in json.loads(ump.get_page(domain+"/api/v2/cautare/"+search,encoding,data=d).encode("ascii","replace")):
			meta=result["meta"].lower()
			if ump.is_same(name,result["title"]):
				if (is_serie and "show" in meta) or (not is_serie and "movie" in meta and ump.is_same(str(i["year"]),str(result["year"]))):
					found=True
					break
	if found: 
		ump.add_log("cartoonhd has matched %s"%names[0])
	else:
		ump.add_log("cartoonhd can't match %s"%names[0])
		return
	if is_serie:
		sourcepage=domain+result["permalink"]+"/season/%01d/episode/%01d"%(int(i["season"]),int(i["episode"]))
	else:
		sourcepage=domain+result["permalink"]
	page=ump.get_page(sourcepage,encoding)
	header={'X-Requested-With':'XMLHttpRequest'}
	data={}
	header["Authorization"]="Bearer false"
	for cookie in ump.cj:
		if _domain in cookie.domain and cookie.name == "__utmx":
			header["Authorization"]="Bearer %s"%cookie.val
	
	if is_serie:
		data["action"]="getEpisodeEmb"
		mname="%s %dx%d %s" % (i["tvshowtitle"],i["season"],i["episode"],i["title"])
	else:
		data["action"]="getMovieEmb"
		mname=names[0]
	data["elid"]=urllib.quote(str(int(time.time())).encode("base-64")[:-1])
	data["token"]=re.findall("var\s*tok\s*\=\s*'(.*?)'", page)[0]
	data["idEl"]= re.findall('elid\s*=\s*"(.*?)"', page)[0]
	for name,source in json.loads(ump.get_page(domain+"/ajax/nembeds.php",encoding,data=data,header=header)).iteritems():
		sname=source["type"].lower()
		link=iframe(source["embed"])
		if not link:continue
		upname=None
		if "google" in sname:
			upname="google"
			hash={"video":link}
		elif "openload" in sname:
			upname="openload"
			paths=link.split("/")
			hash=None
			for path in range(len(paths)):
				if paths[path]=="embed":
					hash=paths[path+1]
					break
			if not hash : continue
		elif "allmyvideos" in sname:
			upname="allmyvideos"
			path=urlparse.urlparse(link).path
			path=path.replace(".html","")
			path=path.replace(".htm","")
			hash=path.split("-")[1]
		elif "vidspot" in sname:
			upname="vidspot"
			path=urlparse.urlparse(link).path
			path=path.replace(".html","")
			path=path.replace(".htm","")
			hash=path.split("-")[1]
		if upname:
			parts=[{"url_provider_name":upname,"url_provider_hash":hash,"testid":name}]
			ump.add_mirror(parts,mname)			
			
			