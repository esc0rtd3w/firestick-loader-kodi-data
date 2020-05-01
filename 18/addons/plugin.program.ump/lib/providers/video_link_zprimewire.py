import re
import urlparse

domain="http://www.primewire.ag"
encoding="utf-8"
matches=[]
max_match=3
max_pages=10

newdoms={"wholecloud":"movshare","cloudtime":"divxstage"}
def codify(prv,path,query=""):
	if prv in newdoms:prv=newdoms[prv]

	try:
		path=path.replace(" ","")
		if prv in ["movshare","vodlocker","nowvideo","divxstage","videoweed","thefile","vidup","thevideo","vidto","vidzi","promptfile","vshare"]:
			hash=path.split("/")[-1]
			hash=hash.replace(".html","")
			hash=hash.replace(".htm","")
			if hash not in ["embed.php"]:
				return prv,hash
		if prv in ["openload","nowvideo"]:
			return prv,path.split("/")[2]
	except:
		return prv,None
	
	return prv,None

def match_results(results,names):
	exact,page,result=False,None,None
	for result in results:
		page=ump.get_page(domain+result,encoding)
		imdb=re.findall('imdb\.com/title/(.*?)"',page)
		try:
			[(rname,ryear)]=re.findall('<title>Watch (.*?) \(([0-9]{4})\)',page)
		except ValueError:
			continue
		rname=re.sub("\(.*?\)","",rname)
		director=re.findall('strong>Director:</strong></td>(.*?</td>)',page,re.DOTALL)
		if len(director)>0:	director=re.findall('">(.*?)</td>',director[0])
		if len(imdb)>0  and "code" in ump.info.keys() and ump.info["code"]==imdb[0]:
			exact=True
			ump.add_log("Primewire found exact matched imdbid %s" %(ump.info["code"]))
		elif int(ryear)==ump.info["year"]:
			if exact: break
			for name in names:
				if ump.is_same(name,rname):
					exact=True
					ump.add_log("Primewire found exact match for %s (%d)" %(name,ump.info["year"]))
					break
		if exact:
			break

	return exact,page,result

def run(ump):
	globals()['ump'] = ump
	if not (ump.subscribe("movie") or ump.subscribe("tvshow")): return
	i=ump.info
	exact=False
	max_pages=3
	is_serie=ump.info["mediatype"] == ump.defs.MT_EPISODE
	names=ump.getnames()
	for name in names:
		ump.add_log("Primewire is searching %s" % name)
		keypage=ump.get_page(domain+"/index.php?search",encoding)
		key=re.findall('name="key" value="(.*?)"',keypage)
		if not len(key)>0:
			ump.add_log("PRIMEWIRE is stuck with CAPTCHA check, you need to wait or change the User-Agent in settings")
			return None
		query={"search_section":int(is_serie)+1,"search_keywords":name,"key":key[0]}
		#if not is_serie:query["year"]=ump.info["year"]
		page1=ump.get_page(domain+"/index.php",encoding,query=query)
		results=re.findall('\<div class="index_item index_item_ie"\>\<a href="(.*?)"',page1)
		exact,page,result=match_results(results,names)

		pagination=re.findall("class=current(.*?)\<div",page1,re.DOTALL)
		if len(pagination)>0 and not exact:
			lastpage=re.findall('href="(.*?)"',pagination[0])
			if len(lastpage)>0:
				lastpage=urlparse.parse_qs(lastpage[-1])["page"]
				for k in range(2,int(lastpage[0])+1):
					if k>max_pages:
						break
					else:
						ump.add_log("Primewire is searching %s on page %d" % (name,k))
						query={"search_section":int(is_serie)+1,"search_keywords":name,"page":k}
						#if not is_serie:query["year"]=ump.info["year"]
						page1=ump.get_page(domain+"/index.php",encoding,query=query,)
						exact,page,result=match_results(re.findall('\<div class="index_item index_item_ie"\>\<a href="(.*?)"',page1),names)
					if exact:
						break
		if exact:
			break

	if not exact:
		ump.add_log("Primewire can't match %s"%name)
		return None

	if is_serie:
		page=ump.get_page(domain+result.replace("watch-","tv-")+"/season-%d-episode-%d"%(int(i["season"]),int(i["episode"])),encoding)
	
	externals=re.findall('class=quality_(.*?)\>.*?href="/goto.php\?(.*?)".*?onClick="(.*?)"',page,re.DOTALL)
	for external in externals:
		if "special_link" in external[2]:
			continue
		try:
			l=dict(urlparse.parse_qsl(external[1]))
			uri = urlparse.urlparse(l["url"].decode("base-64"))
		except:
			ump.add_log("Primewire can't get from %s"%external[1])
			continue
		if is_serie:
			mname="[%s] %s S%dxE%d %s" % (external[0].upper(),name,i["season"],i["episode"],i["title"])
		else:
			mname="[%s] %s" % (external[0].upper(),name)
		prv=uri.hostname.split(".")[-2]
		prv,hash=codify(prv,uri.path, uri.query)
		if hash is None: 
			hash=l["url"].decode("base-64")
			prv="youtubedl"
		ump.add_log("Primewire decoded %s %s" % (mname,prv))
		parts=[{"url_provider_name":prv, "url_provider_hash":hash}]
		ump.add_mirror(parts,mname)
	ump.add_log("Primewire finished crawling %d mirrors"%len(externals))
	return None