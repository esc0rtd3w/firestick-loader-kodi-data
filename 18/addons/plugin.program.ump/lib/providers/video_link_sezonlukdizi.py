import re

encoding="utf-8"
domain = 'http://sezonlukdizi.com'


def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("tvshow"): return
	names=ump.getnames()
	for name in names:
		ump.add_log("sezonlukdizi is searching %s"%name)
		page=ump.get_page(domain+"/diziler.asp",encoding,query={"adi":name,"tur":"","ulke":"","tv":"","minYil":"","maxYil":"","minImdb":"","siralama_tipi":"imdb","siralama=turu":"desc","ps":"25"})
		series=re.findall('href="(.*?)" class="header">(.*?) \(([0-9]{4})\)</a>',page)
		for serie in series:
			l,t,y=serie
			l,t,s=serie
			tag=l.split("/")[-1][:-5]
			if ump.is_same(t,name):
				url=domain+"/"+tag+"/"+str(i["season"])+"-sezon-"+str(i["episode"])+"-bolum.html"
				epage=ump.get_page(url,encoding)
				if "Haydaaa..." in epage:
					continue
				ump.add_log("sezonlukdizi matched %s %dx%d %s"%(i["tvshowtitle"],i["season"],i["episode"],i["title"]))
				video_ids = re.findall('<div data-id="([0-9]*?)" class="item',epage)
				for video_id in video_ids:
					vurl=domain+"/ajax/dataEmbed.asp"
					vpage=ump.get_page(vurl,encoding,referer=url,data={"id":video_id},header={"X-Requested-With":"XMLHttpRequest"})
					links=re.findall("src=\"(.*?)\"",vpage)
					if len(links):
						parts=[]
						prefix=""
						link=links[0]
						if link.startswith("//"):link="http:"+link
						if "plussd.asp" in link or "plussd2.asp" in link:
							gpage=ump.get_page(link,encoding,referer=url)
							gvids=re.findall('file:"(.*?)", label:"(.*?)",type:"mp4"',gpage)
							mparts={}
							for gvid in gvids:
								glink=gvid[0]
								if glink.startswith("//"):glink="http:"+glink
								mparts[gvid[1]]=glink
							parts.append({"url_provider_name":"google", "url_provider_hash":mparts,"referer":url})
						elif "openload.co" in link:
							olink=link.split("embed/")
							olink=olink[1].split("/")[0]
							parts.append({"url_provider_name":"openload", "url_provider_hash":olink,"referer":url})
							prefix=""
						if len(parts):
							ump.add_mirror(parts,"%s%s %dx%d %s" % (prefix,i["tvshowtitle"],i["season"],i["episode"],i["title"]))
				break