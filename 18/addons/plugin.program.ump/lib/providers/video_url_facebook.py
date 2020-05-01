import re


def run(hash,ump,referer=None):
	src = ump.get_page(hash,"utf8",referer=referer)
	vids=re.findall('(...)_src_no_ratelimit:"(.*?)"',src)
	return dict(vids)