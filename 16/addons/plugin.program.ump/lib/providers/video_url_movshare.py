import re
import urllib
import urlparse


def run(hash,ump,referer=None):
	url="http://www.wholecloud.net/video/"+hash
	src=ump.get_page(url,"utf8")
	key=re.findall('<input type="hidden" name="stepkey" value="(.*?)">',src)
	src=ump.get_page(url,"utf8",data={"stepkey":key[0],"submit":"submit"})
	vid=re.findall('<source src="(.*?)"',src)
	if len(vid):
		vid=vid[0]
	else:
		domain=re.findall('flashvars.domain="(.*?)"',src)
		file=re.findall('flashvars.file="(.*?)"',src)
		key=re.findall('flashvars.filekey="(.*?)"',src)
		url=domain[0]+"/api/player.api.php"
		data={"file":file[0],"key":key[0]}
		for i in range(10):
			#find an available cdn
			src=ump.get_page(url,"utf-8",query=data,referer=url)
			dic=urlparse.parse_qs(src)
			try:
				ump.get_page(dic.get("url")[0],None,head=True,referer=dic.get("site_url")[0])
			except Exception,e:
				data["errorUrl"]=dic.get("url")[0]
				data["errorCode"]=404
				continue
			break
		vid=dic.get("url")[0]
	return {"video":{"url":vid,"referer":url}}