import re
from urllib2 import HTTPError


domain="http://www.animejolt.org"
encoding="utf-8"

def run(ump):
	globals()['ump'] = ump
	if not ump.subscribe("anime"): return
	i=ump.info
	names=ump.getnames(orgfirst=False)
	is_serie=ump.info["mediatype"]==ump.defs.MT_EPISODE
	found=False
	for name in names:
		if found:
			break
		ump.add_log("animejolt is searching %s on sitesearch"%name)
		q={"search":name}
		page=ump.get_page(domain+"/search",encoding,query=q)
		sitenames=re.findall('<a href="/series(/.*?)" class="mse".*?<div class="first"><h2>(.*?)</h2><p class="infoami"><div>Episodes: ([0-9]*?)</div><div>Alt Titles \: (.*?)</div>',page)
		if len(sitenames)<1:
			continue
		for sitename in sitenames:
			if found:
				break
			if len(sitename)<3:
				continue
			matchnames=sitename[3].split(", ")
			matchnames.append(sitename[1])
			for matchname in matchnames:
				matchname=matchname.replace("(TV)","")
				if ump.is_same(name,matchname,strict=True) and (is_serie and not int(sitename[2])==1 or not is_serie and int(sitename[2])==1):
					found=sitename[0]
					break
	if not found:
		page=ump.get_page(domain+"/series",encoding)
		series=re.findall('<a href="(.*?)" class="anm_det_pop egg-whole">(.*?)\n',page)
		for name in names:
			ump.add_log("animejolt is searching %s on sitelist"%name)
			for serie in series:
				sname=serie[1].split("(")[0]
				if ump.is_same(sname,name,strict=True):
					found=serie[0]
				if found:break
			if found:break

	
	if not found:
		ump.add_log("animejolt can't find %s"%names[0])
		return None
	else:
		ump.add_log("animejolt matched %s"%names[0])
		if is_serie:
			u=domain+found+"-episode-%d"%i["absolute_number"]
		else:
			u=domain+found+"-episode-1"
		
		try:
			res=ump.get_page(u,encoding)
		except HTTPError:
			ump.add_log("animejolt: episode %d does not exist for %s"%(i["absolute_number"],name))
			return None

		frames=re.findall('<div id="(sub|dub|raw).*?" class="tab-pane"><iframe src="(.*?)"',res)
		for frame in frames:
			parts=[{"url_provider_name":"acercloud", "url_provider_hash":domain+frame[1],"referer":domain+frame[1]}]
			if frame[0]=="sub":
				prefix="[HS:EN]"
			elif frame[0]=="dub":
				prefix="[D:EN]"
			elif frame[0]=="raw":
				prefix="[D:JP]"
			else:
				prefix=""
			ump.add_mirror(parts,"%s %s"%(prefix,i["title"]))

		if not found:
			ump.add_log("animejolt can't find any links for %s"%i["title"])