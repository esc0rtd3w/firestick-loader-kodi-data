import json
import re
import string
import urlparse

from third import unidecode


domain="http://moviesub.org"
encoding="utf-8"

def decode_link(link):
	prv=parts=None
	if isinstance(link,list):
		prv="google"
		vlinks={}
		for file in link:
			vlinks[file["quality"]]=file["files"]
		parts=[{"url_provider_name":"google", "url_provider_hash":vlinks}]
	else:
		try:
			up=urlparse.urlparse(link)
		except:
			return prv,parts
	
	if "thevideo." in link:
		hash=up.path.split("-")[-1].split(".")[0]
		prv="thevideo"
		if len(hash)>0:
			parts=[{"url_provider_name":prv,"url_provider_hash":hash,"referer":link}]
	
	elif "videomega." in link:
		hash=urlparse.parse_qs(up.query).get("ref",[""])[0]
		prv="videomega"
		if len(hash)>0:
			parts=[{"url_provider_name":prv,"url_provider_hash":hash,"referer":link}]

	elif "openload." in link:
		hash=up.path.split("/")[2]
		prv="openload"
		if len(hash)>0:
			parts=[{"url_provider_name":prv,"url_provider_hash":hash}]
	
	elif "vodlocker." in link:
		hash= up.path.split("-")[1]
		prv="vodlocker"
		if len(hash)>0:
			parts=[{"url_provider_name":prv,"url_provider_hash":hash,"referer":link}]
	

	return prv,parts

def filtertext(text,space=True,rep=""):
	str=string.punctuation
	if space:
		str+=" "
	for c in str:
		text=text.replace(c,rep)
	return text.lower()

def match_results(page,names,info):
	match_name,match_year,subpage,qual=False,False,"",""
	results=re.findall('<p class="title"><a href="(.*?)" title="(.*?)">.*?</a></p>\s*?</div>\s*?<div class="quality">(.*?)</div>',page,re.DOTALL)
	for result in results:
		match_name=False
		if match_year:
			break
		link,title,qual=result
		for name in names:
			if ump.is_same(title,name):
				match_name=True
				break
		if match_name:
			subpage=ump.get_page(link,encoding,referer=domain)
			year=re.findall('Release\sYear\:(.*?)\<\/p',subpage)[0]
			year=str(int(re.sub("\<.*?\>","",year)))
			match_year=info["year"]==int(year)
	if qual=="HD":
		qual=""
	else:
		qual="[%s]"%qual
	return qual,match_year,subpage

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("movie"): return
	names=ump.getnames()

	for name in names:
		ump.add_log("moviesub is searching %s" % unidecode.unidecode(name))
		page=ump.get_page(domain+"/search/%s.html"%unidecode.unidecode(name),encoding)
		camrip,match_year,page=match_results(page,names,i)
		if match_year:
			ump.add_log("moviesub matched %s in %d"%(unidecode.unidecode(name),i["year"]))
			break
		else:
			ump.add_log("moviesub can't match %s"%unidecode.unidecode(name))

	if not match_year:
		return None
		
	medias=re.findall('<div class="swiper-slide.*?"><a data-film="([0-9]*?)" data-name="([0-9]*?)" data-server="([0-9]*?)"',page)
	for media in medias:
		try:
			dfilm,dname,dserver=media
			resp=json.loads(ump.get_page("%s/ip.temp/swf/plugins/ipplugins.php"%domain,None,data={"ipplugins":1,"ip_film":dfilm,"ip_server":dserver,"ip_name":dname},referer=domain))
			url=json.loads(ump.get_page("%s/ip.temp/swf/ipplayer/ipplayer.php"%domain,None,data={"w":"100%","h":"450","s":dserver,"u":resp["s"]},referer=domain))
		except:
			continue
		prv,parts=decode_link(url["data"])
		if not parts is None:
			ump.add_log("moviesub decoded: %s"%url["data"])
			ump.add_mirror(parts,"%s%s" % (camrip,names[0]))