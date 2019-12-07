timeout=60*60*24
tunnel=("redmp3",)
def run(hash,ump,referer=None):
	u=ump.absuri("http://redmp3.su",hash)
	while True:
		u=u.replace("&amp;","&")
		if not "&amp;" in u: break
	try:
		ump.get_page(u,None,referer=referer,head=True)
	except:
		ump.add_log("Redmp3 is geo-blocked please use TOR or proxy")
		return
	return {"url":{"url":u,"referer":referer}}