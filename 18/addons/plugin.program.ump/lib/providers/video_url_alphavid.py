import re
import urlparse

domain="http://www.alphavid.to/"

def run(hash,ump,referer=None):
	src = ump.get_page(domain+"embed.php?id="+hash,"utf8",referer=referer)
	key = re.findall('key: "(.*?)"',src)[0]
	page=ump.get_page("http://www.alphavid.to/api/player.api.php","utf-8",query={"key":key,"file":hash})
	return {"video":urlparse.parse_qs(page)["url"][0]}