import re


def run(hash,ump,referer=None):
	iframe=ump.get_page(hash,"utf-8",referer=referer)
	files=re.findall('file: "(.*?)", label: "(.*?)"',iframe)
	mirrors={}
	for file in files:
		mirrors[file[1]]=file[0]
	return mirrors