from datetime import date
import httplib
import json
import re
import time
from urllib import quote_plus
from urllib import urlencode
import urlparse
from xml.dom import minidom

import xbmc
import xbmcgui
import xbmcplugin

import dateutil.parser as dparser


recnum=50

domain="http://www.animenewsnetwork.com"
encoding="utf-8"
stype="manga"

def scrape_ann_search(page):
	t1=time.time()
	m1=[]
	res=minidom.parseString(page)
	medias=res.getElementsByTagName(stype)
	for media in medias:
		img=""
		title=""
		orgtitle=""
		outline=""
		gen=""
		year=""
		dates=[]
		votes=""
		volumes={}
		dir=""
		cast=[]
		mpaa=""
		runtime=""
		rating=float(0)
		id="!ann!"+str(media.getAttribute("id"))

		for info in media.getElementsByTagName("info"):
			t=info.getAttribute("type")
			#image
			if t=="Picture":
				img=info.lastChild.getAttribute("src")
			if t=="Main title":
				title=info.lastChild.data
			if t=="Alternative title" and info.getAttribute("lang")=="JA":
				orgtitle=info.lastChild.data
			if t=="Plot Summary":
				outline+=info.lastChild.data
			if t=="Genres" or t=="Themes":
				gen+=info.lastChild.data+"/"
			if t=="Vintage":
				try:
					dates.append(dparser.parse(info.lastChild.data,fuzzy=True).year)
				except:
					pass
		for release in media.getElementsByTagName("release"):
			volno=re.findall(title+" \(GN\s([0-9]*?)\)",release.lastChild.data)
			volimg=urlparse.parse_qs(urlparse.urlparse(release.getAttribute("href")).query).get("id")[0]
			if len(volno)==1:
				volumes[volno[0]]=volimg
		
		if len(volumes.keys())<1:
			ump.add_log("Skipping Manga %s:%s since no volumes exists"%(id,title))
			continue

		for rate in media.getElementsByTagName("ratings"):
			rating=float(rate.getAttribute("weighted_score"))
			votes=rate.getAttribute("nb_votes")

		for staff in media.getElementsByTagName("staff"):
			if staff.firstChild.firstChild.data=="Story & Art":
				dir=staff.getElementsByTagName("person")[0].firstChild.data

		if not gen=="":
			gen=gen[0:-1]
		if len(dates)>0:
			dates.sort
			year=str(dates[0])
	
		data={}
		data["info"]={
			"count":len(volumes.keys()),
			"size":0, 
			#"date":"01-01-1970",
			"genre":gen,
			"year":year,
			"episode":-1,
			"season":-1,
			"top250":-1,
			"tracknumber":-1,
			"rating":rating,
			"playcount":-1,
			"overlay":0,
			"cast":cast,
			"castandrole":cast,
			"director":dir,
			"mpaa":mpaa,
			"plot":outline,
			"plotoutline":outline,
			"title":title,
			"originaltitle":orgtitle,
			"sorttitle":"",
			"duration":runtime,
			"studio":"",
			"tagline":"",
			"write":"",
			"tvshowtitle":"",
			"premiered":"",
			"status":"",
			"code":id,
			"aired":"",
			"credits":"",
			"lastplayed":"",
			"album":"",
			"artist":([]),
			"votes":"",
			"trailer":"",
			"dateadded":"",
			}
		data["art"]={
			"thumb":img,
			"poster":img,
			"banner":"",
			"fanart":"",
			"clearart":"",
			"clearlogo":"",
			"landscape":""
			}
		data["volumes"]=volumes #special only for this indexer
		m1.append(data)
	
	return m1

def update(volumes):
	vols={}
	def update(vol):
		#sorry for the mess :( ann is sucky about providing volume covers
		conn = httplib.HTTPConnection("www.animenewsnetwork.com")
		cover="/thumbnails/area200x300/releases/%s.jpg"%volumes[str(vol)]
		conn.request("HEAD", cover)
		res = conn.getresponse()
		if not res.status==200:
			link=domain+"/compare-prices/%s/stores.ajax?cover_placeholder=1"%volumes[str(vol)]
			src=ump.get_page(link,None,head={"X-Requested-With":"XMLHttpRequest"})
			cover=re.findall('img src="(.*?)"',src)
			if len(cover)>0:
				cover=cover[0]
			else:
				cover=""
				ump.add_log("Cant find volume cover of Volume %s for %s"%(str(vol),ump.info["title"]))
		vols[int(vol)]=domain+cover

	for vol in volumes.keys():
		ump.tm.add_queue(update,(vol,))
	
	ump.tm.join()
	return vols

def run(ump):
	globals()['ump'] = ump
	cacheToDisc=True
	if ump.page == "root":
		li=xbmcgui.ListItem("Search", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("search"),li,True)

	elif ump.page == "search":
		kb = xbmc.Keyboard('default', 'Search %s'%stype, True)
		kb.setDefault("")
		kb.setHiddenInput(False)
		kb.doModal()
		what=kb.getText()
		q={"id":155,"type":stype,"search":what}
		res=ump.get_page(domain+"/encyclopedia/reports.xml",None,query=q)
		res=minidom.parseString(res)
		items=res.getElementsByTagName("item")
		ids=[]
		for item in items:
			ids.append(item.getElementsByTagName("id")[0].firstChild.data)

		li=xbmcgui.ListItem("Found %d %s(s) for %s" % (len(items),stype,what), iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=ump.link_to("results_search",{stype:ids,"content_cat":ump.defs.CC_TVSHOWS})
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
	
	elif ump.page == "results_search":
		ump.set_content(ump.args["content_cat"])
		res=ump.get_page(domain+"/encyclopedia/api.xml?"+stype+"="+"/".join(ump.args[stype]),None)
		medias=scrape_ann_search(res)
		if len(medias) > 0: 
			for media in medias:
				li=xbmcgui.ListItem(media["info"]["title"])
				li.setInfo(ump.defs.CT_IMAGE,media["info"])
				try:
					li.setArt(media["art"])
				except AttributeError:
					#backwards compatability
					pass
				ump.art=media["art"]
				ump.info=media["info"]
				u=ump.link_to("show_volumes",{"volumes":media["volumes"]})
				xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
		cacheToDisc=False
	
	elif ump.page== "show_volumes":
		volumes=ump.args["volumes"]
		t1=time.time()
		volumes=update(volumes)
		for vol in sorted(volumes.keys(),reverse=True):
			li=xbmcgui.ListItem("Volume %d"%vol)
			ump.info["season"]=vol
			li.setIconImage(volumes[vol])
			u=ump.link_to("urlselect")
			xbmcplugin.addDirectoryItem(ump.handle,u,li,False)			

	xbmcplugin.endOfDirectory(ump.handle,	cacheToDisc=cacheToDisc)