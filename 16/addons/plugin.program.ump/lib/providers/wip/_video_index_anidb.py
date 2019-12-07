# -*- coding: utf-8 -*-
import datetime
import httplib
import json
import operator
import re
import time
from urllib import quote_plus
from urllib import urlencode
import urlparse
from xml.dom import minidom
from xml.parsers import expat

import xbmc
import xbmcgui
import xbmcplugin

from third.dateutil import parser
from third.unidecode import unidecode


domain="http://anidb.net"
encoding="utf-8"

try:
	language=xbmc.getLanguage(0).lower()
except AttributeError:
	#backwards compatability
	language="en"

def latinise(text):
	# some roman chars are rare on daily usage, and everybody uses latin representatives. Dont know how romaji works in details.
	chars={
		333:"ou", #�?
		215:"x", #instead of × 
		8211:"-", # - instead of –
		}

	for char in chars.keys():
		text=text.replace(unichr(char),chars[char])
	return text

def request_ids(ids):
	medias={}
	def get_single(id):
		query={"client":"umpanidb","protover":"1","request":"anime","aid":id}
		res=ump.get_page("http://api.anidb.net:9001/httpapi",encoding,query=query)
		#no idea why chr 08 causes xml sructure error :/
		res=minidom.parseString(res.replace(chr(8),""))
		media=res.getElementsByTagName("anime")[0]
		localtitle=None
		originaltitle=None
		alts=cast=[]
		votes=userrating=rating=0
		studio=writer=director=creds=[]
		id=media.getAttribute("id")
		premiered= media.getElementsByTagName("startdate")[0].lastChild.data
		aired= media.getElementsByTagName("enddate")[0].lastChild.data
		year=int(startdate[0:4])
		for title in media.getElementsByTagName("title"):
			l=title.getAttribute("xml:lang")
			t=title.getAttribute("type")
			used=False
			if l==language and t in ["main","official"]:
				localtitle=title.lastChild.data
				used=True
			if l=="ja" and t in ["main","official"]:
				originaltitle=title.lastChild.data
				used=True
			if t=="main":
				maintitle=title.lastChild.data
				used=True
			if not used:
				alts.append(title.lastChild.data)

		for creator in media.getElementsByTagName("creators"):
			for name in creator.lastChild.data.getElementsByTagName("name"):
				t=name.getAttribute("type")
				if "Work" in t:
					studio.append(namr.lastChild.data)
				elif "Composition" in t:
					writer.append(name.lastChild.data)
				elif "Direction" in t:
					director.append(name.lastChild.data)
				else:
					creds.append(name.lastChild.data)
		
		for desc in media.getElementsByTagName("description"):
			plot=desc.lastChild.data
		
		for rate in media.getElementsByTagName("ratings"):
			for p in rate.lastChild.data.getElementsByTagName("permanent"):
				votes=int(p.getAttribute("count"))
				rating=float(p.lastChild.data)

			for t in rate.lastChild.data.getElementsByTagName("temporary"):
				votes=int(p.getAttribute("count"))
				urating=int(t.lastChild.data)

		for image in media.getElementsByTagName("image"):
			img="http://img7.anidb.net/pics/anime/"+image.lastChild.data
		
		for characters in media.getElementsByTagName("characters"):
			for character in characters.getElementsByTagName("character"):
				cast.append(character.getElementsByTagName("name")[0].lastChild.data)
		
		data={}
		data["info"]={
			"year":year,
			"episode":-1,
			"season":-1,
			"rating":rating,
			"userrating":urating,
			"cast":cast,
			"director":director.join(","),
			"plot":plot,
			"plotoutline":plot,
			"title":maintitle,
			"originaltitle":originaltitle,
			"tvshowtitle":main,
			"localtitle":localtitle,
			"alternates":alts,
			"studio":studio.join(","),
			"writer":writer.join(","),
			"premiered":premiered,
			"code4":id,
			"aired":aired,
			"votes":votes,
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
		medias[id]=data

	pDialog = xbmcgui.DialogProgress()
	pDialog.create('anidb', 'Retrieving Information')
	gid=ump.tm.create_gid()
	for i in range(len(ids)):
		pDialog.update(100*i/len(ids), 'Retrieving Information')
		ump.tm.add_queue(get_single,(ids[i],),gid=gid)
	ump.tm.join(gid=gid,cnt="all")
	pDialog.close()
	return medias

def grab_searches(link,maxpage=2):
	pages=[]
	pages.append(ump.get_page(link,encoding))
	num=re.findall("pg\=([0-9]*?)\"",pages[0])
	if len(num)<2: 
		return pages
	for i in range(1,int(num[-1])+1):
		link2="%s&pg=%d"%(link,i)
		pages.append(ump.get_page(link2,encoding))
		if i >= maxpage:
			break
	return pages

def getgenres(filter):
	ids=[]
	pages=grab_searches("%s/encyclopedia/search/genreresults?w=series&w=movies&o=rating&%s"%(domain,filter))
	for page in pages:
		ids.extend(re.findall("anime.php\?id=([0-9]*?)\"(.*?)</a>",page))
	return [x[0] for x in ids]

def results_search(animes):
	if isinstance(animes,unicode): items=eval(animes)
	index=ump.args.get("index",0)
	medias=animes[index*50:(index+1)*50]
#	medias=scrape_ann_search(anime)
	
	itemcount=0
	if len(medias) > 0: 
		if not index==0:
			li=xbmcgui.ListItem("Results %d-%d"%((index-1)*50+1,index*50))
			u=ump.link_to("results_search",{"animes":animes,"index":index-1})
			xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
		for media in medias:
			im=media.get("picurl","DefaultFolder.png")
			im=im.replace("-thumb.jpg","")
			im="http://"+im.split("/")[2]+"/pics/anime/"++im.split("/")[-1]
			li=xbmcgui.ListItem("%s (%s)"%(media["name"],media["desc"]), iconImage=im, thumbnailImage=im)
			ump.set_content(ump.defs.CC_MOVIES)
			itemcount+=1
			if len(media["episodes"].keys())==0:
				u=ump.link_to("urlselect")
				xbmcplugin.addDirectoryItem(ump.handle,u,li,False)
			else:
				u=ump.link_to("show_episodes",{"annid":media["info"]["code3"]})
				xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
		if (index+1)*50 < len(animes) and not itemcount==0:
			li=xbmcgui.ListItem("Results %d-%d"%((index+1)*50+1,(index+2)*50))
			u=ump.link_to("results_search",{"anime":animes,"filters":filters,"index":index+1})
			xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
	cacheToDisc=False

def run(ump):
	globals()['ump'] = ump
	cacheToDisc=False
	if ump.page == "root":
		li=xbmcgui.ListItem("Search", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("search"),li,True)

		li=xbmcgui.ListItem("Top Rated Animes", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("select_year"),li,True)

		li=xbmcgui.ListItem("Newest Animes", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("newest"),li,True)

		li=xbmcgui.ListItem("Animes by Genre", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("bygenre"),li,True)

		li=xbmcgui.ListItem("Animes by Themes", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("bytheme"),li,True)

	elif ump.page == "bygenre":
		genres={
			"Adventure":"adventure/A",
			"Comedy":"comedy",
			"Drama":"drama/D",
			"Slice Of Life":"slice%20of%20life/D",
			"Fantasy":"fantasy/F",
			"Magic":"magic/F",
			"Supernatural":"supernatural/F",
			"Horror":"horror",
			"Mystery":"mystery",
			"Psychological":"psychological",
			"Romance":"romance",
			"Science Fiction":"science%20fiction",
			"Thriller":"thriller",
			"Tournament":"tournament",
			"Erotic":"erotica",
			}
			
		for genre in sorted(genres.keys()):
			li=xbmcgui.ListItem(genre, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
			args={"anime":"getgenres('%s')"%urlencode({"g":genres[genre]}),"filters":["numvotes"]}
			xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("results_search",args),li,True)
	
	elif ump.page == "bytheme":
		themes=re.findall('name="th" type="checkbox" value="(.*?)".*?\(([0-9]*?)\)',ump.get_page("%s/encyclopedia/search/genre"%domain,None))
		addthemes=[]
		for theme,count in sorted([(x[0],int(x[1])) for x in themes], key=operator.itemgetter(1),reverse=True):
			if not theme in addthemes:
				addthemes.append(theme)
				li=xbmcgui.ListItem("%s (%d)"%(theme.title().replace("|"," / "),count), iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
				args={"anime":"getgenres('%s')"%urlencode({"th":theme}),"filters":[]}
				xbmcplugin.addDirectoryItem(ump.handle,ump.link_to("results_search",args),li,True)
	
	elif ump.page == "newest":
		ids=[]
		dates=[]
		months=[]
		pages=grab_searches("%s/encyclopedia/search/genreresults?w=series&w=movies&from=%d&to=%d&lic=&a=AA&a=OC&a=TA&a=MA&a=AO&o=rating"%(domain, datetime.datetime.now().year, datetime.datetime.now().year))
		for page in pages:
			ids.extend(re.findall("anime.php\?id=([0-9]*?)\"",page))
			dates.extend(re.findall("class=\"de\-emphasized\">(.*?)<",page))
		
		for i in range(len(dates)):
			since=(datetime.datetime.now() - parser.parse(dates[i],fuzzy=True,default=datetime.datetime(1970, 1, 1, 0, 0))).days
			if  since<= 15 and since >=0:
				months.append(ids[i])

		li=xbmcgui.ListItem("Last 15 Days", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=ump.link_to("results_search",{"anime":months,"filters":[]})
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
		
		li=xbmcgui.ListItem("This Year", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=ump.link_to("results_search",{"anime":ids,"filters":[]})
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
				

	elif ump.page == "select_year":
		li=xbmcgui.ListItem("All Time", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		args={"anime":"getgenres('')","filters":["numvotes"]}
		u=ump.link_to("results_search",args)
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
		for year in reversed(range(datetime.date.today().year-50,datetime.date.today().year+1)):
			args={"anime":"getgenres('%s')"%urlencode({"from":year,"to":year}),"filters":["numvotes"]}
			li=xbmcgui.ListItem(str(year), iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
			u=ump.link_to("results_search",args)
			xbmcplugin.addDirectoryItem(ump.handle,u,li,True)

	elif ump.page == "toprated":
		ids=[]
		pages=grab_searches("%s/encyclopedia/search/genreresults?w=series&w=movies&from=%s&to=%s&lic=&a=AA&a=OC&a=TA&a=MA&o=rating"%(domain,ump.args["year"],ump.args["year"]))
		for page in pages:
			ids.extend(re.findall("anime.php\?id=([0-9]*?)\"(.*?)</a>",page))

		li=xbmcgui.ListItem("Show Both", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=ump.link_to("results_search",{"anime":[x[0] for x in ids],"filters":[]})
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)
		
		li=xbmcgui.ListItem("Show only series", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=ump.link_to("results_search",{"anime":[x[0] for x in ids if not "(movie)" in x[1]],"filters":[],"filters":[]})
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)

		li=xbmcgui.ListItem("Show only movies", iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
		u=ump.link_to("results_search",{"anime":[x[0] for x in ids if "(movie)" in x[1]],"filters":[]})
		xbmcplugin.addDirectoryItem(ump.handle,u,li,True)

	elif ump.page == "search":
		kb = xbmc.Keyboard('default', 'Search Anime', True)
		kb.setDefault("")
		kb.setHiddenInput(False)
		kb.doModal()
		what=kb.getText()
		q={"task":"search","query":what}
#		anisearch.outrance.pl/?task=search&query=bleach
#"		http://anidb.net/perl-bin/animedb.pl?show=json&action=search&type=anime&query=ble"
		pg=ump.get_page("http://anisearch.outrance.pl",encoding,query=q)
		ids=re.findall('aid="(.*?)"',pg)
		if len(ids):
			request_ids(ids)
	
	elif ump.page == "results_search":
		results_search()
	
	elif ump.page== "show_episodes":
		annid=ump.args.get("annid",None)
		if annid is None:
			return None
		medias=scrape_ann_search([annid])
		if len(medias)<1:
			return None
		episodes=medias[0]["episodes"]
		ump.info=medias[0]["info"]
		#keys are parsed as strings
		for k,v in episodes.items():
			episodes.pop(k)
			episodes[int(float(k))]=v
		#below does not work on old versions of python
		#episodes = {float(k):v for k,v in episodes.iteritems()}
		ump.set_content(ump.defs.CC_EPISODES)
		for epi in sorted(episodes.keys(),reverse=True):
			li=xbmcgui.ListItem("%d %s"%(epi,episodes[epi]["title"]))
			try:
				li.setArt(ump.art)
			except AttributeError:
				#backwards compatability
				pass
			ump.info["title"]=episodes[epi]["title"]
			ump.info["episode"]=episodes[epi]["relativenumber"]
			#even though animes dont have season info force it so trakt will scrobble
			ump.info["season"]=1
			ump.info["absolute_number"]=epi
			u=ump.link_to("urlselect")
			li.setInfo(ump.defs.CT_VIDEO,ump.info)
			xbmcplugin.addDirectoryItem(ump.handle,u,li,False)

	xbmcplugin.endOfDirectory(ump.handle,cacheToDisc=cacheToDisc,updateListing=False,succeeded=True)