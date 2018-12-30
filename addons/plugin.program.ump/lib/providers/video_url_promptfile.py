import re

domain = "http://www.promptfile.com/"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
def run(hash, ump, referer=None):
	src = ump.get_page(domain + "l/" + hash, "utf8", referer=referer, header=header)
	validator = re.findall('id="chash" name  =  "(.*?)" value="(.*?)"', src)
	if len(validator):
		pf = re.findall('val\("(.*?)"\+', src)
		data = {validator[0][0]:pf[0] + validator[0][1]}
		src = ump.get_page(domain + "l/" + hash, "utf8", data=data, referer=domain + "l/" + hash, header=header)
	files = re.findall('src:\s*"(.*?)"', src, re.DOTALL)
	if not len(files):
		files = re.findall("url: '(.*?)'", src)
	return {"video":{"url":files[0], "referer":domain + "l/" + hash}}
