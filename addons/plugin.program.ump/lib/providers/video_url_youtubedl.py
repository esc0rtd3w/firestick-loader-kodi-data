# -*- coding: utf-8 -*-
from third import youtube_dl

timeout=60*5
def run(hash,ump,referer=""):
	ydl = youtube_dl.YoutubeDL({'format': 'bestaudio+bestvideo/best',"quiet":True,"nocheckcertificate":True})

	with ydl:
		result = ydl.extract_info(hash,	download=False)
	
	dict={}
	if 'entries' in result:
		# Can be a playlist or a list of videos
		for i,res in enumerate(result['entries']):
			dict[i]=res["url"]
	else:
		# Just a video
		dict["video"] = result["url"]

	return dict