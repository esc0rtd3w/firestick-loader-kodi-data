domain="https://mobile.twitter.com/"
user="boogiepy"
encoding="utf-8"
import re

def run(ump):
	if ump.page=="root":
		page=ump.get_page(domain+user,encoding)
		tweets=re.findall('<div class="Tweet-text.*?">(.*?)</div',page,re.DOTALL)
		ttimes=re.findall('<time datetime="(.*?)"',page)
		if not len(tweets):tweets=re.findall('<div class="Tweet-body">(.*?)</div"',page)
		text=""
		for tweet in zip(ttimes,tweets):
			body=re.sub("<.*?>","",tweet[1]).encode("ascii","replace").replace("\n\n","\n")
			text+="[B][COLOR blue]%s[/COLOR] tweeted @ %s :[/B] \r\n %s \r\n"%(user,tweet[0],body)
		ump.view_text("Follow '%s' at twitter"%user,text)