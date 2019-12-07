domain="http://www.icefilms.info"
encoding="utf-8"
/search.php?q=matrix+reloaded&x=0&y=0
def run(ump):
	i=ump.info
	#only work with imdbid
	if not i["code"][:2]=="tt":
		return None

	is_serie="tvshowtitle" in i.keys() and not i["tvshowtitle"].replace(" ","") == ""
	if is_serie:
		orgname=i["tvshowtitle"]
		altnames=i["tvshowalias"].split("|")
	else:
		orgname=i["title"]
		altnames=i["originaltitle"].split("|")
	
	for k in range(len(altnames)):
		if altnames[k]=="":
			altnames.pop(k)
	
	names=[orgname]
	names.extend(altnames)
	

	#match names with imdbid
	found=False
	for name in names:
		if found:
			break
		ump.add_log("icefilms is searching %s"%name)
		q={"q":name,"x":0,"y":0}
		search=ump.get_page(domain+"/search.php",encoding,query=q)

		vidids=re.findall("href='/ip\.php\?v\=([0-9]*?)\&'",search)
		
		for vidid in vidids:
			link="/ip.php?v=%s&"%vidid
			page=ump.get_page(link,encoding)
			imdbid=re.findall('/(tt[0-9]*?)/"'page)
			if len(imdbid)<1:
				continue
			else:
				if i["code"]==imdbid[0]:
					ump.add_log("icefilms matched %s with imdbid %s"%(name,i["code"]))
					found=True
					matchid=vidid
					break

	if not found:
		ump.add_log("icefilms can't match %s"%name)
		return None

	
	#find links
	mirrors=ump.get_page("%s/membersonly/components/com_iceplayer/video.php?vid=%s"%(domain,matchid))



		
			
