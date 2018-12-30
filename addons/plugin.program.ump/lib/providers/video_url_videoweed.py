import re
import urlparse


def run(hash,ump,referer=None):
	src=ump.get_page("http://www.bitvid.sx/file/"+hash,"utf-8")
	sk=re.findall('<input type="hidden" name="stepkey" value="(.*?)">',src)[0]
	src=ump.get_page("http://www.bitvid.sx/file/"+hash,"utf-8",data={"stepkey":sk,"submit":"submit"},referer="http://www.bitvid.sx/file/"+hash)
	domain=re.findall('flashvars.domain="(.*?)"',src)
	file=re.findall('flashvars.file="(.*?)"',src)
	key=re.findall('flashvars.filekey="(.*?)"',src)
	url=domain[0]+"/api/player.api.php"
	data={"file":file[0],"key":key}
	src=ump.get_page(url,"utf-8",query=data)
	dic=urlparse.parse_qs(src)
	video={"url":dic.get("url")[0],"referer":dic.get("site_url")[0]}
	return video