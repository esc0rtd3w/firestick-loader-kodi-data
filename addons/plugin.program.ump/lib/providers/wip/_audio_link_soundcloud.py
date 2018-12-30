# -*- coding: utf-8 -*-
import json
import re
import urllib
import urllib2
import urlparse


domain="http://redmp3.cc"
encoding="utf-8"


def crawl_search(query):
	def crawl_single(page):
		return re.findall('<a href="/([0-9]*?)/.*?" class="track-title">(.*?) . (.*?)</a>\n<br/>\n(.*?), [0-9]*?\n',page,re.DOTALL)
	page=ump.get_page(domain+"/Search",encoding,data={"str":query})
	results=crawl_single(page)
	nextpage=re.findall('<a href="(.*?)" class="button">Next page',page)
	i=1
	while True:
		if len(nextpage)>0:
			i+=1
			ump.add_log("redmp3 is iterating page: %d"%i)
			if i==11:
				break
			page=ump.get_page(domain+nextpage[0],encoding)
			results.extend(crawl_single(page))
			nextpage=re.findall(' <a href="(.*?)" class="button">Next page',page)
		else:
			break
	#[("id","artist","title","album")]
	return results
		
def return_links(name,mp,h):
	parts=[{"url_provider_name":mp, "url_provider_hash":h}]
	mname="[HS:TR]%s" % (name,)
	ump.add_mirror(parts,mname)

def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if i["title"]=="" :
		ids=[]
		if i["album"]=="":
			ump.add_log("redmp3 is searching artist: %s"%i["artist"])
			#artist only
			parts=[]
			count=0
			for result in crawl_search(i["artist"]):
				id,artist,title,album=result
				if ump.is_same(artist,i["artist"]) and not id in ids:
					ids.append(id)
					count+=1
					parts.append({"url_provider_name":"redmp3", "url_provider_hash":id,"partname":artist+" - "+title,"referer":domain})
			if count>0:
				ump.add_log("redmp3 is found %d tracks for artist: %s"%(count,i["artist"]))
				mname="[ARTIST:%s],%d Tracks" %(i["artist"],count)
				ump.add_mirror(parts,mname)
			else:
				ump.add_log("redmp3 cam't find any tracks for artist %s"%i["artist"])
		else:
			ump.add_log("redmp3 is searching album: %s - %s"%(i["artist"],i["album"]))
			#album only
			parts=[]
			count=0
			for result in crawl_search(i["artist"] + " - " + i["album"]):
				id,artist,title,album=result
				if ump.is_same(artist,i["artist"]) and ump.is_same(album,i["album"]) and not id in ids:
					ids.append(id)
					count+=1
					parts.append({"url_provider_name":"redmp3", "url_provider_hash":id,"partname":artist+" - "+title,"referer":domain})
			if count>0:
				ump.add_log("redmp3 is found %d tracks in album: %s"%(count,i["album"]))
				mname="[ALBUM:%s],%d Tracks" %(i["album"],count)
				ump.add_mirror(parts,mname)
			else:
				ump.add_log("redmp3 can't find any tracks for album: %s"%i["album"])
	else:
		ump.add_log("redmp3 is searching track: %s - %s"%(i["artist"],i["title"]))
		for result in crawl_search(i["artist"] + " - " + i["title"]):
			id,artist,title,album=result
			if ump.is_same(artist,i["artist"]) and ump.is_same(title,i["title"]):
				ump.add_log("redmp3 found track: %s - %s"%(i["artist"],i["title"]))
				parts=[{"url_provider_name":"redmp3", "url_provider_hash":id,"referer":domain}]
				mname="%s - %s" %(artist,title)
				ump.add_mirror(parts,mname)
			else:
				ump.add_log("redmp3 can't find track: %s - %s"%(i["artist"],i["title"]))