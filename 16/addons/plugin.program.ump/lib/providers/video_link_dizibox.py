# -*- coding: utf-8 -*-
import re
import urlparse
import json

encoding="utf-8"
domain = 'http://dizibox.com'
pdomain= "http://play.dizibox.net"

def parse(url,key=None):
	up=urlparse.urlparse(url)
	if key:
		return up,urlparse.parse_qs(up.query).get(key,[None])[0]
	else:
		return up

def scrape_page_safe(*args,**kwargs):
	try:
		return scrape_page(*args,**kwargs)
	except:
		ump.add_log("Dizibox faced an error scraping: %s"%args[1])

def scrape_page(page,etype):
	etype=etype.lower()
	if etype=="ingilizce":
		prefix="[HS:EN]"
	elif etype==u"altyazısız":
		prefix=""
	else:
		prefix="[HS:TR]"
	parts=[]
	
	player=re.findall('iframe src="(https?\://play\.dizibox\.net/.*?)"',page)

	if len(player):
		jq,v=parse(player[0],"v")
		google=["/king/king.php","/hades/hades.php","/zeus/zeus.php"]
		if jq.path in google:
			hash={}
			for quality in json.loads(ump.get_page(pdomain+jq.path,encoding,referer=player[0],query={"p":"GetVideoSources"},data={"ID":v}))["VideoSources"]:
				hash[quality["label"]]=quality["file"]
			parts.append({"url_provider_name":"google","url_provider_hash":hash})
		elif jq.path=="/vidpart/vidpart.php":
			for vid in v.decode("base-64").split("|"):
				parts.append({"url_provider_name":"vidme","url_provider_hash":vid.split("/")[-1]})
			prefix+="[MP]"
		elif jq.path=="/dbxyeni.php":
			parts.append({"url_provider_name":"facebook","url_provider_hash":v.decode("base-64")})
			prefix+="[MP]"
		elif jq.path=="/haydi.php":
			hash=v.decode("base-64").split("/")[-1]
			parts.append({"url_provider_name":"okru","url_provider_hash":hash})
		else:
			return
		
	openload=re.findall('openload.co/embed/(.*?)/?"',page)
	if len(openload):
		parts.append({"url_provider_name":"openload","url_provider_hash":openload[0]})
	
	tune=re.findall('<iframe.*?src="https?://tune.pk/.*?"',page)
	if len(tune):
		up,vid=parse(tune[0],"vid")
		parts.append({"url_provider_name":"tune","url_provider_hash":vid})
	
	if len(parts):
		ump.add_mirror(parts,"%s %s %dx%d %s" % (prefix,i["tvshowtitle"],i["season"],i["episode"],i["title"]))


def scrape_epi(page,elink):
	etype=re.findall("<option class='woca-current-page' href='.*?' selected='selected'>(.*?)</option>",page)
	try:
		etype=etype[0]
	except:
		etype="dbx"
	
	scrape_page_safe(page,etype)
	for link in re.findall("<option value='(.*?)'>(.*?)</option>",page):
		page=ump.get_page(link[0],encoding,referer=domain)
		scrape_page_safe(page,link[1])


def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("tvshow"): return
	globals()['i'] = i
	names=ump.getnames()
	found=False
	page=ump.get_page(domain+"/arsiv",encoding,referer=domain)
	series=re.findall('<li><a title="(.*?)" href="(.*?)"',page)
	for name in names:
		if found: break
		ump.add_log("dizibox is searching %s"%name)
		for serie in series:
			if found:break
			sname,slink=serie
			if ump.is_same(sname,name): 
				found=True
				break
		salias=slink.split("/")[-2]
	if not found: return
	elink="%s/%s-%d-sezon-%d-bolum-izle/"%(domain,salias,int(i["season"]),int(i["episode"]))
	page=ump.get_page(elink,encoding,referer=domain)
	ump.add_log("dizibox matched %s %dx%d %s"%(name,i["season"],i["episode"],i["title"]))
	scrape_epi(page,elink)