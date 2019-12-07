# -*- coding: utf-8 -*-
import json
import re
import urlparse
from third import unidecode

domain="http://www.youtube.com/"
encoding="utf-8"
tunnel=["cookie"]
timetol=5
maxttol=15
filters=["sheetmusic","canli","live","karaoke","cover","concert","konser","remix","reaction","parody","meet","version","tutorial"]

def add(hash,i,artist,title,mname,parts):
	ump.add_log("youtube found track: %s - %s"%(i["artist"],i["title"]))
	part={"url_provider_name":"youtube", "url_provider_hash":hash,"referer":domain,"partname":"%s - %s" %(artist,title),"info":i}
	if "playlist" in ump.args:
		parts.append(part)
	else:
		ump.add_mirror([part],mname,wait=0.2,missing="ignore")

def run(ump):
	globals()['ump'] = ump
	parts=[]
	ids=[]
	tracks=[]
	old_artist=""
	old_artalbum=""
	old_tralbum=""
	if ump.defs.MT_ALBUM==ump.info["mediatype"]:
		playlist=ump.args["playlist"]
		mname=ump.args.get("mname","Grooveshark Playlist")
	else:
		playlist=[{"info":ump.info,"art":ump.art}]
		mname="%s - %s" %(ump.info["artist"],ump.info["title"])
	for item in playlist:
		i=item["info"]
		candidates={}
		q='%s %s'%(i["artist"],i["title"])
		page=ump.get_page(domain+"results",encoding,query={"search_query":q},header={"Cookie":"PREF=f1=50000000&f5=30"})
		ump.add_log("youtube is searching track: %s - %s"%(i["artist"],i["title"]))
		match=False
		for res in re.findall('<h3 class="yt-lockup-title\s*"><a href="(.*?)".*?title="(.*?)".*?</a><span class="accessible-description".*?>(.*?)</span></h3>(.*?)</div></li>',page):
			link,ftitle,times,rest=res
			times=re.findall("([0-9]*?)\:([0-9]*?)\.",times)
			try:
				idur=int(i.get("duration",0))
				dur=int(times[0][0])*60+int(times[0][1])
			except:
				idur=0
				dur=0
			hash=urlparse.parse_qs(urlparse.urlparse(link).query).get("v",[None])[0]
			if not hash or hash in ids: continue
			if dur>0 and idur>0:
				fmtitle=unidecode.unidecode(ftitle).lower().replace(" ","")
				filtered=False
				artist=unidecode.unidecode(i["artist"]).lower().replace(" ","")
				title=unidecode.unidecode(i["title"]).lower().replace(" ","")
				for filter in filters:
					if filter in fmtitle and not filter in title:
						filtered=True
						break
				if filtered: continue
				frest=unidecode.unidecode(rest).lower().replace(" ","")
				if (artist in fmtitle or artist in frest) and title in fmtitle:
					if abs(dur-idur)<=timetol:
						match=True
					elif abs(dur-idur)<=maxttol:
						candidates[abs(dur-idur)]=hash
			else:
				title=ftitle.split("-")
				if not len(title)==2:continue
				artist,title=title
				match=ump.is_same(artist,i["artist"]) and ump.is_same(title,i["title"]) 
			if match:
				ids.append(hash)
				add(hash,i,artist,title,ftitle,parts)
				if "playlist" in ump.args:
					break
		if not match and len(candidates):
			hash=candidates[sorted(candidates)[0]]
			ids.append(hash)
			add(hash,i,artist,title,mname,parts)
		
	if len(parts):
		if len(parts)==1:
			ump.add_mirror(parts,mname)
		elif len(parts)>1:
			ump.add_mirror(parts,"%s [TRACKS:%d]"%(mname,len(parts)),wait=0.2,missing="ignore")