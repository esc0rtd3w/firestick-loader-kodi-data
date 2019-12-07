import json
import re

domain="http://mangahere.co"
encoding="utf-8"

def run(ump):
	globals()['ump'] = ump
	if not ump.defs.MT_CHAPTER==ump.info["mediatype"]: return
	i=ump.info
	ump.add_log("Mangahere is searching %s" % i["title"])
	results=json.loads(ump.get_page(domain+"/ajax/search.php",encoding,query={"query":ump.info["title"]}))
	found=False
	results=zip(results["suggestions"],results["data"])
	for result in results:
		if ump.is_same(result[0],ump.info["title"]) or ump.is_same(result[0],ump.info["originaltitle"]):
			matchuri=result[1]
			ump.add_log("Mangahere matched %s"%result[0])
			found=True
			break

	if not found:
		ump.add_log("Mangahere cant find any match for %s"%ump.info["title"])
		return None
	
	res=ump.get_page(matchuri,encoding)
	chapters=re.findall('<span class="left">\r\n\s*?<a class="color_0077" href="(.*?)" >\r\n\s*(.*?)\s*?</a>\r\n\s*?<span class="mr6">',res)
	for chapter in chapters:
		clink,ctit=chapter
		cnum=float(clink.split("/")[-2].replace("c",""))
		parts=[]
		if float(i["episode"])==cnum:
			ump.add_log("Mangahere has matched %s Chapter %s"% (i["title"],i["episode"]))
			firstpg=ump.get_page(clink,encoding)
			pages=sorted([int(x) for x in set(re.findall('option value=".*?" >([0-9]*?)<',firstpg)) if not x=="0"])
			parts=[{"url_provider_name":"mangahere","url_provider_hash":clink}]
			for page in pages:
				parts.append({"url_provider_name":"mangahere","url_provider_hash":"%s%s.html"%(clink,page)})
			ump.add_mirror(parts,ctit,2,missing="ignore")
	return None