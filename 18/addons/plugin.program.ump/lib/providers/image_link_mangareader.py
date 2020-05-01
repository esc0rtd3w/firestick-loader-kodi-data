import re

domain="http://www.mangareader.net"
encoding="utf-8"

def run(ump):
	globals()['ump'] = ump
	if not ump.defs.MT_CHAPTER==ump.info["mediatype"]: return
	i=ump.info
	ump.add_log("Mangareader is searching %s" % i["title"])
	for result in ump.get_page("%s/actions/search/"%domain,encoding,query={"q":ump.info["title"],"limit":100},referer=domain).split("\n"):
		if len(result.split("|"))==6:
			name1,img,name2,mangaka,dir,id=result.split("|")
			if ump.is_same(name1,ump.info["title"]):
				ump.add_log("Mangareader matched %s : %s"%(name1,mangaka))
				res=ump.get_page(domain+dir,encoding,referer=domain)
				for chapter,chname in re.findall('href="'+dir+'/([0-9]*?)">(.*?)<',res):
					if float(i["episode"])==float(chapter):
						ump.add_log("Mangareader has matched %s Chapter %s"% (i["title"],chname))
						firstpg=ump.get_page(domain+dir+"/"+str(chapter),encoding)
						pages=sorted([int(x) for x in set(re.findall('option value=".*?"\s?>([0-9]*?)<',firstpg)) if not x=="0"])
						parts=[{"url_provider_name":"mangareader","url_provider_hash":"%s%s/%s"%(domain,dir,chapter)}]
						for page in pages:
							parts.append({"url_provider_name":"mangareader","url_provider_hash":"%s%s/%s/%d"%(domain,dir,chapter,page)})
						ump.add_mirror(parts,chname,0.2,missing="ignore")