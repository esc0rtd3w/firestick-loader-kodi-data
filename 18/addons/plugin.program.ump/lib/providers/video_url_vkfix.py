import re

import video_url_vk


def run(hash,ump,referer=None):
	src=ump.get_page(hash.replace("amp;",""),"utf-8")
	src=src.replace("'+'","")
	iframe=re.findall('location.href = "(.*?)"',src)
	src=ump.get_page(iframe[0],"utf-8")
	oid=re.findall("'([0-9]*?)' \+ param\[6\]",src)
	video_id=re.findall("'([0-9]*?)' \+ param\[7\]",src)
	embed_hash=re.findall("'([A-z0-9]*?)' \+ param\[8\]",src)
	u="https://api.vk.com/method/video.getEmbed?oid="+oid[0]+"&video_id="+video_id[0]+"&embed_hash="+embed_hash[0]
	return video_url_vk.run(u,ump)