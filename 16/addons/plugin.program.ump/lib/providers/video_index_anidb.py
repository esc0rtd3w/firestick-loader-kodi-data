# -*- coding: utf-8 -*-
import os
from xml.dom import minidom
import xbmc
import time
from ump import dom
import datetime
import re
import md5
from ump import prefs
from third.dateutil import parser
import HTMLParser

html=HTMLParser.HTMLParser()

lt=2.1 # query limit in seconds for api
ul=60*60*24 #cache refresh limit in seconds (1 day) for api
lthttp=3 # query limit in seconds for web scraper
ulhttp=60*60*24*7  #cache refresh limit in seconds (1 day) for web scraper
cd="anidb" #dir to cache the query results 
extu="http://anisearch.outrance.pl/"
apiu="http://api.anidb.net:9001/httpapi"
psrv="http://img7.anidb.net/pics/anime/"
encoding="utf-8"
cid="umpanidb" #httpapi cliend id
cver="1" #httpsapi clientver
pver="1"
langmap={"x-jat":"ja","zh-Hans":"zh","pt-BR":"pt","x-unk":"ja","zh-Hant":"zh","es-LA":"es","x-other":"en","x-kot":"ko"}
publish="anime"

def command(request,args={}):
	last=prefs.get("anidb","lasttime")
	if last == {}:last=time.time()
	comid=request
	for arg in args:
		comid+="_"+arg+"_"+args[arg]
	cf=os.path.join(ump.defs.addon_ddir,cd,comid)
	if (os.path.exists(cf+".xml") and time.time()-os.path.getmtime(cf+".xml")<ul):
		xml=dom.read(cf+".xml")
	elif os.path.exists(cf+"_perm.xml"):
		xml=dom.read(cf+"_perm.xml")
	else:
		while True:
			since=time.time()-last
			if since>lt:
				query={"request":request,"client":cid,"clientver":cver,"protover":pver}
				query.update(args)
				res=ump.get_page(apiu,encoding,query=query,throttle=False)
				prefs.set("anidb","lasttime",time.time())
				xmlstr=minidom.parseString(res.encode(encoding))
				#check if anime ended, if ended store permanently
				sd=re.findall("<startdate>(.*?)</startdate>",res)
				ed=re.findall("<enddate>(.*?)</enddate>",res)
				if len(ed) and len(sd) and parser.parse(ed[0])<datetime.datetime.now() and parser.parse(sd[0])<parser.parse(ed[0]):
					cf=cf+"_perm.xml"
				else:
					cf=cf+".xml"
				dom.write(cf,xmlstr)
				xml=dom.read(cf)
				break
			else:
				xbmc.sleep(100)
				percent=int(since/lt*100)
				ump.dialogpg.update(percent,"Waiting to Cache from Anidb Server for %s:%s"%(request,str(args)[1:-1]))
	return xml

def get_page(*args,**kwargs):
	last=prefs.get("anidb","lasttime")
	if "cachetime" in kwargs:
		ulhttp=kwargs.pop("cachetime")
	if last == {}:last=time.time()
	comid=md5.md5("http"+str(kwargs.get("query",{}))).hexdigest()
	cf=os.path.join(ump.defs.addon_ddir,cd,comid+".html")
	if os.path.exists(cf) and (time.time()-os.path.getmtime(cf)<ulhttp):
		f=open(cf)
		res=unicode(f.read().decode(encoding))
		f.close()
	else:
		while True:
			since=time.time()-last
			if since>lthttp:
				res=ump.get_page(*args,**kwargs)
				f=open(cf,"w")
				f.write(res.encode(encoding))
				f.close()
				prefs.set("anidb","lasttime",time.time())
				break
			else:
				xbmc.sleep(100)
				percent=int(since/lthttp*100)
				ump.dialogpg.update(percent,"Waiting to Cache from Anidb Server for %s"%args[0])	
	return res

