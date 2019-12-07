import json
import re
from third.dateutil import parser


domain="http://kissanime.to"
encoding="utf-8"

def get_alts(page):
	pages={}
	related=re.findall('subdub.png.*<a href="(.*?)"><b>(.*?)</b></a>',page)
	if len(related)>0:
		if "(Sub)" in related[0][1]:
			pages["[HS:EN]"]=ump.get_page("%s%s"%(domain,related[0][0]),encoding)
			pages["[D:EN]"]=page
		elif "(Dub)" in related[0][1]:
			pages["[D:EN]"]=ump.get_page("%s%s"%(domain,related[0][0]),encoding)
			pages["[HS:EN]"]=page
	else:
		pages["[HS:EN]"]=page
	return pages

def match_uri(results,refnames):
	matched=False
	datematch=False
	page=""
	for result in results:
		if matched: break
		depth=result.replace("%s/Anime/"%domain,"").split("/")
		if len(depth)>1:
			continue
		page=ump.get_page(result,encoding)
		if "aired" in ump.info and "startdate" in ump.info:
			daired=re.findall("Date aired:</span>\xa0(.*?)\n",page)
			if len(daired):
				datematch=True
				if " to" in daired[0]:
					adate=daired[0].split(" to")[0]
					idate=ump.info["startdate"]
				else:
					adate=daired[0]
					idate=ump.info["aired"]
				if parser.parse(adate)==parser.parse(idate):
					ump.add_log("kissanime found %s "%refnames[0])
					return True,page
		if datematch:
			continue
		orgname=re.findall('<a Class="bigChar".*?>(.*?)</a>',page)
		orgname=orgname[0].split("(")[0]
		names=[orgname]
		namesdiv=re.findall('class="info">Other name\:</span>(.*?)\n',page)
		for div in namesdiv:
			names.extend(re.findall('">(.*?)</a>',div))

		for name in refnames:
			if matched: break
			for name1 in names:
				if ump.is_same(name1,name,strict=False):
					ump.add_log("kissanime found %s"%name)
					matched=True
					break
	return matched,page

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("anime"): return
	is_serie=i["mediatype"]==ump.defs.MT_EPISODE
	names=ump.getnames(orgfirst=False)
	urls=[]	
	jq_limit=False
	found=False
	ump.get_page(domain,encoding)
	for name in names:
		ump.add_log("kissanime is searching %s on %s"%(name,"sitesearch"))
		u="%s/Search/Anime"%domain
		f={"keyword":name}
		page=ump.get_page(u,encoding,data=f,referer="%s/AdvanceSearch"%domain)
		direct=re.findall('<span class="info">Other name',page)
		if len(direct):
			found=True
			res=page
		else:
			urls=re.findall('class="bigChar" href="(.*?)"',page)
			found,res=match_uri([domain+url for url in urls],names)	
			if found:break
	
	if not found:
		ump.add_log("kissanime is searching %s on %s"%(names[0],"google"))
		urls=ump.web_search('site:%s/Anime/* %s "Genres:"'%(domain,names[0]))
		if not urls is None:
			found,res=match_uri(urls,names)

	if not found and not jq_limit:
		ump.add_log("kissanime is searching %s on %s"%(names[0],"swift"))
		urls=[]
		ekey="orVAutnpwh1yygQ3eGzz"
		q={"engine_key":ekey,"q":names[0]}
		res=ump.get_page("http://api.swiftype.com/api/v1/public/engines/search",encoding,query=q)
		res=json.loads(res)
		pages=res["records"]["page"]
		if "/Message/" in pages[0]["url"]:
			ump.add_log("Kissanime exceeded swift search limit")
			jq_limit=True
		else:
			for page in pages:
				urls.append(page["url"].replace("kissanime.com","kissanime.to"))
			found,res=match_uri(urls,names)
		
	if not found:
		ump.add_log("Kissanime can't find %s"%names[0])
		return None
	else:
		res=get_alts(res)
		found=False
		for dub,page in sorted(res.iteritems(),reverse=True):
			table=re.findall('<table class="listing">(.*?)</table>',page,re.DOTALL)
			if len(table)<1:
				continue
			epilinks=re.findall('href="(/Anime/.*?)"',table[0])
			epinames=re.findall('title="Watch anime (.*?)">',table[0])
			epis={}
			epinums=[]
			epidata=zip(epilinks,epinames)
			for epilink,epirow in epidata:
				if "_" in epirow.lower():
					continue
				epinum=re.findall("([0-9]*?) online",epirow)
				if is_serie and len(epidata)>1:
					if (not len(epinum) or epinum=="" or not epinum[0].isdigit()):
						continue
					epinum=int(epinum[0])
					epinums.append(epinum)
					ekey=epinum
				elif not is_serie or len(epidata)==1:
					is_serie=False
					ekey=epirow
					epinum=-1
				fs=None
				fansub=re.findall("\[(.*?)\]",epirow)
				if len(fansub):
					fs=fansub[0]
				epis[ekey]={"fansub":fs,"link":epilink,"abs":epinum}
			
			if len(epinums):
				absoffset=min(epinums)-1
			else:
				absoffset=0
			for ekey in epis.keys():
				epis[ekey]["rel"]=epis[ekey]["abs"]-absoffset
			
			for ekey,epi in epis.iteritems():
				if is_serie:
					if not epi["rel"]==int(i["absolute_number"]):
						continue
				ump.add_log("kissanime is  loading %s"%i["title"])
				epipage=ump.get_page(domain+epi["link"],encoding)
				if not epi["fansub"] is None:
					prefix="%s[FS:%s]"%(dub,epi["fansub"])
				else:
					prefix=dub
				links=re.findall('<select id="selectQuality">(.*?)\n',epipage)
				for link in links:
					qualities=re.findall('value="(.*?)"',link)
					for quality in qualities:
						url=quality.decode("base-64")
						if "googlevideo.com" in url or "blogspot.com" in url:
							found=True
							parts=[{"url_provider_name":"google", "url_provider_hash":{"url":url}}]
							ump.add_mirror(parts,"%s %s"%(prefix,i["title"]))
		if not found:
			ump.add_log("kissanime can't find any links for %s"%i["title"])
