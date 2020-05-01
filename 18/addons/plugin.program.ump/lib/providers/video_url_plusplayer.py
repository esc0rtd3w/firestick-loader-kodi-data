import re


def run(hash,ump,referer=None):
	src=ump.get_page("http://720pizle.com/player/plusplayer.asp?v="+hash,"iso-8859-9",referer=referer)
	opts={}
	partlar=re.findall('video="(.*?)" id="(.*?)"',src)
	for part in partlar:
		opts[part[1]]="http://webteizle.org"+part[0]
	return opts