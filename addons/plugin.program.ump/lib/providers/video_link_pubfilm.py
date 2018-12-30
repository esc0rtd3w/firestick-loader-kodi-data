import json
import re
import socket
import time

domain="http://pidtv.com/"
encoding="utf-8"

def match_results(link,inf,names):
	prefix=""
	submatch=False
	subpage=ump.get_page(link,encoding,referer=domain)
	imdbid=re.findall('"(http://www.imdb.com/title/tt.*?)"',subpage)
	if len(imdbid)>0 :
		imdbid=imdbid[0]
		if imdbid.endswith("/"):
			imdbid=imdbid[:-1]
		imdbid=imdbid.split("/")[-1]
		if imdbid==inf["code"]:
			submatch=True
			ump.add_log("pubfilm matched %s with imdbid: %s"%(names[0],imdbid))
	else:
		mname=re.findall('<span style\="font-size\: large\;">(.*?)<',subpage)
		if len(mname)>0:
			for name in names:
				if submatch: break
				if ump.is_same(name,mname[0]):
					year=re.findall('\>([0-9]{4})\s',subpage)
					if len(year)>0:
						submatch=inf["year"]==int(year[0])
	prefix0=re.findall("itemprop=\"name\">.*?\((.*?)\)</span>",subpage)
	if len(prefix0)>0:
		prefix=prefix0[0].upper()
		if "HD" == prefix:
			prefix=""
		else:
			prefix="[%s]"%prefix
	return prefix,submatch,subpage
	

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("movie"): return
	prefix=""
	names=ump.getnames(2)
	for name in names:
		ump.add_log("pubfilm is searching %s" % name)
		data={"options":"qtranslate_lang=0&set_intitle=None&customset%5B%5D=post","action":"ajaxsearchpro_search","aspp":name,"asid":"1","asp_inst_id":"1_1"}
		page=ump.get_page(domain+"/wp-admin/admin-ajax.php",encoding,data=data,referer=domain)
		results=re.findall('<a class="asp_res_url" href=\'(.*?)\'>',page)
		for result in results[:3]:
			prefix,match,page=match_results(result,i,names)
			if match : break
		if match:break

	if not match:
		ump.add_log("pubfilm can't match %s"%name)
		return None

	link1=re.findall('"(http://player\..*\.com/api.*?)"',page)
	for link in link1:
		page=ump.get_page(link,encoding,referer=result)
		try:
			data=eval(re.findall("sources\:(.*?\])",page)[0])
			mparts={}
			k=0
			for link in data:
				k+=1
				mparts[link.get("label",str(k))]=link["file"]
			parts=[{"url_provider_name":"google", "url_provider_hash":mparts,"referer":link1}]
			ump.add_mirror(parts,"%s %s"%(prefix,name))			
		except:
			ump.add_log("pubfilm cant scrape %s"%link)
			
