import re
import urlparse

from third.unidecode import  unidecode


domain="http://www.animeram.co"
encoding=None

def codify(url):
	if url.startswith("//"):url="http:"+url
	uri = urlparse.urlparse(url)
	prv=uri.hostname.split(".")[-2]
	path=uri.path.replace(" ","")
	if prv in ["movshare"]:
		return prv,uri.query.split("=")[1].replace("&","")

	if prv in ["auengine"]:
		if "embed.php" in path:
			return prv,urlparse.parse_qs(uri.query).get("file",[""])[0]

	if prv in ["mp4upload", "videonest"]:
		return prv,re.findall("embed-(.+?)\.html", path)[0]
	
	if prv in ["videoweed","novamov"]:
		return prv,urlparse.parse_qs(uri.query).get("v",[""])[0]

	if prv in ["animebam"]:
		return "acercloud",url
	
	if prv in ["auengine","yourupload"]:
		return prv,uri.path.split("/")[-1]

	return None,None


def google(names):
	ump.add_log("animeram is searching %s on %s"%(names[0],"google"))
	results=ump.web_search('site:%s %s "Alternative Title:"'%(domain, names[0]))
	if not results is None:
		for result in results:
			page=ump.get_page(result,encoding)
			info = re.findall("<td\sclass=\"header\"><label>(.+?)</label></td>\s<td\sclass=\"content1\">(.+?)</td>", page, re.DOTALL)
			for info_title, info_value in info:
				if "Title:" in info_title:
					orgname=info_value
					break

			for info_title, info_value in info:
				if "Alternative Title:" in info_title:
					names = [orgname]
					if info_value is not "-":
						#TODO: implement after such found.
						raise
	return False

def searchsite(names):
	found=False
	for name in names:
		if found:break
		ump.add_log("animeram is searching %s on %s"%(unidecode(name),"sitelist"))
		page=ump.get_page(domain+"/search",encoding,query={"search":name},referer=domain)
		ress=re.findall('<a href="/series(/.*?)" class="mse">(.*?)</div></a>',page)
		if len(ress):
			for mlink,res in ress:
				if found:break
				mnames=re.findall("<h2>(.*?)</h2>",res)
				malts=re.findall("<div>Alt Titles \: (.*?)</div>",res)
				mnames.extend(malts)
				for mname in mnames:
					if ump.is_same(mname,name):
						ump.add_log("animeram found %s"%name)
						found=mlink
						break
	return found

def sitelist(names):
	ump.add_log("animeram is searching %s on %s"%(names[0],"sitelist"))
	
	sitenames=ump.get_page(domain+"/anime-list-all",encoding)
	sitenames = re.findall("<a\shref=\"%s/([-\w\s\d]+?)/\".+?rel=\"(\d+)\".+?>(.+?)</a>" % domain, sitenames, re.DOTALL)
	for name in names:
		for sitename in sitenames:
			if ump.is_same(sitename[2],name,strict=True):
				ump.add_log("animeram found %s"%name)
				return sitename[0]
	return False

def add_mirror(page,mname):
	iframes=re.findall('<div class="tab-pane active"><iframe src="(.*?)"',page)
	for iframe in iframes:
		prv,hash=codify(iframe)
		if hash is None: 
			ump.add_log("animeram cant decode %s"%iframe)
			continue
		parts=[{"url_provider_name":prv, "url_provider_hash":hash,"referer":iframe}]
		ump.add_mirror(parts,mname)

def run(ump):
	globals()['ump'] = ump
	if not ump.subscribe("anime"): return
	i=ump.info
	names=ump.getnames(orgfirst=False)
	is_serie=i["mediatype"]==ump.defs.MT_EPISODE

	#page=(searchsite(names) or google(names))
	#google has not cached enough
	found=searchsite(names)

	if not found:
		ump.add_log("animeram can't find %s"%names[0])
		return None

	if is_serie:
		epinum=i["absolute_number"]
	else:
		epinum=1
	

	base_url = "%s%s/%d" % (domain, found, epinum)
	epipage=ump.get_page(base_url, encoding)
	if "Error: Episode not found" in epipage:
		if is_serie:
			epipage=ump.get_page(found+"/%d"%i["episode"],encoding)
			if "Error: Episode not found" in epipage:
				ump.add_log("animeram can't find episode %d of %s"%(epinum,names[0]))
				return None
	
	found=found+"/%d"%i["episode"]
	if is_serie:
		mname=i["title"]
	else:
		mname=names[0]
	issub=re.findall('<a href="\#"><span class="btn\-xs btn\-(.*?)">',epipage)
	if len(issub) and "subbed" in issub[0]:
		prefix="[HS:EN]"
	else:
		prefix="[D:EN]"
	add_mirror(epipage,prefix+mname)

	for page,issub in re.findall('<li><a href="('+found+'/[0-9]*?)"><span class="btn-xs btn-(.*?)">',epipage):
		if "subbed" in issub:
			prefix="[HS:EN]"
		else:
			prefix="[D:EN]"
		add_mirror(ump.get_page(domain+page,encoding,referer=base_url),prefix+mname)