def get_media(xml):
	mtypes={"TV Series":ump.defs.MT_TVSHOW,"Movie":ump.defs.MT_MOVIE,"Music Video":ump.defs.MT_MUSICVIDEO,"Other":ump.defs.MT_NONE}
	type="TV Series"
	startdate=""
	year=0
	lotitle="" #localized title 
	otitle="" #original title
	mtitle="" #main title
	etitle="" #english title
	director=""
	plot=""
	plotoutline=""
	rating=float(0)
	votes=""
	picture=""
	genre=""
	cast=[]
	epis={}
	alternates=[]
	anime=xml.getElementsByTagName("anime")
	code=""
	if len(anime):
		anime=anime[0]
		code=anime.getAttribute("id")
		#type
		xtype=anime.getElementsByTagName("type")
		if len(xtype):
			type=xtype[0].lastChild.data
			
		#year
		xyear=anime.getElementsByTagName("startdate")
		y=xyear[0].lastChild.data
		startdate=y
		year=int(xyear[0].lastChild.data[:4])
		try:
			year=datetime.datetime.strptime(xyear[0].lastChild.data,"%Y-%m-%d").year
		except:
			pass

		#name
		for t in anime.getElementsByTagName("titles"):
			for title in t.getElementsByTagName("title"):
				lan=title.getAttribute("xml:lang")
				ttype=title.getAttribute("type")
				if ttype in ["synonym","short"]:
					continue
				isalternate=True
				ttitle=title.lastChild.data
				ttitle=re.sub("(\s\([0-9]{4}\))","",ttitle)
				ttitle=ttitle.replace(chr(96),"'")
				if lan in langmap: 
					lan=langmap[lan]
				if mtitle=="" and ttype=="main":
					mtitle=ttitle
					mlang=lan
					isalternate=False
				if etitle=="" and lan=="en":
					etitle=ttitle
					isalternate=False
				if otitle=="" and lan=="ja":
					otitle=ttitle
					isalternate=False
				if lotitle=="" and lan==ump.backwards.getLanguage(0).lower():
					lotitle=ttitle
					isalternate=False
				if isalternate and ttitle not in alternates:
					alternates.append(html.unescape(ttitle))
		if not etitle == "" and not mlang == "en": mtitle=etitle
		if lotitle == "": lotitle=mtitle
		if otitle == "": otitle=mtitle
		
		#director
		for creator in anime.getElementsByTagName("creators"):
			for n in creator.getElementsByTagName("name"):
				ttype=n.getAttribute("type")
				if ttype=="Original Work":
					director=n.lastChild.data
					break
		
		#plot
		for desc in anime.getElementsByTagName("description"):
			plot=desc.lastChild.data
			plotoutline=plot
			break
		
		#rating
		for r in anime.getElementsByTagName("ratings"):
			for p in r.getElementsByTagName("permanent"):
				rating=float(p.lastChild.data)
				votes=p.getAttribute("count")
		
		#picture
		for p in anime.getElementsByTagName("picture"):
			picture=psrv+p.lastChild.data
			break
		
		#genre
		genre=[]
		for cat in anime.getElementsByTagName("tag"):
			genre.append(cat.getElementsByTagName("name")[0].lastChild.data)
		genre=", ".join(genre)
		
		#cast
		for c in anime.getElementsByTagName("character"):
			cast.append(html.unescape(c.getElementsByTagName("name")[0].lastChild.data))
		#epis
		ismovie=False
		for eps in anime.getElementsByTagName("episodes"):
			if ismovie: break
			for ep in eps.getElementsByTagName("episode"):
				if ismovie:break
				if not ep.getElementsByTagName("epno")[0].getAttribute("type")=="1":continue
				#epno
				epno=int(ep.getElementsByTagName("epno")[0].lastChild.data)
				
				#duration
				duration=""
				for d in ep.getElementsByTagName("length"):
					duration=int(d.lastChild.data)*60
					break
				
				#aired
				aired=""
				for a in ep.getElementsByTagName("airdate"):
					aired=a.lastChild.data
					break
				
				#rating/votes
				erating=float(0)
				evotes=""
				for r in ep.getElementsByTagName("rating"):
					erating=float(r.lastChild.data)
					evotes=r.getAttribute("count")
					break
					
				#titles
				elotitle="" #localized title 
				eotitle="" #original title
				emtitle="" #en title
				for title in ep.getElementsByTagName("title"):
					lan=title.getAttribute("xml:lang")
					if lan in langmap:lan=langmap[lan]
					if emtitle=="" and lan=="en":emtitle=title.lastChild.data
					if eotitle=="" and lan=="ja":eotitle=title.lastChild.data
					if elotitle=="" and lan==ump.backwards.getLanguage(0).lower():elotitle=title.lastChild.data		
				if elotitle == "": elotitle=emtitle
				if eotitle == "": eotitle=emtitle
				
				if ump.is_same(emtitle, "complete movie") and epno==1:ismovie=True			
				epis[epno]={"duration":duration,
						"aired":aired,
						"rating":erating,
						"votes":evotes,
						"eoriginaltitle":html.unescape(eotitle),
						"elocaltitle":html.unescape(elotitle),
						"title":html.unescape(emtitle),
						"episode":epno,
						"absolute_number":epno,
						"season":1}
	if type in mtypes:
		type=mtypes[type]
	elif len(epis):
		type=ump.defs.MT_TVSHOW
	else:
		type=ump.defs.MT_MOVIE
	
	info={
		"code":code,
		"year":year,
		"startdate":startdate,
		"localtitle":html.unescape(lotitle),
		"originaltitle":html.unescape(otitle),
		"alternates":alternates,
		"tvshowtitle":html.unescape(mtitle),
		"title":html.unescape(mtitle),
		"director":html.unescape(director),
		"plot":html.unescape(plot),
		"plotoutline":html.unescape(plotoutline),
		"rating":rating,
		"votes":votes,
		"genre":html.unescape(genre),
		"cast":cast,
		}
	
	if type==ump.defs.MT_TVSHOW:
		info["tvshowtitle"]=mtitle
		
	art={
		"thumb":picture,
		"poster":picture,
		"banner":"",
		"fanart":"",
		"clearart":"",
		"clearlogo":"",
		"landscape":""
		}
	if ismovie:
		info.update(epis[1])
		info["title"]=info["tvshowtitle"]
		info["tvshowtitle"]=""
		info["episode"]=1
		info["season"]=1
		info["absolute_number"]=1
		epis=[]
	return type,info,art,epis

