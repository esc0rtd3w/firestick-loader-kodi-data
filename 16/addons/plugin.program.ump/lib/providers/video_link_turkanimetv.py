import re

from third.unidecode import unidecode


domain="http://www.turkanime.tv/"
encoding="utf-8"


def return_links(name,mp,h,fs,url):
	parts=[{"url_provider_name":mp, "url_provider_hash":h,"referer":url}]
	prefix=""
	if not fs == "Varsayilan":
		prefix="[FS:%s]"%fs
	name="%s[HS:TR]%s" % (prefix,name)
	ump.add_mirror(parts,name)

def scrape_moviepage(url,fansub,name):
	if not fansub is None:
		url=url+"&fansub="+fansub+"&giris=OK"
		pg=ump.get_page(domain+url,encoding)
	else:
		pg=url
	videos=re.findall('<a class\="btn".*?onclick\="sayfa\(\'#video\',\'(.*?)\',\'#video\'\)\;"><i class\="icon-play"></i>(.*?)</a>',pg)
	for video in videos:
		up=unidecode(video[1].replace(" ","").lower())
		u=video[0]

		try:
			if up=="mail": 
				up="mailru"
				continue
				#skip mailru this provider is messed up
			elif up=="myvi":
				uphash=re.findall("embed/html/(.*?)\"",ump.get_page(domain+u,encoding))[0]
			elif up=="odnoklassniki": 
				up="okru"
				uphash=re.findall("/videoembed/(.*?)\"",ump.get_page(domain+u,encoding))[0]
			elif up=="sibnet":
				continue
				#skip this provider it uses m3u8.
				uphash=re.findall("videoid\=([0-9]*?)\"",ump.get_page(domain+u,encoding))[0]
			elif up in ["cloudy","videohut","videoraj"]:
				uphash=re.findall("\?id\=(.*?)\"",ump.get_page(domain+u,encoding))[0]
			elif up == "vk":
				up="vkext"
				hash=re.findall("\?vid\=(.*?)\"",ump.get_page(domain+u,encoding))[0]
				oid,video_id,embed_hash=hash.split("_")
				uphash="http://vk.com/video_ext.php?oid="+oid+"&id="+video_id+"&hash="+embed_hash
			elif up == "turkanime":
				type1=re.findall('index\.php\?vid=(.*?)"',ump.get_page(domain+u,encoding))
				type2=re.findall('plusv3\.php\?vid=(.*?)"',ump.get_page(domain+u,encoding))
				if len(type1):
					hash1="http://www.schneizel.net/video/index.php?vid="+type1[0]
					hash2=re.findall('<iframe.*?src="(.*?)"',ump.get_page(hash1,encoding,referer=domain+u))[0]
					uphash={}
					labels={"22":"720p","59":"480p1","18":"360p1","43":"360p2","35":"480p2","34":"360p3"}
					for mirror in re.findall('"fmt_stream_map","(.*?)"',ump.get_page(hash2,encoding,referer=hash1))[0].split(","):
						label,link=mirror.split("|")
						if label in labels.keys():label=labels[label]
						uphash[label.decode("unicode-escape")]=link.decode("unicode-escape")
				elif len(type2):
					uphash="http://www.schneizel.net/video/plusv3.php?vid="+type2[0]
				else:
					continue
				up="google"
			elif up == "dailymotion":
				#todo prepare a decoder
				uphash=re.findall("/video/(.*?)\"",ump.get_page(domain+u,encoding))[0]
			elif up == "kiwi":
				uphash=re.findall("v2/(.*?)\"",ump.get_page(domain+u,encoding))[0]
			elif up == "meta":
				#todo this provider is messed up
				continue
				#todo prepare a decoder
				uphash=re.findall("iframe/(.*?)/",ump.get_page(domain+u,encoding))[0]
			else:
				ump.add_log("turkanime: Unknown URL Provider: %s, cant scrape"%up)
				continue
		except IndexError:
			continue

		fansub2=re.findall("fansub\=(.*?)\&",u)
		if len(fansub2):
			fansub = fansub2[0]
		elif fansub is None:
			fansub="Varsayilan"

		return_links(name,up,uphash,fansub,domain+u)	
		
def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("anime"): return
	is_serie=i["mediatype"]==ump.defs.MT_EPISODE

	names=ump.getnames(0,False)

	page=None
	animes=re.findall('<a href="(.*?)" class="btn".*?title="(.*?)">',ump.get_page(domain+"/icerik/tamliste",encoding))
	for name in names:
		ump.add_log("turkanimetv is searching %s" % name)
		for anime in animes:
			if ump.is_same(anime[1],name):
				page=ump.get_page(domain+anime[0],encoding)
				myear=re.findall('<a href="anime-yili/([0-9]{4})"',page)
				if not (len(myear) and int(myear[0])==i["year"]):
					page=None
				else:
					break
		if page: break

	if page is None:	
		ump.add_log("turkanimetv can't find any links for %s"%name)
		return None
	
	url=re.findall('"(icerik/bolumler.*?)"',page)[0]

	if is_serie:
		bolumler=re.findall('<a href="(.*?)" class="btn".*?title=".*?([0-9]*?)\..*?">',ump.get_page(domain+url,encoding))
		url=None
		for bolum in bolumler:
			try:
				bid=int(bolum[1])
			except:
				continue
			if bid == i["absolute_number"]:
				ump.add_log("turkanimetv matched episode %dx%d:%s" % (i["season"],i["episode"],bid))
				url=bolum[0]
				break
	else:
		url=re.findall('<a href="(.*?)" class="btn"',ump.get_page(domain+url,encoding))
		if len(url)==1:
			url=url[0]
			ump.add_log("turkanimetv matched %s" % unidecode(anime[1]))
		else:
			url=None

	if url is None:	
		ump.add_log("turkanimetv can't find any links for %s"%name)
		return None
	if is_serie:
		mname="%s %sx%s %s "%(i["tvshowtitle"],i["season"],i["absolute_number"],i["title"])
	else:
		mname=i["title"]
	spage=ump.get_page(domain+url,encoding)
	fansubs=re.findall("'#video','(.*?)\&fansub=(.*?)&giris\=",spage)
	if not len(fansubs):
		fansubs=[(spage,None)]
	for fansub in fansubs:
		scrape_moviepage(fansub[0],fansub[1],mname)
	if len(fansubs)==0:
		scrape_moviepage(url,"Varsayilan",mname)