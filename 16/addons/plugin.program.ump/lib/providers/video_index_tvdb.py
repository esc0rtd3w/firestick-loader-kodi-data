import random
import urlparse
from xml.dom import minidom
from operator import itemgetter
from datetime import date,datetime,timedelta
import calendar
import time
import xbmc
from third import humanize


mirror="http://thetvdb.com"

encoding="utf-8"
apikey="C738A0A57D46E2CC"
recnum=50

timeformat="%Y-%m-%d"
timegap=60*60*24

def str_int(x):
	return int(float(x))

def str_trim(x):
	return x.split(" (")[0]

def fix_airdate(x):
	try:
		t=time.strptime(x,timeformat)
		c=calendar.timegm(t)+timegap
		x=time.strftime(timeformat,time.gmtime(c))
	except:
		pass
	return x

def get_child_data(p,c,defval,func=None):
	i=p.getElementsByTagName(c)
	if len(i)==1 and not i[0] is None and not i[0].lastChild is None:
		if func is None:
			return i[0].lastChild.data
		else:
			return func(i[0].lastChild.data)
	else:
		return defval

def get_tvdb_art(ids):
	def get_id(id):
		p=ump.get_page("%s/api/%s/series/%s/banners.xml"%(mirror,apikey,str(id)),None,throttle=True)
		x=minidom.parseString(p)
		banners=x.getElementsByTagName("Banner")
		result[id]={
		"banner_series_text":{"local":[],"global":[],"rest":[]},
		"banner_series_graphical":{"local":[],"global":[],"rest":[]},
		"banner_series_blank":{"local":[],"global":[],"rest":[]},
		"poster_season":{"local":{},"global":{},"rest":{}},
		"banner_season":{"local":{},"global":{},"rest":{}},
		"poster":{"local":[],"global":[],"rest":[]},
		"fanart":{"local":[],"global":[],"rest":[]},
		}
		for banner in banners:
			bpath=banner.getElementsByTagName("BannerPath")
			btype1=banner.getElementsByTagName("BannerType")
			btype2=banner.getElementsByTagName("BannerType2")
			lng=banner.getElementsByTagName("Language")

			key="rest"
			if len(lng)>0 and not lng[0].lastChild is None:
				if lng[0].lastChild.data == language:
					key="local"
				elif lng[0].lastChild.data == "en":
					key="global"

			if len(bpath)==1 and len(btype1)==1 and btype1[0].lastChild.data=="poster":
				result[id]["poster"][key].append(bpath[0].lastChild.data)
			if len(bpath)==1 and len(btype1)==1 and btype1[0].lastChild.data=="fanart":
				result[id]["fanart"][key].append(bpath[0].lastChild.data)
			if len(bpath)==1 and len(btype1)==1 and btype1[0].lastChild.data=="season":
				for ref,db in [("season","poster_season"),("seasonwide","banner_season")]:
					if len(btype2[0].lastChild.data) and btype2[0].lastChild.data==ref:
						s=int(banner.getElementsByTagName("Season")[0].lastChild.data)
						if s:
							if s in result[id][db][key].keys() and isinstance(result[id][db][key][s],list):
								result[id][db][key][s].append(bpath[0].lastChild.data)
							else:
								result[id][db][key][s]=[bpath[0].lastChild.data]
			
			if len(bpath)==1 and len(btype1)==1 and btype1[0].lastChild.data=="series":
				for ref,db in [("text","banner_series_text"),("graphical","banner_series_graphical"),("blank","banner_series_blank")]:
					if len(btype2[0].lastChild.data) and btype2[0].lastChild.data==ref:
						result[id][db][key].append(bpath[0].lastChild.data)

	result={}

	gid=ump.tm.create_gid()
	for id in ids:
		ump.tm.add_queue(get_id,(id,),gid=gid)
	
	ump.tm.join(gid=gid,cnt="all")
	return result

