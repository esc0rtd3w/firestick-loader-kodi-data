# -*- coding: utf-8 -*-
import re
import json

encoding="utf-8"
domain = 'http://dizilab.com'


def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("tvshow"): return
	names=ump.getnames()
	ump.add_log("dizilab is searching %s"%names[0])
	found=False
	for name in names:
		if found:break
		page=ump.get_page(domain+"/arsiv",encoding,query={"tur":"","orderby":"","ulke":"","order":"","yil":"","dizi_adi":name})
		series=re.findall('<div class="tv-series-single">\s*?<a href="(.*?)" class="film-image">\s*?<img src=".*?" alt="(.*?)"/>',page,re.DOTALL)
		for serie in series:
			if ump.is_same(name,serie[1]):
				found=True
			else:
				continue
		url=serie[0]+"/sezon-"+str(i["season"])+"/bolum-"+str(i["episode"])
		epage=ump.get_page(url,encoding)
		if "<title>Sayfa Bulunamad" in epage:
			break
		ump.add_log("dizilab matched %s %dx%d %s"%(i["tvshowtitle"],i["season"],i["episode"],i["title"]))
		videos=re.findall("onclick=\"loadVideo\('(.*?)', this\);\">\s*?<span class=\"(.*?)\">",epage)
		for video in videos:
			hash,type=video
			if "tr" in type:
				prefix="[HS:TR]"
			elif "en" in type:
				prefix="[HS:EN]"
			else:
				prefix=""
			vid=json.loads(ump.get_page("%s/request/php/"%domain,None,data={"tip":1,"type":"loadVideo","vid":hash},referer=url,header={"X-Requested-With":"XMLHttpRequest"}))
			if "sources" in vid:
				vlinks={}
				for google in vid["sources"]:
					vlinks[google["label"]]=google["file"]
					parts=[{"url_provider_name":"google", "url_provider_hash":vlinks}]
				ump.add_mirror(parts,"%s%s %dx%d %s" % (prefix,i["tvshowtitle"],i["season"],i["episode"],i["title"]))	
			if "html" in vid:
				vid=re.findall("src=\"(.*?)\"",vid["html"])[0]
				if "openload" in vid:
					hash=vid.split("embed/")
					hash=hash[1].split("/")[0]
					parts=[{"url_provider_name":"openload", "url_provider_hash":hash}]
					ump.add_mirror(parts,"%s%s %dx%d %s" % (prefix,i["tvshowtitle"],i["season"],i["episode"],i["title"]))					
		return None

	ump.add_log("dizilab can't match %s %dx%d %s"%(i["tvshowtitle"],i["season"],i["episode"],i["title"]))
