from datetime import date
import time
import json
import operator
import re

import xbmc

from ump import countries

def _match_list(ref,match,default=""):
	for i in range(len(ref)):
		if i+1>len(match):
			match.append(default)
	return match

def get_localtitle(alts,original):
	local=original
	ww=original
	for country in countries.all:
		cntry=country[0].lower()
		if cntry =="united states of america":cntry="usa"
		if ump.backwards.getLanguage(0).lower() == country[2] and cntry in alts.keys():
			local=alts[cntry]
	for key in alts.keys():
		if ump.is_same("master",key):
			ww=alts[key]		
			break
	if ww == original:
		for key in alts.keys():
			if ump.is_same("USA",key):
				ww=alts[key]		
				break
	if ww == original:
		for key in alts.keys():
			if ump.is_same("World-wide",key):
				ww=alts[key]		
				break
	return local,ww

def scrape_imdb_names(page):
	trs=re.findall('detailed"\>(.*?)\</tr\>',page,re.DOTALL)
	people=[]
	for tr in trs:
		#image
		main=re.findall('a href="/name/(nm[0-9]*?)/" title="(.*?)"><img src="(.*?)"',tr)
		person={}
		person["id"]=main[0][0]
		person["name"]=main[0][1]
		person["poster"]=main[0][2].split("._")[0]
		people.append(person)
	return people

def scrape_imdb_search(page):
	m1=[]
	trs=re.findall('<div class="lister-list">(.*?)<div id="sidebar">',page,re.DOTALL)
	if not len(trs):
		return []
	for tr in trs[0].split("lister-item mode-advanced")[1:]:
		#image
		poster=re.findall('img.*?loadlate="(.*?)"',tr,re.DOTALL)
		if len(poster)>0:
			poster=poster[0].split("._")[0]
		#title
		title=re.findall('img.*?alt="(.*?)"',tr,re.DOTALL)[0]
		
		#id
		id=re.findall('img.*?data-tconst="(.*?)"',tr,re.DOTALL)[0]

		#outline
		outline=re.findall('<p class="text-muted">\n(.*?)<',tr,re.DOTALL)
		if len(outline):
			outline=outline[0]
		else:
			outline=""

		#director/casting
		dir=""
		cast=[]
		dir_stars=re.findall('Directors?:(.*?)</p',tr,re.DOTALL)
		if not len(dir_stars):
			dir_stars=re.findall('(Stars:.*?)</p',tr,re.DOTALL)
		if len(dir_stars):
			if "Stars:" in dir_stars[0]:
				dirs,stars=dir_stars[0].split("Stars:")
			else:
				dirs=dir_stars[0]
				stars=""
			dir=", ".join(re.findall("\n>(.*?)</a",dirs,re.DOTALL))
			cast=re.findall("\n>(.*?)</a",stars,re.DOTALL)
		
		#genre
		gen=re.findall('class="genre"\>\n(.*?)\</span',tr)
		if len(gen):
			gen=gen[0]
		else:
			gen=""

		#year
		year=re.findall('<span class="lister-item-year text-muted unbold">.*?\(([0-9]{4})',tr)
		if len(year)>0:
			year=int(year[0])
		else:
			year=0

		#duration
		runtime=re.findall('class="runtime">([0-9].*?)\s',tr)
		if len(runtime):
			runtime=float(runtime[0])*60
		else:
			runtime=0

		#mpaa
		mpaa=re.findall('class="certificate">(.*?)</span',tr)
		if len(mpaa)>0:
			mpaa=mpaa[0]
		else:
			mpaa=""

		#rating
		rating=re.findall('class="value"\>(.*?)\</span',tr)
		if len(rating)>0:
			if "-" in rating[0][0]:
				rating=float(0)
			else:
				rating=float(rating[0].replace(",","."))
		else:
			rating=float(0)

		movie={}
		movie["info"]={
			"localtitle":title,
			"alternates":[],
			"count":1,
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
			"originaltitle":title,
			"sorttitle":"",
			"duration":runtime,
			"studio":"",
			"tagline":"",
			"write":"",
			"tvshowtitle":"",
			"tvshowalias":"",
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
			"dateadded":""
			}


		movie["art"]={
			"thumb":poster+"._V1_SX214_AL_.jpg",
			"poster":poster,
			"banner":"",
			"fanart":"",
			"clearart":"",
			"clearlogo":"",
			"landscape":""
			}
		m1.append(movie)
	
	def alternate(key,id):
		alts=scrape_name(id,True)
		altl=zip(*alts.items())
		if len(altl):
			m1[key]["info"]["alternates"]= altl[1]
		else:
			m1[key]["info"]["alternates"]= []
		m1[key]["info"]["localtitle"],m1[key]["info"]["title"]=get_localtitle(alts,m1[key]["info"]["originaltitle"])
	try:
		start,end,total=re.findall('<div id="left">\n(.*?)\-(.*?) of (.*?)\n',page)[0]
		start=int(start.replace(",",""))
		end=int(end.replace(",",""))
		total=int(total.replace(",",""))
	except:
		start=end=total=0

	gid=ump.tm.create_gid()
	for m in range(len(m1)):
		ump.tm.add_queue(alternate,(m,m1[m]["info"]["code"]),gid=gid)
	ump.tm.join(gid=gid,cnt="all")

	return start,end,total,m1


			