def get_tvdb_info(ids,force_lang=False):
	if not force_lang:
		force_lang=language

	def get_id(id,lng):
		p=ump.get_page("%s/api/%s/series/%s/%s.xml"%(mirror,apikey,str(id),lng),None)
		x=minidom.parseString(p)
		serie=x.getElementsByTagName("Series")[0]
		info={}
		art={}
		infolabels={
			"ContentRating":("mpaa","",None),
			"FirstAired":("aired","",fix_airdate),
			"IMDB_ID":("code","",None),
			"id":("code2","",None),
			"zap2it_id":("code10","",None),
			"Network":("studio","",None),
			"Overview":("plotoutline","",None),
			"Overview":("plot","",None),
			"Rating":("rating","",float),
			"RatingCount":("votes","",str_int),
			"SeriesName":("localtitle",None,str_trim),
			"added":("dateadded","",None),
			}

		artlabels={
			"banner":("banner","",None),
			"fanart":("fanart","",None),
			"poster":("poster","",None),
			"thumb":("poster","",None),
			}

		for i in infolabels.keys():
			info[infolabels[i][0]]=get_child_data(serie,i,infolabels[i][1],infolabels[i][2])
		
		if info["localtitle"] is None:info.pop("localtitle")
		if len(info["aired"])>4: info["year"]=int(info["aired"][:4])
		for a in artlabels.keys():
			art[a]="%s/banners/%s"%(mirror,get_child_data(serie,artlabels[a][0],artlabels[a][1],artlabels[a][2]))
		
		actors=get_child_data(serie,"Actors","")
		actors=[x for x in actors.split("|") if not x==""]
		info["cast"]=actors

		genre=get_child_data(serie,"Genre","")
		genre=genre.replace("|"," ")
		info["genre"]=genre
		info["code"]=id
		
		result[id]={"info":info,"art":art}

	result={}

	gid=ump.tm.create_gid()
	for id in ids:
		ump.tm.add_queue(get_id,(id,force_lang),gid=gid)
	
	ump.tm.join(gid=gid,cnt="all")
	return result

def get_tvdb_episodes(ids,arts):
	def get_id(id):
		p=ump.get_page("%s/api/%s/series/%s/all/%s.xml"%(mirror,apikey,str(id),language),None)
		x=minidom.parseString(p)
		seasons=x.getElementsByTagName("Combined_season")
		seasons=set([x1.lastChild.data for x1 in seasons])
		epis={}
		for s in seasons:
			epis[int(s)]={"info":{"title":"Season %s"%(str(s),)},"art":make_art(arts[id],int(s)),"episode":{}}
		episodes=x.getElementsByTagName("Episode")
		infolabels={
			"Combined_episodenumber":("episode",-1,str_int),
			"Combined_season":("season",-1,str_int),
			"Director":("director","",None),
			"EpImgFlag":("EpImgFlag",-1,str_int),
			"EpisodeName":("title","",None),
			"EpisodeNumber":("EpisodeNumber",-1,str_int),
			"FirstAired":("aired","",fix_airdate),
			"GuestStars":("GuestStars","",None),
			"Language":("Language","",None),
			"Overview":("plot","",None),
			"Rating":("rating","",float),
			"RatingCount":("votes","",str_int),
			"SeasonNumber":("SeasonNumber","",str_int),
			"Writer":("writer","",None),
			"lastupdated":("dateadded","",None),
			"absolute_number":("absolute_number",-1,str_int),
			}
		artlabels={
			"filename":("thumb","",None),
			}
		for e in episodes:
			epiinfo=ump.info.copy()
			for i in infolabels.keys():
				epiinfo[infolabels[i][0]]=get_child_data(e,i,infolabels[i][1],infolabels[i][2])
			epiart=make_art(arts[id],-1)
			for a in artlabels.keys():
				epiart[artlabels[a][0]]="%s/banners/%s"%(mirror,get_child_data(e,a,artlabels[a][1],artlabels[a][2]))
			epiart["poster"]=epiart["thumb"]
			season=epiinfo["season"]
			episode=epiinfo["episode"]
			epiinfo["mediatype"]=ump.defs.MT_EPISODE
			epis[season]["episode"][episode]={"info":epiinfo,"art":epiart}
		result[id]=epis
	result={}
	gid=ump.tm.create_gid()
	for k in range(len(ids)):
		ump.tm.add_queue(get_id,(ids[k],),gid=gid)
	
	ump.tm.join(gid=gid,cnt="all")
	return result	


def make_art(art,season=-1,banner_tables=["text","graphical","blank"]):
	#make art not war
	def selectrandom(typ):
		selected="DefaultFolder.png"
		for lng in ["local","global","rest"]:
			if season==-1 or typ=="fanart":
				if not typ == "banner":
					if len(art[typ][lng]):
						selected=random.choice(art[typ][lng])
						break
				else:
					if selected=="DefaultFolder.png":
						for banner_table in banner_tables:
							if len(art["banner_series_"+banner_table][lng]):
								selected=random.choice(art["banner_series_"+banner_table][lng])
								break
			else:
				if typ=="poster":typ="poster_season"
				if typ=="banner":typ="banner_season"
				if season in art[typ][lng].keys() and len(art[typ][lng][season]):
					selected=random.choice(art[typ][lng][season])
					break
		return selected

	xart={
		"thumb":"%s/banners/%s"%(mirror,selectrandom("poster")),
		"poster":"%s/banners/%s"%(mirror,selectrandom("poster")),
		"banner":"%s/banners/%s"%(mirror,selectrandom("banner")),
		"fanart":"%s/banners/%s"%(mirror,selectrandom("fanart")),
		"clearart":"",
		"clearlogo":"",
		"landscape":""
		}
	return xart

