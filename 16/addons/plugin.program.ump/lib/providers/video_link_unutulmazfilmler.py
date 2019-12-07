import re
import string


domain="http://www.unutulmazfilmler.co"
encoding="utf-8"

def match_results(page,names,info):
	match_name,match_year,link=False,False,""
	results=re.findall('<h2 class="content-title">\s*?<a href="(.*?)" title=".*?" class="link-unstyled">(.*?)\s\-.*?</a>\s*?<small>\(([0-9]{4})\s|-',page,re.DOTALL)
	for result in results:
		if match_year:
			break
		link,fname,year=result
		for name in names:
			if ump.is_same(fname,name):
				match_name=True
				break
		if match_name:
			match_year=info["year"]==int(year)
	return match_name,match_year,link

def run(ump):
	globals()['ump'] = ump
	i=ump.info

	if not ump.subscribe("movie"): return
	names=ump.getnames()

	for name in names:
		ump.add_log("UnutulmazFilmler is searching %s" % name)
		page=ump.get_page(domain,encoding,query={"s":name})
		match_name,match_year,link=match_results(page,names,i)
		if match_year:
			break
		else:
			paginations=re.findall('<a href="(.*?unutulmazfilmler.co/arama\.php.*?)">[0-9]*?</a>',page)
			for pagination in paginations:
				match_name,match_year,link=match_results(ump.get_page(pagination,encoding),names,i)
				if match_name:
					break

	if not match_year:
		ump.add_log("UntulmazFilmler can't match %s"%name)
		return None

	ump.add_log("UntulmazFilmler matched %s"%name)
	page=ump.get_page(link,encoding)
	players=re.findall('ul class=".*?player-list.*?"(.*?)</ul>',page,re.DOTALL)
	players=re.findall('class="menu-link">(.*?)<',players[0])
	medias={}
	for player in players:
		if "pub" in player.lower():	plyr="pub"
		elif "odno" in player.lower():	plyr="odkl"
		else: plyr=player.lower()
		medias[plyr]=[]
		playerpages=[ump.get_page(link+"?player=%s"%plyr,encoding)]
		parts=re.findall("<\!-- part list -->(.*?)</ul>",playerpages[0],re.DOTALL)
		if len(parts):
			parts=re.findall('<li class="menu-item"><a href="(.*?)" class="menu-link">',parts[0])
		for part in parts:
			playerpages.append(ump.get_page(part,encoding))
		for playerpage in playerpages:
			medias[plyr].extend(re.findall('<div class="embed-responsive-item video-wrapper">\s*?<iframe width=".*?" height=".*?" src="(.*?)" fram',playerpage))
		
	for plyr,urls in medias.iteritems():
		umpparts=[]
		prefix=""
		if len(urls)>1:prefix="[MP]"
		for url in urls:
			if plyr=="pub":
				src=ump.get_page(url,encoding,referer=domain)
				mirrors=re.findall('{"file": "(.*?)", "label": "(.*?)"',src)
				hash={}
				for mirror in mirrors:hash[mirror[1]]=mirror[0]
				umpparts.append({"url_provider_name":"google", "url_provider_hash":hash,"referer":domain})
			elif plyr=="odkl":
				umpparts.append({"url_provider_name":"okru", "url_provider_hash":url.split("/")[-1],"referer":domain})
		
		if len(umpparts):
			ump.add_mirror(umpparts,"[HS:TR]%s%s" % (prefix,name))