def scrape_name(id,lean=False):
	m1={"info":{},"art":{}}
	m1["info"]["originaltitle"]=""
	res=ump.get_page("http://www.imdb.com/title/%s/releaseinfo"%id,"utf-8",throttle=True)
	namediv=re.findall('<h3 itemprop="name">.*?itemprop=\'url\'>(.*?)</a>.*?<span class="nobr">(.*?)</span>',res,re.DOTALL)
	namestr,datestr=namediv[0]
	alts={"master":namestr}
	akas=re.findall('<table id="akas"(.*?)</table>',res,re.DOTALL)
	if len(akas)==1:
		tds=re.findall("<td>(.*?)</td>",akas[0])
		pcountry=[]
		for td in range(1,len(tds),2):
			country=tds[td-1]
			if any(word in country for word in ["fake","informal","version","literal","promotional","working"]) or ("USA" in country and "title" in country):
				continue
			country=re.sub("\s\(.*\)","",tds[td-1]).lower()
			if country in pcountry:
				continue
			pcountry.append(country)
			cname=tds[td]
			alts[country]=cname
		if lean:
			return alts
		else:
			poster=re.findall('<img itemprop="image"\nclass="poster".*?alt="(.*?)".*?src="(.*?)"',res,re.DOTALL)
			if len(namediv)==1:
				namestr,datestr=namediv[0]
				m1["info"]["originaltitle"]=namestr
				m1["info"]["year"]=int(re.sub("[^0-9]", "", datestr.split("-")[0]))
				m1["info"]["localtitle"],m1["info"]["title"]=get_localtitle(alts,namestr)
				m1["info"]["alternates"]= zip(*alts.items())[1]
			if len(poster)==1:
				namestr,link=poster[0]
				m1["art"]["poster"]=link.split("._")[0]
				m1["art"]["thumb"]=m1["art"]["poster"]+"._V1_SX214_AL_.jpg"
			m1["info"]["code"]=id
			return m1
	elif lean:
		return alts
	

