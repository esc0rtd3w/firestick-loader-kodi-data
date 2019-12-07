# -*- coding: utf-8 -*-
import datetime
import re
from urllib import urlencode
from xml.dom import minidom
import xbmc
from third.dateutil import parser
from operator import itemgetter

domain="http://www.animenewsnetwork.com"
encoding="utf-8"

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

def scrape_ann_search(animes):
	ump.dialogpg.update(5, message='Retrieving Information')
	res=ump.get_page(domain+"/encyclopedia/api.xml?anime="+"/".join(animes),None)
	ump.dialogpg.update(40, message='Retrieving Information')
	m1=[]
	#no idea why chr 08 causes xml sructure error :/
	res=minidom.parseString(res.replace(chr(8),""))
	medias=res.getElementsByTagName("anime")
	ump.dialogpg.update(50, message='Retrieving Information')
	count=0
	for media in medias:
		count+=1
		relnum=0
		img=""
		title=""
		maintitle=""
		titlealias=""
		originaltitle=None
		tvshowtitle=""
		localtitle=None
		alts=[]
		alttitle=[]
		outline=""
		gen=""
		year=1900
		dates=[]
		votes="0"
		episodes={}
		dir=""
		cast=[]
		mpaa=""
		runtime=""
		rating=float(0)
		id=str(media.getAttribute("id"))
		type=str(media.getAttribute("precision"))
		epinum=0
		num_of_epis=0
		directors=[]
		for info in media.getElementsByTagName("info"):
			t=info.getAttribute("type")
			#image
			if t=="Picture":
				img=info.lastChild.getAttribute("src")
			if t=="Main title":
				maintitle=latinise(info.lastChild.data)
			if t=="Alternative title":
				alt=latinise(info.lastChild.data)
				alttitle.append((info.getAttribute("lang"),alt))
			if t=="Plot Summary":
				outline+=info.lastChild.data
			if t=="Genres" or t=="Themes":
				gen+=info.lastChild.data+"/"
			if t=="Vintage":
				try:
					pdate=parser.parse(info.lastChild.data.split(" to ")[0],fuzzy=True,default=datetime.datetime(1970, 1, 1, 0, 0))
					dates.append(pdate)
				except:
					pass
			if t=="Premiere date" and type=="movie series":
				epinum+=1
				episodes[epinum]={"title":info.lastChild.data,"relativenumber":epinum}
			
			if t=="Number of episodes":
				num_of_epis=int(info.lastChild.data)

		for episode in media.getElementsByTagName("episode"):
			if not float(episode.getAttribute("num")) == 0:
				relnum+=1
							
			episodes[episode.getAttribute("num")]={"title":episode.lastChild.lastChild.data,"relativenumber":relnum}
		
		##special for ovas, i hate the random stuff with ann
		cur_epis=len(episodes)
		if num_of_epis>cur_epis and num_of_epis>1:
			for k in range(num_of_epis-cur_epis):
				episodes[cur_epis+k+1]={"title":"Episode %d"%(cur_epis+k+1),"relativenumber":cur_epis+k+1}
		
		for staff in media.getElementsByTagName("staff"):
			try:
				if staff.childNodes[0].tagName=="task" and ("original" in staff.childNodes[0].lastChild.data.lower() or "character conceptual design" in staff.childNodes[0].lastChild.data.lower()) and staff.childNodes[1].tagName=="person":
					directors.append(staff.childNodes[1].lastChild.data)
			except:
				continue

		if len(episodes)>0:
			tvshowtitle=maintitle
		title=maintitle
		
		palts=[]
		for alt in alttitle:
			l,a=alt
			if not a in palts:
				l=l.lower()
				palts.append(a)
				if a == "" or a==" ":
					continue
				if l=="ja" and originaltitle is None:
					originaltitle=a
				if l==ump.backwards.getLanguage(0).lower() and localtitle is None:
					localtitle=a
				if not a == localtitle and not a ==originaltitle:
					alts.append(a)
		
		if originaltitle is None:
			originaltitle=maintitle

		if localtitle is None:
			localtitle=maintitle

		for rate in media.getElementsByTagName("ratings"):
			rating=float(rate.getAttribute("weighted_score"))
			votes=rate.getAttribute("nb_votes")

		if not gen=="":
			gen=gen[0:-1]
		if len(dates)>0:
			dates.sort
			m= datetime.datetime.now().month
			y= datetime.datetime.now().year
			if dates[0].year > y or dates[0].year == y and dates[0].month > m:
				continue
			year=int(dates[0].year)

	
		data={}
		data["info"]={
			"count":len(episodes.keys()),
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
			"cast":[],
			"castandrole":[],
			"director":",".join(set(directors)),
			"mpaa":mpaa,
			"plot":outline,
			"plotoutline":outline,
			"title":title,
			"originaltitle":originaltitle,
			"tvshowtitle":tvshowtitle,
			"localtitle":localtitle,
			"alternates":alts,
			"sorttitle":"",
			"duration":runtime,
			"studio":"",
			"tagline":"",
			"write":"",
			"premiered":"",
			"status":"",
			"code":id,
			"aired":"",
			"credits":"",
			"lastplayed":"",
			"album":"",
			"artist":([]),
			"votes":votes,
			"trailer":"",
			"dateadded":"",
			"type":type
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
		data["episodes"]=episodes #special only for this indexer
		m1.append(data)
		ump.dialogpg.update(50+count, message='Retrieving Information')

	return m1

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

def results_search(animes=None,filters=None):
	if filters is None: filters=ump.args["filters"]
	if animes is None: animes=ump.args["anime"]
	if isinstance(animes,unicode): animes=eval(animes)
	index=ump.args.get("index",0)
	anime=animes[index*50:(index+1)*50]
	medias=scrape_ann_search(anime)
	
	itemcount=0
	if len(medias) > 0: 
		if not index==0:
			ump.index_item("Results %d-%d"%((index-1)*50+1,index*50),"results_search",args={"anime":animes,"filters":filters,"index":index-1})
		for media in medias:
			if "numvotes" in filters and int(media["info"]["votes"])<100:
				continue
			name="%s (%s)"%(media["info"]["localtitle"],media["info"]["type"])
			itemcount+=1
			art=media["art"]
			info=media["info"]
			commands2=[]
			for director in info["director"].split(","):
				if not director=="":
					commands2.append(('Search on IMDB : %s'%director, 'XBMC.Container.Update(%s)'%ump.link_to("results_name",{"name":director},module="imdb")))
			if len(media["episodes"].keys())==0:
				commands=[('Search on IMDB : %s'%info["title"], 'XBMC.Container.Update(%s)'%ump.link_to("results_title",{"title":info["title"],"title_type":"feature,tv_movie,short","sort":"moviemeter,asc"},module="imdb"))]
				commands.extend(commands2)
				ump.index_item(name,"urlselect",info=info,art=art,cmds=commands,mediatype=ump.defs.MT_MOVIE)
			else:
				commands=[('Search on IMDB : %s'%info["title"], 'XBMC.Container.Update(%s)'%ump.link_to("results_title",{"title":info["title"],"title_type":"tv_series,mini_series","sort":"moviemeter,asc"},module="imdb"))]
				commands.append(('Search on TVDB : %s'%info["title"], 'XBMC.Container.Update(%s)'%ump.link_to("search",{"title":info["title"]},module="tvdb")))
				commands.extend(commands2)
				ump.index_item(name,"show_episodes",info=info,art=art,cmds=commands,mediatype=ump.defs.MT_TVSHOW)
		if (index+1)*50 < len(animes) and not itemcount==0:
			ump.index_item("Results %d-%d"%((index+1)*50+1,(index+2)*50),"results_search",args={"anime":animes,"filters":filters,"index":index+1})

def run(ump):
	globals()['ump'] = ump
	ump.publish("anime")
	if ump.page == "root":
		ump.index_item("Search","search")
		ump.index_item("Top Rated Animes","select_year")
		ump.index_item("Newest Animes","newest")
		ump.index_item("Animes by Genre","bygenre")
		ump.index_item("Animes by Themes","bytheme")

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
			args={"anime":"getgenres('%s')"%urlencode({"g":genres[genre]}),"filters":["numvotes"]}
			ump.index_item(genre, results_search, args=args)

	elif ump.page == "bytheme":
		themes=re.findall('name="th" type="checkbox" value="(.*?)".*?\(([0-9]*?)\)',ump.get_page("%s/encyclopedia/search/genre"%domain,None))
		addthemes=[]
		for theme,count in sorted([(x[0],int(x[1])) for x in themes], key=itemgetter(1),reverse=True):
			if not theme in addthemes:
				addthemes.append(theme)
				args={"anime":"getgenres('%s')"%urlencode({"th":theme}),"filters":[]}
				ump.index_item("%s (%d)"%(theme.split("|")[0].title(),count),"results_search",args=args)

	elif ump.page == "newest":
		ids=[]
		dates=[]
		months=[]
		pages=grab_searches("%s/encyclopedia/search/genreresults?w=series&w=movies&from=%d&to=%d&lic=&a=AA&a=OC&a=TA&a=MA&a=AO&o=rating"%(domain, datetime.datetime.now().year, datetime.datetime.now().year))
		for page in pages:
			ids.extend(re.findall("anime.php\?id=([0-9]*?)\"",page))
			dates.extend(re.findall("class=\"de\-emphasized\">(.*?)<",page))
		
		for i in range(len(dates)):
			try:
				since=(datetime.datetime.now() - parser.parse(dates[i],fuzzy=True,default=datetime.datetime(1970, 1, 1, 0, 0))).days
			except:
				continue
			if  since<= 15 and since >=0:
				months.append(ids[i])

		ump.index_item("Last 15 Days","results_search",args={"anime":months,"filters":[]})
		ump.index_item("This Year","results_search",args={"anime":ids,"filters":[]})

	elif ump.page == "select_year":
		ump.index_item("All Time","results_search",args={"anime":"getgenres('')","filters":["numvotes"]})
		for year in reversed(range(datetime.date.today().year-50,datetime.date.today().year+1)):
			ump.index_item(str(year),"results_search",args={"anime":"getgenres('%s')"%urlencode({"from":year,"to":year}),"filters":["numvotes"]})

	elif ump.page == "search":
		what=ump.args.get("title",None)
		if what is None:
			conf,what=ump.get_keyboard('default', 'Search Anime', True)
		q={"id":155,"type":"anime","search":what}
		res=ump.get_page(domain+"/encyclopedia/reports.xml",None,query=q)
		res=minidom.parseString(res)
		items=res.getElementsByTagName("item")
		ids=[]
		for item in items:
			ids.append(item.getElementsByTagName("id")[0].firstChild.data)
		
		if len(ids):
			results_search(ids,[])
	
	elif ump.page == "results_search":
		results_search()

	elif ump.page== "show_episodes":
		annid=ump.info.get("code",None)
		if annid is None:
			return None
		medias=scrape_ann_search([annid])
		if len(medias)<1:
			return None
		episodes=medias[0]["episodes"]
		info=medias[0]["info"]
		#keys are parsed as strings
		for k,v in episodes.items():
			episodes.pop(k)
			episodes[int(float(k))]=v
		#below does not work on old versions of python
		#episodes = {float(k):v for k,v in episodes.iteritems()}
		for epi in sorted(episodes.keys(),reverse=True):
			info["title"]=episodes[epi]["title"]
			info["episode"]=episodes[epi]["relativenumber"]
			#even though animes dont have season info force it so trakt will scrobble
			info["season"]=1
			info["absolute_number"]=epi
			ump.index_item("%d %s"%(epi,episodes[epi]["title"]),"urlselect",info=info,mediatype=ump.defs.MT_EPISODE)
		ump.index_item("Custom Episode Number","customepi",info=info,isFolder=False)

	elif ump.page=="customepi":
		conf,what=ump.get_keyboard('default', 'Episode Number', True)
		if what.isdigit():
			ump.info["title"]="Episode %s"%what
			ump.info["episode"]=int(what)
			ump.info["absolute_number"]=int(what)
			ump.info["season"]=1
			ump.info["mediatype"]=ump.defs.MT_EPISODE
			xbmc.executebuiltin("Container.Update(%s)"%ump.link_to("urlselect"))