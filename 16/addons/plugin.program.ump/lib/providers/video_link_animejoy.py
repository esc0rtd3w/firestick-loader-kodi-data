import json
import re
import time

domain="http://anime-joy.tv"
encoding="utf-8"

slower=0
def match_uri(results,refnames):
	matched=False
	for result in results:
		if matched: break
		depth=result.replace(domain+"/","").replace("http://www.animejoy.tv/","").split("/")
		if len(depth)>2:
			continue
		time.sleep(slower)
		page=ump.get_page(result,encoding)
		orgname=re.findall('<h2 class="animeicbaslik">\n\t(.*?)\n</h2>',page)
		orgname=orgname[0].split("(")[0]
		names=[orgname]
		namesdiv=re.findall('<div class="ozelliksol">Alternative Name:</div>\n\t\t<div class="ozelliksag">\t\n\t\t\t\t(.*?)\t\t</div>',page,re.DOTALL)
		if not namesdiv[0]=="-":
			names.extend(namesdiv[0].split(";"))

		for name in refnames:
			if matched: break
			for name1 in names:
				if ump.is_same(name1,name,strict=True):
					ump.add_log("animejoy found %s"%name)
					matched=result
					break
	return matched

def run(ump):
	globals()['ump'] = ump
	if not ump.subscribe("anime"): return
	i=ump.info
	names=ump.getnames(orgfirst=False)
	is_serie=i["mediatype"]==ump.defs.MT_EPISODE

	urls=[]	
	found=False
	
	for name in names:
		ump.add_log("animejoy is searching %s on %s"%(name,"sitesearch"))
		try:
			time.sleep(slower)
			results=json.loads(ump.get_page(domain+"/search.php",encoding,query={"term":name}))
		except ValueError:
			continue
		
		found=match_uri([domain+"/watch/"+item["id"] for item in results],names)
		if found:break
	
	if not found:
		time.sleep(slower)
		sitenames=ump.get_page(domain+"/animelist",encoding)
		sitenames=re.findall('<div class="anim"><a href="(.*?)">(.*?)</a>',sitenames)
		ump.add_log("animejoy is searching %s on %s"%(name,"sitelist"))
		for name in names:
			for sitename in sitenames:
				if ump.is_same(sitename[1],name,strict=True):
					found=domain+"/"+sitename[0]
					ump.add_log("animejoy found %s"%name)
				if found:break
			if found:break

	if not found:
		ump.add_log("animejoy is searching %s on %s"%(names[0],"google"))
		urls=ump.web_search('site'+domain+'/watch %s "Alternative Name:"'%names[0])
		if not urls is None:
			found=match_uri(urls,names)
		
	if not found:
		ump.add_log("animejoy can't find %s"%names[0])
		return None
	else:

		if is_serie:
			epinum=i["absolute_number"]
		else:
			epinum=1
		time.sleep(slower)
		epilink=found+"/%d"%epinum
		epipage=ump.get_page(epilink,encoding)
		if epipage.endswith("No Anime"):
			if is_serie:
				time.sleep(slower)
				epilink=found+"/%d"%i["episode"]
				epipage=ump.get_page(epilink,encoding)
				if epipage.endswith("No Anime"):
					ump.add_log("animejoy can't find episode %d of %s"%(epinum,name))
					return None
		ump.add_log("animejoy is  loading %s"%i["title"])
		iframes=re.findall('src="(.*?/embed/.*?)"',epipage)
		time.sleep(slower)
		iframe=ump.get_page(iframes[0],encoding)
		link=re.findall('<source src="(.*?)" type=',iframe)[0]
		parts=[{"url_provider_name":"transparent", "url_provider_hash":{"video":link},"referer":epilink}]
		ump.add_mirror(parts,"%s %s"%("[HS:EN]",i["title"]))

	if not found:
			ump.add_log("animejoy can't find any links for %s"%i["title"])