def run(ump):
	globals()['ump'] = ump
	ump.publish("tvshow")
	language=ump.backwards.getLanguage(0).lower()
	if not language in ["en","sv","no","da","fi","nl","de","it","es","fr","pl","hu","el","tr","ru","he","ja","pt","zh","cs","sl","hr","ko"]:language="en"
	globals()["language"] = language
	if ump.page == "root":
		ump.index_item("Search","search",args={"search":True})
		ump.index_item("My Episodes","myepisodes")

	elif ump.page == "search":
		what=ump.args.get("title",None)
		if what is None:
			conf,what=ump.get_keyboard('default', 'Search Series', True)
		q={"seriesname":what,"language":"all"}
		p=ump.get_page("%s/api/GetSeries.php"%mirror,None,query=q)
		x=minidom.parseString(p)
		series=x.getElementsByTagName("Series")
		names={}
		suggest=""
		otherids=[]
		processed=[]
		for s in series:
			sid=s.getElementsByTagName("seriesid")[0].lastChild.data
			if sid in processed:
				continue
			else:
				processed.append(sid)
			lang=s.getElementsByTagName("language")[0].lastChild.data
			if not lang == "":
				otherids.append(sid)
			if not sid in names.keys():
				names[sid]={}
			sname=s.getElementsByTagName("SeriesName")[0].lastChild.data
			names[sid]["title"]=names[sid]["tvshowtitle"]=names[sid]["localtitle"]=names[sid]["originaltitle"]=sname.split(" (")[0]
			alternates=list(set([x.split(" (")[0] for x in get_child_data(s,"AliasNames","").split("|")]))
			for k in range(len(alternates)):
				if alternates[k]=="": alternates.pop(k)
			if "alternates" in names[sid].keys():
				names[sid]["alternates"].extend(alternates)
			else:
				names[sid]["alternates"]=alternates

		#get english names locally returned values
		if len(otherids):
			other_data=get_tvdb_info(otherids,"en")
			for otherid in otherids:
				if "localtitle" in other_data[otherid]["info"].keys():
					names[otherid]["originaltitle"]=other_data[otherid]["info"]["localtitle"]

		#if there is no result do a google search
		if len(names)==0:
			suggest="[SUGGESTED] "
			sug_ids=[]
			urls=ump.web_search("inurl:thetvdb.com/?tab=series %s"%what)
			if not urls:
				return None
			for u in urls:
				idx=urlparse.parse_qs(urlparse.urlparse(u).query).get("id",None)
				if not idx:
					continue
				sug_ids.append(idx[0])
			sug_data=get_tvdb_info(sug_ids,"en")
			for sug_id in sug_ids:
				names[sug_id]={}
				names[sug_id]["title"]=names[sug_id]["tvshowtitle"]=names[sug_id]["localtitle"]=names[sug_id]["originaltitle"]=sug_data[sug_id]["info"]["localtitle"]
				names[sug_id]["alternates"]=[]


		data=get_tvdb_info(names.keys())
		for id in data.keys():
			names[id].update(data[id]["info"])
			commands=[]
			commands.append(('Search on IMDB : %s'%names[id]["tvshowtitle"], 'XBMC.Container.Update(%s)'%ump.link_to("results_title",{"title":names[id]["tvshowtitle"],"title_type":"tv_series,mini_series","sort":"moviemeter,asc"},module="imdb")))
			commands.append(('Search on ANN : %s'%names[id]["tvshowtitle"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":names[id]["tvshowtitle"]},module="ann")))
			for person in data[id]["info"].get("cast","")[:3]:
				if not person=="":
					commands.append(('Search Actor: %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person},module="imdb")))
			ump.index_item(suggest+names[id]["localtitle"],"seasons",{"tvdbid":id},info=names[id],art=data[id]["art"],cmds=commands,mediatype=ump.defs.MT_TVSHOW)

	elif ump.page == "seasons":
		id=ump.args.get("tvdbid",None)
		if not id:
			return None
		arts=get_tvdb_art([id])
		epis=get_tvdb_episodes([id],arts)[id]
		#todo get names in all langs

		for sno in sorted(epis.keys(),reverse=True):
			info=ump.info.copy()
			info["season"]=sno
			ump.index_item("Season %d"%sno,"episodes",{"tvdbid":id,"season":sno},art=epis[sno]["art"],info=info,mediatype=ump.defs.MT_SEASON)
			
	elif ump.page == "episodes":
		#xbmc.executebuiltin("XBMC.Container.Update(plugin://plugin.program.ump/?test=123)")
		id=ump.args.get("tvdbid",None)
		season=ump.args.get("season",None)
		if not id or not season:
			return None
		arts=get_tvdb_art([id])
		epis=get_tvdb_episodes([id],arts)[id][season]
		for epno in sorted([int(x) for  x in epis["episode"].keys()],reverse=True):
			#json keys are strings :(
			commands=[]
			commands.append(('Search on IMDB : %s'%epis["episode"][epno]["info"]["tvshowtitle"], 'XBMC.Container.Update(%s)'%ump.link_to("results_title",{"title":epis["episode"][epno]["info"]["tvshowtitle"],"title_type":"tv_series,mini_series","sort":"moviemeter,asc"},module="imdb")))
			commands.append(('Search on ANN : %s'%epis["episode"][epno]["info"]["tvshowtitle"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":epis["episode"][epno]["info"]["tvshowtitle"]},module="ann")))
			for person in epis["episode"][epno]["info"].get("cast","")[:3]:
				if not person=="":
					commands.append(('Search Actor: %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person},module="imdb")))
			for person in epis["episode"][epno]["info"].get("director","").split(","):
				if not person=="":
					commands.append(('Search Director : %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person},module="imdb")))
			ump.index_item("%dx%d %s"%(season,epno,epis["episode"][epno]["info"]["title"]),"urlselect",info=epis["episode"][epno]["info"],art=epis["episode"][epno]["art"],cmds=commands,mediatype=ump.defs.MT_EPISODE)
	
	elif ump.page=="myepisodes":
		dt = date.today()
		ws=time.strftime("%Y-%m-%d",(dt+timedelta(days=-7)).timetuple())
		we=time.strftime("%Y-%m-%d",(dt+timedelta(days=+7)).timetuple())
		ump.index_item("Last + This Week","agenda",args={"seen":True,"start":ws,"end":we,"human":True})
		for i in range(8):
			day=dt+timedelta(days=i-1)
			if i== 0: dayname="Yesterday"
			elif i== 1: dayname="Today"
			elif i==2: dayname="Tomorrow"
			else:dayname=calendar.day_name[day.weekday()]
			filter=time.strftime("%Y-%m-%d",day.timetuple())
			ump.index_item(dayname,"agenda",args={"seen":True,"start":filter,"end":filter})
		ump.index_item("All Unseen","agenda",args={"seen":True,"human":True})
		ump.index_item("All Seen","agenda",args={"seen":False,"human":True,"reverse":True})
	elif ump.page=="agenda":
		from ump import bookmark
		seenfilter=ump.args.get("seen",True)
		startfilter=ump.args.get("start",None)
		human=ump.args.get("human",False)
		rev=ump.args.get("reverse",False)
		if startfilter:
			startfilter=calendar.timegm(time.strptime(startfilter,"%Y-%m-%d"))
		endfilter=ump.args.get("end",None)
		if endfilter:
			endfilter=calendar.timegm(time.strptime(endfilter,"%Y-%m-%d"))
		favs=bookmark.load()[1]
		codes=[]
		for fav in favs:
			wid,name,thumb,data,cat,module,page,args,info,art=fav
			indexer=info.get("index",None)
			code=info.get("code",None)
			if code and indexer=="video_index_tvdb":
				codes.append(code)
		if not len(codes):
			ump.dialog.ok("No Bookmark","There is no bookmark that created from TVDB. Please bookmark a serie to track. [COLOR orange]WARNING: This function only works with bookmarks created UMP 0.0.89 or later. If you have older bookmarks you have to recreate your bookmarks to track releases.[/COLOR]")
			return
		tvdb=get_tvdb_info(codes)
		episodes=[]
		for code,tvshow in get_tvdb_episodes(codes,get_tvdb_art(codes)).iteritems():
			for season in sorted(tvshow.keys(),reverse=True):
				if season==0:continue
				for episode in tvshow[season]["episode"].keys():
					data=tvshow[season]["episode"][episode]
					info=data["info"]
					art=data["art"]
					airtime=ump.stats.gettime(info)
					if airtime:
						if startfilter and airtime<startfilter:continue
						if endfilter and airtime>endfilter:continue
						einfo=tvdb[code]["info"].copy()
						einfo.update(info)
						einfo["tvshowtitle"]=einfo["localtitle"]
						info["mediatype"]==ump.defs.MT_EPISODE
						isseen=bool(ump.stats.isseen(einfo))
						if not isseen==seenfilter:
							episodes.append([code,season,episode,einfo,art,airtime])
		if not len(episodes):
			ump.dialog.notification("No Episode","TVDB cant find any episode to track in this view")
			return
		for episode in  sorted(episodes,key=itemgetter(5),reverse=rev):
			code,season,epi,info,art,airtime=episode
			
			ename="%s %dx%d %s"%(info["localtitle"],season,epi,info["title"])
			if human:
				airdt=datetime.utcfromtimestamp(airtime)
				ename="[COLOR blue][%s][/COLOR] %s"%(humanize.naturaltime(airdt),ename)
			ump.index_item(ename,"urlselect",mediatype=ump.defs.MT_EPISODE,info=info,art=art)