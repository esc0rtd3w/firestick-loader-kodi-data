# -*- coding: utf-8 -*-
import re


domain="http://musicmp3.ru"
encoding="utf-8"
tunnel=["cookie"]
#tunnel="disabled"
		
def run(ump):
	globals()['ump'] = ump
	if not ump.is_same(ump.buffermode,"3"):
		ump.add_log("MUSICMP3 CAN NOT RUN WITH BUFFERING ENABLED. GO TO ADDON SETTINGS-> ADVANCED SETTINGS and SET FORCE LIBCURL: NO BUFFER")
		return None
	ids=[]
	s_old=""
	a_old=""
	t_old=""
	parts=[]
	if ump.defs.MT_ALBUM==ump.info["mediatype"]:
		playlist=ump.args["playlist"]
		mname=ump.args.get("mname","Musicmp3 Playlist")
	else:
		playlist=[{"info":ump.info,"art":ump.art}]
		mname="%s - %s" %(ump.info["artist"],ump.info["title"])
	for item in playlist:
		i=item["info"]
		albums=[]
		ump.add_log("musicmp3 is searching %s"%i["artist"])
		if not i["album"]=="":
			s_query=i["artist"]
			q={"text":s_query}
		else:
			s_query="%s %s"%(i["artist"],i["title"])
			q={"text":s_query,"all":"songs"}
		if not s_old==s_query:
			s_page=ump.get_page(domain+"/search.html",encoding,q,tunnel=tunnel)
		s_old=s_query
		ump.add_log("musicmp3 is searching track: %s - %s"%(i["artist"],i["title"]))
		if not i["album"]=="":
			artists=re.findall('<a class="artist_preview__title" href="(.*?)">(.*?)</a>',s_page)
			for artist in artists:
				if ump.is_same(artist[1],i["artist"]):
					ump.add_log("musicmp3 matched Artist: %s"%artist[1])
					if not a_old==artist[0]:
						a_page=ump.get_page(ump.absuri(domain,artist[0]),encoding,tunnel=tunnel)
					a_old=artist[0]
					albums=re.findall('<a class="album_report__link" href="(.*?)".*?class="album_report__name">(.*?)</span>',a_page)
					break
		else:
			albums=re.findall('<a class="song__link" href="(.*?)">(.*?)</a></td><td class="song__artist song__artist.*?"><a class="song__link" href=.*?">(.*?)<',s_page)
		for album in albums:
			if (not i["album"]=="" and ump.is_same(album[1],i["album"])) or (i["album"]=="" and ump.is_same(i["artist"],album[2]) and ump.is_same(i["title"],album[1])):
				ump.add_log("musicmp3 matched Artist: %s, Album : %s"%(i["artist"],album[1]))
				if not t_old==album[0]:
					t_page=ump.get_page(ump.absuri(domain,album[0]),encoding,tunnel=tunnel)
				t_old=album[0]
				tracks=re.findall('<tr class="song" id="(.*?)".*?rel="(.*?)".*?<span itemprop="name">(.*?)</span>',t_page)
				for track in tracks:
					trackid,rel,tn=track
					if ump.is_same(i["title"],tn):
						if not rel+trackid in ids:
							parts.append({"url_provider_name":"musicmp3", "url_provider_hash":rel,"partname":i["artist"]+" - "+tn,"referer":trackid,"info":i})
							ump.add_log("musicmp3 matched Artist: %s, Track : %s"%(i["artist"],tn))
							ids.append(rel+trackid)
				break
	if len(parts):
		if len(parts)==1:
			ump.add_mirror(parts,mname)
		elif len(parts)>1:
			ump.add_mirror(parts,"%s [TRACKS:%d]"%(mname,len(parts)),wait=0.2,missing="ignore")