def listitems(aids):
	processed=[]
	for aid in aids:
		if isinstance(aid,list) or isinstance(aid,tuple):
			aid=list(aid)
			suffix=" /"+"/".join(aid[1:])
			aid=aid[0]			
		else:
			suffix=""
		if aid in processed:
			continue
		else:
			processed.append(aid)
		c=command("anime",{"aid":aid})
		type,info,art,epis=get_media(c)
		if not len(epis):
			ump.index_item(info["localtitle"]+suffix,"urlselect",info=info,art=art,mediatype=ump.defs.MT_MOVIE)
		else:
			ump.index_item(info["localtitle"]+suffix,"episodes",info=info,art=art,args={"aid":aid},mediatype=ump.defs.MT_TVSHOW)
			
def run(ump):

	globals()['ump'] = ump
	ump.publish("anime")
	if not os.path.exists(os.path.join(ump.defs.addon_ddir,cd)):os.makedirs(os.path.join(ump.defs.addon_ddir,cd))
	
	if ump.page=="root":
		ump.index_item("Search Anime","search")
		regex='<div class="name"><a class="name-colored" href=".*?aid\=([0-9]*?)">.*?<div class="data">\s*?<div class="date">(.*?)\n\s*?</div>'
		args={"show":"calendar","do":"schedule","regex":regex,"rflag":re.DOTALL}
		#ump.index_item("Calendar","animedb",args=args)

		regex='</a></td><td class="name anime">\s*?<a href=".*?aid\=(.*?)"'
		args={"show":"latest2","do":"hotanime","regex":regex,"rflag":re.DOTALL}
		ump.index_item("Currently Popular","animedb",args=args)
		
		regex='<div class="name"><a class="name-colored" href=".*?aid\=(.*?)">'
		args={
			"Recently Started":{"show":"calendar","regex":regex},
			"Recently Ended":{"show":"calendar","cmode":"1","regex":regex}
			}
		ump.index_item("Recently Started/Ended","keylist",args=args)
		
		regex='<td data-label="Title" class="name main anime">\s*?<a href=".*?aid\=(.*?)">'
		args={
			"Best Of 2000s":{"show":"animelist","do.search":"Search","airdate1":"2010-01-01","airdate0":"2000-01-01","h":"1","votes":"1000","airing":"2","orderby.rating":"0.2","regex":regex,"rmode":re.DOTALL},
			"Best Of 1990s":{"show":"animelist","do.search":"Search","airdate1":"2000-01-01","airdate0":"1990-01-01","h":"1","votes":"1000","airing":"2","orderby.rating":"0.2","regex":regex,"rmode":re.DOTALL},
			"Best Of 1980s":{"show":"animelist","do.search":"Search","airdate1":"1990-01-01","airdate0":"1980-01-01","h":"1","votes":"1000","airing":"2","orderby.rating":"0.2","regex":regex,"rmode":re.DOTALL},
			"Best Of 1970s":{"show":"animelist","do.search":"Search","airdate1":"1980-01-01","airdate0":"1970-01-01","h":"1","votes":"100","airing":"2","orderby.rating":"0.2","regex":regex,"rmode":re.DOTALL},
			}
		ump.index_item("Best of 2K/90s/80s/70s","keylist",args=args)
		
		args={
			"Josei":{"show":"animelist","tag.2614":"0","do.search":"Search","orderby.ucnt":"0.2","regex":regex,"rmode":re.DOTALL},
			"Kodomo":{"show":"animelist","tag.1846":"0","do.search":"Search","orderby.ucnt":"0.2","regex":regex,"rmode":re.DOTALL},
			"Mina":{"show":"animelist","tag.2616":"0","do.search":"Search","orderby.ucnt":"0.2","regex":regex,"rmode":re.DOTALL},
			"Seinen":{"show":"animelist","tag.1802":"0","tag.2869":"-1","do.search":"Search","orderby.ucnt":"0.2","regex":regex,"rmode":re.DOTALL},
			"Shoujo":{"show":"animelist","tag.1077":"0","do.search":"Search","orderby.ucnt":"0.2","regex":regex,"rmode":re.DOTALL},
			"Shounen":{"show":"animelist","tag.922":"0","do.search":"Search","orderby.ucnt":"0.2","regex":regex,"rmode":re.DOTALL},
			}
		ump.index_item("Animes by Target Audience","keylist",args=args)
		
	if ump.page=="keylist":
		for k,v in ump.args.iteritems():
			ump.index_item(k,"animedb",args=v)
		
	elif ump.page=="search":
		what=ump.args.get("title",None)
		if what is None:
			conf,what=ump.get_keyboard('default', 'Search Anime', True)
		res=ump.get_page(extu,encoding,query={"task":"search","query":"\\"+what})
		res=minidom.parseString(res.encode(encoding))
		results=res.getElementsByTagName("anime")
		if len(results)<24:
			res=ump.get_page(extu,encoding,query={"task":"search","query":what})
			res=minidom.parseString(res.encode(encoding))
			results.extend(res.getElementsByTagName("anime"))
		listitems([x.getAttribute("aid") for x in results[:24]])
		
	elif ump.page=="episodes":
		type,info,art,epis=get_media(command("anime",{"aid":ump.args["aid"]}))
		epinfo=info.copy()
		for epno,epi in epis.iteritems():
			epinfo.update(epi)
			ump.index_item(str(epno)+". "+epinfo["elocaltitle"],"urlselect",info=epinfo,art=art,mediatype=ump.defs.MT_EPISODE)
		
	elif ump.page=="animedb":
		oldargs=ump.args.copy()
		regex=ump.args.pop("regex")
		if "rflag" in ump.args:
			rflag=ump.args.pop("rflag")
		else:
			rflag=0
		
		if "pagenum" in ump.args:
			pagenum=ump.args.pop("pagenum")
		else:
			pagenum=1
		
		cachetime=ulhttp
		if ump.args["show"]=="animelist":
			pagecap=30
			cachetime=60*60*24*7
		elif ump.args["show"]=="calendar":
			pagecap=99999999999 #those pages are single
			cachetime=60*60*12
		elif ump.args["show"]=="latest2":
			pagecap=49
			cachetime=60*60*12
		perpage=8
		pages={}
		for index in range((pagenum-1)*perpage,pagenum*perpage):
			inpage=int(index/pagecap)
			pointer=index%pagecap
			if not inpage in pages: 
				if inpage-1 in pages:
					pages[inpage]=[0,1]
				else:
					pages[inpage]=[pointer,pointer+pointer%perpage+1]
			else:
				pages[inpage][1]=pointer+1
		
		results=[]
		for page,index in pages.iteritems():
			start,end=index
			ump.args["page"]=page
			src=get_page("http://anidb.net/perl-bin/animedb.pl",encoding,query=ump.args,cachetime=cachetime)
			reg=re.findall(regex,src,rflag)
			results.extend(reg[start:end])
					
		listitems(results)
		if not len(results)<perpage or True:
			oldargs["pagenum"]=pagenum+1
			ump.index_item("Results %d - %d"%(pagenum*perpage+1,(pagenum+1)*perpage),"animedb",args=oldargs,noicon=True)
			