def run(ump):
	globals()['ump'] = ump
	if ump.page == "root":
		ump.index_item("Search Movies","results_title",args={"title":"?","title_type":"feature,tv_movie,short","sort":"moviemeter,asc"})
		ump.index_item("Search Series","results_title",args={"title":"?","title_type":"tv_series,mini_series","sort":"moviemeter,asc"})		
		ump.index_item("Search Documentaries","results_title",args={"title":"?","title_type":"documentary","sort":"moviemeter,asc"})
		ump.index_item("Search People","results_name",args={"name":"?"})
		ump.index_item("Top Rated Movies","select_year",args={"at":"0","num_votes":"60000,","sort":"user_rating","title_type":"feature,tv_movie,short","next_page":"results_title"})
		ump.index_item("Top Voted Movies","select_year",args={"at":"0","sort":"num_votes,desc","title_type":"feature,tv_movie,short","next_page":"results_title"})
		ump.index_item("Top Box Office Movies","select_year",args={"at":"0","sort":"boxoffice_gross_us,desc","title_type":"feature,tv_movie,short","next_page":"results_title"})
		ump.index_item("Top Rated Series","select_year",args={"at":"0","num_votes":"5000,","sort":"user_rating","title_type":"tv_series,mini_series","next_page":"results_title"})
		ump.index_item("Top Voted Series","select_year",args={"at":"0","sort":"num_votes,desc","title_type":"tv_series,mini_series","next_page":"results_title"})
		ump.index_item("Top Rated Documentaries","select_year",args={"at":"0","num_votes":"5000,","sort":"user_rating","title_type":"documentary","next_page":"results_title"})
		ump.index_item("Top Voted Documentaries","select_year",args={"at":"0","sort":"num_votes,desc","title_type":"documentary","next_page":"results_title"})
		ump.index_item("Genres","genres")
		ump.index_item("Awards","awards")
		ump.index_item("World Cinema","languages")

	elif ump.page == "genres":
		genres=("Action","Adventure","Animation","Biography","Comedy","Crime","Drama","Family","Fantasy","Film-Noir","Game-Show","History","Horror","Music","Musical","Mystery","News","Reality-TV","Romance","Sci-Fi","Sport","Talk-Show","Thriller","War","Western")
		for genre in genres:
			ump.index_item(genre,"select_year",args={"at":"0","sort":"moviemeter,asc","num_votes":"1000,","genres":genre.lower().replace("-","_")})

	elif ump.page == "awards":
		awards=(("oscar_best_picture_winners","OSCARS: Best Picture Winning Movies",0),
				("oscar_best_director_winners","OSCARS: Best Director Winning Movies",0),
				("oscar_best_director_winners","OSCARS: Best Director Winning People",2),
				("oscar_best_actress_winners","OSCARS: Best Actress Winning People",2),
				("oscar_best_actor_winners","OSCARS: Best Actor Winning People",2),
				("oscar_best_supporting_actress_winners","OSCARS: Best Supporting Actress Winning People",2),
				("oscar_best_supporting_actor_winners","OSCARS: Best Supporting Actor Winning People",2),
				("oscar_winners","OSCARS: Any Category Winning Movies",0),
				("oscar_winners","OSCARS: Any Category Winning People",2),
				("emmy_winners","EMMIES: Award Winning Series",1),
				("golden_globe_winners","GOLDEN GLOBE: Award Winning Movies",0),
				("razzie_winners","RAZZIES: Award Winning Movies",0),
				("national_film_registry","National Film Board Preserved Movies",0),
				("oscar_best_director_nominees","OSCARS: Best Director Nominated People",2),
				("oscar_best_actress_nominees","OSCARS: Best Actress Nominated People",2),
				("oscar_best_actor_nominees","OSCARS: Best Actor Nominated People",2),
				("oscar_best_supporting_actress_nominees","OSCARS: Best Supporting Actress Nominated People",2),
				("oscar_best_supporting_actor_nominees","OSCARS: Best Supporting Actor Nominated People",2),
				("oscar_nominees", "OSCARS: Any Category Nominated Movies",0),
				("emmy_nominees Emmy","EMMIES: Award Nominated Series",1),
				("golden_globe_nominees","GOLDEN GLOBE: Award Nominated Movies",0),
				("razzie_nominees","RAZZIES: Award Nominated Movies",0))

		for award in awards:
			key,val,tt=award
			if tt == 0:
				ump.index_item(val,"results_title",args={"at":"0","sort":"release_date_us,desc","groups":key,"title_type":"feature,tv_movie,short,documentary"})
			elif tt == 1:
				ump.index_item(val,"results_title",args={"at":"0","sort":"release_date_us,desc","groups":key,"title_type":"tv_series,mini_series"})
			elif tt == 2:
				ump.index_item(val,"results_name",args={"groups":key})

	elif ump.page == "languages":		
		langs=("ar","Arabic"),("bg","Bulgarian"),("zh","Chinese"),("hr","Croatian"),("nl","Dutch"),("fi","Finnish"),("fr","French"),("de","German"),("el","Greek"),("he","Hebrew"),("hi","Hindi"),("hu","Hungarian"),("is","Icelandic"),("it","Italian"),("ja","Japanese"),("ko","Korean"),("no","Norwegian"),("fa","Persian"),("pl","Polish"),("pt","Portuguese"),("pa","Punjabi"),("ro","Romanian"),("ru","Russian"),("es","Spanish"),("sv","Swedish"),("tr","Turkish"),("uk","Ukrainian")

		for lang in langs:
			key,val=lang
			ump.index_item(val,"select_year",{"at":"0","sort":"moviemeter,asc","num_votes":"1000,","languages":key})

	elif ump.page == "select_year":
		ump.args["year"]=""
		if "next_page" in ump.args:
			next_page=ump.args["next_page"]
			ump.args.pop("next_page")
		else:
			next_page="search"
		ump.index_item("All Time",next_page,ump.args)
		for year in reversed(range(date.today().year-100,date.today().year+1)):
			ump.args["year"]=year
			ump.index_item(str(year),next_page,args=ump.args)
	
	elif ump.page == "search":
		title=ump.args.get("title","")
		if title==" ":
			conf,ump.args["title"]=ump.get_keyboard('default', 'Title', True)
		
		mquery=ump.args.copy()
		mquery["title_type"]="feature,tv_movie,short"
		ump.index_item("Show Only Movies","results_title",args=mquery,art=None)

		squery=ump.args.copy()
		squery["title_type"]="tv_series,mini_series"
		ump.index_item("Show Only Series","results_title",args=squery,art=None)

		dquery=ump.args.copy()
		dquery["title_type"]="documentary"
		ump.index_item("Show Only Documentaries","results_title",args=dquery,art=None)
	
	elif ump.page == "results_name":
		name=ump.args.get("name","")
		if name=="?":
			conf,name=ump.get_keyboard("default","Name",True)
			ump.args["name"]=name
		ids=[]
		
		page=ump.get_page("http://www.imdb.com/search/name","utf-8",query=ump.args)
		people=scrape_imdb_names(page)
		for p in people:ids.append(p["id"])
		if "name" in ump.args and not ump.args["name"]=="":
			js=json.loads(ump.get_page("http://www.imdb.com/xml/find?json=1&nr=1&q=%s&nm=on"%ump.args["name"],"utf-8"))
			for key in ["name_popular","name_substring","name_approx"]:
				for p in js.get(key,[]):
					if not p["id"] in ids:
						people.append({"id":p["id"],"name":p["name"],"poster":"DefaultFolder.png"})

		for person in people:
			ump.index_item(person["name"],"search",args={"role":person["id"],"sort":"release_date_us,desc",},art={"thumb":person["poster"], "thumb":person["poster"]})
	
	elif ump.page == "results_title":
		title=ump.args.get("title","")
		if title=="?":
			conf,title=ump.get_keyboard("default","Title",True)
			ump.args["title"]=title
		page=ump.get_page("http://www.imdb.com/search/title","utf-8",query=ump.args,header={"Accept-Language":"tr"})#hack imdb to give me original title with my unstandart language header
		start,end,total,movies=scrape_imdb_search(page)
		suggest=""
		if (len(movies) < 1 or ump.args.get("google",False)) and "title" in ump.args.keys():
			suggest="[SUGGESTED] "
			movies=[]
			ids=[]
			if "tv_series" in ump.args["title_type"]:
				suffix='"TV Series"'
			elif "documentary" in ump.args["title_type"]:
				suffix='"Documentary"'
			else:
				suffix=''
			urls=ump.web_search('inurl:http://www.imdb.com/title/ inurl:releaseinfo %s %s'%(ump.args["title"],suffix))
			if len(urls)<1:
				return None
			else:
				for u in urls:
					idx=u.split("/")[4]
					if not idx[:2]=="tt":
						continue
					ids.append(idx)
			for id in set(ids):
				movies.append(scrape_name(id))

		allowed=[]
		if "role" in ump.args.keys():
			page=ump.get_page("http://www.imdb.com/name/%s/"%ump.args["role"],"utf-8")
			roles=re.findall('id="(.*?)-(tt[0-9]*?)"',page)
			for role in roles:
				role_t,role_id=role
				if role_t in ["director","writer","actor"]:
					allowed.append(role_id)
		if not len(movies) < 1: 
			for movie in movies:
				if len(allowed) and not movie["info"]["code"] in allowed and "role" in ump.args.keys():
					continue
				commands=[]
				for person in movie["info"].get("director","").split(","):
					if not person=="":
						commands.append(('Search Director : %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person})))
				for person in movie["info"].get("cast",[""])[:3]:
					if not person=="":
						commands.append(('Search Actor: %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person})))
				if "tv_series" in ump.args["title_type"]:
					commands.append(('Search on TVDB : %s'%movie["info"]["title"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":movie["info"]["title"]},module="tvdb")))
					commands.append(('Search on ANN : %s'%movie["info"]["title"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":movie["info"]["title"]},module="ann")))
					ump.index_item(suggest+movie["info"]["localtitle"],"show_seasons",args={"imdbid":movie["info"]["code"]},info=movie["info"],art=movie["art"],cmds=commands,mediatype=ump.defs.MT_TVSHOW)
				else:
					ump.publish("movie")
					commands.append(('Search on ANN : %s'%movie["info"]["title"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":movie["info"]["title"]},module="ann")))
					movie["info"]["mediatype"]=ump.defs.MT_MOVIE
					ump.index_item(suggest+movie["info"]["localtitle"],"urlselect",info=movie["info"],art=movie["art"],cmds=commands,mediatype=ump.defs.MT_MOVIE)

			if total>end:
				ump.index_item("Results %d-%d"%(end+1,end+51),"results_title",args=ump.args)
			
			if not ump.args.get("google",False) and "title" in ump.args.keys():
				ump.args["google"]=True
				ump.index_item("Search \"%s\" in Google"%ump.args["title"],"results_title",args=ump.args)

	elif ump.page=="show_seasons":
		imdbid=ump.args.get("imdbid",None)
		if not imdbid :
			return None
		res=ump.get_page("http://www.imdb.com/title/%s/episodes"%imdbid,"utf-8")
		seasons=re.findall('<option.*?value="([0-9]{1,2})">',res)
		if not len(seasons)>0:
			return None
		for season in sorted([int(x) for x in seasons if x.isdecimal()],reverse=True):
			info=ump.info.copy()
			info["season"]=season
			ump.index_item("Season %d"%season,"show_episodes",args={"imdbid":imdbid,"season":season},info=info,mediatype=ump.defs.MT_SEASON)
	
	elif ump.page=="show_episodes":
		ump.publish("tvshow")
		imdbid=ump.args.get("imdbid",None)
		season=ump.args.get("season",None)
		if not imdbid or not season:
			return None
		res=ump.get_page("http://www.imdb.com/title/%s/episodes?season=%d"%(imdbid,season),"utf-8")
		#episodes=re.findall('<div class="list_item(.*?)<div class="wtw-option-standalone"',res,re.DOTALL)
		episodes=re.findall('<meta itemprop="episodeNumber" content="([0-9]*?)"/>',res)
		img=re.findall('class="zero-z-index".*?src="(.*?)"',res)
		title=re.findall('title="(.*?)" itemprop="url"',res)
		episodes=[int(x) for x in episodes]
		plots=re.findall('<div class="item_description" itemprop="description">(.*?)</div>',res,re.DOTALL)
		airdates=re.findall('<div class="airdate">\n\s*(.*?)\n\s*</div',res)
		airdates=[time.strftime("%Y-%m-%d",time.strptime(airdate.strip().replace(".",""),"%d %b %Y")) for airdate in airdates]
		airdates=_match_list(episodes,airdates)
		plots=_match_list(episodes,plots)
		title=_match_list(episodes,title,"Unknown Title")
		img=_match_list(episodes,img,"DefaultFolder.png")
		episodes=zip(episodes,airdates,plots,title,img)
		episodes.sort(key=operator.itemgetter(0), reverse=True)
		info=ump.info
		info["tvshowtitle"]=info["title"]
		info["season"]=season
		art=ump.art
		for episode in episodes:
			epi,airdate,plot,title,img=list(episode)
			info["title"]=title
			info["episode"]=epi
			info["aired"]=airdate
			plot=plot.replace("\n","")
			if not 'href="/updates' in plot:
				info["plot"]=plot
				info["plotoutline"]=plot
			art["thumb"]=img
			art["poster"]=img
			commands=[('Search on ANN : %s'%info["tvshowtitle"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":info["tvshowtitle"]},module="ann"))]
			commands.append(('Search on TVDB : %s'%info["tvshowtitle"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":info["tvshowtitle"]},module="tvdb")))
			for person in ump.info.get("director","").split(","):
				if not person=="":
					commands.append(('Search Director : %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person})))
			for person in ump.info.get("cast",[""])[:2]:
				commands.append(('Search Actor: %s'%person, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":person})))
			ump.index_item("%d. %s"%(epi,title),"urlselect",info=info,art=art,cmds=commands,mediatype=ump.defs.MT_EPISODE)