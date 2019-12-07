from operator import itemgetter
import re
import time

encoding="utf-8"
stype="manga"
domain="https://www.mangaupdates.com"
perpage=30

def cln(str):
	return re.sub('<[^<]+?>', '', str)

def get_releases(id):
	fpage=ump.get_page("%s/releases.html?page=1&search=%s&stype=series&perpage=%d"%(domain,str(id),perpage),encoding)
	pcount=re.findall("Pages \(([0-9]*?)\)",fpage)
	res=[]
	
	if len(pcount)>0:
		pages=range(2,int(pcount[0])+1)
	else:
		pages=[]
	
	def parse_page(page):
		i=0
		for td in re.findall("class='text pad'.*?\>(.*?)\</td",page):
			td=re.sub('<[^<]+?>', '', td)
			m=i%5
			if m==0:
				#release date
				try:
					rel_dat=time.strptime(td,"%m/%d/%y")
				except:
					rel_dat=time.strptime("01/01/0001","%m/%d/%Y")
					ump.add_log("Baka release does not have a valid date '%s' for id: %s and is set to Jesus time."%(td,id))
				i+=1
				continue
			if m==1:
				#title
				tit=td
				i+=1
				continue
			if m==2:
				#volume
				vol=td
				i+=1
				continue
			if m==3:
				#chapter
				cha=td
				i+=1
				continue
			if m==4:
				#group
				gro=td
				res.append((rel_dat,tit,vol,cha,gro))
				i+=1
	parse_page(fpage)

	def parse_pages(pid):
		page=ump.get_page("%s/releases.html?page=%s&search=%s&stype=series&perpage=%d"%(domain,str(pid),str(id),perpage),encoding)
		return parse_page(page)
	
	gid=ump.tm.create_gid()
	for p in pages:
		ump.tm.add_queue(parse_pages,(p,),gid=gid)
		
	ump.tm.join(gid=gid,cnt="all")

	return res

def get_details_mangaka(matches):
	res={}
	ids=[]
	pops=[]
	def update(k,id,name):
		if not id in ids:
			ids.append(id)
		else:
			pops.append(k)
		thumb="DefaultFolder.png"
		link="%s/authors.html?id=%s"%(domain,id)
		src=ump.get_page(link,encoding)
		info={}
		cover=re.findall("<img height.*?src='(.*?)'>",src)
		if len(cover):thumb=cover[0]
		names1=sorted(re.findall('series\.html\?id\=(.*?)"\>(.*?)</a.*?>([0-9]*?)</td>\s*?</tr>',src,re.DOTALL),key=itemgetter(2),reverse=True)
		names=[]
		for name in names1:
			names.append((name[0],name[1]))
		info["orginaltitle"]=info["title"]=re.findall("<span class='tabletitle'><b>(.*?)</b>",src)[0]
		res[k]={"info":info,"art":{"thumb":thumb,"poster":thumb},"names":names}

	gid=ump.tm.create_gid()
	for k in matches.keys():
		id,name=matches[k]
		ump.tm.add_queue(update,(k,id,name),gid=gid)


	ump.tm.join(gid=gid,cnt="all")
	for p in pops:res.pop(p)
	return  res

def get_details(matches):
	res={}
	ids=[]
	pops=[]
	def update(k,id,name):
		if not id in ids:
			ids.append(id)
		else:
			pops.append(k)
		thumb="DefaultFolder.png"
		link="%s/series.html?id=%s"%(domain,id)
		src=ump.get_page(link,encoding)
		cover=re.findall('class="sContent".*?\<img.*?src=\'(.*?)\'',src)
		if len(cover)>0:
			thumb=cover[0]
		else:
			ump.add_log("Cant find mangaka for baka id %s"%str(id))
		mangaka=re.findall("title='Author Info'\>(.*?)\</",src)
		if len(mangaka)>0:
			mangaka=re.sub('<[^<]+?>', '', mangaka[0])
		else:
			mangaka=""
			ump.add_log("Cant find cover for baka %s"%str(id))
		title=re.findall('releasestitle tabletitle"\>(.*?)\</',src)
		if len(title)>0:
			title=re.sub('<[^<]+?>', '', title[0])
		else:
			title=name
		info={"title":title,"originaltitle":name,"writer":mangaka,"code":id}
		res[k]={"info":info,"art":{"thumb":thumb,"poster":thumb}}

	gid=ump.tm.create_gid()
	for k in matches.keys():
		id=matches[k][0]
		name=matches[k][1]
		ump.tm.add_queue(update,(k,id,name),gid=gid)
	
	ump.tm.join(gid=gid,cnt="all")

	for p in pops:res.pop(p)
	return  res

