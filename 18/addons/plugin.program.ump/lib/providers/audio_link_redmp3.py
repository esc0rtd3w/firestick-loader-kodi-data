# -*- coding: utf-8 -*-
import re
from urllib2 import HTTPError
domain="http://redmp3.su"
encoding="utf-8"
tunnel=("redmp3",)

def crawl_search(query):
	def crawl_single(page):
		return re.findall('<div class="player" data-mp3url="(.*?)" data-title="(.*?) . (.*?)">.*?\n<br/>\n(.*?), [0-9]*?\n',page,re.DOTALL)
	page=ump.get_page(domain+"/Search",encoding,data={"str":query},tunnel=tunnel)
	results=crawl_single(page)
	nextpage=re.findall('<a href="(.*?)" class="button">Next page',page)
	i=1
	while True:
		if len(nextpage)>0:
			i+=1
			ump.add_log("redmp3 is iterating page: %d"%i)
			if i==11:
				break
			page=ump.get_page(ump.absuri(domain,nextpage[0]),encoding,tunnel=tunnel)
			results.extend(crawl_single(page))
			nextpage=re.findall(' <a href="(.*?)" class="button">Next page',page)
		else:
			break
	#[("id","artist","title","album")]
	return results
		
def run(ump):
	globals()['ump'] = ump
	parts=[]
	if ump.defs.MT_ALBUM==ump.info["mediatype"]:
		playlist=ump.args["playlist"]
		mname=ump.args.get("mname","Redmp3 Playlist")
	else:
		playlist=[{"info":ump.info,"art":ump.art}]
		mname="%s - %s" %(ump.info["artist"],ump.info["title"])
	for item in playlist:
		found=False
		i=item["info"]
		ump.add_log("redmp3 is searching track: %s - %s"%(i["artist"],i["title"]))
		try:
			results=crawl_search(i["artist"] + " " + i["title"])
		except HTTPError,e:
			if e.code==404:
				ump.add_log("Redmp3 content is copyrighted")
				continue
			else:
				raise e
		for result in results:
			id,artist,title,album=result
			if ump.is_same(artist,i["artist"]) and ump.is_same(title,i["title"]):
				found=True
				ump.add_log("redmp3 found track: %s - %s"%(i["artist"],i["title"]))
				parts.append({"url_provider_name":"redmp3", "url_provider_hash":id,"referer":domain,"partname":"%s - %s" %(i["artist"],i["title"]),"info":i})
				break
		if not found:
			ump.add_log("Redmp3 cant find %s - %s"%(i["artist"], i["title"]))

	if len(parts):
		if len(parts)==1:
			ump.add_mirror(parts,mname)
		elif len(parts)>1:
			ump.add_mirror(parts,"%s [TRACKS:%d]"%(mname,len(parts)),wait=0.2,missing="ignore")