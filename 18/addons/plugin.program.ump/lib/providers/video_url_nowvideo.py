import re
import urlparse


dmn="http://www.nowvideo.sx"
def run(hash,ump,referer=None):
	link=dmn+"/video/"+hash
	src=ump.get_page(link,"utf-8",referer=referer)
	stepkey=re.findall('name="stepkey" value="(.*?)"',src)
	if len(stepkey)>0:
		src=ump.get_page(link,"utf-8",data={"stepkey":stepkey[0],"submit":"submit"},referer=link)
		sources=re.findall('<source src="(.*?)"',src)
		if len(sources):
			video=sources[0]
		if not len(sources):
			domain=re.findall('flashvars.domain="(.*?)"',src)
			file=re.findall('flashvars.file="(.*?)"',src)
			key=re.findall('var fkzd="(.*?)"',src)
			url=domain[0]+"/api/player.api.php"
			data={"file":file[0],"key":key[0]}
			for i in range(10):
				#find an available cdn
				src=ump.get_page(url,"utf-8",query=data,referer=link)
				dic=urlparse.parse_qs(src)
				try:
					ump.get_page(dic.get("url")[0],None,head=True,referer=dic.get("site_url")[0])
				except Exception,e:
					data["errorUrl"]=dic.get("url")[0]
					data["errorCode"]=404
					continue
				break
			video={"url":dic.get("url")[0]+"?start=0","referer":dic.get("site_url")[0]}
		return {"video":video}