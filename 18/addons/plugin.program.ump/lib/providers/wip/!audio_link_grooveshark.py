# -*- coding: utf-8 -*-
import json
import re


domain="http://groovesharks.org"
encoding="utf-8"
tunnel=["cookie"]

def run(ump):
	globals()['ump'] = ump
	parts=[]
	ids=[]
	tracks=[]
	old_artist=""
	old_artalbum=""
	old_tralbum=""
	if "playlist" in ump.args:
		playlist=ump.args["playlist"]
		mname=ump.args.get("mname","Grooveshark Playlist")
	else:
		playlist=[{"info":ump.info,"art":ump.art}]
		mname="%s - %s" %(ump.info["artist"],ump.info["title"])
	for item in playlist:
		match=False
		i=item["info"]
		if not i["album"]=="":
			if match:continue
			if not ump.is_same(i["artist"],old_artist):
				artist_page=ump.get_page("%s/music/searchArtist/"%domain,encoding,query={"csrf_yme":"","query":i["artist"]},referer=domain,tunnel=tunnel)
			old_artist=i["artist"]
			ump.add_log("grooveshark is searching track: %s - %s"%(i["artist"],i["title"]))
			results=re.findall('<h4 class="nowrap">(.*?)</h4>\s*?<p class="nowrap"><a href="(.*?)".*?>Artist Info</a>',artist_page)
			for result in results:
				if match:break
				artist=result[0]
				if ump.is_same(artist,i["artist"]):
					if not ump.is_same(artist,old_artalbum):
						album_page=ump.get_page("%s/music/getAlbums/"%domain,encoding,query={"csrf_yme":"","artist":artist},referer=domain,tunnel=tunnel)
					old_artalbum=i["artist"]
					albums=re.findall('title="Album Info" onclick="getTracksAlbum\(\'(.*?)\'',album_page)
					if not len(albums):	albums=re.findall('<h4 class="truncate">(.*?)</h4>',album_page) #nojs for webtunnels
					for album in albums:
						if match:break
						if ump.is_same(i["album"],album):
							if not ump.is_same(old_tralbum,album):
								tralbum_page=ump.get_page("%s/music/getTracksAlbums/"%domain,encoding,query={"csrf_yme":"","artist":artist,"album":album},referer=domain,tunnel=tunnel)
							old_tralbum=album
							tracks=re.findall('onclick="addPlayList\(\'(.*?)\',\'(.*?)\',\'.*?\'\);"><i class="fa fa-plus">',tralbum_page)
							if not len(tracks):
								tracks=re.findall('</i>.(.*?)\s*?<div class="btn-group pull-right">',tralbum_page)
								tracks=[(x,i["artist"]) for x in tracks]
							match=True
		else:
			page=ump.get_page("%s/music/search/"%domain,encoding,query={"csrf_yme":"","query":"%s %s"%(i["artist"],i["title"])},referer=domain,tunnel=tunnel)
			tracks=re.findall('"Add to Playlist" onclick="addPlayList\(\'(.*?)\',\'(.*?)\'',page)
			if not len(tracks):
				tracks=re.findall('data-track="(.*?)"  data-cover=".*?" data-artist="(.*?)"',page) #nojs
			if not len(tracks):
				tracks=[(i["title"],i["artist"])]
			match=True
		for track in tracks:
			match=False
			if match:break
			title,artist=track
			if ump.is_same(title,i["title"]) and ump.is_same(artist,i["artist"]):
				links=json.loads(ump.get_page("%s/music/getYoutube/"%domain,encoding,query={"csrf_yme":"","artist":artist,"track":title},referer=domain,tunnel=tunnel))
				ump.add_log("grooveshark found track: %s - %s"%(i["artist"],i["title"]))
				id=links["id"]
				if not id in ids:
					parts.append({"url_provider_name":"youtube", "url_provider_hash":id,"referer":domain,"partname":"%s - %s" %(artist,title),"info":i})
					ids.append(id)
				break
	if len(parts):
		if len(parts)==1:
			ump.add_mirror(parts,mname)
		elif len(parts)>1:
			ump.add_mirror(parts,"%s [TRACKS:%d]"%(mname,len(parts)),wait=0.2,missing="ignore")