import json
import re
import urllib
import urllib2
import urlparse

from third.unidecode import unidecode


domain="http://www.solarmovie.la"
encoding="utf-8"
matches=[]
max_match=3
max_pages=10

def codify(prv,path):
	path=path.replace(" ","")
	if prv in ["movshare","vodlocker","sharesix","novamov","nowvideo","divxstage","sharerepo","videoweed","thefile","stagevu","vidxden","filenuke","vidbull"]:
		return path.split("/")[-1]
	elif prv in ["zalaa","uploadc","mightyupload"]:
		return path.split("/")[-2]
	else:
		return None

def match_results(results,names):
	exact,page,result=False,None,None
	for result in results:
		page=ump.get_page(result,encoding)
		imdb=re.findall('"http://www.imdb.com/title/(tt.*?)"',page)
		title=re.findall('headerText"> (.*?) </span>',page)
		year=re.findall('Year\:</strong> ([0-9]*?)<',page)
		director=re.findall('http://www.solarmovie.la/?director\=(.*?)"',page,re.DOTALL)
		if len(imdb)>0  and "code" in ump.info.keys() and ump.info["code"]==imdb[0]:
			exact=True
			ump.add_log("Solarmovies found exact matched imdbid %s" %(ump.info["code"]))
		elif len(imdb)==0 and len(title)>0 and len(year)>0 and len(director)>0 and year[0]==ump.info["year"] and ump.is_same(director[0],ump.info["director"]):
			for name in names:
				if ump.is_same(name,title[0]):
					exact=True
					ump.add_log("Solarmovie found exact match with %s/%s/%s" %(name,ump.info["director"],ump.info["year"]))
					break
		if exact:
			break

	return exact,page,result

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	exact=False
	max_pages=3
	is_serie,names=ump.get_vidnames()
	if not i["code"][:2]=="tt" or is_serie:
		return None

	for name in names:
		if exact:
			break
		ump.add_log("Solarmovie is searching %s" % name)
		keypage=ump.get_page(domain+"/index.php?search",encoding)
		query={"keywords":name,"year":i["year"]}
		page1=ump.get_page(domain,encoding,query=query)
		results=re.findall('class="coverImage" href="(.*?)"',page1)
		exact,page,result=match_results(results,names)

		lastpage=re.findall('page=([0-9]*?)">>>',page1)
		if len(lastpage)>0 and not int(lastpage)==1:
			for k in range(2,int(lastpage[0])+1):
				if k>max_pages:
					break
				else:
					ump.add_log("Solarmovie is searching %s on page %d" % (name,k))
					query={"keywords":name,"year":i["year"],"page":k}
					page1=ump.get_page(domain,encoding,query=query,)
					exact,page,result=match_results(re.findall('class="coverImage" href="(.*?)"',page1),names)
				if exact:
					break

	if not exact:
		ump.add_log("Solarmovie can't match %s"%names[0])
		return None
	
	return None

	if is_serie:
		page=ump.get_page(domain+result.replace("watch-","tv-")+"/season-%d-episode-%d"%(int(i["season"]),int(i["episode"])),encoding)

	externals=re.findall('class=quality_(.*?)\>.*?href="(/external.php.*?)".*?onClick="(.*?)"',page,re.DOTALL)
	for external in externals:
		if "special_link" in external[2]:
			continue
		page=ump.get_page(domain+"/external.php?"+external[1],encoding)
		link=re.findall('frame src="(http.*?)"',page)
		if len(link)>0:
			uri = urlparse.urlparse(link[0])
			if is_serie:
				mname="[%s] %s S%dxE%d %s" % (external[0].upper(),i["tvshowtitle"],i["season"],i["episode"],i["title"])
			else:
				mname="[%s] %s" % (external[0].upper(),i["title"])
			prv=uri.hostname.split(".")[-2]
			hash=codify(prv,uri.path)
			if hash is None: 
				continue
			ump.add_log("Primewire decoded %s %s" % (mname,prv))
			parts=[{"url_provider_name":prv, "url_provider_hash":hash}]
			ump.add_mirror(parts,mname)
	ump.add_log("Primewire finished crawling %d mirrors"%len(externals))
	return None