def run(ump):
	globals()['ump'] = ump
	ump.publish("manga")
	if ump.page == "root":
		ump.index_item("Search","select_type",args={"stype":"title","perpage":perpage,"page":1})
		ump.index_item("Genres","genres")
		ump.index_item("Themes","categories")
		ump.index_item("Mangakas","search_mangaka",args={"orderby":"series","perpage":perpage,"page":1})
		ump.index_item("Latest Releases","releases",args={"page":1})
		ump.index_item("Charts","charts",args={"page":1})
	
	elif ump.page=="genres":
		page=ump.get_page("%s/genres.html"%domain,encoding)
		genres=set(re.findall("\?genre\=(.*?)'",page))
		for genre in genres:
			name=genre.replace("+"," ")
			args={"genre":genre.lower(),"orderby":"rating","filter":"somereleases","search":None,"stype":"title","perpage":perpage,"page":1}
			ump.index_item(name,"select_type",args=args)

	elif ump.page=="categories":
		page=ump.get_page("%s/categories.html?perpage=100&orderby=agree"%domain,encoding)
		cats=re.findall("\?category\=(.*?)'>(.*?)</a",page)
		for cat in cats:
			v,c=cat
			name=c.replace("/s","").replace("/ies","")
			args={"category":v,"orderby":"rating","filter":"somereleases","search":None,"stype":"title","perpage":perpage,"page":1}
			ump.index_item(name,"select_type",args=args)

	elif ump.page=="charts":
		charts=(
			("Weekly Top Rankings",{"period":"week"}),
			("Monthly Top Rankings",{"period":"month1"}),
			("3 Months Top Rankings",{"period":"month3"}),
			("6 months Top Rankings",{"period":"month6"}),
			("Yearly Top Rankings",{"period":"month12"}),
			("Most Listed to read",{"list":"read","act":"list"}),
			("Most Added to Wishlist",{"list":"wish","act":"list"}),
			("Most add to list and read",{"list":"complete","act":"list"}),
			("Most add to list but not read",{"list":"unfinished","act":"list"}),
			)
		for chart in charts:
			name,args=chart
			ump.args.update(args)
			ump.index_item(name,"stats",ump.args)

	elif ump.page=="select_type":
		if not "search" in ump.args:
			conf,ump.args["search"]=ump.get_keyboard('default', 'Search Baka', True)
		elif ump.args["search"] is None:
			ump.args.pop("search")
		types=(("Search Manga (Japanese Comics)","manga"),("Search Mangaka (Author)","mangaka"),("Search Manhwa (Korean Comics)","manhwa"),("Search Manhua (Chinese Comics)","manhua"),("Search Novel","novel"),("Search Artbook","artbook"),("Search Doujinshi (Self Published)","doujinshi"),("Drama CD (Scripts)","drama_cd"),("Search OEL (Original English Language)","oel"),("Search All kinds of Puplications",""))
		for type in types:
			t,v=type
			if v == "mangaka" :
				if not "search" in ump.args: continue
				ump.index_item(t,"search_mangaka",ump.args)
			else:
				ump.args["type"]=v
				ump.index_item(t,"search",ump.args)

	elif ump.page=="stats":
		page=ump.get_page("%s/stats.html"%domain,encoding,query=ump.args)
		names=re.findall('href\="series\.html\?id\=([0-9]*?)"><u>(.*?)</u>',page)
		pagination=re.findall('title="(.*?)">Last</a>',page)
		matches={}
		k=0
		for name in names:
			k+=1
			(id,title)=name
			matches[k] = (cln(id),cln(title))
		matches=get_details(matches)
		for k in sorted(matches.keys()):
			cmd=('Search Mangaka: %s' % matches[k]["info"]["writer"], 'XBMC.Container.Update(%s)'%ump.link_to("search_mangaka",{"search":matches[k]["info"]["writer"]}))
			ump.index_item(matches[k]["info"]["title"],"show_chapters",args=matches[k],info=matches[k]["info"],art=matches[k]["art"],cmds=[cmd])
		if len(pagination):
			page=ump.args["page"]+1
			ump.args["page"]=page
			ump.index_item("Page %d"%page,"stats",ump.args)

	elif ump.page=="releases":
		page=ump.get_page("%s/releases.html"%domain,encoding,query=ump.args)
		names=re.findall("id=([0-9]*?)' title='Series Info'\>(.*?)</a></td>\s*?(<td .*?</td>)\s*?(<td .*?</td>)",page,re.DOTALL)
		pagination=re.findall('title="(.*?)">Last</a>',page)
		releases={}
		k=0

		for name in names:
			k+=1
			(id,title,chap,grp)=name
			releases[k] = (cln(id),cln(title),cln(chap),cln(grp))
		matches=get_details(releases)

		for k in sorted(matches.keys()):
			name="%s , %s, %s"% (releases[k][1],releases[k][2],releases[k][3])
			cmd=('Search Mangaka: %s' % matches[k]["info"]["writer"], 'XBMC.Container.Update(%s)'%ump.link_to("search_mangaka",{"search":matches[k]["info"]["writer"]}))
			ump.index_item(name,"show_chapters",args=matches[k],info=matches[k]["info"],art=matches[k]["art"],cmds=[cmd],mediatype=ump.defs.MT_MANGA)
		if len(pagination):
			page=ump.args["page"]+1
			ump.args["page"]=page
			ump.index_item("Page %d"%page,"releases",ump.args)

	elif ump.page=="search_mangaka":
		page=ump.get_page("%s/authors.html"%domain,encoding,query=ump.args)
		names=re.findall("id=([0-9]*?)' alt='Author Info'\>(.*?)\</",page)
		pagination=re.findall('title="(.*?)">Last</a>',page)
		matches={}
		k=0
		for name in names:
			k+=1
			(id,title)=name
			if id in matches.keys():
				matches[k]+=(id," / " + re.sub('<[^<]+?>', '', title))
			else:
				matches[k] = (id,re.sub('<[^<]+?>', '', title))
		matches=get_details_mangaka(matches)

		for k in sorted(matches.keys()):
			ump.index_item(matches[k]["info"]["title"],"search",args={"names":matches[k]["names"],"page":1},info=matches[k]["info"],art=matches[k]["art"])
		if len(pagination):
			page=ump.args["page"]+1
			ump.args["page"]=page
			ump.index_item("Page %d"%page,"search_mangaka",ump.args)

	elif ump.page == "search":
		if "names" in ump.args:
			names=ump.args["names"][(ump.args["page"]-1)*perpage:ump.args["page"]*perpage]
			if perpage*ump.args["page"]<len(ump.args["names"]):
				pagination=[True]
			else:
				pagination=[]
		else:
			page=ump.get_page("%s/series.html"%domain,encoding,query=ump.args)
			names=re.findall("id=([0-9]*?)' alt='Series Info'\>(.*?)\</a",page)
			pagination=re.findall('title="(.*?)">Last</a>',page)
		matches={}
		k=0
		for name in names:
			k+=1
			(id,title)=name
			if id in matches.keys():
				matches[k]+=(id," / " + re.sub('<[^<]+?>', '', title))
			else:
				matches[k] = (id,re.sub('<[^<]+?>', '', title))
		matches=get_details(matches)
		for k in sorted(matches.keys()):
			cmd=('Search Mangaka: %s' % matches[k]["info"]["writer"], 'XBMC.Container.Update(%s)'%ump.link_to("search_mangaka",{"search":matches[k]["info"]["writer"]}))
			name="%s , %s"% (matches[k]["info"]["title"],matches[k]["info"]["writer"])
			ump.index_item(name,"show_chapters",args={"names":matches[k]},info=matches[k]["info"],art=matches[k]["art"],cmds=[cmd],mediatype=ump.defs.MT_MANGA)
		if len(pagination):
			page=ump.args["page"]+1
			ump.args["page"]=page
			ump.index_item("Page %d"%page,"search",ump.args)

	elif ump.page== "show_chapters":
		id=ump.info["code"]
		releases=get_releases(id)
		rel_sort=sorted(releases,key=itemgetter(0,3),reverse=True)
		
		def create_li(chapter):
			if chapter in cache:
				return
			else:
				chapter=str(chapter)
				cache.append(chapter)
				ump.info["season"]="-1"
				ump.info["episode"]=chapter
				ump.info["mediatype"]=ump.defs.MT_CHAPTER
				ump.index_item("Chapter %s"%chapter,"urlselect",mediatype=ump.defs.MT_CHAPTER)
		cache=[]
		pre=0
		suffixes=["end"]
		for rel in rel_sort:
			chapter=rel[3]
			#clear suffixes
			for suffix in suffixes:
				if " (%s)"%suffix in chapter:
					chapter=chapter.replace(" (%s)"%suffix,"")
			#clear versions
			chapter=re.sub("v[0-9].*","",chapter)

			#clear sequence releases
			if "-" in chapter:
				sequences=chapter.split("-")
				if len(sequences)==2 and sequences[0].isnumeric() and sequences[1].isnumeric():
					if int(sequences[0])>int(sequences[1]):
						chapter=sequences[0]
					else:
						chapter=sequences[1]

			#fill the missing releases
			if chapter.isnumeric():
				chapter=int(chapter)
			else:
				create_li(chapter)
				continue
			if pre==0:
				create_li(chapter)
				pre=chapter
				continue
			else:
				for i in range(pre-chapter):
					create_li(pre-i-1)
				pre=chapter

		for p in range(pre-1):
			create_li(pre-p-1)