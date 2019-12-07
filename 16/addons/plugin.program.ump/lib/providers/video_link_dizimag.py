import json
import re
from urllib2 import HTTPError


encoding="utf-8"
domain = 'http://dizimag.co'
version = 2


def run(ump):
	globals()['ump'] = ump
	i=ump.info
	if not ump.subscribe("tvshow"): return
	names=ump.getnames()
	ump.add_log("dizimag is searching %s"%names[0])	
	page=ump.get_page(domain+"/insert/d16.js",encoding)
	series=json.loads(page[9:-1].replace('{d:"','{"d":"').replace('",s:"','","s":"'))

	for name in names:
		for serie in series:
			l=serie["s"]+"/"
			t=serie["d"]
			if ump.is_same(t,name):
				url=domain+l+str(i["season"])+"-sezon-"+str(i["episode"])+"-bolum-izle-dizi"
				try:
					epage=ump.get_page(url+".html",encoding)
				except HTTPError, err:
					if err.code == 404:
						ump.add_log("dizimag can't match %s %dx%d %s"%(i["tvshowtitle"],i["season"],i["episode"],i["title"]))
						return None
				ump.add_log("dizimag matched %s %dx%d %s"%(i["tvshowtitle"],i["season"],i["episode"],i["title"]))
				if version==2:
					ids=re.findall("kaynakdegis\('([0-9]*?)'",epage)
					for id in set(ids):
						if id.isnumeric():
							try:
								data=ump.get_page(domain+"/service/partikule",encoding,data={"id":id},header={"X-Requested-With":"XMLHttpRequest"})
							except:
								ump.add_log("dizimag can't get video id:%s"%id)
								continue
						else:
							continue
						videos=json.loads(data)
						vlink={}
						if videos.get("player_type","")=="altyazili" and not videos.get("altyazitype","")=="noalt":prefix=""
						else:prefix="[HS:TR]"
						for k in range(1,7):
							if isinstance(videos,dict) and "videolink%d"%k in videos.keys():
								vlink[videos["videokalite%d"%k]]=videos["videolink%d"%k]
						parts=[{"url_provider_name":"google", "url_provider_hash":vlink}]
						ump.add_mirror(parts,"%s%s %dx%d %s" % (prefix,i["tvshowtitle"],i["season"],i["episode"],i["title"]))	

				#dizimag web site is on beta stage an subject to change, they keep below algo for videos but they dont use it. so lets keep below code for now
				if version==1:
					sources=re.findall("Change_Source\(([0-9]*?),'(.*?)'\)",epage)
					for source in sources:
						idd,pname=source
						serie1=re.findall('var serie1 = "(.*?)";',epage)[0]
						episode1=re.findall('var episode1 = "(.*?)";',epage)[0]
						vid1=re.findall('var vid1 = "(.*?)";',epage)[0]
						n=0
						if pname=="Roosy":
							codep=ump.get_page(domain+"/insert/js15.js",encoding)
							code=re.findall("\?type=Roosy\&a=(.*?)\&b",codep)[0]
							query={"type":pname,"a":code,"b":"3"+str(idd),"s":serie1,"e":episode1}
							script=ump.get_page(domain+"/service/vdmg",encoding,query=query)
						else:
							data={"i":idd,"n":pname,"p":n}
							js=json.loads(ump.get_page(domain+"/service/givevideo",encoding,data=data,referer=url,header={"X-Requested-With":"XMLHttpRequest"}))
							tur=js["p"]["tur"]
							code=js["p"]["c"]
							is_single_part=js["tekpart"]
							query={"type":tur,"a":code,"b":"1"+str(idd),"s":serie1,"episode":episode1}
							script=ump.get_page(domain+'/service/idmg',encoding,query=query)
						vids=re.findall('file:"(.*?)",label: "(.*?)"',script)
						vlink={}
						if len(vids)>0:
							method=1
						else:
							method=2
							iframe=re.findall('<iframe src="(.*?)"',script)
							if len(iframe)>0:
								vids=re.findall('"file": "(.*?)", "label": "(.*?)"',ump.get_page(iframe[0],encoding))
						if len(vids)>0:
							for vid in vids:
								if method==1:
									chrs=vid[0].split("\\x")
									vidurl="".join(chr(int(x,16)) for x in chrs if not x=="")
									if "//217.20.157.199" in vidurl:
										upname="okru"
									else:
										upname="google"
								else:
									upname="google"
									vidurl=vid[0]
								vlink[vid[1]]=vidurl
							parts=[{"url_provider_name":upname, "url_provider_hash":vlink}]
							ump.add_mirror(parts,"%s %dx%d %s" % (i["tvshowtitle"],i["season"],i["episode"],i["title"]))	
				return None
	ump.add_log("dizimag can't match %s %dx%d %s"%(i["tvshowtitle"],i["season"],i["episode"],i["title"]))