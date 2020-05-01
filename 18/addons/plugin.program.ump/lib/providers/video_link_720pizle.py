import re
import time
import urlparse


domain="http://720pizle.com"
encoding="iso-8859-9"


def crawl_movie_page(src,url,name):
	movie_function=re.findall("script>(.*)\(\'(.*)\',",src)
	res=re.findall('class="a oval">(.*?)<',src)
	name=re.findall('<h1>(.*?)<',src)
	if len(name)>0: name= name[0]
	if len(res)>0:
		res=res[0]
	else:
		res="HD"
	if len(movie_function) > 0:
		(prv,hash)=movie_function[0]
		if prv == "vidag":
			prv="vid"
		return prv,hash,res,name,None
	else:
		#try plusplayer
		hash=re.findall("class=\"plusplayer\".*?>(.*)</div",src)
		if len(hash) > 0:
			return "plusplayer",hash[0],res,name,None
		hash=re.findall("(http\://webteizle.org/player/vk\.asp.*?)\"",src)
		if len(hash) > 0:
			return "vkplayer",hash[0],res,name,None
		hash=re.findall('<iframe src="(http://720pizle.com/player/pcloud\.asp.*?)"',src)
		if len(hash):
			src=ump.get_page(hash[0],encoding,referer=domain+url)
			hash=re.findall("url: '(https://api.pcloud.com/getvideolinks.*?)'",src)
			if len(hash):
				hash=urlparse.urlparse(hash[0])
				hash=urlparse.parse_qs(hash.query)
				return "pcloud",hash.get("fileid",[''])[0],res,name,hash.get("auth",[''])[0]
			hash=""
		ump.add_log("720pizle Movie page has different encryption: %s" % str(url))
		return None,None,None,None,None

def return_links(name,type,upname,uphash,res,referer):
	if not upname is None:
		dub=["","[D:TR]"][type=="dub"]
		sub=["","[HS:TR]"][type=="sub"]
		mname="%s%s%s" % (dub,sub,name)
		#ump.add_log("720pizle decoded %s %s" % (mname,movie_link[0][0]))
		parts=[{"url_provider_name":upname, "url_provider_hash":uphash,"referer":referer}]
		ump.add_mirror(parts,mname)

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	names=ump.getnames()
	
	if not ump.subscribe("movie"):return
	match=False
	for name in names:
		if match:break
		ump.add_log("720pizle is searching %s" % name)
		results=ump.get_page("%s/ara.asp"%domain,encoding,query={"a":name})
		results=re.findall('<span class="oval">(.*?)</span>.*?<a class="sayfa\-icerik\-baslik" href="(.*?)">',results,re.DOTALL)
		#results=json.loads(ump.get_page(domain+"/api/autocompletesearch.asp",encoding,query={"limit":"10","q":name}))
		#if len(results)==0 or len(results)==1 and "orgfilmadi" in results[0].keys() and "Bulunamad" in results[0]["orgfilmadi"] : 
		#	ump.add_log("720pizle can't find any links for %s"%name)
		#	continue

		for result in results:
			#if result["imdbid"]==i["code"]:
			#	ump.add_log("720pizle matched %s with imdb:%s" % (i["title"],result["imdbid"]))
			#	match=result["url"]
			#	break
			#elif ump.is_same(result["orgfilmadi"],name) and ump.is_same(result["yil"],i["year"]):
			#	ump.add_log("720pizle matched %s in %s" % (name,result["yil"]))
			#	match=result["url"]
			#	break
			[(u'Matrix Reloaded - The Matrix Reloaded (2003)', u'/detay/the-matrix-reloaded.html'), (u'Matrix Revolutions - The Matrix Revolutions (2003)', u'/detay/the-matrix-revolutions.html'), (u'Matrix - The Matrix (1999)', u'/detay/the-matrix.html')]
			sub=result[0].split("(")
			link=result[1]
			year=0
			if len(sub) and len(sub[1])==5:
					year=int(sub[1][:-1])
					fnames=sub[0].split("-")
			else:
				fnames=result[0].split["-"]
			for fname in fnames:
				if ump.is_same(name,fname):
					if year>0 and i["year"]==year:
						ump.add_log("720pizle matched %s in %d" % (name,year))
						match=link
						break
					elif year==0:
						ump.add_log("720pizle matched %s "%name)
						match=link
						break
		time.sleep(1)

	if not match:
		ump.add_log("720pizle cant find any match from %d results"%len(results))
		return None

	src=ump.get_page(domain+match,encoding)
	movie_pages=re.findall('href="(/izle/.*?)" title=""',src)
	count=len(movie_pages)
	for movie_page in movie_pages:
		movie_page_type=["dub","sub"][movie_page.split("/")[2]=="altyazi"]
		src=ump.get_page(domain+movie_page,encoding)
		prv,hash,res,name2,ref=crawl_movie_page(src,movie_page,name)
		if ref is None:	ref=domain+movie_page
		return_links(name2,movie_page_type,prv,hash,res,ref)
		alts=[]
		urls = re.findall('href="(/izle/.*?)" rel="nofollow"(.*?)</a>',src)
		alts=[x[0] for x in urls if not "tlb_isik" in x[1] ]
		count+=len(alts)
		ump.add_log("720pizle found %d mirrors for Turkish %s %s" % (len(alts),movie_page_type,name2))
		for alt in alts:
			src=ump.get_page(domain+alt,encoding)
			#ump.add_log("720pizle is crawling %s" % alt)
			prv,hash,res,name2,ref=crawl_movie_page(src,alt,name)
			if ref is None:	ref=domain+movie_page
			return_links(name2,movie_page_type,prv,hash,res,ref)
	ump.add_log("720pizle finished crawling %d mirrors"%count)
	return None
