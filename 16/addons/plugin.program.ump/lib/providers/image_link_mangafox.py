import json
import re
from xml.dom import minidom


domain="http://mangafox.me"
encoding="utf-8"

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	ump.add_log("Mangafox is searching %s" % i["title"])
	results=json.loads(ump.get_page(domain+"/ajax/search.php",encoding,query={"term":ump.info["title"]}))
	found=False
	for result in results:
		if ump.is_same(result[1],ump.info["title"]) or ump.is_same(result[1],ump.info["originaltitle"]):
			matchname=result[1]
			matchuri=result[2]
			ump.add_log("Mangafox matched %s"%matchname)
			found=True
			break

	if not found:
		ump.add_log("Mangafox cant find any match for %s"%ump.info["title"])
		return None
	

	res=ump.get_page(domain+"/rss/"+matchuri+".xml",None)
	res=minidom.parseString(res)
	items=res.getElementsByTagName("item")
	for item in items:
		#inhuman title
		title=item.getElementsByTagName("title")[0].firstChild.data
		
		#chapter name
		desc=item.getElementsByTagName("description")[0]
		if desc.firstChild is None:
			desc=""
		else:
			desc=desc.firstChild.data

		u=item.getElementsByTagName("link")[0].firstChild.data
		[(hash)]=re.findall("http://mangafox.me/manga(/"+matchuri+".*?.html)",u)
		[(chapter)]=re.findall("/c(.*?)/",hash)
		#chapter no
		try:
			chapter=str(int(chapter))
		except ValueError:
			pass

		parts=[]
		if str(ump.info["episode"])==chapter:
			ump.add_log("Mangafox is matched %s Chapter %s"% (i["title"],chapter))
			firstpg=ump.get_page("%s/manga%s"%(domain,hash),encoding)
			pages=sorted([int(x) for x in set(re.findall('option value="([0-9]*?)"',firstpg)) if not x=="0"])
			parts=[]
			for page in pages:
				h="/".join(hash.split("/")[:-1])+"/"+str(page)+".html"
				parts.append({"url_provider_name":"mangafox","url_provider_hash":"/manga"+h})
			mname="%s : %s " % (title,desc)
			ump.add_mirror(parts,mname,0.2,missing="ignore")
	return None