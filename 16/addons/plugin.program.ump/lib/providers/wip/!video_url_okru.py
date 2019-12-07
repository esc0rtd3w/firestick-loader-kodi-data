import json
from xml.dom import minidom

def run(hash,ump,referer=None):
	if isinstance(hash,dict):
		return hash
	else:
		src = ump.get_page("http://ok.ru/dk?cmd=videoPlayerMetadata&mid="+hash,"utf8",referer=referer)
		js=json.loads(src)
		videos=js["videos"]
		res=minidom.parseString(js["metadataEmbedded"])
		opts={}
		#for rep in res.getElementsByTagName("Representation"):
		#	for mirror in rep.getElementsByTagName("BaseURL"):
		#		opts[rep.getAttribute("height")]=mirror.lastChild.data.replace("&amp;","&").replace("https","http")
		#print opts
		#return opts
		opts={}
		for video in videos:
			if not video["disallowed"]:
				opts[video["name"]]={"url":video["url"],"referer":"https://ok.ru/videoembed/%s?wmode=opaque"%hash,"user-agent":ump.ua}
		return opts